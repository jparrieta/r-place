#!/usr/bin/env python3
"""B3b: the four half packets (B0192a/b, B0927a/b) were served in room ids with no codes_by_item, so the dispatch
could not refuse a concept outside the item. Check every concept each pass-1 and pass-2 line cites (support,
also_present, multiplacement records) against the item batches-B3.jsonl holds at that position: the item's own,
another item's of the same room (and whether that item is in the packet), or not of the room. Reads only."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import importlib.util
spec = importlib.util.spec_from_file_location("bpf", os.path.join(OUT, "_analysis", "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def cited(x):
    c = list(x.get("support") or [])
    for v in (x.get("also_present") or {}).values():
        c += v if isinstance(v, list) else [v]
    for r in x.get("multiplacement_log") or []:
        if isinstance(r, dict):
            c += list(r.get("support_primary") or []) + list(r.get("support_additional") or [])
    return c


def main():
    store = bpf.pk.Store(ROOT, OUT)
    owner = {}
    for (s, t), th in store.themes.items():
        for c in th.get("code_ids") or []:
            owner[(s, c)] = t
    batches = {b["batch"]: b for b in jl(os.path.join(OUT, "batches-B3.jsonl"))}
    tot = own = 0
    for h in ("B0192a", "B0192b", "B0927a", "B0927b"):
        b = batches[h]
        d = os.path.join(OUT, "_fleet_raw", "B3", h)
        f = [x for x in os.listdir(d) if x.endswith(".jsonl")][0]
        for i, x in enumerate(jl(os.path.join(d, f)), 1):
            if "position" not in x:
                continue
            p = x.get("revises") or x["position"]
            it = b["items"][p - 1]
            s, t = it.split("/")
            if x.get("sub", "").replace("r/", "") != s or (x.get("revises") is None and x.get("theme_id") != t):
                print("%s line %d: typed %s/%s, the cell holds %s" % (h, i, x.get("sub"), x.get("theme_id"), it))
            for c in cited(x):
                tot += 1
                o = owner.get((s, c))
                if o == t:
                    own += 1
                elif o is None:
                    print("%s line %d (%s): %s is no concept of r/%s" % (h, i, it, c, s))
                else:
                    print("%s line %d (%s): %s is %s/%s's%s" % (h, i, it, c, s, o,
                          ", an item of this packet" if "%s/%s" % (s, o) in b["items"] else ""))
    print("concepts cited %d; the item's own %d" % (tot, own))


if __name__ == "__main__":
    main()
