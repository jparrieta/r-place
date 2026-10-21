"""D3a-56 census of the verdict rulings (rules logged before it ran). Counts only; nothing is written."""
import collections, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
rows = [json.loads(l) for l in open(os.path.join(OUT, "verdicts-D.jsonl"), encoding="utf-8") if l.strip()]
ru = [r for r in rows if r.get("ruled_by") == "analyst"]
print("rulings:", len(ru), dict(collections.Counter(r["verdict"] for r in ru)))
pair = collections.Counter((" against ".join(sorted(set(r["changed_from"].values()))), r["verdict"]) for r in ru)
print("(1) by the readers' pair and the ruled verdict:")
for (p, v), n in sorted(pair.items()):
    print("   %s -> %s: %d" % (p, v, n))
ids = ["P%d" % n for n in range(23, 35)] + ["K05", "K06", "K07"]
cnt = collections.Counter()
wr = [r for r in ru if r["verdict"] == "composes-with-residue"]
for r in wr:
    named = set(re.findall(r"\b(P2[3-9]|P3[0-4]|K0[5-7])\b", r["reason"]))
    for i in named:
        cnt[i] += 1
print("(2) with-residue rulings (%d) naming each candidate as an act the served model lacked:" % len(wr))
for i in ids:
    print("   %s: %d" % (i, cnt[i]))
none = [r["sub"] for r in wr if not re.search(r"\b(P2[3-9]|P3[0-4]|K0[5-7])\b", r["reason"])]
print("   with-residue rulings naming no candidate:", none if none else "none")
odd = [r["sub"] for r in ru if r["verdict"] not in set(r["changed_from"].values())]
print("(3) rulings matching neither reader: %d %s" % (len(odd), odd))
