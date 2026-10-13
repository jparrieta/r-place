#!/usr/bin/env python3
"""B4b, read-only: rule 0 as tools/packets.py reads it from the contract, against the rule 0 paragraph of
RETURN-B3.md and RETURN-B4.md, showing where they first differ.

    python3 out/_analysis/b4b_rule0_diff.py
"""
import importlib.util, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("packets", os.path.join(ROOT, "tools", "packets.py"))
pk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pk)

c = pk.rule0(ROOT)
print("contract (%d chars): %s" % (len(c), c))
for f in ("RETURN-B3.md", "RETURN-B4.md"):
    t = open(os.path.join(ROOT, "out", f), encoding="utf-8").read()
    m = re.search(r"^Rule 0\..*$", t, re.M)
    r = " ".join(m.group(0).split()) if m else ""
    i = next((k for k in range(min(len(c), len(r))) if c[k] != r[k]), min(len(c), len(r)))
    print("%s (%d chars): same=%s; first difference at %d: contract %r | file %r" % (f, len(r), r == c, i, c[i:i + 80], r[i:i + 80]))
