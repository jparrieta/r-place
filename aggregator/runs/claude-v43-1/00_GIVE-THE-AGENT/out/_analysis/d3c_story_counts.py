#!/usr/bin/env python3
"""D3c, the counts read last, by version: the close-check's story figures (stage_D3.py lines 468 to 485) computed
three ways: on its own verdict map (the last analyst ruling per room in verdicts-D.jsonl, else the first-return
readers' agreed line), on the first return alone (e15f9647...) and on the re-check alone (46384686...). For each:
the last story's rooms by its verdict value, how they fare, and the composition rate of rooms read against any story
at C2 beside rooms never read against one. Also the four verdicts over 705 rooms. Read-only.

    python3 out/_analysis/d3c_story_counts.py
"""
import collections, glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


vr = jl(os.path.join(OUT, "verdicts-D.jsonl"))
first_r = {r["sub"]: r["verdict"] for r in vr if r.get("ruled_by") == "analyst" and not r.get("recheck")}
re_r = {r["sub"]: r["verdict"] for r in vr if r.get("ruled_by") == "analyst" and r.get("recheck")}
last_any = {}
for r in vr:
    if r.get("ruled_by") == "analyst":
        last_any[r["sub"]] = r["verdict"]


def agreed(rows):
    d = {}
    for r in rows:
        if r.get("ruled_by"):
            continue
        vs = {e["verdict"] for e in r["readers"]}
        d[r["sub"]] = vs.pop() if len(vs) == 1 else None
    return d


a1 = agreed(vr)
a2 = agreed(jl(os.path.join(OUT, "verdicts-recheck-D.jsonl")))
maps = {
    "close-check's map (mixed)": {s: last_any.get(s, a1[s]) for s in a1},
    "first return (e15f9647)": {s: first_r.get(s, a1[s]) for s in a1},
    "re-check (46384686)": {s: re_r.get(s, a2[s]) for s in a2},
}
stories = sorted(glob.glob(os.path.join(OUT, "story_rooms-p*.jsonl")),
                 key=lambda p: int(re.search(r"p(\d+)", os.path.basename(p)).group(1)))
last_all = jl(stories[-1])
last = [r for r in last_all if r.get("sub")]
print("lines with no room in the last story file:", [json.dumps(r)[:200] for r in last_all if not r.get("sub")])
read_any = set()
for p in stories:
    read_any |= {r.get("sub") for r in jl(p)}
print("last story file:", os.path.basename(stories[-1]), len(last), "rooms; its verdict values:",
      dict(collections.Counter(r.get("verdict") for r in last)))
comp = lambda v: v in ("composes", "composes-with-residue")
for name, v in maps.items():
    print("== %s: %s" % (name, dict(sorted(collections.Counter(v.values()).items(), key=str))))
    for val in sorted({r.get("verdict") for r in last}, key=str):
        rs = [r["sub"] for r in last if r.get("verdict") == val]
        print("   story %s (%d): %s; not composing: %s" % (val, len(rs), dict(collections.Counter(v.get(s) for s in rs)),
                                                        sorted((s, v.get(s)) for s in rs if not comp(v.get(s)))))
    ra = [s for s in v if s in read_any]
    nr = [s for s in v if s not in read_any]
    print("   rate read against a story: %d of %d (%.3f); never read: %d of %d (%.3f)" % (
        sum(comp(v[s]) for s in ra), len(ra), sum(comp(v[s]) for s in ra) / len(ra),
        sum(comp(v[s]) for s in nr), len(nr), sum(comp(v[s]) for s in nr) / len(nr)))
