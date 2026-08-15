"""Pure operational selection and handbook-law evaluation functions."""

from __future__ import annotations

from collections import Counter
from datetime import date
from typing import Any, Iterable, Mapping


def _available(
    model_id: str,
    roster: Mapping[str, Mapping[str, Any]],
    absent: frozenset[str],
    excluded: frozenset[str],
) -> bool:
    entry = roster.get(model_id)
    return (
        model_id not in excluded
        and model_id not in absent
        and entry is not None
        and entry.get("eligible") is True
    )


def _exception_records_for(
    config: Mapping[str, Any],
    strategy_name: str,
    first: str,
    second: str,
) -> list[Mapping[str, Any]]:
    pair = {first, second}
    return [
        record
        for record in config["correlated_seat_exceptions"]
        if strategy_name in record["scope"]
        and set(record["pair"]) == pair
        and record["writer_condition"] == config["writer_assumed"]
    ]


def _candidate_records(
    model_id: str,
    seated: list[str],
    config: Mapping[str, Any],
    strategy_name: str,
) -> tuple[bool, str | None, list[Mapping[str, Any]]]:
    if model_id == config["writer_assumed"]:
        return False, "writer-model", []
    lineages = config["model_lineages"]
    writer_lineage = lineages[config["writer_assumed"]]
    if (
        lineages[model_id] == writer_lineage
        and model_id not in config["same_family_authorization"]["seats"]
    ):
        return False, "same-family-unauthorized", []
    if model_id in seated:
        return False, "duplicate-model", []
    applied: list[Mapping[str, Any]] = []
    for other in seated:
        if lineages[other] != lineages[model_id]:
            continue
        records = _exception_records_for(config, strategy_name, other, model_id)
        if not records:
            return False, "correlated-lineage-unrecorded", []
        applied.append(records[0])
    return True, None, applied


def _append_records(target: list[Mapping[str, Any]], records: Iterable[Mapping[str, Any]]) -> None:
    for record in records:
        if record not in target:
            target.append(record)


def _fixed_panel(
    config: Mapping[str, Any],
    strategy_name: str,
    strategy: Mapping[str, Any],
    roster: Mapping[str, Mapping[str, Any]],
    absent: frozenset[str],
    excluded: frozenset[str],
) -> dict[str, Any]:
    panel = list(strategy["panel"])
    substitutes = list(strategy.get("substitutes", []))
    cap = strategy.get("substitution_cap", 0)
    unavailable = [item for item in panel if not _available(item, roster, absent, excluded)]
    final_seats: list[str] = []
    replacements: list[dict[str, str]] = []
    missing: list[str] = []
    seated: list[str] = []
    uncountable: list[dict[str, str]] = []
    applied_exceptions: list[Mapping[str, Any]] = []

    for model_id in panel:
        if model_id not in unavailable:
            lawful, reason, records = _candidate_records(
                model_id, seated, config, strategy_name
            )
            if not lawful:
                uncountable.append({"model": model_id, "reason": reason or "invalid-seat"})
                replacement = None
                replacement_records: list[Mapping[str, Any]] = []
                if strategy["selection_path"] == "machine" and len(replacements) < cap:
                    for candidate in substitutes:
                        if candidate in seated or candidate in panel:
                            continue
                        candidate_lawful, candidate_reason, candidate_records = _candidate_records(
                            candidate, seated, config, strategy_name
                        )
                        if _available(candidate, roster, absent, excluded) and candidate_lawful:
                            replacement = candidate
                            replacement_records = candidate_records
                            break
                        if _available(candidate, roster, absent, excluded) and not candidate_lawful:
                            uncountable.append({"model": candidate, "reason": candidate_reason or "invalid-seat"})
                if replacement is None:
                    missing.append(model_id)
                else:
                    replacements.append({"absent": model_id, "replacement": replacement})
                    final_seats.append(replacement)
                    seated.append(replacement)
                    _append_records(applied_exceptions, replacement_records)
                continue
            final_seats.append(model_id)
            seated.append(model_id)
            _append_records(applied_exceptions, records)
            continue
        replacement = None
        replacement_records: list[Mapping[str, Any]] = []
        if len(replacements) < cap:
            for candidate in substitutes:
                if candidate in seated or candidate in panel:
                    continue
                lawful, reason, records = _candidate_records(
                    candidate, seated, config, strategy_name
                )
                if _available(candidate, roster, absent, excluded) and lawful:
                    replacement = candidate
                    replacement_records = records
                    break
                if _available(candidate, roster, absent, excluded) and not lawful:
                    uncountable.append({"model": candidate, "reason": reason or "invalid-seat"})
        if replacement is None:
            missing.append(model_id)
        else:
            replacements.append({"absent": model_id, "replacement": replacement})
            final_seats.append(replacement)
            seated.append(replacement)
            _append_records(applied_exceptions, replacement_records)

    return {
        "required": strategy["required"],
        "panel": panel,
        "unavailable": unavailable,
        "substitutions": replacements,
        "final_seats": final_seats,
        "missing": missing,
        "rotation_shortfall": 0,
        "uncountable": uncountable,
        "applied_exception_records": applied_exceptions,
    }


def _standing_rotation(
    config: Mapping[str, Any],
    strategy_name: str,
    strategy: Mapping[str, Any],
    roster: Mapping[str, Mapping[str, Any]],
    absent: frozenset[str],
    excluded: frozenset[str],
) -> dict[str, Any]:
    standing = strategy["standing"]
    pool = list(strategy["rotation_pool"])
    rotation_count = strategy["rotation_count"]
    universe = [standing, *pool]
    unavailable = [item for item in universe if not _available(item, roster, absent, excluded)]
    substitutions: list[dict[str, str]] = []
    missing: list[str] = []
    final_seats: list[str] = []
    seated: list[str] = []
    uncountable: list[dict[str, str]] = []
    applied_exceptions: list[Mapping[str, Any]] = []

    standing_seat = None
    if _available(standing, roster, absent, excluded):
        lawful, reason, records = _candidate_records(
            standing, seated, config, strategy_name
        )
        if lawful:
            standing_seat = standing
            _append_records(applied_exceptions, records)
        else:
            uncountable.append({"model": standing, "reason": reason or "invalid-seat"})
    if standing_seat is None:
        for candidate in strategy.get("standing_substitutes", []):
            lawful, reason, records = _candidate_records(
                candidate, seated, config, strategy_name
            )
            if _available(candidate, roster, absent, excluded) and lawful:
                standing_seat = candidate
                substitutions.append({"absent": standing, "replacement": candidate})
                _append_records(applied_exceptions, records)
                break
            if _available(candidate, roster, absent, excluded) and not lawful:
                uncountable.append({"model": candidate, "reason": reason or "invalid-seat"})
        if standing_seat is None:
            missing.append(standing)
    if standing_seat is not None:
        final_seats.append(standing_seat)
        seated.append(standing_seat)

    rotation: list[str] = []
    for candidate in pool:
        if len(rotation) == rotation_count:
            break
        if candidate in seated:
            continue
        lawful, reason, records = _candidate_records(
            candidate, seated, config, strategy_name
        )
        if _available(candidate, roster, absent, excluded) and lawful:
            rotation.append(candidate)
            seated.append(candidate)
            _append_records(applied_exceptions, records)
        elif _available(candidate, roster, absent, excluded) and not lawful:
            uncountable.append({"model": candidate, "reason": reason or "invalid-seat"})
    final_seats.extend(rotation)
    return {
        "required": strategy["required"],
        "panel": [standing, *rotation],
        "unavailable": unavailable,
        "substitutions": substitutions,
        "final_seats": final_seats,
        "missing": missing,
        "rotation_shortfall": rotation_count - len(rotation),
        "uncountable": uncountable,
        "applied_exception_records": applied_exceptions,
    }


def _review_lineage_count(
    config: Mapping[str, Any],
    roster: Mapping[str, Mapping[str, Any]],
    absent: frozenset[str],
    excluded: frozenset[str],
) -> int:
    writer = config["writer_assumed"]
    writer_lineage = config["model_lineages"][writer]
    authorized = set(config["same_family_authorization"]["seats"])
    return len(
        {
            config["model_lineages"][model_id]
            for model_id in config["models"]
            if _available(model_id, roster, absent, excluded)
            and model_id != writer
            and (
                config["model_lineages"][model_id] != writer_lineage
                or model_id in authorized
            )
        }
    )


def _apply_downgrades(
    config: Mapping[str, Any],
    strategy_name: str,
    selected: dict[str, Any],
    roster: Mapping[str, Mapping[str, Any]],
    absent: frozenset[str],
    excluded: frozenset[str],
) -> None:
    final_seats = selected["final_seats"]
    required = selected["required"]
    selected["seat_instances"] = [
        {"model": model_id, "agent": None, "kind": "model"}
        for model_id in final_seats
    ]
    selected["applied_downgrade_records"] = []
    if len(final_seats) >= required:
        return
    if _review_lineage_count(config, roster, absent, excluded) >= required:
        return

    for record in config["downgrade_records"]:
        if len(final_seats) >= required:
            break
        model_id = record["model"]
        if strategy_name not in record["scope"] or model_id not in final_seats:
            continue
        instances = [
            item for item in selected["seat_instances"] if item["model"] == model_id
        ]
        if not instances:
            continue
        if instances[0]["agent"] is None:
            instances[0]["agent"] = record["agents"][0]
        used_agents = {
            item["agent"] for item in instances if item["agent"] is not None
        }
        added = False
        for agent in record["agents"]:
            if len(final_seats) >= required:
                break
            if agent in used_agents:
                continue
            final_seats.append(model_id)
            selected["seat_instances"].append(
                {"model": model_id, "agent": agent, "kind": "downgrade"}
            )
            used_agents.add(agent)
            added = True
            if selected["missing"]:
                selected["missing"].pop(0)
            elif selected["rotation_shortfall"]:
                selected["rotation_shortfall"] -= 1
        if added:
            selected["applied_downgrade_records"].append(record)


def resolve(
    config: Mapping[str, Any],
    size: str,
    risk_areas: Iterable[str],
    absent_models: Iterable[str],
    roster: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Resolve seats without I/O from validated configuration and roster data."""

    normalized_risks = sorted(set(risk_areas))
    risk_state = "present" if normalized_risks else "absent"
    if (
        risk_state == "absent"
        and size in config["floor3"]["sizes"]
        and config["floor3"]["effective"] is False
    ):
        strategy_name = config["floor3"]["pre_effect_strategy"]
    else:
        strategy_name = config["rule_table"][size][risk_state]
    strategy = config["panel_strategies"][strategy_name]
    absent = frozenset(absent_models)
    excluded = frozenset(config["excluded_models"])
    if strategy["type"] == "fixed":
        selected = _fixed_panel(
            config, strategy_name, strategy, roster, absent, excluded
        )
    else:
        selected = _standing_rotation(
            config, strategy_name, strategy, roster, absent, excluded
        )

    _apply_downgrades(
        config, strategy_name, selected, roster, absent, excluded
    )

    final_seats = selected["final_seats"]
    required = selected["required"]
    quorum_met = len(final_seats) == required
    authorization = config["same_family_authorization"]
    same_family = (
        set(authorization["seats"])
        if authorization["writer"] == config["writer_assumed"]
        else set()
    )
    return {
        "size": size,
        "risk_areas": normalized_risks,
        "risk_override": bool(normalized_risks),
        "strategy": strategy_name,
        "selection_path": strategy["selection_path"],
        **selected,
        "same_family_seats": [item for item in final_seats if item in same_family],
        "writer_assumed": config["writer_assumed"],
        "quorum_met": quorum_met,
        "status": "GO" if quorum_met else "SEAT-WAIT",
        "note": "" if quorum_met else config["notes"]["seat_wait"],
        "availability_note": config["notes"]["availability"],
        "writer_note": config["notes"]["writer"],
        "citations": list(config["citations"]),
        "rules_version": config["rules_version"],
    }


def _required_seats(given: Mapping[str, Any], config: Mapping[str, Any]) -> int:
    size = given["size"]
    if given.get("high_risk") is True:
        strategy_name = config["rule_table"][size]["present"]
    elif size in config["floor3"]["sizes"]:
        floor = given.get("member_floor3")
        if isinstance(floor, Mapping) and floor.get("effective") is False:
            strategy_name = config["floor3"]["pre_effect_strategy"]
        else:
            strategy_name = config["rule_table"][size]["absent"]
    else:
        strategy_name = config["rule_table"][size]["absent"]
    return config["panel_strategies"][strategy_name]["required"]


def _validate_panel_given(given: Mapping[str, Any], config: Mapping[str, Any]) -> None:
    if not isinstance(given, Mapping):
        raise ValueError("panel given must be an object")
    if given.get("size") not in config["sizes"] or not isinstance(given.get("high_risk"), bool):
        raise ValueError("panel size/high_risk is invalid")
    writer = given.get("writer")
    if writer is not None:
        if not isinstance(writer, Mapping) or set(writer) != {"model", "lineage"}:
            raise ValueError("writer must contain model and lineage")
        if writer["model"] not in config["model_lineages"]:
            raise ValueError("writer model is not configured")
        if config["model_lineages"][writer["model"]] != writer["lineage"]:
            raise ValueError("writer lineage disagrees with model_lineages")
    seats = given.get("seats")
    if not isinstance(seats, list):
        raise ValueError("seats must be an array")
    seat_keys = {"model", "lineage", "agent", "downgrade", "role_conflict"}
    for index, seat in enumerate(seats):
        if not isinstance(seat, Mapping) or not {"model", "lineage"}.issubset(seat) or set(seat) - seat_keys:
            raise ValueError(f"seat {index} has an invalid shape")
        model_id = seat["model"]
        lineage = seat["lineage"]
        if not isinstance(model_id, str) or model_id not in config["model_lineages"]:
            raise ValueError(f"seat {index} model is not configured")
        if not isinstance(lineage, str) or config["model_lineages"][model_id] != lineage:
            raise ValueError(f"seat {index} lineage disagrees with model_lineages")
        if "agent" in seat and (not isinstance(seat["agent"], str) or not seat["agent"]):
            raise ValueError(f"seat {index} agent is invalid")
        if "role_conflict" in seat and seat["role_conflict"] not in config["conformance"]["role_conflicts"]:
            raise ValueError(f"seat {index} role_conflict is invalid")
        if "downgrade" in seat:
            downgrade = seat["downgrade"]
            fields = config["conformance"]["downgrade_fields"]
            if not isinstance(downgrade, Mapping) or set(downgrade) != set(fields):
                raise ValueError(f"seat {index} downgrade is malformed")
            if any(not isinstance(downgrade[field], bool) for field in fields):
                raise ValueError(f"seat {index} downgrade flags must be boolean")
    distinct = given.get("distinct_lineages_available")
    if distinct is not None and (
        not isinstance(distinct, int) or isinstance(distinct, bool) or distinct < 0
    ):
        raise ValueError("distinct_lineages_available is invalid")
    review = given.get("review_record")
    if review is not None:
        if not isinstance(review, Mapping) or set(review) - {"cites_correlated_seats", "requested_actual_present"}:
            raise ValueError("review_record is malformed")
        if "cites_correlated_seats" in review and review["cites_correlated_seats"] not in {True, False, None}:
            raise ValueError("review_record.cites_correlated_seats is invalid")
        if "requested_actual_present" in review and not isinstance(review["requested_actual_present"], bool):
            raise ValueError("review_record.requested_actual_present is invalid")
    record = given.get("exception_record")
    if record is not None:
        allowed = {
            "present", "fields_present", "scope_covers_lane",
            "scope", "pair", "reason", "approved_by", "date", "writer_condition",
        }
        if not isinstance(record, Mapping) or set(record) - allowed:
            raise ValueError("exception_record is malformed")
        if not isinstance(record.get("present"), bool):
            raise ValueError("exception_record.present must be boolean")
        fields = record.get("fields_present")
        if not isinstance(fields, list) or any(not isinstance(item, str) for item in fields) or len(set(fields)) != len(fields):
            raise ValueError("exception_record.fields_present is invalid")
        if not set(fields).issubset(config["conformance"]["exception_fields"]):
            raise ValueError("exception_record.fields_present contains an unknown field")
        if not isinstance(record.get("scope_covers_lane"), bool):
            raise ValueError("exception_record.scope_covers_lane must be boolean")
        for field in fields:
            if field not in record:
                raise ValueError(f"exception_record.{field} value is missing")
        for field in ("scope", "reason", "approved_by"):
            if field in fields and (not isinstance(record[field], str) or not record[field].strip()):
                raise ValueError(f"exception_record.{field} is invalid")
        if "date" in fields:
            try:
                parsed_date = date.fromisoformat(record["date"])
            except (TypeError, ValueError) as exc:
                raise ValueError("exception_record.date is invalid") from exc
            if parsed_date.isoformat() != record["date"]:
                raise ValueError("exception_record.date is invalid")
        if "writer_condition" in fields:
            expected_writer = writer.get("model") if isinstance(writer, Mapping) else None
            if record.get("writer_condition") != expected_writer:
                raise ValueError("exception_record.writer_condition does not match writer")
        if "pair" in fields:
            pair = record["pair"]
            if not isinstance(pair, list) or len(pair) != 2 or any(item not in config["models"] for item in pair) or pair[0] == pair[1]:
                raise ValueError("exception_record.pair is invalid")
            if config["model_lineages"][pair[0]] != config["model_lineages"][pair[1]]:
                raise ValueError("exception_record.pair is not correlated")


def _valid_exception(
    given: Mapping[str, Any],
    policy: Mapping[str, Any],
    writer_model: str | None,
    pair: tuple[str, str],
) -> bool:
    record = given.get("exception_record", {})
    review = given.get("review_record", {})
    return (
        record.get("present") is True
        and set(record.get("fields_present", [])) == set(policy["exception_fields"])
        and record.get("scope_covers_lane") is True
        and record.get("writer_condition") == writer_model
        and ("pair" not in record or set(record["pair"]) == set(pair))
        and review.get("cites_correlated_seats") is True
    )


def evaluate_panel(given: Mapping[str, Any], config: Mapping[str, Any]) -> dict[str, Any]:
    """Evaluate a normalized panel fact set against generic law inputs."""

    _validate_panel_given(given, config)
    policy = config["conformance"]
    required = _required_seats(given, config)
    writer = given.get("writer") or {}
    seats = list(given.get("seats", []))
    countable = [
        seat
        for seat in seats
        if seat.get("model") != writer.get("model")
        and seat.get("role_conflict") not in set(policy["role_conflicts"])
    ]
    distinct_available = given.get("distinct_lineages_available", required)
    credited = 0
    seen_models: Counter[str] = Counter()
    seen_lineages: Counter[str] = Counter()
    seen_agents: dict[str, set[str]] = {}

    for seat in countable:
        model = seat.get("model")
        lineage = seat.get("lineage")
        seen_models[model] += 1
        agent = seat.get("agent")
        model_agents = seen_agents.setdefault(model, set())
        if seen_models[model] > 1:
            downgrade = seat.get("downgrade", {})
            valid_downgrade = (
                distinct_available < required
                and all(downgrade.get(field) is True for field in policy["downgrade_fields"])
                and agent is not None
                and agent not in model_agents
            )
            if valid_downgrade:
                credited += 1
            if agent is not None:
                model_agents.add(agent)
            continue
        if agent is not None:
            model_agents.add(agent)
        seen_lineages[lineage] += 1
        if seen_lineages[lineage] > 1:
            prior_model = next(
                item["model"]
                for item in countable
                if item["model"] != model and item["lineage"] == lineage
            )
            if not _valid_exception(
                given, policy, writer.get("model"), (prior_model, model)
            ):
                continue
        credited += 1

    lawful = credited >= required
    return {
        "required_seats": required,
        "lawful": lawful,
        "failure_class": None if lawful else "underseated",
    }


def evaluate_seat_wait(given: Mapping[str, Any], config: Mapping[str, Any]) -> dict[str, Any]:
    policy = config["conformance"]
    record = given.get("seat_wait", {})
    valid = (
        record.get("target") == policy["seat_wait_target"]
        and set(policy["seat_wait_fields"]).issubset(record.get("fields_present", []))
    )
    return {"valid": valid, "failure_class": None if valid else "invalid-seat-wait"}


def evaluate_record(given: Mapping[str, Any], config: Mapping[str, Any]) -> dict[str, Any]:
    record = given.get("review_record", {})
    valid = record.get("requested_actual_present") is True
    return {"valid": valid, "failure_class": None if valid else "invalid-record"}
