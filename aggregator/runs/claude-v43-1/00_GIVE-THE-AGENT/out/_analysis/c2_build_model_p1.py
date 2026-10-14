#!/usr/bin/env python3
"""C2 section 4, pass 1: write the typed model from c2_elements_p1.json and c2_arrows_p1.json, one move at a time.

1. findings.jsonl is opened with the pass's findings (F-001 on), if it does not exist.
2. The elements are written to model/elements.jsonl with a history line each (move: developing or dropping working
   hypotheses), logged once through `mem.py log --kind move` and snapped (`snap.py C2 move-hypotheses-<n>`).
3. Each arrow, in order: its support quotes are fetched through cite.py (one logged read each); its transitions are
   filled from the store (item, thread, interval) and checked (same thread, the second later); the line is appended
   to model/arrows.jsonl with a history line (move sequencing for an order arrow, relating otherwise); the move is
   logged and snapped (`snap.py C2 move-<move>-<n>`).
model/loops.jsonl is written empty: no loop is grounded at pass 1.
The stamp on each history line is read from the stage's read log (out/_mem_reads-C2.jsonl): the leg, the rooms whose
page or forest was read so far, the reads so far; the record holds no token count, and the stamp says so.
Refuses if model/elements.jsonl or model/arrows.jsonl exists.

    python3 out/_analysis/c2_build_model_p1.py [--write]
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
els = json.load(open(os.path.join(OUT, "_analysis", "c2_elements_p1.json"), encoding="utf-8"))["elements"]
arrs = json.load(open(os.path.join(OUT, "_analysis", "c2_arrows_p1.json"), encoding="utf-8"))
for p in ("elements.jsonl", "arrows.jsonl"):
    if os.path.exists(os.path.join(MOD, p)):
        sys.exit("model/%s exists; this builder writes pass 1 once" % p)
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--grep", ".", "--json", "--limit",
                    "10000000"], cwd=ROOT, capture_output=True, text=True)
codes = dict(((c["sub"], c["code_id"]), c) for c in (json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")))

FINDINGS = [
    {"id": "F-001", "statement": "Most rooms aligned their placers without deciding how they were organized: decided order (a leader, a vote, an oath, a sanction, a division of the work) reaches 48 placement lines in 46 of 705 rooms, and the question who is in charge is asked in 14 rooms.", "warrant": "read",
     "status": "standing", "evidence": {"codes": ["italy:c0145", "fireemblem:c0309"], "files": ["fourth/fourth.md", "form_pass-C1.md"]}},
    {"id": "F-002", "statement": "A room that loses its spot goes back to choosing a spot, not to recruiting: in rooms that relocate, a call or a build report after the first relocation is rarer than a permutation of the same concepts would make it (calls 0.722 of 79 rooms against a null mean of 0.962; builds 0.754 of 65 against 0.939).", "warrant": "inferred",
     "status": "standing", "evidence": {"codes": ["day9:c0023", "day9:c0027"], "files": ["_analysis/c2_arrow_evidence-p1c.txt"]}},
    {"id": "F-003", "statement": "Organizing can stop early because a work is finished and holds: day9's last coordinating turn (h53.3) follows a relocation finished at h53.1, and the room then recounts a kept work.", "warrant": "read",
     "status": "standing", "evidence": {"codes": ["day9:c0031", "day9:c0036"], "files": ["within_case.md"]}},
    {"id": "F-004", "statement": "The close runs in order in most rooms that carry its parts: marking the finished work, then recording what happened, then carrying the work on (0.779 and 0.779 against null means of 0.565 and 0.563).", "warrant": "inferred",
     "status": "standing", "evidence": {"codes": ["lakers:c0226", "uiuc:c0155"], "files": ["_analysis/c2_arrow_evidence-p1b.txt"]}},
    {"id": "F-005", "statement": "Machine hands arrive under strain: in rooms that both keep their work and run scripts or spare accounts, upkeep comes first in 0.788 of 203 rooms against a null mean of 0.603.", "warrant": "inferred",
     "status": "standing", "evidence": {"codes": ["foxes:c0061", "TheFarLeftSide:c0385"], "files": ["_analysis/c2_arrow_evidence-p1c.txt"]}}]
EL_FINDINGS = {"C01": ["F-001"], "P10": ["F-002"], "P11": ["F-004"], "P12": ["F-004"], "P13": ["F-003", "F-004"],
               "P14": ["F-005"], "K02": ["F-002"]}


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


# the elements, checked before anything is written
erows = []
for e in els:
    for c in e["codes"]:
        s, k = c.split(":")
        if (s, k) not in codes:
            sys.exit("element %s cites %s, not in the store" % (e["id"], c))
    erows.append({"id": e["id"], "kind": e["kind"], "statement": e["statement"], "tier": e["tier"],
                  "dimension": e["dimension"], "range": e["range"],
                  "evidence": {"findings": EL_FINDINGS.get(e["id"], []), "codes": e["codes"]},
                  "since": "C2-pass-1", "leg": leg, "status": "standing"})
print("elements checked: %d" % len(erows))
if not write:
    sys.exit(0)
os.makedirs(MOD, exist_ok=True)
if not os.path.exists(os.path.join(OUT, "findings.jsonl")):
    with open(os.path.join(OUT, "findings.jsonl"), "w", encoding="utf-8") as f:
        for r in FINDINGS:
            f.write(json.dumps(dict(r, pass_=1, leg=leg, t=now()), ensure_ascii=False).replace('"pass_"', '"pass"') + "\n")
    print("opened findings.jsonl: %d findings" % len(FINDINGS))
open(os.path.join(MOD, "loops.jsonl"), "w").close()
with open(os.path.join(MOD, "elements.jsonl"), "w", encoding="utf-8") as f:
    for r in erows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
st = stamp({"room": "ubc, ultrahardcore, day9", "theme": "the 28 fourth-order themes and the four things the model owes"})
with open(os.path.join(MOD, "history.jsonl"), "a", encoding="utf-8") as f:
    for r in erows:
        f.write(json.dumps({"t": now(), "stage": "C2", "leg": leg, "id": r["id"], "event": "entered",
                            "move": "developing or dropping working hypotheses",
                            "why": "an element of the pass 1 model: %s" % r["statement"][:120], "stamp": st},
                           ensure_ascii=False) + "\n")
log("Model, pass 1 (section 4): %d elements entered model/elements.jsonl (move: developing or dropping working hypotheses): "
    "%s. Each tied to its tier and dimension; findings.jsonl opened with F-001 to F-005. model/loops.jsonl written empty: no "
    "loop grounded at pass 1." % (len(erows), ", ".join("%s %s" % (r["id"], r["kind"]) for r in erows)))
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
            "since": "C2-pass-1", "leg": leg, "status": "standing"}
    move = "sequencing" if a["kind"] == "order" else "relating"
    with open(os.path.join(MOD, "arrows.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    with open(os.path.join(MOD, "history.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps({"t": now(), "stage": "C2", "leg": leg, "id": a["id"], "event": "added", "move": move,
                            "why": "%s -> %s: %s" % (a["from"], a["to"], a["mechanism"]),
                            "stamp": stamp({"room": ", ".join(a["subs"]), "theme": "%s and %s" % (a["from"], a["to"])})},
                           ensure_ascii=False) + "\n")
    c = a["counts"] or {}
    log("Arrow added (section 4), move %s: %s %s -> %s, %s, strength %s. Connection: %s.%s Mechanism: %s Fails if: %s "
        "Sampled against: %s. Bound: %s" % (
            move, a["id"], a["from"], a["to"], a["kind"], a["strength"], a["connection"],
            (" Holds in %s of %s rooms (%.3f) against a null mean of %.3f (p95 %.3f)." % (
                c["holds"], c["both"], c["share"], c["null_mean"], c["null_p95"])) if c else " Never counted (form pass).",
            a["mechanism"], a["mechanism_fails_if"], ", ".join("%s %s" % (s, f) for s, f in a["sampled"]), a["bound"]))
    snap(move)
print("arrows written: %d" % len(jl(os.path.join(MOD, "arrows.jsonl"))))
