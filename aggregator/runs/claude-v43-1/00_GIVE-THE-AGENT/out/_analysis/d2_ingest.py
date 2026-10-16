#!/usr/bin/env python3
"""D2a §1: what ingest did, by count. Reads out/adaptations.jsonl by count only (never prints a line), the
ingest report, RUN.json's D2 counts, DROPS/D/DONE and UNRETURNED.tsv, the rooms' run.json copies
(out/rooms/<sub>/run.json) and out/adaptation-returns.jsonl. Writes nothing.

    python3 out/_analysis/d2_ingest.py

Prints: rooms and lines; lines per room (min, p10, quartiles, p90, max); ops and kinds with shares; rooms holding
each op; non-portable lines (share, rooms, the fields of the hits by kind of hit); none rooms; lines with a source
and the share whose source theme is placed nowhere (lift[1] null), by op; lines with no element, by op; the
labelers' run records (model, resumed_with, attempts); the labelers' grades and local status; the counts against
RUN.json and DONE.
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def q(xs):
    xs = sorted(xs)
    n = len(xs)
    return xs[0], xs[int(0.1 * (n - 1))], xs[n // 4], xs[n // 2], xs[(3 * n) // 4], xs[int(0.9 * (n - 1))], xs[-1]


L = jl(os.path.join(OUT, "adaptations.jsonl"))
rooms = collections.Counter(l["sub"] for l in L)
print("rooms %d; lines %d" % (len(rooms), len(L)))
print("lines per room: min %d, p10 %d, q1 %d, median %d, q3 %d, p90 %d, max %d" % q(rooms.values()))
ops = collections.Counter(l["op"] for l in L)
kinds = collections.Counter(l["kind"] for l in L)
print("ops: " + ", ".join("%s %d (%.1f%%)" % (k, v, 100.0 * v / len(L)) for k, v in ops.most_common()))
print("kinds: " + ", ".join("%s %d (%.1f%%)" % (k, v, 100.0 * v / len(L)) for k, v in kinds.most_common()))
rooms_op = collections.defaultdict(set)
for l in L:
    rooms_op[l["op"]].add(l["sub"])
print("rooms holding each op: " + ", ".join("%s %d" % (k, len(rooms_op[k])) for k, _ in ops.most_common()))
np_ = [l for l in L if not l["portable"]]
print("non-portable: %d lines (%.2f%%) in %d rooms; by op: %s" % (
    len(np_), 100.0 * len(np_) / len(L), len({l["sub"] for l in np_}),
    dict(collections.Counter(l["op"] for l in np_).most_common())))
own = sum(1 for l in np_ if l["sub"] in l["nonportable_hits"])
print("non-portable lines whose hits include the room's own name: %d; hits per line: median %d, max %d" % (
    own, sorted(len(l["nonportable_hits"]) for l in np_)[len(np_) // 2] if np_ else 0,
    max((len(l["nonportable_hits"]) for l in np_), default=0)))
none_rooms = {s for s in rooms if all(l["op"] == "none" for l in L if l["sub"] == s)} if "none" in ops else set()
print("none rooms: %d (%.1f%%)" % (len(none_rooms), 100.0 * len(none_rooms) / len(rooms)))
src = [l for l in L if l["source"]]
unpl = [l for l in src if not (l["lift"] and l["lift"][1])]
print("lines with a source: %d; source placed nowhere (lift[1] null): %d (%.1f%% of sourced lines, %.1f%% of all)" % (
    len(src), len(unpl), 100.0 * len(unpl) / max(1, len(src)), 100.0 * len(unpl) / len(L)))
by = collections.Counter(l["op"] for l in src)
bu = collections.Counter(l["op"] for l in unpl)
print("  by op (unplaced / sourced): " + ", ".join("%s %d/%d" % (k, bu[k], by[k]) for k, _ in by.most_common()))
print("  rooms with any unplaced-source line: %d" % len({l["sub"] for l in unpl}))
srcs = collections.Counter(("code" if (l["source"] or "").startswith("c") else "theme") for l in src)
print("  sources by form: %s" % dict(srcs))
noel = collections.Counter(l["op"] for l in L if not l["element"])
print("lines with no element, by op: %s" % dict(noel))
print("contradict lines by element: %s" % dict(collections.Counter(l["element"] for l in L if l["op"] == "contradict")))
print("propose lines: %d in %d rooms; with an element named: %d" % (
    ops["propose"], len(rooms_op["propose"]), sum(1 for l in L if l["op"] == "propose" and l["element"])))
dec = collections.Counter(l["decision"] for l in L)
orig = collections.Counter(l["origin"] for l in L)
print("decision: %s; origin: %s; model_version values: %d" % (dict(dec), dict(orig), len({l["model_version"] for l in L})))

runs = {}
for s in rooms:
    p = os.path.join(OUT, "rooms", s, "run.json")
    if os.path.exists(p):
        runs[s] = json.load(open(p))
print("run.json copies: %d; model %s; resumed_with %s; attempts %s; keys %s" % (
    len(runs), dict(collections.Counter(r.get("model") for r in runs.values())),
    dict(collections.Counter(r.get("resumed_with") for r in runs.values())),
    dict(collections.Counter(r.get("attempts") for r in runs.values())),
    dict(collections.Counter(k for r in runs.values() for k in r))))
ar = jl(os.path.join(OUT, "adaptation-returns.jsonl"))
print("adaptation-returns: %d records; phase %s; local_grade %s; local_status %s" % (
    len(ar), dict(collections.Counter(r.get("phase") for r in ar)), dict(collections.Counter(r.get("local_grade") for r in ar)),
    dict(collections.Counter(str(r.get("local_status")) for r in ar))))
run = json.load(open(os.path.join(ROOT, "RUN.json"))).get("D2")
done = open(os.path.join(ROOT, "DROPS", "D", "DONE"), encoding="utf-8").read().split()
unret = [l for l in open(os.path.join(ROOT, "DROPS", "D", "UNRETURNED.tsv"), encoding="utf-8")
         if l.strip() and not l.startswith("sub\t")]
print("RUN.json D2 %s; DONE %s; UNRETURNED rows %d; ledger rooms %d" % (run, done, len(unret), len(rooms)))
