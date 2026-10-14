#!/usr/bin/env python3
"""C2 section 4, pass 3 (C2a-03): add pass 3's findings, elements, arrow and bound to the typed model, one move at a
time. Every number comes from c2_arrow_evidence-p3a.txt, c2_vetting_concepts-p3.txt, c2_first_concepts-*-p3.txt and
c2_empty_brief-p3.json.

1. findings.jsonl: F-010 to F-012 appended first, so every finding an element cites exists before the element.
2. Elements P20 (standing), K04 and P19 (candidates) appended to model/elements.jsonl with a history line each (move
   developing or dropping working hypotheses); logged and snapped. P17 is unchanged: the declared split stands only if
   P19 earns an arrow, and it earned none.
3. Arrow A20 of c2_arrows_p3.json: quotes through cite.py, transitions checked against the store, appended to
   model/arrows.jsonl with a history line (move sequencing); logged and snapped.
4. A10's bound and counterexample response gain the two pass 2 story rooms (guatemala, MiamiHurricanes):
   model/arrows.jsonl rewritten in place, a history line carrying the old line as was (move relating or contrasting);
   logged and snapped.
5. The hypotheses dropped at pass 3 logged once (move developing or dropping working hypotheses) and snapped.
Refuses if any pass 3 id is already present.

    python3 out/_analysis/c2_build_model_p3.py [--write]
"""
import datetime, glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
MOD = os.path.join(OUT, "model")
write = "--write" in sys.argv


def jl(p):
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


leg = open(os.path.join(ROOT, ".leg")).read().strip()
els_p3 = dict((e["id"], e) for e in json.load(open(os.path.join(OUT, "_analysis", "c2_elements_p3.json"), encoding="utf-8"))["elements"])
arrs = json.load(open(os.path.join(OUT, "_analysis", "c2_arrows_p3.json"), encoding="utf-8"))
empty = set(json.load(open(os.path.join(OUT, "_analysis", "c2_empty_brief-p3.json"), encoding="utf-8"))["empty"])
have_e = set(r["id"] for r in jl(os.path.join(MOD, "elements.jsonl")))
have_a = set(r["id"] for r in jl(os.path.join(MOD, "arrows.jsonl")))
have_f = [r for r in jl(os.path.join(OUT, "findings.jsonl"))]
if have_e & {"P19", "P20", "K04"} or have_a & set(a["id"] for a in arrs["arrows"]) or any(r["id"] == "F-010" for r in have_f):
    sys.exit("a pass 3 id is already present; this builder writes pass 3 once")
hosts = ["PlaceNL", "ainbowroad", "greenlattice", "orderofthebluecorner", "placehearts", "thebluecorner"]
if not all(h in empty for h in hosts) or "yugioh" in empty:
    sys.exit("the host rooms' empty-brief claim does not hold against c2_empty_brief-p3.json")
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--grep", ".", "--json", "--limit",
                    "10000000"], cwd=ROOT, capture_output=True, text=True)
codes = dict(((c["sub"], c["code_id"]), c) for c in (json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")))

base = {"stage": "C2", "leg": leg, "refuted_by": []}
FINDINGS = [
    dict(base, id="F-010", tier="element", warrant="inferred", status="standing",
         statement="Calls to the canvas bring the host sub's line around canvas talk: in 132 of 155 rooms carrying both, the "
                   "first call comes before the first megathread, removal by rule, changed rule, canvas sub, objection to the "
                   "flood or dismissal of the canvas (0.852 against a null mean of 0.538, p95 0.594); early side 48 of 57, "
                   "late side 2 of 2.",
         evidence=["out/_analysis/c2_arrow_evidence-p3a.txt", "out/_analysis/c2_first_concepts-P01-P20-fails-p3.txt",
                   "nintendo:c0121", "rocketleague:c0722", "darksouls:c0150"],
         bound="Partly constitutive: a removal or an objection needs canvas posts. 23 rooms draw the line first: rules remove "
               "the first call as it is posted (9), a canvas sub or megathread is set up before the host carries a call (7), "
               "members dismiss the canvas or object to other rooms' canvas posts before the room calls (7)."),
    dict(base, id="F-011", tier="element", warrant="inferred", status="standing",
         statement="Membership carried in does not come before the attack more than chance: in 86 of 145 rooms carrying "
                   "both, the first concept of the body carried in (a nation's flag and history, a colour, the sub's "
                   "quarrel, lore, jokes or ideology; 22 third-order themes) comes before the first attack (0.593 against a "
                   "null mean of 0.580, p95 0.634).",
         evidence=["out/_analysis/c2_arrow_evidence-p3a.txt", "out/_analysis/c2_arrow_evidence-p2a.txt"],
         bound="The quarrel theme alone failed at pass 2 (2 of 9 rooms). The story rooms show membership framing a fight "
               "after it (a fight told as national history); that order was not tested."),
    dict(base, id="F-012", tier="element", warrant="inferred", status="standing",
         statement="Hosting follows neither exchange, coalition nor upkeep: help between rooms comes first in 11 of 29 rooms "
                   "carrying both (0.379, p95 0.552), a coalition in 5 of 17 (0.294, below the null mean of 0.451), upkeep "
                   "in 33 of 52 (0.635, p95 0.654). Where hosts give a ground for a ruling on a request to build, it is "
                   "space or design in 12 of 23 concepts, fit with the body in 6 and ties in 5. The six rooms whose own "
                   "rulings are cited all have an empty pre-event brief; the seventh room with a cited ruling (yugioh) "
                   "carries a host's ruling on itself.",
         evidence=["out/_analysis/c2_arrow_evidence-p3a.txt", "out/_analysis/c2_vetting_concepts-p3.txt",
                   "out/_analysis/c2_empty_brief-p3.json", "greenlattice:c0292", "orderofthebluecorner:c0047",
                   "yugioh:c0100"],
         bound="Membership then hosting beat the null (21 of 28 rooms, 0.750 against p95 0.714, thin) but is not an arrow: "
               "the declared mechanism (guests come to the body's mark) shows in 5 of the 21 rooms, and 16 show the "
               "reverse role, a room asking a host for space after laying its own mark "
               "(c2_first_concepts-K04-P19-p3.txt). The ruling reading covers only the concepts cited under vetting "
               "others' requests (61 in 7 rooms); national hosts' rulings coded under other themes are not in it."),
]
NEW_EL = {"P20": ("standing", ["F-010"], ["nintendo:c0121", "rocketleague:c0722", "darksouls:c0150"]),
          "K04": ("candidate", ["F-011"], ["spain:c0001", "orderofthebluecorner:c0001"]),
          "P19": ("candidate", ["F-012"], ["orderofthebluecorner:c0047", "greenlattice:c0292", "malta:c0009"])}
BOUNDS = {
    "A10": (" At pass 2 the story rooms add two more: in a late room the judgment of too few hands can be written after "
            "the move (guatemala, h79.1), and a room inside a coalition can move by the coalition's plan with no doubt of "
            "its own (MiamiHurricanes).",
            " Pass 3: guatemala and MiamiHurricanes, read at pass 2, are one late room and one room moved by a coalition. "
            "Alternatives considered: withdrawing the arrow, or a second element for a planned move. Response: two scope "
            "conditions; A10 stays thin.")}
DROPPED = ("Hypotheses dropped at pass 3 (move developing or dropping working hypotheses), each tested under the declared "
           "statement and null: membership then attack (K04 to P09, 0.593 against p95 0.634; finding F-011); membership "
           "then hosting (K04 to P19, 0.750 against p95 0.714, thin) not admitted, because its declared mechanism shows in "
           "5 of 21 holding rooms and the reading of the hosts' rulings finds fit with the body in 6 of 23 grounded "
           "concepts (F-012); exchange then hosting (P16 to P19, 0.379 against 0.552); coalition then hosting (P17 "
           "narrowed to P19, 0.294, below the null mean); upkeep then hosting (P05 to P19, 0.635 against 0.654). The split "
           "of P17 into coalitions and hosting is not taken (P19 earned no arrow); P19 and K04 enter as candidates. "
           "Upkeep then coalition on the narrowed element held (0.719 against p95 0.686), consistent with A19; A19 is "
           "unchanged.")


def stamp(prompt):
    reads = jl(os.path.join(OUT, "_mem_reads-C2.jsonl"))
    rooms = set()
    for r in reads:
        if r.get("verb") in ("room", "forest", "when", "after") and r.get("args"):
            rooms.add(str(r["args"][0]).split("/")[0])
    return {"leg": leg, "rooms_read": sorted(rooms), "n_rooms_read": len(rooms), "reads_so_far": len(reads),
            "tokens_read": "not recorded in the read log", "prompted_by": prompt}


def snap(move):
    n = 1 + max([int(m.group(1)) for m in (re.search(r"C2-move-[a-z]+-(\d+)\.sha256$", q)
                                            for q in glob.glob(os.path.join(OUT, "_snap", "C2-move-*.sha256"))) if m] or [0])
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "snap.py"), "C2", "move-%s-%d" % (move, n)],
                       cwd=ROOT, capture_output=True, text=True)
    print((r.stdout or r.stderr).strip())
    if r.returncode:
        sys.exit("snap failed")


def log(msg):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "log", msg, "--kind", "move"],
                       cwd=ROOT, capture_output=True, text=True)
    print((r.stdout or "").strip())
    if r.returncode:
        sys.exit("mem.py log failed: %s" % r.stderr[-300:])


def quote(sub, code):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py"), "--room", sub, "--code", code],
                       cwd=ROOT, capture_output=True, text=True)
    for line in r.stdout.splitlines():
        m = re.match(r'^"(.*)"  \[%s/%s\]' % (re.escape(sub), re.escape(code)), line)
        if m:
            return m.group(1)
    sys.exit("cite.py gave no quote for %s:%s" % (sub, code))


def transition(sub, pair):
    a, b = codes.get((sub, pair[0])), codes.get((sub, pair[1]))
    if not a or not b:
        sys.exit("transition %s %s: a code is not in the store" % (sub, pair))
    if a.get("thread_id") != b.get("thread_id") or not (b["hour"] > a["hour"]):
        sys.exit("transition %s %s: not one thread in order" % (sub, pair))
    return {"sub": sub, "thread": a["thread_id"], "items": [a["item_id"], b["item_id"]], "codes": list(pair),
            "hours": [a["hour"], b["hour"]], "interval_min": int(round((b["hour"] - a["hour"]) * 60))}


# checks before anything is written
for r in FINDINGS:
    for ev in r["evidence"]:
        if ev.startswith("out/") and not os.path.exists(os.path.join(ROOT, ev)):
            sys.exit("finding %s cites %s, which does not exist" % (r["id"], ev))
        if ":" in ev and not ev.startswith("out/") and tuple(ev.split(":")) not in codes:
            sys.exit("finding %s cites %s, not in the store" % (r["id"], ev))
erows = []
for eid, (status, fins, cs) in NEW_EL.items():
    e = els_p3[eid]
    for c in cs:
        s, k = c.split(":")
        if (s, k) not in codes:
            sys.exit("element %s cites %s, not in the store" % (eid, c))
    erows.append({"id": eid, "kind": e["kind"], "statement": e["statement"], "tier": e["tier"], "dimension": e["dimension"],
                  "range": e["range"], "evidence": {"findings": fins, "codes": cs}, "since": "C2-pass-3", "leg": leg,
                  "status": status})
for a in arrs["arrows"]:
    for t in a["support_transition"]:
        transition(t["sub"], t["codes"])
    for s in a["support"]:
        if (s["sub"], s["code"]) not in codes:
            sys.exit("arrow %s cites %s:%s, not in the store" % (a["id"], s["sub"], s["code"]))
    for e in (a["from"], a["to"]):
        if e not in have_e and e not in NEW_EL:
            sys.exit("arrow %s names %s, not an element" % (a["id"], e))
if not all(k in have_a for k in BOUNDS):
    sys.exit("a bounded arrow is not in arrows.jsonl")
print("checked: %d elements, %d arrows, %d findings, %d bounds" % (len(erows), len(arrs["arrows"]), len(FINDINGS), len(BOUNDS)))
if not write:
    sys.exit(0)

with open(os.path.join(OUT, "findings.jsonl"), "a", encoding="utf-8") as f:
    for r in FINDINGS:
        f.write(json.dumps(dict(r, t=now()), ensure_ascii=False) + "\n")
print("findings appended: %s" % ", ".join(r["id"] for r in FINDINGS))

with open(os.path.join(MOD, "elements.jsonl"), "a", encoding="utf-8") as f:
    for r in erows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
st = stamp({"room": "the pass 2 story rooms with residues", "theme": "Boundary work, Flagging the nation, Neo-tribes, Frame bridging, Meta-organization"})
with open(os.path.join(MOD, "history.jsonl"), "a", encoding="utf-8") as f:
    for r in erows:
        f.write(json.dumps({"t": now(), "stage": "C2", "leg": leg, "id": r["id"], "event": "entered",
                            "move": "developing or dropping working hypotheses",
                            "why": "pass 3 (%s): %s" % (r["status"], r["statement"][:140]), "stamp": st},
                           ensure_ascii=False) + "\n")
log("Model, pass 3 (section 4): elements entered model/elements.jsonl (move: developing or dropping working hypotheses), "
    "from the pass 2 story residues: P20 the host's line around canvas talk (standing; Boundary work; finding F-010), K04 "
    "membership carried in (candidate; Flagging the nation, Neo-tribes, Frame bridging; F-011: not before the attack), P19 "
    "hosting (candidate; four members of Meta-organization; F-012: it follows neither exchange, coalition nor upkeep). P17 "
    "unchanged: the declared split stands only if P19 earns an arrow. Findings first: F-010, F-011, F-012.")
snap("hypotheses")

for a in arrs["arrows"]:
    sup = [{"sub": s["sub"], "code": s["code"], "quote": quote(s["sub"], s["code"])} for s in a["support"]]
    tr = [transition(t["sub"], t["codes"]) for t in a["support_transition"]]
    line = {"id": a["id"], "from": a["from"], "to": a["to"], "kind": a["kind"], "grounding": a["grounding"],
            "grounding_note": a["grounding_note"], "connection": a["connection"], "counts": a["counts"],
            "sampled_against": [{"sub": s, "why_chosen": arrs["sample_rule"], "found": f, "note": n} for s, f, n in a["sampled"]],
            "strength": a["strength"], "subs": a["subs"], "mechanism": a["mechanism"],
            "mechanism_fails_if": a["mechanism_fails_if"], "mechanism_failure_present": a["mechanism_failure_present"],
            "negative_check": a["negative_check"], "base_rate_beaten": a["base_rate_beaten"],
            "early_late": a["early_late"], "bound": a["bound"], "counterexample_response": a["counterexample_response"],
            "in_model": True, "support": sup, "support_transition": tr, "gloss": a["gloss"],
            "since": "C2-pass-3", "leg": leg, "status": "standing"}
    with open(os.path.join(MOD, "arrows.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    with open(os.path.join(MOD, "history.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps({"t": now(), "stage": "C2", "leg": leg, "id": a["id"], "event": "added", "move": "sequencing",
                            "why": "%s -> %s: %s" % (a["from"], a["to"], a["mechanism"]),
                            "stamp": stamp({"room": ", ".join(a["subs"]), "theme": "%s and %s" % (a["from"], a["to"])})},
                           ensure_ascii=False) + "\n")
    c = a["counts"]
    log("Arrow added (section 4, pass 3), move sequencing: %s %s -> %s, %s, strength %s. Connection: %s. Holds in %s of %s "
        "rooms (%.3f) against a null mean of %.3f (p95 %.3f); early %s of %s, late %s of %s. Mechanism: %s Fails if: %s "
        "Sampled against: %s. Bound: %s" % (
            a["id"], a["from"], a["to"], a["kind"], a["strength"], a["connection"], c["holds"], c["both"], c["share"],
            c["null_mean"], c["null_p95"], a["early_late"]["early"], a["early_late"]["early_n"], a["early_late"]["late"],
            a["early_late"]["late_n"], a["mechanism"], a["mechanism_fails_if"],
            "; ".join("%s %s (%s)" % (s, f, n) for s, f, n in a["sampled"]), a["bound"]))
    snap("sequencing")

rows = jl(os.path.join(MOD, "arrows.jsonl"))
was = {}
for r in rows:
    if r["id"] in BOUNDS:
        was[r["id"]] = json.loads(json.dumps(r))
        r["bound"] = (r.get("bound") or "").rstrip() + BOUNDS[r["id"]][0]
        r["counterexample_response"] = (r.get("counterexample_response") or "").rstrip() + BOUNDS[r["id"]][1]
with open(os.path.join(MOD, "arrows.jsonl"), "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
for aid, (add, resp) in BOUNDS.items():
    with open(os.path.join(MOD, "history.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps({"t": now(), "stage": "C2", "leg": leg, "id": aid, "event": "bounded",
                            "move": "relating or contrasting", "why": "bound added from the pass 2 story rooms:%s" % add,
                            "was": was[aid], "stamp": stamp({"room": "guatemala, MiamiHurricanes", "theme": aid})},
                           ensure_ascii=False) + "\n")
    log("Arrow bounded (section 4, pass 3), move relating or contrasting: %s.%s Counterexample response:%s The old line is "
        "kept as was in model/history.jsonl." % (aid, add, resp))
    snap("contrasting")
log(DROPPED)
snap("dropping")
print("arrows now: %d; elements now: %d" % (len(jl(os.path.join(MOD, "arrows.jsonl"))), len(jl(os.path.join(MOD, "elements.jsonl")))))
