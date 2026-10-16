#!/usr/bin/env python3
"""Counts for a field entry under 'The field's entries' (stage D3 section 4), from my own rulings
(via d3_group_rulings.py, the latest ruling per line).

Prints rooms by op as the labelers returned them (instantiate, restrict, contradict, absent), the
same by my rulings, the rooms where the element is shown (an accepted specification or elaboration
in any op, or an absent line rejected because its concepts show it), the rooms whose lines are all
evidence limits, and, for each --clause label=regex, the shown rooms whose ruling reasons match.

  python3 out/_analysis/d3_field_entry_counts.py --element P22 --clause cleanup='cleanup|final clean'
"""
import argparse
import re
import subprocess
import sys
from collections import defaultdict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--element", required=True)
    ap.add_argument("--clause", action="append", default=[])
    ap.add_argument("--ids", action="store_true")
    a = ap.parse_args()
    out = subprocess.run([sys.executable, "out/_analysis/d3_group_rulings.py", "--element", a.element],
                         capture_output=True, text=True).stdout
    latest = {}
    for ln in out.splitlines():
        parts = [p.strip() for p in ln.split("|")]
        if len(parts) < 6 or parts[0] == "id":
            continue
        latest[parts[0]] = {"op": parts[1], "decision": parts[2], "kind": parts[3],
                            "reason": "|".join(parts[5:])}
    room = lambda i: i.rsplit("-", 1)[0]
    returned, shown, limit_only = defaultdict(set), set(), defaultdict(set)
    ruled = defaultdict(set)
    for i, r in latest.items():
        returned[r["op"]].add(room(i))
        is_shown = (r["decision"] == "accept" and r["kind"] in ("specification", "elaboration")
                    and not (r["op"] == "absent")) or (r["op"] == "absent" and r["decision"] == "reject")
        if is_shown:
            shown.add(room(i))
            ruled["shown by " + r["op"]].add(room(i))
        if r["op"] == "absent" and r["decision"] == "accept" and r["kind"] == "specification":
            ruled["observed absent"].add(room(i))
        if r["op"] == "restrict" and r["decision"] == "accept" and r["kind"] == "correction":
            ruled["restricted (accepted correction)"].add(room(i))
        if r["op"] == "contradict" and r["decision"] == "accept":
            ruled["contradicted (accepted)"].add(room(i))
    rooms = {room(i) for i in latest}
    print(f"{a.element}: {len(latest)} lines in {len(rooms)} rooms")
    print("rooms by op as returned: " + ", ".join(f"{op} {len(s)}" for op, s in sorted(returned.items())))
    print("rooms by my rulings: " + ", ".join(f"{k} {len(s)}" for k, s in sorted(ruled.items())))
    print(f"rooms where the element is shown (any op): {len(shown)}")
    print(f"rooms with no line showing it: {len(rooms - shown)}")
    shown_rows = [(i, r) for i, r in latest.items() if room(i) in shown and (
        (r["decision"] == "accept" and r["kind"] in ("specification", "elaboration") and r["op"] != "absent")
        or (r["op"] == "absent" and r["decision"] == "reject"))]
    for c in a.clause:
        label, rx = c.split("=", 1)
        hit = sorted({room(i) for i, r in shown_rows if re.search(rx, r["reason"], re.I)})
        print(f"clause {label}: {len(hit)} rooms" + (": " + " ".join(hit) if a.ids else ""))


if __name__ == "__main__":
    main()
