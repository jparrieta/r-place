#!/usr/bin/env python3
"""C5c-02: rooms carrying any member of a set of third-order themes, before and after Stigmergy's recut, via
`mem.py rooms --with <T3> --limit 2000` (as c3c_rooms_per_theme.py counts). Member lists are read from
fourth/fourth.jsonl, so nothing is typed. Prints, for the old and the new membership: Collective representation
(T4-006), Stigmergy (T4-007), and the information-provision themes of F-016 (Sensemaking T4-003, Stigmergy T4-007,
Backstage decision-making T4-010, Attribution T4-019). Writes out/_analysis/c5c2_room_unions.json.

    python3 out/_analysis/c5c2_room_unions.py
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
fourth = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "fourth", "fourth.jsonl"), encoding="utf-8")
          if l.strip()}
MOVE = ["T3-041", "T3-060"]
cache = {}


def rooms(t3):
    if t3 not in cache:
        p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "rooms", "--with", t3, "--limit",
                            "2000"], cwd=ROOT, capture_output=True, text=True)
        n = int(re.search(r"rooms with \S+: (\d+) of", p.stdout).group(1))
        got = set(re.findall(r"^  (\S+)\s*$", p.stdout, re.M))
        if len(got) != n:
            sys.exit("%s: header says %d rooms, parsed %d" % (t3, n, len(got)))
        cache[t3] = got
    return cache[t3]


def union(ts):
    u = set()
    for t in ts:
        u |= rooms(t)
    return u


old = {k: list(v["members"]) for k, v in fourth.items()}
new = dict(old)
new["T4-007"] = [m for m in old["T4-007"] if m not in MOVE]
new["T4-006"] = old["T4-006"] + MOVE
out = {}
for label, mem in (("old", old), ("new", new)):
    cr, st = union(mem["T4-006"]), union(mem["T4-007"])
    info = union(mem["T4-003"] + mem["T4-007"] + mem["T4-010"] + mem["T4-019"])
    out[label] = {"T4-006": len(cr), "T4-007": len(st), "information": len(info)}
    print("%s: Collective representation %d rooms; Stigmergy %d; information provision (4 themes) %d" % (
        label, len(cr), len(st), len(info)))
for t in ["T3-038"] + MOVE:
    print("%s: %d rooms" % (t, len(rooms(t))))
    out[t] = len(rooms(t))
json.dump(out, open(os.path.join(OUT, "_analysis", "c5c2_room_unions.json"), "w"), indent=1)
