#!/usr/bin/env python3
"""D4a-06: read a form's members as rooms (the cut carried, k from d4a06_forms.json). Prints the best fits (the
largest share of selected changes on the form's signature, then more changes), the misfits the signature rule
takes out (Ward members placed elsewhere, those with the most changes first) and the placed members with the
smallest signature share; for each room its counts on the signatures and up to N of its lines' how sentences,
those on the form's signature first. Read-only.

    python3 out/_analysis/d4a06_read.py --form A --n 3
"""
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import adaptation_ledger as al  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
ap.add_argument("--n", type=int, default=3)
ap.add_argument("--k")
ap.add_argument("--lines", type=int, default=3)
ap.add_argument("--rooms", help="comma-separated rooms to read instead")
a = ap.parse_args()
T = json.load(open(os.path.join(OUT, "_analysis", "d4a06_forms.json"), encoding="utf-8"))
C = T["cuts"][a.k or str(T["k_stab"])]
sig = {f: {d["node"] for d in v["sig_T4"]} for f, v in C["forms"].items()}
CH = {"add-step", "add-condition", "link", "restrict", "contradict"}
L = [r for r in al.shared_lines(OUT) if r.get("op") in CH and len(r.get("lift") or []) >= 4]
by = {}
for r in L:
    by.setdefault(r["sub"], []).append(r)


def show(s, tag):
    r = C["rooms"][s]
    on = {f: n for f, n in r["on_signature"].items() if n}
    print("  [%s] %s: placed %s (mix %s), %d changes, on signatures %s, share own %.2f%s" % (
        tag, s, r["form"], r["mix_form"], r["changes"], on, r["share_own"], (", tied " + ",".join(r["tied"])) if r["tied"] else ""))
    lines = sorted(by.get(s, []), key=lambda x: (x["lift"][2] not in sig[a.form], x["id"]))
    for x in lines[:a.lines]:
        print("     - %s %s %s/%s: %s" % (x["op"], x["element"], x["lift"][1], x["lift"][2], (x.get("how") or "").strip()))


if a.rooms:
    for s in a.rooms.split(","):
        show(s, "asked")
    sys.exit()
f = a.form
placed = [s for s, r in C["rooms"].items() if r["form"] == f]
best = sorted(placed, key=lambda s: (-C["rooms"][s]["share_own"], -C["rooms"][s]["changes"], s.lower()))[:a.n]
best_def = sorted((s for s in placed if C["rooms"][s]["defining"] and s not in best),
                  key=lambda s: (-C["rooms"][s]["share_own"], -C["rooms"][s]["changes"], s.lower()))[:a.n]
best = best + best_def
out = sorted((s for s, r in C["rooms"].items() if r["mix_form"] == f and r["form"] != f),
             key=lambda s: (-C["rooms"][s]["changes"], s.lower()))[:a.n]
low = sorted((s for s in placed if C["rooms"][s]["defining"]),
             key=lambda s: (C["rooms"][s]["share_own"], -C["rooms"][s]["changes"], s.lower()))[:a.n]
print("== form", f, "placed", len(placed), "signature", sorted(sig[f]))
for s in best:
    show(s, "best")
for s in out:
    show(s, "moved out")
for s in low:
    show(s, "low share")
