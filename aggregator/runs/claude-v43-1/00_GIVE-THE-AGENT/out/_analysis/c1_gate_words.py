#!/usr/bin/env python3
"""C1, read-only: a triage packet for gate changes that make the T3-010|T3-149 line turn on visible words (gates 15 to
21). For each owed, not yet rechecked item of the named changes (an item owed by several is shown once, with the
changes that owe it), the concepts where the new question can give another answer than the old one:
  A. concepts counted for T3-010 whose label or words name peace, a truce, a deal word, or an attack;
  B. concepts counted for T3-149 whose label and words name none of them;
  C. concepts counted for no theme whose label or words name peace or a truce (for the listing test).
Shown whole (id | label | words). An item with none of the three is listed by name only. Writes
out/_analysis/c1_rechecks/<name>.md, refusing to overwrite.

    python3 out/_analysis/c1_gate_words.py --changes gate:15,gate:16 --name gates-15-21-words
"""
import argparse, importlib.util, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib
spec = importlib.util.spec_from_file_location("bpf", os.path.join(AN, "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)

PEACE = re.compile(r"peace|truce|cease|armistice|aggression|\bnap\b|\bpax\b|paix|\bpace\b|tregua|frieden|parley|treat(y|ies)|\bpact", re.I)
ATTACK = re.compile(r"attack|\bwars?\b|warfare|fight|battle|invad|invasion|raid|hostil|guerra|krieg|combat", re.I)


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--changes", required=True); ap.add_argument("--name", required=True)
    a = ap.parse_args()
    owed = {}
    for o in vlib.owed_rechecks(OUT, "C1"):
        if o["ref"] in a.changes.split(","):
            for k in o["owed"]:
                if k not in o["done"]:
                    owed.setdefault(tuple(k), []).append(o["ref"])
    fin = {(r["sub"], r["theme_id"]): r for r in jl("assignments_final.jsonl")}
    store = bpf.pk.Store(ROOT, OUT)
    L = ["# T3-010|T3-149 triage for %s" % a.changes, "", "%d items owed and not yet rechecked." % len(owed), ""]
    quiet = []
    for k in sorted(owed):
        s, t = k
        th = store.themes[k]
        r = fin[k]
        sup = r.get("support_by_theme") or {}
        counted = set().union(*[set(v or []) for v in sup.values()]) if sup else set()

        def txt(cid):
            cd = store.codes.get((s, cid)) or {}
            return "%s %s" % (cd.get("first_order") or "", " ".join(str(cd.get("text") or "").split()))

        def show(cid):
            cd = store.codes.get((s, cid)) or {}
            return "- **%s** | %s | %s" % (cid, cd.get("first_order"), " ".join(str(cd.get("text") or "").split()))
        A = [c for c in sup.get("T3-010") or [] if PEACE.search(txt(c)) or ATTACK.search(txt(c))]
        B = [c for c in sup.get("T3-149") or [] if not PEACE.search(txt(c)) and not ATTACK.search(txt(c))]
        C = [c for c in th.get("code_ids") or [] if c not in counted and store.codes.get((s, c)) and PEACE.search(txt(c))]
        head = "%s/%s [%s]: %s" % (s, t, ",".join(owed[k]), "; ".join(
            "%s (%d)" % (x, len(sup.get(x) or [])) for x in (r.get("third_order") or [])) or "no theme")
        if not (A or B or C):
            quiet.append(head)
            continue
        L += ["### " + head, "", "*%s*" % th.get("second_order"), ""]
        for lab, xs in (("A. counted T3-010, naming peace, a deal word or an attack", A),
                        ("B. counted T3-149, naming none", B), ("C. counted for no theme, naming peace or a truce", C)):
            if xs:
                L.append(lab + ":")
                L += [show(c) for c in xs]
        L.append("")
    L += ["## Items where no counted T3-010 or T3-149 concept and no uncounted concept can cross the line (%d)" % len(quiet), ""]
    L += ["- " + q for q in quiet]
    p = os.path.join(AN, "c1_rechecks", a.name + ".md")
    if os.path.exists(p):
        sys.exit("%s exists" % p)
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote %s: %d items, %d with concepts to read, %d bytes" % (os.path.relpath(p, ROOT), len(owed),
                                                                        len(owed) - len(quiet), os.path.getsize(p)))


if __name__ == "__main__":
    main()
