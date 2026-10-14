#!/usr/bin/env python3
"""C2d-01, pass 4: the authored texts the two recuts left stale, and the notes for structure-p4.md.

  1. fourth/fourth.jsonl: Meta-organization's and Flagging the nation's construct fields (changed, mistaken_for,
     disconfirm, and Flagging the nation's adaptation) still described hosting and making the flag, which the recuts
     moved out. They are rewritten in place, one tier_history line each with the old line as `was` (a correction
     completing the recuts, same moves).
  2. out/_analysis/c2_t4_fields_p4.json: pass 1's fourth-order fields with the four recut themes' changed, question,
     outside and least_sure rewritten (changed is copied from fourth.jsonl).
  3. out/_analysis/c2_structure_notes_p4.json: pass 2's notes with D02's, D04's and D05's texts revised and pass 4's
     Part A return.
Refuses to overwrite either JSON file; the fourth.jsonl correction refuses to run twice.

    python3 out/_analysis/c2d_structure_notes_p4.py [--write]
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
FP = os.path.join(OUT, "fourth", "fourth.jsonl")
TH = os.path.join(OUT, "tier_history.jsonl")
DF, DN = os.path.join(AN, "c2_t4_fields_p4.json"), os.path.join(AN, "c2_structure_notes_p4.json")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
for p in (DF, DN):
    if os.path.exists(p):
        sys.exit("%s exists; not overwritten" % os.path.relpath(p, ROOT))
rows = [json.loads(l) for l in open(FP, encoding="utf-8") if l.strip()]
t4 = dict((r["id"], r) for r in rows)
NAME = dict((r["name"], r["id"]) for r in rows)
MO, FN, CR, TE = NAME["Meta-organization"], NAME["Flagging the nation"], NAME["Collective representation"], NAME["Territoriality"]
if "hosts included" not in t4[MO]["mistaken_for"]:
    sys.exit("Meta-organization's fields already corrected")
FIX = {
    MO: {"changed": ("Ahrne and Brunsson's meta-organizations have formal members and decided rules; here membership in "
                     "an alliance or a hub is often one message in a chat, revocable by anyone's pixels."),
         "mistaken_for": ("One room's diplomacy: the construct holds bodies of rooms acting as partners, not one room's deal "
                          "with a neighbour (Negotiated order) or its rule over guests on its mark (Territoriality)."),
         "disconfirm": ("Fails where groups on a shared surface act only one by one, or where bodies of rooms are named but "
                        "never defend, tally or build for a member's work.")},
    FN: {"adaptation": ("Billig's flagging is the daily, unnoticed reminding of nationhood by flags hung everywhere. Here "
                        "the nation is claimed out loud around a flag made by hand, so banal flagging turns into enacted "
                        "nationalism at small stakes. Changed: making the flag is the mark's content and sits with "
                        "Collective representation; what stays here is the claim of the nation beyond the mark, its "
                        "history, kin, belonging and national others, drawn into a game."),
         "changed": ("Billig's flagging works because it goes unnoticed; here the nation is claimed out loud, around a "
                     "flag made on purpose and noticed by everyone."),
         "mistaken_for": ("Nationalism as ideology: the construct holds the practice of claiming the nation through the "
                          "canvas (kin, history, belonging, national others), not doctrines; and making the flag, which "
                          "is the mark's content (Collective representation)."),
         "disconfirm": ("Fails where building a national flag on a shared surface stirs no talk of belonging, history, kin "
                        "nations or national others.")}}
why = ("pass 4: the recuts (declarations 1 and 2) rewrote these themes' members, gloss and prose and left their construct "
       "fields describing hosting and making the flag, which moved out; corrected in the same pass")
was = dict((k, json.loads(json.dumps(t4[k]))) for k in FIX)
for k, f in FIX.items():
    t4[k].update(f)
    t4[k]["t"] = T
hist = [{"t": T, "stage": "C2", "leg": LEG, "tier": "fourth", "id": k, "move": t4[k]["move"], "event": "fields_corrected",
         "was": was[k], "now": [dict({"id": k}, **FIX[k])], "why": why} for k in FIX]

f4 = json.load(open(os.path.join(AN, "c2_t4_fields_p1.json"), encoding="utf-8"))
f4["about"] = "pass 4 fields: pass 1's, with the four themes the pass 4 recuts touched rewritten"
for k in (MO, FN, CR, TE):
    f4["themes"][k]["changed"] = t4[k]["changed"]
f4["themes"][TE].update({
    "question": ("How a room claims, grants, yields and abandons a place on a finite surface that no one owns, and whose "
                 "works may live on its mark."),
    "outside": ("Growing into a neighbour's space (Repertoire of contention); rooms defending one another's works as partners "
                "(Meta-organization); near case: expansion over another flag, a claim made by attack."),
    "least_sure": ("T3-099, relying on a bigger neighbour: a guest living under a host's rule (inside, from pass 4) or a small "
                   "room's partnership with a stronger one (Meta-organization).")})
f4["themes"][MO].update({
    "question": "How rooms organize as bodies of rooms: partners that gather, tally, plan and build together.",
    "outside": ("A room hosting another room's work on its mark (Territoriality, from pass 4); canvas-born colour factions "
                "(Neo-tribes); near case: the void, a body of individual placers rather than of rooms."),
    "least_sure": ("T3-153, meeting other rooms in chat: a shared council (inside) or a backstage (Backstage "
                   "decision-making).")})
f4["themes"][CR].update({
    "outside": ("Claiming the nation beyond the mark: kin nations, national history, belonging (Flagging the nation); near "
                "case: a national room arguing whether its flag should carry a disputed emblem, which settles the mark here "
                "and argues belonging there."),
    "least_sure": ("T3-113, drawing national emblems: what the room's mark shows (inside, by the pass 4 rule) or a claim of "
                   "the nation beyond the mark (Flagging the nation), where an emblem is drawn to answer a rival people.")})
f4["themes"][FN].update({
    "question": "What national rooms claimed of the nation beyond the mark, and why their fights could be told as history.",
    "outside": ("Making the land's flag or its emblems the mark (Collective representation, from pass 4); arguing over a "
                "political or religious symbol (Symbolic boundaries); near case: covering a swastika near a national flag, "
                "which draws a moral line rather than claiming a nation."),
    "least_sure": ("T3-079, joining flags with a heart: a joint mark's content (Collective representation) or a claim of "
                   "kinship between nations (inside).")})

n = json.load(open(os.path.join(AN, "c2_structure_notes_p2.json"), encoding="utf-8"))
n["about"] = "pass 4 notes: pass 2's, with D02, D04 and D05 revised after the two pass 4 recuts, and pass 4's Part A return"
n["dimensions"]["D02"] = {
    "outside": ("Calling hands (Mobilization, in Critical mass); claiming the nation beyond the mark (Flagging the nation, in "
                "Collective identity); near case: a call that brings placers but says nothing about what or where to place."),
    "least_sure": ("T4-006 Collective representation: choosing the emblem settles what the room acts on (inside), but it is "
                   "argued as what the room is (Collective identity); from pass 4 it holds the land's flag and emblems.")}
n["dimensions"]["D04"] = {
    "outside": n["dimensions"]["D04"]["outside"],
    "least_sure": ("T4-014 Territoriality, widened at pass 4: a room's claim on space (inside), and with hosting a rule over "
                   "guests' works on its mark, which could read as one relation with each guest (Reciprocity).")}
n["dimensions"]["D05"] = {
    "outside": ("Choosing the emblem, the land's flag and emblems included from pass 4 (Collective representation, in "
                "Coordination without command); near case: a fandom room arguing which character to draw, a choice inside "
                "a membership rather than the membership itself."),
    "least_sure": n["dimensions"]["D05"]["least_sure"]}
n["return"] = {
    "least_sure_dims": {"text": ("D05 Collective identity and D02 Coordination without command**, now that the land's flag "
                                 "and emblems cross from the first to the second (pass 4)"),
                        "pairs": ["D02|D05"]},
    "alternative": ("The reviewer's partition (C2c), adjusted Rand 0.661 against mine. Two of its divergences were taken at "
                    "pass 4 as recuts by rules written first: hosting beside territory, and the land's flag and emblems "
                    "beside the mark's content. Three were refused: relocation joined to collective efficacy (it would hide "
                    "the order the move arrow claims), reconciliation apart from restraint (both answer how a room keeps from "
                    "harming another's work) and identity split by activity (membership must stay a construct the return "
                    "can test); the last stands beside the claim. The host sub split by actor was run as a test, not a "
                    "recut: both actors' acts follow the calls."),
    "least_sure_t4": ("T4-022 Flagging the nation.** After the flag and emblems left it, it holds the nation claimed beyond "
                      "the mark, and its one test (membership carried in before the attack, on the narrowed candidate) came "
                      "out below the null mean. Next to it, T4-007 Stigmergy, which rests on two large themes.")}
print("fourth.jsonl: corrected %s; fields for %s; notes D02, D04, D05 and the return" % (
    ", ".join(FIX), ", ".join((MO, FN, CR, TE))))
if "--write" in sys.argv:
    with open(FP, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(TH, "a", encoding="utf-8") as fh:
        for h in hist:
            fh.write(json.dumps(h, ensure_ascii=False) + "\n")
    with open(DF, "w", encoding="utf-8") as fh:
        json.dump(f4, fh, ensure_ascii=False, indent=1)
    with open(DN, "w", encoding="utf-8") as fh:
        json.dump(n, fh, ensure_ascii=False, indent=1)
    print("written: fourth.jsonl (%d lines), %d tier_history lines, %s, %s" % (
        len(rows), len(hist), os.path.relpath(DF, ROOT), os.path.relpath(DN, ROOT)))
