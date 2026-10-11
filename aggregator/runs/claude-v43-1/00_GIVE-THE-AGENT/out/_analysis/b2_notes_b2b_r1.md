
## Leg B2b-r1, check round 1, 2026-10-11

### What the PI and J ruled before and during this leg

- **QB2-001** (answered 15:15Z): serve oversize items in parts to the same reader, as stage B3 serves a large room. Do not cap the hard set by size. Each part stays under the 50 KB ceiling with its end marker, and the reader answers once per item after the last part. If `packets.py` cannot part a B2 item, the splitter is a helper in `out/_analysis/`, and the parts are recorded in `MANIFEST.json` and here. Round 1 goes out as built.
- **The round-2 rule** (same message): from round 2, the ten biggest bags of `notes-B1.md` are served in parts. No round may meet a stopping rule of section 5 before those ten have been read by the round's readers at least once.
- **QB2-002** was first answered "flat", then corrected by the handler at 15:29Z. `fleet.py` reads `*.md` flat in the folder it is given, but `CONTROL/harness/dispatch.sh` gives it `out/_packets-B2/round-K/` for B2 and refuses when that folder is missing. `packets.py`'s default, `round-K/`, is the right place. J copied round 1's packets into `out/_packets-B2/round-1/` to dispatch them. Later rounds are built in `round-K/`, and earlier rounds stay where they are. The flat copy in `out/_packets-B2/` is round 1's and stays.
- **QB2-003** (answered during this leg): repairs the gate check found are recorded in `scheme_edits.jsonl` with `caused_by ["gates:T3-a|T3-b"]`. A word-for-word mirror takes kind `gate-check` and owes no recheck and no tier_history line. A new sentence takes its ordinary kind and owes both. Repair all in this leg if possible, before round 2's packets.
- **v43.2 tools** (J, "Do all changes"):
  - `mem.py blind on|off`;
  - `--width` on reads, with the guard refusing `cut -c` after `mem.py`;
  - `mem.py gates` (with `--confirm`);
  - `tools/tokens.py`;
  - rule 0's `also_present` clause for bags, on the return line from the next round;
  - `support_by_theme` on my records;
  - rechecks owed by every edit (`mem.py rechecks --owed`, `mem.py recheck`).
- **The reader settings** (J, 20:42 Berlin): from round 2 the reader preset is pinned to one provider (Relace) at medium reasoning effort. Round 1's three readers ran at high effort on mixed providers (Relace, Baidu Qianfan, Reka AI), all on the same model, deepseek/deepseek-v4-flash-0731. A change in agreement between rounds 1 and 2 is partly the reader settings, not only my edits. This goes in the round-2 manifest entry too.
- **Corrections from the B1e interview**, made on the record (`notes-B1.md` and `handback-B1.md` carry an appended correction):
  - The T3-005 and T3-021 gates contradicted each other on repair during a raid. Corrected before the pair was scored (edit below).
  - F-001's grain bound does not hold across rooms. `out/_analysis/b2_grain_check.py`: Spearman −0.08 between a room's mean concepts per theme and its single-kind share (633 rooms). Within rooms, mean Spearman 0.28 between a theme's concepts and its kinds (positive in 482 of 619 rooms). `findings.jsonl` has the superseding F-001 line, status bounded.
  - "107 episode lines" is 106 (line, kind) pairs over 81 lines (`out/_analysis/b2_episode_kinds.py`).

### The dispatch, in `fleet.py`'s counts

`out/_fleet_raw/B2/round-1/` holds four attempts.
- The first (DONE, 17:08Z) returned nothing valid. The reader model reasoned before answering and used its whole 16k output budget. The gateway's response cache then handed eight reissues the same empty reply. `EXHAUSTED.tsv` names r5, r7 and r9: no end marker. The handler then changed `fleet.py`: the reader id opens each message, readers run in parallel, the output limit is raised, and the served model is read from the reply.
- Two more attempts failed the same way while those fixes went in (r10, r11; r13 was cut off). Every `*.failed.txt` is a failed attempt, not a reading.
- The round scored is the last, `PARTIAL-2026-10-11T183640Z.json`: three valid returns of 40 lines each, r12, r15 and r16. All were served by deepseek/deepseek-v4-flash-0731 (served matches the probe).

| reader | reissue | elapsed (s) | input tokens | output tokens (thinking) | cost (USD) |
|---|---|---|---|---|---|
| r12 | 0 | 582.7 | 158,259 | 85,776 (61,498) | 0.066 |
| r15 | 1 | 1,396.4 | 286,397 | 129,100 (117,668) | 0.099 |
| r16 | 1 | 273.0 | 133,410 | 60,104 (49,156) | 0.046 |

The whole last run cost 0.369 USD, with 747,469 input and 494,282 output tokens. Each reader's usage record shows one tool call; the record does not say what it was.

### Round 1's three numbers

Scored by `out/_analysis/b2_score.py` on r12, r15 and r16 only, by the definitions declared above:
- **Fidelity** against `author_items.jsonl`: mean Jaccard 0.594. The primary matches mine in 0.742 of reader-items.
- **Pairwise agreement**: 0.733 (mean Jaccard; primary pairwise 0.767).
- **Alpha** (distance 1 − Jaccard, chance over the round's pooled sets): 0.726.
- **Disagreement**: 18 of 40 items have two readers differing.

What licenses these figures, in FLEET.md's words: readers share an architecture with me or with each other, so the figures bound whether the written instrument decides, never whether it is right. The claim they support is what I would have produced at a scale one analyst cannot reach, not what any competent reader would have produced.

By source and by my confidence:
- confusion-pair items: fidelity 0.558, pairwise 0.755;
- bags: fidelity 0.500, pairwise 0.749;
- random items: fidelity 0.705, pairwise 0.692;
- items I marked clear: fidelity 0.833; arguable: 0.560.

**The main finding is mine to own.** I placed 24 of the 40 items on two kinds. The readers placed one kind in most items: 3, 6 and 1 multi lines out of 40. In 14 items all three readers placed one theme that is among mine, so the item scores 0.5 against me while the readers agree perfectly. Rule 0 asks for a second placement only where one cannot carry the material. The readers read it more strictly than I did. Those second placements are author-errors (the rechecks below record them). The readers are not wrong.

**Stopping.** Pairwise agreement (0.733) clears the declared threshold of 0.70. Under the round-2 rule no round may stop before the ten biggest bags have been read, and this round made edits. So round 2 opens.

### What divided readers, and the verdicts

`out/_analysis/b2_r1_items.tsv` has every item.

- **Author-error** (readers right, me wrong):
  - My second kind was not needed, all three readers placing one: 4chan t07, GreenCorner t03, england t03, flashtv t13, floridagators t09, harrypotter t08, kpop t04, megaman t11, redhotchilipeppers t09, furry t10 and nyu t01 (T3-004 never chosen), signal t01, WisconsinBadgers t04, simonfraser t08.
  - My primary was wrong: orderofthebluecorner t08 (all three placed T3-121, exclusion, against my T3-087); stardustcrusaders t19 (all three placed T3-043, thanks, where the gate's default made T3-009 primary).
- **Scheme-ambiguous** (edited):
  - guatemala t02 (a national flag started and announced; readers placed T3-026 twice and T3-002 once, none T3-065) and catalunya t01 (one reader T3-002);
  - dofus t01 (T3-092, T3-038 and T3-002);
  - cubers t12 (T3-002, T3-041 and T3-169);
  - nVade t04 (all T3-005, where the work defended is another room's);
  - WisconsinBadgers t04 (one reader T3-042);
  - farmcarrots t15 (one reader T3-031).
- **Item-is-a-bag** (flagged, no edit): acecombat t05, Goodboye t03 and simonfraser t08. They hold four or more kinds and were bags in the B1 record.
- **Genuine-joint, or one reader recording rule 0's exception** (no edit): Slovakia t07, anarcho_capitalism t12, parabola t02, korea t15, furry t10 (T3-034) and donaldglover t04 (two readers added T3-032).
- **Reader-error**: none named. The single-reader misses (catalunya, n64, signal, farmcarrots) are covered by edits or by discriminators that already decide.

### The edits

`scheme_edits.jsonl`: 272 lines, all round 1.

The first record bundled mirrors and new questions one line per theme and field (36 lines). After QB2-003 it moved to `out/_analysis/scheme_edits_b2b-r1_bundled.jsonl`, and the record was rewritten one line per change. The 36 tier_history lines written for the bundled record (253 to 288) are superseded by the per-edit lines that follow them.

- **Sentence changes, 6:**
  - T3-005 must_not_show: repair "with or without an attacker in view, where no fight is called" goes to T3-021 (the contradiction).
  - T3-021 must_show: repair during a raid counts there when the fixing leads.
  - T3-009 and T3-043 decide_when_both: the side with more concepts is primary (author-error).
  - T3-065 must_show: announcements and calls for the room's own flag go there.
  - T3-092 decide_when_both: a piece begun alone and offered to the room is T3-033 when the offer leads.
- **8 discriminators from round-1 splits:** T3-087/T3-121 (author-error), T3-005/T3-011, T3-026/T3-065 and T3-002/T3-169, each in both gates.
- **Gate repairs no item caused** (QB2-003), until `mem.py gates` found no defect:
  - 202 word-for-word mirrors of one-way discriminators (kind gate-check);
  - 28 new questions, each written into both gates (56 lines), for `must_not_show` lines that sent material to a theme with no discriminator. 7 in the first pass are in `b2_edits_r1.py`; 21 are in `out/_analysis/b2_newpairs_r1b.json`.
  - Together with the 6 sentence changes and the 8 split-driven discriminators, that makes 70 edits that owe rechecks and tier_history lines.
- **After the edits:** `mem.py gates` reports 0 one-way discriminators, 0 such `must_not_show` lines and 0 unknown ids. Eleven pairs were read and confirmed (`out/gate_checks.jsonl`): T3-005/T3-021, T3-009/T3-043, T3-002/T3-065, T3-087/T3-121, T3-005/T3-011, T3-026/T3-065, T3-042/T3-076, T3-062/T3-084, T3-033/T3-092, T3-002/T3-169 and T3-004/T3-070. The other pairs of edited themes are not yet confirmed; they are read before the freeze.
- No theme was narrowed, and no theme's members changed. **Base rates** (author against readers, over 40 items):
  - T3-004: 2 against 0;
  - T3-021: 1 against 0;
  - T3-011: 3 against 1;
  - T3-014: 2 against 8 (2.7 per reader);
  - T3-005: 3 against 9 (3.0 per reader);
  - T3-121: 0 against 3.

  The full table is in the score script's output. Round 2 watches T3-004 and T3-021, which no reader chose.

### The rechecks

Every edit that is not a gate-check owes rechecks of my own placements on the themes it touches. There are 70 such edits; they owe 594 records over 78 items. `out/_analysis/b2_rechecks_r1.py` decides each item once and records it under every edit that owes it, with `mem.py recheck` and the concepts behind each theme.
- **22 items move:** 18 are author-errors, mostly second kinds that rule 0 does not need, and 4 are the edits doing their work (GreenCorner t03, dofus t01, stardustcrusaders t19, guatemala t02).
- The rest are unchanged, each with its reason.
- `author_items.jsonl` stays as written. From round 2, fidelity is reported twice: against it, and against the rechecked placements.

### Section 4

**Position curves** (each reader's items at positions 1 to 10 against 31 to 40):
- r12: arguable 6 then 5; agreement with the other two 0.70 then 0.80.
- r15: arguable 8 then 6; agreement 0.65 then 0.70.
- r16: arguable 6 then 4; agreement 0.75 then 0.70.

Two of three readers still improve inside the round, so convention formation is not over at 40 items. Ten items per bin and three readers make this weak evidence. Following section 4, the remedy is a warm-up block, not a bigger batch.

**The batch cap for stage B3** (declared here): 40 items per batch, the first 10 of them a warm-up block that is placed and not counted. To be revisited with round 2's curves.

**Exemplar candidates:** the 18 items that divided readers are in `exemplar_candidates.jsonl`, with the readers' sets and mine.

### Predicted confusions, so far

Of the 19 pairs in `confusions.md`, round 1's readers split on:
- pair 6 (dofus t01, T3-002/T3-033), though not along the predicted line;
- pair 8 (furry t10, T3-004/T3-070), by adding T3-034;
- pair 10 (signal t01, T3-038 against T3-009, not T3-004);
- pairs 2, 7 and 12 by adding a second kind (anarcho_capitalism t12, korea t15, parabola t02);
- pair 11 by moving off both themes (acecombat t05, T3-014 and T3-062).

The hardest predicted pair, T3-005/T3-021, did not split: GreenCorner t03 went to T3-005 for all three readers. The scored scorecard comes after the gold round.

### Next

Round 2 is built at `B2a-r2`, in `out/_packets-B2/round-2/`, from the edited `scheme.jsonl`:
- the ten biggest bags served in parts (the splitter as a helper if `packets.py` cannot part a B2 item);
- `RETURN-B2.md` with the `also_present` clause;
- the manifest entry noting the reader settings.
