#!/usr/bin/env python3
"""D2a §2: the verdicts. Reads out/verdicts-D.jsonl, out/_fleet_raw/D2v/ (arm.json, DONE, log.jsonl), the packets'
digests (out/verdict-D/<sub>.md) and the store's concept counts and off-platform pointers (rooms.jsonl; the same
figures each packet stated). Writes nothing unless --list is given, which writes out/_analysis/d2_verdict_rooms.json
(the split rooms and the cannot-tell lines the numbers do not support, for notes-D2.md and D3).

    python3 out/_analysis/d2_verdicts.py [--list]

The thresholds are prior.md §8's, read from it: the concept floor (FLOOR) and the off-platform threshold (PTR_ABS
pointers, or at least PTR_MIN pointers and one or more for every PTR_PER concepts). A cannot-tell under coded-share is
supported by the numbers when the room is below the floor; under off-platform when the room is past the threshold;
under both when both hold. The other values the criterion allows name no number and are reported apart. These are
review prompts (FLEET §3), so an unsupported line is listed for D3, not ruled on.
"""
import collections, hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
RAW = os.path.join(OUT, "_fleet_raw", "D2v")

s8 = re.search(r"##\s*8\..*?(?=\n##\s|\Z)", open(os.path.join(OUT, "prior.md"), encoding="utf-8").read(), re.S).group(0)
FLOOR = int(re.search(r"concept floor: (\d+)", s8).group(1))
m = re.search(r"threshold: (\d+) off-platform pointers, or at least (\d+) pointers and one or more for every (\w+) "
              r"concepts", s8)
WORDS = {"two": 2, "three": 3, "four": 4, "five": 5}
PTR_ABS, PTR_MIN = int(m.group(1)), int(m.group(2))
PTR_PER = WORDS.get(m.group(3)) or int(m.group(3))

rooms = {json.loads(l)["sub"]: json.loads(l) for l in open(os.path.join(ROOT, "package", "store", "rooms.jsonl"),
                                                             encoding="utf-8") if l.strip()}
V = [json.loads(l) for l in open(os.path.join(OUT, "verdicts-D.jsonl"), encoding="utf-8") if l.strip()]


def below(s):
    return (rooms[s].get("codes") or 0) < FLOOR


def past(s):
    c, p = rooms[s].get("codes") or 0, rooms[s].get("n_off_platform") or 0
    return p >= PTR_ABS or (p >= PTR_MIN and p * PTR_PER >= c)


print("prior.md §8 read: floor %d; off-platform %d, or at least %d and one per %d concepts" % (FLOOR, PTR_ABS, PTR_MIN, PTR_PER))
print("rooms below the floor %d; past the off-platform threshold %d; both %d" % (
    sum(below(s) for s in rooms), sum(past(s) for s in rooms), sum(below(s) and past(s) for s in rooms)))
readers = [dict(r, sub=v["sub"], sub_written=r.get("sub")) for v in V for r in v["readers"]]
for v in V:
    v["readers"] = [dict(r, sub=v["sub"]) for r in v["readers"]]
print("verdict lines %d (rooms); reader lines %d; readers per room %s; reader ids r1 %d, r2 %d, others %d (reissues)" % (
    len(V), len(readers), dict(collections.Counter(len(v["readers"]) for v in V)),
    sum(1 for r in readers if r["reader"] == "r1"), sum(1 for r in readers if r["reader"] == "r2"),
    sum(1 for r in readers if r["reader"] not in ("r1", "r2"))))
print("reader lines whose written sub differs from the room's: %d (%s)" % (
    sum(1 for r in readers if r["sub_written"] != r["sub"]),
    dict(collections.Counter("r/ prefix" if str(r["sub_written"]).startswith("r/") else "other"
                             for r in readers if r["sub_written"] != r["sub"]))))
dig = {s: re.search(r"Your `served` value: ([0-9a-f]{64})", open(os.path.join(OUT, "verdict-D", s + ".md"),
                                                                     encoding="utf-8").read()).group(1) for s in rooms}
print("reader lines whose served value equals the value the packet states: %d of %d; not equal: %s" % (
    sum(1 for r in readers if (r.get("served") or "").replace("sha256:", "") == dig[r["sub"]]), len(readers),
    [(r["sub"], r["reader"], len(str(r.get("served")))) for r in readers
     if (r.get("served") or "").replace("sha256:", "") != dig[r["sub"]]]))
print("rooms whose reader wrote another room's name in sub: %s" % sorted(
    (r["sub"], r["sub_written"]) for r in readers
    if r["sub_written"] != r["sub"] and str(r["sub_written"]).lower().replace("r/", "") != r["sub"].lower()))
print("reader lines with fields beyond the return line: %d (%s)" % (
    sum(1 for r in readers if "agent" in r), sorted({r["sub"] for r in readers if "agent" in r})))

rv = collections.Counter(r["verdict"] for r in readers)
print("reader verdicts: " + ", ".join("%s %d (%.1f%%)" % (k, n, 100.0 * n / len(readers)) for k, n in rv.most_common()))
room_v, pairs, split = {}, collections.Counter(), []
for v in V:
    vs = sorted(r["verdict"] for r in v["readers"])
    pairs[tuple(vs)] += 1
    room_v[v["sub"]] = vs[0] if len(set(vs)) == 1 else "split"
    if len(set(vs)) > 1:
        split.append(v["sub"])
print("rooms agreed %d, split %d; disagreement rate %.1f%%" % (len(V) - len(split), len(split), 100.0 * len(split) / len(V)))
print("room verdicts: %s" % dict(collections.Counter(room_v.values()).most_common()))
print("verdict pairs (rooms):")
for p, n in sorted(pairs.items(), key=lambda x: -x[1]):
    print("  %-50s %d%s" % (" / ".join(p), n, "" if p[0] == p[1] else "  (split, %.1f%% of rooms)" % (100.0 * n / len(V))))
for val in sorted(rv):
    touched = sum(1 for v in V if any(r["verdict"] == val for r in v["readers"]))
    both = sum(1 for v in V if all(r["verdict"] == val for r in v["readers"]))
    print("  %s: rooms with at least one reader %d, both readers %d (agreement within the value %.0f%%)" % (
        val, touched, both, 100.0 * both / max(1, touched)))

ct = [r for r in readers if r["verdict"] == "cannot-tell"]
print("cannot-tell reader lines %d; by threshold %s" % (len(ct), dict(collections.Counter(r["cannot_tell_under"] for r in ct))))
unsup, sup = [], collections.Counter()
for r in ct:
    s, u = r["sub"], r["cannot_tell_under"]
    ok = {"coded-share": below(s), "off-platform": past(s), "both": below(s) and past(s)}.get(u)
    if ok is None:
        sup["%s: no number" % u] += 1
    elif ok:
        sup["%s: supported" % u] += 1
    else:
        sup["%s: not supported" % u] += 1
        unsup.append({"sub": s, "reader": r["reader"], "under": u, "codes": rooms[s].get("codes"),
                      "off_platform": rooms[s].get("n_off_platform"), "other_reader": [
                          x["verdict"] for v in V if v["sub"] == s for x in v["readers"] if x["reader"] != r["reader"]]})
print("cannot-tell against the numbers: %s" % dict(sup))
print("unsupported cannot-tell lines %d in %d rooms" % (len(unsup), len({u["sub"] for u in unsup})))
nonct_thr = sum(1 for r in readers if r["verdict"] != "cannot-tell" and r["cannot_tell_under"] not in (None, "null"))
res_bad = sum(1 for r in readers if r["verdict"] != "composes-with-residue" and r["residue"] not in (None, [], "null"))
print("threshold named on a verdict other than cannot-tell: %d; residue on a verdict other than with-residue: %d" % (
    nonct_thr, res_bad))
print("rooms below the floor, by room verdict: %s" % dict(collections.Counter(room_v[s] for s in rooms if below(s))))
print("rooms past the off-platform threshold, by room verdict: %s" % dict(collections.Counter(room_v[s] for s in rooms if past(s))))
print("readers naming residue: themes per with-residue line median %s" % (
    sorted(len(r["residue"] or []) for r in readers if r["verdict"] == "composes-with-residue")[
        len([1 for r in readers if r["verdict"] == "composes-with-residue"]) // 2]
    if any(r["verdict"] == "composes-with-residue" for r in readers) else "-"))

grades = collections.Counter(v.get("grade") for v in V)
print("labeler grade beside the verdict: %s" % dict(grades))
print("cross-table, labeler grade (rows) by room verdict (columns):")
cols = ["composes", "composes-with-residue", "does-not-compose", "cannot-tell", "split"]
print("  %-24s" % "" + "".join("%24s" % c for c in cols))
for g in sorted(grades, key=str):
    print("  %-24s" % g + "".join("%24d" % sum(1 for v in V if v.get("grade") == g and room_v[v["sub"]] == c) for c in cols))
print("cross-table, labeler grade by reader verdict: %s" % {
    g: dict(collections.Counter(r["verdict"] for v in V if v.get("grade") == g for r in v["readers"])) for g in grades})

arm = json.load(open(os.path.join(RAW, "arm.json")))
done = json.loads(open(os.path.join(RAW, "DONE"), encoding="utf-8").read())
log = [json.loads(l) for l in open(os.path.join(RAW, "log.jsonl"), encoding="utf-8") if l.strip()]
print("fleet: served %s (verified %s), effort %s, readers %s, reissue limit %s; DONE valid %s, exhausted %s, cost $%.2f" % (
    arm.get("served"), arm.get("served_verified"), arm.get("reasoning_effort"), arm.get("readers"), arm.get("reissue"),
    done.get("valid_returns"), done.get("exhausted"), done.get("cost_usd") or 0))
print("log: %d attempts; valid %s; reissue attempts (reissue > 0) %d; served_matches_probe %s; invalid why (first 3 kinds) %s" % (
    len(log), dict(collections.Counter(l.get("valid") for l in log)), sum(1 for l in log if (l.get("reissue") or 0) > 0),
    dict(collections.Counter(l.get("served_matches_probe") for l in log)),
    collections.Counter(str(l.get("why"))[:60] for l in log if not l.get("valid")).most_common(3)))
story = [json.loads(l) for l in open(os.path.join(OUT, "story_rooms-p5.jsonl"), encoding="utf-8")][1:]
miss = [s["sub"] for s in story if s["verdict"] != "told"]
print("story-miss rooms (%d) by room verdict: %s" % (len(miss), {s: room_v[s] for s in miss}))
if "--list" in sys.argv:
    dest = os.path.join(OUT, "_analysis", "d2_verdict_rooms.json")
    if os.path.exists(dest):
        sys.exit("d2_verdict_rooms.json exists; not overwritten")
    json.dump({"split": [{"sub": s, "pair": sorted(r["verdict"] for r in v["readers"])} for v in V for s in [v["sub"]]
                         if s in split], "unsupported_cannot_tell": unsup}, open(dest, "w"), indent=1)
    print("wrote %s" % dest)
