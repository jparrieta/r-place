#!/usr/bin/env python3
"""D2a §3: ten room models drawn by seed, stratified on the room verdict, and the mechanical checks on each. The
rule was logged before the draw (diary, D2a): seed 20261016; random.Random(SEED).sample over each stratum's sorted
rooms; two per stratum, or all of a smaller stratum; the remainder from the largest stratum.

    python3 out/_analysis/d2_sample.py           draw and print the checks
    python3 out/_analysis/d2_sample.py --write   also write out/_analysis/d2_sample.json (refuses if it exists)

Per room, from out/rooms/<sub>/model-D.md, the room's ledger lines (counted by op and element, never printed) and the
store's codes: words; element and arrow ids cited; [absent <id>] markers; [new: ...] markers; adapted elements of the
ledger the file never names; concept citations, and those not in the room's codes; paragraphs and bullets that carry
no concept citation; the grade line with the sentence after it; local_status; the Local exceptions section.
"""
import collections, json, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
SEED, K, N = 20261016, 2, 10

V = [json.loads(l) for l in open(os.path.join(OUT, "verdicts-D.jsonl"), encoding="utf-8") if l.strip()]
strata = collections.defaultdict(list)
for v in V:
    vs = {r["verdict"] for r in v["readers"]}
    strata[vs.pop() if len(vs) == 1 else "split"].append(v["sub"])
rng = random.Random(SEED)
draw, take = {}, {}
for s in sorted(strata):
    take[s] = min(K, len(strata[s]))
take[max(strata, key=lambda s: len(strata[s]))] += N - sum(take.values())
for s in sorted(strata):
    draw[s] = rng.sample(sorted(strata[s]), take[s])
print("strata %s; taken %s" % ({s: len(r) for s, r in sorted(strata.items())}, take))
print("drawn: %s" % draw)

codes = collections.defaultdict(set)
for l in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if not r.get("retracted"):
        codes[r["sub"]].add(r["code_id"])
want = {s for ss in draw.values() for s in ss}
led = collections.defaultdict(list)
for l in open(os.path.join(OUT, "adaptations.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r["sub"] in want:
        led[r["sub"]].append(r)
ID = re.compile(r"\b([PKCRA]\d{2})\b")
for stratum, subs in sorted(draw.items()):
    for sub in subs:
        t = open(os.path.join(OUT, "rooms", sub, "model-D.md"), encoding="utf-8").read()
        body = t.split("## Local exceptions")[0]
        cited = collections.Counter(ID.findall(t))
        absent = re.findall(r"\[absent ([PKCRA]\d{2})\]", t)
        new = re.findall(r"\[new:[^\]]*\]", t)
        cites = re.findall(r"\b(c\d{4})\b", t)
        bad = sorted({c for c in cites if c not in codes[sub]})
        blocks = [b.strip() for b in re.split(r"\n\s*\n|\n(?=- )", body) if b.strip() and not b.strip().startswith("#")]
        bare = [b for b in blocks if not re.search(r"\bc\d{4}\b", b)]
        ops = collections.Counter(r["op"] for r in led[sub])
        adapted = {r["element"] for r in led[sub] if r["element"] and r["op"] != "propose"}
        missing = sorted(e for e in adapted if e not in cited)
        g = re.search(r"^grade:.*$", t, re.M)
        after = t[g.end():].strip().split("\n")[0] if g else ""
        print("\n== %s (%s; readers %s; ledger lines %d)" % (
            sub, stratum, [r["verdict"] for v in V if v["sub"] == sub for r in v["readers"]], len(led[sub])))
        print("  words %d; ids cited %d distinct (%d mentions); [absent] %d; [new:] %d; concept citations %d, "
              "not in the room's codes %s" % (len(t.split()), len(cited), sum(cited.values()), len(absent), len(new),
                                              len(cites), bad))
        print("  ledger ops %s; adapted elements the file never names: %s" % (dict(ops.most_common()), missing))
        print("  paragraphs and bullets before Local exceptions: %d; without a concept citation: %d" % (len(blocks), len(bare)))
        print("  %s | next line: %s" % (g.group(0)[:200] if g else "no grade line", after[:300]))
        print("  local_status: %s; Local exceptions section: %s" % (
            (re.search(r"^local_status:\s*(\S+)", t, re.M) or [None, None])[1], "## Local exceptions" in t))
if "--write" in sys.argv:
    dest = os.path.join(OUT, "_analysis", "d2_sample.json")
    if os.path.exists(dest):
        sys.exit("d2_sample.json exists; not overwritten")
    json.dump({"seed": SEED, "rule": "two per verdict stratum, all of a smaller stratum, the remainder from the largest",
               "draw": draw}, open(dest, "w"), indent=1)
    print("wrote %s" % dest)
