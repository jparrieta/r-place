"""D3b: the flagged re-check absent lines (every d3_rulings/recheck-absent-flagged*.jsonl, the first batch's and the
second's) still unruled, by element, with their flags and observation states. Counts only."""
import collections, glob, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ruled = {json.loads(l)["adaptation"] for l in open(os.path.join(OUT, "adjudications.jsonl"), encoding="utf-8") if l.strip()}
fl = [json.loads(l) for p in sorted(glob.glob(os.path.join(OUT, "_analysis", "d3_rulings", "recheck-absent-flagged*.jsonl")))
      for l in open(p, encoding="utf-8") if l.strip()]
un = [r for r in fl if r["adaptation"] not in ruled]
print("flagged %d; unruled %d" % (len(fl), len(un)))
by = collections.defaultdict(collections.Counter)
for r in un:
    by[r["element"]]["+".join(sorted(set(r["flags"])))] += 1
    by[r["element"]]["obs:" + str(r["observation"])] += 1
for e in sorted(by, key=lambda e: -sum(v for k, v in by[e].items() if k.startswith("obs:"))):
    c = by[e]
    print("%-5s %4d  %s" % (e, sum(v for k, v in c.items() if k.startswith("obs:")),
                            "  ".join("%s=%d" % kv for kv in sorted(c.items()))))
