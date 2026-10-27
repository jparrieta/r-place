# Audit, sections 6 and 7: what bore the load, and what the study cannot say (E1b-08)

Written at E1b-08, 27 October 2026. The figures come from `audit-E1/load_limits.py` and `audit-E1/shelf_terms.py`, each with its output beside it, and from E1a's and the earlier legs' outputs.

## 1. Which stage was load-bearing

**By stage.**
- Every stage from A1 to D6 has outputs that a later stage names in its commands or reads:

| stage | outputs named later | outputs | stage | outputs named later | outputs |
|---|---|---|---|---|---|
| A1 | 13 | 20 | C4 | 6 | 10 |
| B1 | 15 | 25 | C5 | 13 | 74 |
| B2 | 18 | 61 | D1 | 54 | 722 |
| B3 | 11 | 1,266 | D2 | 4 | 7 |
| B4 | 10 | 146 | D3 | 4 | 23 |
| C1 | 6 | 16 | D4 | 20 | 70 |
| C2 | 15 | 37 | D5 | 11 | 48 |
| C3 | 4 | 9 | D6 | 7 | 271 |

- So every stage was load-bearing for something downstream, and no stage is the one whose output nothing read.
- The files no later stage names are mostly fleet packets, superseded copies, answers, notes and handbacks. Fleets, tools or the harness read these without naming them in a command, so this test cannot call them unread.
- By hand, some look read by nothing: `lexicon-A1.md`, `leads-outside-frame-A1.jsonl`, `ideas-B1.jsonl`, `kinds-B1.jsonl`, `form_pass-C1.md`, `gate_history.jsonl`, `within_case.md`, `sketches.md` and `author_claims.jsonl`.
- These were not checked against every tool's inputs. They are listed as candidates for a file nothing read, a defect in this instrument (`defects.jsonl` line 120, not sure).

**The three files given for this test.**
- **`tools/chunk_compare.py`.** Its sha256 now equals the receipt in `departures.jsonl` (chunk-comparison-v1.1, `c8d2eb8c7c309c02…`), and its outputs are present (`chunk-share-D4.jsonl` and `.md`, `projections-D4.jsonl`). A stranger can rerun it. I did not.
- **The data-structure view.** It moved between C2's last snap (`57f68644867d`) and C5's (`c4a4c4884570`), and it is unchanged since. `data_structure-C5.md` is present. The C5 passes, which rewrote the declarations under the prose rule, moved it.
- **`account_passes.jsonl`.** It holds 15 passes, so the account's loop ran.

**The model's tiers: do the dimensions do any work?**
- **Where they work:** the dimensions sort the elements (44 lines of `model/elements.jsonl` name one). They state the propositions' levels (14 times by name in `propositions.jsonl`). They order D6's retelling (`retelling-D6.md`, by its parts). They weigh 1.0 in D4's distance.
- **Where they do not:** they appear in no line of `branches.jsonl`, `branches-D5.jsonl` or `model/arrows.jsonl`, and nowhere in `account.md`, by id or by name.
- So the dimension tier works in the model's layout and in the retelling, but does no work in the account's argument, the arrows or the branches' keys. Read alone, it looks sound. Read with the stages, it is the tier the account never uses.

## 2. What the study cannot say, in one place

- **Absence claims marked weak:** F-015 (the rooms do not read their numbers off the replies to a call).
- **Looked for and not found**, stated as results:
  - no loop passed the one-room test;
  - A11's order never beat its null, and A12 has no order count;
  - the held-size test of the arrows, declared in `prior.md` section 3, was not run;
  - the onset contrast cannot be read, since each arrow's late side holds 0 to 15 rooms;
  - the "dear enemy" and superordinate-goal predictions were declined, because no query recovers their targets (`literature-C3.md` lines 84 and 89).
- **Relationships weaker than the rest of the model:** two arrows are theorised (A11, A12), four are thin (A05, A10, A14, A19) and two are partly constitutive (A16, A20). A21 is the one arrow no proposition rests on.
- **The coders' disagreements:** 72 lines in `coder_conflicts.jsonl`. Which reading each affected claim rests on, with both quotes, was not read line by line at this leg. That is a limit.
- **Third-order themes the model does not use:** 35 of 195 are reached by no standing element.
- **What C1's form pass found that no tier could hold**, four kinds:
  - April Fools play that stages no fake (17 lines in 15 rooms);
  - another sub's April Fools change seen from this room (8 in 8);
  - the sub's own moderation outside the canvas (8 in 7);
  - disputes over the room's own jokes (4 in 4).
- **Stage C3's remainder:** 19 themes, covering talk in 694 rooms.
- **Whether any room's problems were settled:** only the room models speak to it, and nothing measures it.
- **What a group leaves behind:** the contract's section 1 question has no measure. The canvas is what the drawing left behind, and the instrument does not know whether the room went on.

**The standing departures of this design**, beside the run's own:
- **Five tiers** rather than three.
- **The fourth-order tier cut at C1**, before the loop. B1 made 197 third-order themes, C1 kept 195 inside fourth-order themes, and C2 to C5 wrote 8 third-order tier lines, merges and splits.
- **Literature after the model.**
- **A scheme frozen at B2**, before B3 (part 2 of the audit).
- **The frame:** 705 coded rooms against a target census of 706, with no drops. `leads-outside-frame-A1.jsonl` names 2 rooms outside it.
- **The canvas held from the start**, never scored against.
- **One analyst above the assignment tier**, seen by the hostile reader at C2, the three readers at C5, the labelers and the return's readers. There were no forks, and the room notes are the one input nothing checks.
- **No human check at any tier**, beyond J's rulings.
- **No theoretical sampling.** What stood in: the census, and 67 distinct rooms read against the stories.
- **Saturation** as 5 story passes and 2.51 new kinds per hundred themes.
- **Replication as the in-sample return.**

**The critique shelf.** I read the four read-tier files after the findings were fixed: Jowsey et al. (2025) and the call for papers whole, and O'Sullivan and Ravasi (2026) and Schildt (2026) by the objections' terms with their pages.

| objection | the shelf | does this run answer it? |
|---|---|---|
| invented quotes | O'Sullivan and Ravasi, p. 16; Schildt, pp. 1, 4 | **In large part.** 3,218 of 3,230 cited quotes resolve to their concept. The handler's raw check finds every coder quote in its item, and none of the case-account strings I could check is an invention. 33 strings from uncoded items stay unchecked (part 1). |
| the reasoning handed to the machine (cognitive offloading) | Schildt, p. 1; O'Sullivan and Ravasi, p. 2 | **No.** The design hands every tier above the coders to a model, and J's rulings are the only human steer. The run shows its reasoning; it does not keep a human doing it. |
| an opaque process | O'Sullivan and Ravasi, p. 17; Schildt, p. 1 | **For the record of decisions, yes.** Every move is snapped, every diary line drawn is borne out by its transcript (905 of 905), and every script states its rule. **For the reasons inside a model's judgment, no.** |
| the craft and reflexivity a model does not have | Jowsey et al., pp. 1 and 2; O'Sullivan and Ravasi, p. 13; Schildt, p. 14 | **No.** No positioned human researcher read the rooms. The experience file will be a model's account of itself. |
| more output instead of better | the call, p. 1; Schildt, pp. 1 and 2 | **No.** The run wrote thousands of files. The audit found the account at 3,326 words, not one to two pages, and 293 handback counts unchecked. |
| harm to the environment and to data workers | Jowsey et al., p. 2 | **Not addressed.** |

**The call for papers' asks**, for section 8, without changing a finding:
- **Met in kind:** an AI-enabled research loop under human direction; qualitative theory-building with a stated test; boundary-setting work, which this audit is.
- **Partly met:** reproducibility, since scripts declare their rules, but no rerun is promised. A repository-like artifact also exists, since `out/` holds every file.
- **Not met:** ethicality, as the call frames it, is not examined.

**The one thing to say plainly.**
- **What the study produced:** a **model**, the frozen spine and its arrows, with a **typology** below it (six room forms over 35 facet branches). It set out to produce a model.
- **The strongest argument that the partition is size as form** (contract section 5): D4's volume verdict. The cluster labels explain 0.255 of the variance in log concepts, at the 100th percentile of the permutation null (null maximum 0.026). The branches lean to large rooms.
- **What answers it, in part:** D6's size-matched test, under which 62 of the forms' 72 changed cells survive. I did not locate stage D4's line-count division at this leg.
- **What would overturn the study:** the re-check composes 686 of 705 rooms (0.973). If 4 or more of a stratified sample of 30 uncoded rooms did not compose (6 or more of 60), the uncoded rooms would fall outside the coded rate at the 1 per cent level.
- **What I could not answer:**
  - whether the forms survive outside the sample;
  - the coders' disagreements, read one by one;
  - D4's line-count division;
  - the leaf, which is the reconstruction's test.

## 3. Defects named at this leg

One line was appended to `defects.jsonl` (line 120, stage E1, leg E1b-08, not sure): the files that no later stage names and that look read by nothing.
