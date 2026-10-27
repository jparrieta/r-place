# Audit, section 1, part 3: the moves, provenance, the manifest and the figures (E1b-03)

Written at E1b-03, 27 October 2026. This part covers four items of stage E1 section 1:
- the moves;
- the provenance of D6's proposals, with PR-D6-10 against the ruling of D3a-55, and the extra legs D6a-09 to D6a-18;
- the manifest, whole;
- the fleet's figures, restated with their definitions.

Every figure comes from a script in `audit-E1/` with its output beside it, or from a reading by hand that the diary logs. The new script is `provenance_D6.py`. E1a's `moves.py`, `manifest.py` and `fleet_figures.py` are read here.

## 1. The moves

**`tier_history.jsonl`, 1,026 lines, by stage and tier.**

| stage | third order | fourth order | dimension | the tree |
|---|---|---|---|---|
| B1 | 252 | | | |
| B2 | 140 | | | |
| C1 | 1 | 28 | | |
| C2 | 6 | 40 | 9 | |
| C3 | | 2 | | |
| C4 | | 2 | | |
| C5 | 2 | 61 | 18 | |
| D4 | | | | 459 (branch 35, cross-link 348, room form 43, room sub-form 33) |
| D6 | | | | 6 (room form, final names) |

By move, the tier history uses seven of Grodal, Anteby and Holm's eight moves, and the run's joint label "relating or contrasting": relating 357, asking questions 255, merging 105, dropping 93, relating or contrasting 76, developing or dropping working hypotheses 76, splitting 58, contrasting 6. "Focusing on puzzles" is never named.

**`model/history.jsonl`, 182 lines.** By stage: C2 82, C3 3, C4 3, C5 46, D3 38, D4 10. Two names are not among the eight:
- **"Stabilizing"**: 2 lines at D3. An appended D3 line corrects move 174's name to developing working hypotheses.
- **"Sequencing"**: 18 lines at C2a-01 to C2a-03, where arrows were added. No line or note declares or corrects the name. This is a defect of naming. Each of these moves has its snap, so the provenance stands.

**Recuts after C5.**
- No third-order, fourth-order or dimension line was written after C5. The D4 and D6 lines of the tier history are the tree's: the branches, the cross-links and the room forms.
- The model history holds 48 lines after C5: 38 at D3 and 10 at D4. All 48 name a D3 cause: return lines, the re-check, or the lines they correct.
- Two of the 48 carry the held-proposal mark (P05 and A11, moves 198 and 199), and two are the reverts (move 203, J's QD4-001).
- So every model change after C5 is either a rule 11 amendment with its D3 cause or a held proposal.

**The move snaps against the diary's move lines.** From C2, a claim with no provenance is a defect.

| stage | diary move lines | move snaps | how compared |
|---|---|---|---|
| C2 | 47 | 47 | by count (the diary's lines carry no number) |
| C3 | 3 | 3 | by count |
| C4 | 2 | 2 | by count |
| C5 | 119 | 119 | by count |
| D3 | 27 (26 numbered) | 27 | by number: no numbered line lacks its snap; the one snap with no line is the duplicate `D3-move-181-1`, declared at D3a-53 |
| D4 | 116 | 116 | by number, one to one (moves 198 to 313) |
| D6 | 6 | 6 | by number, one to one (moves 314 to 319) |

Before C2 the snaps are numbered per move name, so they are counted only. B1 has 6 lines and 6 snaps. C1 has 214 diary move lines against 29 snaps. The 29 are the 28 fourth-order cuts and one moved theme, and they match C1's 29 tier-history lines. The other 185 lines all begin "reassigned": each moves one room's second-order theme from one placement to another.

## 2. D6's proposals and the legs D6a-09 to D6a-18

**The eleven proposals** (`proposals-D6.jsonl`, `provenance_D6.py`). All 11 are `unvalidated` on base `46384686d617…`, the D3 freeze, and `amendments-D6.jsonl` holds 0 lines.
- **Evidence.** The proposals name 254 concept ids, and all are in the store. They name 61 other items (fractal lines, files, room lists and one finding, F-026, which exists), and none fails to resolve.
- **Record.** Each proposal has at least one diary line at the leg that wrote it, D6a-01 to D6a-07.
- **Provenance.** No proposal lacks it.

**PR-D6-10 against D3a-55.** Rule G59, written in `notes-D3.md` at D3a-55 before any propose line was read (lines 1464 and 1475), put "the subs' own April Fools pranks, styling and games (T4-001's themes)" outside the model's scope, as particulars. PR-D6-10 proposes a process element under Host framing: the sub administers its play. Its `change` field says that it "would bring into the model what the ruling of D3a-55 put outside its scope", and it leaves "whether the scope is widened" to a later model. So the proposal names the ruling it would reverse, and it changes nothing: it is a proposal, not an amendment. Its evidence holds 89 concept ids, all in the store.

**The extra legs D6a-09 to D6a-18** (the form telling, its second round and the Dutch telling). Between the close of D6a-08 and the close of D6a-18:
- **Unchanged:** the model, its history, the tiers, the scheme, the assignments, the branches, the cross-links, the return's ledgers, the verdicts, the findings, the propositions, the proposals, the amendments, the fractal lines, the room forms, the defects and the account.
- **Changed:** `departures.jsonl` gained line 21 at D6a-09. Under J's ruling 1d, it records as a dated amendment a widening of D6's branch-naming rule, and it says the amendment applies backwards. The amendment states that the widened readings were in use from D6a-02, before they were written down at D6a-04. That makes it a provision acted on before it was written, and it is reported in the departures section (part 6). No branch line was rewritten.
- **Added:** `retelling-D6.md` was written at D6b, between the two closes.

## 3. The manifest, whole

`run_manifest.json` holds 19 entries, for stages A1, B2, B3, B4, C2, C5 and D2, and each names a model, seeds and decoding. These fleet figures have complete provenance:

| file | entries |
|---|---|
| `stability-B2.md` | 8 |
| `fidelity-B3.md` | 2 |
| `position-B3.md` | 2 |
| `transmission-B4.md` | 5 |
| `transmission-after-revision-B4.md` | 5 |
| `review-C2.md` | 1 |
| `account-readers-C5.md` | 1 |
| `verdicts-D.jsonl` | 1 |

**Missing:** the D3 re-check return (`adaptations-recheck.jsonl` and each room's `verdict-D-recheck.jsonl`) has no entry. Each room's `run-recheck.json` names the readers' model (gpt-6.1-sol) and a session, but no seed and no decoding. The re-check's figures, among them the verdicts of all 705 rooms at the re-check, therefore have partial provenance. The analyst's own figures come from scripts in `out/_analysis/` and `audit-E1/`, which state their seeds. The analyst's model and effort per stage are set in `arm.json`, not in the manifest.

## 4. The figures restated

FLEET.md section 2 defines each figure, and says what all of them license: "readers share an architecture with you or with each other, so they bound whether the written instrument decides, never whether it is right." Readers in fresh contexts are instances of one model, not two minds. None of these figures is reliability, and none is intra-rater. No file of the run calls any of them either; the one passage near those words, in `notes-B3.md` line 11, discusses what a second reader per item would have bought.

| figure | FLEET.md section 2's definition | the run's value | where |
|---|---|---|---|
| fidelity | how often a reader holding only the frozen instrument lands where I did | gold fidelity 0.624 at B2; 0.645 at B3 (the whole fleet); corpus readings of gold items 0.683 | `pilot_report.md`, `fidelity-B3.md` |
| agreement | how often the readers of one item agree with each other, with Krippendorff's alpha, and Jaccard where rule 0 allowed more than one theme | B2: 0.800 and 0.756 inside the two stability rounds, 0.818 inside gold, alpha 0.784 (six readers) and 0.794 (nine); B3 corpus: 0.786, alpha 0.782 | `stability-B2.md`, `handback-B3.md` |
| gold fidelity | fidelity on gold items seeded unannounced into live batches | 0.645 at B3; its fall against B2 on the same items, -0.014 (interval -0.031 to 0.003), sits inside the floor of 0.193 | `fidelity-B3.md` |
| stability | the same reader arm agreeing with itself on the gold set under two rewordings of the brief | 0.807 (B2) | `stability-B2.md` |
| transmission | whether the written instrument carries my judgement, decomposed over items where my answer is on record (40 gold, 50 pilot) | the scheme decides 21 and 30; fails to transmit 1 and 0; the instrument does not decide 6 and 12; teaches something unintended 12 and 8 | `transmission-B4.md` |
| transmission after revision | how often fresh readers holding only the revised instrument reproduce the adjudicated line, which is my own line | arm 1's two readers agree at 0.781 on the uniform stratum, under the floor of 0.807; arm 1 disagrees with the settled line on 0.742 of readings of contested items and 0.400 of unanimous ones | `transmission-after-revision-B4.md` |
| position curve | the outcome against position within the batch | agreement +0.003 over 14 positions (interval -0.015 to +0.022; the fit would catch 0.027); the arguable rate rises +0.040 | `position-B3.md` |
| the verdict fleet's disagreement rate | how often the D2 readers' verdicts differ | 163 of 705 rooms with two readers (0.2312) | `verdicts-D.jsonl` first return (`fleet_figures.py`) |

## 5. Defects named at this leg

Two lines were appended to `defects.jsonl` (lines 112 and 113, stage E1, leg E1b-03), both the instrument's:
- the 18 C2 model-history lines named "sequencing";
- the D3 re-check return with no manifest entry.

No earlier file is changed.

## What this part cannot say

- Whether each of C1's 185 reassignments matches its line in the assignments ledger. They are counted by their first word, not read one by one.
- The seed and decoding of the D3 re-check readers.
- Whether the earlier lines of `proposals-D6.jsonl` stayed as written while the file grew (part 2 of this section).
