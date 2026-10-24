#!/usr/bin/env python3
"""D4a-01: A11's census classes by id, for the history line of A11's amendment. Runs D3a-38's census
(d3_a11_census.py with the re-rulings that d3_a11_census2.py applies, the same rules and priority) and writes, per
class, the line ids and the rooms (each room once, by the census's priority), plus the first-return A11 restrict
lines accepted as specifications whose 'how' names settling. Prints the counts, so they can be checked against
d3_a11_census_run2.txt. Run from the folder root. Writes only --out, and never overwrites.

    python3 out/_analysis/d4a01_a11_classes.py --out out/_analysis/d4a01_a11_classes.json
"""
import argparse, collections, contextlib, io, json, os

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
a = ap.parse_args()
if os.path.exists(a.out):
    raise SystemExit("refusing to overwrite %s" % a.out)
src = open("out/_analysis/d3_a11_census2.py", encoding="utf-8").read()
ns = {"__name__": "census2"}
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(src, "d3_a11_census2.py", "exec"), ns)
line_class = ns["line_class"]
by_id = {}
for name in ("adaptations.jsonl", "adaptations-recheck.jsonl"):
    for l in open(os.path.join("out", name), encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            by_id[r["id"]] = r
PRIORITY = ["transition", "templatefirst", "across", "onepost", "talkonly", "layoutonly", "oneend", "held", "el",
            "other", "limit"]
cls_lines = collections.defaultdict(list)
room_classes = collections.defaultdict(set)
for i, c in line_class.items():
    cls_lines[c].append(i)
    room_classes[by_id[i]["sub"]].add(c)
rooms_once = collections.defaultdict(list)
for s, cs in room_classes.items():
    for c in PRIORITY:
        if c in cs:
            rooms_once[c].append(s)
            break
last = {}
for l in open("out/adjudications.jsonl", encoding="utf-8"):
    if l.strip():
        r = json.loads(l)
        last[r["adaptation"]] = r
settl = sorted(i for i, l in by_id.items() if l.get("element") == "A11" and l.get("op") == "restrict"
               and not i.startswith("R-") and "settl" in (l.get("how") or "").lower()
               and (last.get(i, {}).get("decision"), last.get(i, {}).get("kind")) == ("accept", "specification"))
out = {"source": "d3_a11_census2.py (D3a-38), re-run at D4a-01",
       "lines_by_class": {c: sorted(v) for c, v in cls_lines.items()},
       "rooms_once_by_priority": {c: sorted(v, key=str.lower) for c, v in rooms_once.items()},
       "restrict_naming_settling_accepted_specification": settl}
json.dump(out, open(a.out, "w", encoding="utf-8"), indent=1)
print("lines by class:", {c: len(v) for c, v in cls_lines.items()})
print("rooms once, by priority:", {c: len(rooms_once[c]) for c in PRIORITY})
print("first-return restrict lines naming settling, accepted as specifications:", len(settl))
print("talk-only rooms:", ", ".join(sorted(rooms_once["talkonly"], key=str.lower)))
print("wrote", a.out)
