# Room forms, D4a-08: the changes and the codes

Leg D4a-08, 26 October 2026, an addition after the 35 branches, as at D4a-05 to D4a-07. J, through the handler, 21:05 Berlin: "How about using the code counts, dimensions for example, as well?" 21:06: "Yes. Please also tell it not to close but write us so we can iterate." 21:09: "Tell it to use the code counts as deviations from a mean normalized use. Same as the changes, 0 should be the global model." The amendment is dated in `departures.jsonl` (line 15).

This leg is not closed. The cut is written down here for J and the handler to answer, and `done.sh` waits until I am told to run it. Nothing earlier is replaced: `branches.jsonl`, `crosslinks.jsonl`, `tree-D4.md`, the forms, `room-forms-D4a05.*` to `room-forms-D4a07.*` and every D5 file are unchanged; I checked 87 files against the D4a-07 close snap (`_analysis/d4a08_unchanged.py`).

Files: `room-forms-D4a08.jsonl` (the five forms and the core, with members), `room-forms-D4a08.tsv` (one row per room), and this file. The computation is `_analysis/d4a08b_room_forms.py`; its rule, and the two amendments made while running it, are in the diary.

## 1. The two blocks

**The change block** is D4a-07's, unchanged. A room's selected changes count at the third-order themes, fourth-order themes and dimensions, with the arrows and link ops lifted as links. A room with no change sits at 0, the global model. The changes say where the model failed a room.

**The code block** follows J's 21:09 message. For each level, I take a room's share of its coded concepts on each node, minus the mean share over all 705 rooms. A room that uses its codes like the average room sits at 0. The concepts are lifted through their second-order theme's placements: 112,999 of the 115,388 reach a fourth-order theme; 1,982 sit on the two residue themes and count at the third-order level only; 407 have no placement. The codes say what a room did.

**No z-scores.** Dividing each node by its spread across rooms would give rare themes the same weight as common ones. A room with few codes (the smallest has 1, the median 101) would take large scores from one or two concepts on a rare theme. Raw deviations keep each node's weight in proportion to how much rooms differ on it.

**How the blocks combine.** The two blocks count equally, and within each block the three levels count equally. Each is scaled to the same total variance over the 558 defining rooms. The codes are nodes only; the arrow links stay in the change block.

**A first form, superseded.** Before J's 21:09 message I had run the code block as Hellinger distances on the shares. That run (`_analysis/d4a08_forms_hellinger_superseded.json`) is kept and not delivered. It carried 6 forms, and its forms agree with D4a-07's at 0.051.

## 2. The handler's proposals

- **(a) Equal weight: taken, by total variance.** But equal variance is not equal influence. Within the five forms, the code block's between-form share of its variance is 0.271, and the change block's is 0.051. The cut follows the codes. The code variance runs along a few strong directions (the April Fools frame, the order between rooms, repair); the change variance is spread thin over 673 columns. This is the main question for J (section 10).
- **(b) Shares, not counts: taken,** as deviations from the mean share, as J asked.
- **(c) Codes as nodes: taken.**
- **(d) The split-half check: taken** (section 6).
- **(e) The reports: given** (sections 4 to 8).
- **(f) Kept:** the floor of 5 selected changes, and placement by the whole mix of both blocks. **Changed:** the count. Stability against a shuffled null cannot choose it for this distance (section 3), so the merge-height gap carries it, and the stability rule's cut is given in full (section 8).

## 3. The count

{{TABLE:count}}

**The gap carries k = 5** (lifetime 0.290, against 0.220 to 0.221 at k = 4 and 6, 0.215 at 7, and 0.020 at 8).

**Why the shuffled null fails here.** The real stability is flat, 0.24 to 0.26 at every k, and the shuffled copies come out more stable, 0.28 to 0.53. I first shuffled raw code counts. That mixes rooms of 1 to 2,054 concepts, so each shuffled room's shares pile onto whichever column drew a large count. I then permuted each node's deviations across rooms instead (an amendment logged after seeing the output). The null was still more stable. Each node keeps its skewed distribution, so the rooms that draw its extreme values form a tight group in every subsample: at k = 4 one copy splits 420, 61, 60 and 17 rooms. The adjusted Rand scores such degenerate cuts as stable. So this test cannot tell structure from its absence for this distance, and I did not use it to choose.

## 4. The five forms

By Ward on the defining rooms the forms hold 161, 143, 101, 100 and 53 rooms (ratio 3.04). Placed by the whole mix they hold 182, 174, 133, 113 and 82 (ratio 2.22).

{{TABLE:forms}}

- **A, the middle, with a raiding core.** No change signature. Ward's own split of A gives 23 rooms whose changes include attack calls in 96 per cent of them, and 138 with no lean. A is the population's middle, as B was at D4a-07, and it holds the raiding core (section 7).
- **B, keeping.** The keeping lines add conditions and steps: r/floridagators attempts a first maintenance bot; r/soylent records a defence after the close. Their codes lean to repair, mobilization, traded help and blame.
- **C, the terms between neighbours.** r/riskofrain sends negotiation to a chat where a representative must ask for diplomatic status; in r/detroitredwings a promise of shared upkeep is offered and not shown kept. Changes and codes agree: the order between rooms holds 38 per cent of their codes, against 22 in the average room.
- **D, the sub's April Fools play.** r/ontario enacts fake rules by bans and mock sanctions; r/GuildWars2 tolerates the play but not an extended unreadable styling. The frame holds 46 per cent of their codes, against 12 in the average room, and 26 of the 33 takeover rooms are here.
- **E, the design and its marking.** In r/kindafunny members judge newly taken neighbour pixels indefensible and spare them; r/CSUFoCo keeps trying to restore its spot despite fewer hands. These are small records (median 49.5 coded concepts).

{{TABLE:accounts}}

## 5. What the codes did to the D4a-07 forms

The adjusted Rand index against D4a-07's forms is 0.072, so adding the codes reorganizes the forms.

{{TABLE:cross}}

- **Kept:** D4a-07's borders form G goes mostly to C (45 of 59), and its frame form H mostly to D (24 of 51).
- **Spread:** D4a-07's middle B spreads over all five (48, 44, 28, 26 and 13).
- **Dissolved:** machine hands (D4a-07's D) go mostly to the middle A (37 of 64); the spot (F) and the chat (E) spread. Their rooms change the model in the same way, but their codes do not set them apart.

## 6. The split-half check

Each concept went at random to half A or half B. Cut on the changes with half A, the forms differ on half B's codes well beyond chance: pseudo-F 39.2, against a null 95th percentile of 1.41 (p = 0.001), with 22.1 per cent of the variation. Assigned to the nearest form centre on half B, 62.9 per cent of rooms land in their own form, against 17.5 per cent with shuffled labels. Cut on the changes with half A and with half B, the two cuts agree at 0.191, and each agrees with the D4a-07 change-only forms at 0.04. So the forms carry code structure that a held-out half reproduces, but the exact membership moves with the half used.

## 7. The raiding and takeover rooms, the core and r/startrek

{{TABLE:sets}}

- **Raiding.** The 21 rooms with a quarter or more of their changes on attack calls hold together beyond chance in the combined space (silhouette 0.049 against a random-group 95th percentile of 0.038, p = 0.009), more weakly than on the changes alone (0.098). 13 of them sit in A, and A's own split isolates 23 raiding rooms. At k = 8 they make a form of their own (G, section 8).
- **Takeover rooms.** With the codes they come together: 26 of the 33 are in D, the April Fools play.
- **The core** stays together, as the instruction says. Placed by their codes alone, its rooms spread over the five forms. r/startrek, the core's one rich room (137 coded concepts, every accepted line an instantiation), is nearest D: its codes lean to the April Fools frame.

{{TABLE:core}}

## 8. The eight-form cut, the stability rule's choice

{{TABLE:alt}}

At k = 8 the size ratio is 7.25 (174 to 24), and the cut barely lasts in the joining (lifetime 0.020). Two forms appear that the five-form cut holds inside others. G is raiding as the work: 23 defining rooms, attack calls in 96 per cent of them, codes leaning to attack calls, workarounds, symbolic boundaries and rivalry. H is a set of rooms whose records are mostly the April Fools play (the frame holds 67 per cent of their codes). C is again a middle with a weak signature.

## 9. Kinds or a continuum, and size

**Still a continuum,** but with clearer poles than before. Real stability is 0.24 to 0.26 at every k. The forms differ strongly by their codes (section 6), and they differ in room size: the median room has 49.5 coded concepts in E and 181 in D (Kruskal-Wallis H = 78.1). Shares remove the number of codes from the distance. But a small record's shares are coarse, and the April Fools rooms have large records.

## 10. For J and the handler: what to iterate on

1. **The weight of the codes.** At equal variance the codes carry most of the separation (0.27 against 0.05). Should the change block weigh more (for example two thirds), or should the blocks be balanced by their between-form contribution rather than their variance?
2. **Five forms or eight.** The gap says 5; at 8, raiding becomes a form of its own, but the sizes run from 174 to 24.
3. **The April Fools play (D).** With the codes it is a form, and the sub's play sits beside the canvas work. Keep it as a form, or set it apart as the frame, as the account does?
4. **The count.** The shuffled null fails for this distance. Is the gap alone acceptable, or should I build another null (for example, one that redraws each room's codes from the population's mean use at the room's own size)?
5. **The core.** Keep the 21 together, or place them by their codes, as section 7 shows they could be?

## 11. The room table

One row per room, in case-ignored order (also in `room-forms-D4a08.tsv`, with the coded-concept counts and both branches). The form is placed by the whole mix of both blocks; a thin room is marked. The k = 8 and D4a-07 forms are given beside it.

{{TABLE:rooms}}
