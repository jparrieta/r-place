#!/usr/bin/env python3
"""C5c-08, problem 1 (the unit): the quotes each candidate for restoring the room rests on, for reading under the rule
logged first. For each element: its cited codes and 8 quotes drawn from its fourth-order theme (cite.py --tier 4th,
seed 20261015). For each arrow: its support quotes. For each declaration: the quote lines of its section in the field
packages (served there through cite.py). Writes out/_analysis/c5c8_unit_quotes.txt; prints its size.

    python3 out/_analysis/c5c8_unit_quotes.py
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ELEMENTS = ["P01", "P03", "P04", "P05", "C02"]
ARROWS = ["A01", "A05", "A08", "A17"]
DECL = {"T4-014": "05-D04-Order-without-law.md", "T4-018": "05-D04-Order-without-law.md",
        "T4-028": "08-D07-Imprinting.md"}
N, SEED = 8, 20261015


def cite(args):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py")] + args + ["--json"],
                       capture_output=True, text=True, cwd=ROOT)
    try:
        return json.loads(p.stdout).get("quotes") or []
    except ValueError:
        return []


def line(q):
    return '  [%s/%s] h%.2f %s: "%s"' % (q["sub"], q["code_id"], q["hour"], q.get("author") or "?",
                                        q["text"].replace("\n", " ").strip())


def jl(p):
    return {r["id"]: r for r in (json.loads(l) for l in open(os.path.join(OUT, p), encoding="utf-8") if l.strip())}


L = []
el, ar = jl("model/elements.jsonl"), jl("model/arrows.jsonl")
for i in ELEMENTS:
    e = el[i]
    L.append("== %s: %s\n cited:" % (i, e["statement"]))
    for c in e["evidence"]["codes"]:
        sub, code = c.split(":")
        L += [line(q) for q in cite(["--room", sub, "--code", code])]
    for t in e["tier"][:1]:
        L.append(" drawn from %s:" % t)
        L += [line(q) for q in cite(["--tier", "4th", "--id", t, "--n", str(N), "--seed", str(SEED)])]
for i in ARROWS:
    a = ar[i]
    L.append("== %s (%s to %s): %s\n support:" % (i, a["from"], a["to"], a["mechanism"]))
    for s in a.get("support") or []:
        L += [line(q) for q in cite(["--room", s["sub"], "--code", s["code"]])]
for d, f in DECL.items():
    t = open(os.path.join(OUT, "field-packages-C5", f), encoding="utf-8").read()
    i = t.index("### %s " % d)
    j = t.find("\n### ", i + 5)
    sec = t[i:j if j > 0 else len(t)]
    L.append("== %s (field package section, quote lines)" % d)
    L += [s for s in sec.splitlines() if s.startswith("- [")]
txt = "\n".join(L) + "\n"
open(os.path.join(OUT, "_analysis", "c5c8_unit_quotes.txt"), "w", encoding="utf-8").write(txt)
print("written c5c8_unit_quotes.txt: %d lines, %d bytes" % (len(L), len(txt.encode("utf-8"))))
