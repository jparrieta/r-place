"""Print the gate fields of named themes from scheme_v2.jsonl (read-only).

Usage: python3 out/_analysis/c1_theme_fields.py T3-001 T3-095 [--fields must_show,must_not_show]
"""
import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
DEFAULT = "name,must_show,must_not_show,decide_when_both,discriminators"

ap = argparse.ArgumentParser()
ap.add_argument("ids", nargs="+")
ap.add_argument("--fields", default=DEFAULT)
ap.add_argument("--vs", default="", help="keep only discriminators against these ids (comma list)")
a = ap.parse_args()
vs = set(x for x in a.vs.split(",") if x)

themes = {}
with open(os.path.join(OUT, "scheme_v2.jsonl"), encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            t = json.loads(line)
            themes[t["id"]] = t

fields = a.fields.split(",")
for tid in a.ids:
    t = themes.get(tid)
    if t is None:
        print("## " + tid + ": not in scheme_v2.jsonl")
        continue
    print("## " + tid + " (" + str(t.get("tier", "")) + ")")
    for k in fields:
        v = t.get(k)
        if k == "discriminators" and vs and isinstance(v, list):
            v = [x for x in v if x.get("vs") in vs]
        if v in (None, "", [], {}):
            continue
        if isinstance(v, (dict, list)):
            v = json.dumps(v, ensure_ascii=False)
        print("- " + k + ": " + str(v))
    print()
