#!/usr/bin/env python3
"""D6a-17: a compact summary of round-2 rooms from d6a11_form_telling.py --facts, with each restrict line's D5 sort.
Prints text. Reads no room's record.

    python3 out/_analysis/d6a17_room_summary.py --form A --rooms monalisaclan,norway,ripcity
"""
import argparse, collections, json, os, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
ap.add_argument("--rooms", required=True)
a = ap.parse_args()
AN = os.path.dirname(os.path.abspath(__file__))
TAG = {"A": "d5a36", "B": "d5a37", "C": "d5a38", "D": "d5a39", "E": "d5a40", "F": "d5a41"}
SORT = {x["id"]: x["code"] for x in json.load(open(os.path.join(AN, "%s_restrict_sorted.json" % TAG[a.form]),
                                                   encoding="utf-8"))["sorted"]}
d = json.loads(subprocess.run([sys.executable, os.path.join(AN, "d6a11_form_telling.py"), "--form", a.form, "--rooms",
                               a.rooms, "--facts"], capture_output=True, text=True, check=True).stdout)
marks = {c["unit"]: (c["size_mark"], c["deciding_ops"]) for c in d["cells"]}
for x in d["rooms"]:
    ops = collections.Counter(c["op"] for c in x["changes"])
    dims = collections.Counter(c["dimension"] for c in x["changes"])
    print("=====", x["sub"], "changes", len(x["changes"]), "concepts", x["coded_concepts"])
    for k in ("carried_as_stated", "absent", "no_line", "ledger_changes_not_selected", "changes_outside_form_cells"):
        print(" %s %d %s" % (k, len(x[k]), x[k]))
    print(" shows", [(u, marks[u][0]) for u in x["shows_form_cells"]])
    print(" lacks", [(u, marks[u][0], "changed by other op" if u in x["changed_units"] else "") for u in
                     x["lacks_form_cells"]])
    print(" ops", dict(ops), "dims", dict(sorted(dims.items(), key=lambda kv: str(kv[0]))))
    for c in x["changes"]:
        s = SORT.get(c["id"], "") if c["op"] == "restrict" and c["arrow"] else ""
        print("  %s %s %s %s | %s %s | %s %s %s | %s" % (c["op"], c["unit"], c["arrow"] or "", s, c["t3"],
                                                        c["t3_name"], c["t4"], c["t4_name"], c["dimension"], c["how"]))
