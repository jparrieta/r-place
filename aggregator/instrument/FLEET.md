# FLEET, v38. The fan-out, the figures, and the return.

Given with stages B2 to B4 and D2 beside the contract. The vocabulary of the figures is this
file's; the rules that bind the fleets are the contract's (rules 0, 3, 7, 12, 19).

<!-- INDEX -->
| section | lines | words |
|---|---|---|
| 1. The fan-out | 14 to 54 | 500 |
| 2. The figures, one definition each | 55 to 70 | 294 |
| 3. The return, stages D1 to D3 | 71 to 113 | 465 |
<!-- /INDEX -->

## 1. The fan-out

**The fleets at B2 to C1** are hands: they place what you would have placed, under the instrument
you wrote, as close to how you would have done it as a written instrument allows, at `R = 2`
readers per item at B3 and B4 so that a disagreement is visible (the pilot, B2, uses three). `R = 2` detects disagreement; it does not
estimate stability, which is measured once, on the gold set, in the pilot, with the same items
under two rewordings of the brief.

| step | stage | for |
|---|---|---|
| 1 pilot | B2 | you answer hard items yourself, *then* write the instrument, then learn whether it decides for a stranger |
| 2 fleet | B3 | the frozen instrument applied by many readers in fresh contexts, gold seeded unannounced |
| 3 adjudication | B4 | the contested items only, with a taxonomy; transmission decomposed; a blind sample re-placed by fresh readers: transmission after revision, with alpha |
| 4 revision | C1 | the instrument revised on its sources; the object the next stage consumes |

Files: `author_items.jsonl`, `scheme_final.md/.jsonl`, `gold_items.jsonl` (never shown),
`assign_raw.jsonl`, `fidelity-B3.md`, `disagreements.jsonl`, `transmission-B4.md`,
`assign_final.jsonl`, `reassign.jsonl`, `transmission-after-revision-B4.md`, `scheme_v2.md/.jsonl`,
`assignments_final.jsonl`. Stage C2 reads `assignments_final.jsonl` and never the adjudicated
line.

**Every fleet stage is three legs, and the dispatch is not yours.** In the build leg you write the
packets and the brief and close. The dispatch leg runs outside your session: the operator's dispatch, a script with no model of its own (your platform file names it), sends each packet to fresh readers:
the routine reader model on the platform's reader route, or, for the reviewers of C2 and C5, the reviewer model,
each in a session of its own, records the model that
served in `arm.json`, validates each return against the return specification, reissues a failed
return to a fresh reader id, collects the returns into `_fleet_raw/`, and closes; you are not
running, and no model reads a return before you do. In the check leg you are relaunched
and told one thing, that the readers left their files in `_fleet_raw/`, and you validate, score
and adjudicate. It is how every fleet in v38 runs: B2, B3,
B4's blind sample, D2's verdict fleet. Your platform file names the routine and reviewer models. No reader runs in your
session.

**What every fleet stage has.** One return specification, `RETURN-NN.md`, frozen with the stage
file; the packet builder emits it verbatim, the brief cites it, and the validator's schema is
generated from it. A packet ceiling of 50 KB, asserted in `packets.py`, with an end marker and one
line telling the reader to confirm it reached it. A room whose material exceeds the ceiling is served in parts to the same reader in one conversation, never split across readers (stage B3 §1.2). Answer keys outside the readers' directory.
When reissues are exhausted: stop, diagnose, rebuild the packets. A return line keyed on packet
heading and cell number. The serving arm declared on both sides of any cross-stage comparison.
Cells used for a brief's worked examples leave fidelity and transmission.

## 2. The figures, one definition each

| figure | what it is | denominator |
|---|---|---|
| **fidelity** | how often a reader holding only the frozen instrument lands where you did in `author_items` | your own answered items |
| **agreement** | how often the `R` readers of one item agree with each other; reported with Krippendorff's alpha on the overlap, with Jaccard distance between placement sets as the metric where rule 0 allowed more than one | items run at `R > 1` |
| **gold fidelity** | fidelity on gold items seeded unannounced into live batches | seeded gold returned |
| **transmission after revision** | how often fresh readers holding only the revised instrument reproduce the adjudicated line, which is your own line; not reliability in the intercoder sense, and never called that | the blind sample at B4 |
| **stability** | agreement of the same reader arm with itself on the gold set under two rewordings of the brief, measured once in the pilot | the gold set |
| **position curve** | the outcome against position within batch, the drift check | items by position |
| **transmission** | whether the written instrument carries your judgement: agree with each other and with you; split and you were confident (fails to transmit; step 4 repairs); split and you were unsure (the instrument does not decide this item; never revised away); agree with each other and not with you (teaches something unintended) | the gold and pilot items |

**Fidelity is primary and agreement secondary.** **What these figures license**: readers share an
architecture with you or with each other, so they bound whether the written instrument decides,
never whether it is right. Say so wherever a figure appears.

## 3. The return, stages D1 to D3

Before the run, every room's coder documents were copied into the package. At D1 you write the
handoff folder: the return specification, one task per room (the room's coder documents, the
model as prose with ids, the ladder from quote to dimension for the elements the room's themes
were placed under, the id vocabulary, the two outputs), and the handler's brief. The adaptation
handler runs the labelers outside the run, in Codex, by resuming each room's verified original case-lead store (the yard's `_lead_sessions`), and returns
`model-D.md` and `adaptations.jsonl` into `DROPS/D/<sub>/`; `ingest.py` validates every line
(schema, model version, node ids, concept ids not retracted, one-sentence `how`, portability,
end marker) and compiles the ledger. The verdict comes from a separate fleet on the cheap arm,
holding the model, the room's second-order themes and the concepts the model did not use, and
none of the coder's prose (no `case.md`, no theme notes); the
labeler's own grade is reported beside it and never in its place. At D3 you adjudicate by
element, never as a list; corrections aligning in two rooms require a recorded shared-branch or scope decision in the
same leg; substantive alignment, not the count, warrants a revision; a `propose` line you accept becomes an element and the model is rewritten, and a
few of the rooms whose evidence produced the change are sent back through the labeler against
the revised model. **The verdict's criterion.** This diagnoses the fixed global model before local adaptations,
not the adequacy of the adapted room model or final cluster. This is an in-sample return: the model was built from these rooms,
so a theme's placement alone is never evidence that the room composes. The verdict fleet answers,
per room, from the model, the room's second-order themes with their placements, and the room's
first-order concepts the model did not use (the concepts of themes placed nowhere, and a seeded
sample of those no element cites): `composes` when the room's organizing can be restated in the
model's terms and none of the unused concepts shows organizing the model lacks or contradicts;
`composes-with-residue` when the restatement stands but named unused concepts or themes carry
organizing the model lacks, and the residue is listed; `does-not-compose` when an unused concept
contradicts a standing element or arrow the room bears on, or the restatement fails;
`cannot-tell` when the available evidence cannot decide the claim. Concept counts and off-platform
pointers are review prompts, not sufficient or exhaustive rules. `cannot_tell_under` names
`coded-share`, `off-platform`, `both`, `missing-decisive-evidence`, `conflicting-evidence` or
`other-evidence-limit`; the sentence states the decisive gap or conflict. The reader writes
the verdict, the themes and concepts it rests on, and that sentence.
`RETURN-D.md` carries this text verbatim.

**The scheme in packets.** A stage B2 or B3 reader never holds the whole scheme: `packets.py`
serves an index page of the families and one page per family, and a batch's second-order themes
with their sibling block, under the 50 KB ceiling, as v37 did.

The schema is `SCHEMA-adaptations.md`; the operations, the lift through the
ladder and the distance are there and not repeated here.







