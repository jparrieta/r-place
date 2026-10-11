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
