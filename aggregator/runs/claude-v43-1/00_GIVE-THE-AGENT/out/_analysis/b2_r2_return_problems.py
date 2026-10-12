#!/usr/bin/env python3
"""B2b-r2-p2: list every round-2 return line whose concepts are not the item's own (support, also_present,
multiplacement_log codes), with vlib's own checks, and every line missing a field of the return line."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib  # noqa: E402

RAW = os.path.join(OUT, "_fleet_raw", "B2", "round-2")
FIELDS = ["sub", "theme_id", "batch", "agent", "replicate", "position", "third_order", "multi", "why", "confidence",
          "read", "exemplar_read", "families_opened", "t_start", "t", "support"]


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


ct = vlib.code_themes(jl(os.path.join(ROOT, "package", "store", "codes.jsonl")))
ids = {r["id"] for r in jl(os.path.join(OUT, "scheme.jsonl"))}
n = 0
for pk in sorted(os.listdir(RAW)):
    d = os.path.join(RAW, pk)
    if not os.path.isdir(d):
        continue
    for f in sorted(os.listdir(d)):
        if not f.endswith(".jsonl"):
            continue
        for i, x in enumerate(jl(os.path.join(d, f)), 1):
            sub, tid = x.get("sub"), x.get("theme_id")
            P = ["lacks %s" % k for k in FIELDS if k not in x]
            for c in x.get("support") or []:
                th = ct.get((sub, c))
                if th != tid:
                    P.append("support %s is %s" % (c, "not a concept of r/%s" % sub if th is None else "of %s" % th))
            P += ["also_present: " + p for p in vlib.also_present_problems(x.get("also_present"), x.get("third_order"), sub, tid, ct, ids)]
            ml = x.get("multiplacement_log") or {}
            for c in (ml.get("codes") or []) if isinstance(ml, dict) else []:
                th = ct.get((sub, c))
                if th != tid:
                    P.append("multiplacement_log code %s is %s" % (c, "not of r/%s" % sub if th is None else "of %s" % th))
            if P:
                n += 1
                print("%s/%s line %d %s/%s: %s" % (pk, f, i, sub, tid, "; ".join(P)[:600]))
print("%d lines with a problem" % n)
