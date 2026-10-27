# Audit, section 3: composition at each level, expectations and contrasts (E1b-07)

Written at E1b-07, 27 October 2026. The figures come from `audit-E1/expectations.py` and E1a's `element_reach.py`, each with its output beside it. The expectations and the field's entries are tabled in `expectations-E1.md`.

## 1. The composition diagnostics, recomputed

**Fixed-global verdicts**, ruled (both readers agreeing, or the analyst's D3 ruling on a split):

| return | model | composes | composes with residue | cannot tell | does not compose |
|---|---|---|---|---|---|
| first | e15f9647… (C5, pass 15) | 201 | 489 | 14 | 1 |
| re-check | 46384686… (D3, the freeze) | 630 | 56 | 19 | 0 |

The readers agreed on 542 rooms at the first return and split on 163. At the re-check they agreed on 544 and split on 161.

**Particulars and corrections met twice.**
- **Particulars:** 2,749 lines were ruled particular, in 545 rooms.
- **Distinct shared changes:** 223, counting one op on one element accepted in two or more rooms. These are the candidates for shared branches, not failures.
- **Accepted changes met in one room only:** 20.

**Limited branching or unbounded revision** (prior.md section 3).
- In A1's seeded reading order, the distinct shared changes number 184 after the first third of the rooms (235), 211 after two thirds and 223 at the end.
- The curve flattens over the last third, which is section 3's sign of limited branching.
- How many rooms carry a particular touching the model's top elements was not counted at this leg.

**Local validation, apart.**
- The element-reach half of section 3's measure was computed at E1a: 4,759 of 5,380 second-order themes that hold a coordinating turn are reached by a standing element (88.46 per cent), and 297 of the 696 rooms with a turn are reached in full.
- The other half, a validated adaptation or a theme listed as unresolved with its reason, was not computed.
- **Local validation is not established.**

**Unresolved evidence, apart:** 14 rooms could not be told at the first return and 19 at the re-check. 944 expectations had no line to test them (`expectations-E1.md`).

**Clusters and distinct global changes, against prior.md section 3.**
- The 223 shared changes gather into 35 branches, which overlap as facets: 476 rooms sit in a branch and 229 in none. Two branches pass the form test (F09, F32); 33 are groupings.
- Six room forms were cut from changes and codes at D4a-05 to D4a-08, by J's ruling.
- A branch's members share a key and the words of their records. A stated condition explains its members jointly only in the two forms.

## 2. Whether composition succeeded, failed or remains uncertain

**At the population level, the model composes in the return's terms.**
- The re-check finds the frozen model composing in 630 of 705 rooms, and in 56 more with residue. No room fails to compose.
- The expectations score 0.924, in-sample.
- The mechanism the composite rests on is the spine, start, call, build and keep, whose order counts beat their nulls; the propositions are tabled in `claims-E1.md`.

**Below it, the population compiles rather than composes**, in Kozlowski and Klein's sense: different rooms contribute different configurations. The facets, the two forms, the six room forms and the particulars in 545 rooms all show it. That word describes how the levels emerge. It is not a success grade.

**At the leaf, composition remains uncertain.**
- Local validation is not established.
- The reconstruction sample, the test at the leaf, has not yet been run; it comes at E1c and E1d.
- The `composition_status` line is written in `audit-E1.md` after that check. Until then, the stated level, scope and evidence are these: the population level is supported in the return's own terms; the leaf is unresolved.
- The original fixed-global verdicts above are kept apart from the current adapted-local status and from shared-branch adequacy, as the stage asks.

## 3. prior.md section 2's expectations, and stage A1's three sentences

| expectation | held? | against |
|---|---|---|
| (operator's) continuity at the top, drops at the bottom, a model all the way down | **In part.** The top holds at the re-check. The branches state mostly restrictions, and the levels go down to room forms, branches and particulars. | the verdicts, `branches-D5.jsonl` |
| becoming able to act rests on a find more than on persuasion; a call alone often draws nothing | **In part.** The start comes before the call in the spine. Most calls get no written reply. | `account.md`, the spine's arrows |
| what to act on is settled before the room speaks, by the canvas, a host or one member's start; votes are rare and late | **In part.** Decided order is rare in the coding but often in the return (C01 taken up where absence was expected in 81 rooms). A template does not settle the design for good (the A11 proposal held). | `expectations-E1.md`, `claims-E1.md` |
| loss of the spot sends a room back; then it moves, shrinks, joins or stops | **Held, thin.** A10, on 21 rooms. F09: rooms rebuild after moving. | `claims-E1.md` |
| what follows organizing is talk about it, and the end clusters near hour 73 | **Held.** The close: celebration, record and carrying on. | the propositions, `waterfall-D5.md` |
| a handful of forms, differing in where work is coordinated and on whose terms the room holds its space; the national rooms not one form | **In part.** Six room forms, two of them (behind the thread; moving for the spot) close to the expected kinds. The national rooms spread across forms (the Dutch telling of D6). The branches are facets, not forms. | `room-forms-names.md` |
| at the top the population compiles; limited branching for deals and venues; particulars for rooms carried by one member | **Held for compilation and limited branching.** Particulars are far wider than expected: 545 rooms. | this section |

**Stage A1's three sentences** (`notes-A1.md`, "Three sentences on what I expect"), against the structure:
- *One burst of calls, coordinates and reports, then a long tail of defence and looking back, stopping near hour 73.* **Held.** The dimensions of coordination, upkeep and imprinting carry it.
- *Fights with canvas neighbours more than distant rivals; deals about borders and space, in the thread or sent to Discord.* **Held in part.** Border terms and the chat carry it, but a tie from before the canvas can name the rival (C02, untested for order).
- *The goal settled in the first hours by one person's call, and changed only under a neighbour's pressure or a loss, rarely by argument inside the room.* **Not held.** Form C, "the design reopened" (96 defining rooms), and the return's 627 accepted restrict lines on A11 show the design argued and reopened inside rooms.

## 4. The onset contrast

The late side of every arrow holds 0 to 15 rooms, so by rule 6 no gap is read. A1's four expectations on onset are untested by these counts, as a boundary condition the record could not test. `expectations-E1.md` gives the figures.

## What this part cannot say

- Whether the model composes at the leaf. That is the reconstruction's test (E1c, E1d).
- How many rooms carry a particular that touches the model's top elements.
- Whether any expectation scored here would hold out of sample. None was held out.
