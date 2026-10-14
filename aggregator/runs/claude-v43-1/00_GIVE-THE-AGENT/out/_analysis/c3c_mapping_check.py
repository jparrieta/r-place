#!/usr/bin/env python3
"""C3c: check mapping-C3.jsonl against fourth/fourth.jsonl (every fourth-order theme once, no other id), and print, for
each of the four universal problems and for none, the themes it holds with their names, and the union of rooms
carrying any member of those themes (from `mem.py rooms --with`), so counts in literature-C3.md are read, not typed.
Reads my own files and the store through mem.py; writes nothing.

    python3 out/_analysis/c3c_mapping_check.py
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
t4 = {r["id"]: r for r in (json.loads(l) for l in open(os.path.join(OUT, "fourth", "fourth.jsonl"), encoding="utf-8"))}
mp = [json.loads(l) for l in open(os.path.join(OUT, "mapping-C3.jsonl"), encoding="utf-8") if l.strip()]
ids = [m["fourth"] for m in mp]
print("lines %d; themes in tier %d; missing %s; extra %s; repeated %s" % (
    len(mp), len(t4), sorted(set(t4) - set(ids)), sorted(set(ids) - set(t4)),
    sorted(i for i in set(ids) if ids.count(i) > 1)))
bad = [m["fourth"] for m in mp if m["problem"] not in ("division", "allocation", "reward", "information", "none")
       or not m.get("why") or (m["problem"] != "none" and not m.get("cannot_do"))]
print("lines failing the form: %s" % bad)


def rooms_with(tid):
    # plain text: a header "rooms with <id>: N of 705", then one indented room per line; paged, so ask for all
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "rooms", "--with", tid,
                        "--limit", "2000"], cwd=ROOT, capture_output=True, text=True)
    n = int(re.search(r"rooms with \S+: (\d+) of", p.stdout).group(1))
    got = set(re.findall(r"^  (\S+)\s*$", p.stdout, re.M))
    if len(got) != n:
        sys.exit("%s: header says %d rooms, parsed %d" % (tid, n, len(got)))
    return got


everyone = set()
for prob in ("division", "allocation", "reward", "information", "none"):
    ms = [m for m in mp if m["problem"] == prob]
    u = set()
    for m in ms:
        r = rooms_with(m["fourth"])
        u |= r
        print("  %-11s %s %-28s %3d rooms%s" % (prob, m["fourth"], t4[m["fourth"]]["name"], len(r),
                                               " (by construction)" if m.get("by_construction") else ""))
    if prob != "none":
        everyone |= u
    print("%s: %d themes; rooms carrying any: %d" % (prob, len(ms), len(u)))
print("rooms carrying any mapped theme: %d" % len(everyone))
