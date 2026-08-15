"""Focused regression suite for the reference resolver."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from seat_resolver.catalog import CatalogFormatError, parse_catalog
from seat_resolver.cli import DocumentError, load_config, main
from seat_resolver.conformance import main as conformance_main
from seat_resolver.rules import evaluate_panel, resolve


def catalog_bytes(effective: str = "2099-01-02") -> bytes:
    return (
        "revision: 1\n"
        "date: 2099-01-01\n"
        f"revision_effective_after: {effective}\n"
        "changelog: initial\n"
        "blast_radius: bounded\n"
        "models:\n"
        "  - id: remote-a\n"
        "    lineage: {family: remote-family-a, vendor: remote-vendor-a}\n"
        "    tier: priority\n"
        "    rank: 1\n"
        "    status: current\n"
        "    quorum_eligible: true\n"
        "    cost_class: subscription\n"
        "    escalation_only: false\n"
        "    data_handling: standard\n"
        "    date: 2099-01-01\n"
    ).encode()


class ResolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config, _ = load_config(ROOT / "config.example.json")

    def setUp(self) -> None:
        self.roster = {
            item: {"display": item.upper(), "eligible": True}
            for item in self.config["models"]
        }

    def select(self, size: str, risks=(), absent=(), roster=None):
        return resolve(self.config, size, risks, absent, roster or self.roster)

    def test_small_rule_uses_standing_and_rotation(self) -> None:
        result = self.select("S")
        self.assertEqual(result["final_seats"], ["model-c", "model-a", "model-d"])
        self.assertEqual(result["status"], "GO")

    def test_risk_overrides_every_size(self) -> None:
        expected = ["model-b", "model-c", "model-d", "model-e", "model-y"]
        for size in self.config["sizes"]:
            with self.subTest(size=size):
                result = self.select(size, ("risk-a",))
                self.assertEqual(result["final_seats"], expected)
                self.assertTrue(result["risk_override"])

    def test_risks_are_sorted_and_deduplicated(self) -> None:
        result = self.select("M", ("risk-f", "risk-a", "risk-f"))
        self.assertEqual(result["risk_areas"], ["risk-a", "risk-f"])

    def test_standing_substitution_is_reserved_before_rotation(self) -> None:
        result = self.select("S", absent=("model-c",))
        self.assertEqual(result["substitutions"], [{"absent": "model-c", "replacement": "model-d"}])
        self.assertEqual(result["panel"], ["model-c", "model-a", "model-b"])
        self.assertEqual(result["final_seats"], ["model-d", "model-a", "model-b"])

    def test_second_standing_substitute_is_used(self) -> None:
        result = self.select("S", absent=("model-c", "model-d"))
        self.assertEqual(result["substitutions"], [{"absent": "model-c", "replacement": "model-b"}])
        self.assertEqual(result["final_seats"], ["model-b", "model-a", "model-x"])

    def test_rotation_shortfall_waits_without_named_missing(self) -> None:
        result = self.select("M", absent=("model-a", "model-d", "model-b"))
        self.assertEqual(result["final_seats"], ["model-c", "model-x"])
        self.assertEqual(result["missing"], [])
        self.assertEqual(result["rotation_shortfall"], 1)
        self.assertEqual(result["status"], "SEAT-WAIT")

    def test_missing_standing_and_shortfall_coexist(self) -> None:
        result = self.select("M", absent=("model-c", "model-d", "model-b", "model-a"))
        self.assertEqual(result["missing"], ["model-c"])
        self.assertEqual(result["rotation_shortfall"], 1)
        self.assertEqual(result["final_seats"], ["model-x"])

    def test_roster_ineligibility_matches_explicit_absence(self) -> None:
        roster = copy.deepcopy(self.roster)
        roster["model-a"]["eligible"] = False
        self.assertEqual(self.select("S", roster=roster), self.select("S", absent=("model-a",)))

    def test_omitted_configured_model_is_unavailable(self) -> None:
        roster = copy.deepcopy(self.roster)
        del roster["model-a"]
        result = self.select("S", roster=roster)
        self.assertIn("model-a", result["unavailable"])
        self.assertEqual(result["status"], "GO")

    def test_large_one_substitution(self) -> None:
        result = self.select("L", absent=("model-b",))
        self.assertEqual(result["substitutions"], [{"absent": "model-b", "replacement": "model-d"}])
        self.assertEqual(result["final_seats"], ["model-a", "model-d", "model-c"])

    def test_large_substitution_cap_is_enforced(self) -> None:
        result = self.select("H", absent=("model-a", "model-b"))
        self.assertEqual(len(result["substitutions"]), 1)
        self.assertEqual(result["missing"], ["model-b"])
        self.assertEqual(result["status"], "SEAT-WAIT")

    def test_risk_strategy_has_no_substitution(self) -> None:
        result = self.select("S", risks=("risk-a",), absent=("model-b",))
        self.assertEqual(result["substitutions"], [])
        self.assertEqual(result["missing"], ["model-b"])

    def test_same_family_seat_depends_on_configured_authorization(self) -> None:
        result = self.select("L", risks=("risk-a",))
        self.assertEqual(result["same_family_seats"], ["model-y"])
        self.assertEqual(self.select("L")["same_family_seats"], [])

        config = copy.deepcopy(self.config)
        config["same_family_authorization"]["seats"] = []
        blocked = resolve(config, "L", ("risk-a",), (), self.roster)
        self.assertEqual(blocked["status"], "SEAT-WAIT")
        self.assertIn({"model": "model-y", "reason": "same-family-unauthorized"}, blocked["uncountable"])

    def test_writer_model_is_never_counted(self) -> None:
        config = copy.deepcopy(self.config)
        config["panel_strategies"]["large"]["panel"][0] = "model-w"
        result = resolve(config, "L", (), (), self.roster)
        self.assertEqual(result["status"], "SEAT-WAIT")
        self.assertNotIn("model-w", result["final_seats"])
        self.assertIn({"model": "model-w", "reason": "writer-model"}, result["uncountable"])

    def test_machine_path_skips_correlated_candidate_and_scans_on(self) -> None:
        config = copy.deepcopy(self.config)
        config["model_lineages"]["model-a"] = "family-c"
        result = resolve(config, "S", (), (), self.roster)
        self.assertEqual(result["final_seats"], ["model-c", "model-d", "model-b"])
        self.assertIn({"model": "model-a", "reason": "correlated-lineage-unrecorded"}, result["uncountable"])

    def test_named_panel_correlated_seat_waits_without_record(self) -> None:
        config = copy.deepcopy(self.config)
        config["model_lineages"]["model-c"] = "family-a"
        result = resolve(config, "L", (), (), self.roster)
        self.assertEqual(result["status"], "SEAT-WAIT")
        self.assertIn("model-c", result["missing"])
        self.assertEqual(result["applied_exception_records"], [])

    def test_machine_fixed_path_replaces_an_uncountable_candidate(self) -> None:
        config = copy.deepcopy(self.config)
        config["panel_strategies"]["large"]["selection_path"] = "machine"
        config["model_lineages"]["model-c"] = "family-a"
        result = resolve(config, "L", (), (), self.roster)
        self.assertEqual(result["status"], "GO")
        self.assertEqual(result["final_seats"], ["model-a", "model-b", "model-d"])
        self.assertEqual(result["substitutions"], [{"absent": "model-c", "replacement": "model-d"}])

    def test_named_and_machine_paths_apply_the_same_scoped_exception(self) -> None:
        for strategy_name, size in (("large", "L"), ("small", "S")):
            with self.subTest(strategy=strategy_name):
                config = copy.deepcopy(self.config)
                if strategy_name == "large":
                    pair = ["model-a", "model-c"]
                    config["model_lineages"]["model-c"] = "family-a"
                else:
                    pair = ["model-c", "model-a"]
                    config["model_lineages"]["model-a"] = "family-c"
                record = {
                    "scope": [strategy_name], "pair": pair,
                    "reason": "bounded record", "approved_by": "member-a",
                    "date": "2026-08-16", "writer_condition": "model-w",
                }
                config["correlated_seat_exceptions"].append(record)
                result = resolve(config, size, (), (), self.roster)
                self.assertEqual(result["status"], "GO")
                self.assertIn(record, result["applied_exception_records"])

    def test_downgrade_fills_shortfall_only_when_lineages_are_insufficient(self) -> None:
        roster = {item: {"eligible": item in {"model-a", "model-b"}} for item in self.config["models"]}
        result = self.select("L", roster=roster)
        self.assertEqual(result["status"], "GO")
        self.assertEqual(result["final_seats"], ["model-a", "model-b", "model-a"])
        self.assertEqual(
            result["seat_instances"],
            [
                {"model": "model-a", "agent": "agent-a-1", "kind": "model"},
                {"model": "model-b", "agent": None, "kind": "model"},
                {"model": "model-a", "agent": "agent-a-2", "kind": "downgrade"},
            ],
        )
        self.assertEqual(result["applied_downgrade_records"], self.config["downgrade_records"])

        roster["model-e"]["eligible"] = True
        blocked = self.select("L", roster=roster)
        self.assertEqual(blocked["status"], "SEAT-WAIT")
        self.assertEqual(blocked["applied_downgrade_records"], [])

    def test_excluded_model_is_never_selected(self) -> None:
        config = copy.deepcopy(self.config)
        config["panel_strategies"]["large"]["panel"][0] = "model-z"
        result = resolve(config, "L", (), (), self.roster)
        self.assertNotIn("model-z", result["final_seats"])
        self.assertEqual(result["substitutions"], [{"absent": "model-z", "replacement": "model-d"}])

    def test_four_seat_risk_panel_needs_no_code_change(self) -> None:
        config = copy.deepcopy(self.config)
        strategy = config["panel_strategies"]["risk"]
        strategy["panel"] = strategy["panel"][:4]
        strategy["required"] = 4
        result = resolve(config, "S", ("risk-a",), (), self.roster)
        self.assertEqual(result["required"], 4)
        self.assertEqual(len(result["final_seats"]), 4)
        self.assertEqual(result["status"], "GO")


class ConfigurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = json.loads((ROOT / "config.example.json").read_text(encoding="utf-8"))

    def load(self, payload: dict) -> dict:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            return load_config(path)[0]

    def test_empty_floor3_sizes_do_not_require_pre_effect_strategy(self) -> None:
        payload = copy.deepcopy(self.base)
        payload["floor3"]["sizes"] = []
        del payload["floor3"]["pre_effect_strategy"]
        loaded = self.load(payload)
        self.assertEqual(loaded["floor3"], {"sizes": [], "effective": True})

    def test_floor3_effective_remains_required_and_boolean(self) -> None:
        mutations = []
        missing = copy.deepcopy(self.base)
        missing["floor3"]["sizes"] = []
        del missing["floor3"]["pre_effect_strategy"]
        del missing["floor3"]["effective"]
        mutations.append(missing)
        for value in (None, 1, "true"):
            payload = copy.deepcopy(self.base)
            payload["floor3"]["sizes"] = []
            del payload["floor3"]["pre_effect_strategy"]
            payload["floor3"]["effective"] = value
            mutations.append(payload)
        for index, payload in enumerate(mutations):
            with self.subTest(index=index):
                with self.assertRaises(DocumentError):
                    self.load(payload)

    def test_nonempty_floor3_sizes_still_require_a_nonempty_known_strategy(self) -> None:
        mutations = []
        missing = copy.deepcopy(self.base)
        del missing["floor3"]["pre_effect_strategy"]
        mutations.append(missing)
        empty = copy.deepcopy(self.base)
        empty["floor3"]["pre_effect_strategy"] = ""
        mutations.append(empty)
        unknown = copy.deepcopy(self.base)
        unknown["floor3"]["pre_effect_strategy"] = "unknown"
        mutations.append(unknown)
        for index, payload in enumerate(mutations):
            with self.subTest(index=index):
                with self.assertRaises(DocumentError):
                    self.load(payload)

    def test_strategy_references_to_excluded_models_remain_invalid(self) -> None:
        payload = copy.deepcopy(self.base)
        payload["floor3"]["sizes"] = []
        del payload["floor3"]["pre_effect_strategy"]
        payload["panel_strategies"]["large"]["panel"][0] = "model-z"
        with self.assertRaisesRegex(DocumentError, "excluded model"):
            self.load(payload)


class CatalogTests(unittest.TestCase):
    def test_valid_catalog_parses(self) -> None:
        value = parse_catalog(catalog_bytes())
        self.assertEqual(value["revision_effective_after"], "2099-01-02")

    def test_bom_is_rejected(self) -> None:
        with self.assertRaisesRegex(CatalogFormatError, "BOM"):
            parse_catalog(b"\xef\xbb\xbf" + catalog_bytes())

    def test_tabs_are_rejected(self) -> None:
        with self.assertRaisesRegex(CatalogFormatError, "tabs"):
            parse_catalog(catalog_bytes().replace(b"revision: 1", b"revision:\t1"))

    def test_duplicate_top_level_key_is_rejected(self) -> None:
        with self.assertRaisesRegex(CatalogFormatError, "duplicate key"):
            parse_catalog(catalog_bytes().replace(b"revision: 1", b"revision: 1\nrevision: 2"))

    def test_missing_effective_field_is_rejected(self) -> None:
        line = b"revision_effective_after: 2099-01-02\n"
        with self.assertRaisesRegex(CatalogFormatError, "revision_effective_after"):
            parse_catalog(catalog_bytes().replace(line, b""))

    def test_duplicate_effective_field_is_rejected(self) -> None:
        line = b"revision_effective_after: 2099-01-02\n"
        with self.assertRaisesRegex(CatalogFormatError, "duplicate key"):
            parse_catalog(catalog_bytes().replace(line, line + line))

    def test_nested_effective_field_is_rejected(self) -> None:
        mutated = catalog_bytes().replace(
            b"    lineage: {family: remote-family-a, vendor: remote-vendor-a}\n",
            b"    revision_effective_after: 2099-01-02\n",
        )
        with self.assertRaises(CatalogFormatError):
            parse_catalog(mutated)

    def test_anchor_alias_and_tag_are_rejected(self) -> None:
        for marker in (b"&named", b"*named", b"!kind"):
            with self.subTest(marker=marker):
                mutated = catalog_bytes().replace(b"changelog: initial", b"changelog: " + marker)
                with self.assertRaisesRegex(CatalogFormatError, "unsupported"):
                    parse_catalog(mutated)

    def test_malformed_date_and_reversed_window_are_rejected(self) -> None:
        with self.assertRaisesRegex(CatalogFormatError, "valid ISO"):
            parse_catalog(catalog_bytes().replace(b"2099-01-02", b"2099-02-30"))
        with self.assertRaisesRegex(CatalogFormatError, "on or after"):
            parse_catalog(catalog_bytes("2098-12-31"))

    def test_duplicate_row_key_is_rejected(self) -> None:
        mutated = catalog_bytes().replace(b"    rank: 1\n", b"    rank: 1\n    rank: 2\n")
        with self.assertRaisesRegex(CatalogFormatError, "duplicate key"):
            parse_catalog(mutated)


class CliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.config_path = self.root / "config.json"
        self.config_path.write_bytes((ROOT / "config.example.json").read_bytes())
        self.catalog_path = self.root / "catalog.yaml"
        self.catalog_path.write_bytes(catalog_bytes("2099-01-02"))
        config, _ = load_config(self.config_path)
        self.roster = {
            "roster_version": 1,
            "models": {item: {"eligible": True} for item in config["models"]},
            "catalog": {
                "path": str(self.catalog_path),
                "adopted_digest": hashlib.sha256(self.catalog_path.read_bytes()).hexdigest(),
            },
        }
        self.roster_path = self.root / "roster.json"
        self.write_roster()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_roster(self) -> None:
        self.roster_path.write_text(json.dumps(self.roster), encoding="utf-8")

    def invoke(self, *extra: str, today_value: date = date(2099, 1, 1)):
        output = io.StringIO()
        errors = io.StringIO()
        code = main(
            ("--size", "S", "--config", str(self.config_path), "--roster", str(self.roster_path), *extra),
            stdout=output,
            stderr=errors,
            environ={},
            today=today_value,
        )
        return code, output.getvalue(), errors.getvalue()

    def test_matched_catalog_go_and_frozen_key_order(self) -> None:
        code, output, error = self.invoke()
        self.assertEqual(code, 0, error)
        payload = json.loads(output)
        self.assertEqual(payload["catalog_state"], "matched")
        self.assertEqual(
            list(payload),
            ["size", "risk_areas", "risk_override", "strategy", "selection_path", "required", "panel", "unavailable", "uncountable", "substitutions", "final_seats", "seat_instances", "applied_exception_records", "applied_downgrade_records", "same_family_seats", "writer_assumed", "missing", "rotation_shortfall", "quorum_met", "status", "note", "availability_note", "writer_note", "citations", "roster_path", "config_path", "catalog_digest", "catalog_state", "selection_fn_version", "config_digest", "rules_version"],
        )

    def test_config_digest_hashes_exact_config_bytes(self) -> None:
        code, output, _ = self.invoke()
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output)["config_digest"], hashlib.sha256(self.config_path.read_bytes()).hexdigest())

    def test_grace_is_inclusive_and_preserves_adopted_digest(self) -> None:
        adopted = "0" * 64
        self.roster["catalog"]["adopted_digest"] = adopted
        self.write_roster()
        code, output, error = self.invoke(today_value=date(2099, 1, 2))
        self.assertEqual(code, 0, error)
        payload = json.loads(output)
        self.assertEqual(payload["catalog_state"], "grace")
        self.assertEqual(payload["catalog_digest"], adopted)
        self.assertIn("2099-01-02", payload["note"])

    def test_stale_catalog_is_exit_four(self) -> None:
        self.roster["catalog"]["adopted_digest"] = "0" * 64
        self.write_roster()
        code, output, error = self.invoke(today_value=date(2099, 1, 3))
        self.assertEqual(code, 4)
        self.assertEqual(json.loads(output)["status"], "CATALOG-STALE")
        self.assertIn("window ended", error)

    def test_matching_malformed_catalog_is_still_unreadable(self) -> None:
        self.catalog_path.write_bytes(b"revision:\t1\n")
        self.roster["catalog"]["adopted_digest"] = hashlib.sha256(self.catalog_path.read_bytes()).hexdigest()
        self.write_roster()
        code, output, _ = self.invoke()
        self.assertEqual(code, 4)
        self.assertEqual(json.loads(output)["status"], "CATALOG-UNREADABLE")

    def test_unstamped_example_is_exit_four(self) -> None:
        output = io.StringIO()
        code = main(("--size", "S", "--config", str(ROOT / "config.example.json"), "--roster", str(ROOT / "roster.example.json")), stdout=output, stderr=io.StringIO(), environ={})
        self.assertEqual(code, 4)
        self.assertEqual(json.loads(output.getvalue())["status"], "CATALOG-UNSTAMPED")

    def test_unknown_roster_key_is_exit_three(self) -> None:
        self.roster["models"]["model-unknown"] = {"eligible": True}
        self.write_roster()
        code, output, error = self.invoke()
        self.assertEqual((code, output), (3, ""))
        self.assertIn("unknown roster keys", error)

    def test_invalid_configuration_is_exit_three(self) -> None:
        self.config_path.write_text("{}", encoding="utf-8")
        code, output, error = self.invoke()
        self.assertEqual((code, output), (3, ""))
        self.assertIn("configuration", error)

    def test_unknown_vocabulary_is_exit_two(self) -> None:
        for extra in (("--size", "XX"), ("--risk", "risk-unknown"), ("--absent", "model-unknown")):
            with self.subTest(extra=extra):
                arguments = list(extra)
                if extra[0] == "--size":
                    output, errors = io.StringIO(), io.StringIO()
                    code = main((*extra, "--config", str(self.config_path), "--roster", str(self.roster_path)), stdout=output, stderr=errors, environ={})
                    result = (code, output.getvalue(), errors.getvalue())
                else:
                    result = self.invoke(*arguments)
                self.assertEqual(result[0], 2)

    def test_wait_exit_one_and_text_order(self) -> None:
        code, output, error = self.invoke("--risk", "risk-a", "--absent", "model-b", "--format", "text")
        self.assertEqual(code, 1, error)
        labels = [line.split(":", 1)[0] for line in output.splitlines()]
        self.assertEqual(labels[:6], ["status", "strategy", "selection_path", "seats", "substitutions", "unavailable"])

    def test_malformed_operational_records_are_configuration_errors(self) -> None:
        base = json.loads(self.config_path.read_text(encoding="utf-8"))
        mutations = []
        missing_field = copy.deepcopy(base)
        del missing_field["correlated_seat_exceptions"][0]["writer_condition"]
        mutations.append(missing_field)
        wrong_writer = copy.deepcopy(base)
        wrong_writer["correlated_seat_exceptions"][0]["writer_condition"] = "model-a"
        mutations.append(wrong_writer)
        same_agent = copy.deepcopy(base)
        same_agent["downgrade_records"][0]["agents"] = ["agent-a-1", "agent-a-1"]
        mutations.append(same_agent)
        no_approval = copy.deepcopy(base)
        no_approval["downgrade_records"][0]["owner_approval"] = ""
        mutations.append(no_approval)
        for index, payload in enumerate(mutations):
            with self.subTest(index=index):
                self.config_path.write_text(json.dumps(payload), encoding="utf-8")
                code, output, error = self.invoke()
                self.assertEqual((code, output), (3, ""))
                self.assertIn("document error", error)

    def test_launcher_runs_with_bytecode_disabled(self) -> None:
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "bin" / "seat-resolver"), "--size", "S", "--config", str(self.config_path), "--roster", str(self.roster_path)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


class ConformanceTests(unittest.TestCase):
    def invoke(self, vectors: list[dict]) -> tuple[int, str, str]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "vectors.json"
            path.write_text(json.dumps({"vectors": vectors}), encoding="utf-8")
            output, errors = io.StringIO(), io.StringIO()
            code = conformance_main(
                ("--vectors", str(path), "--config", str(ROOT / "config.example.json")),
                stdout=output,
                stderr=errors,
            )
            return code, output.getvalue(), errors.getvalue()

    def test_success_uses_loaded_vector_count_instead_of_fixed_total(self) -> None:
        document = json.loads((ROOT.parent / "conformance" / "vectors-v1.json").read_text(encoding="utf-8"))
        code, output, error = self.invoke(document["vectors"][:1])
        self.assertEqual(code, 0, error)
        self.assertIn("summary passed=1 failed=0 unrepresentable=0", output)

    def test_empty_vector_set_fails_closed(self) -> None:
        code, output, error = self.invoke([])
        self.assertEqual(code, 1, error)
        self.assertEqual(output, "summary passed=0 failed=0 unrepresentable=0\n")


class GenericLawTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_config(ROOT / "config.example.json")[0]

    def base(self) -> dict:
        return {
            "size": "L", "high_risk": False, "member_floor3": None,
            "writer": {"model": "model-w", "lineage": "family-w"},
            "seats": [],
        }

    def test_invalid_correlated_extra_still_credits_one_lineage_representative(self) -> None:
        given = self.base()
        given["seats"] = [
            {"model": "model-x", "lineage": "family-w"},
            {"model": "model-y", "lineage": "family-w"},
            {"model": "model-b", "lineage": "family-b"},
            {"model": "model-c", "lineage": "family-c"},
        ]
        self.assertTrue(evaluate_panel(given, self.config)["lawful"])

    def test_third_duplicate_cannot_reuse_a_previously_credited_agent(self) -> None:
        given = self.base()
        given["distinct_lineages_available"] = 1
        given["seats"] = [
            {"model": "model-a", "lineage": "family-a", "agent": "agent-1"},
            {"model": "model-a", "lineage": "family-a", "agent": "agent-2", "downgrade": {"owner_approval": True, "noted_in_review_record": True}},
            {"model": "model-a", "lineage": "family-a", "agent": "agent-2", "downgrade": {"owner_approval": True, "noted_in_review_record": True}},
        ]
        self.assertFalse(evaluate_panel(given, self.config)["lawful"])

    def test_duplicate_model_base_registers_its_lineage(self) -> None:
        config = copy.deepcopy(self.config)
        config["model_lineages"]["model-c"] = "family-a"
        given = self.base()
        given["distinct_lineages_available"] = 2
        given["seats"] = [
            {"model": "model-a", "lineage": "family-a", "agent": "agent-1"},
            {"model": "model-a", "lineage": "family-a", "agent": "agent-2", "downgrade": {"owner_approval": True, "noted_in_review_record": True}},
            {"model": "model-c", "lineage": "family-a"},
        ]
        self.assertFalse(evaluate_panel(given, config)["lawful"])

    def test_duplicate_model_first_occurrence_still_checks_lineage_normally(self) -> None:
        """#71 delta2・Grok 席 M1 first duplicate occurrence still needs normal lineage checks."""
        config = copy.deepcopy(self.config)
        config["model_lineages"]["model-c"] = "family-a"
        given = self.base()
        given["size"] = "S"
        given["high_risk"] = True
        given["distinct_lineages_available"] = 3
        given["seats"] = [
            {"model": "model-b", "lineage": "family-b"},
            {"model": "model-d", "lineage": "family-d"},
            {"model": "model-c", "lineage": "family-a"},
            {"model": "model-a", "lineage": "family-a", "agent": "agent-1"},
            {"model": "model-a", "lineage": "family-a", "agent": "agent-2", "downgrade": {"owner_approval": True, "noted_in_review_record": True}},
        ]
        self.assertFalse(evaluate_panel(given, config)["lawful"])

    def test_malformed_panel_facts_and_writer_condition_fail_closed(self) -> None:
        cases = []
        wrong_lineage = self.base()
        wrong_lineage["seats"] = [{"model": "model-a", "lineage": "family-b"}]
        cases.append(wrong_lineage)
        bad_seat = self.base()
        bad_seat["seats"] = ["model-a"]
        cases.append(bad_seat)
        wrong_writer_condition = self.base()
        wrong_writer_condition["seats"] = [
            {"model": "model-x", "lineage": "family-w"},
            {"model": "model-y", "lineage": "family-w"},
            {"model": "model-b", "lineage": "family-b"},
        ]
        wrong_writer_condition["exception_record"] = {
            "present": True,
            "fields_present": list(self.config["conformance"]["exception_fields"]),
            "scope_covers_lane": True,
            "scope": "lane",
            "pair": ["model-x", "model-y"],
            "reason": "bounded record",
            "approved_by": "member-a",
            "date": "2026-08-16",
            "writer_condition": "model-a",
        }
        wrong_writer_condition["review_record"] = {
            "cites_correlated_seats": True,
            "requested_actual_present": True,
        }
        cases.append(wrong_writer_condition)
        for index, given in enumerate(cases):
            with self.subTest(index=index):
                with self.assertRaises(ValueError):
                    evaluate_panel(given, self.config)

    def test_operational_rule_change_also_changes_law_requirement(self) -> None:
        given = self.base()
        given["seats"] = [
            {"model": "model-a", "lineage": "family-a"},
            {"model": "model-b", "lineage": "family-b"},
            {"model": "model-c", "lineage": "family-c"},
        ]
        changed = copy.deepcopy(self.config)
        changed["panel_strategies"]["large"]["required"] = 4
        self.assertEqual(evaluate_panel(given, changed)["required_seats"], 4)
        self.assertFalse(evaluate_panel(given, changed)["lawful"])

    def test_pre_effect_floor_changes_operational_selection(self) -> None:
        changed = copy.deepcopy(self.config)
        changed["floor3"]["effective"] = False
        roster = {item: {"eligible": True} for item in changed["models"]}
        result = resolve(changed, "S", (), (), roster)
        self.assertEqual(result["required"], 2)
        self.assertEqual(len(result["final_seats"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
