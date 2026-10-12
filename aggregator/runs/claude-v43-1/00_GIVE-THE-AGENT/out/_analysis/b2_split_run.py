#!/usr/bin/env python3
"""B2b-r2-p2: run `mem.py split` from a written cut (QB2-010; J approved the cut by doing).

A cut file, out/_analysis/b2_split_<sub>_<tNN>.txt:
    item: <sub>/<tNN>
    reason: <why the theme is cut>
    child <KEY> | <label> | <note>
    <KEY>: c0001 c0002, c0003 ...        (any number of lines per key; commas or spaces)
The helper checks against the store: every concept of the parent in exactly one child, nothing outside the
parent, each child three concepts or more; it prints what is missing or doubled. Then `mem.py split
--dry-run` (default) or, with --write, the split itself.
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def main():
    path = sys.argv[1]
    item = reason = None
    meta, codes = {}, {}
    for ln in open(path, encoding="utf-8"):
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        if ln.startswith("item:"):
            item = ln[5:].strip(); continue
        if ln.startswith("reason:"):
            reason = ln[7:].strip(); continue
        m = re.match(r"^child\s+(\S+)\s*\|\s*(.+?)\s*\|\s*(.+)$", ln)
        if m:
            meta[m.group(1)] = (m.group(2), m.group(3)); continue
        m = re.match(r"^(\S+):\s*(.*)$", ln)
        if m and m.group(1) in meta:
            codes.setdefault(m.group(1), []).extend(re.findall(r"c\d{4}", m.group(2))); continue
        sys.exit("cannot read line: %s" % ln)
    sub, tid = item.split("/")
    t = None
    for x in open(os.path.join(ROOT, "package", "store", "themes.jsonl"), encoding="utf-8"):
        r = json.loads(x)
        if r["sub"] == sub and r["theme_id"] == tid:
            t = r; break
    have = list(t["code_ids"])
    seen, errs = {}, []
    for k, cs in codes.items():
        for c in cs:
            if c in seen:
                errs.append("%s in both %s and %s" % (c, seen[c], k))
            seen[c] = k
        if len(set(cs)) < 3:
            errs.append("child %s has %d concepts" % (k, len(set(cs))))
    out_ = sorted(set(seen) - set(have))
    miss = [c for c in have if c not in seen]
    if out_:
        errs.append("not concepts of %s: %s" % (item, " ".join(out_)))
    if miss:
        errs.append("unassigned (%d): %s" % (len(miss), " ".join(miss)))
    for k in meta:
        print("  %-4s %3d  %s" % (k, len(set(codes.get(k, []))), meta[k][0]))
    print("%s: %d concepts, %d children" % (item, len(have), len(meta)))
    if errs:
        for e in errs:
            print("ERROR", e)
        sys.exit(1)
    cmd = [sys.executable, os.path.join(ROOT, "tools", "mem.py"), "split", "%s:%s" % (sub, tid)]
    for k in meta:
        lab, note = meta[k]
        cmd += ["--child", "%s|%s|%s" % (lab, note, ",".join(codes[k]))]
    cmd += ["--reason", reason]
    if "--write" not in sys.argv:
        cmd.append("--dry-run")
    p = subprocess.run(cmd, capture_output=True, text=True)
    print("\n".join(l for l in (p.stdout + p.stderr).splitlines() if "Deprecation" not in l and "utcnow" not in l)[-3000:])
    sys.exit(p.returncode)


if __name__ == "__main__":
    main()
