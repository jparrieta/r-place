## D6a-09: corrections after the interview (J's rulings, 27 October, 09:27 Berlin)

**The close-check report of D6b, at the interview cut** (`_analysis/d6b_validate_D6_final.txt`): 0 errors, 0 warnings; fractal lines 50, branches placed 35 of 35.

**J's rulings, through the handler (the PI's message of 08:27 UTC).** This leg was added after D6b and replaces nothing. It corrects the telling's wording and records what is owed, and it changes no data file. The interview's answers themselves are not in the folder: `out/interview/` holds my brief under a new name and no transcript. So I worked from J's summary of answers 3 and 4 and recomputed every count by script.

### What this leg did, ruling by ruling

- **1a, the wording.** "Specifies without contradicting" and its kin are replaced in the frame (`retelling-D6-parts/D01.md`), part 2 (`D6b-telling.md`, rewritten whole), `handback-D6.md` (rewritten whole) and the figure's opening paragraph. The figure was redrawn by its script, with the drawing and the tables unchanged, checked in Python. The new wording:
  - No form replaces an element.
  - Replace was nearly unreachable: the readers returned 11 contradict lines among 42,243 at the first return and 4 among 53,493 at the re-check (`adaptations.jsonl`, `adaptations-recheck.jsonl`), and none stands among the forms' selected lines.
  - Of each form's restrict lines on arrows, D5's sort finds that the arrow fails in the room in A 201 of 432, B 135 of 292, C 172 of 301, D 171 of 316, E 130 of 304 and F 72 of 114. That is 43 to 63 per cent, as J's summary of answer 4 said; the shares count the lines sorted as fails alone, not those sorted as both.
- **1b, the sensitivity section.** It is written by `_analysis/d6a09_sensitivity.py --md` to `retelling-D6-parts/D6a09-sensitivity.md` and assembled after part 2. The marks are in `out/form-cells-sensitivity-D6.tsv`, from the same script.
  - The base run (ratio 1.2, floor 10 per cent) gives back all 396 written relations.
  - Changed cells by ratio 1.0 to 1.5: 99 to 27 at the 10 per cent floor, 67 to 20 at 15 per cent.
  - Of the 72 changed cells, 20 are marked "robust" (they keep their relation at ratio 1.5 and floor 15 per cent) and 52 "marginal": A 0 of 11, B 2 of 7, C 1 of 10, D 6 of 17, E 4 of 13, F 7 of 14.
  - In the prose, "robust" appears only as J's name for the mark, in quotes, because the prose check counts it as a watch word.
- **1c, local validation.** The frame now says that it is not established, and that every room named as showing a pattern shows it in its ruled lines, not in a validated account. Part 2's opening and the handback say the same.
- **1d, the branch-naming rule.** `departures.jsonl` line 21 is dated 2026-10-27 and applies backwards to every branch line from D6a-01; no line changes. `_analysis/d6a09_branch_rule_check.py` reads each line.
  - 38 of the 50 stand on the rule as stated (the key's element is the cell's).
  - 12 stand on the widened readings: key theme 1, arrow end 5, antecedent theme 2, and the branch's own words of change 4.
  - 7 of the 12 were written before D6a-04: F11 and F12 at P01 in D; F35 at A12 in E; F07 at P02 and at A11 in C; F33 at A11 in C; F08 at P05 in F.
  - The four J named all stand. F08 at P05 in F rests on its change's words, at 1.51 and 2 of 7 holders, the weakest. F35 at A12 in E is an arrow end below the form's lean. F11 and F12 at P01 in D rest on their change's words, at 2.62 and 2.69 and 3 of 16 holders.
- **1e, form B.** It is told as a residual grouping with three facets, counted by the lines' fourth-order themes (`_analysis/d6a09_b_facets.py`, which reproduces the account's 49, 48 and 40 and its 20 rooms with none).
  - 43 of its 113 defining rooms lie nearer another form's centre, the most of any form.
  - Its lead after the close is restated as a property of the chat and script rooms: 26 of its 35 after-close rooms hold the chat or the scripts (26 of 78), against 3 of the 15 raid-only rooms.
- **2 to 5, what is owed.** These are recorded in part 2 ("What is owed") and in the handback:
  - the size-held test, at D6a-10;
  - prior.md section 3's element-reach half, at E1;
  - defects 100 and 101, open, with no rewrite;
  - PR-D6-10, unvalidated and flagged for E1 against the D3a-55 ruling.

**Licences exercised at D6a-09.**
- B's facets are counted by the lines' fourth-order themes, which reproduce B's account. An element-based count gives 56, 51 and 30 and is not used.
- The "robust" and "marginal" marks follow J's definition (ratio 1.5 and floor 15 per cent), applied as "keeps its written relation".
- The figure's opening paragraph and its line on B were corrected with the telling, though the ruling names only the retelling and the handback.

**Slips at D6a-09.**
- A first count of B's facets by elements did not reproduce the account and was replaced.
- A `diff` with process substitution was refused by the sandbox, and the chain after it did not run. The comparison was redone in Python, and the figure was redrawn after it.
