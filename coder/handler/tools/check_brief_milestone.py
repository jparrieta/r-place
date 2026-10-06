#!/usr/bin/env python3
"""Read-only verifier for the first N briefs in an Atlas Yard queue."""

import argparse
import importlib.util
import json
import sys
from pathlib import Path


DEFAULT_YARD = Path(__file__).resolve().parents[1]
EXPECTED_MODEL = "gpt-5.6-sol"
QUEUE_SIZE = 395

# Importing the yard helper must not leave bytecode in the source yard, even when
# the caller did not set PYTHONDONTWRITEBYTECODE.
sys.dont_write_bytecode = True


class InputError(Exception):
    """The yard cannot be interpreted safely."""


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise InputError(f"missing file: {path}") from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise InputError(f"cannot read JSON {path}: {exc}") from exc


def load_room_helper(yard):
    path = yard / "_tools" / "room.py"
    if not path.is_file():
        raise InputError(f"missing room helper: {path}")
    try:
        spec = importlib.util.spec_from_file_location("atlas_yard_room_readonly", path)
        if spec is None or spec.loader is None:
            raise ImportError("no loader available")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as exc:
        raise InputError(f"cannot load room helper {path}: {exc}") from exc
    helper = getattr(module, "_brief_validation", None)
    if not callable(helper):
        raise InputError(f"room helper has no _brief_validation: {path}")
    return helper


def validate_queue(queue, count):
    if not isinstance(queue, dict) or not isinstance(queue.get("rooms"), list):
        raise InputError("BRIEF-QUEUE.json must contain a rooms list")
    rows = queue["rooms"]
    if len(rows) != QUEUE_SIZE:
        raise InputError(f"queue must contain {QUEUE_SIZE} rooms; found {len(rows)}")
    if not 1 <= count <= QUEUE_SIZE:
        raise InputError(f"count must be between 1 and {QUEUE_SIZE}")

    previous_items = None
    seen_subs = set()
    for expected_rank, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            raise InputError(f"queue row {expected_rank} is not an object")
        if row.get("rank") != expected_rank:
            raise InputError(
                f"queue ranks must be sequential; row {expected_rank} has rank {row.get('rank')!r}"
            )
        sub = row.get("sub")
        if not isinstance(sub, str) or not sub or sub in seen_subs:
            raise InputError(f"queue rank {expected_rank} has an invalid or duplicate sub")
        seen_subs.add(sub)
        items = row.get("items_in_window")
        if isinstance(items, bool) or not isinstance(items, int) or items < 0:
            raise InputError(f"queue rank {expected_rank} has invalid items_in_window")
        if previous_items is not None and items < previous_items:
            raise InputError("queue is not ascending by items_in_window (97h)")
        previous_items = items
        if row.get("work") not in {"writer", "harness"}:
            raise InputError(f"queue rank {expected_rank} has invalid work value")
        if not isinstance(row.get("status"), str) or not row["status"]:
            raise InputError(f"queue rank {expected_rank} has invalid status")
    return rows[:count]


def transcript_models(path):
    if not path.is_file():
        return None
    models = set()
    try:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise InputError(f"malformed JSONL {path}:{line_number}: {exc}") from exc
                if not isinstance(record, dict):
                    raise InputError(f"JSONL record is not an object: {path}:{line_number}")
                if record.get("type") == "turn_context":
                    payload = record.get("payload")
                    if not isinstance(payload, dict):
                        raise InputError(f"turn_context payload is not an object: {path}:{line_number}")
                    model = payload.get("model")
                    if not isinstance(model, str) or not model:
                        raise InputError(f"turn_context model is empty: {path}:{line_number}")
                    models.add(model)
    except (OSError, UnicodeError) as exc:
        raise InputError(f"cannot read transcript {path}: {exc}") from exc
    return models


def proof_summary(validation):
    receipt = validation.get("receipt") if isinstance(validation.get("receipt"), dict) else {}
    proof = {
        "status": validation.get("status"),
        "current": validation.get("current") is True,
        "passed": validation.get("passed") is True,
    }
    checked = receipt.get("checked_at") or receipt.get("checked_utc")
    digest = receipt.get("digest")
    if checked:
        proof["checked_at"] = checked
    if digest:
        proof["digest"] = digest
    return proof


def inspect_room(yard, row, brief_validation):
    room = yard / "rooms" / row["sub"]
    state_path = room / "STATE.json"
    state = load_json(state_path)
    if not isinstance(state, dict):
        raise InputError(f"STATE must be an object: {state_path}")

    reasons = []
    if state.get("prior_runs"):
        reasons.append("prior_runs_present")
    if row["status"] != "verified":
        reasons.append(f"queue_status:{row['status']}")

    brief_path = room / "brief" / "out" / "brief.md"
    if not brief_path.is_file():
        reasons.append("brief_missing")
    try:
        validation = brief_validation(str(room))
    except Exception as exc:
        raise InputError(f"brief validation helper failed for {row['sub']}: {exc}") from exc
    if not isinstance(validation, dict):
        raise InputError(f"brief validation helper returned invalid data for {row['sub']}")
    proof = proof_summary(validation)
    if not (proof["current"] and proof["passed"]):
        reasons.append(f"validation:{proof['status'] or 'invalid'}")

    if row["work"] == "writer":
        path = room / "brief" / "out" / "_transcript.jsonl"
        models = transcript_models(path)
        if models is None:
            model_status = {"status": "missing", "models": []}
            reasons.append("transcript_missing")
        elif not models:
            model_status = {"status": "no_turn_context_models", "models": []}
            reasons.append("transcript_no_turn_context_models")
        elif models != {EXPECTED_MODEL}:
            listed = sorted(models)
            model_status = {"status": "mismatch", "models": listed}
            reasons.append("writer_models:" + ",".join(listed))
        else:
            model_status = {"status": "passed", "models": [EXPECTED_MODEL]}
    else:
        model_status = {"status": "not_applicable"}

    report = {
        "rank": row["rank"],
        "sub": row["sub"],
        "work": row["work"],
        "model_status": model_status,
        "proof": proof,
    }
    return report, reasons


def emit(value):
    print(json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--yard",
        type=Path,
        default=DEFAULT_YARD,
        help=f"Atlas Yard root (default: {DEFAULT_YARD})",
    )
    parser.add_argument("--count", type=int, default=10, help="leading queue rooms required (default: 10)")
    args = parser.parse_args(argv)

    try:
        yard = args.yard.expanduser().resolve()
        queue = load_json(yard / "BRIEF-QUEUE.json")
        selected = validate_queue(queue, args.count)
        brief_validation = load_room_helper(yard)
        rooms = []
        pending = []
        for row in selected:
            report, reasons = inspect_room(yard, row, brief_validation)
            rooms.append(report)
            if reasons:
                pending.append({"rank": row["rank"], "sub": row["sub"], "reasons": reasons})
    except InputError as exc:
        emit({"error": str(exc), "ready": False})
        return 2

    verified_current = sum(
        1
        for row, report in zip(selected, rooms)
        if row["status"] == "verified" and report["proof"]["current"] and report["proof"]["passed"]
    )
    result = {
        "ready": not pending,
        "verified_current": verified_current,
        "count": args.count,
        "pending": pending,
        "rooms": rooms,
    }
    emit(result)
    return 0 if result["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
