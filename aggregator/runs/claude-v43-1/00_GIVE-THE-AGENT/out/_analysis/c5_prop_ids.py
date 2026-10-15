#!/usr/bin/env python3
"""C5a-02: rename the proposition keys in c5_propositions.json from N1..N9 to N01..N09, the form the check requires
(vlib.PROPOSITION, ^N\\d{2,3}$). Keys only; nothing else in the spec changes. Refuses if a key is already of the form.

    python3 out/_analysis/c5_prop_ids.py
"""
import collections, json, os, re, sys

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c5_propositions.json")
spec = json.load(open(P, encoding="utf-8"), object_pairs_hook=collections.OrderedDict)
if any(re.match(r"^N\d{2,3}$", k) for k in spec):
    sys.exit("a key is already of the form N01")
new = collections.OrderedDict(("N%02d" % int(k[1:]), v) for k, v in spec.items())
json.dump(new, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("renamed: %s" % ", ".join(new))
