#!/usr/bin/env python3
"""B4b, read-only: check what out/_packets-B4/ serves, independently of the builder.

- The folder holds only index.md, G01.md to G21.md, the S05 packets and MANIFEST.json: no sample, order, return,
  ruling or note file.
- Each packet: under 51,200 bytes, at most 15 items, ends with packets.py's end line, its brief's item count, its
  positions 1..n and its MANIFEST entry (items, bytes, sha256) agree.
- The 500 sample items are served once each, in sample-B4.jsonl's serving order; each heading's fleet theme id
  translates back (fleet_ids.jsonl) to the sampled room and theme.
- Each item's concept lines carry exactly the fleet code ids MANIFEST's codes_by_item gives for it.
- No third-order id (T3-), no room id in an id position, no canvas field in any item packet; words that could hint at
  a decision (ruling, adjudicat, settled, stratum, unresolved, disagree, B1, analyst) are counted and shown with their
  line, to be read: inside participants' words they are no hint.

    python3 out/_analysis/b4b_packets_check.py
"""
import collections, hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
TO = os.path.join(OUT, "_packets-B4")
sys.path.insert(0, os.path.join(ROOT, "tools"))
END = ("This is the end of the packet. Confirm you reached it by returning your lines and then the "
       "end marker the return specification names. END OF PACKET")
HINT = re.compile(r"\b(rulings?|adjudicat\w*|settled|stratum|strata|unresolved|disagree\w*|B1|analyst)\b", re.I)


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    errs, notes = [], []
    files = sorted(os.listdir(TO))
    shared = ["index.md"] + ["G%02d.md" % i for i in range(1, 22)]
    packets = [f for f in files if re.match(r"^S05-\d{2}\.md$", f)]
    extra = [f for f in files if f not in shared + packets + ["MANIFEST.json"]]
    if extra:
        errs.append("the folder holds other files: %s" % extra)
    missing = [f for f in shared if f not in files]
    if missing:
        errs.append("shared pages missing: %s" % missing)
    man = json.load(open(os.path.join(TO, "MANIFEST.json"), encoding="utf-8"))
    if sorted(man) != sorted(p[:-3] for p in packets):
        errs.append("MANIFEST and packet files differ")
    fid = {}
    for r in jl(os.path.join(OUT, "fleet_ids.jsonl")):
        if r["kind"] == "t":
            fid[r["fleet"]] = (r["sub"], r["id"])
    order = [(r["sub"], r["theme_id"]) for r in sorted(jl(os.path.join(OUT, "sample-B4.jsonl")), key=lambda r: r["order"])]
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
        if not t.rstrip("\n").endswith(END):
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
            cids = re.findall(r"^- (C\d{7})  ", part, re.M)
            if cids != cbi.get(tf):
                errs.append("%s position %s: concept ids differ from codes_by_item" % (name, pos))
        if re.search(r"\bT3-\d{3}\b", t):
            errs.append("%s carries a third-order id" % name)
        if re.search(r"^(### \d+\. r/\S+ [ct]\d|- [ct]\d{4}\s)", t, re.M):
            errs.append("%s carries a room id in an id position" % name)
        if re.search(r"\bcanvas_[a-z_]+\b", t):
            errs.append("%s carries a canvas field" % name)
        for ln in t.splitlines():
            if HINT.search(ln):
                hints.append("%s: %s" % (name, ln.strip()[:160]))
    if served != order:
        errs.append("the served items are not the sample in its serving order (%d served, %d sampled)" % (len(served), len(order)))
    if len(set(served)) != len(served):
        errs.append("an item is served twice")
    big = max(os.path.getsize(os.path.join(TO, f)) for f in shared)
    print("files %d: shared %d (largest %d bytes), packets %d, MANIFEST 1; items served %d, distinct %d; lines due %d"
          % (len(files), len(shared), big, len(packets), len(served), len(set(served)), sum(v["items"] for v in man.values())))
    print("lines with a word that could hint at a decision: %d" % len(hints))
    for h in hints:
        print("  " + h)
    for x in errs:
        print("ERROR " + x)
    print("%d errors" % len(errs))
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
