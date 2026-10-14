#!/usr/bin/env python3
"""C1, read-only: run the close-check's last-pass checks on the fourth-order themes and the form pass now, before the
last pass, by calling tools/checks/stage_C1.py's own functions (_history_06, _check_scheme, _check_fourth,
_check_form_pass). Prints the errors and warnings they collect; writes nothing.

    python3 out/_analysis/c1_check_fourth_now.py
"""
import importlib.util, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("c1check", os.path.join(ROOT, "tools", "checks", "stage_C1.py"))
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)
import vlib

hist = c1._history_06(OUT)
ids = c1._check_scheme(OUT, hist)
c1._check_fourth(OUT, ids, hist, None)
c1._check_form_pass(OUT)
print("errors %d" % len(vlib.E))
print("\n".join("  E " + str(m)[:300] for m, _, _ in vlib.E[:20]))
print("warnings %d" % len(vlib.W))
print("\n".join("  W " + str(m)[:300] for m, _, _ in vlib.W[:20]))
