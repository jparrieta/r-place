#!/usr/bin/env python3
"""C2d-01, pass 4 declaration 3: the instance audit. For every arrow in model/arrows.jsonl and every support transition
it carries, the checks run by script:
  (i)   the room holds the arrow's order (first FROM concept before first TO concept, cited concepts, pass 4 elements);
  (ii)  both turns in one thread; the second replies at some depth to the first (its coordinate lies under the first's,
        or the first is the submission); another author; later;
  (iii) the first concept is cited under a FROM theme and the second under a TO theme;
  (vi)  the printed hours and interval match the store; any support quote of those concepts is the store's text.
Checks (iv) and (v), whether the first line's words do the FROM act and the second does the TO act as a new act
answering it, are read: the script prints both passages whole for that reading. Read-only.

    python3 out/_analysis/c2d_instance_audit.py [A19 A20 ...]
"""
import collections, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
want = sys.argv[1:]
arrows = [json.loads(l) for l in open(os.path.join(OUT, "model", "arrows.jsonl"), encoding="utf-8") if l.strip()]
els = dict((e["id"], e) for e in json.load(open(os.path.join(OUT, "_analysis", "c2_elements_p4.json"), encoding="utf-8"))["elements"])
subs = sorted(set(t["sub"] for a in arrows for t in (a.get("support_transition") or []) if not want or a["id"] in want))
codes = {}
for s in subs:
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--sub", s, "--json", "--limit",
                        "100000"], cwd=ROOT, capture_output=True, text=True)
    for l in p.stdout.splitlines():
        if l.startswith("{"):
            c = json.loads(l)
            codes[(c["sub"], c["code_id"])] = c
cited = collections.defaultdict(lambda: collections.defaultdict(set))
for l in open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r["sub"] not in subs:
        continue
    for t, cs in (r.get("support_by_theme") or {}).items():
        for c in cs:
            cited[r["sub"]][c].add(t)


def first(sub, el):
    th = set(els[el]["themes"])
    hs = [codes[(sub, c)]["hour"] for c, ts in cited[sub].items() if ts & th and (sub, c) in codes
          and codes[(sub, c)].get("hour") is not None]
    return min(hs) if hs else None


def under(c1, c2):
    a, b = str(c1.get("coord")), str(c2.get("coord"))
    return a == "0" or b.startswith(a + ".")


tot = collections.Counter()
for a in arrows:
    if want and a["id"] not in want:
        continue
    fr, to = a["from"], a["to"]
    sq = dict(((x["sub"], x["code"]), x["quote"]) for x in (a.get("support") or []))
    for t in a.get("support_transition") or []:
        s, (k1, k2) = t["sub"], t["codes"]
        c1, c2 = codes.get((s, k1)), codes.get((s, k2))
        if not c1 or not c2:
            print("== %s %s %s -> %s: a concept is not in the store" % (a["id"], s, k1, k2))
            tot["missing"] += 1
            continue
        f1, f2 = first(s, fr) if els[fr]["themes"] else None, first(s, to) if els[to]["themes"] else None
        chk = collections.OrderedDict()
        chk["i"] = "n/a" if f1 is None or f2 is None else ("pass" if f1 < f2 else "FAIL (first %s h%s, first %s h%s)" % (fr, f1, to, f2))
        chk["ii"] = "pass" if (c1["thread_id"] == c2["thread_id"] and under(c1, c2) and c1.get("author") != c2.get("author")
                               and c1["hour"] < c2["hour"]) else "FAIL (thread %s/%s, coord %s/%s, author %s/%s)" % (
            c1["thread_id"], c2["thread_id"], c1.get("coord"), c2.get("coord"), c1.get("author"), c2.get("author"))
        th1, th2 = set(els[fr]["themes"]), set(els[to]["themes"])
        ok1 = bool(cited[s].get(k1, set()) & th1) if th1 else None
        ok2 = bool(cited[s].get(k2, set()) & th2) if th2 else None
        chk["iii"] = "pass" if (ok1 is not False and ok2 is not False) else "FAIL (%s cited under %s; %s under %s)" % (
            k1, sorted(cited[s].get(k1, [])) or "none", k2, sorted(cited[s].get(k2, [])) or "none")
        iv = int(round((c2["hour"] - c1["hour"]) * 60))
        qok = all(" ".join(str(codes[(s, k)]["text"]).split()) == q for k in (k1, k2) for q in [sq.get((s, k))] if q)
        chk["vi"] = "pass" if (t.get("hours") in (None, [c1["hour"], c2["hour"]]) and abs(t.get("interval_min", iv) - iv) <= 1
                               and qok) else "FAIL (hours %s, interval %s against %s, quotes %s)" % (
            t.get("hours"), t.get("interval_min"), iv, "match" if qok else "differ")
        bad = [k for k, v in chk.items() if v.startswith("FAIL")]
        tot["transitions"] += 1
        tot["failing"] += bool(bad)
        print("== %s %s->%s %s %s -> %s (%s min): %s" % (a["id"], fr, to, s, k1, k2, iv,
                                                      "; ".join("%s %s" % (k, v) for k, v in chk.items())))
        print("   1 [h%s %s] %s" % (c1["hour"], c1.get("author"), " ".join(str(c1["text"]).split())))
        print("   2 [h%s %s] %s" % (c2["hour"], c2.get("author"), " ".join(str(c2["text"]).split())))
print("\ntransitions %d; failing a scripted check %d; concepts missing %d" % (tot["transitions"], tot["failing"], tot["missing"]))
