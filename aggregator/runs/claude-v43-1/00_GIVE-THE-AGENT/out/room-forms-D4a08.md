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

| k | Ward merge height: the cut begins | ends | lifetime (the gap) | stability: matched subsamples | shuffled null mean | null 95th percentile | margin | sizes of the real cut | sizes of one shuffled copy's cut |
|---|---|---|---|---|---|---|---|---|---|
| 4 | 4.2322 | 4.4525 | 0.2203 | 0.2557 | 0.5310 | 0.7341 | -0.2753 | 304, 101, 100, 53 | 420, 61, 60, 17 |
| 5 | 3.9428 | 4.2322 | 0.2895 | 0.2413 | 0.3493 | 0.4816 | -0.1080 | 161, 143, 101, 100, 53 | 268, 152, 61, 60, 17 |
| 6 | 3.7216 | 3.9428 | 0.2212 | 0.2370 | 0.3178 | 0.4309 | -0.0808 | 161, 143, 101, 81, 53, 19 | 159, 152, 109, 61, 60, 17 |
| 7 | 3.5063 | 3.7216 | 0.2153 | 0.2404 | 0.2971 | 0.3919 | -0.0567 | 143, 138, 101, 81, 53, 23, 19 | 159, 152, 109, 60, 46, 17, 15 |
| 8 | 3.4863 | 3.5063 | 0.0200 | 0.2400 | 0.2820 | 0.3716 | -0.0421 | 143, 101, 89, 81, 53, 49, 23, 19 | 159, 152, 90, 60, 46, 19, 17, 15 |

**The gap carries k = 5** (lifetime 0.290, against 0.220 to 0.221 at k = 4 and 6, 0.215 at 7, and 0.020 at 8).

**Why the shuffled null fails here.** The real stability is flat, 0.24 to 0.26 at every k, and the shuffled copies come out more stable, 0.28 to 0.53. I first shuffled raw code counts. That mixes rooms of 1 to 2,054 concepts, so each shuffled room's shares pile onto whichever column drew a large count. I then permuted each node's deviations across rooms instead (an amendment logged after seeing the output). The null was still more stable. Each node keeps its skewed distribution, so the rooms that draw its extreme values form a tight group in every subsample: at k = 4 one copy splits 420, 61, 60 and 17 rooms. The adjusted Rand scores such degenerate cuts as stable. So this test cannot tell structure from its absence for this distance, and I did not use it to choose.

## 4. The five forms

By Ward on the defining rooms the forms hold 161, 143, 101, 100 and 53 rooms (ratio 3.04). Placed by the whole mix they hold 182, 174, 133, 113 and 82 (ratio 2.22).

| form | what its rooms change and do | defining rooms (Ward) | placed | change signature: fourth-order nodes and links (share; times the population; members holding it) | codes most above the average room (form's share against the mean share) | median coded concepts | one kind or a mixture |
|---|---|---|---|---|---|---|---|
| A | the middle, with a raiding core | 161 | 182 | none | Workarounds (0.042 against 0.022); Repertoire of contention (0.048 against 0.031); Territoriality (0.063 against 0.051) | 123.5 | a mixture |
| B | keeping: defence and repair, with the hands for them | 143 | 174 | Repair work (0.11; 1.6; 73%) | Repair work (0.135 against 0.095); Mobilization (0.083 against 0.059); Reciprocity (0.055 against 0.035) | 97 | one kind |
| C | the terms between neighbours | 101 | 133 | Negotiated order (0.20; 2.0; 83%); Negotiated order > Live and let live (0.03; 1.7; 50%) | Negotiated order (0.189 against 0.093); Territoriality (0.084 against 0.051); Live and let live (0.041 against 0.024) | 84 | one kind |
| D | the sub's April Fools play | 100 | 113 | Keying (0.13; 3.6; 72%) | Keying (0.463 against 0.120); Direct information sharing (0.041 against 0.033); Boundary work (0.021 against 0.021) | 181 | one kind |
| E | the design and its marking | 53 | 82 | Collective representation (0.24; 2.9; 94%); Completion ritual (0.06; 1.6; 43%) | Collective representation (0.260 against 0.117); Repair work (0.144 against 0.095); Completion ritual (0.100 against 0.079) | 49.5 | one kind |
| K | the core: no selected change | | 21 | none | | | |

- **A, the middle, with a raiding core.** No change signature. Ward's own split of A gives 23 rooms whose changes include attack calls in 96 per cent of them, and 138 with no lean. A is the population's middle, as B was at D4a-07, and it holds the raiding core (section 7).
- **B, keeping.** The keeping lines add conditions and steps: r/floridagators attempts a first maintenance bot; r/soylent records a defence after the close. Their codes lean to repair, mobilization, traded help and blame.
- **C, the terms between neighbours.** r/riskofrain sends negotiation to a chat where a representative must ask for diplomatic status; in r/detroitredwings a promise of shared upkeep is offered and not shown kept. Changes and codes agree: the order between rooms holds 38 per cent of their codes, against 22 in the average room.
- **D, the sub's April Fools play.** r/ontario enacts fake rules by bans and mock sanctions; r/GuildWars2 tolerates the play but not an extended unreadable styling. The frame holds 46 per cent of their codes, against 12 in the average room, and 26 of the 33 takeover rooms are here.
- **E, the design and its marking.** In r/kindafunny members judge newly taken neighbour pixels indefensible and spare them; r/CSUFoCo keeps trying to restore its spot despite fewer hands. These are small records (median 49.5 coded concepts).

| form | could an account that differs from the global model be written? |
|---|---|
| A, the middle, with a raiding core | No for the form as a whole. Its raiding half might carry one (attack calls as the room's work), and is a candidate for the split below. |
| B, keeping: defence and repair, with the hands for them | In part. The conditions and steps on keeping (who covers the work, handoffs, sleep) are additions the model lacks; the rest is restricts. |
| C, the terms between neighbours | In part. The changes limit A04 and A05 (talk with neighbours can come before keeping; sparing holds where an agreement is known and accepted), limits the account already states in part. |
| D, the sub's April Fools play | Yes, for the frame: the sub's play is administered with steps the model holds only as a key (K01 add-step 111 lines). It is beside the canvas work, not a form of canvas organizing. |
| E, the design and its marking | In part. The design argued and the template not settling it bear on A11 (the held proposal); the other changes are restricts. |

## 5. What the codes did to the D4a-07 forms

The adjusted Rand index against D4a-07's forms is 0.072, so adding the codes reorganizes the forms.

| D4a-07 form | rooms | in D4a-08's A | B | C | D | E |
|---|---|---|---|---|---|---|
| A | 148 | 16 | 70 | 11 | 25 | 26 |
| B | 159 | 48 | 44 | 28 | 26 | 13 |
| C | 87 | 28 | 7 | 13 | 6 | 33 |
| D | 64 | 37 | 8 | 10 | 9 | 0 |
| E | 60 | 17 | 22 | 7 | 9 | 5 |
| F | 56 | 19 | 7 | 18 | 10 | 2 |
| G | 59 | 3 | 7 | 45 | 4 | 0 |
| H | 51 | 14 | 9 | 1 | 24 | 3 |

- **Kept:** D4a-07's borders form G goes mostly to C (45 of 59), and its frame form H mostly to D (24 of 51).
- **Spread:** D4a-07's middle B spreads over all five (48, 44, 28, 26 and 13).
- **Dissolved:** machine hands (D4a-07's D) go mostly to the middle A (37 of 64); the spot (F) and the chat (E) spread. Their rooms change the model in the same way, but their codes do not set them apart.

## 6. The split-half check

Each concept went at random to half A or half B. Cut on the changes with half A, the forms differ on half B's codes well beyond chance: pseudo-F 39.2, against a null 95th percentile of 1.41 (p = 0.001), with 22.1 per cent of the variation. Assigned to the nearest form centre on half B, 62.9 per cent of rooms land in their own form, against 17.5 per cent with shuffled labels. Cut on the changes with half A and with half B, the two cuts agree at 0.191, and each agrees with the D4a-07 change-only forms at 0.04. So the forms carry code structure that a held-out half reproduces, but the exact membership moves with the half used.

## 7. The raiding and takeover rooms, the core and r/startrek

| set | rooms | A | B | C | D | E | core |
|---|---|---|---|---|---|---|---|
| raiding core (a quarter or more of the changes on attack calls) | 21 | 13 | 2 | 3 | 3 | 0 | 0 |
| takeover (F02) | 33 | 4 | 3 | 0 | 26 | 0 | 0 |

- **Raiding.** The 21 rooms with a quarter or more of their changes on attack calls hold together beyond chance in the combined space (silhouette 0.049 against a random-group 95th percentile of 0.038, p = 0.009), more weakly than on the changes alone (0.098). 13 of them sit in A, and A's own split isolates 23 raiding rooms. At k = 8 they make a form of their own (G, section 8).
- **Takeover rooms.** With the codes they come together: 26 of the 33 are in D, the April Fools play.
- **The core** stays together, as the instruction says. Placed by their codes alone, its rooms spread over the five forms. r/startrek, the core's one rich room (137 coded concepts, every accepted line an instantiation), is nearest D: its codes lean to the April Fools frame.

| core room | the form its codes alone are nearest (k = 5) |
|---|---|
| r/bannedfromanime_irl | B |
| r/churchofhelix | B |
| r/GreenEmpire | C |
| r/greenland | E |
| r/Lugarix | B |
| r/mcgillrobotics | B |
| r/n64 | D |
| r/nonbinary | B |
| r/NovaScotia | E |
| r/pgang | E |
| r/PokemonSage | C |
| r/quq | B |
| r/Redox | B |
| r/sakartvelo | E |
| r/signal | B |
| r/startrek | D |
| r/TheID | B |
| r/UMiami | A |
| r/UNLincoln | B |
| r/wario | A |
| r/yerbamate | B |

## 8. The eight-form cut, the stability rule's choice

| form at k = 8 | reading | defining rooms (Ward) | placed | change signature | codes most above the average room |
|---|---|---|---|---|---|
| A | keeping | 143 | 174 | Repair work (0.11; 1.6; 73%) | Repair work (0.135 against 0.095); Mobilization (0.083 against 0.059); Reciprocity (0.055 against 0.035) |
| B | the terms between neighbours | 101 | 128 | Negotiated order (0.20; 2.0; 83%); Negotiated order > Live and let live (0.03; 1.7; 50%) | Negotiated order (0.189 against 0.093); Territoriality (0.084 against 0.051); Live and let live (0.041 against 0.024) |
| C | the middle (a mixture) | 89 | 97 | Workarounds (0.08; 2.0; 35%) | Collective representation (0.160 against 0.117); Negotiated order (0.121 against 0.093); Boundary work (0.040 against 0.021) |
| D | the April Fools play | 81 | 91 | Keying (0.10; 2.7; 72%); Collective memory (0.05; 1.6; 40%) | Keying (0.415 against 0.120); Direct information sharing (0.044 against 0.033); Boundary work (0.025 against 0.021) |
| E | the design and its marking | 53 | 82 | Collective representation (0.24; 2.9; 94%); Completion ritual (0.06; 1.6; 43%) | Collective representation (0.260 against 0.117); Repair work (0.144 against 0.095); Completion ritual (0.100 against 0.079) |
| F | the spot and the report | 49 | 58 | Territoriality (0.16; 3.3; 69%); Direct information sharing (0.06; 2.7; 43%) | Territoriality (0.156 against 0.051); Direct information sharing (0.076 against 0.033); Keying (0.150 against 0.120) |
| G | raiding as the work | 23 | 30 | Repertoire of contention (0.17; 8.0; 96%); Workarounds (0.07; 1.7; 48%) | Repertoire of contention (0.177 against 0.031); Workarounds (0.074 against 0.022); Symbolic boundaries (0.032 against 0.004) |
| H | the April Fools play, most of the record | 19 | 24 | Keying (0.26; 7.3; 74%); Mobilization (0.08; 2.9; 53%); Mobilization > Direct information sharing (0.02; 2.2; 37%) | Keying (0.668 against 0.120); Visibility returns (0.012 against 0.013); Mobilization (0.057 against 0.059) |

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

| room | form (k = 5) | form at k = 8 | D4a-07 form | secondary forms | near-equal centres | changes | coded concepts | primary branch |
|---|---|---|---|---|---|---|---|---|
| 2007scape | E | E | E |  |  | 13 | 1445 |  |
| 49ers | B | A | G | C | C | 14 | 98 | F10 |
| 4chan | D | D | H |  |  | 13 | 299 | F01 |
| aceattorney | B | A | A |  |  | 15 | 121 |  |
| acecombat | D | D | B |  |  | 9 | 64 | F02 |
| AceOfAngels8 | D (thin) | H | B | E |  | 1 | 32 |  |
| AcePlace | C | B | B |  |  | 9 | 133 | F17 |
| achievement_hunter | C (thin) | F | F |  | A, B | 3 | 36 |  |
| adventuretime | C | B | F |  |  | 13 | 123 | F09 |
| aeon | A | C | D |  | B, E | 7 | 7 | F19 |
| aeskwadraat | E (thin) | E | C |  |  | 3 | 18 | F12 |
| afip | A (thin) | E | D | E | B, E | 3 | 75 | F19 |
| aggies | E | E | C |  | A, C | 12 | 158 |  |
| ainbowroad | C | B | E |  |  | 19 | 2054 |  |
| albania | A (thin) | C | C | E | E | 3 | 69 |  |
| alberta | A | C | H |  |  | 9 | 42 |  |
| AMD | A | C | C | D, E |  | 11 | 441 | F01 |
| AmericanFlaginPlace | B | A | A |  | A, E | 23 | 609 | F08 |
| anaheimducks | B | A | A |  |  | 16 | 94 | F14 |
| anarchism | A | G | D |  |  | 5 | 124 |  |
| anarcho_capitalism | B | A | A |  |  | 12 | 204 |  |
| anarchocapitalism | B (thin) | G | A |  |  | 1 | 12 |  |
| androidgaming | B | A | A |  |  | 16 | 46 |  |
| animalcrossing | B | A | F |  | A, C | 10 | 154 | F09 |
| anime | A | C | G |  | B | 24 | 214 | F19 |
| anime_irl | D | H | H |  |  | 5 | 175 | F01 |
| aoe2 | A (thin) | C | C | E | B | 2 | 245 | F34 |
| apocalypserising | A | C | B | E | B | 6 | 51 |  |
| AprilKnights | A | C | E |  | C | 6 | 101 | F16 |
| araragi | E | E | B |  | A | 5 | 33 |  |
| archlinux | B | A | C | E | A, C, E | 11 | 249 | F07 |
| argentina | A | G | E |  |  | 8 | 609 |  |
| armenia | C | B | B |  | A, B | 5 | 167 |  |
| armok | B | A | E |  | A, E | 14 | 75 | F27 |
| aromantic | A (thin) | F | B |  | C, E | 2 | 9 |  |
| asexual | A | G | B |  | B | 6 | 57 |  |
| asexuality | C | B | A | B | B | 15 | 91 | F17 |
| asktransgender | B (thin) | A | B | D |  | 4 | 177 |  |
| auburn | B (thin) | A | G | C | C | 4 | 49 |  |
| australia | A | C | H | E |  | 7 | 409 | F07 |
| austria | A | G | B | C |  | 16 | 131 |  |
| austriahungary | E (thin) | E | C |  |  | 1 | 2 |  |
| AvoArmy | E | E | C |  |  | 12 | 230 | F07 |
| AyyMD | B | A | A | E | A, C, E | 14 | 139 | F07 |
| azerbaijan | E (thin) | E | B |  | A | 3 | 8 | F19 |
| azores | E (thin) | E | B |  |  | 1 | 4 |  |
| babymetal | B | A | A |  |  | 25 | 243 | F22 |
| bahrain | D (thin) | H | H |  |  | 1 | 46 | F01 |
| bakchodi | A | G | H |  |  | 5 | 279 | F08 |
| bangladesh | A | C | E |  |  | 8 | 33 |  |
| bangtan | B | A | E |  |  | 12 | 105 | F17 |
| bannedfromanime_irl | K | K | K |  |  | 0 |  |  |
| bardmains | E | E | A |  |  | 16 | 85 | F07 |
| batman | D | D | G | C | A, B, C | 12 | 65 |  |
| battlecats | D | H | F |  |  | 9 | 201 | F02 |
| baylor | D | D | C | E | A, E | 5 | 17 | F33 |
| bdsm | E (thin) | E | C |  | A | 2 | 15 |  |
| bees | A (thin) | G | H |  | B, C | 1 | 5 |  |
| belgium | A | G | D |  |  | 13 | 246 | F24 |
| berkeley | C (thin) | B | F | E | A | 4 | 98 | F09 |
| berserk | B | A | F |  |  | 18 | 129 | F09 |
| bigbang | E (thin) | E | H |  | A | 2 | 3 |  |
| bih | E | E | A | B | B | 7 | 43 |  |
| bindingofisaac | B | A | A |  |  | 23 | 332 | F01 |
| bisexual | B | A | A | C | A, C | 23 | 150 | F07 |
| bitcoin | A | C | C | C |  | 8 | 484 |  |
| blackmirror | E (thin) | E | C |  |  | 4 | 62 |  |
| bobross | E (thin) | E | B |  | A, B | 4 | 12 |  |
| borderlands | E | E | A | B |  | 6 | 31 | F27 |
| borussiadortmund | D | D | H |  |  | 19 | 99 | F21 |
| bostonbruins | B | A | G | C |  | 7 | 203 | F32 |
| bostonceltics | A | F | B |  |  | 8 | 145 | F04 |
| brasil | A | C | E |  | B | 10 | 568 |  |
| Bravenewbies | B (thin) | A | E | E | A, E | 2 | 7 |  |
| Braveryjerk | A (thin) | G | H |  | B, C | 1 | 4 |  |
| bretagne | E | E | A | B |  | 6 | 42 |  |
| btc | D (thin) | D | G | C |  | 4 | 221 | F28 |
| buffalo | B | A | H |  | A | 10 | 50 | F12 |
| buffalobills | C | B | G |  |  | 17 | 135 | F10 |
| buffalowizards | B | A | F |  |  | 5 | 31 | F09 |
| bulgaria | B | A | C | E | A, C | 16 | 97 |  |
| calgaryflames | A | G | B |  | B | 6 | 295 | F09 |
| calvinandhobbes | E | E | C |  |  | 7 | 91 | F07 |
| canada | A | C | B |  | B | 13 | 543 | F01 |
| canucks | A | G | B |  |  | 25 | 201 | F01 |
| cardinals | A | F | B |  |  | 11 | 102 |  |
| carletonu | C (thin) | B | G |  |  | 3 | 7 |  |
| catalonia | A | C | D |  | C, E | 8 | 45 | F08 |
| catalunya | C | B | G |  |  | 18 | 69 | F07 |
| catholicism | A | F | H |  | D | 9 | 142 | F23 |
| cavestory | C | B | D |  |  | 7 | 82 | F10 |
| CelticFc | C (thin) | B | G |  |  | 1 | 18 | F28 |
| cfb | D | H | H |  |  | 7 | 559 | F02 |
| cgpgrey | B | A | B |  |  | 12 | 76 | F14 |
| chelseafc | B | A | A | E | A, D | 20 | 225 | F04 |
| chess | D | D | F |  |  | 9 | 79 | F33 |
| chibears | C | B | G |  |  | 7 | 184 | F09 |
| chicago | A | C | C | E |  | 19 | 108 | F07 |
| chicubs | B | A | A |  |  | 14 | 279 |  |
| chile | B | A | A |  | E | 22 | 173 | F21 |
| ChronoTrigger | B | A | A |  | C, E | 6 | 93 | F12 |
| churchofhelix | K | K | K |  |  | 0 |  |  |
| cirkeltrek | B (thin) | A | A |  |  | 3 | 308 |  |
| CKCrusaders | E | E | A |  |  | 8 | 86 |  |
| Clannad | B (thin) | A | A | E | E | 2 | 18 |  |
| clashroyale | D | H | H | C |  | 11 | 452 | F35 |
| clg | A | C | B |  | B | 14 | 87 | F32 |
| cloud9 | B | A | A |  | A | 10 | 83 | F12 |
| clubpenguin | A | F | B |  | B, C | 11 | 121 | F12 |
| cmu | A | F | D | C | C | 10 | 41 |  |
| coldplay | C | B | G |  |  | 14 | 82 | F07 |
| colombia | C (thin) | B | B |  |  | 4 | 81 | F22 |
| colorado | E (thin) | E | A | B |  | 3 | 35 | F15 |
| columbia | B | A | G |  |  | 11 | 46 | F15 |
| completeanarchy | B | A | D |  | A | 13 | 307 |  |
| compsoc | B (thin) | A | B | E | A, C | 2 | 9 |  |
| Cornwall | C (thin) | B | G |  |  | 1 | 11 |  |
| corridor | A | F | F |  | B, C | 15 | 58 | F25 |
| COSI | C (thin) | F | F |  |  | 1 | 7 |  |
| costa_rica | B | A | E |  | A, C | 8 | 87 |  |
| counting | B (thin) | A | B |  | A | 2 | 143 |  |
| cowchop | B | A | A |  |  | 13 | 103 | F24 |
| criticalrole | A | C | C |  |  | 19 | 87 | F01 |
| croatia | C (thin) | B | G | E |  | 4 | 237 | F07 |
| crusaderkings | A | C | A |  | B | 11 | 222 | F08 |
| CryptoFR | B (thin) | A | B |  | A, E | 3 | 10 |  |
| crystalclear | E (thin) | E | A | B |  | 2 | 8 | F34 |
| CSUFoCo | E | E | C |  |  | 5 | 13 | F33 |
| cubers | A | C | C | E | B, E | 12 | 320 | F12 |
| cuboulder | A (thin) | A | B |  | B, E | 1 | 35 |  |
| czech | C | B | A |  |  | 14 | 295 | F07 |
| daftpunk | B | A | G | C |  | 9 | 61 |  |
| dallasstars | A | F | D |  |  | 11 | 109 | F01 |
| danganronpa | D | D | D |  | A, B | 16 | 181 | F02 |
| dankmemes | D | H | H |  |  | 10 | 670 | F01 |
| darksouls | B | A | E |  |  | 8 | 185 | F16 |
| DatBoi | A | G | H |  | B, E | 5 | 50 |  |
| davidbowie | E (thin) | E | A |  |  | 4 | 43 | F15 |
| day9 | C (thin) | B | F |  |  | 3 | 38 | F09 |
| dbz | B | A | F | C | A, C, D | 14 | 137 | F01 |
| DCFU | B | A | B | C, E | C | 6 | 28 | F22 |
| de | A | C | B |  | B | 23 | 754 | F16 |
| denmark | B | A | E |  |  | 8 | 393 | F11 |
| denverbroncos | B | A | A |  |  | 20 | 95 | F03 |
| destiny | A (thin) | G | B |  |  | 4 | 96 | F22 |
| DestinyTheGame | A | F | A |  | B | 17 | 355 | F02 |
| detroitlions | D | D | B |  |  | 13 | 158 | F34 |
| detroitredwings | C | B | G |  |  | 12 | 229 |  |
| DevonUK | C (thin) | B | G |  | B | 2 | 24 |  |
| diablo | A | F | F |  | B, C | 9 | 57 |  |
| DiamondClub | E (thin) | E | B |  | A, B | 1 | 8 |  |
| dmt | E (thin) | E | H |  | B | 2 | 25 |  |
| dofus | E (thin) | E | C |  |  | 1 | 14 |  |
| Dominican | E | E | F |  |  | 10 | 82 |  |
| donaldglover | B | A | E |  | A | 12 | 144 | F11 |
| Dorset | C | B | G |  |  | 6 | 17 |  |
| dota2 | D | D | D |  |  | 15 | 1218 | F05 |
| dragonquest | C | B | C | E |  | 8 | 84 | F33 |
| drawhelix | E | E | A |  |  | 7 | 67 | F10 |
| drugs | A (thin) | C | C | C, E | E | 3 | 199 |  |
| drumcorps | D | D | A | C |  | 7 | 151 | F01 |
| duckgame | C | B | G |  |  | 7 | 68 |  |
| ducks | A | F | B |  | C, E | 5 | 14 |  |
| Dustforce | C (thin) | B | F |  |  | 4 | 47 | F09 |
| dwarffortress | E | E | E |  |  | 17 | 164 | F16 |
| eagles | B | A | B |  |  | 10 | 256 |  |
| earthbound | B | A | A | C |  | 12 | 105 | F10 |
| edboxes | B | A | A |  | A, C | 16 | 87 | F07 |
| eder | E (thin) | E | C |  |  | 2 | 17 | F20 |
| edmontonoilers | B | A | A |  | A | 12 | 142 |  |
| eesti | A | F | D |  | B, C | 8 | 115 | F08 |
| egypt | E (thin) | E | C |  |  | 4 | 27 | F22 |
| ElderScrolls | D | D | A | B, E |  | 6 | 25 | F01 |
| elitedangerous | D (thin) | D | A |  |  | 4 | 371 | F04 |
| ElSalvador | A | C | B |  | B, C | 5 | 14 |  |
| empiredidnothingwrong | B | A | A |  |  | 20 | 235 | F27 |
| england | A | G | B |  |  | 9 | 36 |  |
| enterthegungeon | B | A | B |  |  | 10 | 113 | F23 |
| epublica | C | B | D |  |  | 16 | 98 | F24 |
| EraseThePlace | C | B | B |  | A, B | 19 | 341 | F29 |
| esperanto | B | A | A |  | A | 11 | 91 | F12 |
| ethereum | D | D | B |  |  | 16 | 154 | F01 |
| ethoslab | A | F | F | C | B | 5 | 58 | F01 |
| europe | A | C | B |  |  | 17 | 822 |  |
| eve | A | C | E |  | B | 12 | 428 | F07 |
| evedreddit | C (thin) | B | G |  |  | 1 | 30 |  |
| evex | C | B | C |  |  | 13 | 94 | F08 |
| factorio | A | C | D |  | E | 9 | 232 | F07 |
| faeria | B | A | A | C |  | 14 | 73 | F18 |
| falcons | A | G | A |  |  | 11 | 203 | F01 |
| farmcarrots | E | E | C |  | C | 12 | 194 | F07 |
| FaroeIslands | C | B | B |  | A, B | 10 | 71 | F09 |
| FederationPlace | B | A | C |  | A, C | 15 | 66 | F08 |
| feedthebeast | D | D | A |  |  | 10 | 190 | F14 |
| Fez | A | C | A |  | B, C, E | 9 | 94 | F21 |
| FinalFantasy | B | A | B |  | A | 15 | 126 |  |
| finland | C | B | G |  |  | 6 | 87 |  |
| fireemblem | A | F | B |  | B, D | 10 | 480 |  |
| fivenightsatfreddys | D | D | A |  |  | 22 | 625 | F01 |
| FlaggyFlag | E | E | A | B |  | 7 | 34 | F07 |
| flashtv | D | D | F |  |  | 16 | 229 | F02 |
| FlipnoteStudio3D | B (thin) | A | H |  | A | 1 | 2 |  |
| floridagators | B | A | A |  | A | 5 | 141 |  |
| FloydVsVoid | C | B | E |  |  | 26 | 205 | F15 |
| flyers | A | F | B |  |  | 14 | 255 | F18 |
| formula1 | D | D | F |  |  | 6 | 465 | F02 |
| forsen | B | A | B |  |  | 15 | 114 | F12 |
| foxes | B | A | A |  |  | 16 | 102 | F31 |
| foxstevenson | A (thin) | F | F |  | C | 3 | 29 |  |
| france | A | C | D |  | B, C | 6 | 589 |  |
| frankocean | B | A | A |  |  | 21 | 260 | F27 |
| frc | B | A | A |  | A | 10 | 152 | F24 |
| freedomplanet | C | B | F |  | A, B, E | 6 | 58 | F19 |
| ftlgame | B | A | B |  | A, C | 7 | 93 | F18 |
| fullcommunism | B | A | A | E | A, E | 6 | 273 | F17 |
| funhaus | C | B | G |  |  | 15 | 307 | F30 |
| furry | C | B | G |  | A, B | 16 | 314 | F26 |
| furry_irl | A | F | B |  | B | 10 | 192 | F05 |
| futanari | B | A | B | E |  | 5 | 14 |  |
| futurama | E | E | A |  |  | 10 | 122 | F23 |
| fxKorea | E | E | C |  |  | 9 | 101 | F18 |
| GabrielDropout | E (thin) | E | C |  |  | 4 | 74 |  |
| gameattack | B | A | B |  | A | 11 | 56 | F21 |
| gameboy | A (thin) | F | F |  | B, E | 3 | 14 |  |
| gameofthrones | D | D | A |  |  | 10 | 152 | F02 |
| gamindustri | B | A | B |  | A | 20 | 181 | F12 |
| gatech | E | E | C |  |  | 19 | 124 | F08 |
| genderfluid | D (thin) | D | A | B |  | 4 | 15 |  |
| geometrydash | B | A | B | D | A, D | 8 | 85 | F01 |
| germany | C | B | G |  | A | 5 | 122 |  |
| ghibli | B | A | B |  | A, E | 6 | 61 | F15 |
| giantbomb | A | F | D |  |  | 15 | 250 |  |
| giivasunner | B | A | B |  | C | 11 | 231 | F09 |
| glasgow | D | D | A | B, E |  | 6 | 15 |  |
| globaloffensive | D | D | A |  |  | 9 | 1142 | F13 |
| Goodboye | B | A | A |  | C | 9 | 92 |  |
| gorillaz | E | E | A |  | B | 17 | 183 | F25 |
| GranColombia | E | E | E |  |  | 7 | 66 | F16 |
| gratefuldead | A | F | F |  | B | 8 | 85 |  |
| gravityfalls | A | C | A | E | B, C, E | 9 | 97 | F12 |
| greece | E | E | A |  |  | 11 | 194 | F27 |
| greenbaypackers | D | H | D |  |  | 11 | 232 |  |
| GreenCorner | C | B | A |  | B | 9 | 111 |  |
| GreenEmpire | K | K | K |  |  | 0 |  |  |
| greenland | K | K | K |  |  | 0 |  |  |
| greenlattice | C | B | B |  |  | 24 | 1217 | F12 |
| greyblob | B | A | B |  | C | 9 | 115 | F12 |
| GrowTheTree | E (thin) | E | C | C | B, C | 4 | 60 |  |
| GuardiansOfDatBoi | A | G | B |  | B, C | 7 | 47 | F15 |
| guatemala | E | E | C |  |  | 6 | 19 |  |
| GuildWars2 | D | H | H |  |  | 9 | 215 | F01 |
| h3h3productions | A | C | B |  | E | 12 | 171 | F21 |
| habs | A | F | B |  | D | 15 | 246 | F32 |
| halo | E | E | B |  | A | 8 | 425 |  |
| harrypotter | A | C | C | C, E | B, C | 8 | 329 | F01 |
| haskell | A (thin) | F | F |  |  | 3 | 88 |  |
| hatsune | C | B | A |  |  | 16 | 65 | F20 |
| hawks | D | D | A |  | B | 14 | 220 | F22 |
| hearthstone | D | D | C |  |  | 13 | 342 | F10 |
| hellointernet | E | E | B | C | B, C | 12 | 138 | F27 |
| hentai | B | A | C | E | E | 10 | 107 | F07 |
| heroesofthestorm | D | D | A | B | A, B | 9 | 415 | F01 |
| heyyea | E | E | C |  |  | 7 | 47 | F11 |
| homelab | D | D | B |  |  | 12 | 62 |  |
| HomestarRunner | A | G | H |  | B | 15 | 155 |  |
| homestuck | B | A | A |  |  | 9 | 303 | F35 |
| Homura | C (thin) | C | E |  | A, B | 1 | 30 |  |
| Honduras | E | E | B |  |  | 5 | 19 |  |
| hongkong | C | B | C | E | A, E | 7 | 74 | F07 |
| hoodr | C (thin) | B | B |  |  | 3 | 50 |  |
| hsv | B | A | A |  |  | 13 | 93 |  |
| httyd | A | F | B |  | B, C, E | 8 | 62 | F32 |
| hungary | C (thin) | B | G |  |  | 4 | 64 | F23 |
| hunterxhunter | D | D | B | C |  | 8 | 146 | F03 |
| hyperlightdrifter | C | B | D |  | A, E | 12 | 74 | F07 |
| iastate | E | E | A |  |  | 10 | 62 |  |
| ibo | B (thin) | A | H |  | A | 4 | 28 |  |
| ice_poseidon | B | A | H |  |  | 11 | 265 | F21 |
| iceland | C (thin) | B | G |  |  | 1 | 77 |  |
| ik_ihe | A (thin) | C | E |  |  | 2 | 15 | F16 |
| india | A | C | D |  |  | 14 | 504 | F08 |
| indieheads | A | F | F |  |  | 17 | 246 | F01 |
| indonesia | E | E | B |  | A, B, C | 16 | 226 | F25 |
| ireland | A | C | C |  | C | 10 | 513 |  |
| israel | C | B | C | E |  | 7 | 223 | F07 |
| italy | A | C | D |  | C | 9 | 335 | F12 |
| Jamaica | B | A | B |  | A, E | 8 | 54 | F15 |
| japan | E | E | B |  |  | 11 | 140 | F15 |
| jerma985 | B | A | A |  |  | 16 | 91 | F09 |
| k_on | B | A | B |  | A | 8 | 27 |  |
| kamenrider | B | A | A |  |  | 11 | 49 | F15 |
| kanye | B | A | A |  |  | 14 | 471 | F06 |
| katawashoujo | E | E | C |  |  | 6 | 52 | F07 |
| kcroyals | A | C | B |  |  | 10 | 123 | F18 |
| kerbalspaceprogram | D | H | A |  |  | 10 | 227 | F01 |
| kilian | B | A | E | C |  | 5 | 91 | F16 |
| kindafunny | E | E | C |  |  | 6 | 24 | F34 |
| kingdomhearts | A | F | C |  | D | 9 | 221 | F09 |
| kirby | D | D | A | E | A, B, C | 7 | 74 | F18 |
| konosuba | B | A | C | E | A, C, E | 5 | 79 | F33 |
| korea | A | C | G | E |  | 15 | 163 | F07 |
| kpop | A | F | H | E |  | 7 | 94 | F01 |
| KState | A | F | D |  |  | 13 | 67 | F08 |
| kurdistan | C | B | B |  | A | 7 | 43 | F10 |
| kuwait | E | E | A |  |  | 10 | 26 | F33 |
| lakers | A | C | B |  | B | 13 | 236 | F16 |
| landry | C (thin) | B | G |  |  | 4 | 12 |  |
| latin | A | F | F |  | B, C, E | 9 | 33 |  |
| latvia | C | B | B |  | A, E | 8 | 65 |  |
| leafs | A | C | C | C |  | 7 | 329 |  |
| leagueoflegends | D | D | E | E |  | 7 | 1913 |  |
| lebanon | C | B | A |  |  | 12 | 222 | F35 |
| lego | D | D | B |  |  | 12 | 217 | F13 |
| lexington | B (thin) | A | H |  | A, E | 2 | 15 |  |
| lifeisstrange | C | B | G |  | A, B | 10 | 75 | F26 |
| linux | A | C | D |  | B | 11 | 133 | F10 |
| liquicity | C | B | A |  | A, B | 11 | 70 | F15 |
| lithuania | C | B | B |  | A | 8 | 121 | F16 |
| littlebusters | E (thin) | E | B |  | A, B | 1 | 4 |  |
| littlewitchacademia | B | A | A |  |  | 13 | 63 | F10 |
| livecounting | B (thin) | A | D |  | A, C | 4 | 61 | F08 |
| liverpoolfc | D | D | E |  | A | 6 | 195 | F29 |
| lofihiphop | A | C | E |  | D | 6 | 12 | F15 |
| loliconsunite | B | A | E |  |  | 16 | 88 | F23 |
| loltyler1 | A | G | D |  |  | 10 | 218 | F08 |
| lost | B | A | B | E | E | 8 | 84 |  |
| lovelive | A | F | B |  | B | 9 | 79 | F13 |
| lsu | C | B | F |  |  | 13 | 97 | F09 |
| luciomains | E | E | C |  |  | 9 | 103 | F19 |
| Lugarix | K | K | K |  |  | 0 |  |  |
| luxembourg | A | G | B |  | B | 11 | 19 | F32 |
| Madeon | D | D | C | E |  | 5 | 41 |  |
| madokamagica | A | C | E |  |  | 9 | 109 |  |
| magictcg | D | D | B |  |  | 16 | 353 | F01 |
| malaysia | C | B | G |  |  | 11 | 209 | F09 |
| malta | E | E | A |  |  | 5 | 52 |  |
| mamamoo | C (thin) | B | H |  | B | 1 | 10 | F35 |
| ManningPlace | C | B | G |  |  | 5 | 55 | F26 |
| Mario | B (thin) | A | B |  | A | 2 | 20 | F12 |
| mariokart | D (thin) | H | H |  |  | 4 | 16 | F03 |
| marvel | D | D | F |  |  | 7 | 56 | F34 |
| maryland | A | C | A |  | B, C, E | 8 | 292 | F22 |
| masseffect | C | B | F |  | A | 9 | 238 | F09 |
| math | B | A | A | C |  | 12 | 84 |  |
| mcgill | D (thin) | D | E |  |  | 1 | 77 | F16 |
| mcgillrobotics | K | K | K |  |  | 0 |  |  |
| mechanicalkeyboards | D | D | G | C |  | 14 | 200 | F26 |
| megaman | B | A | A |  | C | 15 | 74 | F07 |
| metalcore | D | D | A | B | B | 14 | 170 | F27 |
| metalgearsolid | A | C | C | E |  | 13 | 159 | F01 |
| metroid | C | B | C |  |  | 15 | 214 | F26 |
| mexico | B | A | D |  | A, C, E | 8 | 379 | F08 |
| miamidolphins | B | A | G | C |  | 6 | 175 | F26 |
| MiamiHurricanes | C | B | F |  |  | 6 | 43 |  |
| mindcrack | C | B | C |  | B | 14 | 143 | F24 |
| minecraft | D | D | H |  |  | 15 | 269 | F01 |
| minnesotavikings | C | B | D |  | A | 9 | 322 | F08 |
| miraculousladybug | C (thin) | F | F | D | A, B | 4 | 28 | F05 |
| mit | C | B | A | E |  | 8 | 23 | F10 |
| mizzou | E | E | A | B | B | 8 | 44 |  |
| mls | D | D | D |  |  | 17 | 412 | F06 |
| MMA | D | D | B |  |  | 14 | 513 | F01 |
| monalisaclan | C | B | B |  |  | 17 | 264 | F15 |
| monero | A | C | D |  | C | 11 | 131 | F16 |
| MonkeyIsland | B | A | A |  | E | 10 | 31 | F15 |
| monstercat | D | H | D |  |  | 15 | 249 | F01 |
| monsterhunter | A | F | A |  |  | 6 | 213 |  |
| montenegro | E (thin) | E | E |  |  | 3 | 14 | F16 |
| Moondye7 | B | A | G | C |  | 6 | 71 | F19 |
| mordhau | C (thin) | B | F | B | B | 3 | 34 |  |
| morrowind | E | E | B |  |  | 15 | 108 | F07 |
| msu | C | B | D |  |  | 7 | 62 | F09 |
| muse | A | C | C | E |  | 6 | 159 | F07 |
| mylittlepony | B | A | B |  |  | 20 | 242 | F16 |
| mysterydungeon | B | A | B |  |  | 9 | 54 |  |
| n64 | K | K | K |  |  | 0 |  |  |
| naruto | A | F | B |  | B, D | 11 | 219 | F02 |
| nascar | D | H | G | C |  | 9 | 223 | F10 |
| natsume | E (thin) | E | A |  |  | 3 | 21 |  |
| nbaspurs | A | F | F |  | B, C | 21 | 243 | F01 |
| necrodancer | C | B | C | E |  | 8 | 97 | F09 |
| neopets | B | A | A |  | C | 16 | 105 | F29 |
| nerf | B | A | B |  | A, E | 10 | 85 | F15 |
| neu | C | B | D |  |  | 7 | 95 | F08 |
| neutralmilkhotel | C (thin) | B | G |  | B | 3 | 25 |  |
| NewMexico | C | B | C | E |  | 10 | 71 | F10 |
| newzealand | A | C | A |  | B | 14 | 453 | F07 |
| NieR | D | D | H | E |  | 8 | 130 | F05 |
| nightinthewoods | A | F | B |  |  | 14 | 93 | F01 |
| nin | A | C | C | E |  | 20 | 183 | F18 |
| nintendo | D | D | H |  |  | 16 | 158 | F01 |
| nlsscirclejerk | A | C | A | B, E |  | 11 | 91 | F34 |
| nonbinary | K | K | K |  |  | 0 |  |  |
| norge | A (thin) | C | H |  |  | 1 | 302 |  |
| Northwestern | C | B | F |  | A | 8 | 50 |  |
| norway | C | B | G |  | A | 13 | 111 |  |
| notredame | C | B | G |  |  | 9 | 101 | F07 |
| NovaScotia | K | K | K |  |  | 0 |  |  |
| npr | B | A | B |  | C | 9 | 63 |  |
| nuclearthrone | A | C | B |  | B, E | 10 | 86 | F33 |
| nVade | B | A | A | C | C | 14 | 96 |  |
| nyjets | A | F | B |  | B | 13 | 164 | F02 |
| nyu | E | E | B |  | A, B, C | 6 | 32 |  |
| ockytop | A | G | D |  | B | 9 | 107 | F15 |
| ohio | B | A | E |  | A, E | 10 | 132 | F10 |
| Okami | B | A | B | E |  | 8 | 54 | F19 |
| OKState | A | C | D |  | E | 7 | 28 | F08 |
| oltp | B (thin) | A | A |  | E | 1 | 1 |  |
| oman | E (thin) | E | H |  | A, B | 2 | 24 |  |
| OnePiece | B | A | B |  | A | 17 | 376 | F22 |
| oneplus | D | D | H | E |  | 6 | 81 | F01 |
| onepunchman | C (thin) | C | G |  | A | 4 | 130 | F10 |
| oneshot | C | B | B |  | B | 5 | 94 |  |
| OneTrueEmilia | D | D | A | B |  | 8 | 20 | F21 |
| ontario | D | H | H |  |  | 5 | 61 | F01 |
| opticgaming | C | B | G |  | A | 16 | 218 | F19 |
| orderofthebluecorner | C | B | B | B |  | 6 | 66 |  |
| OrderOfTheKoi | A | C | E |  | B, C | 7 | 21 | F16 |
| osu | D | D | H | E | A, B | 14 | 145 | F07 |
| osugame | B | A | E |  |  | 20 | 816 | F29 |
| overwatch | D | D | E |  |  | 23 | 1198 |  |
| pakistan | A | C | D |  | C | 12 | 277 | F08 |
| paladins | D | D | B |  |  | 25 | 317 | F01 |
| palestine | B | A | C | E | A, C, E | 5 | 96 | F34 |
| pansexual | C (thin) | B | G |  |  | 3 | 21 |  |
| parabola | B (thin) | A | A |  | C | 3 | 20 |  |
| paragon | D | H | H |  |  | 11 | 151 | F01 |
| parahumans | B | A | E |  |  | 15 | 196 | F25 |
| paranatural | C | B | F |  |  | 10 | 30 |  |
| parrots | E | E | A |  |  | 10 | 76 | F13 |
| partyparrot | B | A | E |  | A, C | 15 | 152 |  |
| pathofexile | A | C | E |  |  | 12 | 389 |  |
| patriots | B | A | B |  | A | 10 | 282 | F21 |
| paydaytheheist | D (thin) | D | B |  |  | 4 | 175 | F32 |
| pcmasterrace | D | D | A |  |  | 17 | 1106 | F25 |
| pebble | A | F | F |  |  | 13 | 55 | F09 |
| penguins | A | F | F |  |  | 14 | 108 | F09 |
| pepe | B | A | D |  | A | 8 | 40 | F08 |
| Peru | C | B | G | E |  | 12 | 88 | F30 |
| peterdraws | C (thin) | B | G | E |  | 3 | 10 |  |
| pgang | K | K | K |  |  | 0 |  |  |
| philippines | B | A | B |  | A, C, E | 12 | 595 | F15 |
| phish | A | C | D |  |  | 11 | 97 | F01 |
| physical_removal | B (thin) | A | A |  | A | 3 | 92 | F23 |
| picturegame | D (thin) | H | H |  |  | 4 | 13 | F25 |
| Pigifs | B (thin) | G | B | E | A, C | 4 | 38 |  |
| PinkUnion | C | B | F |  |  | 9 | 77 |  |
| PinkVomitMonster | B | A | E | C | C | 5 | 78 |  |
| pitt | A | C | C | E | B, C, E | 9 | 165 | F14 |
| placecanada | A | C | D |  | C, E | 13 | 206 |  |
| placeDE | A | C | H |  | E | 9 | 372 | F23 |
| placehearts | C | B | E | B |  | 6 | 417 |  |
| placehfarts | A (thin) | G | H |  | B, E | 1 | 15 |  |
| PlaceNL | A | C | D |  |  | 22 | 246 | F08 |
| placeportalpattern | C | B | G |  |  | 9 | 135 | F23 |
| placesnek | B | A | E |  | C | 13 | 115 |  |
| placestart | C | B | D |  |  | 12 | 477 | F15 |
| placetardis | C | B | G |  |  | 12 | 92 | F10 |
| planetside | A | F | E |  |  | 20 | 134 | F03 |
| pokemon | D | H | A | B |  | 8 | 540 | F27 |
| PokemonSage | K | K | K |  |  | 0 |  |  |
| poland | C | B | G |  |  | 10 | 117 | F10 |
| polandball | D | H | H | E |  | 7 | 149 | F02 |
| polska | A | C | E |  |  | 10 | 151 | F12 |
| polyamory | B | A | H |  | A | 5 | 7 | F35 |
| popheads | D | D | B |  |  | 10 | 296 | F01 |
| portal | A | F | F |  | B, E | 15 | 110 | F33 |
| porterrobinson | D | D | C | E | A, E | 17 | 144 | F07 |
| portugal | A | C | E |  | B | 17 | 343 | F13 |
| PORTUGALCARALHO | E (thin) | E | C |  |  | 3 | 60 | F34 |
| predators | A | C | D |  |  | 13 | 93 | F08 |
| prequelmemes | C | B | E |  | A, B | 25 | 736 | F13 |
| Produce101 | A (thin) | F | F |  | C, E | 2 | 6 |  |
| ProfessorLayton | E | E | C |  |  | 8 | 30 |  |
| PUBATTLEGROUNDS | A | C | A | E | B, C | 14 | 161 | F03 |
| purdue | B | A | D |  |  | 16 | 341 | F08 |
| purplecorner | C | B | B |  |  | 16 | 109 | F23 |
| PurplePixels | C | B | E |  | A, B | 13 | 216 | F16 |
| pusheen | E | E | F |  | A, B, C | 5 | 17 | F07 |
| puzzleanddragons | B | A | A |  |  | 12 | 190 | F07 |
| python | D | D | D | C |  | 12 | 122 | F08 |
| qotsa | A | F | F |  |  | 8 | 51 |  |
| quebec | A | C | A |  | B, C | 22 | 203 | F28 |
| quq | K | K | K |  |  | 0 |  |  |
| radiohead | B | A | A |  |  | 17 | 310 | F27 |
| Rainbow6 | D | D | A | C |  | 12 | 627 | F01 |
| rainbowgrid | C | B | G |  |  | 10 | 36 |  |
| rangers | A | C | E |  |  | 14 | 226 | F29 |
| raocow | C | B | A |  |  | 9 | 69 | F35 |
| ravens | D | D | A |  | B | 16 | 74 | F15 |
| re_zero | A | C | E | E | E | 12 | 84 | F20 |
| ReBoot | B (thin) | A | B |  | A, C | 2 | 4 |  |
| reddevils | B | A | A |  | A | 22 | 236 | F03 |
| redhotchilipeppers | B | A | E |  | A | 5 | 136 | F16 |
| Redox | K | K | K |  |  | 0 |  |  |
| redpandas | E | E | A |  |  | 11 | 63 | F22 |
| redvsblue | C (thin) | B | G |  |  | 3 | 41 |  |
| RelientK | C | B | B |  |  | 11 | 33 | F22 |
| rhythmheaven | C | B | B |  |  | 9 | 82 | F21 |
| rickandmorty | D | D | B |  | A, B, E | 12 | 447 | F32 |
| ripcity | C | B | G |  | B | 8 | 209 | F18 |
| riskofrain | C | B | G |  |  | 5 | 23 | F10 |
| rit | D | H | A | C |  | 10 | 99 |  |
| rocketbeans | B | A | A |  |  | 14 | 159 | F19 |
| rocketleague | D | D | B | C |  | 10 | 858 |  |
| rojava | E | E | A | B |  | 5 | 16 |  |
| romania | A | F | A | D |  | 15 | 270 | F01 |
| roosterteeth | B | A | B |  |  | 5 | 240 |  |
| rotmg | B | A | B |  |  | 20 | 290 | F23 |
| rpi | C | B | C |  | A | 11 | 120 | F08 |
| runescape | D | D | D |  |  | 11 | 569 | F01 |
| rush | D | D | F | E |  | 8 | 102 | F02 |
| russia | C | B | F |  | A | 7 | 111 | F22 |
| Russiaclan | A | C | B |  | C | 13 | 125 |  |
| rust | D | D | D |  |  | 20 | 177 | F08 |
| rutgers | B | A | B |  | A | 15 | 199 | F09 |
| rwby | D | D | F | C |  | 14 | 320 | F01 |
| sabres | A | G | H |  | B | 8 | 113 | F12 |
| sadboys | B | A | B |  |  | 11 | 60 | F12 |
| sakartvelo | K | K | K |  |  | 0 |  |  |
| sakuragakuin | E | E | A |  |  | 6 | 74 |  |
| samuraijack | D | D | E |  |  | 21 | 329 | F01 |
| satania | E | E | C |  |  | 10 | 119 | F07 |
| sbu | A | F | D |  | B, C | 7 | 39 | F08 |
| schoolidolfestival | A | F | B | C | D | 11 | 108 | F01 |
| scotland | A | C | H |  |  | 9 | 192 | F24 |
| ScottPilgrim | C | B | C |  | B, E | 5 | 63 |  |
| scp | D | D | F |  |  | 14 | 148 | F21 |
| seahawks | D | D | A | E | A | 16 | 161 | F01 |
| seolhyun | C (thin) | B | G |  |  | 3 | 38 | F09 |
| serbia | A | C | D |  |  | 9 | 259 | F08 |
| seventeen | B (thin) | A | B |  | A | 2 | 12 |  |
| sheffield | E | E | C |  |  | 14 | 62 | F07 |
| shield | A | C | C |  | B, C, E | 10 | 109 | F07 |
| shishamo | B (thin) | A | B |  | A, C | 1 | 22 | F22 |
| shitredditsays | A | G | B | B | B, E | 11 | 65 | F24 |
| shrooms | B (thin) | A | A |  | E | 1 | 29 |  |
| signal | K | K | K |  |  | 0 |  |  |
| simonfraser | B | A | E |  | A, C | 5 | 76 | F22 |
| singapore | A | C | B |  |  | 13 | 190 |  |
| sips | A | F | D |  | B | 21 | 109 | F20 |
| sixers | B | A | A |  |  | 13 | 150 | F27 |
| skyrim | C | B | C |  |  | 7 | 173 | F10 |
| Slovakia | C | B | G |  |  | 8 | 87 |  |
| slovenia | A | C | D |  | C | 6 | 80 | F08 |
| smashbros | D | D | E |  |  | 7 | 398 | F02 |
| smite | D (thin) | D | B |  |  | 2 | 435 | F22 |
| snsd | A | F | F |  | C | 11 | 72 |  |
| sonicthehedgehog | B | A | A |  | C | 6 | 50 |  |
| sooners | C | B | D |  |  | 10 | 49 | F08 |
| southafrica | A | C | C | C | E | 7 | 174 | F21 |
| southpark | D | D | A |  | A, B | 11 | 55 | F21 |
| soylent | B | A | A |  | A, C | 7 | 52 | F26 |
| spacex | D (thin) | D | H | E |  | 4 | 31 | F06 |
| spacexmasterrace | A | C | D | E | E | 11 | 118 | F07 |
| spain | A | G | B |  | C | 17 | 118 | F16 |
| spelunky | D (thin) | D | H |  |  | 4 | 21 | F01 |
| splatoon | A | C | A |  | B, C | 15 | 101 | F17 |
| spongebob | C | B | B |  | A, B | 11 | 41 | F15 |
| SquareSpiral | C | B | B |  | B | 11 | 222 | F09 |
| ss13 | A | C | C |  |  | 15 | 131 | F15 |
| ssbpm | D | D | E |  |  | 12 | 145 | F16 |
| starbound | E | E | A | C | A, B | 10 | 97 | F35 |
| starcitizen | A | F | B |  | D | 21 | 412 | F08 |
| starcraft | A | C | A |  | B | 15 | 216 | F01 |
| stardewvalley | B | A | F |  | C | 11 | 126 | F09 |
| stardustcrusaders | D | D | E | E |  | 14 | 320 | F01 |
| stargate | A | F | B |  |  | 12 | 59 | F01 |
| starlightstage | D | D | B | C |  | 14 | 123 | F10 |
| starryknights | B | A | B |  | E | 12 | 99 | F15 |
| startrek | K | K | K |  |  | 0 |  |  |
| starvstheforcesofevil | B | A | A | C |  | 6 | 358 | F23 |
| stevenuniverse | D | D | E |  |  | 19 | 497 | F01 |
| stlouis | B | A | A |  |  | 12 | 97 | F20 |
| stlouisblues | A | C | B |  | B, C | 13 | 162 |  |
| strangerthings | C (thin) | B | C | E |  | 3 | 147 | F34 |
| straya | A | C | D |  | C, E | 7 | 384 |  |
| streetfighter | D | D | F |  |  | 9 | 34 | F03 |
| Summit1G | C (thin) | B | G |  | A, B | 4 | 148 |  |
| suomi | A | C | C |  |  | 20 | 308 |  |
| superman | E (thin) | E | C |  |  | 2 | 32 | F33 |
| survivor | D | H | B |  |  | 11 | 326 | F02 |
| sweden | E (thin) | G | E |  | A | 4 | 835 |  |
| SwissNeutralityZone | C | B | B | E | A, B, E | 7 | 115 | F19 |
| switzerland | C | B | A |  |  | 11 | 76 | F10 |
| swordartonline | D | D | B |  |  | 12 | 58 | F18 |
| SydneyFC | E (thin) | E | C |  |  | 2 | 19 |  |
| tagpro | B | A | E |  |  | 10 | 179 | F29 |
| taiwan | E | E | C |  | B | 7 | 81 | F18 |
| tampabaylightning | A | C | C | E | E | 6 | 168 | F07 |
| teamcube | B | A | C | E | A, C, E | 10 | 41 |  |
| TeamDignitas | A | G | A |  | B, E | 8 | 61 |  |
| TeamYellowPlace | C (thin) | B | G |  |  | 3 | 63 |  |
| telegram | C | B | A | B | B | 7 | 24 |  |
| Temple | B | A | D |  | C | 17 | 123 | F08 |
| tenma | B (thin) | A | H |  | A | 1 | 2 | F35 |
| terraria | B | A | A | C |  | 12 | 155 | F01 |
| teslamotors | D | D | A | E |  | 7 | 269 | F08 |
| tetris | E (thin) | E | C |  |  | 3 | 16 |  |
| texans | D | D | D |  | A, B | 15 | 132 | F02 |
| texas | C | B | C |  |  | 10 | 289 | F08 |
| texastech | C | B | B |  |  | 6 | 48 |  |
| tf2 | E | E | C |  |  | 5 | 473 | F33 |
| thailand | C | B | B |  | A | 14 | 195 | F26 |
| the_pack | B | A | A |  |  | 10 | 118 |  |
| THE_R | B (thin) | A | A |  |  | 1 | 7 | F27 |
| TheAdventuresofTintin | A (thin) | A | C | E | B, C, E | 3 | 12 |  |
| TheB1G | C (thin) | B | G |  | B | 4 | 52 |  |
| theblackvoid | C | B | D |  | A, B, E | 12 | 1915 | F12 |
| thebluecorner | C | B | B |  | A, B | 20 | 1276 | F23 |
| theexpanse | C | B | E |  | B, E | 24 | 153 | F16 |
| TheFarLeftSide | A | G | B |  | B, C | 13 | 683 | F23 |
| Thegreatblackhole | C | B | B |  | A, B | 6 | 82 |  |
| TheGreatGreenBox | C (thin) | B | B |  | A, B | 4 | 57 |  |
| TheHulk | B | A | A | E |  | 13 | 111 | F07 |
| TheID | K | K | K |  |  | 0 |  |  |
| theitalyplace | B | A | D |  | A, C, E | 9 | 359 |  |
| thenetherlands | D | D | B |  |  | 8 | 414 | F02 |
| thepointing | B | A | A |  | C | 10 | 64 | F09 |
| thesilphroad | D (thin) | H | B |  |  | 4 | 776 |  |
| thesimpsons | A | C | A |  | B, D | 7 | 73 | F01 |
| thetreesnetwork | B (thin) | D | A | E | A, D, E | 4 | 12 |  |
| timbers | A | C | C | E | B, C, E | 13 | 80 | F07 |
| tinytardis | B | A | A |  |  | 8 | 62 | F15 |
| titanfall | A | F | B |  |  | 10 | 272 | F01 |
| tokyo | B (thin) | A | B |  | A | 3 | 14 | F20 |
| toolband | B | A | A | C |  | 10 | 241 | F09 |
| torontoraptors | A | F | C |  |  | 14 | 161 | F07 |
| totallynotrobots | D | H | B |  |  | 17 | 257 | F01 |
| touhou | A | C | E |  | C | 14 | 239 | F13 |
| traaaaaaannnnnnnnnns | B | A | A |  |  | 15 | 123 |  |
| TransFlagPlace | A | C | E |  | B, C | 5 | 331 | F16 |
| transformers | B | A | A | C | C | 13 | 91 | F10 |
| transgender | B (thin) | A | H |  |  | 3 | 12 |  |
| TreePlace | B (thin) | A | F | E | C | 4 | 35 |  |
| trees | A | C | C | E | E | 6 | 698 |  |
| truestl | A | C | C | C | E | 5 | 70 |  |
| TsundereSharks | E | E | A | B |  | 10 | 108 | F07 |
| turkey | A | C | B |  | B, C | 17 | 262 | F09 |
| twentyonepilots | A | F | F |  | B | 16 | 107 | F25 |
| twice | B | A | E | C | A, C | 6 | 176 | F09 |
| twitch | A | F | F |  | B | 8 | 32 | F07 |
| twitchplayspokemon | D | D | B |  |  | 17 | 284 | F01 |
| ubc | A (thin) | D | G | C | D | 3 | 107 | F22 |
| ubreddit | C | B | G |  |  | 10 | 45 | F09 |
| ucf | B | A | B |  |  | 11 | 110 | F15 |
| udub | A | G | B |  | E | 5 | 50 | F15 |
| ufl | A (thin) | A | B |  | B, C | 4 | 33 |  |
| uiowa | A | F | D |  | C | 11 | 35 |  |
| uiuc | B | A | F |  | A, C | 13 | 175 | F09 |
| ukplace | A | C | D |  | C | 7 | 92 | F08 |
| ukraine | A (thin) | C | D |  | C, E | 3 | 51 | F08 |
| ultrahardcore | D | D | H |  |  | 8 | 215 | F01 |
| UMiami | K | K | K |  |  | 0 |  |  |
| undertale | B | A | E |  |  | 9 | 284 | F32 |
| unitedkingdom | A | C | C | E |  | 7 | 291 | F07 |
| UNLincoln | K | K | K |  |  | 0 |  |  |
| unturned | D | D | C | E | A, B, C, E | 16 | 159 | F21 |
| uofm | B | A | A |  | A, C | 12 | 246 | F08 |
| uofmn | A | C | D |  | C | 9 | 99 | F10 |
| uoft | D | D | A |  |  | 13 | 187 | F24 |
| UPenn | A | F | F |  | B, C | 7 | 20 | F09 |
| uruguay | A | C | B |  | B, C, E | 7 | 69 |  |
| utahjazz | C | B | F |  | B | 12 | 145 | F14 |
| utaustin | C | B | B |  |  | 20 | 185 | F28 |
| uva | C | B | A |  |  | 9 | 36 |  |
| uvic | E | E | C |  |  | 8 | 61 | F07 |
| uwaterloo | D | D | B |  |  | 17 | 140 | F02 |
| vegan | B | A | A |  | A | 8 | 395 |  |
| VelvetUnderground | B (thin) | A | A | C |  | 2 | 15 |  |
| vermont | C | B | G | B | B, E | 8 | 40 |  |
| vietnam | E (thin) | E | C |  |  | 2 | 11 |  |
| Villanova | E | E | A | B | B | 5 | 19 |  |
| vim | B (thin) | A | H | E |  | 4 | 15 | F32 |
| vinesauce | C | B | F |  |  | 11 | 106 | F09 |
| virginiatech | A | C | D |  |  | 13 | 116 | F08 |
| vocaloid | C | B | B | E |  | 8 | 106 | F17 |
| wales | B | A | E |  |  | 8 | 72 |  |
| wallstreetbets | A | G | D |  |  | 13 | 214 | F08 |
| warframe | D | D | B | C |  | 21 | 294 | F01 |
| wario | K | K | K |  |  | 0 |  |  |
| warriors | B | A | A |  |  | 9 | 221 | F13 |
| warthunder | D | D | F |  |  | 12 | 135 | F09 |
| watchmen | E (thin) | E | C |  |  | 1 | 2 |  |
| weezer | E | E | A |  |  | 15 | 180 | F18 |
| wholesomememes | D | D | A | B | B | 24 | 246 | F01 |
| wildhockey | A | F | D |  |  | 16 | 218 | F01 |
| wine | D | D | C | E |  | 8 | 57 | F19 |
| winnipegjets | B | A | A | C |  | 8 | 84 |  |
| WisconsinBadgers | B (thin) | A | B |  |  | 4 | 30 | F15 |
| witcher | C | B | B |  | A, B | 13 | 110 | F27 |
| worldoftanks | D | D | B |  |  | 14 | 181 | F02 |
| worldpowers | B | A | D |  |  | 7 | 52 |  |
| wow | D | H | H |  |  | 11 | 364 | F01 |
| WPI | C (thin) | B | D |  |  | 3 | 57 | F08 |
| wsu | A (thin) | F | B |  | B, E | 3 | 15 |  |
| xcom | B | A | E |  | C | 14 | 113 | F30 |
| xenoblade_chronicles | C | B | B |  | B | 14 | 78 |  |
| yerbamate | K | K | K |  |  | 0 |  |  |
| yogscast | B | A | B | E |  | 9 | 135 | F19 |
| yugioh | D | D | H |  |  | 17 | 142 | F03 |
| yumenikki | B | A | B |  |  | 6 | 74 |  |
| yuyuyu | D | D | B | E |  | 7 | 29 |  |
| zelda | D | H | H |  |  | 15 | 223 | F01 |
| zootopia | A | C | C |  | B | 15 | 221 | F08 |

