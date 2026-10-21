#!/usr/bin/env python3
"""D3a-48: P06's census under G53's census rules (logged before this ran). Reads the six ruling files, the spec files
for each line's class and the six tag files; a line shows P06 when it has a tag row. Prints lines by op and class,
rooms showing P06 with their forms, TURN and AC marks, the TURN share by form, the lines not shown by class, the
particulars, and the ordering lines (E-PAIR, PART). Writes nothing.

  python3 out/_analysis/d3_p06_census.py
"""
import json
from collections import Counter, defaultdict

R = "out/_analysis/d3_rulings/"
OPS = [("instantiate", "P06-inst", "P06-inst-spec.txt", "P06-tags-inst.txt"),
       ("restrict", "P06-restrict", "P06-restrict-spec.txt", "P06-tags-restrict.txt"),
       ("add-condition", "P06-addcond", "P06-addcond-spec.txt", "P06-tags-addcond.txt"),
       ("add-step", "P06-addstep", "P06-addstep-spec.txt", "P06-tags-addstep.txt"),
       ("link", "P06-link", "P06-link-spec.txt", "P06-tags-link.txt"),
       ("absent", "P06-absent", "P06-absent-spec.txt", "P06-tags-absent.txt")]
FORMS = ("TR", "FF", "OM", "BO", "DIS", "Q")


def room(aid):
    return aid.rsplit("-", 1)[0]


lines = {}
for op, base, spec, tags in OPS:
    rul = [json.loads(l) for l in open(R + base + ".jsonl", encoding="utf-8") if l.strip()]
    cls, pair = {}, {}
    for l in open(R + spec, encoding="utf-8"):
        if l.strip():
            p = [x.strip() for x in l.rstrip("\n").split("|")]
            cls[p[0]] = p[1]
            if len(p) == 4:
                pair[p[0]] = p[3]
    tg = {}
    for l in open(R + tags, encoding="utf-8"):
        if l.strip():
            i, t = l.strip().split("|")
            tg[i] = set(t.split(","))
    for r in rul:
        i = r["adaptation"]
        assert i not in lines, i
        c = cls.get(i)
        if c is None:
            assert op == "absent", i
            c = {"accept": "EL", "reject": "REJ", "particular": "P-G6"}[r["decision"]]
        assert i not in tg or op != "absent" or c == "REJ", i
        lines[i] = {"op": op, "class": c, "decision": r["decision"], "kind": r.get("kind"), "tags": tg.get(i),
                    "pair": pair.get(i)}

print("lines: %d; rooms: %d" % (len(lines), len({room(i) for i in lines})))
byop = defaultdict(Counter)
for i, x in lines.items():
    byop[x["op"]][x["class"]] += 1
for op, *_ in OPS:
    print("  %-13s %4d  %s" % (op, sum(byop[op].values()), dict(sorted(byop[op].items()))))
print("decisions:", dict(Counter(x["decision"] for x in lines.values())),
      "kinds:", dict(Counter(str(x["kind"]) for x in lines.values())))

shown = {i: x for i, x in lines.items() if x["tags"]}
rooms = defaultdict(list)
for i, x in lines.items():
    rooms[room(i)].append(x)
srooms = {r: [x for x in xs if x["tags"]] for r, xs in rooms.items()}
srooms = {r: xs for r, xs in srooms.items() if xs}
print("\nlines showing P06: %d of %d; rooms showing P06: %d of %d" % (len(shown), len(lines), len(srooms), len(rooms)))
print("  lines with TURN: %d of %d shown (%.3f)" % (sum("TURN" in x["tags"] for x in shown.values()), len(shown),
      sum("TURN" in x["tags"] for x in shown.values()) / len(shown)))
forms = {r: set().union(*[x["tags"] for x in xs]) for r, xs in srooms.items()}
turn = {r for r, f in forms.items() if "TURN" in f}
aconly = {r for r, xs in srooms.items() if all("AC" in x["tags"] for x in xs)}
qonly = {r for r, f in forms.items() if (f & set(FORMS)) == {"Q"}}
print("  rooms with TURN: %d of %d (%.3f); AC-only rooms: %d; Q-only rooms: %d"
      % (len(turn), len(srooms), len(turn) / len(srooms), len(aconly), len(qonly)))
print("  rooms by form, and the share of them with TURN:")
for f in FORMS:
    rs = {r for r, s in forms.items() if f in s}
    if rs:
        print("    %-4s %3d rooms; TURN in %3d (%.3f)" % (f, len(rs), len(rs & turn), len(rs & turn) / len(rs)))
soft = {r for r, s in forms.items() if (s & set(FORMS)) and (s & set(FORMS)) <= {"BO", "Q", "DIS"}}
print("  rooms whose forms are only BO, Q or DIS: %d; TURN in %d" % (len(soft), len(soft & turn)))
hard = {r for r, s in forms.items() if s & {"TR", "FF", "OM"}}
print("  rooms with TR, FF or OM: %d; TURN in %d (%.3f)" % (len(hard), len(hard & turn), len(hard & turn) / len(hard)))
nform = Counter(len(s & set(FORMS)) for s in forms.values())
print("  rooms by number of forms:", dict(sorted(nform.items())))

print("\nlines not showing P06, by class:", dict(Counter(x["class"] for x in lines.values() if not x["tags"])))
part = [i for i, x in lines.items() if x["decision"] == "particular"]
print("particulars: %d, of which PO (P06 shown): %d" % (len(part), sum(1 for i in part if lines[i]["tags"])))
nos = [r for r in rooms if r not in srooms]
lim = [r for r in nos if all(x["decision"] == "accept" and x["kind"] == "none" for x in rooms[r])]
print("rooms not showing P06: %d; of them, rooms whose lines are all evidence limits: %d" % (len(nos), len(lim)))
print("rooms not showing P06 with a NOT, VIS or EL line other than absent limits: %d"
      % sum(1 for r in nos if any(x["class"] in ("NOT", "VIS", "EL-NOT", "EL-VIS", "S-OTHER") for x in rooms[r])))

print("\nordering lines (E-PAIR with its pair; PART):")
for i, x in sorted(lines.items()):
    if x["class"] in ("E-PAIR", "PART"):
        print("  %-26s %-9s %-6s %s" % (i, x["op"], x["class"], x["pair"] or ""))
