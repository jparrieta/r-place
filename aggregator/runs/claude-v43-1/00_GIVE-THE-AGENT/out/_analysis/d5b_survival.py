#!/usr/bin/env python3
"""D5b, section 4: survival per branch from the record, then the canvas projected afterwards.

Reads branches.jsonl, organizing_end-A1.jsonl, the D5b re-readings of work_remained
(d5b_wr_read1.json to d5b_wr_read5.json, with the overrides below), branches-D5.jsonl's canvas
fields, and package/pixels.csv. Prints JSON: per branch, then the 476 rooms in a branch, then
the population.

    python3 out/_analysis/d5b_survival.py
"""
import collections, csv, json, os, statistics

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
PKG = os.path.join(ROOT, "package")

# Corrections made after the reading files were written; each is logged in the diary.
OVERRIDES = {
    "detroitlions": ["unclear", "mixed: the Stafford face said not to survive; the field says kept"],
    "placetardis": ["unclear", "a member's hour; read as the like lines edboxes and seahawks"],
    "liverpoolfc": ["unclear", "a post that place ended; read as the like line malaysia"],
}
# Brackets on hour_since_open (prior.md section 4; hour 8 to 32 is the April Fools marker).
BRACKETS = [("before_open", -99, 0), ("h0_8", 0, 8), ("h8_32_april_fools", 8, 32),
            ("h32_64", 32, 64), ("h64_73", 64, 73)]


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


B = jl(os.path.join(OUT, "branches.jsonl"))
D5 = {d["branch"]: d for d in jl(os.path.join(OUT, "branches-D5.jsonl"))}
oe = {d["sub"]: d for d in jl(os.path.join(OUT, "organizing_end-A1.jsonl"))}
reading = {}
for i in range(1, 6):
    part = json.load(open(os.path.join(AN, "d5b_wr_read%d.json" % i), encoding="utf-8"))
    dup = set(part) & set(reading)
    if dup:
        raise SystemExit("duplicate readings: %s" % sorted(dup))
    reading.update(part)
reading.update(OVERRIDES)
inbranch = {s for b in B for s in b["members"]}
missing = sorted(inbranch - set(reading))
extra = sorted(set(reading) - inbranch)

px = collections.defaultdict(lambda: collections.Counter())
for r in csv.DictReader(open(os.path.join(PKG, "pixels.csv"), encoding="utf-8")):
    h = float(r["hour_since_open"])
    for name, lo, hi in BRACKETS:
        if lo <= h < hi:
            px[r["sub"]]["win_" + name] += int(float(r["px_by_window_members"] or 0))
            px[r["sub"]]["any_" + name] += int(float(r["px_in_region_any"] or 0))
    px[r["sub"]]["win_by_hour_%d" % int(h)] += int(float(r["px_by_window_members"] or 0))

KINDS = ["stood", "gone", "during", "other", "unclear", "silent"]


def block(members):
    m = sorted(members, key=str.lower)
    ends = [oe[s]["organizing_end_hour"] for s in m if isinstance(oe[s].get("organizing_end_hour"), (int, float))]
    aft = [oe[s]["aftermath_share"] for s in m if isinstance(oe[s].get("aftermath_share"), (int, float))]
    field = collections.Counter(oe[s]["work_remained"] for s in m)
    read = collections.Counter(reading[s][0] for s in m if s in reading)
    cross = {f: dict(collections.Counter(reading[s][0] for s in m if oe[s]["work_remained"] == f and s in reading))
             for f in ("kept", "lost", "silent")}
    agree = sum(1 for s in m if s in reading and (oe[s]["work_remained"], reading[s][0]) in
                {("kept", "stood"), ("lost", "gone"), ("silent", "silent")})
    win = collections.Counter()
    anyp = collections.Counter()
    hours = collections.Counter()
    for s in m:
        for k, v in px[s].items():
            if k.startswith("win_by_hour_"):
                hours[int(k[len("win_by_hour_"):])] += v
            elif k.startswith("win_"):
                win[k[4:]] += v
            elif k.startswith("any_"):
                anyp[k[4:]] += v
    wt, at = sum(win.values()), sum(anyp.values())
    peak = max(hours.items(), key=lambda kv: kv[1])[0] if hours else None
    return {
        "n": len(m),
        "median_end": round(statistics.median(ends), 2) if ends else None,
        "end_before_64": sum(1 for e in ends if e < 64), "end_64_73": sum(1 for e in ends if 64 <= e < 73),
        "end_73_on": sum(1 for e in ends if e >= 73),
        "aftermath_mean": round(statistics.mean(aft), 4) if aft else None,
        "aftermath_median": round(statistics.median(aft), 4) if aft else None,
        "rooms_with_aftermath_coord": sum(1 for s in m if oe[s].get("aftermath_coordinating_codes")),
        "field": {k: field.get(k, 0) for k in ("kept", "lost", "silent")},
        "reading": {k: read.get(k, 0) for k in KINDS},
        "field_by_reading": cross, "agree": agree,
        "win_share": {k: round(win[k] / wt, 3) if wt else None for k, _, _ in BRACKETS},
        "any_share": {k: round(anyp[k] / at, 3) if at else None for k, _, _ in BRACKETS},
        "win_total": wt, "any_total": at, "own_share": round(wt / at, 3) if at else None,
        "win_peak_hour": peak,
    }


res = {"missing_readings": missing, "extra_readings": extra, "readings": len(reading), "branches": []}
for b in B:
    row = {"branch": b["id"], "name": D5[b["id"]]["name"]}
    row.update(block(b["members"]))
    row["ledger_D5"] = D5[b["id"]]["survival"]
    row["canvas_D5"] = {k: D5[b["id"]]["canvas"].get(k) for k in ("median_area_px", "rooms_with_artwork")}
    res["branches"].append(row)
res["in_a_branch"] = block(inbranch)
res["population"] = block(set(oe))
print(json.dumps(res, ensure_ascii=False))
