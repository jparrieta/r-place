#!/usr/bin/env python3
"""status.py — rebuild STATUS.tsv from every room's STATE.json (after refreshing each).

    python3 _tools/status.py [--yard .] [--no-refresh]

One line per room, tab-separated, sorted by items in the window, largest first. The scheduler
runs this after every step it takes; the file is the yard's face and is never edited by hand.
"""
import argparse, glob, json, os, subprocess, sys, time


def write_file(path, data, aside=None):
    """Write data to path, replacing the file. On a mount that refuses to open an existing
    file for writing (some synced folders do), rename the old file aside (into `aside`, or
    beside it as .old) and write a new one."""
    mode = "wb" if isinstance(data, bytes) else "w"
    try:
        with open(path, mode, encoding=None if mode == "wb" else "utf-8") as fh:
            fh.write(data)
        return "written"
    except PermissionError:
        if not os.path.exists(path):
            raise
        if aside:
            os.makedirs(aside, exist_ok=True)
            dst = os.path.join(aside, os.path.basename(path) + ".%d" % int(time.time() * 1000))
        else:
            dst = path + ".old"
        os.replace(path, dst)
        with open(path, mode, encoding=None if mode == "wb" else "utf-8") as fh:
            fh.write(data)
        return "replaced"

HERE = os.path.dirname(os.path.abspath(__file__))
COLS = ["sub", "items_in_window", "threads", "brief", "expected_branch", "branch", "slices", "stage",
        "model", "started", "finished", "verdict", "codes", "themes", "verified_utc",
        "run_agent_specs", "run_agent_token_totals", "run_total_tokens", "run_usage_complete",
        "lead_archive", "lead_archive_sha256", "lead_archive_bytes",
        "lead_archive_history", "run_archive", "run_archive_sha256", "run_archive_bytes",
        "materials_archive", "materials_archive_sha256", "materials_archive_bytes",
        "coded_before", "coded_under", "coded_by", "in_v35_package", "last_note"]


def prior_columns(st):
    """What was done to this room before the yard: from STATE.json's prior_runs, written by
    _tools/prior_runs.py. Coder runs only; the hub runs stay in PRIOR-RUNS.tsv."""
    runs = [r for r in st.get("prior_runs") or [] if r.get("kind") == "coder"]
    runs.sort(key=lambda r: r.get("started_utc") or "")
    def name(r):
        n = r["run"].replace(".tar.gz", "")
        if "_contaminated" in (r.get("path") or ""):
            n += " (contaminated start)"
        elif r.get("complete") != "yes":
            n += " (partial)"
        return n
    st["coded_before"] = "; ".join(name(r) for r in runs)
    st["coded_under"] = "; ".join(r.get("instrument") or "?" for r in runs)
    st["coded_by"] = "; ".join(r.get("model") or "unrecorded" for r in runs)
    st["in_v35_package"] = "yes" if any(r.get("in_v35_package") == "yes" for r in runs) else "no"


def run_columns(room, st):
    """Flatten the immutable verified-run receipt into one TSV row.

    Each receipt names the lead and every ephemeral fleet batch and carries the
    token report captured from that agent's own transcript.  Keeping the fields
    here, rather than in a separate report, makes STATUS.tsv the live ledger the
    scheduler and reviewers can compare without following store paths.
    """
    receipt_path = os.path.join(room, "validation", "RUN-RECEIPT.json")
    if not os.path.exists(receipt_path):
        return
    try:
        receipt = json.load(open(receipt_path, encoding="utf-8"))
    except (OSError, ValueError):
        return
    model = receipt.get("model") or st.get("lead_model") or "unrecorded"
    effort = receipt.get("effort") or "unrecorded"
    usage = receipt.get("reported_usage_by_agent") or {}
    names = sorted(usage, key=lambda name: (name != "case-lead", name))
    st["run_agent_specs"] = "; ".join("%s=%s/%s" % (name, model, effort) for name in names)
    st["run_agent_token_totals"] = "; ".join(
        "%s=%s" % (name, info.get("total_tokens", "unreported"))
        for name, info in ((name, usage.get(name) or {}) for name in names))
    st["run_total_tokens"] = receipt.get("reported_total_tokens", "")
    st["run_usage_complete"] = receipt.get("usage_complete", "")


def active_queue_columns(yard, st):
    """Add active worker specs before a receipt exists."""
    if st.get("run_agent_specs"):
        return
    for dirname, label in (("_repair_queue", "active-repair"), ("_coding_queue", "active-coding")):
        state_path = os.path.join(yard, dirname, "STATE.json")
        if not os.path.exists(state_path):
            continue
        try:
            queue_state = json.load(open(state_path, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        active = (queue_state.get("active") or {}).get(st.get("sub")) or {}
        model = active.get("model") or (queue_state.get("model") if active else "")
        effort = active.get("effort") or (queue_state.get("effort") if active else "")
        if not model and active:
            model, effort = "gpt-5.6-sol", "medium"
        if not model:
            continue
        effort = effort or "unrecorded"
        st["model"] = model
        st["started"] = active.get("started_utc", st.get("started", ""))
        st["run_agent_specs"] = "%s=%s/%s" % (label, model, effort)
        st["run_usage_complete"] = "running"
        return


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--yard", default=".")
    ap.add_argument("--no-refresh", action="store_true")
    a = ap.parse_args()
    yard = os.path.abspath(a.yard)
    rows = []
    for room in sorted(glob.glob(os.path.join(yard, "rooms", "*"))):
        sp = os.path.join(room, "STATE.json")
        if not os.path.exists(sp):
            continue
        if not a.no_refresh:
            subprocess.run(["python3", os.path.join(HERE, "room.py"), "status", "--room", room],
                           capture_output=True, text=True)
        st = json.load(open(sp, encoding="utf-8"))
        st["last_note"] = (st.get("notes") or [{}])[-1].get("note", "") if st.get("notes") else ""
        prior_columns(st)
        run_columns(room, st)
        active_queue_columns(yard, st)
        rows.append(st)
    rows.sort(key=lambda r: -(r.get("items_in_window") or 0))
    out = os.path.join(yard, "STATUS.tsv")
    text = "\t".join(COLS) + "\n" + "".join(
        "\t".join(str(r.get(c, "") if r.get(c) is not None else "") for c in COLS) + "\n" for r in rows)
    write_file(out, text)
    write_file(os.path.join(yard, "status.tsv"), text)
    stages = {}
    for r in rows:
        k = (r.get("stage") or "?").split(",")[0].split(" of ")[0]
        stages[k] = stages.get(k, 0) + 1
    print("%d rooms -> %s" % (len(rows), os.path.relpath(out, yard)))
    for k, v in sorted(stages.items(), key=lambda kv: -kv[1]):
        print("  %4d  %s" % (v, k))
    return 0


if __name__ == "__main__":
    sys.exit(main())
