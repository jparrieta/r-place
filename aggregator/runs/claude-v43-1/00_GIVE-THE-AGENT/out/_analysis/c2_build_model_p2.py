#!/usr/bin/env python3
"""C2 section 4, pass 2 (C2a-02): add pass 2's findings, elements, arrows and bounds to the typed model, one move at a
time. Every number comes from c2_arrow_evidence-p2a/p2b.txt, c2_relocation_window-p2.txt and c2_play_frame-p2b.txt.

1. findings.jsonl: F-002 superseded (bounded, the relocation window test); F-007 to F-009 appended. Written first, so
   every finding an element cites exists before the element is written.
2. Elements P16, P17, P18 (standing) and K03 (candidate: its one test had 9 rooms and failed) appended to
   model/elements.jsonl with a history line each (move: developing or dropping working hypotheses); logged and snapped.
3. Each arrow of c2_arrows_p2.json: quotes through cite.py, transitions checked against the store, appended to
   model/arrows.jsonl with a history line (move sequencing); logged and snapped.
4. Bounds added from the pass 1 story rooms to A04, A06 and A07: model/arrows.jsonl rewritten in place, a history line
   each carrying the old line as was (move relating or contrasting); logged and snapped.
5. The hypotheses dropped at pass 2 logged once (move developing or dropping working hypotheses) and snapped.
Refuses if any pass 2 id is already present.

    python3 out/_analysis/c2_build_model_p2.py [--write]
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
els_p2 = dict((e["id"], e) for e in json.load(open(os.path.join(OUT, "_analysis", "c2_elements_p2.json"), encoding="utf-8"))["elements"])
arrs = json.load(open(os.path.join(OUT, "_analysis", "c2_arrows_p2.json"), encoding="utf-8"))
have_e = set(r["id"] for r in jl(os.path.join(MOD, "elements.jsonl")))
have_a = set(r["id"] for r in jl(os.path.join(MOD, "arrows.jsonl")))
have_f = [r for r in jl(os.path.join(OUT, "findings.jsonl"))]
if have_e & {"P16", "P17", "P18", "K03"} or have_a & set(a["id"] for a in arrs["arrows"]) or any(r["id"] == "F-007" for r in have_f):
    sys.exit("a pass 2 id is already present; this builder writes pass 2 once")
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--grep", ".", "--json", "--limit",
                    "10000000"], cwd=ROOT, capture_output=True, text=True)
codes = dict(((c["sub"], c["code_id"]), c) for c in (json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")))

base = {"stage": "C2", "leg": leg, "refuted_by": []}
FINDINGS = [
    dict(base, id="F-002", supersedes="F-002@C2a-01", tier="element", warrant="inferred", status="bounded",
         statement="A move lowers a room's calling and building from the crisis before it, but not below other rooms: a call "
                   "falls in the six hours after the first move in 29 of 74 rooms (0.392), against 37 of 74 in the six hours "
                   "before (0.500) and 0.290 for other rooms at the same hours; a build report in 19 of 60 (0.317), against "
                   "0.417 before and 0.309 for other rooms.",
         why="Pass 1's statement (calls after a move rarer than a shuffle predicts, against a null of 0.962) set a bar raised "
             "by rooms dense in calls; four of the twenty pass 1 story rooms called again after a loss; the window test "
             "declared at pass 2 replaces it (c2_relocation_window-p2.txt).",
         evidence=["out/_analysis/c2_relocation_window-p2.txt", "out/_questions/relocation-renewed-calls.md"],
         bound="A move is followed by fewer calls than the crisis before it; it does not stop a room from calling."),
    dict(base, id="F-007", tier="element", warrant="inferred", status="standing",
         statement="A room's own call to attack is answered inside the room: in 82 of 104 rooms carrying both, the first "
                   "attack call comes before the first sparing, refusal or apology (0.788 against a null mean of 0.529), and "
                   "in 95 of 172 before the first border talk (0.552 against 0.423).",
         evidence=["out/_analysis/c2_arrow_evidence-p2a.txt", "nyjets:c0087", "leafs:c0240", "czech:c0153"],
         bound="Reining in needs an attack to rein in, so the first share is partly constitutive; on the late side border "
               "talk comes first (0 of 4)."),
    dict(base, id="F-008", tier="element", warrant="inferred", status="standing",
         statement="Short of hands, rooms turn to other rooms: in 171 of 240 rooms carrying both, the first upkeep comes "
                   "before the first help given, asked for or traded with another room (0.713 against a null mean of "
                   "0.596), and in 106 of 157 before the first coalition (0.675 against 0.569).",
         evidence=["out/_analysis/c2_arrow_evidence-p2a.txt", "out/_analysis/c2_arrow_evidence-p2b.txt", "naruto:c0145",
                   "naruto:c0168"],
         bound="Late rooms often enter the canvas through other rooms, with help or a coalition first (A19 holds in 2 of 7 "
               "late rooms)."),
    dict(base, id="F-009", tier="element", warrant="inferred", status="standing",
         statement="The play frame does not delay the canvas work across rooms: 59 frame-filled rooms at held size start "
                   "their canvas work at a median h21.80, against h20.25 for 275 others (one-sided permutation p 0.43, "
                   "2,000 permutations).",
         evidence=["out/_analysis/c2_play_frame-p2b.txt", "out/_analysis/c2_play_frame-p2.txt"],
         bound="A first run that counted only cited frame concepts put 8 rooms in the group and found a 15.5-hour delay; the "
               "rule undercounted the frame and was corrected before the result was used. ultrahardcore and "
               "totallynotrobots started late inside the frame; they are not its rule."),
]
NEW_EL = {"P16": ("standing", ["F-008"], ["naruto:c0145", "dragonquest:c0037", "littlewitchacademia:c0051"]),
          "P17": ("standing", ["F-008"], ["naruto:c0168", "criticalrole:c0058"]),
          "P18": ("standing", [], ["rpi:c0026", "anarcho_capitalism:c0089"]),
          "K03": ("candidate", [], ["purdue:c0255"])}
BOUNDS = {
    "A04": " At pass 2 the story rooms add three more paths where border talk comes first: a work found already placed "
           "(unitedkingdom), a room entering the canvas through another room's offer (yuyuyu), and neighbours present from "
           "the room's first post (sweden, worldoftanks).",
    "A06": " Spare accounts can also serve an attack before any upkeep (canucks).",
    "A07": " Where hour 73 cut the work unfinished, the room marks the attempt instead: 'We almost did it!' (ultrahardcore), "
           "a watermark mourned (totallynotrobots)."}
DROPPED = ("Hypotheses dropped at pass 2 (move developing or dropping working hypotheses), each tested under the declared "
           "statement and null and not grounded: exchange then sparing (P16 to P07, 0.427 against a null mean of 0.494); "
           "border talk then coalition (P08 to P17, 0.632 against a 95th percentile of 0.654); exchange then coalition "
           "(P16 to P17, 0.384 against 0.450); a quarrel carried in, then attack (K03 to P09, 2 of 9 rooms; K03 enters as a "
           "candidate only); attack then building (P09 to P03, 0.385 against 0.469, reversed); the play frame delaying the "
           "canvas work (59 frame-filled rooms, median h21.80 against h20.25, p 0.43; finding F-009).")


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
erows = []
for eid, (status, fins, cs) in NEW_EL.items():
    e = els_p2[eid]
    for c in cs:
        s, k = c.split(":")
        if (s, k) not in codes:
            sys.exit("element %s cites %s, not in the store" % (eid, c))
    erows.append({"id": eid, "kind": e["kind"], "statement": e["statement"], "tier": e["tier"], "dimension": e["dimension"],
                  "range": e["range"], "evidence": {"findings": fins, "codes": cs}, "since": "C2-pass-2", "leg": leg,
                  "status": status})
for a in arrs["arrows"]:
    for t in a["support_transition"]:
        transition(t["sub"], t["codes"])
    for s in a["support"]:
        if (s["sub"], s["code"]) not in codes:
            sys.exit("arrow %s cites %s:%s, not in the store" % (a["id"], s["sub"], s["code"]))
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
st = stamp({"room": "the twenty pass 1 story rooms", "theme": "Reciprocity, Meta-organization, Rivalry, T3-086"})
with open(os.path.join(MOD, "history.jsonl"), "a", encoding="utf-8") as f:
    for r in erows:
        f.write(json.dumps({"t": now(), "stage": "C2", "leg": leg, "id": r["id"], "event": "entered",
                            "move": "developing or dropping working hypotheses",
                            "why": "pass 2 (%s): %s" % (r["status"], r["statement"][:140]), "stamp": st},
                           ensure_ascii=False) + "\n")
log("Model, pass 2 (section 4): elements entered model/elements.jsonl (move: developing or dropping working hypotheses), "
    "from the pass 1 story residues: P16 exchange between rooms (standing; Reciprocity; finding F-008), P17 coalitions and "
    "hosting (standing; Meta-organization; F-008), P18 rivalry talk (standing; Rivalry), K03 a quarrel carried in "
    "(candidate; T3-086; its one test failed on 9 rooms). Findings first: F-002 superseded as bounded (the relocation window "
    "test), F-007 (attack answered inside the room), F-008 (short of hands, rooms turn to other rooms), F-009 (the play "
    "frame does not delay the canvas work).")
snap("hypotheses")

for a in arrs["arrows"]:
    sup = [{"sub": s["sub"], "code": s["code"], "quote": quote(s["sub"], s["code"])} for s in a["support"]]
    tr = [transition(t["sub"], t["codes"]) for t in a["support_transition"]]
    line = {"id": a["id"], "from": a["from"], "to": a["to"], "kind": a["kind"], "grounding": a["grounding"],
            "grounding_note": a["grounding_note"], "connection": a["connection"], "counts": a["counts"],
            "sampled_against": [{"sub": s, "why_chosen": arrs["sample_rule"], "found": f} for s, f in a["sampled"]],
            "strength": a["strength"], "subs": a["subs"], "mechanism": a["mechanism"],
            "mechanism_fails_if": a["mechanism_fails_if"], "mechanism_failure_present": a["mechanism_failure_present"],
            "negative_check": a["negative_check"], "base_rate_beaten": a["base_rate_beaten"],
            "early_late": a["early_late"], "bound": a["bound"], "counterexample_response": a["counterexample_response"],
            "in_model": True, "support": sup, "support_transition": tr, "gloss": a["gloss"],
            "since": "C2-pass-2", "leg": leg, "status": "standing"}
    with open(os.path.join(MOD, "arrows.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    with open(os.path.join(MOD, "history.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps({"t": now(), "stage": "C2", "leg": leg, "id": a["id"], "event": "added", "move": "sequencing",
                            "why": "%s -> %s: %s" % (a["from"], a["to"], a["mechanism"]),
                            "stamp": stamp({"room": ", ".join(a["subs"]), "theme": "%s and %s" % (a["from"], a["to"])})},
                           ensure_ascii=False) + "\n")
    c = a["counts"]
    log("Arrow added (section 4, pass 2), move sequencing: %s %s -> %s, %s, strength %s. Connection: %s. Holds in %s of %s "
        "rooms (%.3f) against a null mean of %.3f (p95 %.3f); early %s of %s, late %s of %s. Mechanism: %s Fails if: %s "
        "Sampled against: %s. Bound: %s" % (
            a["id"], a["from"], a["to"], a["kind"], a["strength"], a["connection"], c["holds"], c["both"], c["share"],
            c["null_mean"], c["null_p95"], a["early_late"]["early"], a["early_late"]["early_n"], a["early_late"]["late"],
            a["early_late"]["late_n"], a["mechanism"], a["mechanism_fails_if"],
            ", ".join("%s %s" % (s, f) for s, f in a["sampled"]), a["bound"]))
    snap("sequencing")

rows = jl(os.path.join(MOD, "arrows.jsonl"))
was = {}
for r in rows:
    if r["id"] in BOUNDS:
        was[r["id"]] = json.loads(json.dumps(r))
        r["bound"] = (r.get("bound") or "").rstrip() + BOUNDS[r["id"]]
with open(os.path.join(MOD, "arrows.jsonl"), "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
for aid, add in BOUNDS.items():
    with open(os.path.join(MOD, "history.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps({"t": now(), "stage": "C2", "leg": leg, "id": aid, "event": "bounded",
                            "move": "relating or contrasting", "why": "bound added from the pass 1 story rooms:%s" % add,
                            "was": was[aid], "stamp": stamp({"room": "pass 1 story rooms", "theme": aid})},
                           ensure_ascii=False) + "\n")
    log("Arrow bounded (section 4, pass 2), move relating or contrasting: %s.%s The old line is kept as was in "
        "model/history.jsonl." % (aid, add))
    snap("contrasting")
log(DROPPED)
snap("dropping")
print("arrows now: %d; elements now: %d" % (len(jl(os.path.join(MOD, "arrows.jsonl"))), len(jl(os.path.join(MOD, "elements.jsonl")))))
