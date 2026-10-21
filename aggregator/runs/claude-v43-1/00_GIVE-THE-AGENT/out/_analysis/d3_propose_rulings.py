#!/usr/bin/env python3
"""D3a-55: build the propose lines' ruling files from the spec rows (QD3-001: every id its own decision and reason).

Each spec row is id|CLASS|evidence. CLASS decides the ruling (G59, G59a):
  C-<GROUP>  accept, kind proposal, pair a line of another room in the same group; the reason names the candidate
  H-<ID>     reject, kind proposal; the element (or arrow) named holds the act
  NOT        reject, kind proposal; the codes do not show the act
  OUT        particular; outside the model's scope
  PART       particular; one room's, with no shared warrant
  P-G6       particular; the line is NONPORTABLE (G6)
Refuses on an unknown class, an unknown element or arrow, a C-group with no candidate, a candidate whose element is
not in elements.jsonl, or a group with no second room. Writes one rulings file per spec file into d3_rulings/,
named propose-rulings-<suffix>.jsonl, for d3_adjudicate_batch.py to check and write.

    python3 out/_analysis/d3_propose_rulings.py [--write]
"""
import argparse, collections, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
RD = os.path.join(OUT, "_analysis", "d3_rulings")
ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


READING = {"0000": 1, "0100": 2, "0200": 3, "0300": 4, "0400": 5, "0500": 6, "0600": 7, "0700": 8,
           "0800": 9, "0900": 10, "1000": 11, "1100": 12, "1200": 13, "1300": 14}
MOVE = {"P23": 182, "P24": 183, "P25": 184, "P26": 185, "P27": 186, "P28": 187, "P29": 188, "P30": 189,
        "P31": 190, "P32": 191, "P33": 192, "P34": 193, "K05": 194, "K06": 195, "K07": 196}
led = {l["id"]: l for l in jl(os.path.join(OUT, "adaptations.jsonl"))}
els = {e["id"] for e in jl(os.path.join(OUT, "model", "elements.jsonl"))}
arrows = {r["id"] for r in jl(os.path.join(OUT, "model", "arrows.jsonl"))}
cands = {c["class"]: c for c in json.load(open(os.path.join(RD, "propose-candidates.json"), encoding="utf-8"))}

specs = sorted(glob.glob(os.path.join(RD, "propose-spec-*.txt")))
rows = []
for s in specs:
    suf = re.search(r"propose-spec-(.+)\.txt$", s).group(1)
    for line in open(s, encoding="utf-8"):
        line = line.rstrip("\n")
        if line:
            i, cls, ev = line.split("|", 2)
            rows.append((suf, i, cls, ev))

errs = []
groups = collections.defaultdict(list)
for suf, i, cls, ev in rows:
    if i not in led or led[i].get("op") != "propose":
        errs.append("%s: not a propose line of the ledger" % i)
    if cls.startswith("C-"):
        if cls not in cands:
            errs.append("%s: class %s has no candidate" % (i, cls))
        elif cands[cls]["id"] not in els:
            errs.append("%s: candidate %s is not in elements.jsonl" % (i, cands[cls]["id"]))
        groups[cls].append(i)
    elif cls.startswith("H-"):
        x = cls[2:]
        if x not in els and x not in arrows:
            errs.append("%s: %s is neither an element nor an arrow" % (i, x))
    elif cls not in ("NOT", "OUT", "PART", "P-G6"):
        errs.append("%s: unknown class %s" % (i, cls))

pair = {}
for cls, ids in groups.items():
    for n, i in enumerate(ids):
        p = None
        for k in range(1, len(ids)):
            j = ids[(n + k) % len(ids)]
            if led[j]["sub"] != led[i]["sub"]:
                p = j
                break
        if p is None:
            errs.append("%s (%s): no line of another room in the group" % (i, cls))
        pair[i] = p
if errs:
    print("\n".join(errs[:40]))
    sys.exit("refused: nothing written")

out = collections.defaultdict(list)
for suf, i, cls, ev in rows:
    rd = ("G59's reading %d" % READING[suf]) if suf in READING else "G59's reading named in the row"
    if cls.startswith("C-"):
        c = cands[cls]
        r = {"adaptation": i, "decision": "accept", "kind": "proposal", "pair": pair[i],
             "reason": "G59 and G59a (%s): %s; the act is stated by no element's statement or range and by no arrow, and "
                       "other rooms show it; accepted as a proposal for candidate %s (%s), entered at D3a-55 by move %d"
                       % (rd, ev, c["id"], c["name"], MOVE[c["id"]])}
    elif cls.startswith("H-"):
        x = cls[2:]
        what = "arrow" if x in arrows else "element"
        r = {"adaptation": i, "decision": "reject", "kind": "proposal",
             "reason": "G59 and G59a (%s): %s; the %s %s holds the act by its statement or range, so the proposal adds "
                       "nothing the model lacks" % (rd, ev, what, x)}
    elif cls == "NOT":
        r = {"adaptation": i, "decision": "reject", "kind": "proposal",
             "reason": "G59 (%s): %s; the line's codes do not show the act it proposes" % (rd, ev)}
    elif cls == "OUT":
        r = {"adaptation": i, "decision": "particular", "kind": "particular",
             "reason": "G59 (%s): %s; outside the model's scope, since here the room did not organize or did something the "
                       "model is not about (stage section 4); this room's particular" % (rd, ev)}
    elif cls == "PART":
        r = {"adaptation": i, "decision": "particular", "kind": "particular",
             "reason": "G59 (%s): %s; a locally supported particular with no shared warrant (stage section 1)" % (rd, ev)}
    else:
        r = {"adaptation": i, "decision": "particular", "kind": "particular",
             "reason": "G59 and G6 (%s): %s; a particular by construction" % (rd, ev)}
    out[suf].append(r)

counts = collections.Counter(r["decision"] for v in out.values() for r in v)
print("rows %d in %d files; %s" % (sum(len(v) for v in out.values()), len(out), dict(counts)))
for cls in sorted(groups):
    print("  %s -> %s: %d accepted" % (cls, cands[cls]["id"], len(groups[cls])))
if not a.write:
    print("dry run: nothing written")
    sys.exit(0)
for suf, v in sorted(out.items()):
    p = os.path.join(RD, "propose-rulings-%s.jsonl" % suf)
    if os.path.exists(p):
        sys.exit("refused: %s exists; never overwrite" % p)
    with open(p, "w", encoding="utf-8") as f:
        for r in v:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("wrote %s (%d rows)" % (os.path.relpath(p, OUT), len(v)))
