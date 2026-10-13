#!/usr/bin/env python3
"""C1, J's answer to QC1-002 (22:12 Berlin): lean to one placement; a second theme stands only with three concepts or
more of its own. For each of the 16 lines re-placed in C1a-03 under gates 8 to 14 (the moves of leg C1a-03 made before
QC1-002 was answered), the themes that move added and the concepts each carries. A line keeps an added theme with
three concepts or more; an added theme below three is taken off. Where none stays, the line goes back to its placement
before the move (the move's `from`, with the support the move before it wrote, or the settled line's); where some
stay, the line keeps them and drops only the ones below. Prints the plan; --write makes one `mem.py reassign` each.

    python3 out/_analysis/c1_revert_floor.py [--write]
"""
import argparse, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ITEMS = ["finland:t06", "korea:t15", "mit:t01", "alberta:t04", "placestart:t04", "DatBoi:t01", "unturned:t08",
         "wallstreetbets:t02", "lsu:t01", "slovenia:t03", "notredame:t05", "nyjets:t12", "uoft:t12",
         "unitedkingdom:t10", "czech:t04", "muse:t06"]
FLOOR = 3


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def codes(themes, sup):
    return ";".join("%s=%s" % (t, ",".join(sup[t])) for t in themes)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    fin = {"%s:%s" % (r["sub"], r["theme_id"]): r for r in jl("assignments_final.jsonl")}
    settled = {"%s:%s" % (r["sub"], r["theme_id"]): r for r in jl("assign_final.jsonl")}
    plan = []
    for it in ITEMS:
        r = fin[it]
        mv = [m for m in r.get("moves") or [] if m.get("leg") == "C1a-03"]
        if not mv:
            sys.exit("%s: no C1a-03 move" % it)
        m = mv[0]                                # the gates 8 to 14 re-placement; a later one is this script's own
        i = r["moves"].index(m)
        prev = r["moves"][i - 1]["support"] if i > 0 else settled[it]["support_by_theme"]
        sup = m["support"]
        added = [t for t in m["to"] if t not in m["from"]]
        low = [t for t in added if len(sup.get(t) or []) < FLOOR]
        if not low:
            plan.append((it, "keep", m["to"], sup, added, low, None))
            continue
        kept = [t for t in m["to"] if t not in low]
        if all(t in m["from"] for t in kept) and set(kept) == set(m["from"]):
            new, nsup = list(m["from"]), {t: prev[t] for t in m["from"]}
            kind = "revert"
        else:
            new, nsup = kept, {t: sup[t] for t in kept}
            kind = "drop"
        plan.append((it, kind, new, nsup, added, low, m))
    for it, kind, new, nsup, added, low, m in plan:
        print("%s %s: added %s; below the floor %s -> %s (%s)" % (
            kind, it, ",".join("%s(%d)" % (t, len(fin[it]["support_by_theme"].get(t) or [])) for t in added) or "-",
            ",".join(low) or "-", ",".join(new), codes(new, nsup)))
    if not a.write:
        return
    for it, kind, new, nsup, added, low, m in plan:
        if kind == "keep" or fin[it]["third_order"] == new:
            continue
        cnt = ", ".join("%s on %d concept%s (%s)" % (t, len(m["support"][t]), "" if len(m["support"][t]) == 1 else "s",
                                                      ",".join(m["support"][t])) for t in low)
        why = ("J's answer to QC1-002 (22:12 Berlin): lean to one placement; a second theme stands only with three "
               "concepts or more of its own. The C1a-03 re-placement added %s, below that floor, so it comes off%s." % (
                   cnt, "; the line returns to its placement before that move" if kind == "revert" else
                   "; the themes that meet the floor stay"))
        r = subprocess.run([sys.executable, "-W", "ignore", os.path.join(ROOT, "tools", "mem.py"), "reassign", it,
                            "--theme", ",".join(new), "--codes", codes(new, nsup), "--reason", why],
                           cwd=ROOT, capture_output=True, text=True)
        out = " ".join((r.stdout or "").split())
        if r.returncode != 0 or not out.startswith("moved"):
            sys.exit("stopped at %s: %s %s" % (it, out[:300], (r.stderr or "").strip()[-300:]))
        print("wrote " + it)


if __name__ == "__main__":
    main()
