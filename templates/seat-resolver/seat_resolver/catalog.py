"""Strict, standard-library parser for the published catalog YAML profile."""

from __future__ import annotations

import codecs
import json
import re
import unicodedata
from datetime import date
from pathlib import Path
from typing import Any


KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
TOP_KEYS = {"revision", "date", "revision_effective_after", "changelog", "blast_radius", "models"}
ROW_KEYS = {
    "id", "lineage", "tier", "rank", "status", "quorum_eligible",
    "recheck_after", "cost_class", "escalation_only", "data_handling", "date",
}
ROW_REQUIRED = ROW_KEYS - {"recheck_after"}


class CatalogFormatError(ValueError):
    """Catalog bytes are not valid under the restricted profile."""


def _commentless(line: str) -> str:
    single = double = escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
        elif double and char == "\\":
            escaped = True
        elif char == "'" and not double:
            single = not single
        elif char == '"' and not single:
            double = not double
        elif char == "#" and not single and not double and (index == 0 or line[index - 1].isspace()):
            return line[:index].rstrip()
    if single or double:
        raise CatalogFormatError("unterminated quoted scalar")
    return line.rstrip()


def _split_items(body: str, line_number: int) -> list[str]:
    items: list[str] = []
    current: list[str] = []
    single = double = escaped = False
    depth = 0
    for char in body:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if double and char == "\\":
            current.append(char)
            escaped = True
            continue
        if char == "'" and not double:
            single = not single
        elif char == '"' and not single:
            double = not double
        elif not single and not double:
            if char in "[{":
                depth += 1
            elif char in "]}":
                depth -= 1
                if depth < 0:
                    raise CatalogFormatError(f"line {line_number}: malformed flow value")
            elif char == "," and depth == 0:
                items.append("".join(current).strip())
                current = []
                continue
        current.append(char)
    if single or double or depth:
        raise CatalogFormatError(f"line {line_number}: malformed flow value")
    items.append("".join(current).strip())
    return items


def _key_value(text: str, line_number: int) -> tuple[str, str]:
    if ":" not in text:
        raise CatalogFormatError(f"line {line_number}: expected key: value")
    key, value = text.split(":", 1)
    key = key.strip()
    if not KEY_RE.fullmatch(key):
        raise CatalogFormatError(f"line {line_number}: invalid key {key!r}")
    return key, value.strip()


def _scalar(value: str, line_number: int) -> Any:
    if value == "":
        return None
    if value in {"true", "false"}:
        return value == "true"
    if value in {"null", "~"}:
        return None
    if re.fullmatch(r"-?(0|[1-9][0-9]*)", value):
        return int(value)
    if value.startswith("{"):
        if not value.endswith("}"):
            raise CatalogFormatError(f"line {line_number}: malformed flow mapping")
        result: dict[str, Any] = {}
        body = value[1:-1].strip()
        for item in ([] if not body else _split_items(body, line_number)):
            key, nested = _key_value(item, line_number)
            _put(result, key, _scalar(nested, line_number), line_number)
        return result
    if value.startswith("["):
        if not value.endswith("]"):
            raise CatalogFormatError(f"line {line_number}: malformed flow sequence")
        body = value[1:-1].strip()
        return [] if not body else [_scalar(item, line_number) for item in _split_items(body, line_number)]
    if value.startswith(("&", "*", "!")):
        raise CatalogFormatError(f"line {line_number}: anchors, aliases, and tags are unsupported")
    if value[0] in {"'", '"'}:
        if len(value) < 2 or value[-1] != value[0]:
            raise CatalogFormatError(f"line {line_number}: unterminated quoted scalar")
        if value[0] == "'" and ("\\" in value[1:-1] or "''" in value[1:-1]):
            raise CatalogFormatError(f"line {line_number}: unsupported single-quoted scalar")
        try:
            parsed = json.loads(value) if value[0] == '"' else value[1:-1]
        except ValueError as exc:
            raise CatalogFormatError(f"line {line_number}: invalid quoted scalar") from exc
        if not isinstance(parsed, str) or any(unicodedata.category(char) == "Cc" for char in parsed):
            raise CatalogFormatError(f"line {line_number}: invalid quoted scalar")
        return parsed
    if re.search(r"(?:^|[\s:\[,])[&*!][A-Za-z0-9_-]+", value):
        raise CatalogFormatError(f"line {line_number}: anchors, aliases, and tags are unsupported")
    return value


def _put(mapping: dict[str, Any], key: str, value: Any, line_number: int) -> None:
    if key in mapping:
        raise CatalogFormatError(f"line {line_number}: duplicate key {key!r}")
    mapping[key] = value


def parse_catalog(raw: bytes) -> dict[str, Any]:
    """Parse and validate catalog raw bytes, rejecting YAML extensions."""

    if raw.startswith(codecs.BOM_UTF8):
        raise CatalogFormatError("UTF-8 BOM is not canonical")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CatalogFormatError(f"invalid UTF-8: {exc}") from exc
    data: dict[str, Any] = {}
    models: list[dict[str, Any]] | None = None
    current: dict[str, Any] | None = None
    nested: dict[str, Any] | None = None
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        raw_line = lines[index]
        number = index + 1
        if "\t" in raw_line:
            raise CatalogFormatError(f"line {number}: tabs are not allowed")
        try:
            line = _commentless(raw_line)
        except CatalogFormatError as exc:
            raise CatalogFormatError(f"line {number}: {exc}") from exc
        if not line.strip():
            index += 1
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line[indent:]
        if indent == 0:
            current = nested = None
            key, value = _key_value(stripped, number)
            if key == "models":
                if value:
                    raise CatalogFormatError(f"line {number}: models must be a block sequence")
                models = []
                _put(data, key, models, number)
                index += 1
                continue
            if value in {">", ">-", "|", "|-"}:
                block: list[str] = []
                index += 1
                while index < len(lines):
                    part = lines[index]
                    if "\t" in part:
                        raise CatalogFormatError(f"line {index + 1}: tabs are not allowed")
                    if part.strip() and len(part) - len(part.lstrip(" ")) == 0:
                        break
                    block.append(part[2:] if part.startswith("  ") else part.lstrip(" "))
                    index += 1
                scalar = " ".join(item.strip() for item in block if item.strip()) if value.startswith(">") else "\n".join(block)
                _put(data, key, scalar, number)
                continue
            _put(data, key, _scalar(value, number), number)
            index += 1
            continue
        if models is None:
            raise CatalogFormatError(f"line {number}: unexpected indentation")
        if indent == 2 and stripped.startswith("- "):
            current = {}
            models.append(current)
            nested = None
            key, value = _key_value(stripped[2:], number)
            _put(current, key, _scalar(value, number), number)
        elif indent == 4 and current is not None:
            key, value = _key_value(stripped, number)
            parsed = _scalar(value, number)
            nested = {} if value == "" else None
            _put(current, key, nested if nested is not None else parsed, number)
        elif indent == 6 and nested is not None:
            key, value = _key_value(stripped, number)
            _put(nested, key, _scalar(value, number), number)
        else:
            raise CatalogFormatError(f"line {number}: unsupported catalog YAML shape")
        index += 1
    _validate(data)
    return data


def _iso(value: Any, path: str) -> date:
    if not isinstance(value, str):
        raise CatalogFormatError(f"{path} must be a canonical ISO date")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise CatalogFormatError(f"{path} must be a valid ISO date") from exc
    if parsed.isoformat() != value:
        raise CatalogFormatError(f"{path} must be a canonical ISO date")
    return parsed


def _validate(data: dict[str, Any]) -> None:
    if set(data) != TOP_KEYS:
        missing = sorted(TOP_KEYS - set(data))
        extra = sorted(set(data) - TOP_KEYS)
        detail = f"missing {missing[0]!r}" if missing else f"unexpected {extra[0]!r}"
        raise CatalogFormatError(f"catalog top-level keys invalid: {detail}")
    if not isinstance(data["revision"], int) or isinstance(data["revision"], bool) or data["revision"] < 1:
        raise CatalogFormatError("revision must be an integer >= 1")
    catalog_date = _iso(data["date"], "date")
    effective = _iso(data["revision_effective_after"], "revision_effective_after")
    if effective < catalog_date:
        raise CatalogFormatError("revision_effective_after must be on or after date")
    for key in ("changelog", "blast_radius"):
        if not isinstance(data[key], str) or not data[key].strip():
            raise CatalogFormatError(f"{key} must be a non-empty string")
    if not isinstance(data["models"], list) or not data["models"]:
        raise CatalogFormatError("models must be a non-empty sequence")
    seen: set[str] = set()
    tier_ranks: set[tuple[str, int]] = set()
    drawable = False
    for index, row in enumerate(data["models"]):
        path = f"models[{index}]"
        if not isinstance(row, dict) or not ROW_REQUIRED.issubset(row) or set(row) - ROW_KEYS:
            raise CatalogFormatError(f"{path} has invalid keys")
        model_id = row["id"]
        if not isinstance(model_id, str) or not model_id or model_id in seen:
            raise CatalogFormatError(f"{path}.id must be unique and non-empty")
        seen.add(model_id)
        lineage = row["lineage"]
        if not isinstance(lineage, dict) or set(lineage) != {"family", "vendor"} or not all(isinstance(value, str) and value for value in lineage.values()):
            raise CatalogFormatError(f"{path}.lineage is invalid")
        if row["tier"] not in {"priority", "substitute"}:
            raise CatalogFormatError(f"{path}.tier is invalid")
        rank = row["rank"]
        if not isinstance(rank, int) or isinstance(rank, bool) or rank < 1:
            raise CatalogFormatError(f"{path}.rank must be an integer >= 1")
        pair = (row["tier"], rank)
        if pair in tier_ranks:
            raise CatalogFormatError(f"{path} has duplicate tier-rank")
        tier_ranks.add(pair)
        if row["status"] not in {"current", "trial", "retired"}:
            raise CatalogFormatError(f"{path}.status is invalid")
        for key in ("quorum_eligible", "escalation_only"):
            if not isinstance(row[key], bool):
                raise CatalogFormatError(f"{path}.{key} must be boolean")
        if row["cost_class"] not in {"subscription", "cheap-api", "expensive"}:
            raise CatalogFormatError(f"{path}.cost_class is invalid")
        if row["data_handling"] not in {"standard", "training-contributor"}:
            raise CatalogFormatError(f"{path}.data_handling is invalid")
        _iso(row["date"], f"{path}.date")
        if row["status"] == "trial":
            if "recheck_after" not in row or row["quorum_eligible"]:
                raise CatalogFormatError(f"{path} trial row is invalid")
            _iso(row["recheck_after"], f"{path}.recheck_after")
        elif "recheck_after" in row:
            _iso(row["recheck_after"], f"{path}.recheck_after")
        if row["status"] == "retired" and row["quorum_eligible"]:
            raise CatalogFormatError(f"{path} retired row is invalid")
        drawable = drawable or (row["tier"] == "priority" and row["status"] == "current" and row["quorum_eligible"])
    if not drawable:
        raise CatalogFormatError("at least one drawable priority row is required")


def read_catalog(path: Path) -> tuple[bytes, dict[str, Any]]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise CatalogFormatError(f"cannot read catalog {path}: {exc}") from exc
    return raw, parse_catalog(raw)
