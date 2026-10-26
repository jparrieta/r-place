#!/usr/bin/env python3
"""D5b, rule 7: the canvas projected onto the re-reading of work_remained, afterwards. For the 476 rooms in a
branch, per reading (stood, gone, during, other, unclear, silent) and per field value (kept, lost, silent):
rooms, rooms with an artwork, median canvas_area_px, and the members' share of their placements in hours 64
to 73. Prints JSON. Nothing here changes a reading.

    python3 out/_analysis/d5b_canvas_by_reading.py
"""
import collections, csv, json, os, statistics

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
PKG = os.path.join(ROOT, "package")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


rooms = {r["sub"]: r for r in jl(os.path.join(PKG, "store", "rooms.jsonl"))}
oe = {d["sub"]: d for d in jl(os.path.join(OUT, "organizing_end-A1.jsonl"))}
reading = {}
for i in range(1, 6):
    reading.update(json.load(open(os.path.join(AN, "d5b_wr_read%d.json" % i), encoding="utf-8")))
OVR = {"detroitlions": "unclear", "placetardis": "unclear", "liverpoolfc": "unclear"}
late, tot = collections.Counter(), collections.Counter()
for r in csv.DictReader(open(os.path.join(PKG, "pixels.csv"), encoding="utf-8")):
    v = int(float(r["px_by_window_members"] or 0))
    tot[r["sub"]] += v
    if 64 <= float(r["hour_since_open"]) < 73:
        late[r["sub"]] += v


def summary(subs):
    areas = [rooms[s].get("canvas_area_px") for s in subs if isinstance(rooms.get(s, {}).get("canvas_area_px"), (int, float))]
    art = sum(1 for s in subs if (rooms.get(s, {}).get("canvas_entries") or 0) > 0)
    lt, tt = sum(late[s] for s in subs), sum(tot[s] for s in subs)
    return {"rooms": len(subs), "with_artwork": art, "median_area_px": statistics.median(areas) if areas else None,
            "late_share": round(lt / tt, 3) if tt else None}


by_read, by_field = collections.defaultdict(list), collections.defaultdict(list)
for s, v in reading.items():
    by_read[OVR.get(s, v[0])].append(s)
    by_field[oe[s]["work_remained"]].append(s)
print(json.dumps({"by_reading": {k: summary(v) for k, v in sorted(by_read.items())},
                  "by_field": {k: summary(v) for k, v in sorted(by_field.items())}}, ensure_ascii=False))
