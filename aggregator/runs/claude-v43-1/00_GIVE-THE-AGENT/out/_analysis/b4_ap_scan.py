#!/usr/bin/env python3
"""B4a-05: J's ruling of 13 October (09:09 Berlin): rule (1) extends to also_present; also_present lists only themes
that a reader or my B1 named. This scan finds the ruled lines whose also_present holds a theme outside the placements.

    python3 out/_analysis/b4_ap_scan.py [--packet N] [--decisions-dir DIR] [--list]

Read-only on the ledger. "Placed" is the readings' lists and my B1 grouping (rule 1's placements); "named, broad"
adds the themes a reader listed only under its own also_present (QB4-002 asks J which reading holds). Per packet it
counts the lines touched under each reading and the bags that keep no also_present theme. --list prints each line
touched. --decisions-dir writes, per packet, decisions-apNN.jsonl for b4_rerule_draft.py: the old ruling and
concepts, also_present cut to placed themes, and the old why with one sentence added; a bag left with no
also_present theme is not written there but listed in emptied-apNN.jsonl to be re-ruled by hand.
"""
import argparse
import collections
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def ap_themes(v):
    if isinstance(v, dict):
        return set(v)
    if isinstance(v, list):
        s = set()
        for e in v:
            if isinstance(e, dict) and e.get("theme"):
                s.add(e["theme"])
            elif isinstance(e, str):
                s.add(e)
        return s
    return set()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", type=int)
    ap.add_argument("--decisions-dir")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--ledger", help="a ledger file name in out/ to scan instead of disagreements.jsonl")
    ap.add_argument("--reading", choices=("placed", "named"), default="placed",
                    help="which themes also_present may keep in the decisions: placed only, or named (placed or "
                         "listed in a reader's own also_present); files for 'named' carry the suffix -named")
    a = ap.parse_args()
    raw_ap = collections.defaultdict(set)
    for x in jl(os.path.join(OUT, "assign_raw.jsonl")):
        if x["copy_kind"] == "corpus":
            raw_ap["%s/%s" % (x["sub"], x["theme_id"])] |= ap_themes(x.get("also_present"))
    rows = jl(os.path.join(OUT, a.ledger or "disagreements.jsonl"))
    stat = collections.defaultdict(collections.Counter)
    dropped = collections.Counter()
    dropped_named = collections.Counter()
    dec = collections.defaultdict(list)
    emptied = collections.defaultdict(list)
    for d in rows:
        p = d.get("packet")
        if a.packet and p != a.packet:
            continue
        apd = d.get("also_present") or {}
        stat[p]["lines"] += 1
        if not apd:
            continue
        stat[p]["with also_present"] += 1
        key = "%s/%s" % (d["sub"], d["theme_id"])
        placed = set(d["readers"][0]) | set(d["readers"][1]) | set(d.get("b1") or [])
        broad = placed | raw_ap[key]
        dn = sorted(t for t in apd if t not in placed)
        db = sorted(t for t in apd if t not in broad)
        if not dn:
            continue
        stat[p]["touched (placed)"] += 1
        if db:
            stat[p]["touched (broad)"] += 1
        left = {t: v for t, v in apd.items() if t in placed}
        bag = d["taxonomy"] == "item-is-a-bag"
        if not left:
            stat[p]["also_present emptied (placed)"] += 1
            if bag:
                stat[p]["bags emptied (placed)"] += 1
        if not {t: v for t, v in apd.items() if t in broad} and bag:
            stat[p]["bags emptied (broad)"] += 1
        for t in dn:
            dropped[t] += 1
        for t in db:
            dropped_named[t] += 1
        if a.list:
            print("packet %s item %s %s | %s | ruling %s | b1 %s | readers %s | ap %s | drop %s | broad-drop %s"
                  % (p, d["n"], key, d["taxonomy"], d["ruling"], d.get("b1"), d["readers"], sorted(apd), dn, db))
        keepset, drop, verb = (placed, dn, "placed") if a.reading == "placed" else (broad, db, "named")
        if not drop:
            continue
        kept = {t: v for t, v in apd.items() if t in keepset}
        line = {"n": d["n"], "key": key, "taxonomy": d["taxonomy"], "ruling": d["ruling"], "ap_old": apd,
                "ap_new": kept, "dropped": dn, "broad_dropped": db}
        if bag and not kept:
            emptied[p].append(line)
        else:
            w = (str(d.get("why") or "").rstrip() + " Under J's ruling of 13 October (09:09 Berlin) also_present "
                 "drops %s, which neither reading nor my B1 %s." % (" and ".join(drop), verb))
            dec[p].append({"n": d["n"], "r": d["ruling"], "w": w, "ap": kept})
    for p in sorted(stat):
        print("packet %s: %s" % (p, dict(stat[p])))
    tot = collections.Counter()
    for p in stat:
        tot.update(stat[p])
    print("all: %s" % dict(tot))
    print("themes dropped (placed): %s" % dropped.most_common(25))
    print("themes dropped (named): %s; %d entries" % (dropped_named.most_common(25), sum(dropped_named.values())))
    if a.decisions_dir:
        os.makedirs(a.decisions_dir, exist_ok=True)
        sfx = "" if a.reading == "placed" else "-named"
        for p in sorted(set(dec) | set(emptied)):
            if dec[p]:
                fp = os.path.join(a.decisions_dir, "decisions-ap%02d%s.jsonl" % (p, sfx))
                with open(fp, "w", encoding="utf-8") as fh:
                    for r in dec[p]:
                        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
                print("wrote %s (%d)" % (os.path.relpath(fp, ROOT), len(dec[p])))
            if emptied[p]:
                fp = os.path.join(a.decisions_dir, "emptied-ap%02d%s.jsonl" % (p, sfx))
                with open(fp, "w", encoding="utf-8") as fh:
                    for r in emptied[p]:
                        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
                print("wrote %s (%d)" % (os.path.relpath(fp, ROOT), len(emptied[p])))


if __name__ == "__main__":
    main()
