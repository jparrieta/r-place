#!/usr/bin/env python3
"""C2d-02, pass 5, declaration 3 (QC2-002): the claim C02, carried in the rooms' words and marked untested for order.

Reads the candidates listed by c2d2_claim_candidates.py (c2d2_claim_candidates.txt) and records my reading of each
candidate that calls for or carries out an attack, against the three checks: (a) the turn calls for or carries out an
attack on another room's work; (b) it names the rival; (c) it names the tie the members had before the canvas (a
league or school rivalry, a nation's history, an ideology, lore) or rests on it in its words (a team's colours, a
school's name). Every candidate not listed in DECISIONS fails check (a): it neither calls for nor carries out an attack
(peace, defence, rulings on guests, building, taunts built as the room's own mark, talk after the close).
Colour-faction turns are read the same way and reported apart (declaration 4), since the factions are bodies the
canvas gathered.

Writes out/_analysis/c2d2_claim_checks.json; with --write also appends F-013 to findings.jsonl, then C02 to
model/elements.jsonl with a model/history.jsonl line (event added, move developing or dropping working hypotheses).
Refuses to add C02 or F-013 twice.

    python3 out/_analysis/c2d2_claim_c02.py [--write]
"""
import collections, datetime, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
CAND = os.path.join(OUT, "_analysis", "c2d2_claim_candidates.txt")
DEST = os.path.join(OUT, "_analysis", "c2d2_claim_checks.json")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# (sub, code, result, note). result: "C02" passes all three; "colour" passes all three in a colour faction;
# otherwise the failing check.
DECISIONS = [
    ("unitedkingdom", "c0146", "C02", "covering Germany's flag; the two world wars named"),
    ("unitedkingdom", "c0186", "C02", "taking Argentina; the Falklands named"),
    ("unitedkingdom", "c0154", "c", "turning the Scottish flag British: the union is the room's own nation, not a tie that names a rival outside it"),
    ("unitedkingdom", "c0187", "c", "the EU flag to be replaced; no tie named in the words"),
    ("unitedkingdom", "c0250", "c", "the Scottish flag into St George's; no tie named in the words"),
    ("unitedkingdom", "c0279", "b", "the Belgrano drawn over 'their centre design'; the rival is a pronoun in the turn"),
    ("sweden", "c0122", "b", "expansion called with the Great Power era named; no rival named"),
    ("sweden", "c0144", "b", "Operation Little Belt names a Danish strait; the rival only by allusion"),
    ("sweden", "c0195", "b", "Operation Little Belt and the Caroleans; the rival only by allusion"),
    ("anarcho_capitalism", "c0009", "C02", "Commie Red to Capitalist Gold: the rival and the ideology named"),
    ("completeanarchy", "c0192", "C02", "taking over the ancap flag: the rival named by its ideology"),
    ("completeanarchy", "c0193", "c", "'do step on snek': the rival's flag altered; no tie named"),
    ("completeanarchy", "c0244", "c", "the snake stepped on; no tie named"),
    ("CKCrusaders", "c0063", "C02", "the Byzantine flag to replace the Turkish flag"),
    ("CKCrusaders", "c0085", "C02", "a crusade to recapture Constantinople; the flag of Turkey to conquer"),
    ("CKCrusaders", "c0071", "b", "the next target named only by a slur for Turks; no flag or people named"),
    ("lakers", "c0075", "C02", "the Celtics' logo lit up in purple and gold, the Lakers' colours"),
    ("lakers", "c0050", "c", "the Celtics named and the attack called; no tie in the words"),
    ("lakers", "c0051", "b", "'replace it with the purple and gold'; the rival a pronoun"),
    ("lakers", "c0058", "b", "'hit the green'; the rival by colour only"),
    ("lakers", "c0082", "c", "a guide to replace the Celtics logo; the team named only as the work's own logo"),
    ("lakers", "c0085", "b", "'cover up all your championships'; the rival a pronoun"),
    ("lakers", "c0231", "c", "vandalising the Celtic territory, told after the close; no tie named"),
    ("cardinals", "c0033", "C02", "the Cubs logo to be turned red, the Cardinals' colour"),
    ("cardinals", "c0029", "c", "the Cubs logo into Cubsuck; no tie named"),
    ("cardinals", "c0034", "c", "help to get rid of the Cubs logo; no tie named"),
    ("cardinals", "c0043", "c", "the Cubs U made an O; no tie named"),
    ("cardinals", "c0063", "c", "destroy the Cubs logo; no tie named"),
    ("cardinals", "c0089", "c", "it would be fun to destroy the Cubs logo; no tie named"),
    ("cardinals", "c0090", "c", "the Cubs logo made to say Cucs; no tie named"),
    ("cardinals", "c0094", "c", "the same; no tie named"),
    ("cardinals", "c0097", "c", "Cobs achieved; no tie named"),
    ("cardinals", "c0102", "c", "the logo made to say cocks; no tie named"),
    ("cardinals", "c0100", "c", "help change the Cubs logo to say Cocks; no tie named"),
    ("cardinals", "c0101", "c", "'TAKE THAT YOU DIRTY CUBS FANS'; the rival's fans named, no tie named"),
    ("rpi", "c0023", "c", "'Yes, WPI.' confirms the target; no tie named"),
    ("rpi", "c0022", "C02", "'a lil interpolytechnic griefing' of WPI: the schools' tie named"),
    ("rpi", "c0093", "C02", "erase WPI, 'thinking they can take our name': the schools' rivalry over the name"),
    ("rpi", "c0021", "b", "the call names RPI's own spot by mistake"),
    ("rpi", "c0024", "c", "hijack WPI; no tie named"),
    ("rpi", "c0029", "c", "the W made an R; no tie named"),
    ("purplecorner", "c0008", "colour", "'Team Purp! Only replace filthy blue tiles!'"),
    ("purplecorner", "c0023", "c", "'Bring down the Blue'; the faith not named in the turn"),
    ("orderofthebluecorner", "c0014", "colour", "the red and green to be purged as heresy from the blue's canvas"),
    ("thebluecorner", "c0009", "colour", "the destruction of the Red war machine for a blue place"),
    ("thebluecorner", "c0230", "colour", "'Blue the Purple Corner!'"),
    ("thebluecorner", "c0943", "colour", "move to the Green Lattice and make it blue"),
    ("thebluecorner", "c0088", "c", "the attack on the Green Corner announced; the faith not named"),
    ("thebluecorner", "c0106", "c", "destroy the purple triangle; the faith not named"),
    ("thebluecorner", "c0461", "c", "take down the Void; the faith not named"),
    ("thebluecorner", "c0047", "c", "finish the red corner; the faith not named"),
]
text = {}
for l in open(CAND, encoding="utf-8"):
    m = re.search(r"^\"(.*)\"\s+\[([^/\]]+)/(c\d{4})\]\s+item \S+\s+thread \S+\s+h\+([\d.]+)\s+(\S+)\s+(t\d\d)", l)
    if m:
        text[(m.group(2), m.group(3))] = {"quote": m.group(1), "hour": float(m.group(4)), "second": m.group(6)}
missing = [(s, c) for s, c, _, _ in DECISIONS if (s, c) not in text]
if missing:
    sys.exit("decisions name candidates not in the candidates file: %s" % missing)
rows = []
for s, c, res, note in DECISIONS:
    x = text[(s, c)]
    rows.append({"sub": s, "code": c, "hour": x["hour"], "second_order": x["second"], "quote": x["quote"], "result": res,
                 "note": note})
passed = [r for r in rows if r["result"] == "C02"]
colour = [r for r in rows if r["result"] == "colour"]
json.dump({"about": "C02's three checks, read by me (c2d2_claim_c02.py); every candidate in c2d2_claim_candidates.txt "
           "not listed fails check (a)", "rows": rows}, open(DEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
c = collections.Counter(r["result"] for r in rows)
print("listed %d of %d candidates: %s" % (len(rows), len(text), dict(c)))
print("C02: %d turns in %d rooms: %s" % (len(passed), len(set(r["sub"] for r in passed)),
                                         ", ".join("%s/%s" % (r["sub"], r["code"]) for r in passed)))
print("colour factions: %d turns in %d rooms" % (len(colour), len(set(r["sub"] for r in colour))))
if "--write" not in sys.argv:
    sys.exit(0)
FP = os.path.join(OUT, "findings.jsonl")
EP = os.path.join(OUT, "model", "elements.jsonl")
HP = os.path.join(OUT, "model", "history.jsonl")
if any(json.loads(l).get("id") == "F-013" for l in open(FP, encoding="utf-8") if l.strip()):
    sys.exit("F-013 exists; not written again")
if any(json.loads(l).get("id") == "C02" for l in open(EP, encoding="utf-8") if l.strip()):
    sys.exit("C02 exists; not written again")
rooms = sorted(set(r["sub"] for r in passed))
# status must be standing|bounded|withdrawn (validate.py); untested-for-order is carried in "untested" and the bound.
# The first run wrote status "untested for order"; c2d2_f013_status.py appended the superseding line.
f = {"stage": "C2", "leg": LEG, "id": "F-013", "tier": "element", "warrant": "read", "status": "standing", "untested": "order",
     "statement": ("In some rooms a tie the members had before the canvas names the rival in the same turn that calls "
                   "for or carries out the attack. Read in the story rooms of passes 1 to 4, %d turns in %d rooms pass "
                   "three checks (an attack called or carried out, the rival named, the tie named or rested on in the "
                   "words): %s. Examples: \"For two world wars the French and british have stood together against the "
                   "germans ... covering the flag of Germany\" (unitedkingdom/c0146); \"You mean WPI? I'm down for a lil "
                   "interpolytechnic griefing.\" (rpi/c0022); \"Proposal: CRUSADE against the infidel. Recapture "
                   "Constantinople ... The flag of Turkey is bottom left from us, let's conquer it.\" (CKCrusaders/c0085)."
                   % (len(passed), len(rooms), ", ".join(rooms))),
     "evidence": ["out/_analysis/c2d2_claim_checks.json", "out/_analysis/c2d2_claim_candidates.txt"] +
                 ["%s:%s" % (r["sub"], r["code"]) for r in passed],
     "bound": ("Untested for order (QC2-002): the tie and the attack are one turn, so no order statement can count it, "
               "and no share of rooms is claimed. The coders placed these turns under the attack and taunt themes; in "
               "lakers, rpi and cardinals no concept sits under the membership candidate's themes. Colour factions the "
               "canvas gathered name rivals the same way (%d turns in %d rooms) and are reported as a boundary, not as "
               "this finding, since their faith is not a tie from before the canvas." % (len(colour), len(set(r["sub"] for r in colour)))),
     "refuted_by": ["a reading in which the cited turns' rivals were chosen by the canvas (neighbours, attackers) and the "
                    "named tie only dresses the choice: the rival named in the turn is the room's nearest neighbour or "
                    "its attacker, not a rival known before the canvas"],
     "t": T, "why": "pass 5, declaration 3: J's ruling on QC2-002"}
with open(FP, "a", encoding="utf-8") as fh:
    fh.write(json.dumps(f, ensure_ascii=False) + "\n")
e = {"id": "C02", "kind": "claim",
     "statement": ("In some rooms, a tie the members had before the canvas (a league or school rivalry, a nation's "
                   "history, an ideology, lore) names the rival in the same turn that calls for or carries out the attack."),
     "tier": ["T4-020", "T4-021", "T4-022", "T4-004"], "dimension": ["D08", "D05"],
     "range": ("from a team's colours turned on a league rival's logo to a war from the nation's history named as the "
               "reason to cover a neighbour's flag"),
     "evidence": {"findings": ["F-013"], "codes": ["%s:%s" % (r["sub"], r["code"]) for r in passed]},
     "since": "C2-pass-5", "leg": LEG, "status": "standing", "untested": "order"}
rows_e = [json.loads(l) for l in open(EP, encoding="utf-8") if l.strip()]
with open(EP, "a", encoding="utf-8") as fh:
    fh.write(json.dumps(e, ensure_ascii=False) + "\n")
with open(HP, "a", encoding="utf-8") as fh:
    fh.write(json.dumps({"t": T, "stage": "C2", "leg": LEG, "id": "C02", "event": "added",
                         "move": "developing or dropping working hypotheses",
                         "why": "pass 5 declaration 3 (QC2-002): membership naming the rival in the same turn as the "
                                "attack, carried as a claim in the rooms' words, untested for order", "was": None},
                        ensure_ascii=False) + "\n")
print("F-013 appended; C02 appended (elements now %d); 1 history line" % (len(rows_e) + 1))
