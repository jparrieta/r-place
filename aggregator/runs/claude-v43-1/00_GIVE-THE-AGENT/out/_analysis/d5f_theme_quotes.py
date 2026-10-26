#!/usr/bin/env python3
"""D5, room-form accounts, section 9: for each named fourth-order theme, concepts of one form's defining members that
lift to it (by the same placement mapping as the theme counts), from the members holding the largest share on it, read
through cite.py. Prints one quote line per concept.

    python3 out/_analysis/d5f_theme_quotes.py --form A --themes T4-008,T4-013 --per 3
"""
import argparse, collections, os, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
ap.add_argument("--themes", required=True)
ap.add_argument("--per", type=int, default=3)
a = ap.parse_args()
sys.argv = [sys.argv[0]]
AN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AN)
import d4a08_embed as E  # noqa: E402
import d4a07_features as F  # noqa: E402

DEFS = {s for s in E.FORMS[a.form]["members"] if s in E.IDX}
by = collections.defaultdict(lambda: collections.defaultdict(list))
tot = collections.Counter()
for r in E.CODES:
    s = r["sub"]
    if s not in DEFS:
        continue
    t4s = {F.T4OF3.get(x) for x in E.PLACE.get((s, r.get("theme_id")), [])}
    tot[s] += 1
    for t in t4s:
        if t:
            by[t][s].append(r["code_id"])
for t in a.themes.split(","):
    rooms = sorted(by[t], key=lambda s: (-len(by[t][s]) / tot[s], s.lower()))[:a.per]
    for s in rooms:
        code = by[t][s][len(by[t][s]) // 2]
        out = subprocess.run([sys.executable, "-W", "ignore", os.path.join(E.ROOT, "tools", "cite.py"), "--room", s, "--code", code],
                             capture_output=True, text=True, cwd=E.ROOT).stdout
        line = next((x for x in out.splitlines() if x.startswith('"')), "NOT FOUND")
        print(t, "%.3f" % (len(by[t][s]) / tot[s]), line)
