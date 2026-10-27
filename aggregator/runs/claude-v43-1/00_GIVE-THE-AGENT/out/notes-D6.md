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

## D6a-02: the restructure (QD6-001), D02 (Coordination without command)

**The close-check report of D6a-01** (`_closes/` holds no report for a pause close; `_analysis/d6a01_validate_D6.txt`): 110 errors in 6 shapes, as above, the sixth being the missing trusted tree hash (below).

**QD6-001 answered (option c, the handler's view on J's instruction; J has not seen it), with the PI's message of 03:57 UTC.** Done as one amendment, `departures.jsonl` line 20, citing J's 18:01 ruling and applying backwards to D6a-01's outputs; line 19 stays. The 42 form lines moved to `fractal-forms-D6.jsonl` (letter in `form`; content compared equal), with one correction on its line: P01|F no longer names F09, because of F09's rooms in F only r/penguins links the call, and not to a move. `fractal-D6.jsonl` holds branch lines only (16 after this leg). `retelling-D6.md` was moved to `retelling-D6-parts/D01.md`, and D02's section is `retelling-D6-parts/D02.md`; D6b assembles `retelling-D6.md`.

**QD6-002 asked.** After the restructure `validate.py D6` gives one error: "D4 tree has no matching trusted closure hash", because `_closes/tree-D4.sha256` was never written (only the checks' test fixtures write it). The tree has not moved: `branches.jsonl` and `crosslinks.jsonl` match the D4a-08 close snap, and `subforms.jsonl` is absent then and now. I do not write a trusted hash myself. Until the answer, a leg whose only refusal is this file closes with `done.sh D6 --pause`.

### Answers to the branch notes that touch D02

- **Branch renaming proposals (F07, F15, F16, F24, F30).** Declined as amendments: the D4 tree is frozen at D6 (`tree_moved`), and a branch's name is part of it. The proposed names stay in `defects.jsonl` for E1, and the retelling describes each branch by what its rooms do.
- **F09 (D5a-09), the arrow from P10 to P03.** Acted on: PR-D6-04. Form F specifies P03 by link lines, and 8 of the 12 holders are F09's rooms.
- **F34 (D5a-34), a link from K02 to P02** (sent here at D6a-01). Acted on: PR-D6-05, from F34's rooms holding P02 lines in forms C (4) and E (5).
- **F15 (D5a-15), the plan follows the work.** Borne out at the form level, without a proposal: form A specifies P04 by add-steps that correct the template against the placements, and 20 of the 32 holders are F15's rooms. It lies inside P04's statement.
- **F15 and F33 (D5a-33), one change at two nodes.** At the form level they fall in different forms, F15 in A and F33 in C, so the coders' placement of the template talk follows the form's lean. No change.
- **F15, F29 and the held A11 proposal (D5a-15, D5a-29).** Noted beside the held proposal, which stays held (QD4-001); form C restricts A11, with 40 of 58 lines failing as stated.
- **F16, F29 and F30 (D5a-16, D5a-29, D5a-30), the chat family.** Read together, as asked: form B holds F16 and F29 at its P23 specification, A specifies P23's upkeep, and E restricts it. One change at P23 with three ops; no amendment.
- **F16, P24 in the coders' chat theme** (sent here at D6a-01). P24 is untouched as a change in every form, and E's restricting P23 line from r/pcmasterrace says the same: interface instructions in a chat-labelled theme are teaching. A coding note for E1, no change.
- **F16, entry control; P33 not coded for it.** No form changes P33. The reading stays a reading.
- **F24 (D5a-24), P14's two evidence states.** Declined as a change: the form lines already keep them apart (A and D restrict P14 where scripts are offered and not shown placing; B, E and F specify it where machines are run).
- **F24, a norm of means without enforcement; F24 and F30, restrict-keyed branches.** For D07 and E1: the first is a remainder the telling names, the second a coding pattern for E1.
- **F07, F08 and F15 (D5a-07, D5a-08, D5a-15), P05's telling clause** (F-025, the machine form, the clause carried through the plan). To D03, where P05 is read.
- **F16 (D5a-16), host containment and the move to a chat (P20 to P23).** To D06, where P20 is read.

### D02 in brief

78 form lines (21 leaning, 57 untouched) and 13 branch lines; 197 evidence codes resolve. Each form specifies the part of coordination its name says; D only restricts here (A01, A06, P14). Two unvalidated proposals: PR-D6-04, PR-D6-05.

**Slips at D6a-02.** Two Edits to `_analysis/d6a02_move_form_lines.py` in one turn; a stray `open('/dev/stdout','w')` in a check command, which raised an error and wrote nothing; one Python read of `notes-D5.md` refused by the guard, redone with `grep`.

**Licences exercised at D6a-02.** QD6-001's shape; the correction to P01|F recorded on its line; a branch named as explaining a cell only where it leans to the form and its own key matches the cell (chosen from a script's candidates); the renamings declined because the tree is frozen.

## D6a-03: QD6-002 answered, D03 (Maintenance)

**The close-check report of D6a-02** (`_analysis/d6a02_validate_D6.txt`): 1 error, 1 warning. The error was the missing trusted tree hash; the warning, that `retelling-D6.md` is not written yet, is expected until D6b.

**QD6-002, answered by J's ruling** (27 October, 06:33 Berlin, through the PI's message of 05:34 UTC): "The file should be the last cut we did. Prepare a file like the one it needs and give it the authority it needs for the run to continue." The handler wrote `_closes/tree-D4.sha256` with the tree hash at D4a-08's close (0499928b..., the value I had checked). The answer recorded in `asks.jsonl` is the handler's earlier view (do not write it; keep pausing); J's ruling supersedes it, and I record the ruling as QD6-002's answer here and in the diary. From this leg the dimension legs close with `done.sh D6`.

### Answers to the branch and form notes that touch D03

- **F07, F26 and F27 (D5a-07, D5a-26, D5a-27): read F-024 to F-027 together, beside the held P05 proposal, before any change to P05.** Done at the form level (`retelling-D6-parts/D03.md`). Four ways the clause holds only in part are seen in the forms: refusal by informed keepers (C; r/de in A), the border (D04), the script's target (F; F08) and the check before repair (D). No form's lines show a planned change lost only for want of telling. P05 is not amended (the model is frozen), and the held proposal stays held.
- **F27 (D5a-27), a step the room models propose: checking whether a change is intended before undoing it.** Acted on: PR-D6-06, the check before repair, from D's P05 add-steps (five rooms) and one link line in A.
- **F08 (D5a-08), a machine form of the telling clause.** Seen in form F's keeping (r/wildhockey's repair tool) and carried in PR-D6-06's text as a route; no separate proposal, since F-027 already states it.
- **F15 (D5a-15), the telling clause carried through the plan.** Seen in form A's P04 add-steps (D02: helpers ask for warnings on obsolete templates so that repair does not undo the plan). No separate proposal; it is the template route of F-024's scope.
- **C's note (D5a-38), P05's telling clause meets disagreement.** Borne out at the form level: C restricts P05 (46 of 96), and F07 explains it.
- **F32 (D5a-32), the marking returns to keeping.** Form A specifies P05 by link lines, and 9 of F32's rooms hold them; a return from the marking (P11) to keeping (P05) that the model's arrows do not state, read in the telling at D6b beside PR-D6-01 and PR-D6-04.

### D03 in brief

18 form lines (4 leaning: P05 in A, C, D and F; 14 untouched) and 4 branch lines (F07, F27, F32, F08); 62 evidence codes resolve. One unvalidated proposal: PR-D6-06 (proposals now 6).

**Slip at D6a-03.** A `cut -c` after `mem.py diary` at the opening, refused by the guard (J's rule on whole reads); redone without it.

**Licences exercised at D6a-03.** J's ruling recorded as QD6-002's answer; F26 dropped from A's P05 cell after its two rooms' lines were read (they do not concern the border); F27's sentence limited to the two rooms of four that check before repair.

## D6a-04: D04 (Order without law)

**The close-check report of D6a-03** (`_analysis/d6a03_validate_D6.txt`): 0 errors, 1 warning; fractal lines 20, branches placed 14 of 35. The warning, that `retelling-D6.md` is not written yet, is expected until D6b. The leg closed normally with `done.sh D6`. Correction of record: the head was 2,998 words at that close, not 2,997 as its closing diary line said.

### Answers to the branch and form notes that touch D04

- **A's note (D5a-36), terms and plans that bind only the placers they reach.** Borne out at A05 in A, B and D, and carried as PR-D6-07, a bound on A05 (24 rooms; F26 explains A's cell, F08 B's).
- **F26 (D5a-26), A05 as P05's telling clause stated on P07; F-026.** F26 explains A's A05 cell (6 rooms). PR-D6-07 states F-026's border half on A05. The renaming is declined: the tree is frozen.
- **F10 (D5a-10), the telling problem between rooms.** F10 explains A's P08 cell (14 rooms), and relaying the terms to placers is one of its steps (r/poland, r/transformers). It is carried in PR-D6-07. r/buffalobills's limit stands: the record does not show whether the placers who pushed past its deal had heard of it. The renaming is declined.
- **F22 and F28 (D5a-22, D5a-28), P16's order of tasks: the helper's own work first.** Borne out in D (F22: 11 rooms at P16, 3 at A13) and in A (F28: 10 rooms at P16, where the form as a whole leaves P16 untouched). Carried as PR-D6-08, a condition on P16 and a bound on A13. F22 and F28 share no room and fall in different forms, D and A, as the D5 note expected of one change split by where the coders lifted the line. The renamings are declined.
- **F22 (D5a-22), recognising the form, in help and in keeping.** r/OnePiece's P16 line in D says accurate aid needs the allied image. With PR-D6-06 (the check before repair) and PR-D6-07 (the terms reach the placers) it makes one thread: a placer acts on the form or the terms only where they reach it. For the telling at D6b; no separate proposal.
- **F31 (D5a-31), read the hosts' records beside the guests'.** Done for the two hosts the note names. r/greenlattice (form A) holds applications, an approved-project document and no-build diagrams, and hosting contested by a proposal to purge guest work. r/thebluecorner (form B) holds guest permission reversed by a vote or a purity demand. Neither is an F31 member. The host's rule is in the record where the room is the host, so F31's limit is the guests' record's limit, as the note says. F31 restricts P19 in A (8 of 12 holders), and D and F restrict P19 the same way.
- **D's note (D5a-39), help from surplus (A13).** Borne out in C and D; PR-D6-08.
- **F's notes (D5a-41), the cause of the move (A10) and border talk before keeping (A04).** E and F restrict A10. P10's statement already names the loss of the spot, and F-019 agrees, so no proposal. A04 is carried as PR-D6-09: two routes into P08 before keeping, from seeking the spot and from building.
- **F27, F30 and F31 on A07 (D5a-31).** For D07, where A07 ends.

### D04 in brief

120 form lines (22 leaning, 98 untouched) and 7 branch lines (F10, F26, F28, F31, F08, and F22 twice); 134 distinct evidence codes resolve. Branches placed: 19 of 35. Three unvalidated proposals: PR-D6-07 to PR-D6-09 (proposals now 9; their 57 codes resolve).

**Licences exercised at D6a-04.** The D6a-02 rule that a branch's own key matches the cell, read as: the key's element is the cell's element or an end of the cell's arrow, or the key's theme belongs to the arrow's antecedent (F26: restrict on P05 at T3-010, settling borders with neighbours, a theme of P08). F08 at A05 in B rests on its change's own text ("a revision must reach the operator and the target file"), not on its key, as F08 at P05 in F did at D6a-03. F28 and F31 are placed at their key elements in form A, where the form line stays untouched; their branch lines give the branch's share of the form's holders. Candidates set aside after reading their lines: F10 at A14 in A (help as the terms, not the deal's work), F29 at A05 in B (one of three rooms concerns the chat), F07 at A13 in C (its change is the telling clause, not help). The proposals' rooms are my reading of the lines.

**Slips at D6a-04.** A read of `model/elements.jsonl` at the wrong path (the model is in `out/model/`), which failed and wrote nothing. The context was compacted during the leg; the head was reconciled with the diary before the next write.
