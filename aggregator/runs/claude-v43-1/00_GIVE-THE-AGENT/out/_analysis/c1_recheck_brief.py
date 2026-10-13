#!/usr/bin/env python3
"""C1: the read packet of c1_recheck_packets.py without the scheme fields repeated under every item (the amended
sentences are printed once at the top). For each owed placement not yet rechecked: the item's label, note and
concepts, whole (id | label | the participant's words), and its line in assignments_final.jsonl. Writes
out/_analysis/c1_rechecks/<ref>-brief.md (gate:2 -> gate-2-brief.md), refusing to overwrite.

    python3 out/_analysis/c1_recheck_brief.py --change gate:2
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
    ap = argparse.ArgumentParser(); ap.add_argument("--change", required=True)
    a = ap.parse_args()
    o = next((x for x in vlib.owed_rechecks(OUT, "C1") if x["ref"] == a.change), None)
    if o is None:
        sys.exit("no change %s" % a.change)
    g = next(x for x in vlib.gate_changes(OUT, "C1") if x["ref"] == a.change)
    fin = {(r["sub"], r["theme_id"]): r for r in jl("assignments_final.jsonl")}
    store = bpf.pk.Store(ROOT, OUT)
    todo = [k for k in o["owed"] if k not in o["done"]]
    L = ["# Rechecks for %s: %s %s (brief)" % (a.change, g["theme"], g["field"]), "",
         "**Was:** %s" % json.dumps(g["was"], ensure_ascii=False), "", "**Now:** %s" % json.dumps(g["now"], ensure_ascii=False), "",
         "Candidates %d, owed %d%s, done %d, to do %d." % (len(o["candidates"]), len(o["owed"]),
                                                       " (a seeded sample)" if o["sampled"] else "", len(o["done"]), len(todo)), ""]
    for i, k in enumerate(todo, 1):
        s, t = k
        th = store.themes[k]
        r = fin[k]
        L += ["### %d. %s/%s" % (i, s, t), "", "**%s** | note: %s" % (th.get("second_order"), th.get("theme_note")), ""]
        for cid in th.get("code_ids") or []:
            cd = store.codes.get((s, cid))
            if cd:
                L.append("- %s | %s | %s" % (cid, cd.get("first_order"), " ".join(str(cd.get("text") or "").split())))
        L.append("")
        L.append("**Now placed:** %s; support %s; also_present %s; flagged B1 %s; source %s; class %s" % (
            ", ".join(r.get("third_order") or []) or "(none)",
            "; ".join("%s=%s" % (x, ",".join(v)) for x, v in (r.get("support_by_theme") or {}).items()) or "-",
            ", ".join((r.get("also_present") or {}).keys()) or "-",
            ", ".join(r.get("b1_themes_without_reader_support") or []) or "-", r.get("source"), r.get("class")))
        L.append("")
    d = os.path.join(AN, "c1_rechecks")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, a.change.replace(":", "-") + "-brief.md")
    if os.path.exists(p):
        sys.exit("%s exists" % p)
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote %s: %d items, %d bytes, %d lines" % (os.path.relpath(p, ROOT), len(todo), os.path.getsize(p), len(L)))


if __name__ == "__main__":
    main()
