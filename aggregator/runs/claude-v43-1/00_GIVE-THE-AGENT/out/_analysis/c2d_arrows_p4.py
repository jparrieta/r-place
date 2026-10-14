#!/usr/bin/env python3
"""C2d-01, pass 4: write into model/arrows.jsonl what pass 4 found, every number parsed from the evidence files, each
arrow changed carrying one model/history.jsonl line with the old line as `was` (move relating or contrasting).

  audit            every support transition gets `audit`: pass, or the checks it fails (c2d_instance_audit-p4.txt for
                   (i), (ii), (iii), (vi); the readings of (iv) and (v) in READ below). A12's check (iii) on its second
                   line is void: P15 is a form-pass element with no cited theme.
  clause_holds     every counted order arrow: rooms where no TO comes after the first FROM (c2_arrow_evidence-p4d.txt,
                   the second statement), the failure clause counted (the reviewer's error 9).
  without_joining  A01, A02, A15, A20: the order count with P01 stripped of joining lines (c2_arrow_evidence-p4c.txt).
  A19              recounted on the narrowed coalition element (c2_arrow_evidence-p4a.txt): counts, sides, sampled rooms.
  A11              recounted on the widened P02 (p4a).
  A20              the host's line by actor before hour 73, and whole before hour 73 (c2_arrow_evidence-p4b.txt).
  A10              its one transition fails check (i) (paranatural moved before its doubt); support gains the quotes
                   of a holding room (fivenightsatfreddys c0623 at h33.55, c0341 at h33.79, one thread, not a reply).

    python3 out/_analysis/c2d_arrows_p4.py [--write]
"""
import datetime, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
AP = os.path.join(OUT, "model", "arrows.jsonl")
HP = os.path.join(OUT, "model", "history.jsonl")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
READ = {  # checks (iv) and (v), read whole (c2d_instance_audit-p4.txt passages)
    ("A01", "latin"): "fails (iv): the first line, 'Consider me conscripted!', joins; it does not call",
    ("A07", "touhou"): "fails (v): the second line, 'The bomb is already done tho. lol', corrects the first; it does not celebrate",
    ("A08", "titanfall"): "fails (iv): the first line posts the final image, a record, not a celebration",
}


def blocks(name):
    """{(from, to): {...}} from an evidence file: counts, sides, sampled rooms."""
    out, cur = {}, None
    for l in open(os.path.join(AN, name), encoding="utf-8"):
        m = re.match(r"== (\S+) -> (\S+), statement", l)
        if m:
            cur = (m.group(1), m.group(2))
            out[cur] = {"sampled": []}
            continue
        if cur is None:
            continue
        m = re.search(r"both (\d+); holds in (\d+) \(([\d.]+)\); null mean ([\d.]+), p95 ([\d.]+); base rate beaten: (\w+)", l)
        if m:
            out[cur].update({"both": int(m.group(1)), "holds": int(m.group(2)), "share": float(m.group(3)),
                             "null_mean": float(m.group(4)), "null_p95": float(m.group(5)), "beaten": m.group(6) == "True"})
        m = re.search(r"early side: holds (\d+) of (\d+); late side: holds (\d+) of (\d+)", l)
        if m:
            out[cur]["early_late"] = {"early": int(m.group(1)), "early_n": int(m.group(2)), "late": int(m.group(3)),
                                      "late_n": int(m.group(4))}
        m = re.search(r"sampled (\S+): first \S+ h([\d.]+), first \S+ h([\d.]+): (holds|fails)", l)
        if m:
            out[cur]["sampled"].append({"sub": m.group(1), "first_from": float(m.group(2)), "first_to": float(m.group(3)),
                                        "found": m.group(4)})
    return out


p4a, p4b, p4c, p4d = (blocks("c2_arrow_evidence-p4%s.txt" % x) for x in "abcd")
audit = {}
cur = None
for l in open(os.path.join(AN, "c2d_instance_audit-p4.txt"), encoding="utf-8"):
    m = re.match(r"== (A\d+) \S+ (\S+) (c\d+) -> (c\d+) \(\-?\d+ min\): (.*)$", l.rstrip("\n"))
    if m:
        res = [x for x in re.split(r"; (?=(?:i|ii|iii|vi) )", m.group(5)) if "FAIL" in x]
        if m.group(1) == "A12":
            res = [x for x in res if "under none" not in x and "FP-01" not in x]
            res = [x for x in res if not (x.startswith("iii FAIL") and "T3-002" in x.split(";")[0])]
        audit[(m.group(1), m.group(2), m.group(3), m.group(4))] = res
rows = [json.loads(l) for l in open(AP, encoding="utf-8") if l.strip()]
A = dict((r["id"], r) for r in rows)
was = dict((k, json.loads(json.dumps(v))) for k, v in A.items())
changed = {}
for a in rows:
    for t in a.get("support_transition") or []:
        key = (a["id"], t["sub"], t["codes"][0], t["codes"][1])
        fails = list(audit.get(key, []))
        if (a["id"], t["sub"]) in READ:
            fails.append(READ[(a["id"], t["sub"])])
        t["audit"] = "pass" if not fails else "fails: " + "; ".join(fails)
        changed.setdefault(a["id"], []).append("audit")
    k = (a["from"], a["to"])
    if a.get("kind") == "order" and k in p4d:
        b = p4d[k]
        a["clause_holds"] = {"both": b["both"], "rooms": b["both"] - b["holds"],
                             "statement": "no TO concept after the first FROM concept (c2_arrow_evidence-p4d.txt)"}
        changed[a["id"]].append("clause_holds") if a["id"] in changed else changed.setdefault(a["id"], ["clause_holds"])
    if a["id"] in ("A01", "A02", "A15", "A20") and k in p4c:
        b = p4c[k]
        a["without_joining"] = dict((x, b[x]) for x in ("both", "holds", "share", "null_mean", "null_p95", "beaten"))
        a["without_joining"]["note"] = "P01 without the concepts c2d_enrol_drop.txt reads as joining (an over-reading)"
        changed.setdefault(a["id"], []).append("without_joining")
b = p4a[("P05", "P17")]
A["A19"]["counts"] = dict((x, b[x]) for x in ("both", "holds", "share", "null_mean", "null_p95"))
A["A19"]["early_late"] = b["early_late"]
A["A19"]["sampled_against"] = [{"sub": s["sub"], "why_chosen": "pass 4, coalition element narrowed: rooms carrying both, drawn by "
                                "random.Random(20261014) in c2_arrow_evidence.py; holds when the connection statement holds",
                                "found": s["found"]} for s in b["sampled"]] + [dict(x, why_chosen="pass 2 draw, kept: " + x["why_chosen"])
                                                                               for x in was["A19"]["sampled_against"]]
A["A19"]["bound"] = ("Late side: no late room of 4 holds; late rooms enter the canvas through other rooms (bretagne, "
                     "MiamiHurricanes, yuyuyu). Thin: 0.719 against a p95 of 0.678 on the coalition element without "
                     "hosting (pass 4). Its pass 2 lead instance (naruto) sits in a room that joined a coalition before "
                     "any upkeep, and its yugioh transition ends on a hosting ruling; criticalrole's transition passes.")
changed.setdefault("A19", []).append("recounted on the narrowed coalition element")
b = p4a[("P02", "P04")]
A["A11"]["counts"] = dict((x, b[x]) for x in ("both", "holds", "share", "null_mean", "null_p95"))
A["A11"]["early_late"] = b["early_late"]
changed.setdefault("A11", []).append("recounted on the widened P02")
A["A20"]["before_h73"] = dict((lab, dict((x, p4b[("P01", to)][x]) for x in ("both", "holds", "share", "null_mean", "null_p95", "beaten")))
                              for lab, to in (("rulings", "P20r"), ("objections", "P20o"), ("whole", "P20")))
A["A20"]["before_h73"]["decision"] = ("both actors beat the null while the canvas runs, so by the rule written first A20 "
                                      "stands on the whole host's line, with both counts printed")
changed.setdefault("A20", []).append("the host's line by actor before hour 73")
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--sub", "fivenightsatfreddys", "--json",
                    "--limit", "100000"], cwd=ROOT, capture_output=True, text=True)
fc = dict((c["code_id"], c) for c in (json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")))
A["A10"]["support"] = A["A10"]["support"] + [{"sub": "fivenightsatfreddys", "code": k, "quote": " ".join(str(fc[k]["text"]).split())}
                                             for k in ("c0623", "c0341")]
A["A10"]["instance_note"] = ("Pass 4 instance audit: the one transition (paranatural c0020 -> c0021) fails check (i): "
                             "paranatural moved at h38.15, before its doubt at h54.27. The support now leads with a holding "
                             "room's words, fivenightsatfreddys: 'Everyone has given up... Osu is taking over.' (c0623, "
                             "h33.55) and, 14 minutes later in the same thread but not as a reply, the proposal to abandon "
                             "the defence and focus on moving (c0341, h33.79). No transition in a holding room passes all six checks.")
changed["A10"].append("support from a holding room")
fail_n = sum(1 for a in rows for t in (a.get("support_transition") or []) if t["audit"] != "pass")
tot = sum(len(a.get("support_transition") or []) for a in rows)
print("transitions %d; failing %d" % (tot, fail_n))
print("\n".join("%s %s %s -> %s: %s" % (a["id"], t["sub"], t["codes"][0], t["codes"][1], t["audit"])
                for a in rows for t in (a.get("support_transition") or []) if t["audit"] != "pass"))
print("A19 %s; A11 %s; A20 %s" % (A["A19"]["counts"], A["A11"]["counts"], json.dumps(A["A20"]["before_h73"])[:400]))
if "--write" in sys.argv:
    with open(AP, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(HP, "a", encoding="utf-8") as f:
        for k in sorted(changed):
            f.write(json.dumps({"t": T, "stage": "C2", "leg": LEG, "id": k, "event": "pass 4: " + ", ".join(sorted(set(changed[k]))),
                                "move": "relating or contrasting", "why": "pass 4 declarations 3 to 7 (notes-C2.md)",
                                "was": was[k]}, ensure_ascii=False) + "\n")
    print("arrows.jsonl rewritten (%d lines); %d history lines appended" % (len(rows), len(changed)))
