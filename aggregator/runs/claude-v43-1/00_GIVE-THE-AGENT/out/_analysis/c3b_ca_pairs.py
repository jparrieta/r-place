#!/usr/bin/env python3
"""C3b, abductive read prompted by conversation analysis (adjacency pairs and preference organization; recalled:
Schegloff and Sacks 1973, Pomerantz 1984, Levinson 1983). A call to attack is a first pair part; a reply that joins it
is the preferred second, a reply that refuses it the dispreferred second. Prediction: refusals carry an account (a
stated reason) more often than acceptances, and are longer.

Pairs, from the store through `mem.py codes --fourth ... --json`:
  first part   a concept under T4-020 (Repertoire of contention, the attack element's theme) on an item;
  acceptance   a concept under T4-020 on an item replying (at any depth) to the first part's item, same thread, another
               author, later in time;
  refusal      a concept under T4-015 (Live and let live, the restraint element's theme) on such a replying item.
At most one acceptance and one refusal per room (the earliest), then a seeded sample (random.Random(20261014)) of up to
40 rooms per kind. Prints each sampled pair whole (first part, reply, interval in minutes, reply length in words) for
reading. Writes the sample to out/_analysis/c3b_ca_sample.json; writes nothing else.

    python3 out/_analysis/c3b_ca_pairs.py
"""
import collections, json, os, random, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DEST = os.path.join(OUT, "_analysis", "c3b_ca_sample.json")


def codes(t4):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--fourth", t4, "--json",
                        "--limit", "10000000"], cwd=ROOT, capture_output=True, text=True)
    return [json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")]


atk, res = codes("T4-020"), codes("T4-015")
need = ("sub", "code_id", "item_id", "thread_id", "coord", "hour", "author")
miss = [k for k in need if atk and k not in atk[0]]
if miss:
    sys.exit("codes --fourth --json lacks fields %s; fields are %s" % (miss, sorted(atk[0])))


def below(fc, tc):
    fc, tc = str(fc), str(tc)
    return (fc == "0" and tc != "0") or (fc != "0" and tc.startswith(fc + "."))


def ok(c):
    return c.get("thread_id") and c.get("coord") not in (None, "", "-") and c.get("hour") is not None


byth = collections.defaultdict(lambda: {"A": [], "R": []})
for c in atk:
    if ok(c):
        byth[(c["sub"], c["thread_id"])]["A"].append(c)
for c in res:
    if ok(c):
        byth[(c["sub"], c["thread_id"])]["R"].append(c)
pairs = {"acceptance": {}, "refusal": {}}
for (s, th), d in byth.items():
    for f in d["A"]:
        for kind, pool in (("acceptance", d["A"]), ("refusal", d["R"])):
            for t in pool:
                if t is f or t["item_id"] == f["item_id"]:
                    continue
                if below(f["coord"], t["coord"]) and t.get("author") != f.get("author") and t["hour"] > f["hour"]:
                    cur = pairs[kind].get(s)
                    if cur is None or (t["hour"], f["hour"]) < (cur[1]["hour"], cur[0]["hour"]):
                        pairs[kind][s] = (f, t)
print("rooms with a pair: acceptance %d, refusal %d" % (len(pairs["acceptance"]), len(pairs["refusal"])))
rnd = random.Random(20261014)
sample = {}
for kind in ("acceptance", "refusal"):
    rooms = sorted(pairs[kind])
    pick = sorted(rnd.sample(rooms, min(40, len(rooms))))
    sample[kind] = []
    for s in pick:
        f, t = pairs[kind][s]
        text = " ".join(str(t.get("text") or "").split())
        row = {"sub": s, "first": f["code_id"], "reply": t["code_id"], "interval_min": round((t["hour"] - f["hour"]) * 60),
               "reply_words": len(text.split()), "first_text": " ".join(str(f.get("text") or "").split()),
               "reply_text": text}
        sample[kind].append(row)
with open(DEST, "w", encoding="utf-8") as out:
    json.dump(sample, out, ensure_ascii=False, indent=1)
for kind in ("acceptance", "refusal"):
    print("\n== %s: %d sampled" % (kind, len(sample[kind])))
    for i, r in enumerate(sample[kind], 1):
        print("%s %d. %s %s -> %s, %d min, %d words | FIRST: %s || REPLY: %s" % (
            kind[0].upper(), i, r["sub"], r["first"], r["reply"], r["interval_min"], r["reply_words"], r["first_text"],
            r["reply_text"]))
