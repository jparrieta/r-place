# Pilot report, stage B2

Written at stage B2, leg B2d, 2026-10-12. Three pilot rounds ran on the hard set, then the scheme was frozen. One gold round and two stability rounds then ran on the gold set. Every figure below is mean Jaccard on placement sets, as declared in `notes-B2.md`. Fidelity is agreement with my own placements. Pairwise agreement is the readers' agreement with each other. Alpha uses distance 1 − Jaccard.

This figure bounds whether the instrument decides, not whether it is right. In FLEET.md's terms, the figures support the claim that the fleet produces what I would have produced, at a scale one analyst cannot reach. They do not support the claim that any competent reader would have produced it.

## The rounds

The next table lists each round's three figures. The declared threshold for stopping was pairwise agreement of 0.70 on the hard set.

| round | set | readers | fidelity | against rechecked | pairwise | alpha | items with two readers differing |
|---|---|---|---|---|---|---|---|
| 1 | 40 hard items | 3 (deepseek-v4-flash-0731, preset, high effort) | 0.594 | - | 0.733 | 0.726 | 18 of 40 |
| 2 | 50 hard items | 15 (deepseek-v4.1-flash, direct, medium effort) | 0.639 | 0.701 | 0.718 | 0.710 | 27 of 50 |
| 3 | the same 50 | 15, as round 2 | 0.682 | 0.760 | 0.728 | 0.721 | 23 of 50 |
| gold | 40 gold items, frozen scheme | 9, as round 2 | 0.624 | 0.661 | 0.818 | 0.809 | 14 of 40 |
| stab-1 | the same 40, reworded brief | 9 | 0.636 | 0.674 | 0.800 | 0.789 | 14 of 40 |
| stab-2 | the same 40, second rewording | 9 | 0.631 | 0.669 | 0.756 | 0.743 | 18 of 40 |

**Did agreement climb?** Fidelity on the hard set climbed from 0.594 to 0.639 to 0.682. Against my rechecked placements it reached 0.760. Pairwise agreement held near the threshold: 0.733, 0.718 and 0.728.

The readers changed between rounds 1 and 2 (J, 2026-10-12). Every change across that step is partly the readers. Rounds 2 and 3 used the same readers, so the change from round 2 to round 3 is the scheme's edits 287 to 295 and the readers' own variation.

Round 3 cleared the threshold, and the rounds stopped (J, QB2-012). The 40 items carried from round 1 stayed under the threshold in every round: pairwise 0.685 at round 2 and 0.676 at round 3.

**Second placements.** At round 1, the readers placed two or more themes on 10 of 120 lines. At round 2 the new readers did so on 47 of 150, reading rule 0's "carry" as "cover every concept". At round 3 it fell to 27 of 150, and at the gold round to 10 of 120.

## The gold number beside the last pilot number

Gold fidelity is 0.624, against round 3's 0.682 on the hard set. Gold pairwise agreement is 0.818 and gold alpha 0.809, both higher than round 3's 0.728 and 0.721.

**What the gap means.** On the gold set the readers agree with each other more and with me less. The gap is mine, not the scheme's fitting to the hard set:
- **Second placements the readers dropped.** On ten gold items I placed two themes, and the readers kept only my primary. For eight of them all nine readers across the three rounds did so: DevonUK t04, cubers t27, floridagators t04, natsume t01, tinytardis t06, kurdistan t03, russia t09 and predators t04. On uiuc t04 one reader in nine kept my second theme. On alberta t04 no reader kept my second theme, and two of nine chose T3-046. These are the round-1 author-error under rule 0 again. The gold set was placed at B2a-r1, before round 1 taught it.
- **Rechecked placements.** My rechecks had already caught three of the ten (kurdistan t03, predators t04, russia t09). Against the rechecked placements, gold fidelity is 0.661.
- **Primary match.** It is 0.800 on the gold set, as at round 3 (0.780). On the primary placement the scheme carries as well to unseen items as to the hard set it was edited against. A much worse gold figure would have meant a fitted scheme, and the primary match shows none.

**Per family on the gold set**, by the family of my primary placement:
- G14 (deals with neighbours, 7 items): fidelity 0.40, pairwise 0.81. Readers place T3-010 alone where I added a second deal kind.
- G02 (the sub's rules, 4 items): fidelity 0.46, pairwise 0.64, the lowest pairwise of any family with more than one item.
- G07 (choosing what to make, 3 items): fidelity 0.33, pairwise 0.67.
- G21 (endings, 5 items): fidelity 0.90.
- G09 (defence and repair, 2 items): fidelity 1.00.

**Per theme**, where a theme is in my set for three or more gold items:

| theme | gold items | fidelity | pairwise |
|---|---|---|---|
| T3-002 | 3 | 0.54 | 0.83 |
| T3-004 | 4 | 0.50 | 0.83 |
| T3-009 | 4 | 0.92 | 0.83 |
| T3-010 | 5 | 0.50 | 1.00 |
| T3-015 | 3 | 0.50 | 0.74 |
| T3-063 | 3 | 0.46 | 0.63 |

## The stability figure

**0.807.** For each item, every stab-1 reader is compared with every stab-2 reader by Jaccard, and the nine pairs are averaged. The pairwise agreement inside each stability round is 0.800 and 0.756. A reworded brief adds no disagreement beyond what three fresh readers show under one brief. About one placement in five differs between readers in any case, and that share is the floor every later figure is read against. The full table is in `stability-B2.md`.

## My own consistency

Ten hard items, drawn by seed (`out/_analysis/b2_blind_pick.py`), were read whole and placed again inside a blind window (`out/_analysis/b2_blind_replace.jsonl`). My blind placements agree with my original ones at 0.883, primary 0.90. Against my rechecked placements they agree at 0.900. On the same ten items the round-3 readers' fidelity is 0.806.

I disagree with myself less than the readers disagree with me, so the fleet's distance from me is not my own noise. The two items where I moved:
- **harrypotter t08:** blind T3-159 and T3-017, against my T3-017 and T3-043.
- **megaman t11:** blind T3-087 alone, against T3-087 and T3-188.

On harrypotter t08 my blind primary differs: T3-159 for the house points, against T3-017. On megaman t11 only the second theme drops.

A caveat: earlier legs of this session showed me my placements of several of these ten items in round tables. The window guarded the reads, not my memory, so 0.883 is an upper bound.

## Every edit, by theme

`scheme_edits.jsonl` holds 306 lines:
- 202 are word-for-word mirrors (kind gate-check): one question copied into the other gate of its pair (QB2-003).
- 100 are scheme-ambiguous.
- 4 are author-error.

By field: discriminators 294, decide_when_both 8, must_show 2, must_not_show 1, gloss 1. By round: 286 at round 1, 9 at round 2, and 11 at round 3 and the freeze. No edit narrowed a theme.

The next table lists every theme edited. The "caused by" column names the hard-set items whose readers divided, or "pair A/B" where the edit came from reading a pair of gates rather than from a reader's split. The last column counts the theme's mirror lines.

| theme | lines by field | rounds | kind | caused by | mirrors |
|---|---|---|---|---|---|
| T3-001 | - | - | - | - | 1 |
| T3-002 | decide when both 1, discriminators 6 | 1, 2, 3 | scheme-ambiguous | 2007scape/t04, catalunya/t01, cubers/t12, guatemala/t02, n64/t02, pair T3-002/T3-044, pair T3-002/T3-084, pair T3-144/T3-002, signal/t01 | 5 |
| T3-004 | discriminators 1 | 1 | scheme-ambiguous | pair T3-038/T3-004 | 4 |
| T3-005 | discriminators 2, must not show 1 | 1, 2 | scheme-ambiguous | GreenCorner/t03, nVade/t04 | 5 |
| T3-006 | - | - | - | - | 8 |
| T3-009 | decide when both 1, discriminators 2 | 1 | author-error, scheme-ambiguous | pair T3-009/T3-072, pair T3-073/T3-009, redhotchilipeppers/t09, stardustcrusaders/t19 | 10 |
| T3-010 | discriminators 7 | 1 | scheme-ambiguous | pair T3-012/T3-010, pair T3-035/T3-010, pair T3-039/T3-010, pair T3-040/T3-010, pair T3-084/T3-010, pair T3-123/T3-010, pair T3-139/T3-010 | 4 |
| T3-011 | discriminators 3 | 1, 2 | scheme-ambiguous | nVade/t04, pair T3-115/T3-011 | 5 |
| T3-012 | discriminators 2 | 1 | scheme-ambiguous | pair T3-012/T3-010, pair T3-115/T3-012 | 0 |
| T3-014 | - | - | - | - | 2 |
| T3-015 | discriminators 1 | 1 | scheme-ambiguous | pair T3-197/T3-015 | 2 |
| T3-016 | - | - | - | - | 2 |
| T3-017 | - | - | - | - | 1 |
| T3-018 | - | - | - | - | 1 |
| T3-021 | must show 1 | 1 | scheme-ambiguous | GreenCorner/t03 | 4 |
| T3-022 | discriminators 1 | 1 | scheme-ambiguous | pair T3-029/T3-022 | 1 |
| T3-023 | discriminators 2 | 1 | scheme-ambiguous | pair T3-023/T3-032, pair T3-100/T3-023 | 3 |
| T3-026 | discriminators 2 | 1, 2 | scheme-ambiguous | guatemala/t02 | 0 |
| T3-028 | - | - | - | - | 3 |
| T3-029 | discriminators 1 | 1 | scheme-ambiguous | pair T3-029/T3-022 | 5 |
| T3-031 | - | - | - | - | 6 |
| T3-032 | discriminators 1 | 1 | scheme-ambiguous | pair T3-023/T3-032 | 2 |
| T3-033 | decide when both 1, discriminators 2 | 2, 3 | scheme-ambiguous | 2007scape/t04, dofus/t01, n64/t02, signal/t01 | 2 |
| T3-035 | discriminators 1 | 1 | scheme-ambiguous | pair T3-035/T3-010 | 2 |
| T3-037 | - | - | - | - | 2 |
| T3-038 | decide when both 1, discriminators 4 | 1, 2, 3 | scheme-ambiguous | 2007scape/t04, dofus/t01, n64/t02, pair T3-026/T3-038, pair T3-038/T3-004, signal/t01 | 1 |
| T3-039 | discriminators 1 | 1 | scheme-ambiguous | pair T3-039/T3-010 | 0 |
| T3-040 | discriminators 1 | 1 | scheme-ambiguous | pair T3-040/T3-010 | 2 |
| T3-041 | - | - | - | - | 3 |
| T3-042 | - | - | - | - | 1 |
| T3-043 | decide when both 1 | 1 | author-error | redhotchilipeppers/t09, stardustcrusaders/t19 | 3 |
| T3-044 | discriminators 1 | 1 | scheme-ambiguous | pair T3-002/T3-044 | 3 |
| T3-047 | - | - | - | - | 1 |
| T3-048 | - | - | - | - | 2 |
| T3-049 | - | - | - | - | 1 |
| T3-050 | - | - | - | - | 6 |
| T3-051 | discriminators 1 | 1 | scheme-ambiguous | pair T3-051/T3-062 | 1 |
| T3-052 | - | - | - | - | 1 |
| T3-054 | - | - | - | - | 1 |
| T3-056 | - | - | - | - | 2 |
| T3-057 | - | - | - | - | 2 |
| T3-058 | discriminators 1 | 1 | scheme-ambiguous | pair T3-073/T3-058 | 1 |
| T3-059 | - | - | - | - | 2 |
| T3-060 | discriminators 1 | 1 | scheme-ambiguous | pair T3-060/T3-068 | 0 |
| T3-061 | discriminators 1 | 1 | scheme-ambiguous | pair T3-192/T3-061 | 1 |
| T3-062 | discriminators 1 | 1 | scheme-ambiguous | pair T3-051/T3-062 | 4 |
| T3-063 | discriminators 1 | 1 | scheme-ambiguous | pair T3-140/T3-063 | 4 |
| T3-065 | discriminators 2, gloss 1, must show 1 | 1, 2 | scheme-ambiguous | catalunya/t01, guatemala/t02 | 0 |
| T3-068 | discriminators 1 | 1 | scheme-ambiguous | pair T3-060/T3-068 | 1 |
| T3-070 | discriminators 2 | 3 | scheme-ambiguous | 2007scape/t04, n64/t02, pair T3-026/T3-038, signal/t01 | 3 |
| T3-072 | decide when both 1, discriminators 3 | 1, 3 | scheme-ambiguous | pair T3-009/T3-072, pair T3-104/T3-072, pair T3-159/T3-072 | 1 |
| T3-073 | discriminators 2 | 1 | scheme-ambiguous | pair T3-073/T3-009, pair T3-073/T3-058 | 1 |
| T3-075 | - | - | - | - | 2 |
| T3-076 | - | - | - | - | 5 |
| T3-079 | - | - | - | - | 1 |
| T3-080 | discriminators 1 | 1 | scheme-ambiguous | pair T3-177/T3-080 | 0 |
| T3-081 | - | - | - | - | 2 |
| T3-082 | - | - | - | - | 1 |
| T3-084 | discriminators 2 | 1 | scheme-ambiguous | pair T3-002/T3-084, pair T3-084/T3-010 | 1 |
| T3-087 | discriminators 1 | 1 | author-error | orderofthebluecorner/t08 | 2 |
| T3-088 | - | - | - | - | 1 |
| T3-090 | - | - | - | - | 1 |
| T3-091 | - | - | - | - | 3 |
| T3-092 | decide when both 1 | 1 | scheme-ambiguous | dofus/t01 | 2 |
| T3-093 | - | - | - | - | 1 |
| T3-098 | discriminators 1 | 1 | scheme-ambiguous | pair T3-098/T3-136 | 0 |
| T3-100 | discriminators 1 | 1 | scheme-ambiguous | pair T3-100/T3-023 | 0 |
| T3-101 | - | - | - | - | 2 |
| T3-104 | discriminators 1 | 1 | scheme-ambiguous | pair T3-104/T3-072 | 0 |
| T3-105 | discriminators 1 | 1 | scheme-ambiguous | pair T3-131/T3-105 | 2 |
| T3-115 | discriminators 2 | 1 | scheme-ambiguous | pair T3-115/T3-011, pair T3-115/T3-012 | 0 |
| T3-116 | - | - | - | - | 1 |
| T3-118 | discriminators 1 | 1 | scheme-ambiguous | pair T3-118/T3-185 | 0 |
| T3-121 | discriminators 1 | 1 | author-error | orderofthebluecorner/t08 | 0 |
| T3-122 | - | - | - | - | 3 |
| T3-123 | discriminators 1 | 1 | scheme-ambiguous | pair T3-123/T3-010 | 1 |
| T3-126 | - | - | - | - | 2 |
| T3-130 | - | - | - | - | 3 |
| T3-131 | discriminators 1 | 1 | scheme-ambiguous | pair T3-131/T3-105 | 0 |
| T3-132 | - | - | - | - | 1 |
| T3-136 | discriminators 1 | 1 | scheme-ambiguous | pair T3-098/T3-136 | 1 |
| T3-138 | - | - | - | - | 1 |
| T3-139 | discriminators 1 | 1 | scheme-ambiguous | pair T3-139/T3-010 | 1 |
| T3-140 | discriminators 1 | 1 | scheme-ambiguous | pair T3-140/T3-063 | 1 |
| T3-141 | - | - | - | - | 1 |
| T3-144 | discriminators 1 | 1 | scheme-ambiguous | pair T3-144/T3-002 | 1 |
| T3-146 | - | - | - | - | 1 |
| T3-147 | - | - | - | - | 1 |
| T3-149 | discriminators 1 | 1 | scheme-ambiguous | pair T3-194/T3-149 | 3 |
| T3-150 | discriminators 2 | 1 | scheme-ambiguous | pair T3-194/T3-150, pair T3-195/T3-150 | 5 |
| T3-151 | discriminators 2 | 1 | scheme-ambiguous | pair T3-194/T3-151, pair T3-195/T3-151 | 3 |
| T3-157 | decide when both 1 | 3 | scheme-ambiguous | pair T3-009/T3-157 | 0 |
| T3-158 | - | - | - | - | 1 |
| T3-159 | discriminators 1 | 1 | scheme-ambiguous | pair T3-159/T3-072 | 1 |
| T3-165 | - | - | - | - | 1 |
| T3-169 | discriminators 1 | 1 | scheme-ambiguous | cubers/t12 | 0 |
| T3-171 | - | - | - | - | 1 |
| T3-174 | - | - | - | - | 2 |
| T3-175 | - | - | - | - | 2 |
| T3-177 | discriminators 1 | 1 | scheme-ambiguous | pair T3-177/T3-080 | 0 |
| T3-179 | - | - | - | - | 1 |
| T3-181 | - | - | - | - | 1 |
| T3-182 | - | - | - | - | 1 |
| T3-185 | discriminators 1 | 1 | scheme-ambiguous | pair T3-118/T3-185 | 2 |
| T3-188 | - | - | - | - | 1 |
| T3-192 | discriminators 1 | 1 | scheme-ambiguous | pair T3-192/T3-061 | 1 |
| T3-194 | discriminators 3 | 1 | scheme-ambiguous | pair T3-194/T3-149, pair T3-194/T3-150, pair T3-194/T3-151 | 2 |
| T3-195 | discriminators 3 | 1, 2 | scheme-ambiguous | nVade/t04, pair T3-195/T3-150, pair T3-195/T3-151 | 0 |
| T3-197 | discriminators 1 | 1 | scheme-ambiguous | pair T3-197/T3-015 | 1 |

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
