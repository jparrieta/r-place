#!/usr/bin/env python3
"""C1, J's floor (QC1-002) on my own earlier C1 re-placements: take a theme that a move of --leg added below three
concepts off the named lines. A theme that same move dropped (pushed past third) comes back with the support it had
before the move. The other themes keep their current support. Prints the plan; --write makes one `mem.py reassign`
each, with the reason naming the concepts and the floor.

    python3 out/_analysis/c1_floor_drop.py --items "aggies:t07,sixers:t06" --theme T3-084 --leg C1a-02 [--write]
"""
import argparse, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", required=True); ap.add_argument("--theme", required=True); ap.add_argument("--leg", required=True)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    fin = {"%s:%s" % (r["sub"], r["theme_id"]): r for r in jl("assignments_final.jsonl")}
    settled = {"%s:%s" % (r["sub"], r["theme_id"]): r for r in jl("assign_final.jsonl")}
    plan = []
    for it in [x.strip() for x in a.items.split(",") if x.strip()]:
        r = fin[it]
        th, sup = list(r["third_order"]), dict(r["support_by_theme"])
        mv = [m for m in r.get("moves") or [] if m.get("leg") == a.leg and a.theme in m["to"] and a.theme not in (m.get("from") or [])]
        if len(mv) != 1 or a.theme not in th or len(sup.get(a.theme) or []) >= 3 or th[0] == a.theme:
            sys.exit("%s: not a below-floor addition of %s at %s" % (it, a.theme, a.leg))
        m = mv[0]
        i = r["moves"].index(m)
        prev = r["moves"][i - 1]["support"] if i > 0 else settled[it]["support_by_theme"]
        gone = sup[a.theme]
        new = [t for t in th if t != a.theme]
        held = set(gone).union(*[set(sup[t]) for t in new])     # concepts that left with the move or count elsewhere
        cand = {t: [c for c in prev.get(t) or [] if c not in held] for t in m["from"] if t not in m["to"] and t not in new}
        back = [t for t, cs in cand.items() if len(cs) >= 3 or (not new and cs)]
        new += back
        nsup = {t: (sup[t] if t in sup else cand[t]) for t in new}
        new.sort(key=lambda t: -len(nsup[t]))           # stable: equal counts keep their order
        plan.append((it, th, new, nsup, gone, back))
    for it, th, new, nsup, gone, back in plan:
        print("%s: %s -> %s (%s off on %s%s)" % (it, ",".join(th), ",".join(new), a.theme, ",".join(gone),
                                                 "; back: " + ",".join(back) if back else ""))
    if not a.write:
        return
    for it, th, new, nsup, gone, back in plan:
        why = ("J's answer to QC1-002 (22:12 Berlin): a second or third theme stands only with three concepts or more of its "
               "own. %s was added here at %s on %d concept%s (%s), under rule 0's old 'a theme alone at its level is kept', "
               "which the floor replaces; it comes off. The concepts stay out of T3-011 and T3-062, whose gates (5 to 7, the "
               "visitor rule) exclude an arriving request.%s" % (
                   a.theme, a.leg, len(gone), "" if len(gone) == 1 else "s", ", ".join(gone),
                   " %s, pushed off by that move, comes back with its earlier concepts." % ", ".join(back) if back else ""))
        codes = ";".join("%s=%s" % (t, ",".join(nsup[t])) for t in new)
        r = subprocess.run([sys.executable, "-W", "ignore", os.path.join(ROOT, "tools", "mem.py"), "reassign", it,
                            "--theme", ",".join(new), "--codes", codes, "--reason", why],
                           cwd=ROOT, capture_output=True, text=True)
        out = " ".join((r.stdout or "").split())
        if r.returncode != 0 or not out.startswith("moved"):
            sys.exit("stopped at %s: %s %s" % (it, out[:300], (r.stderr or "").strip()[-300:]))
        print("wrote " + it)


if __name__ == "__main__":
    main()
