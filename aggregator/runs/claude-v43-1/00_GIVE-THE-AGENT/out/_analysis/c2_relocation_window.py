#!/usr/bin/env python3
"""C2, pass 2: the relocation window test declared in notes-C2.md (pass 2, before any count), for
_questions/relocation-renewed-calls.md. Read-only.

For each room carrying both a move (element P10) and TO (P01 calls, then P03 build reports): t0 is the hour of its first
move concept; the room counts only if 6 <= t0 <= 67, so both six-hour windows lie inside the placement period. Three
shares are reported:
- rooms with a TO concept in (t0, t0 + 6];
- rooms with a TO concept in (t0 - 6, t0];
- the control at the same hours: for each moving room, the share of all other rooms carrying TO that have a TO concept in
  (t0, t0 + 6]; averaged over the moving rooms.
Reading 1 (a move does not send a room back to recruiting) holds if the share after is below both the share before and
the control; Reading 2 holds if the share after is at or above the share before. Counts of TO concepts in each window
are given beside, and the rooms with a TO concept after the move are listed.

    python3 out/_analysis/c2_relocation_window.py
"""
import collections, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
W = 6.0
els = dict((e["id"], e) for e in json.load(open(os.path.join(OUT, "_analysis", "c2_elements_p2.json"), encoding="utf-8"))["elements"])
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--grep", ".", "--json", "--limit",
                    "10000000"], cwd=ROOT, capture_output=True, text=True)
codes = dict(((c["sub"], c["code_id"]), c) for c in (json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")))
rows = [json.loads(l) for l in open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8") if l.strip()]


def hours_by_room(el):
    out = collections.defaultdict(list)
    for r in rows:
        for t, ids in (r.get("support_by_theme") or {}).items():
            if t in el["themes"]:
                for i in ids:
                    c = codes.get((r["sub"], i))
                    if c and c.get("hour") is not None:
                        out[r["sub"]].append(c["hour"])
    return out


move = hours_by_room(els["P10"])
for to in ("P01", "P03"):
    T = hours_by_room(els[to])
    rooms = sorted(s for s in move if s in T and 6 <= min(move[s]) <= 67)
    after = before = 0
    n_after = n_before = 0
    ctrl = []
    listed = []
    for s in rooms:
        t0 = min(move[s])
        a_ = [h for h in T[s] if t0 < h <= t0 + W]
        b_ = [h for h in T[s] if t0 - W < h <= t0]
        after += bool(a_)
        before += bool(b_)
        n_after += len(a_)
        n_before += len(b_)
        if a_:
            listed.append("%s (t0 h%.1f, %d after, %d before)" % (s, t0, len(a_), len(b_)))
        others = [x for x in T if x != s]
        ctrl.append(sum(1 for x in others if any(t0 < h <= t0 + W for h in T[x])) / float(len(others)))
    n = len(rooms)
    print("\n== a move (P10) and %s: %d rooms with both and a first move between h6 and h67" % (to, n))
    print("share with %s in the six hours after the first move: %d of %d (%.3f); concepts %d" % (to, after, n, after / float(n), n_after))
    print("share with %s in the six hours before: %d of %d (%.3f); concepts %d" % (to, before, n, before / float(n), n_before))
    print("control, other rooms carrying %s with one in the same six hours after, averaged: %.3f" % (to, sum(ctrl) / len(ctrl)))
    verdict = ("Reading 1 (fewer after than before and than the control)" if after < before and after / float(n) < sum(ctrl) / len(ctrl)
               else "Reading 2 (after at or above before)" if after >= before else "neither reading cleanly (after below before, not below the control)")
    print("by the declared rule: %s" % verdict)
    print("rooms with %s after the first move: %s" % (to, "; ".join(listed)))
