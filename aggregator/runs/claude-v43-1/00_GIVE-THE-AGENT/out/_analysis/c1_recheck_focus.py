#!/usr/bin/env python3
"""C1: a focused read packet for a gate change whose amendment can only take concepts out of one theme (gate:6, T3-011's
'called to it by the room's own members', can only move an arriving request out of T3-011). For each owed placement
not yet rechecked: the item's label and note, its line (themes with their concept counts and concepts), the concepts
that support the named theme, whole (id | label | the participant's words), and the item's other concepts' labels only.
Writes out/_analysis/c1_rechecks/<ref>-focus.md, refusing to overwrite.

    python3 out/_analysis/c1_recheck_focus.py --change gate:6 --theme T3-011
"""
import argparse, importlib.util, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib
spec = importlib.util.spec_from_file_location("bpf", os.path.join(AN, "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--change", required=True); ap.add_argument("--theme", required=True)
    a = ap.parse_args()
    o = next((x for x in vlib.owed_rechecks(OUT, "C1") if x["ref"] == a.change), None)
    if o is None:
        sys.exit("no change %s" % a.change)
    fin = {(r["sub"], r["theme_id"]): r for r in jl("assignments_final.jsonl")}
    store = bpf.pk.Store(ROOT, OUT)
    todo = [k for k in o["owed"] if k not in o["done"]]
    L = ["# Rechecks for %s, focused on %s's concepts" % (a.change, a.theme), "",
         "To do %d of %d owed." % (len(todo), len(o["owed"])), ""]
    for i, k in enumerate(todo, 1):
        s, t = k
        th = store.themes[k]
        r = fin[k]
        sup = r.get("support_by_theme") or {}
        L += ["### %d. %s/%s" % (i, s, t), "", "**%s** | note: %s" % (th.get("second_order"), th.get("theme_note")), ""]
        L.append("**Now placed:** %s" % "; ".join("%s (%d)=%s" % (x, len(sup.get(x) or []), ",".join(sup.get(x) or []))
                                                  for x in (r.get("third_order") or [])))
        L.append("")
        mine = set(sup.get(a.theme) or [])
        for cid in th.get("code_ids") or []:
            cd = store.codes.get((s, cid))
            if cd and cid in mine:
                L.append("- **%s** | %s | %s" % (cid, cd.get("first_order"), " ".join(str(cd.get("text") or "").split())))
        rest = [cid for cid in th.get("code_ids") or [] if cid not in mine and store.codes.get((s, cid))]
        if rest:
            L.append("- others: " + "; ".join("%s %s" % (cid, store.codes[(s, cid)].get("first_order")) for cid in rest))
        L.append("")
    p = os.path.join(AN, "c1_rechecks", a.change.replace(":", "-") + "-focus.md")
    if os.path.exists(p):
        sys.exit("%s exists" % p)
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote %s: %d items, %d bytes, %d lines" % (os.path.relpath(p, ROOT), len(todo), os.path.getsize(p), len(L)))


if __name__ == "__main__":
    main()
