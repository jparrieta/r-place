#!/usr/bin/env python3
"""C5d: how rooms whose record says their work was kept organized, against rooms whose record says it was lost or falls
silent (stage C5 sections 12 and 13), in the model's terms. For each element, the rooms carrying it (any concept cited
under its third-order themes, c2_elements_c5c2.json and assignments_final.jsonl) and their work_remained shares from
organizing_end-A1.jsonl; the same within the middle two room-size quartiles (items_in_window), since a room that writes
more carries more elements (contract section 5). A comparison of the record, never the canvas, and never a prediction.
Writes out/_analysis/c5d_kept.json.

    python3 out/_analysis/c5d_kept.py
"""
import collections, json, os, statistics

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
rooms = {json.loads(l)["sub"]: json.loads(l) for l in open(os.path.join(ROOT, "package", "store", "rooms.jsonl"))}
end = {json.loads(l)["sub"]: json.loads(l) for l in open(os.path.join(OUT, "organizing_end-A1.jsonl"))}
sizes = sorted(r.get("items_in_window") or 0 for r in rooms.values())
q1, q3 = sizes[len(sizes) // 4], sizes[3 * len(sizes) // 4]
mid = {s for s, r in rooms.items() if q1 <= (r.get("items_in_window") or 0) < q3}
carry = collections.defaultdict(set)
for l in open(os.path.join(OUT, "assignments_final.jsonl")):
    r = json.loads(l)
    for t3, codes in (r.get("support_by_theme") or {}).items():
        if codes:
            carry[t3].add(r["sub"])
els = json.load(open(os.path.join(OUT, "_analysis", "c2_elements_c5c2.json")))["elements"]
fourth = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "fourth", "fourth.jsonl"))}


def shares(subs):
    c = collections.Counter(end[s]["work_remained"] for s in subs if s in end)
    n = sum(c.values())
    return n, {k: round(c[k] / n, 3) if n else None for k in ("kept", "lost", "silent")}


out = {}
base_all, base_mid = shares(set(end)), shares(mid)
print("all rooms: n %d %s; middle half by size: n %d %s" % (base_all[0], base_all[1], base_mid[0], base_mid[1]))
want = ["P05", "P08", "P07", "P09", "P10", "P14", "P16", "P17", "P18", "P20", "K01", "K02"]
for e in els:
    if e["id"] not in want:
        continue
    subs = set()
    for t in e.get("themes") or []:
        subs |= carry.get(t, set())
    a, m = shares(subs), shares(subs & mid)
    out[e["id"]] = {"all": a, "mid": m}
    print("%s rooms %3d: kept %.3f lost %.3f silent %.3f | middle half n %3d: kept %s lost %s silent %s" % (
        e["id"], a[0], a[1]["kept"], a[1]["lost"], a[1]["silent"], m[0], m[1]["kept"], m[1]["lost"], m[1]["silent"]))
dec = set()
for t in fourth["T4-011"]["members"]:
    dec |= carry.get(t, set())
a, m = shares(dec), shares(dec & mid)
out["C01 (T4-011)"] = {"all": a, "mid": m}
print("C01 decided order rooms %d: %s | middle half n %d: %s" % (a[0], a[1], m[0], m[1]))
eh = [end[s]["organizing_end_hour"] for s in end if end[s].get("organizing_end_hour") is not None]
af = [end[s]["aftermath_share"] for s in end if end[s].get("aftermath_share") is not None]
print("organizing_end_hour median %.2f (n %d); aftermath_share median %.3f, mean %.3f" % (
    statistics.median(eh), len(eh), statistics.median(af), statistics.mean(af)))
out["_base"] = {"all": base_all, "mid": base_mid, "end_hour_median": statistics.median(eh),
                "aftermath_median": statistics.median(af), "aftermath_mean": statistics.mean(af), "mid_bounds": [q1, q3]}
json.dump(out, open(os.path.join(OUT, "_analysis", "c5d_kept.json"), "w"), indent=1)
