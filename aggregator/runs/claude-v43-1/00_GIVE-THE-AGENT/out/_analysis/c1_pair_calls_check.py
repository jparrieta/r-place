"""Check the pair-test call files against the declared order (read-only).

Loads every c1_pair_calls-*.json, checks that the numbers run 1..N with no gap or repeat,
that each pair and item count matches c1_pair_test.json in the order c1_pair_pack.py reads,
that every call is joint, lump or unresolved with evidence, contrary and action, and counts
the calls by kind.
"""
import collections
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

d = json.load(open(os.path.join(HERE, "c1_pair_test.json"), encoding="utf-8"))
declared = [p for p in d["pairs"] if p["material"]]
declared.sort(key=lambda p: (-p["n"], p["pair"]))

calls = []
files = sorted(glob.glob(os.path.join(HERE, "c1_pair_calls-*.json")))
for path in files:
    calls.extend(json.load(open(path, encoding="utf-8"))["calls"])
calls.sort(key=lambda c: c["n"])

problems = []
nums = [c["n"] for c in calls]
if nums != list(range(1, len(calls) + 1)):
    problems.append("numbers do not run 1..%d" % len(calls))
if len(calls) != len(declared):
    problems.append("%d calls against %d declared material pairs" % (len(calls), len(declared)))
for c, p in zip(calls, declared):
    if list(c["pair"]) != list(p["pair"]):
        problems.append("n=%d pair %s, declared %s" % (c["n"], c["pair"], p["pair"]))
    if c["items"] != p["n"]:
        problems.append("n=%d items %s, declared %s" % (c["n"], c["items"], p["n"]))
    want = p["n"] if p["n"] <= 12 else 12
    if c["read"] != want:
        problems.append("n=%d read %s, rule gives %s" % (c["n"], c["read"], want))
    if c["call"] not in ("joint", "lump", "unresolved"):
        problems.append("n=%d call %s" % (c["n"], c["call"]))
    if not (c.get("evidence") and c.get("contrary") and c.get("action")):
        problems.append("n=%d lacks evidence, contrary or action" % c["n"])

print("files: %d; calls: %d; declared material pairs: %d" % (len(files), len(calls), len(declared)))
print("by kind: " + json.dumps(dict(collections.Counter(c["call"] for c in calls))))
print("not joint: " + json.dumps([[c["n"], c["pair"], c["call"]] for c in calls if c["call"] != "joint"]))
print("actions other than plain retain: %d" % sum(1 for c in calls if c["action"] != "retain."))
print("problems: %d" % len(problems))
print("\n".join(problems))

print("item readings: %d (pairs read whole: %d; pairs sampled at 12: %d)" % (
    sum(c["read"] for c in calls),
    sum(1 for c in calls if c["read"] == c["items"]),
    sum(1 for c in calls if c["read"] < c["items"])))
print("\n## actions other than plain retain")
print("\n".join("%d %s | %s: %s" % (c["n"], c["pair"][0], c["pair"][1], c["action"])
                for c in calls if c["action"] != "retain."))
FLAGS = ("must_not_show sends", "discriminator sends", "reads as", "does not name",
         "must_show takes", "must_show names", "go to the arguables", "goes to the arguables")
print("\n## contrary readings naming a written field or carried item")
print("\n".join("%d %s | %s: %s" % (c["n"], c["pair"][0], c["pair"][1], c["contrary"])
                for c in calls if any(f in c["contrary"] or f in c["action"] for f in FLAGS)))
