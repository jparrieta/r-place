#!/usr/bin/env python3
"""Print, for each ruling of one leg that places a theme or lists it under also_present,
the concept lines behind that theme, read from the packet's chunk files.

Usage: python3 out/_analysis/b4_theme_support_lines.py --leg B4a-02 --packet 2 --theme T3-033
"""
import argparse
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def chunk_sections(packet):
    pdir = os.path.join(OUT, "_adjudication-B4", "packet-%02d" % packet)
    sections = {}
    for name in sorted(os.listdir(pdir)):
        if not re.match(r"chunk-\d+\.md$", name):
            continue
        cur = None
        with open(os.path.join(pdir, name), encoding="utf-8") as fh:
            for line in fh:
                m = re.match(r"### (\d+)\. (\S+), class", line)
                if m:
                    cur = int(m.group(1))
                    sections[cur] = {"head": line.strip(), "label": "", "concepts": {}}
                    continue
                if cur is None:
                    continue
                if line.startswith("**") and not sections[cur]["label"] and "| note:" in line:
                    sections[cur]["label"] = line.strip()
                m = re.match(r"- (c\d{4}) \| (.*)$", line.rstrip("\n"))
                if m:
                    sections[cur]["concepts"][m.group(1)] = m.group(2)
    return sections


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--leg", required=True)
    ap.add_argument("--packet", type=int, required=True)
    ap.add_argument("--theme", required=True)
    args = ap.parse_args()
    sections = chunk_sections(args.packet)
    with open(os.path.join(OUT, "disagreements.jsonl"), encoding="utf-8") as fh:
        rows = [json.loads(l) for l in fh if l.strip()]
    for r in rows:
        if r.get("leg") != args.leg or r.get("packet") != args.packet:
            continue
        ap_ = r.get("also_present") or {}
        if args.theme not in (r.get("ruling") or []) and args.theme not in ap_:
            continue
        sec = sections.get(r["n"], {})
        where = "ruling" if args.theme in (r.get("ruling") or []) else "also_present"
        cids = (r.get("support_by_theme") or {}).get(args.theme) or ap_.get(args.theme) or []
        print("%s | %s %s | ruling %s | %s" % (sec.get("head", r["n"]), args.theme, where,
                                              ",".join(r.get("ruling") or []), r.get("taxonomy")))
        if sec.get("label"):
            print("  " + sec["label"])
        if not cids:
            print("  (no support listed for %s; the readers' concepts stand)" % args.theme)
        for c in cids:
            print("  - %s | %s" % (c, sec.get("concepts", {}).get(c, "(not found)")))
        print()


if __name__ == "__main__":
    main()
