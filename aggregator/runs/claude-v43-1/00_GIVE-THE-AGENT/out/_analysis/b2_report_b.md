
The edits that came from readers' splits, in short:
- **Repair during a raid** (T3-005, T3-021; GreenCorner t03).
- **Whose flag a flag in a room named for a land is** (T3-065, T3-002, T3-026; guatemala t02, catalunya t01). At round 3, two of three readers on guatemala t02 followed the new gloss.
- **A pledge named as the reason for help** (T3-195, T3-011, T3-005; nVade t04). Two of three readers moved to T3-005.
- **The offer, the call and the build** (T3-002, T3-033, T3-038, T3-070; signal t01, n64 t02, 2007scape t04, dofus t01). This edit was made at the freeze and is tested only by the gold round. On the gold set no item divided readers between these themes. Across all six rounds the T3-002/T3-033 pair split once in 97 reader pairs.
- **Credit and celebration** (T3-009, T3-043; redhotchilipeppers t09, stardustcrusaders t19), as author-error.
- **Tracing and excluding** (T3-087, T3-121; orderofthebluecorner t08), as author-error.

## The author-error verdicts

In each case below the readers were right and I was wrong.

**On the hard set, 21 items.**
- **Caught by my rechecks after rounds 1 and 2:** 4chan t07, Goodboye t03, WisconsinBadgers t04, acecombat t05, england t03, flashtv t13, floridagators t09, furry t10, harrypotter t08, kpop t04, megaman t11, nyu t01, orderofthebluecorner t08, signal t01 and simonfraser t08.
- **Named at round 2 with no sentence changed:** AyyMD t08, cubers t12, farmcarrots t15, parabola t02, redhotchilipeppers t09 and Slovakia t07.

Most are second placements that the readers did not keep.

**On the gold set, 11 items.**
- **Second placements no reader kept, by my rechecks before the gold round:** kurdistan t03, predators t04 and russia t09.
- **Second placements found at the gold round:** DevonUK t04, cubers t27, floridagators t04, natsume t01, tinytardis t06, uiuc t04 and alberta t04.
- **A primary placement:** cloud9 t12. Seven of nine readers placed it on T3-117 (marking the canvas's end). The item's two concepts sit at the close, and one of them is a failed attempt after the end.

**On the gold set, the readers missed what I placed.** I hold my placement on these four. The scheme is frozen, so they go to C1 as wording defects.
- **uofmn t01:** all nine readers chose T3-001 (members' fakes) against my T3-048 (the university's own prank). The concepts barely name the maker.
- **cuboulder t04:** the gold readers chose T3-033 (proposing a mark) for a new plan for an existing logo. The T3-004/T3-033 question does not say that a plan for a mark already standing is design.
- **mariokart t04:** readers chose T3-005 or T3-002 for a member of r/ainbowroad asking this room for help (my T3-084). The question does not say whose room the asker speaks for.
- **ireland t12:** readers chose T3-002 for calls to join a memorial (my T3-160 and T3-084).

**Items no single placement decides.** portugal t41 (T3-137 and T3-180) is genuine-joint. shitredditsays t09 is one concept, "mods plz", that cannot decide. On dankmemes t10 the readers split evenly between T3-031 and T3-033.

**Author-error count:** 32 items (21 hard, 11 gold). Of the 306 lines in `scheme_edits.jsonl`, 4 are author-error.

## Themes that never stabilised, and what stage B4 should expect

- **T3-004 against T3-070** (design against directions) was the most divided pair of `confusions.md`: 6 splits in 55 reader pairs. B4 should expect readers to file a posted template as directions when I filed it as the design settled, and the reverse.
- **T3-009 against T3-073** (celebrating against telling how the work fared; flashtv t13 in every round): 5 splits in 65.
- **T3-001 against T3-023 and T3-048** (April Fools by members, by the sub, by the maker; AyyMD t08 in every round, uofmn t01 on gold). B4 should expect readers to call any unattributed fake a member's.
- **The sub's rules, G02** (T3-015, T3-063, T3-075, T3-185, T3-182; overwatch t23, finland t06, shitredditsays t09). Gold pairwise was 0.64. Short moderator lines carry too little to decide.
- **Second kinds in deals with neighbours, G14** (T3-010 with T3-151, T3-150, T3-024 or T3-123). Readers agree with each other (pairwise 0.81 on gold) and place T3-010 alone. B4 should expect a single T3-010 where the record carries two kinds.
- **The cluster T3-002/T3-033/T3-038.** It was quiet on the gold set, but it divided signal t01, n64 t02 and 2007scape t04 at round 3, and the count rule is tested only once.

**Base rates.** No theme was tightened by narrowing. On the gold round every edited theme's rate per reader stayed within half an item of my count. T3-002 had 3.3 against my 3, T3-033 1.3 against 1, T3-038 2.0 against 2, and T3-010 5.0 against 5. No theme's base rate fell while it was tightened.

## The prediction scorecard

`out/_analysis/b2_score_final.py` scored the nineteen pairs of `confusions.md` over every reader pair in all six rounds. A pair splits when one reader's primary is one theme and the other's the other, or when one set holds one theme without the other and the other set the reverse.

| predicted rank | pair | reader pairs touching | splits | rate | observed rank |
|---|---|---|---|---|---|
| 1 | T3-005 / T3-021 | 67 | 0 | 0.00 | 6 |
| 2 | T3-010 / T3-149 | 78 | 0 | 0.00 | 7 |
| 3 | T3-001 / T3-023 | 58 | 3 | 0.05 | 3 |
| 4 | T3-028 / T3-070 | 53 | 0 | 0.00 | 8 |
| 5 | T3-004 / T3-020 | 24 | 0 | 0.00 | 9 |
| 6 | T3-002 / T3-033 | 97 | 1 | 0.01 | 5 |
| 7 | T3-015 / T3-075 | 45 | 0 | 0.00 | 10 |
| 8 | T3-004 / T3-070 | 55 | 6 | 0.11 | 1 |
| 9 | T3-009 / T3-073 | 65 | 5 | 0.08 | 2 |
| 10 | T3-004 / T3-038 | 60 | 0 | 0.00 | 11 |
| 11 | T3-010 / T3-151 | 84 | 0 | 0.00 | 12 |
| 12 | T3-010 / T3-150 | 79 | 0 | 0.00 | 13 |
| 13 | T3-010 / T3-024 | 87 | 1 | 0.01 | 4 |
| 14 | T3-009 / T3-043 | 64 | 0 | 0.00 | 14 |
| 15 | T3-001 / T3-095 | 53 | 0 | 0.00 | 15 |
| 16 | T3-188 / T3-087 | 20 | 0 | 0.00 | 16 |
| 17 | T3-044 / T3-082 | 23 | 0 | 0.00 | 17 |
| 18 | T3-014 / T3-152 | 40 | 0 | 0.00 | 18 |
| 19 | T3-015 / T3-063 | 58 | 0 | 0.00 | 19 |

**Which predicted confusions were real.** Four of the nineteen pairs split readers at all, and only three more than once:
- T3-004/T3-070 (predicted 8th, observed 1st);
- T3-009/T3-073 (predicted 9th, observed 2nd);
- T3-001/T3-023 (predicted 3rd, observed 3rd).

The order of the predictions did not hold. Readers chose one theme, so most rule-0 pairs the record had joined never divided them.

**The hardest pair's estimate failed.** I estimated that 15 to 20% of reader pairs would split on which of T3-005 and T3-021 carries a theme. In 64 reader pairs with either as a primary, none split.

**The family boundary test.** `confusions.md` asked whether a reader holding G14 alone files truces and alliances under T3-010. The splits were 0 on T3-010/T3-149 and 0 on T3-010/T3-150, with 2 primary splits each. Readers did not confuse them, and the G14 and G15 index pages need no merge.

## What it cost

The next table lists each dispatch's DONE record. For round 3 the record is the dispatch's own: 36 calls, before the handler's rescue kept three valid replies per packet.

| round | readers scored | items | cost (USD) | input tokens | output tokens |
|---|---|---|---|---|---|
| 1 | 3 (of 7 attempts) | 40 | 0.369 | the last call: 84,435 | the last call: 16,000 |
| 2 | 15 | 50 | 0.598 | 751,923 | 489,651 |
| 3 | 15 (of 36 calls) | 50 | 1.490 | 2,988,066 | 1,117,845 |
| gold | 9 | 40 | 0.231 | 288,978 | 225,436 |
| stab-1 | 9 | 40 | 0.178 | 46,041 | 211,978 |
| stab-2 | 9 | 40 | 0.220 | 132,118 | 276,244 |

In all, 60 readers' returns were scored. The rounds served 260 items: 40, 50 and 50, then 40 three times. The six dispatches cost about 3.09 USD. Round 1's DONE record holds only its last call. Its total of 0.369 USD is from round 1's check leg. `tools/tokens.py --dispatched` lists the input tokens of every call.

## The one sentence I am least sure a stranger reads as I meant

It is the cluster's count rule in the decide_when_both of T3-002, T3-033 and T3-038: "count the concepts of each: the act with the most concepts of its own is primary". A reader must sort each concept into one act before counting. On a 349-concept item like 2007scape t04, that sorting is itself a judgement.
