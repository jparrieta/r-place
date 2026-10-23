#!/usr/bin/env python3
"""D3b: in one packet of unruled re-check lines of one element and op (rebuilt as d3b_packet.py does), list the lines
whose cited concepts all fall after hour 73, when placement ended on the event's canvas, and those with some after it,
with each code's hour, so that upkeep or acts on a later canvas are not read as acts on the event's canvas (G11's
readings). Reads only.

    python3 out/_analysis/d3b_postclose.py --element P05 --op instantiate
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ST = os.path.join(ROOT, "package", "store")
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--op", required=True)
ap.add_argument("--ids", help="optional file of ids, one a line, to check instead of the current packet")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def codes(r):
    ev = r.get("evidence") or []
    if isinstance(ev, dict):
        ev = ev.get("codes") or []
    return [str(c).split(":")[-1] for c in ev]


ruled = {r["adaptation"] for r in jl(os.path.join(OUT, "adjudications.jsonl"))}
rows = jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
if a.ids:
    if a.ids.endswith(".jsonl"):
        want = {json.loads(l)["adaptation"] for l in open(a.ids, encoding="utf-8") if l.strip()}
    else:
        want = {l.strip() for l in open(a.ids, encoding="utf-8") if l.strip()}
    page = [r for r in rows if r["id"] in want]
else:
    page = sorted((r for r in rows if r.get("element") == a.element and r["op"] == a.op and r["id"] not in ruled),
                  key=lambda r: (r["sub"].lower(), r["op"], r["id"]))[:100]
subs = {r["sub"] for r in page}
hr = {}
for l in open(os.path.join(ST, "codes.jsonl"), encoding="utf-8"):
    c = json.loads(l)
    if c["sub"] in subs:
        hr[(c["sub"], c["code_id"])] = c.get("hour")
for r in page:
    hs = [(c, hr.get((r["sub"], c))) for c in codes(r)]
    known = [h for _, h in hs if isinstance(h, (int, float))]
    if known and min(known) > 73:
        tag = "ALL AFTER 73"
    elif known and max(known) > 73:
        tag = "some after 73"
    else:
        continue
    print("%-14s %s  %s" % (tag, r["id"], ", ".join("%s h%s" % (c, h) for c, h in hs)))
