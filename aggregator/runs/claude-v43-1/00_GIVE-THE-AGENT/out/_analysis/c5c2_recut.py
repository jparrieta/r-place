#!/usr/bin/env python3
"""C5c-02: write Stigmergy's recut, decided by three codings under the rule logged before the tally (diary, C5c-02,
kind abductive; c5c2_stigmergy_three.py), and what it touches. Every count is parsed from a file, not typed.

  fourth/fourth.jsonl   T4-006 Collective representation gains T3-041 and T3-060, its prose rewritten (535 rooms,
                        c5c2_room_unions.json); T4-007 Stigmergy keeps T3-038 alone, its prose, changed and gloss
                        rewritten, its one member said in the prose
  tier_history.jsonl    T3-041 and T3-060 (merging, fourth-order home changed), T4-006 (merging, members_changed),
                        T4-007 (splitting, members_changed), each with the old line as `was`
  model/elements.jsonl  P02 and P03 statements, ranges and codes; one model/history.jsonl line each (merging, splitting)
  model/arrows.jsonl    A01, A03, A07, A11 recounted on c2_elements_c5c2.json (c5c2_arrow_evidence.txt; the failure
                        clause from c5c2_arrow_evidence_after.txt; A01 without joining from c5c2_arrow_evidence_nojoin.txt);
                        A01 strong to fair; A07's touhou transition noted as outside P03; one history line each
                        (relating or contrasting)

    python3 out/_analysis/c5c2_recut.py            print what would change
    python3 out/_analysis/c5c2_recut.py --write    write it
"""
import copy, datetime, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
WRITE = "--write" in sys.argv
MOVE = ["T3-041", "T3-060"]


def jl(p):
    return [json.loads(l) for l in open(os.path.join(OUT, p), encoding="utf-8") if l.strip()]


def wjl(p, rows):
    open(os.path.join(OUT, p), "w", encoding="utf-8").write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def ajl(p, rows):
    with open(os.path.join(OUT, p), "a", encoding="utf-8") as f:
        f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


three = json.load(open(os.path.join(AN, "c5c2_stigmergy_three.json"), encoding="utf-8"))
unions = json.load(open(os.path.join(AN, "c5c2_room_unions.json"), encoding="utf-8"))
p38, n38, _ = three["T3-038"]["verdicts"]["M"]
WHY_MOVE = ("three codings of the 72 records drawn at C5a-01 (mine, the C5c-01 fleet reader of the member theme, the field "
            "analyst), each record taking the code two coders gave, under the rule logged before the tally: T3-041 has P "
            "in %d to %d of %d records that are not O, and T3-060 in %d of %d, so each meets the rule (P at least half), and "
            "by the rule written before the read each moves to Collective representation, where proposals of what the mark "
            "shows sit; T3-038 has P in %d of %d and stays" % (
                three["T3-041"]["verdicts"]["M"][0], three["T3-041"]["verdicts"]["P"][0], three["T3-041"]["verdicts"]["M"][1],
                three["T3-060"]["verdicts"]["M"][0], three["T3-060"]["verdicts"]["M"][1], p38, n38))

# ---- fourth.jsonl
fourth = jl("fourth/fourth.jsonl")
f6 = [r for r in fourth if r["id"] == "T4-006"][0]
f7 = [r for r in fourth if r["id"] == "T4-007"][0]
was6, was7 = copy.deepcopy(f6), copy.deepcopy(f7)
assert all(m in f7["members"] for m in MOVE) and not any(m in f6["members"] for m in MOVE)
f6["members"] = f6["members"] + MOVE
old6 = ("They argue its design (281 rooms), propose it (166), build their homeland's flag (96), find their mark already "
        "placed by others (43), draw national emblems (39) and sign the sub's name (35).")
new6 = ("They argue its design (281 rooms), propose it (166), add to it or enlarge it (168), build their homeland's flag "
        "(96), find their mark already placed by others (43), draw national emblems (39), sign the sub's name (35) and add "
        "personal pieces to a shared mark (7): 'We can try to write Knock Knock/Cheer Up/Ooh-Ahh under it!' "
        "[twice/c0057]; 'CAN I PLEASE BUILD \"DONATE BLOOD\"' [TransFlagPlace/c0253].")
assert old6 in f6["prose"] and "483 of 705 rooms" in f6["prose"]
f6["prose"] = f6["prose"].replace(old6, new6).replace("483 of 705 rooms", "%d of 705 rooms" % unions["new"]["T4-006"])
f6["pass"], f6["leg"] = "C5c-02", LEG
f7["members"] = [m for m in f7["members"] if m not in MOVE]
f7["prose"] = (
    "Members build the mark and report its state in the thread (building and reporting the mark, %d rooms): 'Hat is "
    "done, moving onto outline and glasses now.' [physical_removal/c0012]; 'It looks like the gridref (600,456) is "
    "wrong. It should be (600,482).' [starcitizen/c0330]. The record holds the talk, not the placing. Three coders read "
    "24 records drawn from this theme. By the code at least two of them gave, %d of the %d records that bear on the "
    "work report what is placed, done or missing, or say that a member acted on what the canvas showed, and %d propose "
    "or ask what to add. The record does not show whether placers who never wrote followed the canvas. Since C5c-02 the "
    "theme has one member. The name reads that member's records as coordination through the trace; it is not a group "
    "of several themes." % (unions["T3-038"], n38 - p38, n38, p38))
old7c = ("Here members do both. They report the state of the mark to the thread, which is a marker in Heylighen's sense. "
         "They also propose and argue what to add, which both sources set apart (Grassé, pp. 74-75; Heylighen, pp. 9-10).")
assert old7c in f7["changed"]
f7["changed"] = f7["changed"].replace(old7c, (
    "Here members report the state of the mark to the thread, which is a marker in Heylighen's sense. Their proposals "
    "of what to add, which both sources set apart (Grassé, pp. 74-75; Heylighen, pp. 9-10), sit under Collective "
    "representation: three coders read most records of extending the room's work and of adding a personal piece as "
    "such proposals, and both themes moved there at C5c-02."))
f7["gloss"], f7["gloss_from"] = "Hat is done, moving onto outline and glasses now.", "physical_removal/c0012"
f7["pass"], f7["leg"] = "C5c-02", LEG
th = []
for m in MOVE:
    th.append({"t": T, "stage": "C5", "leg": LEG, "tier": "third", "id": m, "move": "merging",
               "event": "fourth-order home changed", "was": {"fourth": "T4-007"}, "now": [{"id": m, "fourth": "T4-006"}],
               "why": WHY_MOVE})
th.append({"t": T, "stage": "C5", "leg": LEG, "tier": "fourth", "id": "T4-006", "move": "merging",
           "event": "members_changed", "was": was6, "now": f6, "why": "gains T3-041 and T3-060: " + WHY_MOVE})
th.append({"t": T, "stage": "C5", "leg": LEG, "tier": "fourth", "id": "T4-007", "move": "splitting",
           "event": "members_changed", "was": was7, "now": f7,
           "why": "loses T3-041 and T3-060 (" + WHY_MOVE + "). Kept with one member: withdrawing it would leave T3-038 in "
                  "no fourth-order theme and P03, on the spine, outside its dimension, while the three coders read most of "
                  "T3-038's bearing records as reports of the work's state, the trace the construct names. A one-member "
                  "theme breaks C2's criterion for a group (it answers no question its member does not answer alone); "
                  "the prose says so. The gloss is replaced: starbound/c0082 sits under celebration and credit, not "
                  "under any member."})
# ---- elements
els = jl("model/elements.jsonl")
e2 = [e for e in els if e["id"] == "P02"][0]
e3 = [e for e in els if e["id"] == "P03"][0]
w2, w3 = copy.deepcopy(e2), copy.deepcopy(e3)
e2["statement"] = ("The room settles what its mark will show of it: a member proposes a picture, the room argues its "
                   "design, makes its land's flag or emblems the mark, signs it or leaves it unsigned, claims a mark others "
                   "made, adds to it or enlarges it, or adds a personal piece to a shared mark.")
e2["range"] = w2["range"] + ", or one member asking to add their own words to a shared flag"
e2["evidence"]["codes"] = w2["evidence"]["codes"] + ["twice:c0057", "TransFlagPlace:c0253"]
e3["statement"] = "Members build the mark and report its state to the thread: what is placed, done or missing, and where."
e3["range"] = "from one report that the logo is half done to reports on each part of a mark over two days"
e3["evidence"]["codes"] = ["physical_removal:c0012", "starcitizen:c0330"]
mh = [{"t": T, "stage": "C5", "leg": LEG, "id": "P02", "event": "statement widened (T4-006 gains T3-041 and T3-060)",
       "move": "merging", "why": WHY_MOVE, "was": w2},
      {"t": T, "stage": "C5", "leg": LEG, "id": "P03", "event": "statement narrowed (T4-007 keeps T3-038 alone)",
       "move": "splitting", "why": WHY_MOVE + "; the evidence codes are now T3-038 records the three coders read alike "
                                             "(starbound:c0082 and day9:c0031 sit under no member of the narrowed theme)",
       "was": w3}]


# ---- arrows
def blocks(name):
    out = {}
    cur = None
    for l in open(os.path.join(AN, name), encoding="utf-8"):
        m = re.match(r"== (\S+) -> (\S+), statement", l)
        if m:
            cur = (m.group(1), m.group(2))
            out[cur] = {}
            continue
        m = re.match(r"rooms carrying \S+ \d+, \S+ \d+, both (\d+); holds in (\d+) \(([\d.]+)\); null mean ([\d.]+), "
                     r"p95 ([\d.]+); base rate beaten: (\w+)", l)
        if m and cur:
            out[cur].update({"both": int(m.group(1)), "holds": int(m.group(2)), "share": float(m.group(3)),
                             "null_mean": float(m.group(4)), "null_p95": float(m.group(5)), "beaten": m.group(6) == "True"})
        m = re.match(r"early side: holds (\d+) of (\d+); late side: holds (\d+) of (\d+)", l)
        if m and cur:
            out[cur]["early_late"] = {"early": int(m.group(1)), "early_n": int(m.group(2)), "late": int(m.group(3)),
                                      "late_n": int(m.group(4))}
    return out


first, after, nojoin = (blocks("c5c2_arrow_evidence.txt"), blocks("c5c2_arrow_evidence_after.txt"),
                        blocks("c5c2_arrow_evidence_nojoin.txt"))
arrows = jl("model/arrows.jsonl")
STRENGTH = {"A01": "fair"}
for a in arrows:
    if a["id"] not in ("A01", "A03", "A07", "A11"):
        continue
    key = (a["from"], a["to"])
    f, w = first[key], copy.deepcopy(a)
    a["counts"] = {k: f[k] for k in ("both", "holds", "share", "null_mean", "null_p95")}
    a["early_late"] = f["early_late"]
    a["base_rate_beaten"] = "true" if f["beaten"] else "false"
    if a.get("clause_holds"):
        a["clause_holds"] = {"both": after[key]["both"], "rooms": after[key]["both"] - after[key]["holds"],
                             "statement": "no TO concept after the first FROM concept (c5c2_arrow_evidence_after.txt)"}
    if a.get("without_joining"):
        nj = nojoin[key]
        a["without_joining"] = {k: nj[k] for k in ("both", "holds", "share", "null_mean", "null_p95")}
        a["without_joining"].update({"beaten": nj["beaten"], "note": w["without_joining"].get("note")})
    if a["id"] in STRENGTH:
        a["strength"] = STRENGTH[a["id"]]
    if a["id"] == "A07":
        for t in a.get("support_transition") or []:
            if t["sub"] == "touhou":
                t["recut_note"] = ("C5c-02: touhou/c0090 sits under T3-041, which left P03 with Stigmergy's recut; this "
                                   "transition (which failed its audit at C2) no longer joins P03 to P11")
    a["recount"] = {"leg": LEG, "elements": "out/_analysis/c2_elements_c5c2.json",
                    "evidence": ["out/_analysis/c5c2_arrow_evidence.txt", "out/_analysis/c5c2_arrow_evidence_after.txt"]
                                + (["out/_analysis/c5c2_arrow_evidence_nojoin.txt"] if a.get("without_joining") else []),
                    "not_recounted": "sampled_against and the support transitions' audits are C2's, on the pass 4 elements"}
    mh.append({"t": T, "stage": "C5", "leg": LEG, "id": a["id"], "event": "recounted after Stigmergy's recut",
               "move": "relating or contrasting",
               "why": "%s -> %s on the recut elements: %d of %d (%.3f; null p95 %.3f; beaten %s); was %d of %d%s" % (
                   a["from"], a["to"], f["holds"], f["both"], f["share"], f["null_p95"], f["beaten"],
                   w["counts"]["holds"], w["counts"]["both"],
                   ("; strength %s to %s, the margin over the null now %.3f, like the arrows called fair" % (
                       w["strength"], a["strength"], f["share"] - f["null_p95"])) if a["id"] in STRENGTH else ""),
               "was": w})
for r in th:
    print("tier_history %s %s %s" % (r["id"], r["move"], r["event"]))
for r in mh:
    print("model/history %s %s: %s" % (r["id"], r["move"], r["event"]))
for a in arrows:
    if a["id"] in ("A01", "A03", "A07", "A11"):
        print(a["id"], a["counts"], a["early_late"], a["strength"], a.get("clause_holds"), a.get("without_joining"))
print("T4-006 prose:", f6["prose"][:400])
print("T4-007 prose:", f7["prose"])
if WRITE:
    wjl("fourth/fourth.jsonl", fourth)
    ajl("tier_history.jsonl", th)
    wjl("model/elements.jsonl", els)
    wjl("model/arrows.jsonl", arrows)
    ajl("model/history.jsonl", mh)
    print("written: fourth.jsonl, elements.jsonl, arrows.jsonl rewritten; %d tier_history and %d model/history lines"
          % (len(th), len(mh)))
