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

