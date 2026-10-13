#!/usr/bin/env python3
"""B4b-p4, read-only: b4b_packets_check.py's checks over all of out/_packets-B4/ after the 18 unresolved items of U and
A were read again as R's own items. The served order is sample-B4.jsonl's 500 (orders 1-500) followed by all 185 lines
of sample-B4-R.jsonl (orders 501-685). Exactly 18 items are served twice: each once in orders 1-500, in the stratum its
also_in names, and once in orders 668-685; no other item is served twice. Also: the 34 entries of B4b, the 36 of
B4b-p2 and the 46 of B4b-p3 are unchanged in MANIFEST.json (against the three kept copies).

The per-packet checks are b4b_packets_check.py's (its END line, its hint words), repeated here because that script
refuses any item served twice.

    python3 out/_analysis/b4b_packets_check4.py
"""
import collections, hashlib, importlib.util, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
spec = importlib.util.spec_from_file_location("chk", os.path.join(OUT, "_analysis", "b4b_packets_check.py"))
chk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chk)
TO = chk.TO


def main():
    errs = []
    man = json.load(open(os.path.join(TO, "MANIFEST.json"), encoding="utf-8"))
    for f, n in (("packets-B4_MANIFEST_before_R.json", 34), ("packets-B4_MANIFEST_before_R_all.json", 36),
                 ("packets-B4_MANIFEST_before_R_ua.json", 46)):
        old = json.load(open(os.path.join(OUT, "_analysis", f), encoding="utf-8"))
        changed = [k for k in old if man.get(k) != old[k]]
        if changed or len(old) != n:
            errs.append("%s: entries changed or not %d: %s" % (f, n, changed))
    s0 = chk.jl(os.path.join(OUT, "sample-B4.jsonl"))
    rr = chk.jl(os.path.join(OUT, "sample-B4-R.jsonl"))
    st0 = {(x["sub"], x["theme_id"]): x["stratum"] for x in s0}
    un0 = {(x["sub"], x["theme_id"]) for x in s0 if x.get("unresolved")}
    if len(s0) != 500 or sorted(x["order"] for x in s0) != list(range(1, 501)):
        errs.append("sample-B4.jsonl is not 500 lines in orders 1 to 500")
    if len(rr) != 185 or any(x["read_in"] != "R" or x["stratum"] != "R" for x in rr):
        errs.append("the R record is not 185 lines, all R's and read in R packets")
    if sorted(x["order"] for x in rr) != list(range(501, 686)):
        errs.append("the R record's orders are not 501 to 685")
    again = {(x["sub"], x["theme_id"]): x for x in rr if x.get("also_in")}
    if sorted(x["order"] for x in again.values()) != list(range(668, 686)):
        errs.append("the lines with also_in are not orders 668 to 685")
    if set(again) != un0 or any(st0.get(k) != x["also_in"] for k, x in again.items()):
        errs.append("the lines with also_in are not the 18 unresolved items of U and A, each in its stratum")
    order = [(r["sub"], r["theme_id"]) for r in sorted(s0, key=lambda r: r["order"])]
    order += [(r["sub"], r["theme_id"]) for r in sorted(rr, key=lambda r: r["order"])]

    files = sorted(os.listdir(TO))
    shared = ["index.md"] + ["G%02d.md" % i for i in range(1, 22)]
    packets = [f for f in files if re.match(r"^S05-\d{2}\.md$", f)]
    extra = [f for f in files if f not in shared + packets + ["MANIFEST.json"]]
    if extra:
        errs.append("the folder holds other files: %s" % extra)
    if [f for f in shared if f not in files]:
        errs.append("shared pages missing")
    if sorted(man) != sorted(p[:-3] for p in packets):
        errs.append("MANIFEST and packet files differ")
    fid = {}
    for r in chk.jl(os.path.join(OUT, "fleet_ids.jsonl")):
        if r["kind"] == "t":
            fid[r["fleet"]] = (r["sub"], r["id"])
    served, hints = [], []
    for f in packets:
        name = f[:-3]
        b = open(os.path.join(TO, f), "rb").read()
        t = b.decode("utf-8")
        e = man.get(name, {})
        if len(b) > 50 * 1024:
            errs.append("%s is %d bytes" % (name, len(b)))
        if hashlib.sha256(b).hexdigest() != e.get("sha256") or len(b) != e.get("bytes"):
            errs.append("%s: sha256 or bytes differ from MANIFEST" % name)
        if not t.rstrip("\n").endswith(chk.END):
            errs.append("%s does not end with the end line" % name)
        heads = re.findall(r"^### (\d+)\. r/(\S+) (T2-\d{5})$", t, re.M)
        if [int(h[0]) for h in heads] != list(range(1, len(heads) + 1)):
            errs.append("%s: positions are not 1..n" % name)
        m = re.search(r"it holds (\d+) items; return (\d+) lines", t)
        if not m or int(m.group(1)) != len(heads) or int(m.group(2)) != len(heads) or e.get("items") != len(heads):
            errs.append("%s: the brief's count, the headings and MANIFEST disagree" % name)
        if len(heads) > 15:
            errs.append("%s holds %d items" % (name, len(heads)))
        cbi = e.get("codes_by_item") or {}
        parts = re.split(r"^### \d+\. r/\S+ T2-\d{5}$", t, flags=re.M)[1:]
        for (pos, sub, tf), part in zip(heads, parts):
            back = fid.get(tf)
            if not back or back[0] != sub:
                errs.append("%s position %s: %s does not translate back to r/%s" % (name, pos, tf, sub))
                continue
            served.append(back)
            if re.findall(r"^- (C\d{7})  ", part, re.M) != cbi.get(tf):
                errs.append("%s position %s: concept ids differ from codes_by_item" % (name, pos))
        if re.search(r"\bT3-\d{3}\b", t):
            errs.append("%s carries a third-order id" % name)
        if re.search(r"^(### \d+\. r/\S+ [ct]\d|- [ct]\d{4}\s)", t, re.M):
            errs.append("%s carries a room id in an id position" % name)
        if re.search(r"\bcanvas_[a-z_]+\b", t):
            errs.append("%s carries a canvas field" % name)
        for ln in t.splitlines():
            if chk.HINT.search(ln):
                hints.append("%s: %s" % (name, ln.strip()[:160]))
    if served != order:
        errs.append("the served items are not U and A then R in serving order (%d served, %d due)" % (len(served), len(order)))
    twice = {k: n for k, n in collections.Counter(served).items() if n > 1}
    if set(twice) != set(again) or any(n != 2 for n in twice.values()):
        errs.append("the items served twice are not exactly the 18, twice each: %s" % sorted(twice)[:5])
    for k in again:
        at = [i + 1 for i, x in enumerate(served) if x == k]
        if len(at) != 2 or not (at[0] <= 500 and 668 <= at[1] <= 685):
            errs.append("%s/%s is not served once in orders 1-500 and once in 668-685: %s" % (k[0], k[1], at))
    print("MANIFEST: %d entries; earlier entries unchanged: %s; R record: %d lines, %d also in U, %d also in A"
          % (len(man), not any("entries changed" in e for e in errs), len(rr),
             sum(x["also_in"] == "U" for x in again.values()), sum(x["also_in"] == "A" for x in again.values())))
    print("files %d: shared %d, packets %d, MANIFEST 1; items served %d, distinct %d, served twice %d; lines due %d"
          % (len(files), len(shared), len(packets), len(served), len(set(served)), len(twice),
             sum(v["items"] for v in man.values())))
    print("lines with a word that could hint at a decision: %d" % len(hints))
    for h in hints:
        print("  " + h)
    for x in errs:
        print("ERROR " + x)
    print("%d errors" % len(errs))
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
