# Notes, stage B2: the pilot

## Standing instruction from J (2026-10-11, 16:54 Berlin, through the handler)

"Stop cutting room reads to a line length (cut -c1-100 or any other cut). Read room lines whole. When a read is too long, page it by line ranges or by offset, never by truncating lines."

From B2a-r1 on, every room read is whole by line. A long read is paged by line range or offset. No `cut -c` and no other truncation is applied to room material.

J also said (17:01 Berlin): ask J whenever a question is needed, with `mem.py ask`; asking does not stop the run.

## Leg B2a-r1, build round 1, 2026-10-11

### Declarations, made before round 1

**The hard set: sizes and sources.** 40 items, drawn by `out/_analysis/b2_select.py` with the string seed `b2a-r1:hard`. The list is `out/_analysis/b2_hardset_r1.tsv`.
- 19 confusion-pair items, one for each pair in `confusions.md`: the 17 ranked at B1e and two sibling pairs added at this leg (T3-014/T3-152 and T3-015/T3-063). Ten of the nineteen pairs are siblings inside one family. Each pair uses the item `confusions.md` nominated, unless that item renders over 2,500 bytes. Then the pick is seeded from the pair's pool: second-order themes holding both kinds in `scheme_current.jsonl` and rendering at or under 1,600 bytes. Five nominated items were replaced this way (pairs 7, 8, 11, 12 and 19).
- 8 rule 0 bags: second-order themes with an `item_is_a_bag` line in `multiplacement_log.jsonl`, rendering at or under 1,600 bytes, seeded.
- 13 random items, seeded, from the 3,933 placed second-order themes rendering at or under 1,500 bytes.

**A departure from section 1, and why (QB2-001 asks J).** `packets.py B2` serves each round as one packet under the 50 KB ceiling. Section 1 asks for 40 to 60 items, including the ten biggest bags of `notes-B1.md`.
- Those ten hold about 3,500 concepts. leagueoflegends t02 alone renders 86,762 bytes, over the whole ceiling, and sweden t01 renders 43,314.
- The median second-order theme renders 1,470 bytes, so 40 items fit only near or below the median.
- Rule 0 bags stand in for the ten biggest; the ten stay for stage B3 to flag.
- The cost: the random sample covers only themes at or under the median rendered size. Small themes sit on one kind more often (70.4% at five concepts or fewer, B1e). So the random items are likely easier than the corpus, and the pair and bag items carry the hard part.
- The round-1 items render 49,401 bytes.

**The gold set.** 40 items by the same rule, seed `b2a-r1:gold`, in `out/_analysis/b2_goldset.tsv`: 19 pair items from the pairs' pools (none a round-1 item), 8 rule 0 bags and 13 random. No second-order theme sits in both sets. The items render 42,148 bytes. I placed them myself into `out/gold_items.jsonl` with confidence and reasons. They are shown to no pilot reader and kept outside the readers' directory.

**The stopping threshold.** Rounds stop when the mean pairwise agreement on the hard set reaches 0.70 (the definition is below). The other stops of section 5 also hold: a round with no scheme edit, or four rounds. Why 0.70: the set is drawn hard, half from pairs a reader is expected to confuse. On easy items the scheme should do far better, and stage B3 reports that.

**The agreement definition, which stages B3 and B4 reuse unchanged.**
- An item's placement is the set of third-order themes a reader returns (`third_order`).
- Two sets agree by their Jaccard index, |A ∩ B| / |A ∪ B|. `["T3-004"]` against `["T3-004","T3-011"]` scores 0.5, which is partial agreement. Disjoint sets score 0, and identical sets score 1.
- **Pairwise agreement** is the mean Jaccard over the three reader pairs of each item, then over items.
- **Fidelity** is the mean Jaccard between each reader's set and the author's set in `author_items.jsonl`, over readers and items.
- **Alpha** is Krippendorff's alpha with distance 1 − Jaccard between sets, over items run at more than one reader. Chance correction is over sets: the expected disagreement is computed from all placement sets returned in the round, pooled, as the values of the nominal-like distribution.
- Also reported, never in place of the above: exact agreement on the primary, the first theme of each set.

**The gold policy.**
- 40 gold items, placed by me, in `out/gold_items.jsonl`.
- Stage B3 seeds them unannounced into live batches at one gold item per 20 items, so about 5% of a batch, with no more than two in any batch.
- Each gold item is seeded at least once over the run.
- The policy names the rate and that gold is seeded, never which items.

**The batch cap for stage B3.** Set at the check leg B2b-r1, from the position curves of section 4. It is not set here.

**Author placements.** Every item of both sets was placed by me into `author_items.jsonl` and `gold_items.jsonl` before any packet existed. Each line has the set of third-order themes, a `why` per theme, a confidence (`clear` or `arguable`) and the concepts it rests on. I read each item through `mem.py theme <sub>/<tNN>`, whole, paged where long. That verb prints the working placements of `scheme_current.jsonl` above the concepts, so they were in view. Those placements are my own from B1. Each author placement was made against the shipped gates in `scheme.jsonl`, and where it differs from the working placement, the line says so.

### What was built

**The author's placements** (`out/_analysis/b2_author.py`, which checked every theme id against `scheme.jsonl` and every support concept against the item's own concepts in the store):
- `author_items.jsonl`: 40 items. 5 are clear and 35 arguable; 24 are placed on more than one kind; 25 differ from the B1 working grouping in at least one kind.
- `gold_items.jsonl`: 40 items. 4 are clear and 36 arguable; 17 are on more than one kind; 19 differ from the B1 working grouping.
- The many arguable placements fit how the sets were drawn: half the items come from pairs I predicted readers would confuse, and eight from rule 0 bags.
- Where my placement differs from the working grouping, it mostly drops a kind whose concepts the gate does not support on their own (`b2_author_vs_working.py`). In the hard set, 18 items only drop a kind, 5 only add one, and 2 do both; 15 are the same. In the gold set, 15 only drop, 4 only add and 21 are the same. My primary is among the working kinds in 39 of 40 hard items and 40 of 40 gold items. Three examples of a dropped kind: dofus t01 drops T3-002, GreenCorner t03 drops T3-069, and flashtv t13 drops T3-054.

**RETURN-B2.md.** It holds rule 0 in the contract's words and the return line of section 1. Rule 0's line for `multiplacement_log.jsonl` is carried on the return line as `multiplacement_log`, null when `multi` is false. The check leg copies those lines into the pilot's record, never into the B1 log. It also holds `item_is_a_bag`, the end marker `END-OF-RETURN` in the fenced block, and the line telling the reader to confirm it reached the marker.

**The packets.** `packets.py B2 --round 1 --scheme scheme.jsonl --items author_items.jsonl --seed 20261011 --to out/_packets-B2` wrote:
- `index.md` (33,148 bytes);
- 21 family pages (6,566 to 16,448 bytes);
- `P03-r1.md`, 40 items in seeded order, 49,720 bytes, sha256 1efc10ac60398acee09ad3503aca758803f96cd1fae8ee0afea3044d0bf868ff;
- `MANIFEST.json`.

No exemplar is served, and no gold file is in the folder. The scheme served is `scheme.jsonl` as shipped at B1e. `packets.py` would otherwise have preferred `scheme_current.jsonl`, which holds no gates, so `--scheme` was given.

**Where the packets live (QB2-002 asks J).** `packets.py` writes to `_packets-B2/round-1/` by default. HOW-TO-RUN.md and `validate.py B2` expect the packets flat in `_packets-B2/`. I built flat. The first, nested build is byte-identical and moved to `out/_analysis/b2_packets_round1_nested/`, so the dispatch finds one packet only.

**Manifest.** `run_manifest.json` has a B2 round-1 entry: readers on `@preset/cheap` through the gateway, three of them; the seeds; 40 items; and the packet's path and hash. The decoding settings are left to the dispatch, which records what served.

**Questions open:** QB2-001 (the 50 KB ceiling against the ten biggest bags) and QB2-002 (the packet path). Each carries its assumption, and the work above rests on both.

**Reading.** From this leg on, no room read was cut to a line length. The only "…" in the reads is `mem.py`'s own display of the label column; the quote column was whole in every read.

### The close-check, B2a-r1

`validate.py B2` reported:

```
stage B2:
  leg: build (0 dispatch folders with DONE)
  author items 40, gold items 40, scheme ids 197

0 errors (0 distinct shapes), 0 warnings
```

The leg closes with `done.sh B2 --cut packets-out`. The dispatch sends `P03-r1.md` to three fresh readers. The check leg B2b-r1 scores fidelity, pairwise agreement and alpha, sets the batch cap for stage B3, and makes the edits.

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

### Added after the section above, in the same leg

**The deal cluster.** Reading T3-010's 17 pairs found seven where a decide_when_both names T3-010 but no discriminator separates the pair: T3-012, T3-035, T3-039, T3-040, T3-084, T3-123 and T3-139. `mem.py gates` checks only `must_not_show` lines, so it does not see this shape. Seven questions were written into both gates (`out/_analysis/b2_newpairs_r1c.json`; scheme_edits 273 to 286). They are kind scheme-ambiguous, with `caused_by gates:A|T3-010` and 14 tier_history lines.

The final counts are:
- `scheme_edits.jsonl`: 286 lines, 202 gate-check mirrors and 84 edits that owe rechecks;
- `tier_history.jsonl`: 372 lines;
- `mem.py gates`: no defect; 28 pairs confirmed, 0 stale, 464 unconfirmed. The unconfirmed pairs are read before the freeze.

**The rechecks, final.** 697 recheck records, none owed. 22 items moved from my original placement: 18 author-errors and 4 edits doing their work.
- 70 records failed when first tried. An earlier recheck had already moved those items off the themes the later edits touch, so `mem.py` no longer counted them as owed; the record was right to refuse them.
- `mem.py recheck` takes about 4.5 seconds a record, and the first run went past the ten-minute foreground limit into the background. The rest ran in the foreground in slices (`--max`).

### The close-check, B2b-r1

`validate.py B2` reported:

```
stage B2:
  leg: check (1 dispatch folders with DONE)
  _fleet_raw/B2/round-1: 3 readers, 120 return lines
  author items 40, gold items 40, rounds scored 1, edits 286 (author-error 4), scheme ids 197 (scheme/scheme_current.jsonl)

0 errors (0 distinct shapes), 443 warnings
warn   scheme.jsonl: the pair T3-001|T3-017 touches an edited theme and is not confirmed against its current sentences (mem.py gates T3-001 T3-017 --confirm --reason ...)  [443 lines with this shape; first: T3-001|T3-017]
```

The 443 warnings are pairs touching an edited theme that are not yet confirmed. They are read and confirmed before the freeze, where they become errors. The check counts 120 return lines because `round-1` holds only the three valid readers' `.jsonl` files; the failed attempts are `.failed.txt`.

The leg closes with `done.sh B2`. Round 2's build leg, B2a-r2, comes next.

## Leg B2a-r2, build round 2, 2026-10-11

### QB2-003, revisited

The PI's answer to QB2-003 arrived during B2b-r1, and that leg applied it in full. Every repair is a `scheme_edits.jsonl` line with `caused_by` `gates:T3-a|T3-b`; mirrors are kind gate-check, with no recheck and no tier_history line; new sentences are scheme-ambiguous and owe both. My assumption, to repair only the pairs round 1's edited themes belong to, was dropped in that leg. No work of this leg rested on it. `mem.py gates` on the scheme served this round finds 0 one-way discriminators, 0 `must_not_show` lines without a discriminator and 0 unknown ids. 28 pairs are confirmed and 464 are not. The answer asks me to confirm each pair I read; the 464 are read and confirmed before the freeze.

### The ten biggest bags, placed

I read all ten second-order themes whole, paged with `--limit` and `--offset` and never cut. Then I placed them, before any round-2 packet existed. `out/_analysis/b2_author_r2.py` appended them to `author_items.jsonl`. It checked every theme id against `scheme.jsonl`, and every concept against the item's own concepts with `vlib.support_problems` and `vlib.also_present_problems`. It also checked that no item was already in the hard or gold set, and it took each item's rank from `notes-B1.md`'s list. Each line carries `source` "biggest-bag", `support_by_theme`, `item_is_a_bag` and `also_present`. All ten are arguable. The hard set is now 50 items.

Rule 0, as amended, decides the form. Round 1 showed that my second kinds were author-errors whenever one theme carried the material. So no line places more than one theme. A bag, an item that needs more than three themes, places one and names the rest under `also_present`, each with its own concepts.

The next table lists the ten items: the theme placed, the themes named under `also_present`, and the B1 working kinds.

| rank | item | concepts | placed | also_present | B1 working kinds |
|---|---|---|---|---|---|
| 1 | leagueoflegends t02 | 798 | T3-023 | none | T3-023 |
| 2 | theblackvoid t09 | 389 | T3-006 | none | T3-006, T3-080, T3-085 |
| 3 | ainbowroad t11 | 361 | T3-035 | none | T3-035, T3-084, T3-139 |
| 4 | 2007scape t04 | 349 | T3-038 | T3-005, T3-123, T3-010, T3-179, T3-157 | T3-038 |
| 5 | theblackvoid t12 | 335 | T3-174 | T3-006, T3-163, T3-190, T3-005 | T3-031, T3-163, T3-174 |
| 6 | ainbowroad t04 | 327 | T3-021 | T3-139, T3-024, T3-011, T3-084 | T3-021 |
| 7 | ainbowroad t03 | 326 | T3-005 | T3-084, T3-149, T3-050, T3-124 | T3-005 |
| 8 | dota2 t05 | 314 | T3-023 | none | T3-023, T3-032 |
| 9 | ainbowroad t07 | 311 | T3-041 | T3-035, T3-160, T3-033, T3-061 | T3-038, T3-041, T3-160 |
| 10 | sweden t01 | 310 | T3-065 | T3-035, T3-012, T3-061, T3-113, T3-151 | T3-065 |

Six are bags and four take one theme. Points from the reads:
- leagueoflegends t02 and dota2 t05 are the two moderator makeovers (Marc Merrill, and Arteezy as r/tz). Objections to the joke, reactions to Riot's own jokes and asks to keep the theme are present, but the takeover carries them.
- theblackvoid t09 calls attacks on named targets: national flags, the EU flag, the trans ribbon, "the slimy swedes". The B1 working kinds added T3-080 and T3-085. I found the calls to attack carry the material and placed T3-006 alone.
- ainbowroad t11 is outside rooms addressing Rainbow Road as host. Requests for space, pleas for help and pleas not to be run over sit on one host relation, and T3-035 carries them.
- theblackvoid t12: I placed T3-174 (loyalty to the Void's colour: hails, the oath, anthems) over the B1 working T3-031. The creeds are professions of loyalty, not in-jokes played inside the room.
- ainbowroad t07: I placed T3-041 (extending strands, adding features) over T3-038. The road was already built; these concepts extend it.
- ainbowroad t03 holds the line "KILL THE GAYS" (c1395), posted to the room. It is served to readers as it stands.

### What was built

**`RETURN-B2.md`.** It gains the `also_present` clause in J's words of section 1. A bag places one theme and names every other with its own concept ids; otherwise the field is `{}`. It also gains a paragraph on parts: read every part, reply with the end marker alone on every part but the last, and answer for all items on the last. The batch name is now `P03-r2`. The round-1 text is kept as `out/_analysis/RETURN-B2_round1.md`; round 1 is scored as it was sent.

**The packets, in parts (QB2-001).** `packets.py B2` writes one packet and exits when it is over 50 KB. Round 2 renders to about 513 KB, and leagueoflegends t02 alone is about 87 KB. So the splitter `out/_analysis/b2_parts_r2.py` imports `packets.py` and uses its own `Store.item` and `scheme_pages`. It shuffles the 50 items as `packets.py` does, with seed 20261012. Then it cuts the rendered lines into parts. An item that does not fit runs on into the next part under its heading marked "(continued)". A concept line always travels with its quote line, and positions run on across parts. The helper checks that every concept of every item is served exactly once. It wrote `out/_packets-B2/round-2/`:
- `index.md` (33,542 bytes) and 21 family pages (7,839 to 19,772 bytes), from the edited `scheme.jsonl`, with no exemplars;
- `P03-r2-p1` to `P03-r2-p11`. Ten parts are 50,254 to 50,394 bytes and the last is 9,799; each is under 51,200 bytes with its end line, 513,096 bytes in all;
- `MANIFEST.json`.

The next table lists the positions each part holds.

| part | positions | part | positions |
|---|---|---|---|
| p1 | 1-8 | p7 | 37 |
| p2 | 8-19 | p8 | 37-39 |
| p3 | 19-27 | p9 | 39-43 |
| p4 | 27-28 | p10 | 43-47 |
| p5 | 28-36 | p11 | 47-50 |
| p6 | 36-37 | | |

Position 37 runs over four parts (p5 to p8); it is leagueoflegends t02. The seeded order and the positions per part are in `out/_analysis/b2_order_r2.json`, outside the readers' folder. Round 1's packets are where they were: flat in `out/_packets-B2/`, and J's copy in `round-1/`. No gold item and no room note is in the folder.

**MANIFEST.json, on QB2-004's assumption.** QB2-004 is open. It asks what form `fleet.py` expects when one item is larger than a part. Until it is answered, each part carries `count_key` position, the B3 exclusions, `group` P03-r2, `part` k and `parts` 11. Parts 1 to 10 carry `items` 0, since their reply is the end marker alone, and part 11 carries all 50. Each entry also records its positions and the seed. If J answers otherwise, the next build leg rebuilds from the same helper.

**Manifest.** `run_manifest.json` has a B2 round-2 entry (`out/_analysis/b2_manifest_r2.py`). It records the model, deepseek/deepseek-v4-flash-0731, and J's reader settings: one provider (Relace) and medium reasoning effort. Round 1 ran at high effort on mixed providers. A change in agreement between the rounds is therefore partly the settings and not only the edits. The entry also records the seed, 3 agents, 50 items, and every part's bytes and sha256.

**The PI's round-2 rule.** No round may meet a stopping rule before the ten biggest bags have been read once. Round 2 serves all ten, so its check leg may apply the stopping rules.

**Questions open:** QB2-004.

### The rechecks the ten new items owed

The ten bags sit on themes that round 1's edits changed. The first run of `validate.py B2` in this leg therefore found 57 rechecks owed under 42 edits, one error line per edit. No edit can have moved a placement made after it. The check still asks for the record, so `out/_analysis/b2_rechecks_r2.py --show` printed each edit's changed sentence beside the items it owes. I read each and wrote one reason per edit. None moves a placement. The 57 records went in through `mem.py recheck`, all unchanged, with the concepts from each line's `support_by_theme`. `rechecks-B2.jsonl` now has 754 records, and none is owed.

### The close-check, B2a-r2

`validate.py B2` reported:

```
stage B2:
  leg: check (1 dispatch folders with DONE)
  _fleet_raw/B2/round-1: 3 readers, 120 return lines
  author items 50, gold items 40, rounds scored 1, edits 286 (author-error 4), scheme ids 197 (scheme/scheme_current.jsonl)

warn   scheme.jsonl: the pair T3-001|T3-017 touches an edited theme and is not confirmed against its current sentences (mem.py gates T3-001 T3-017 --confirm --reason ...)  [443 lines with this shape; first: T3-001|T3-017]

0 errors (0 distinct shapes), 443 warnings
```

The 443 warnings are the unconfirmed pairs that touch an edited theme. They are read and confirmed before the freeze. The check calls the leg "check" because round 1's dispatch folder holds DONE; this leg is round 2's build. The leg closes with `done.sh B2 --cut packets-out`. The dispatch sends the eleven parts of P03-r2 to each of three fresh readers. The check leg B2b-r2 scores fidelity against `author_items.jsonl` and against the rechecked placements, with pairwise agreement and alpha.
