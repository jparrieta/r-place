#!/usr/bin/env python3
"""D5b: the tables of survival-D5.md, from d5b_survival.json, d5b_timing.json, d5b_endings_themes.json and
branches-D5.jsonl, so that no figure is typed by hand. --table record|reread|canvas|timing|aid.
--fill TEMPLATE prints the template with each line '{{TABLE:name}}' replaced by that table.

    python3 out/_analysis/d5b_surv_tables.py --table record
    python3 out/_analysis/d5b_surv_tables.py --fill out/_analysis/d5b_surv_template.md > out/survival-D5.md
"""
import argparse, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
ap = argparse.ArgumentParser()
ap.add_argument("--table")
ap.add_argument("--fill")
a = ap.parse_args()

S = json.load(open(os.path.join(AN, "d5b_survival.json"), encoding="utf-8"))
T = json.load(open(os.path.join(AN, "d5b_timing.json"), encoding="utf-8"))
E = json.load(open(os.path.join(AN, "d5b_endings_themes.json"), encoding="utf-8"))
D5 = {json.loads(l)["branch"]: json.loads(l) for l in open(os.path.join(OUT, "branches-D5.jsonl"), encoding="utf-8") if l.strip()}
oe = {json.loads(l)["sub"]: json.loads(l) for l in open(os.path.join(OUT, "organizing_end-A1.jsonl"), encoding="utf-8") if l.strip()}
B = [json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8") if l.strip()]
EMPTY = {"ockytop"}  # amendment logged at D5b: no member placement on either side corroborates nothing


def f(x, d=2):
    return "" if x is None else ("%.*f" % (d, x))


def rows_all():
    return [(b["branch"], b) for b in S["branches"]] + [("in a branch", S["in_a_branch"]), ("population", S["population"])]


def record():
    out = ["| branch | n | median organizing_end_hour | ended before 64 | 64 to 73 | 73 or later | aftermath share (mean) | rooms coordinating after 73 | kept | lost | silent |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for name, b in rows_all():
        out.append("| %s | %d | %s | %d | %d | %d | %s | %d | %d | %d | %d |" % (
            name, b["n"], f(b["median_end"]), b["end_before_64"], b["end_64_73"], b["end_73_on"], f(b["aftermath_mean"], 4),
            b["rooms_with_aftermath_coord"], b["field"]["kept"], b["field"]["lost"], b["field"]["silent"]))
    return "\n".join(out)


def reread():
    out = ["| branch | n | kept | lost | silent | stood | gone | during | other | unclear | silent (re-read) | field agrees |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for name, b in rows_all()[:-1]:
        r, fl = b["reading"], b["field"]
        out.append("| %s | %d | %d | %d | %d | %d | %d | %d | %d | %d | %d | %d |" % (
            name, b["n"], fl["kept"], fl["lost"], fl["silent"], r["stood"], r["gone"], r["during"], r["other"], r["unclear"],
            r["silent"], b["agree"]))
    return "\n".join(out)


def crosstab():
    c = S["in_a_branch"]["field_by_reading"]
    kinds = ["stood", "gone", "during", "other", "unclear", "silent"]
    out = ["| the field says | " + " | ".join(kinds) + " | all |", "|---|" + "---|" * (len(kinds) + 1)]
    for fld in ("kept", "lost", "silent"):
        row = c.get(fld, {})
        out.append("| %s | %s | %d |" % (fld, " | ".join(str(row.get(k, 0)) for k in kinds), sum(row.values())))
    return "\n".join(out)


def pct(bid):
    m = re.search(r"at the ([0-9.]+)(?:st|nd|rd|th) percentile", D5[bid]["canvas"]["read"])
    return m.group(1) if m else ""


def canvas():
    out = ["| branch | rooms with artwork | median area (px) | percentile against random groups of its size | members' share of placements in their regions | share of members' placements in hours 8 to 32 | in hours 64 to 73 | peak hour |",
           "|---|---|---|---|---|---|---|---|"]
    for name, b in rows_all():
        if name in D5:
            cv = D5[name]["canvas"]
            area, art, p = cv.get("median_area_px"), cv.get("rooms_with_artwork"), pct(name)
            area = ("%g" % area) if area is not None else ""
        else:
            area, art, p = "", "", ""
        ws = b["win_share"]
        out.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
            name, art, area, p, f(b["own_share"], 3), f(ws["h8_32_april_fools"], 3), f(ws["h64_73"], 3), b["win_peak_hour"]))
    return "\n".join(out)


def bracket(h):
    if h >= 73:
        return "aftermath (73 to 97)"
    return "placement (0 to 73)" + (", April Fools hours 8 to 32" if 8 <= h < 32 else "")


def timing():
    out = ["| branches | room | hour | bracket | the act, as the narrative dates it | implied | members' placements, 4 hours before and from it | result |",
           "|---|---|---|---|---|---|---|---|"]
    for r in T:
        res = r["result"]
        if r["sub"] in EMPTY and res == "corroborated":
            res = "empty (amended: no member placement either side)"
        pl = "" if r.get("members_before") is None else "%d, %d" % (r["members_before"], r["members_after"])
        out.append("| %s | r/%s | %s | %s | %s | %s | %s | %s |" % (
            r["branches"], r["sub"], f(r["hour"]), bracket(r["hour"]), r["act"], r["implied"], pl, res))
    return "\n".join(out)


def aid():
    th = {x["branch"]: x for x in E["branches"]}
    for b in B:
        bid = b["id"]
        L, A = th[bid]["last_coordinating_code"], th[bid]["aftermath_coordinating_codes"]
        after = sorted([s for s in b["members"] if oe[s].get("aftermath_coordinating_codes")], key=str.lower)
        print(bid, D5[bid]["name"])
        print("  last:", [(t["name"], t["count"], t["share"], t["pop_share"]) for t in L["top"][:3]])
        print("  after:", [(t["name"], t["count"], t["share"], t["pop_share"]) for t in A["top"][:3]], "rooms", len(after), after)


T_ = {"record": record, "reread": reread, "crosstab": crosstab, "canvas": canvas, "timing": timing}
if a.table == "aid":
    aid()
elif a.table:
    print(T_[a.table]())
if a.fill:
    for line in open(a.fill, encoding="utf-8").read().split("\n"):
        m = re.fullmatch(r"\{\{TABLE:([a-z]+)\}\}", line.strip())
        print(T_[m.group(1)]() if m else line)
