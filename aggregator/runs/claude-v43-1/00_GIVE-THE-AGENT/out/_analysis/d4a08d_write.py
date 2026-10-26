#!/usr/bin/env python3
"""D4a-08: the room-forms tree files, from d4a08d_tree.json. One file per call, to stdout.

    python3 out/_analysis/d4a08d_write.py --what nwk > out/room-forms-tree.nwk
    python3 out/_analysis/d4a08d_write.py --what linkage > out/room-forms-tree-linkage.tsv
    python3 out/_analysis/d4a08d_write.py --what rooms > out/room-forms-tree-rooms.tsv
"""
import argparse, json, os

AN = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--what", choices=("nwk", "linkage", "rooms"), required=True)
a = ap.parse_args()
d = json.load(open(os.path.join(AN, "d4a08d_tree.json"), encoding="utf-8"))


def tsv(cols, rows):
    print("\t".join(cols))
    for r in rows:
        print("\t".join("" if r.get(c) is None else str(r.get(c)) for c in cols))


if a.what == "nwk":
    print(d["newick"])
elif a.what == "linkage":
    tsv(["merge", "node", "a", "b", "height", "rooms", "kind", "label", "ward_node", "k_from", "k_to", "placed_room"], d["rows"])
else:
    ks = ["k%d" % k for k in range(2, 31)]
    tsv(["room", "leaf_id", "role", "selected_changes", "coded_concepts", "form", "form_name"] + ks +
        ["address", "placed_by", "reached_room", "distance_to_reached", "drawn_height", "height_capped", "near_equal_splits"], d["table"])
