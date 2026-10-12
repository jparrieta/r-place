# B4: contests decided by three placements, and a blind sample of 500

2026-10-12T19:00Z. From the orchestrator (Claude) to the handler. Target length: under 700 words. Advice: the handler implements it as amendments to stage B4, its check and the assembly of B3's returns. B4 has not started.

## J's rulings, 12 October

- "I think we should use all three as determinants for adjudication. If all agree then all good. If two agree then multiple routes open up but I would be ok with adjudication in both." A difference in order alone goes to adjudication like any other case: J would "just add the case to adjudication".
- On the items where both readers agree on fewer themes than the analyst's B1 grouping: "I would just leave the aggregator's, view." Confirmed the same evening: the B1 grouping stands. I had advised the readers' list: on 20 gold items, in the reader pairs that agree on a smaller set, the analyst's own B2 placement matched that smaller set in 44% and the full B1 grouping in 26%.
- The blind sample: "Ok let's add 250 each for adjudication and random".

## The three placements

For each item: the two readers' pass-1 lines (replicates 1 and 2), and the analyst's B1 grouping. The B1 grouping is the item's themes among the members of `out/scheme/scheme_current.jsonl` (sha256 `8b67360b8d0dfefc`), joined by sub and second-order label through `package/store/themes.jsonl`. It is a set with no order. Gold copies and the duplicate's second copy are left out.

## The rule, replacing §1's "every item where the two readers differ, plus every `multi` item"

The placement stands, with no adjudication:

1. The two readers return the same list, order included, and its set equals the B1 grouping. The readers' list stands, `multi` or not.
2. The two readers return the same list, and its set is smaller than the B1 grouping and inside it. The B1 grouping stands: the readers' list first, then B1's other themes. `assign_final.jsonl` tags the source of these lines, so that C1 can tell them from placements made under the frozen scheme.

The item goes to B4:

3. The readers differ, including the same themes in another order.
4. The readers agree on a set that is not inside the B1 grouping.
5. The item has no B1 grouping (58 at B1).

§1's other rule stands: a placement into a family neither reader opened is read whether or not the readers agreed.

**Expected load**, from 4,247 items with both readings in 931 returned packets:
- rule 1: 32.3% of items;
- rule 2: 26.3%;
- to B4: 41.4%, about 3,250 of 7,844, or 7 legs at 500 contested items a leg, before the unopened-family reads.

## The blind sample, §10 to §12

- 500 items: 250 drawn uniformly from the analysed set and 250 from the adjudicated items, by a recorded seed.
- Two fresh readers per item, as `arm.json` sets B4's readers now: 1,000 comparisons.
- The strata stay apart. Within the uniform stratum, report the items kept under rule 2 as a row of their own: they were neither adjudicated nor placed under the frozen scheme.
- Places that name the old size: §10 ("one hundred items, fifty … fifty", "two hundred comparisons"), §12 ("alpha on the hundred", "a hundred items over hundreds of themes"), and the fixture text in `tools/checks/stage_B4.py`.

## Assembly

Your `assemble` verb fits this. Three additions:
- Tag gold copies and the duplicate's second copy from `batches-B3.jsonl`, so that no seeded copy counts as a corpus reading.
- Join each item's B1 grouping as above.
- Write each item's class, 1 to 5, and print the counts.

Then the contested inventory is built by the tool, not by a hand-written script.

## Not checked

- The figures rest on 54% of items; 279 packets were still out.
- I computed no intervals.
- I read `stage_B4.py` only at the lines named, and not the tool that writes `disagreements.jsonl`.
