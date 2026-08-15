"""Adapter from the shared vectors to generic law-evaluation functions."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence, TextIO

from .cli import DocumentError, load_config
from .rules import evaluate_panel, evaluate_record, evaluate_seat_wait


EVALUATORS = {
    "panel": evaluate_panel,
    "seat_wait": evaluate_seat_wait,
    "record": evaluate_record,
}


def evaluate_vector(vector: Mapping[str, Any], policy: Mapping[str, Any]) -> dict[str, Any]:
    kind = vector.get("kind")
    evaluator = EVALUATORS.get(kind)
    if evaluator is None:
        raise ValueError(f"unsupported vector kind {kind!r}")
    given = copy.deepcopy(vector.get("given"))
    if not isinstance(given, Mapping):
        raise ValueError("given must be an object")
    if kind == "panel":
        adapted_config = copy.deepcopy(policy)
        mapped_lineages: dict[str, str] = {}
        writer_value = given.get("writer")
        facts = list(given.get("seats", []))
        if isinstance(writer_value, Mapping):
            facts.append(writer_value)
        for fact in facts:
            if not isinstance(fact, Mapping):
                continue
            model_id = fact.get("model")
            lineage = fact.get("lineage")
            if model_id in mapped_lineages and mapped_lineages[model_id] != lineage:
                raise ValueError(f"model {model_id!r} has conflicting lineage facts")
            mapped_lineages[model_id] = lineage
        adapted_config["model_lineages"].update(mapped_lineages)
        record = given.get("exception_record")
        writer = given.get("writer")
        if (
            isinstance(record, dict)
        ):
            fields = record.get("fields_present", [])
            correlated_pair = None
            seats = given.get("seats", [])
            for left_index, left in enumerate(seats):
                for right in seats[left_index + 1:]:
                    if (
                        isinstance(left, Mapping)
                        and isinstance(right, Mapping)
                        and left.get("model") != right.get("model")
                        and left.get("lineage") == right.get("lineage")
                    ):
                        correlated_pair = [left.get("model"), right.get("model")]
                        break
                if correlated_pair is not None:
                    break
            values = {
                "scope": "lane",
                "pair": correlated_pair,
                "reason": "recorded exception",
                "approved_by": "member-a",
                "date": "2026-08-16",
                "writer_condition": writer.get("model") if isinstance(writer, Mapping) else None,
            }
            for field in fields:
                if field not in record:
                    record[field] = values[field]
        return evaluator(given, adapted_config)
    return evaluator(given, policy)


def main(argv: Sequence[str] | None = None, *, stdout: TextIO | None = None, stderr: TextIO | None = None) -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(prog="run-conformance")
    parser.add_argument("--vectors", default=str(root.parent / "conformance" / "vectors-v1.json"))
    parser.add_argument("--config", default=str(root / "config.example.json"))
    args = parser.parse_args(argv)
    output = sys.stdout if stdout is None else stdout
    errors = sys.stderr if stderr is None else stderr
    try:
        config, _ = load_config(Path(args.config).expanduser().resolve())
        document = json.loads(Path(args.vectors).expanduser().resolve().read_text(encoding="utf-8"))
        vectors = document["vectors"]
        if not isinstance(vectors, list):
            raise ValueError("vectors must be an array")
    except (OSError, ValueError, KeyError, DocumentError) as exc:
        errors.write(f"run-conformance: cannot load inputs: {exc}\n")
        return 2
    passed = failed = unrepresentable = 0
    for vector in vectors:
        vector_id = vector.get("id", "<missing-id>") if isinstance(vector, dict) else "<invalid-vector>"
        try:
            actual = evaluate_vector(vector, config)
            expected = vector["expect"]
            if actual == expected:
                passed += 1
                output.write(f"{vector_id} PASS\n")
            else:
                failed += 1
                output.write(f"{vector_id} FAIL expected={json.dumps(expected, sort_keys=True)} actual={json.dumps(actual, sort_keys=True)}\n")
        except (KeyError, TypeError, ValueError) as exc:
            failed += 1
            unrepresentable += 1
            output.write(f"{vector_id} FAIL unrepresentable={exc}\n")
    output.write(f"summary passed={passed} failed={failed} unrepresentable={unrepresentable}\n")
    return 0 if vectors and passed == len(vectors) else 1


if __name__ == "__main__":
    raise SystemExit(main())
