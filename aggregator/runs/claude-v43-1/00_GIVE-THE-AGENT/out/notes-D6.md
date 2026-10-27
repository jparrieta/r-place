# Notes, stage D6

Target length: under 4,000 words. One section per leg. Each item that `notes-D5.md` left for this stage is answered here: acted on (as an unvalidated proposal, since `amendments-D6.jsonl` stays empty), declined with a reason, or sent to the dimension leg where its element falls, and then answered there. The close-check report of each leg is pasted at the opening of the next leg's section, because `done.sh` closes the leg.

## D6a-01: the names, the rule, D01 (Critical mass)

**How the stage is read.** On J's word through the PI (message of 27 October, 03:28 UTC): the forms are the six room forms of D4a-08c, the 35 branches are the level below, and `fractal-D6.jsonl` has one line per element and room form, with a branch only where it explains the form. The line's field `branch` holds the form's letter; `branches` names any D4 branch that explains it.

**The final names (J, 27 October 00:43 Berlin).** Written to `room-forms-names.md` and logged as moves 314 to 319 (contrasting), one per form, each with a `tier_history` line and a snap. A, Border terms and the announced plan; B, Behind the thread: chat, scripts, raids; C, The design reopened; D, Keeping, with help or carrying on; E, The sub's play, run as work; F, Moving for the spot. Below D, the splits the account kept: D.1, Keeping with the call; D.2, Keeping inside the sub's play; D.2.1, The play, carried on; D.2.2, The play, kept.

**The rule for each fractal line** is logged in the diary before it ran and stated at the head of `retelling-D6.md` (`_analysis/d6_fractal.py`). Its floor is proportional, max(5, a tenth of the form's defining rooms), so that form F is read at all. An element without a dimension (P15) and the arrow that ends at it (A12) are read with D01, the dimension of the call they answer.

### Answers to the room-form notes (D5a-36 to D5a-41)

- **D's renaming proposal (D5a-39, *or* for *and*).** Taken up in D's final name (move 317).
- **C's and E's sharpenings (D5a-38, D5a-40).** Carried into their final names (moves 316, 318).
- **Subform candidates A.2, B.2 and B.1.2 (D5a-36, D5a-37).** Declined as subforms: the split rule did not read their splits. They are listed in `room-forms-names.md` as candidates named, not kept.
- **D.1, D.2, D.2.1 and D.2.2 (D5a-39).** Named (move 317); not cut. The D4 tree stays as it is, and a cut would be a new structural claim; the telling at D6b uses them as named parts of D.
- **E.2 and E.1.2 (D5a-40).** Declined: the account called them descriptions, not candidates.
- **D.2 beside E (D5a-39, D5a-40).** Accepted: D.2 is a part of D (`room-forms-names.md`).
- **The return from carrying on to the call (D5a-39) and from the move to building and the call (D5a-41).** Acted on: PR-D6-01, the call returns.
- **To their dimension legs:** A's candidate reading (terms and plans that bind only the placers they reach; D04); D's A13, help from surplus (D04); F's A10, the cause of the move, and A04, border talk before keeping (D04); C's P05 telling clause met by disagreement (D03) and A11 (D02); E's play held only as a key, and F01 with E restating each other in part (D06); the share where the record cannot show an arrow, highest in E (D6b, the telling).

### Answers to the branch notes that touch D01

- **F32 (D5a-32), A02: a proposal that is itself the call.** Acted on: PR-D6-03. Forms D and E restrict A02 at the rule's lean, and their lines say that the start and the first call share one post.
- **F35 (D5a-35), P15 and A12: an answer that asks for a task.** Acted on: PR-D6-02. Form F restricts A12 at the lean; F35's 18 members show the same exchange.
- **F34 (D5a-34), a link from K02 to P02.** To D02, where P02 is read: F34 leans to form C (11 of its 22 rooms), and C's P02 lines include designs sized to the hands.
- **F16 (D5a-16), the chat theme holding phone-placing instructions that fit P24.** To D02, where the chat (P23) is read. P24 is untouched as a change in all six forms.
- **F21 (D5a-21), r/osu: a link from K01 to P01 and P23.** To D06, where K01 is read.

The other branch notes (D5a-01 to D5a-35, D5b) are answered in the dimension legs where their elements fall, and listed in each leg's section.

### D01 in brief

42 lines, 7 leaning cells, 35 untouched. Three forms specify the call (C, D, F), each by making it return later in the work; D and E restrict A02; F restricts A12; B restricts P32. Three unvalidated proposals: PR-D6-01, PR-D6-02, PR-D6-03.

**Licences exercised at D6a-01.** The PI's reading of the stage file; the final names as categorization moves (314 to 319, contrasting); the proportional floor; P15 and A12 read with D01; the how sentences of leaning cells written by me after reading the deciding lines, the untouched cells' sentences generated with counts.

**The close, and QD6-001.** `validate.py D6` at this leg's end gave 110 errors in 6 shapes (`_analysis/d6a01_validate_D6.txt`): every fractal line's branch field holds a form's letter, which the check refuses (42); the figure and the handback are not written; no branch has a fractal line yet (35) and the retelling names 30 of them nowhere yet. The check treats the presence of `retelling-D6.md` as the last leg. The form-level lines follow the PI's message; the conflict is asked as QD6-001 and recorded as `departures.jsonl` line 19. Meanwhile the per-dimension legs close at their safe stops with `done.sh D6 --pause`, the work half done by design, and D6b places and names every branch.
