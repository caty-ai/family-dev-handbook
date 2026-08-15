"""Command-line entry point and fail-closed document validation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence, TextIO

from .catalog import CatalogFormatError, read_catalog
from .rules import resolve


CATALOG_UNSTAMPED = "CATALOG-UNSTAMPED"
CATALOG_UNREADABLE = "CATALOG-UNREADABLE"
CATALOG_STALE = "CATALOG-STALE"
HEX_RE = re.compile(r"^[0-9a-f]{64}$")


class DocumentError(ValueError):
    """A configuration or roster document is invalid."""


class CatalogError(ValueError):
    def __init__(self, status: str, message: str):
        super().__init__(message)
        self.status = status


def _digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DocumentError(f"duplicate key {key!r}")
        result[key] = value
    return result


def _read_json(path: Path, label: str) -> tuple[dict[str, Any], bytes]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise DocumentError(f"cannot read {label} {path}: {exc}") from exc
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
    except (UnicodeError, ValueError) as exc:
        raise DocumentError(f"cannot parse {label} {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise DocumentError(f"{label} root must be an object")
    return value, raw


def _string_list(value: Any, path: str, *, nonempty: bool = True) -> list[str]:
    if not isinstance(value, list) or (nonempty and not value):
        raise DocumentError(f"{path} must be a{' non-empty' if nonempty else ''} string array")
    if any(not isinstance(item, str) or not item for item in value) or len(set(value)) != len(value):
        raise DocumentError(f"{path} must contain unique non-empty strings")
    return value


def _positive_int(value: Any, path: str, *, allow_zero: bool = False) -> int:
    floor = 0 if allow_zero else 1
    if not isinstance(value, int) or isinstance(value, bool) or value < floor:
        raise DocumentError(f"{path} must be an integer >= {floor}")
    return value


def load_config(path: Path) -> tuple[dict[str, Any], bytes]:
    config, raw = _read_json(path, "configuration")
    required = {
        "config_version", "selection_fn_version", "rules_version", "sizes",
        "risk_areas", "models", "model_lineages", "excluded_models",
        "writer_assumed", "same_family_authorization", "floor3", "rule_table",
        "panel_strategies", "correlated_seat_exceptions", "downgrade_records",
        "citations", "notes", "conformance",
    }
    if set(config) != required:
        raise DocumentError("configuration keys do not match the version-1 contract")
    if config["config_version"] != 1 or isinstance(config["config_version"], bool):
        raise DocumentError("config_version must be 1")
    _positive_int(config["selection_fn_version"], "selection_fn_version")
    _positive_int(config["rules_version"], "rules_version")
    sizes = _string_list(config["sizes"], "sizes")
    _string_list(config["risk_areas"], "risk_areas")
    models = _string_list(config["models"], "models")
    model_set = set(models)
    lineages = config["model_lineages"]
    if not isinstance(lineages, dict) or set(lineages) != model_set:
        raise DocumentError("model_lineages must map every configured model exactly once")
    if any(not isinstance(value, str) or not value for value in lineages.values()):
        raise DocumentError("model_lineages values must be non-empty strings")
    excluded = _string_list(config["excluded_models"], "excluded_models", nonempty=False)
    if not set(excluded).issubset(model_set):
        raise DocumentError("excluded_models contains an unknown model")
    if config["writer_assumed"] not in model_set:
        raise DocumentError("writer_assumed must be a configured model")
    authorization = config["same_family_authorization"]
    if not isinstance(authorization, dict) or set(authorization) != {"writer", "seats"}:
        raise DocumentError("same_family_authorization must contain writer and seats")
    seats = _string_list(authorization["seats"], "same_family_authorization.seats", nonempty=False)
    if authorization["writer"] not in model_set or not set(seats).issubset(model_set):
        raise DocumentError("same_family_authorization references an unknown model")
    if authorization["writer"] != config["writer_assumed"] or config["writer_assumed"] in seats:
        raise DocumentError("same_family_authorization must use the writer premise and cannot authorize the writer model")
    writer_lineage = lineages[authorization["writer"]]
    if any(lineages[item] != writer_lineage for item in seats):
        raise DocumentError("same_family_authorization seats must share the writer lineage")

    floor = config["floor3"]
    floor_keys = {"sizes", "effective"}
    floor_keys_with_strategy = floor_keys | {"pre_effect_strategy"}
    if not isinstance(floor, dict) or set(floor) not in (floor_keys, floor_keys_with_strategy):
        raise DocumentError("floor3 has invalid keys")
    floor_sizes = _string_list(floor["sizes"], "floor3.sizes", nonempty=False)
    if not set(floor_sizes).issubset(sizes) or not isinstance(floor["effective"], bool):
        raise DocumentError("floor3 sizes/effective are invalid")
    if floor_sizes and "pre_effect_strategy" not in floor:
        raise DocumentError("floor3.pre_effect_strategy is required when floor3.sizes is non-empty")
    if "pre_effect_strategy" in floor and (
        not isinstance(floor["pre_effect_strategy"], str) or not floor["pre_effect_strategy"]
    ):
        raise DocumentError("floor3.pre_effect_strategy must be non-empty")

    strategies = config["panel_strategies"]
    if not isinstance(strategies, dict) or not strategies:
        raise DocumentError("panel_strategies must be a non-empty object")
    for name, strategy in strategies.items():
        if not isinstance(name, str) or not name or not isinstance(strategy, dict):
            raise DocumentError("panel_strategies entries are invalid")
        strategy_type = strategy.get("type")
        if strategy_type == "fixed":
            if set(strategy) != {"type", "selection_path", "required", "panel", "substitutes", "substitution_cap"}:
                raise DocumentError(f"panel_strategies.{name} has invalid fixed keys")
            panel = _string_list(strategy["panel"], f"panel_strategies.{name}.panel")
            substitutes = _string_list(strategy["substitutes"], f"panel_strategies.{name}.substitutes", nonempty=False)
            _positive_int(strategy["required"], f"panel_strategies.{name}.required")
            _positive_int(strategy["substitution_cap"], f"panel_strategies.{name}.substitution_cap", allow_zero=True)
            if strategy["required"] != len(panel) or not set(panel + substitutes).issubset(model_set):
                raise DocumentError(f"panel_strategies.{name} references invalid panel data")
        elif strategy_type == "standing_rotation":
            expected = {"type", "selection_path", "required", "standing", "standing_substitutes", "rotation_pool", "rotation_count"}
            if set(strategy) != expected:
                raise DocumentError(f"panel_strategies.{name} has invalid rotation keys")
            substitutes = _string_list(strategy["standing_substitutes"], f"panel_strategies.{name}.standing_substitutes", nonempty=False)
            pool = _string_list(strategy["rotation_pool"], f"panel_strategies.{name}.rotation_pool")
            _positive_int(strategy["required"], f"panel_strategies.{name}.required")
            _positive_int(strategy["rotation_count"], f"panel_strategies.{name}.rotation_count", allow_zero=True)
            if strategy["standing"] not in model_set or not set(substitutes + pool).issubset(model_set):
                raise DocumentError(f"panel_strategies.{name} references an unknown model")
            if strategy["required"] != strategy["rotation_count"] + 1:
                raise DocumentError(f"panel_strategies.{name} required must equal rotation_count + 1")
        else:
            raise DocumentError(f"panel_strategies.{name}.type is invalid")
        if strategy["selection_path"] not in {"named_panel", "machine"}:
            raise DocumentError(f"panel_strategies.{name}.selection_path is invalid")
        referenced = set(strategy.get("panel", [])) | set(strategy.get("substitutes", [])) | set(strategy.get("standing_substitutes", [])) | set(strategy.get("rotation_pool", [])) | {strategy.get("standing")}
        if (referenced - {None}) & set(excluded):
            raise DocumentError(f"panel_strategies.{name} references an excluded model")

    table = config["rule_table"]
    if not isinstance(table, dict) or set(table) != set(sizes):
        raise DocumentError("rule_table must contain every configured size exactly once")
    for size, row in table.items():
        if not isinstance(row, dict) or set(row) != {"absent", "present"}:
            raise DocumentError(f"rule_table.{size} must contain absent and present")
        if any(value not in strategies for value in row.values()):
            raise DocumentError(f"rule_table.{size} references an unknown strategy")
    if "pre_effect_strategy" in floor and floor["pre_effect_strategy"] not in strategies:
        raise DocumentError("floor3.pre_effect_strategy references an unknown strategy")
    _validate_operational_records(config, strategies, model_set, set(excluded), lineages)
    notes = config["notes"]
    if not isinstance(notes, dict) or set(notes) != {"availability", "writer", "seat_wait"} or any(not isinstance(value, str) for value in notes.values()):
        raise DocumentError("notes has invalid keys or values")
    _string_list(config["citations"], "citations")
    _validate_conformance(config["conformance"])
    return config, raw


def _canonical_date(value: Any, path: str) -> None:
    if not isinstance(value, str):
        raise DocumentError(f"{path} must be a canonical ISO date")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise DocumentError(f"{path} must be a valid ISO date") from exc
    if parsed.isoformat() != value:
        raise DocumentError(f"{path} must be a canonical ISO date")


def _validate_operational_records(
    config: Mapping[str, Any],
    strategies: Mapping[str, Any],
    models: set[str],
    excluded: set[str],
    lineages: Mapping[str, str],
) -> None:
    exceptions = config["correlated_seat_exceptions"]
    if not isinstance(exceptions, list):
        raise DocumentError("correlated_seat_exceptions must be an array")
    seen_exceptions: set[tuple[tuple[str, ...], tuple[str, str]]] = set()
    exception_keys = {"scope", "pair", "reason", "approved_by", "date", "writer_condition"}
    for index, record in enumerate(exceptions):
        path = f"correlated_seat_exceptions[{index}]"
        if not isinstance(record, dict) or set(record) != exception_keys:
            raise DocumentError(f"{path} must contain exactly the six exception fields")
        scope = _string_list(record["scope"], f"{path}.scope")
        pair = _string_list(record["pair"], f"{path}.pair")
        if len(pair) != 2 or not set(pair).issubset(models - excluded):
            raise DocumentError(f"{path}.pair must contain two configured, non-excluded models")
        if not set(scope).issubset(strategies):
            raise DocumentError(f"{path}.scope references an unknown strategy")
        if lineages[pair[0]] != lineages[pair[1]]:
            raise DocumentError(f"{path}.pair must identify one correlated lineage")
        for key in ("reason", "approved_by"):
            if not isinstance(record[key], str) or not record[key].strip():
                raise DocumentError(f"{path}.{key} must be a non-empty string")
        _canonical_date(record["date"], f"{path}.date")
        if record["writer_condition"] != config["writer_assumed"]:
            raise DocumentError(f"{path}.writer_condition must equal writer_assumed")
        identity = (tuple(sorted(scope)), tuple(sorted(pair)))
        if identity in seen_exceptions:
            raise DocumentError(f"{path} duplicates an exception scope and pair")
        seen_exceptions.add(identity)

    downgrades = config["downgrade_records"]
    if not isinstance(downgrades, list):
        raise DocumentError("downgrade_records must be an array")
    seen_downgrades: set[tuple[tuple[str, ...], str]] = set()
    downgrade_keys = {"scope", "model", "agents", "owner_approval", "review_notation"}
    for index, record in enumerate(downgrades):
        path = f"downgrade_records[{index}]"
        if not isinstance(record, dict) or set(record) != downgrade_keys:
            raise DocumentError(f"{path} has invalid keys")
        scope = _string_list(record["scope"], f"{path}.scope")
        agents = _string_list(record["agents"], f"{path}.agents")
        if len(agents) < 2:
            raise DocumentError(f"{path}.agents must contain at least two distinct agents")
        if not set(scope).issubset(strategies):
            raise DocumentError(f"{path}.scope references an unknown strategy")
        if record["model"] not in models - excluded or record["model"] == config["writer_assumed"]:
            raise DocumentError(f"{path}.model must be a non-writer, non-excluded configured model")
        for key in ("owner_approval", "review_notation"):
            if not isinstance(record[key], str) or not record[key].strip():
                raise DocumentError(f"{path}.{key} must be a non-empty evidence reference")
        identity = (tuple(sorted(scope)), record["model"])
        if identity in seen_downgrades:
            raise DocumentError(f"{path} duplicates a downgrade scope and model")
        seen_downgrades.add(identity)


def _validate_conformance(policy: Any) -> None:
    required = {
        "role_conflicts", "downgrade_fields", "exception_fields", "seat_wait_target", "seat_wait_fields",
    }
    if not isinstance(policy, dict) or set(policy) != required:
        raise DocumentError("conformance has invalid keys")
    _string_list(policy["role_conflicts"], "conformance.role_conflicts")
    _string_list(policy["downgrade_fields"], "conformance.downgrade_fields")
    _string_list(policy["exception_fields"], "conformance.exception_fields")
    _string_list(policy["seat_wait_fields"], "conformance.seat_wait_fields")
    if not isinstance(policy["seat_wait_target"], str) or not policy["seat_wait_target"]:
        raise DocumentError("conformance.seat_wait_target must be non-empty")


def load_roster(path: Path, config: Mapping[str, Any]) -> tuple[dict[str, Any], bytes]:
    roster, raw = _read_json(path, "roster")
    if set(roster) != {"roster_version", "models", "catalog"}:
        raise DocumentError("roster keys do not match the version-1 contract")
    if roster["roster_version"] != 1 or isinstance(roster["roster_version"], bool):
        raise DocumentError("roster_version must be 1")
    models = roster["models"]
    if not isinstance(models, dict):
        raise DocumentError("roster models must be an object")
    unknown = sorted(set(models) - set(config["models"]))
    if unknown:
        raise DocumentError(f"unknown roster keys: {', '.join(repr(item) for item in unknown)}")
    for model_id, entry in models.items():
        if not isinstance(entry, dict) or not isinstance(entry.get("eligible"), bool):
            raise DocumentError(f"roster model {model_id!r} must have boolean eligible")
        if "display" in entry and not isinstance(entry["display"], str):
            raise DocumentError(f"roster model {model_id!r} display must be a string")
    return roster, raw


def validate_catalog_stamp(roster: Mapping[str, Any], today: date) -> tuple[str, str, str]:
    stamp = roster.get("catalog")
    if not isinstance(stamp, Mapping) or set(stamp) != {"path", "adopted_digest"}:
        raise CatalogError(CATALOG_UNSTAMPED, "catalog stamp must contain path and adopted_digest")
    path_value = stamp.get("path")
    adopted = stamp.get("adopted_digest")
    if not isinstance(path_value, str) or not path_value or not Path(path_value).is_absolute():
        raise CatalogError(CATALOG_UNSTAMPED, "catalog path must be a non-empty absolute path")
    if not isinstance(adopted, str) or not HEX_RE.fullmatch(adopted):
        raise CatalogError(CATALOG_UNSTAMPED, "adopted_digest must be lowercase 64-hex")
    path = Path(path_value)
    try:
        raw, parsed = read_catalog(path)
    except CatalogFormatError as exc:
        raise CatalogError(CATALOG_UNREADABLE, f"catalog {path} is unreadable: {exc}") from exc
    current = _digest(raw)
    if current == adopted:
        return adopted, "matched", ""
    effective = date.fromisoformat(parsed["revision_effective_after"])
    if today <= effective:
        note = (
            f"Catalog digest mismatch is accepted through {effective.isoformat()}; "
            "adopt the current catalog digest before the window closes."
        )
        return adopted, "grace", note
    raise CatalogError(
        CATALOG_STALE,
        f"adopted digest differs from catalog and the window ended {effective.isoformat()}",
    )


def _append_note(note: str, advisory: str) -> str:
    return advisory if not note else f"{note} {advisory}"


def _catalog_failure(error: CatalogError, roster_path: Path, output: TextIO, errors: TextIO, style: str) -> None:
    errors.write(f"seat-resolver: {error}\n")
    payload = {"status": error.status, "message": str(error), "roster_path": str(roster_path)}
    if style == "text":
        for key, value in payload.items():
            output.write(f"{key}: {value}\n")
    else:
        json.dump(payload, output, ensure_ascii=True, separators=(",", ":"))
        output.write("\n")


def _text(result: Mapping[str, Any], roster: Mapping[str, Any], output: TextIO) -> None:
    models = roster["models"]
    def display(model_id: str) -> str:
        value = models.get(model_id, {}).get("display")
        return value if isinstance(value, str) else model_id
    values = [
        ("status", result["status"]),
        ("strategy", result["strategy"]),
        ("selection_path", result["selection_path"]),
        ("seats", ", ".join(f"{display(item)} ({item})" for item in result["final_seats"]) or "none"),
        ("substitutions", ", ".join(f"{item['absent']} -> {item['replacement']}" for item in result["substitutions"]) or "none"),
        ("unavailable", ", ".join(result["unavailable"]) or "none"),
        ("uncountable", json.dumps(result["uncountable"], ensure_ascii=True, separators=(",", ":")) if result["uncountable"] else "none"),
        ("missing", ", ".join(result["missing"]) or "none"),
        ("rotation_shortfall", result["rotation_shortfall"]),
        ("same_family_seats", ", ".join(result["same_family_seats"]) or "none"),
        ("seat_instances", json.dumps(result["seat_instances"], ensure_ascii=True, separators=(",", ":"))),
        ("applied_exception_records", json.dumps(result["applied_exception_records"], ensure_ascii=True, separators=(",", ":")) if result["applied_exception_records"] else "none"),
        ("applied_downgrade_records", json.dumps(result["applied_downgrade_records"], ensure_ascii=True, separators=(",", ":")) if result["applied_downgrade_records"] else "none"),
        ("writer_assumed", result["writer_assumed"]),
        ("availability_note", result["availability_note"]),
        ("writer_note", result["writer_note"]),
        ("catalog_digest", result["catalog_digest"]),
        ("catalog_state", result["catalog_state"]),
        ("selection_fn_version", result["selection_fn_version"]),
        ("config_digest", result["config_digest"]),
    ]
    if result["note"]:
        values.append(("note", result["note"]))
    for key, value in values:
        output.write(f"{key}: {value}\n")


def main(
    argv: Sequence[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    environ: Mapping[str, str] | None = None,
    today: date | None = None,
) -> int:
    root = Path(__file__).resolve().parents[1]
    env = os.environ if environ is None else environ
    parser = argparse.ArgumentParser(prog="seat-resolver")
    parser.add_argument("--size", required=True)
    parser.add_argument("--risk", action="append", default=[])
    parser.add_argument("--absent", action="append", default=[])
    parser.add_argument("--config", default=env.get("SEAT_RESOLVER_CONFIG", str(root / "config.example.json")))
    parser.add_argument("--roster", default=env.get("SEAT_RESOLVER_ROSTER", str(root / "roster.example.json")))
    parser.add_argument("--format", choices=("json", "text"), default="json")
    args = parser.parse_args(argv)
    output = sys.stdout if stdout is None else stdout
    errors = sys.stderr if stderr is None else stderr
    config_path = Path(args.config).expanduser().resolve()
    roster_path = Path(args.roster).expanduser().resolve()
    try:
        config, config_raw = load_config(config_path)
        roster, _ = load_roster(roster_path, config)
    except DocumentError as exc:
        errors.write(f"seat-resolver: document error: {exc}\n")
        return 3
    size_lookup = {item.upper(): item for item in config["sizes"]}
    normalized_size = size_lookup.get(args.size.upper())
    invalid_risks = sorted(set(args.risk) - set(config["risk_areas"]))
    invalid_absent = sorted(set(args.absent) - set(config["models"]))
    if normalized_size is None or invalid_risks or invalid_absent:
        details = []
        if normalized_size is None:
            details.append(f"invalid size {args.size!r}")
        if invalid_risks:
            details.append(f"invalid risk values {invalid_risks!r}")
        if invalid_absent:
            details.append(f"invalid absent values {invalid_absent!r}")
        errors.write(f"seat-resolver: invalid arguments: {'; '.join(details)}\n")
        return 2
    try:
        catalog_digest, catalog_state, catalog_note = validate_catalog_stamp(roster, today or date.today())
    except CatalogError as exc:
        _catalog_failure(exc, roster_path, output, errors, args.format)
        return 4
    result = resolve(config, normalized_size, args.risk, args.absent, roster["models"])
    result = {
        "size": result["size"],
        "risk_areas": result["risk_areas"],
        "risk_override": result["risk_override"],
        "strategy": result["strategy"],
        "selection_path": result["selection_path"],
        "required": result["required"],
        "panel": result["panel"],
        "unavailable": result["unavailable"],
        "uncountable": result["uncountable"],
        "substitutions": result["substitutions"],
        "final_seats": result["final_seats"],
        "seat_instances": result["seat_instances"],
        "applied_exception_records": result["applied_exception_records"],
        "applied_downgrade_records": result["applied_downgrade_records"],
        "same_family_seats": result["same_family_seats"],
        "writer_assumed": result["writer_assumed"],
        "missing": result["missing"],
        "rotation_shortfall": result["rotation_shortfall"],
        "quorum_met": result["quorum_met"],
        "status": result["status"],
        "note": _append_note(result["note"], catalog_note) if catalog_note else result["note"],
        "availability_note": result["availability_note"],
        "writer_note": result["writer_note"],
        "citations": result["citations"],
        "roster_path": str(roster_path),
        "config_path": str(config_path),
        "catalog_digest": catalog_digest,
        "catalog_state": catalog_state,
        "selection_fn_version": config["selection_fn_version"],
        "config_digest": _digest(config_raw),
        "rules_version": result["rules_version"],
    }
    if args.format == "text":
        _text(result, roster, output)
    else:
        json.dump(result, output, ensure_ascii=True, separators=(",", ":"))
        output.write("\n")
    return 0 if result["quorum_met"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
