#!/usr/bin/env python3
"""C5c-12, the fold-in: rewrite the head's top (status, the current account, the reasons for the last revisions, where
the run stands) from the setup before the serial work (serial-C5/head-before-serial.md) with the four findings folded
in, and its next comparison. The carried sections from 'Stage C4, in short' on are kept as they stand. Prints the word
count; refuses to write above 3,000 words.

    python3 out/_analysis/c5c12_head.py            count only
    python3 out/_analysis/c5c12_head.py --write
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.join(ROOT, "out", "_head.md")
cur = open(H, encoding="utf-8").read()
before = open(os.path.join(ROOT, "out", "serial-C5", "head-before-serial.md"), encoding="utf-8").read()
cut = cur.index("## Stage C4, in short")
bottom = cur[cut:]
i = bottom.index("## The next comparison")
bottom = bottom[:i] + ("## The next comparison\n\nThe next leg redoes C5d from `model/` as pass 15 left it. The four "
                       "finding files in `serial-C5/` list what its outputs must take.\n")
# the method and theory questions are carried verbatim from the setup before the serial work
qa = before.index("## The method question, in one sentence")
qb = before.index("## The current account, and the contrary rooms")
questions = before[qa:qb]
top = """# Head, claude-v43-1 (branch claude-v43-1--C4-field)

Under 3,000 words, rewritten whole at every close. Last written at C5c-12, 2026-10-15 (UTC). Stages A1 to C4 are done; stage B is frozen. J lifted the C5d freeze for serial work in this branch (C5c-07). The four problems (C5c-08 to C5c-11) and the fold-in (C5c-12, pass 15) are done. C5d is redone next and closes C5 with `done.sh C5 --cut interview`. `validate.py C5`: 0 errors, 0 warnings.

""" + questions + """## The current account, and the contrary rooms

The account is `account.md`, pass 15 (3,318 words; passes 1, 3, 4, 5 and 8 kept), with the readers' disagreements in `account-readers-C5.md`. The nine propositions are in `propositions.jsonl`. A room, or a group of rooms, is the actor where its members spoke or acted for it.
- **The spine.** A member starts a mark [R01]. The room's calls follow the start in 64 of 89 rooms [A02], building follows calls in 81 of 126 [A01], and keeping follows building in 148 of 190 [A03].
- **The bare answer.** Most calls get no written reply. In written replies, acceptances come bare (25 of 31 to calls to place, F-023) and refusals give a reason (3 of 3; attack calls 23 of 38, F-014). The head-count claim failed (F-015).
- **The host's line.** It follows the calls in 132 of 155 rooms [A20].
- **Alignment without decision** (theorised, thin). 233 of 370 rooms with calls report a work up after the first call, so there the room aligned many hands; the others tried (F-021). A template settles a design inside a thread [A11]. Decided order is coded in 46 of 705 rooms [C01, F-006].
- **Direct information sharing (T4-007, Stigmergy until C5c-10).** Members post the mark's state (10 of 14 bearing records; F-018); one member, against C2's criterion. Posting the state and sharing templates are carried largely apart (89 rooms both, 80 by chance; F-022).
- **Other rooms.** Keeping brings talk with neighbours in 235 of 401 rooms [A04]; border talk that came first mostly offered terms (19 of 26 to 36 of 38, two coders). Help names a deal in 63 of 127 rooms where border talk came first, against 23 of 67 [A14; F-020]. Sparing rests mostly on the room's own norm, so A05's mechanism is theorised (F-020). Rooms join coalitions [A19] and cannot make every placer keep an agreement.
- **The contest.** A call can turn members against a rival [A15]. The same room meets the attack call with sparing, refusal or apology [A16] and border talk [A17].
- **Loss** (thin). A room that judges it has too few hands moves [A10]; read whole, the judgment came first in 10 of 20 rooms that moved. After doubt and a loss, 10 rooms moved and 11 gave the work up (F-019). No loop is grounded.
- **The close.** The room celebrates, records and carries the work on [A07, A08, A09]. Placement stops at hour 73; after it, rooms curate the record (P12; P22 tentative), apart from carrying on (P13).
- **Machine hands.** Scripts follow upkeep under strain [A06].
- **C02** (untested for order): a tie the room had before the canvas names the rival in the attack turn.
- **Cut to candidate:** P06 and R02. K01 restored, with no arrow (F-009). 23 elements stand.

**The room that best supports the account: day9.** It offers a neighbour terms before any damage, loses its border at hour 48, moves within two hours, and finishes the new work at hour 53.

**The room that most threatens it: thebluecorner.** It is a colour faction whose faith names its rivals and rules on guests.

**The condition between them** is what decides whom a room fights and whom it admits. Where the work decides, the model tells the room. Where a faith or a host's rule decides, it does not.

## The reasons for the last revisions

- **J's rulings of 15 October, 01:29 Berlin** (J has delegated C5 questions to the handler):
  1. Work after hour 73 is curation of the record (P12; P22 tentative), apart from carrying on (P13).
  2. The prose pass on the declarations comes first, with the rule written first and each amendment a move.
  3. Stigmergy is recut only if it joins what Heylighen 2016 and Grassé 1959 keep apart.
  4. The C5 readers are the second reader of the declarations; QC5-001 adds the field analyst.
  5. J's language ruling stands.
- **Passes 1 to 4 (C5a).** Declarations amended under the prose rule; A04 bounded; P06 and R02 cut; K01 cut and restored (move 92); nine propositions.
- **J, 07:59 to 09:09 Amsterdam.** I decide what enters and leaves the model; the field analyst reads all 36 declarations against the members' quotes (QC5-001).
- **Passes 5 to 8 (C5c-01 to C5c-04).** The readers' errors fixed; Stigmergy recut by three codings (F-018); 94 pieces of field advice accepted, 30 kept (moves 93 to 146).
- **J, 11:02 and 12:01 Amsterdam.** The field analyst's marks are advice; the room is the unit. Passes 9 and 10 restored K02, A10 and P13 to the room, then changed nothing.
- **J, 13:45 and 14:14 Amsterdam (C5c-07, QC5-002).** The freeze is lifted for serial work; argue from organization design; say how each problem serves the two questions. The border package for a second coder is `field-packages-C5b/`.
- **The serial work, passes 11 to 14,** each with its finding in `serial-C5/`: the unit (C5c-08, moves 150 to 163); thin evidence (C5c-09, F-019, F-020, moves 164 to 167); Stigmergy renamed and "aligned" (C5c-10, F-021, F-022, moves 168 and 169); the reason test (C5c-11, F-023, F-014 superseded, move 170).
- **C5c-12 (pass 15), the fold-in.** The findings folded once into the account, the propositions (N09 narrowed), the prose test and the model (A16, move 171); F-019's quote restored to the record's spelling.

## Where the run stands

- **C5 outputs:** `account.md` (pass 15) and earlier passes, `propositions.jsonl` (9; earlier passes kept), `prose-test-C5.md` (pass 14 kept), `sketches.md`, `account_passes.jsonl` (15 lines), `notes-C5.md`, and `serial-C5/` (the four findings and the head before the serial work).
- **C5b to C5d outputs:** `author_claims.jsonl`, `RETURN-C5.md`, `_packets-C5/`, `readers-C5/`, `account-readers-C5.md`, `field-packages-C5/`, `field-packages-C5b/`; C5d's `data_structure-C5.md`, `figure-C5.md`, `implications-C5.md`, `handback-C5.md` and `interview/C5d.md`, to be redone.
- **Ledgers:** `tier_history.jsonl` 561, `model/history.jsonl` 134, `findings.jsonl` 36 lines (23 findings), `model/elements.jsonl` 30 (23 standing), `model/arrows.jsonl` 21.
- **Snaps** run to C5-move-developing-171. Scripts: `out/_analysis/c5*`.
- **Still open in C5:** the fields the prose rule did not read (`adaptation`, `disconfirm`, the question lines); `structure-C4.md`'s stale prose; Critical mass still flagged; the border coders' slight agreement (kappa 0.19).
- **The questions.** QC5-001 and QC5-002 are answered. QC4-001 and QC4-002 are answered; `out/_field-link-superseded-C4a` stays as it is.

"""
new = top + bottom
n = len(re.findall(r"\S+", new))
print("head: %d words" % n)
if "--write" in sys.argv:
    if n > 3000:
        sys.exit("over 3,000 words; not written")
    open(H, "w", encoding="utf-8").write(new)
    print("written")
