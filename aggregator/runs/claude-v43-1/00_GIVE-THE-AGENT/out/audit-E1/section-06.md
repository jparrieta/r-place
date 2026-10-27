# Audit, section 2: the ledgers, the stories, what a reader was given (E1b-06)

Written at E1b-06, 27 October 2026. This part covers stage E1 section 2. Its script is `audit-E1/ledgers_stories.py`, with its rule in its docstring and its output beside it. The readings by hand are logged in the diary.

## 1. The ledgers, complete

**`findings.jsonl`.**
- 45 lines over 27 findings: 32 lines say standing and 13 say bounded. By each finding's last line, 17 stand and 10 are bounded.
- **The status changes**, each the stage of the line that changed it, all from standing to bounded: F-001 at B2; F-002 and F-010 at C2; F-006 at C3; F-014 and F-018 at C5. No finding was withdrawn.
- **The warrant**, by each finding's last line: read 13, inferred 14.
- **No statable `refuted_by`:** 8 findings, F-002 to F-007, F-009 and F-012.

**Every other ledger.**
- 150 jsonl files were counted, each with its lines now. The table is in `ledgers_stories.json`.
- A hash shows whether a file moved, not which line, so "no line edited after writing" can be shown only in part: through the file's size in each snap that lists it. A size that falls shows an edit or a cut; a size that rises proves nothing.
- The append-only ledgers never shrink: the adjudications, both histories, findings, verdicts, defects, departures and asks.
- Nine files do shrink:
  - **State files rewritten by design**, whose changes the histories hold: `model/elements.jsonl` (13 times), `fourth/fourth.jsonl` (7), `dimensions.jsonl` (4), `model/arrows.jsonl` (3), `propositions.jsonl` (2) and `scheme_final.jsonl` (1).
  - **`author_items.jsonl` and `gold_items.jsonl`**, once each, at B2's pilot rerun (B2a-r3 to B2a-r3-p2), before B3 used them.
  - **`fractal-D6.jsonl`**, once, at D6a-02. Its 42 form lines moved to `fractal-forms-D6.jsonl` under departure line 20. The two were compared equal, with one correction made on its own line, and the move is declared in `notes-D6.md`.

**New kinds per hundred themes, at the census:** 197 kinds over 7,844 second-order themes, which is 2.51.

## 2. The stories

| pass | rooms | told | told with residue | not told |
|---|---|---|---|---|
| 1 | 20 | 0 | 20 | 0 |
| 2 | 32 | 14 | 18 | 0 |
| 3 | 32 | 16 | 16 | 0 |
| 4 | 32 | 11 | 21 | 0 |
| 5 | 35 | 16 | 19 | 0 |

- **Passes and rooms.** Five passes ran (`saturation.jsonl`), and the model's story rests on pass 5. Rooms read against a story: 151 in all, 67 distinct.
- **The last story.** It failed to tell no room outright, and told 19 of its 35 rooms only in part.
- **What the reading behind the stories bought.** Of the 638 rooms no story was read against, the first return gives one that does not compose. None of the 67 read against a story is among those that do not compose. Most of each group composes with residue (346 of the 638; 41 of the 67, by a single verdict).
- **Loops.** None passed the one-room test, and the model grounds no loop.
- **The account's passes.** `account_passes.jsonl` holds 15, so the account's loop ran.

## 3. What a reader was given

| the five things | held? |
|---|---|
| the data-structure view's leftmost column holds material, and one row walks from what somebody typed to a dimension | **Held.** The columns run from room, concept id and the member's words to the dimension, in one file. |
| `structure.md` explains every fourth-order theme with its question, what falls outside, and quotes carrying room, author, hour and concept id, with why the set expresses it | **Held.** Every theme has its sections and five quotes (140 `why_this_one` lines). Whether any five make one point was not read. |
| the residue explained, not listed, beside C3's remainder | **Not held.** `account.md` says the last story told 19 of its 35 rooms only in part, and lists those parts rather than explaining them. C3's remainder is 19 themes. |
| `account.md` at one to two pages | **Not held.** It is 3,326 words. |
| every quote dated and attributed | **Not held, in part.** 37 cited quotes; 34 carry an hour and 3 do not. |

**The rooms the account names, against `branches.jsonl`.** The account names 22 rooms, and 17 of them are in a branch. The five in no branch are r/TeamYellowPlace, r/aceattorney, r/anarcho_capitalism, r/cardinals and r/monsterhunter. r/monsterhunter is the account's room for the return's claim.

## 4. The departures, the defects, the forks, rule 9

**The departures**, 21 lines (A1 9, D4 7, D5 2, D6 3).
- **Cost.** Three state what following the provision would have cost, in their own field. **Eighteen do not.**
- **Acted on before written: two.**
  - Line 5, A1's reading route, says it was logged late, at A1c.
  - Line 21, D6's widened branch-naming rule, was in use from D6a-02, before it was stated at D6a-04 and written at D6a-09 under J's ruling 1d.
- Both are defects.

**The defects**, 119 lines in `defects.jsonl` (A1 8, B3 55, D5 38, E1 18). They were sorted by a keyword rule, and the E1 lines by my own labels.
- **The material's:** A1 6, D5 9, E1 2. These concern the store, the packages and the coders' case accounts.
- **The instrument's:** the rest. Among them are the B3 fleet's record slips, the D5 lines on the `work_remained` field (A1's own) and E1's lines on my outputs.
- **One E1 line is provenance:** J's reading rule.
- **Still open from D5:** lines 100 and 101.

**The forks.** No comparison file arrived (`fork_comparison-C2.json` and `fork_comparison-D.json` are absent). So the spread of the fourth-order partition across forks at C2, and of the verdicts at D2, is **none**: there is nothing to compare.

**Rule 9.**
- **What was handed over:** the field's model handed over P21, P22 and A21 at C4a (`origin: from-field`). None of the three was in the model before.
- **Replicated, not discovered:** D3 ruled each standing, shown in the rooms' own lines, so they are reported as replicated.
- **Nothing else:** no other finding about the corpus was handed over by a stage file or the operator. J's words on national content and on reading are instructions, not findings.
- **Still to come:** `EXPECTATIONS.jsonl`, the operator's sealed expectations, is scored in the next section.

## 5. Defects named at this leg

Three lines were appended to `defects.jsonl` (lines 117 to 119, stage E1, leg E1b-06), all the instrument's:
- the account as a reader was given it;
- the 18 departures with no stated cost;
- the two departures acted on before they were written.

## What this part cannot say

- Whether any line of an append-only ledger was edited in place without changing its size, or with a larger replacement. A hash or a size cannot show it.
- Whether any of `structure.md`'s fourth-order themes is given five quotes that make one point.
- What following each of the 18 uncosted departures would have cost.
