#!/usr/bin/env python3
"""D4a-01: write the two amendment specs for d4_amend.py from their sources, so that no id is typed. P05: the
nine re-check corrections are history line 172's adaptations (move 197), split into the six rooms of 'the shape
read' and the three where informed members hold the change, by the room lists F-024 and line 172 name; the frozen
statement is read from model/elements.jsonl. A11: the lines and rooms are d4a01_a11_classes.json's (D3a-38's census
re-run). Writes out/_analysis/d4a01_amend_P05.json and d4a01_amend_A11.json; never overwrites.

    python3 out/_analysis/d4a01_amend_specs.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
SHAPE = ["completeanarchy", "polska", "satania", "halo", "bangtan", "thesilphroad"]
INFORMED = ["armok", "maryland", "oneshot"]
for f in ("d4a01_amend_P05.json", "d4a01_amend_A11.json"):
    if os.path.exists(os.path.join(AN, f)):
        raise SystemExit("refusing to overwrite %s" % f)
H = [json.loads(l) for l in open(os.path.join(OUT, "model", "history.jsonl"), encoding="utf-8") if l.strip()]
h172 = H[171]
assert h172["id"] == "P05" and h172["leg"] == "D3c", "history line 172 is not move 197's P05 line"
ids = h172["adaptations"]
room_of = {i: i.split("-")[1] for i in ids}
assert sorted(room_of.values()) == sorted(SHAPE + INFORMED), room_of
shape_ids = [i for i in ids if room_of[i] in SHAPE]
inf_ids = [i for i in ids if room_of[i] in INFORMED]
els = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "model", "elements.jsonl"), encoding="utf-8")
       if l.strip()}
frozen = open(os.path.join(OUT, "_closes", "model-D3.sha256"), encoding="utf-8").read().strip()
p05 = els["P05"]
assert p05["status"] == "standing"
old = p05["statement"]
added = ("This holds where the keepers can learn of a planned change only by being told, and no informed member "
         "holds it.")
bound = ("It does not hold where the keepers read a planned change from its shape and stop repairing it with no "
         "telling: %s (%s), a candidate branch, 'the shape read' (F-024). It does not hold where informed members "
         "hold the change against keepers who do not know: %s (%s), a limit below the trigger, at three nodes. "
         "Amended at D4a-01, after the D3 freeze (%s...); not re-checked: no room was served these words." % (
             ", ".join(SHAPE), ", ".join(shape_ids), ", ".join(INFORMED), ", ".join(inf_ids), frozen[:8]))
why_choice = (
    "J asked for the scope written into the element, as the bound or as the widened revision held at D3c, by my "
    "choice with a reason. I write the bound. (1) It keeps the words all 705 rooms were re-checked against and "
    "narrows where they claim to hold. The widened revision adds a second route to the keepers' knowledge (reading "
    "the change's shape) and a holder (informed members), which no room was served and no re-check can now test "
    "(J: no further labelers or readers). (2) The six rooms' alignment warrants a cluster branch, not a new "
    "universal clause (rule 12: repeated corrections can define a cluster branch; they do not force the same "
    "revision everywhere). D4 can still read the trunk and the branch apart; one widened clause would join them. "
    "(3) The three informed-member rooms meet at three different nodes and do not reach the trigger. Writing them "
    "into the statement would widen the claim on evidence that no shared warrant joins, which rule 12 forbids "
    "('Do not loosen claims merely to absorb a case'). The widened revision stays held beside the branch (F-024).")
spec_p05 = {
    "id": "P05", "file": "elements", "move": "contrasting", "adaptations": ids, "rooms": SHAPE + INFORMED,
    "changes": [
        {"field": "statement", "now": old + " " + added,
         "event": "scope written into the statement after the D3 freeze (rule 11; J after the D3c interview): the "
                  "added clause bounded to rooms where the telling is the keepers' only route and no informed member "
                  "holds the change; not re-checked",
         "why": "Move 197 (D3c) decided the scope of the clause move 173 added, without a change to the frozen model "
                "(QD3-011, option b), and left P05's own words universal in form. J asked at D4 that the element's "
                "words carry the scope. The trunk is the frozen clause, bounded by contrasting the rooms where the "
                "keepers learn of a planned change only by being told with the six where they read it from its shape "
                "and the three where informed members hold it. " + why_choice},
        {"field": "status", "now": "bounded",
         "event": "status standing to bounded, with the scope in the statement and the bound; not re-checked",
         "why": "The statement now holds only under a stated condition, and the rooms it does not hold in are named "
                "in the bound (rule 11; stage D3 section 4: no exception printed beside an unchanged universal "
                "claim)."},
        {"field": "bound", "now": bound, "new": True,
         "event": "bound added, naming the six rooms of 'the shape read' and the three where informed members hold "
                  "the change, with their re-check lines; not re-checked",
         "why": "J asked that the element name the six rooms and armok, maryland and oneshot. Their lines are the "
                "nine accepted re-check corrections that history line 172 cites. polska and satania meet at T4-006, "
                "and halo and bangtan at T3-170 and T4-019 (corrections met twice); armok, maryland and oneshot meet "
                "at three different nodes."},
        {"field": "amendment", "new": True,
         "now": {"leg": "D4a-01", "rule": "11", "rechecked": False, "frozen_version": frozen,
                 "frozen": {"statement": old, "status": "standing"},
                 "note": "Amended after the D3 freeze; never served to the rooms. The frozen version stands beside "
                         "it, and every print of P05 marks it not re-checked."},
         "event": "the amendment record: the frozen version beside the amended one; not re-checked",
         "why": "J after the D3c interview: every amendment made after the freeze was never served to the rooms; mark "
                "each as not re-checked wherever it is printed, and keep the frozen version beside it."}]}
cl = json.load(open(os.path.join(AN, "d4a01_a11_classes.json"), encoding="utf-8"))
L, R = cl["lines_by_class"], cl["rooms_once_by_priority"]
a11_ids = sorted(L["talkonly"] + L["layoutonly"] + L["templatefirst"])
arr = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "model", "arrows.jsonl"), encoding="utf-8")
       if l.strip()}
a11 = arr["A11"]
assert a11["status"] == "standing" and a11["in_model"] is True
counts = {c: len(R.get(c, [])) for c in ("transition", "templatefirst", "across", "talkonly", "layoutonly")}
why_w = (
    "Rule 16 and rule 14: preserve what remains supported, and replace or withdraw what does not. No defensible "
    "formulation of A11 as an arrow survives the return. (1) The order between rooms never beat its null "
    "(111 of 185 rooms, 0.600; null p95 0.670; base_rate_beaten false), and C2 withdrew it, keeping a transition "
    "inside threads. (2) Inside threads, the return's census (D3a-38, re-run as _analysis/d4a01_a11_classes.json) "
    "shows the transition in %d rooms and template first in %d of the 228 rooms whose lines show both ends; across "
    "threads %d more. The reverse order is nearly as common, so the arrow carries no direction. (3) The failure "
    "clause is present and stands alone in %d rooms: talk only in %d (%s) and layout only in %d. (4) The "
    "mechanism's word 'settled' is contradicted by %d accepted restrict lines whose 'how' says a template does not "
    "settle the design for good (rival templates, polls, later redesigns, placers who deviate). A reworded arrow (a "
    "layout answers design talk in its thread) would be a new claim, never served to any room, with its reverse "
    "nearly as common: a co-occurrence, not an arrow. What remains supported, that design talk and layouts meet in "
    "threads, is held by P02's and P04's statements and ranges ('a design argued over days and redone'; 'an "
    "official template the room asks everyone to follow against other versions'), which stand. The arrow's record "
    "keeps its evidence and reasoning." % (
        counts["transition"], counts["templatefirst"], counts["across"], counts["talkonly"] + counts["layoutonly"],
        counts["talkonly"], ", ".join(R["talkonly"]), counts["layoutonly"],
        len(cl["restrict_naming_settling_accepted_specification"])))
spec_a11 = {
    "id": "A11", "file": "arrows", "move": "dropping working hypotheses", "adaptations": a11_ids,
    "rooms": R["talkonly"],
    "changes": [
        {"field": "status", "now": "withdrawn",
         "event": "arrow withdrawn after the D3 freeze (rule 11, rule 14; J after the D3c interview); not re-checked",
         "why": why_w},
        {"field": "in_model", "now": False,
         "event": "arrow leaves the model; P02 and P04 stand; not re-checked",
         "why": "A withdrawn arrow is not drawn and claims nothing. The figure without the theorised arrows "
                "(figure-C5.md, drawing 2) already leaves it out."},
        {"field": "withdrawn_why", "now": why_w, "new": True,
         "event": "the reason for the withdrawal, kept in the arrow's record; not re-checked",
         "why": "Rule 14: the evidence and reasoning are retained."},
        {"field": "amendment", "new": True,
         "now": {"leg": "D4a-01", "rule": "11 and 14", "rechecked": False, "frozen_version": frozen,
                 "frozen": {"status": "standing", "in_model": True},
                 "note": "Withdrawn after the D3 freeze; the rooms were re-checked against the arrow as standing. "
                         "Every print of A11 marks it withdrawn and not re-checked, beside the frozen version."},
         "event": "the amendment record: the frozen version beside the withdrawal; not re-checked",
         "why": "J after the D3c interview: mark each amendment as not re-checked wherever it is printed, and keep "
                "the frozen version beside it."}]}
json.dump(spec_p05, open(os.path.join(AN, "d4a01_amend_P05.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
json.dump(spec_a11, open(os.path.join(AN, "d4a01_amend_A11.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("P05: %d lines (%d shape read, %d informed); A11: %d lines, %d talk-only rooms; class counts %s; settling "
      "lines %d" % (len(ids), len(shape_ids), len(inf_ids), len(a11_ids), len(R["talkonly"]), counts,
                    len(cl["restrict_naming_settling_accepted_specification"])))
