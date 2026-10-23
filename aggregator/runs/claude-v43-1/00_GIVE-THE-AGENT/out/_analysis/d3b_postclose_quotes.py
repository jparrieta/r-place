#!/usr/bin/env python3
"""D3b: for re-check lines with cited concepts after hour 73 (as d3b_postclose.py lists them), quote through cite.py
every concept of the line after hour 73, with the line's how, so that each can be read as a report of the event's
canvas, upkeep on a successor canvas or edits to a copy (G11's readings). Reads only.

    python3 out/_analysis/d3b_postclose_quotes.py --element P05 --op instantiate
    python3 out/_analysis/d3b_postclose_quotes.py --element P05 --op instantiate --ids out/_analysis/d3_rulings/recheck-P05-inst-000.jsonl
"""
import argparse, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ST = os.path.join(ROOT, "package", "store")
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--op", required=True)
ap.add_argument("--ids", help="optional file of ids, one a line, or a rulings .jsonl, to check instead of the current packet")
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
        want = {r["adaptation"] for r in jl(a.ids)}
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
cite = os.path.join(ROOT, "tools", "cite.py")
for r in page:
    hs = [(c, hr.get((r["sub"], c))) for c in codes(r)]
    late = [c for c, h in hs if isinstance(h, (int, float)) and h > 73]
    if not late:
        continue
    known = [h for _, h in hs if isinstance(h, (int, float))]
    tag = "ALL AFTER 73" if min(known) > 73 else "some after 73"
    print("== %s  %s  %s" % (r["id"], r["sub"], tag))
    print("   how: %s" % (r.get("how") or ""))
    print("   hours: %s" % ", ".join("%s h%s" % (c, h) for c, h in hs))
    for c in late:
        p = subprocess.run([sys.executable, cite, "--room", r["sub"], "--code", c], capture_output=True, text=True)
        for ln in p.stdout.splitlines():
            if ln.startswith('"'):
                print("   " + ln)
    print()
