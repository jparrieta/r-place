#!/usr/bin/env python3
"""B4b-p3, read-only: b4b_packets_check.py's checks over all of out/_packets-B4/ after stratum R took all 185 unresolved
items. The served order is sample-B4.jsonl's 500 (orders 1-500) followed by the lines of sample-B4-R.jsonl read in R
packets (orders 501-667); the 18 R lines read in U and A (order null) are checked to be among the 500, not served again.
Also: the 34 entries of B4b and the 36 of B4b-p2 are unchanged in MANIFEST.json (against the two kept copies).

    python3 out/_analysis/b4b_packets_check3.py
"""
import importlib.util, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
spec = importlib.util.spec_from_file_location("chk", os.path.join(OUT, "_analysis", "b4b_packets_check.py"))
chk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chk)


def main():
    errs = []
    new = json.load(open(os.path.join(chk.TO, "MANIFEST.json"), encoding="utf-8"))
    for f, n in (("packets-B4_MANIFEST_before_R.json", 34), ("packets-B4_MANIFEST_before_R_all.json", 36)):
        old = json.load(open(os.path.join(OUT, "_analysis", f), encoding="utf-8"))
        changed = [k for k in old if new.get(k) != old[k]]
        if changed or len(old) != n:
            errs.append("%s: entries changed or not %d: %s" % (f, n, changed))
    real_jl = chk.jl
    s0 = real_jl(os.path.join(OUT, "sample-B4.jsonl"))
    rr = real_jl(os.path.join(OUT, "sample-B4-R.jsonl"))
    rin = [x for x in rr if x["read_in"] == "R"]
    rua = [x for x in rr if x["read_in"] in ("U", "A")]
    st0 = {(x["sub"], x["theme_id"]): x["stratum"] for x in s0}
    if len(rr) != 185 or len(rin) != 167 or len(rua) != 18:
        errs.append("the R record is not 185 lines (167 read in R packets, 18 in U and A)")
    if any(st0.get((x["sub"], x["theme_id"])) != x["read_in"] or x["order"] is not None for x in rua):
        errs.append("an R line read in U or A is not that stratum's item, or carries an order")
    if sorted([x["order"] for x in s0] + [x["order"] for x in rin]) != list(range(1, 668)):
        errs.append("the served orders are not 1 to 667")
    def jl(p):
        if os.path.basename(p) == "sample-B4.jsonl":
            return s0 + rin
        return real_jl(p)
    chk.jl = jl
    print("MANIFEST: %d entries; earlier entries unchanged: %s; R record: %d lines, %d read in R packets, %d read in U and A"
          % (len(new), not any("entries changed" in e for e in errs), len(rr), len(rin), len(rua)))
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
