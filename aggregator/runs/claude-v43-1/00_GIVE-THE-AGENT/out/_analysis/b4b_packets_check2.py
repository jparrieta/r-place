#!/usr/bin/env python3
"""B4b-p2, read-only: b4b_packets_check.py's checks over all of out/_packets-B4/ after stratum R was added, with the
served order taken from sample-B4.jsonl and its sibling sample-B4-R.jsonl together (orders 1 to 518), and one more:
the 34 MANIFEST entries of B4b are unchanged (against out/_analysis/packets-B4_MANIFEST_before_R.json) and the 34
packet files still match them.

    python3 out/_analysis/b4b_packets_check2.py
"""
import importlib.util, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
spec = importlib.util.spec_from_file_location("chk", os.path.join(OUT, "_analysis", "b4b_packets_check.py"))
chk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chk)


def main():
    errs = []
    old = json.load(open(os.path.join(OUT, "_analysis", "packets-B4_MANIFEST_before_R.json"), encoding="utf-8"))
    new = json.load(open(os.path.join(chk.TO, "MANIFEST.json"), encoding="utf-8"))
    changed = [k for k in old if new.get(k) != old[k]]
    if changed or len(old) != 34:
        errs.append("B4b's MANIFEST entries changed: %s" % changed)
    added = sorted(set(new) - set(old))
    rows = chk.jl(os.path.join(OUT, "sample-B4.jsonl")) + chk.jl(os.path.join(OUT, "sample-B4-R.jsonl"))
    orders = sorted(r["order"] for r in rows)
    if orders != list(range(1, 519)):
        errs.append("the two sample records do not hold orders 1 to 518")
    # run the B4b check with the joined order: write nothing, patch its reader of the sample
    real_jl = chk.jl
    def jl(p):
        if os.path.basename(p) == "sample-B4.jsonl":
            return real_jl(p) + real_jl(os.path.join(OUT, "sample-B4-R.jsonl"))
        return real_jl(p)
    chk.jl = jl
    print("MANIFEST: %d entries; B4b's 34 unchanged: %s; added %s" % (len(new), not changed, added))
    for x in errs:
        print("ERROR " + x)
    try:
        chk.main()
    except SystemExit as e:
        if e.code or errs:
            sys.exit(1)
    if errs:
        sys.exit(1)


if __name__ == "__main__":
    main()
