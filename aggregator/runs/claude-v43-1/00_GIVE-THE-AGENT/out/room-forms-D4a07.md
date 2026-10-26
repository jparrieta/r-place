# Room forms, D4a-07: the arrow at every level

Leg D4a-07, 26 October 2026, an addition after the 35 branches, as at D4a-05 and D4a-06. J read the D4a-06 interview answers and asked (20:35 to 20:37 Berlin, through the handler): "How come arrows are not used?" "The arrow can work at any level. Just as the T3 are T4 and Ds." "Add the arrow and give your ideas as proposals but not mandated." The amendment is dated in `departures.jsonl` (line 14).

Nothing earlier is replaced. `branches.jsonl`, `crosslinks.jsonl`, `tree-D4.md`, the forms, `room-forms-D4a05.*`, `room-forms-D4a06.*` and every D5 file are unchanged; I checked 84 files against the D4a-06 close snap (`_analysis/d4a07_unchanged.py`). The leg stops at the top cut; the split below waits for J's talk.

Files: `room-forms-D4a07.jsonl` (one line per form and the core, with members), `room-forms-D4a07.tsv` (one row per room), and this file. The computation is `_analysis/d4a07_room_forms.py`; its rule was logged before it ran.

## 1. The arrow at every level

**Why it was missing.** At D4a-05 and D4a-06 a changed arrow counted once per level at the theme of the room's evidence, the second-order theme its line was written from, lifted up the ladder. Which arrow it changed, and so where the arrow leads, did not enter the distance. 2,125 of the 6,634 placed selected lines are on arrows (restrict 1,811, add-condition 285, add-step 29).

**How an arrow is lifted** (logged before the run). An arrow is a link from its source element to its target element (`model/arrows.jsonl`). Each end goes to the ladder through the element's own anchors (`model/elements.jsonl`):
- At the fourth-order level, the element's fourth-order anchors. An element anchored at a third-order theme is taken up to the fourth-order theme that gathers it.
- At the dimension, the dimension that holds that fourth-order theme.
- At the third-order level, the element's third-order anchors where it has them. Otherwise the line's own evidence theme, if it lies under that end; otherwise the end is held at its fourth-order node. The evidence sits under the arrow's source in 485 lines, under its target in 651, and under neither in 989, so at the third-order level most links keep one end at the fourth-order node.
- An end with no node at a level is held at its element. Only P15 is such an end (it is anchored at FP-01, outside the ladder), so the arrow into it (A12, the bare answer) keeps its link.
- An element with several anchors splits the link equally over the pairs.

**How much a link weighs.** Within each level an arrow line gives half its weight to its evidence node, as before, and half to its link. An element line gives all its weight to its node. So a room's mix at each level holds the themes its changes touch and the links its arrow changes touch, and every selected change still weighs the same. Node and link columns that only one defining room holds are dropped. That leaves 406 third-order columns (262 of them links), 200 fourth-order (172 links) and 67 at the dimension (59 links).

**What it does to the cut.** The forms change a good deal. The adjusted Rand index against D4a-06's forms is 0.191. Leaving out every link at k = 8 gives a cut that agrees with this one at 0.151.

## 2. The proposals: taken, changed or declined

- **(a) Placement: taken, changed.** I place each room by its whole mix: a defining room stays in its Ward form, and a thin room goes to the nearest centre. The signatures only describe the forms. J's literal rule (the form whose signature holds most of a room's changes) is reported beside it. Under the literal rule 307 rooms would move, and 102 placements would be ties. The literal rule empties the middle form B (159 to 40) and fills C (87 to 140) and G (59 to 138), whose signature themes, the design and borders, are ones many rooms change. I declined the weighting by distinctiveness: it is one more rule, and the whole mix already uses every change.
- **(b) Form B: declined as a hand-made change.** A form is kept or split only by the stated measures. With the arrows in, B is the middle of the continuum: 159 rooms, its one signature held by 34 per cent of its defining members. Ward's own split of it gives a half that leans to templates and attack calls (54 rooms) and a half that leans to reporting the mark, traded help and carrying on (77). Carrying on is part of the second half; the measures did not cut it on its own.
- **(c) The raiding core: taken.** 21 defining rooms have a quarter or more of their selected changes on attack calls. As one group against the rest their silhouette is 0.098. Random groups of the same size give a mean of 0.000 and a 95th percentile of 0.020 (p = 0.001). So "raiding as the work" holds as a group beyond chance, but it is a small pattern: the top cut does not isolate it, and 13 of the 21 sit in B, 5 in H. It is a candidate for the split below B.
- **(d) The count: kept, and the measures now agree.** Both the merge-height gap and matched-subsample stability carry k = 8 (section 3). I expected 5 to 7; with the arrows in, both measures place the clearest cut at 8, the edge of J's range. I did not look past 8.
- **(e) The floor of 5: kept.** 558 rooms define the forms, 126 thin rooms are placed afterwards, 21 rooms with no selected change stay the core.
- **(f) Restrict lines: taken as a check, the weighting declined.** Restricts are 0.40 to 0.48 of every form's changes, so the share of restricts does not tell the forms apart. But they shape the cut. Without them, at k = 8, one group of 228 rooms forms in the middle (sizes 228, 54, 53, 52, 48, 47, 42, 34), and the cut agrees with this one at 0.149; 3 defining rooms hold only restricts. I declined to weight restricts apart, because op does not count on its own (J's first rule). Telling "the arrow fails here" from "the record cannot show it" needs the lines read. In the lines I read, the restricts on C's and F's signature links mostly say the arrow fails as stated: the design stays open after the template, and the move follows a loss or a neighbour's advance. I did not read enough of the lines on D's links to say. Those on A's calls mostly say the record cannot show the arrow. This is a reading of the lines shown, not a count.
- **(g) Link ops: my own proposal, taken.** 996 element lines use the op link: they propose a connection the model lacks. I lift each as a link the same way, from its evidence node to the element's anchor. Without them (arrows only), the cut agrees with this one at 0.208. They carry, for example, F's return from the move to building.

## 3. The count

| k | Ward merge height: the cut begins | ends | lifetime (the gap) | stability: matched subsamples | shuffled null mean | null 95th percentile | margin |
|---|---|---|---|---|---|---|---|
| 4 | 2.5040 | 2.5992 | 0.0952 | 0.1303 | 0.0747 | 0.1419 | 0.0557 |
| 5 | 2.3643 | 2.5040 | 0.1397 | 0.1478 | 0.0840 | 0.1419 | 0.0638 |
| 6 | 2.2831 | 2.3643 | 0.0812 | 0.1742 | 0.0910 | 0.1458 | 0.0832 |
| 7 | 2.2231 | 2.2831 | 0.0601 | 0.1865 | 0.0964 | 0.1475 | 0.0900 |
| 8 | 2.0741 | 2.2231 | 0.1490 | 0.2019 | 0.1005 | 0.1552 | 0.1014 |

The merge-height gap is longest at k = 8 (0.149, against 0.140 at k = 5), and the stability margin rises to 0.101 at k = 8. The two measures agree. Every real stability is still low (0.13 to 0.20), though from k = 5 to 8 it lies above the shuffled null's 95th percentile.

## 4. The eight forms

By Ward on the defining rooms the forms hold 132, 131, 67, 60, 54, 44, 38 and 32 rooms (ratio 4.13). Placed by the whole mix they hold 148, 159, 87, 64, 60, 56, 59 and 51 (ratio 3.12). The ratio is above J's bound of 3 because the middle form B is the largest; without B it is 2.90. Every form has a signature, and none is set apart only by breadth. B's signature is weak, and I report it as a mixture.

| form | the pattern of change | defining rooms (Ward) | placed by the whole mix | by J's literal rule | signature: fourth-order nodes and links (share of members' changes; times the population; members holding it) | restricts among its changes | one kind or a mixture |
|---|---|---|---|---|---|---|---|
| A | keeping and calling reworked: defence, repair and the hands for them | 132 | 148 | 88 | Repair work (0.16; 2.5; 92%); Mobilization (0.05; 1.6; 45%) | 0.46 | one kind (keeping), with calls |
| B | the middle: templates, reports, help and carrying on, with no shared lean | 131 | 159 | 40 | Standardization of output (0.06; 2.0; 34%) | 0.45 | a mixture |
| C | the design reworked: settled, marked, and not settled by the template | 67 | 87 | 140 | Collective representation (0.27; 3.2; 98%); Completion ritual (0.06; 1.6; 49%); Collective representation > Standardization of output (0.03; 1.5; 61%) | 0.48 | one kind |
| D | machine hands reworked: scripts with steps of their own, adopted beside the work | 60 | 64 | 62 | Workarounds (0.22; 5.1; 93%); Repair work > Workarounds (0.03; 3.0; 60%); Negotiated order > Live and let live (0.02; 1.6; 45%) | 0.42 | one kind |
| E | the chat reworked: planning moved into a chat, its access and what returns | 54 | 60 | 36 | Backstage decision-making (0.20; 6.0; 89%) | 0.42 | one kind |
| F | the spot reworked: lost, chosen or yielded, and building again | 44 | 56 | 72 | Territoriality (0.28; 5.8; 100%); Collective efficacy > Territoriality (0.03; 1.8; 59%); Territoriality > Direct information sharing (0.03; 5.7; 50%) | 0.47 | one kind |
| G | the terms between neighbours reworked | 38 | 59 | 138 | Negotiated order (0.33; 3.3; 97%); Negotiated order > Live and let live (0.03; 2.3; 63%); Repair work > Negotiated order (0.02; 1.8; 45%) | 0.48 | one kind |
| H | the host sub's play and the call reworked | 32 | 51 | 108 | Keying (0.19; 5.2; 69%); Mobilization (0.10; 3.3; 59%); Boundary work (0.08; 3.0; 41%); Repertoire of contention (0.07; 3.1; 41%) | 0.40 | a mixture of the frame and the call, with attack calls |
| K | the core: no selected change | | 21 | 21 | none | | |

Several signatures are now links:
- **C:** the design to the template (A11).
- **D:** keeping to scripts (A06), and borders to sparing (A05).
- **F:** judging hands too few to the move (A10), and the move to building again.
- **G:** borders to sparing (A05), and keeping to borders (A04).

## 5. The members, read as rooms, and whether a differing account could be written

I read each form's best fits and misfits through their lines' how sentences, with the members' lines on each signature column by op (`_analysis/d4a07_read.py`). Best fits and misfits are taken among defining rooms.

| form | best fits (defining rooms, largest share on the signature) | misfits (smallest share), and the forms they lie near |
|---|---|---|
| A | r/FlaggyFlag (7 changes, 0.64), r/warriors (9 changes, 0.50), r/OneTrueEmilia (8 changes, 0.50) | r/chelseafc (0.00; near B, E, G), r/falcons (0.00; near B, C, D, E, F, G, H), r/kuwait (0.00; near B, C, D, E) |
| B | r/ghibli (6 changes, 0.42), r/roosterteeth (5 changes, 0.40), r/npr (9 changes, 0.39) | r/paladins (0.00; near A), r/warframe (0.00; near C, G), r/gamindustri (0.00; near none) |
| C | r/CSUFoCo (5 changes, 0.80), r/Madeon (5 changes, 0.80), r/guatemala (6 changes, 0.75) | r/metroid (0.07; near B, D, F, G), r/mindcrack (0.07; near A, B, D, E, G), r/shield (0.10; near G) |
| D | r/rust (20 changes, 0.70), r/ukplace (7 changes, 0.57), r/minnesotavikings (9 changes, 0.53) | r/cavestory (0.00; near B, C, E, G), r/msu (0.00; near A, B, C, E, F, G), r/ockytop (0.06; near A, B, C, E, G, H) |
| E | r/bangladesh (8 changes, 0.50), r/smashbros (7 changes, 0.50), r/TransFlagPlace (5 changes, 0.50) | r/overwatch (0.00; near A, B, C, D, F, G, H), r/parahumans (0.00; near A, B, H), r/partyparrot (0.00; near A, B, C, D, G, H) |
| F | r/warthunder (12 changes, 0.71), r/twitch (8 changes, 0.69), r/UPenn (7 changes, 0.64) | r/rwby (0.14; near B, G), r/scp (0.14; near A, B, E), r/indieheads (0.15; near C) |
| G | r/mechanicalkeyboards (14 changes, 0.61), r/ManningPlace (5 changes, 0.60), r/riskofrain (5 changes, 0.60) | r/germany (0.00; near A, B, F, H), r/norway (0.12; near B), r/korea (0.20; near B, C, F) |
| H | r/GuildWars2 (9 changes, 0.94), r/anime_irl (5 changes, 0.80), r/ontario (5 changes, 0.80) | r/placeDE (0.11; near B, C, D, E), r/alberta (0.17; near C), r/polandball (0.17; near C) |

- **A, keeping and calling.** r/warriors arranges coverage across members' sleep by handoff; r/FlaggyFlag keeps attribution provisional. The misfits (r/chelseafc, r/falcons, r/kuwait) have none of their changes on A's signature and lie near several forms.
- **B, the middle.** r/ghibli clarifies which corner an anchor marks; r/roosterteeth finds a template that no longer fits. The misfits are rich rooms whose changes spread over many forms (r/paladins, 25 changes; r/warframe; r/gamindustri).
- **C, the design.** r/guatemala asks for publicity after its first placement; r/CSUFoCo keeps trying to restore its spot despite fewer hands. In r/metroid, a misfit near G and others, a source sprite stays open to colour checks after it is posted.
- **D, machine hands.** In r/rust a later target proposal threatens work marked for preservation; r/ukplace needs working chat access to change script targets; r/minnesotavikings tests a promised exemption for a neighbour, finds it missing, and fixes it after a failed update.
- **E, the chat.** r/bangladesh asks that the chat link and goals go into a public sticky; r/TransFlagPlace screens who enters and reports a ban.
- **F, the spot.** r/warthunder times its request for space around when the host's members are awake; r/twitch reports where an image stands. r/day9, the account's best-supporting room, is a thin room (3 changes) and is placed here, all its changes on the signature.
- **G, the terms between neighbours.** r/mechanicalkeyboards meets a contested overlap after a call; r/riskofrain sends negotiation to a chat where a representative must ask for diplomatic status.
- **H, the host sub's play and the call.** r/GuildWars2 tolerates the temporary play but not an extended unreadable styling; r/ontario enacts the fake rules by bans and mock sanctions; r/anime_irl grants a holiday exception for a canvas post.

| form | could an account that differs from the global model be written? |
|---|---|
| A, keeping and calling reworked: defence, repair and the hands for them | In part. The changes to keeping add conditions the model lacks (coverage, handoffs, sleep). The changes to calls are mostly restricts on the bare answer and the order of call and build, which say the record cannot show the arrow. |
| B, the middle: templates, reports, help and carrying on, with no shared lean | No. Its members share no change, so there is no shared account to differ from the model. |
| C, the design reworked: settled, marked, and not settled by the template | Yes. 42 of the 43 lines on the link from the design to the template restrict A11: a posted template does not settle the design. That differs from the frozen model and agrees with the held proposal on A11. |
| D, machine hands reworked: scripts with steps of their own, adopted beside the work | Yes. The scripts gain steps and conditions (add-step 57, add-condition 45 on workarounds), and 27 of the 37 lines on the link from keeping to scripts restrict A06: scripts serve building and planned upkeep together, not only upkeep under strain. |
| E, the chat reworked: planning moved into a chat, its access and what returns | In part. The chat is a candidate element (P23), not in the frozen model; an account could add it, but the record shows the chat from outside (invitations, access, returned reports), not its deliberation. |
| F, the spot reworked: lost, chosen or yielded, and building again | Yes. 27 of the 28 lines on A10's link restrict it (the move follows other causes than a judgment of too few hands), and 25 link lines add the return from the move to building, an arrow the model lacks. |
| G, the terms between neighbours reworked | In part. The links limit A04 and A05 (negotiation can come before defence; agreements guide restraint only where placers learn of them), limits the account already states in part. |
| H, the host sub's play and the call reworked | Yes, for the frame. The April Fools frame gains steps and conditions (add-step 44, add-condition 15 on keying), the sub's play administered beside the canvas, which the model holds only as a key. |

## 6. The raiding and takeover rooms, and r/startrek

| set | rooms | A | B | C | D | E | F | G | H | core |
|---|---|---|---|---|---|---|---|---|---|---|
| raiding core (a quarter or more of the changes on attack calls; defining rooms) | 21 | 0 | 13 | 0 | 2 | 1 | 0 | 0 | 5 | 0 |
| takeover (F02) | 33 | 6 | 12 | 0 | 3 | 1 | 5 | 0 | 6 | 0 |

- **Raiding.** The core holds together beyond chance (section 2c). It sits mostly in B, the middle, and in H, so the top cut does not make it a form.
- **Takeover rooms** (F02's 33) spread over six forms, most in B (12). Only 6 are in H, the form whose signature is the April Fools frame: for most of them the canvas changes outweigh the frame.
- **r/startrek** stays in the core. It has no changed arrow and no other selected change; its 28 accepted lines all instantiate the model.

## 7. Kinds or a continuum, and the codes

**Still a continuum.** The stability of the cut is low, though above the shuffled null. The middle form B holds 159 rooms with no shared lean. 276 rooms have a secondary form, and 307 lie within 5 per cent of another form's centre. The cut moves with each choice of what counts: links, link ops and restricts each change it to an adjusted Rand of 0.15 to 0.21.

**Against the codes**, which the tree does not use: the forms differ, weakly. The pseudo-F is 7.75, against a null 95th percentile of 1.22 (p = 0.001), and the forms explain 7.4 per cent of the variation in the rooms' code shares. The codes come from the same scheme as the changes, so the check is not independent. The forms differ in room size: the median room has 78 coded concepts in F and 158.5 in E.

## 8. For the talk with J

- The cut moves with each choice of what counts (links, link ops, restricts). Which comparison should be the basis?
- B is the middle of the continuum. Should it be split below (its two halves), or read as the population's middle rather than as a form?
- The raiding core holds as a group but sits inside B and H. Should it be a sub-form below them?
- Placement by the whole mix, or J's literal rule, which moves 307 rooms?
- Both measures put the clearest cut at 8, the edge of the range. Should the range be wider?

## 9. The room table

One row per room, in case-ignored order (also in `room-forms-D4a07.tsv`). The form is placed by the whole mix; a thin room is marked. *J's literal rule* gives the form the literal placement would choose, with its ties. The branches are the 35 of D4, primary first.

| room | form | J's literal rule | secondary forms | near-equal centres | changes | primary branch | secondary branches |
|---|---|---|---|---|---|---|---|
| 2007scape | E | A |  | A | 13 |  |  |
| 49ers | G | G |  |  | 14 | F10 | F21 |
| 4chan | H | H |  |  | 13 | F01 | F06, F08, F34 |
| aceattorney | A | A |  |  | 15 |  |  |
| acecombat | B | G |  | G | 9 | F02 | F01 |
| AceOfAngels8 | B (thin) | C | C |  | 1 |  |  |
| AcePlace | B | G |  | G | 9 | F17 | F25 |
| achievement_hunter | F (thin) | F |  |  | 3 |  |  |
| adventuretime | F | F |  |  | 13 | F09 | F25 |
| aeon | D | D |  |  | 7 | F19 | F08, F17 |
| aeskwadraat | C (thin) | C |  | B | 3 | F12 | F11, F34 |
| afip | D (thin) | D (tie: C, D) | C |  | 3 | F19 | F17 |
| aggies | C | D | D |  | 12 |  |  |
| ainbowroad | E | E (tie: E, F) |  |  | 19 |  |  |
| albania | C (thin) | C | D | D | 3 |  |  |
| alberta | H | C | C |  | 9 |  |  |
| AMD | C | H | H | H | 11 | F01 | F03, F04, F07 |
| AmericanFlaginPlace | A | D |  | B, D, E | 23 | F08 | F23, F29 |
| anaheimducks | A | C |  |  | 16 | F14 | F09, F11, F34 |
| anarchism | D | H (tie: C, H) |  | B | 5 |  |  |
| anarcho_capitalism | A | F | F | B, F | 12 |  |  |
| anarchocapitalism | A (thin) | A |  |  | 1 |  |  |
| androidgaming | A | A |  |  | 16 |  |  |
| animalcrossing | F | B | B | B | 10 | F09 | F15 |
| anime | G | G |  | B | 24 | F19 | F17 |
| anime_irl | H | H |  |  | 5 | F01 | F04, F05 |
| aoe2 | C (thin) | C |  | B | 2 | F34 |  |
| apocalypserising | B | C | C, E | C, E | 6 |  |  |
| AprilKnights | E | E |  |  | 6 | F16 | F29 |
| araragi | B | C | C | A, C, D, E, F | 5 |  |  |
| archlinux | C | C |  |  | 11 | F07 | F08 |
| argentina | E | H | H |  | 8 |  |  |
| armenia | B | B |  | A | 5 |  |  |
| armok | E | A |  | A, B, C | 14 | F27 |  |
| aromantic | B (thin) | B |  | D, F | 2 |  |  |
| asexual | B | H |  | A | 6 |  |  |
| asexuality | A | A |  |  | 15 | F17 |  |
| asktransgender | B (thin) | H | H | A, H | 4 |  |  |
| auburn | G (thin) | G |  | A | 4 |  |  |
| australia | H | H | C |  | 7 | F07 |  |
| austria | B | G | G | D | 16 |  |  |
| austriahungary | C (thin) | C |  |  | 1 |  |  |
| AvoArmy | C | C |  |  | 12 | F07 | F24 |
| AyyMD | A | C | C | C | 14 | F07 | F34 |
| azerbaijan | B (thin) | C | C |  | 3 | F19 | F17, F20 |
| azores | B (thin) | C | C |  | 1 |  |  |
| babymetal | A | A |  |  | 25 | F22 | F27 |
| bahrain | H (thin) | H |  |  | 1 | F01 |  |
| bakchodi | H | H |  | D | 5 | F08 |  |
| bangladesh | E | E | F |  | 8 |  |  |
| bangtan | E | F | F | F | 12 | F17 |  |
| bannedfromanime_irl | K |  |  |  | 0 |  |  |
| bardmains | A | H | H |  | 16 | F07 | F23, F34 |
| batman | G | G |  |  | 12 |  |  |
| battlecats | F | F |  |  | 9 | F02 | F01 |
| baylor | C | C |  |  | 5 | F33 |  |
| bdsm | C (thin) | C |  |  | 2 |  |  |
| bees | H (thin) | H |  | B | 1 |  |  |
| belgium | D | C |  | B, E | 13 | F24 |  |
| berkeley | F (thin) | F (tie: C, F) | C, G |  | 4 | F09 |  |
| berserk | F | F |  | A | 18 | F09 | F16, F32 |
| bigbang | H (thin) | H |  |  | 2 |  |  |
| bih | A | A |  |  | 7 |  |  |
| bindingofisaac | A | H |  | B | 23 | F01 | F02, F04, F11, F12, F23 |
| bisexual | A | G | G | G | 23 | F07 | F31 |
| bitcoin | C | D (tie: D, G) | D, G | D | 8 |  |  |
| blackmirror | C (thin) | C |  |  | 4 |  |  |
| bobross | B (thin) | H (tie: A, H) |  | D, H | 4 |  |  |
| borderlands | A | C | C, H |  | 6 | F27 | F34 |
| borussiadortmund | H | H |  |  | 19 | F21 | F35 |
| bostonbruins | G | G | A, H |  | 7 | F32 |  |
| bostonceltics | B | F | F | F, H | 8 | F04 | F01, F09, F17, F18 |
| brasil | E | E |  |  | 10 |  |  |
| Bravenewbies | E (thin) | E | C |  | 2 |  |  |
| Braveryjerk | H (thin) | H |  | B | 1 |  |  |
| bretagne | A | C | C | B | 6 |  |  |
| btc | G (thin) | G |  |  | 4 | F28 |  |
| buffalo | H | D | D | D | 10 | F12 | F11, F24 |
| buffalobills | G | G |  |  | 17 | F10 | F26 |
| buffalowizards | F | A | A | A, B | 5 | F09 |  |
| bulgaria | C | C |  |  | 16 |  |  |
| calgaryflames | B | F |  | F | 6 | F09 |  |
| calvinandhobbes | C | C |  |  | 7 | F07 |  |
| canada | B | H |  | A | 13 | F01 |  |
| canucks | B | D |  | D | 25 | F01 | F03, F04, F20, F24, F30 |
| cardinals | B | H |  |  | 11 |  |  |
| carletonu | G (thin) | G |  |  | 3 |  |  |
| catalonia | D | D |  |  | 8 | F08 |  |
| catalunya | G | G |  |  | 18 | F07 | F10, F28 |
| catholicism | H | H |  |  | 9 | F23 |  |
| cavestory | D | E |  | B, C, E, G | 7 | F10 | F16 |
| CelticFc | G (thin) | G |  |  | 1 | F28 |  |
| cfb | H | H | A |  | 7 | F02 | F01 |
| cgpgrey | B | A (tie: A, H) | A, H |  | 12 | F14 | F11, F23 |
| chelseafc | A | C | C | B, E, G | 20 | F04 | F01, F31 |
| chess | F | C |  | B, C | 9 | F33 |  |
| chibears | G | G |  | B, F | 7 | F09 | F20 |
| chicago | C | C |  |  | 19 | F07 | F21, F31 |
| chicubs | A | G (tie: C, G) |  |  | 14 |  |  |
| chile | A | A |  |  | 22 | F21 | F30 |
| ChronoTrigger | A | A |  |  | 6 | F12 | F11 |
| churchofhelix | K |  |  |  | 0 |  |  |
| cirkeltrek | A (thin) | A (tie: A, G) | G |  | 3 |  |  |
| CKCrusaders | A | A | C, H |  | 8 |  |  |
| Clannad | A (thin) | C | C | C | 2 |  |  |
| clashroyale | H | A (tie: A, H) | A, G | A, B, F, G | 11 | F35 |  |
| clg | B | H |  | A | 14 | F32 |  |
| cloud9 | A | G |  | B, E | 10 | F12 | F11, F28 |
| clubpenguin | B | F | F | A, F | 11 | F12 | F09, F11 |
| cmu | D | G | G |  | 10 |  |  |
| coldplay | G | G |  | C | 14 | F07 | F10, F33 |
| colombia | B (thin) | C (tie: C, D, F, G) |  | C, F, G | 4 | F22 |  |
| colorado | A (thin) | A (tie: A, B, C) | B, C |  | 3 | F15 |  |
| columbia | G | G |  | B | 11 | F15 |  |
| completeanarchy | D | H | A, H | H | 13 |  |  |
| compsoc | B (thin) | C | C |  | 2 |  |  |
| Cornwall | G (thin) | G |  |  | 1 |  |  |
| corridor | F | F |  |  | 15 | F25 |  |
| COSI | F (thin) | F |  |  | 1 |  |  |
| costa_rica | E | G |  | A, B, C, F, G | 8 |  |  |
| counting | B (thin) | B |  |  | 2 |  |  |
| cowchop | A | G |  | B | 13 | F24 | F27, F28 |
| criticalrole | C | B |  | A, B, G | 19 | F01 | F15 |
| croatia | G (thin) | G | C |  | 4 | F07 |  |
| crusaderkings | A | H | H |  | 11 | F08 |  |
| CryptoFR | B (thin) | B |  | E | 3 |  |  |
| crystalclear | A (thin) | A (tie: A, C) | C |  | 2 | F34 |  |
| CSUFoCo | C | C |  |  | 5 | F33 |  |
| cubers | C | C |  |  | 12 | F12 | F11 |
| cuboulder | B (thin) | B |  |  | 1 |  |  |
| czech | A | G | G | B, C, D, E, G | 14 | F07 | F08, F25 |
| daftpunk | G | G |  |  | 9 |  |  |
| dallasstars | D | D |  |  | 11 | F01 | F24 |
| danganronpa | D | D (tie: C, D, H) |  | A, B | 16 | F02 | F01, F24 |
| dankmemes | H | H |  |  | 10 | F01 | F02, F03, F04 |
| darksouls | E | E |  |  | 8 | F16 |  |
| DatBoi | H | H |  |  | 5 |  |  |
| davidbowie | A (thin) | A (tie: A, B, C) | B, C |  | 4 | F15 |  |
| day9 | F (thin) | F |  |  | 3 | F09 |  |
| dbz | F | G | G | G | 14 | F01 |  |
| DCFU | B | C | C, G | G | 6 | F22 |  |
| de | B | G | G | A, E, G | 23 | F16 | F30 |
| denmark | E | E (tie: E, G) |  |  | 8 | F11 |  |
| denverbroncos | A | H | H |  | 20 | F03 | F01, F17, F18 |
| destiny | B (thin) | H | H |  | 4 | F22 |  |
| DestinyTheGame | A | G |  | B, G | 17 | F02 | F01, F23 |
| detroitlions | B | H |  |  | 13 | F34 |  |
| detroitredwings | G | G |  |  | 12 |  |  |
| DevonUK | G (thin) | G |  |  | 2 |  |  |
| diablo | F | F |  |  | 9 |  |  |
| DiamondClub | B (thin) | B |  |  | 1 |  |  |
| dmt | H (thin) | H (tie: A, H) | A |  | 2 |  |  |
| dofus | C (thin) | C |  |  | 1 |  |  |
| Dominican | F | F |  |  | 10 |  |  |
| donaldglover | E | F | F | F | 12 | F11 |  |
| Dorset | G | G |  |  | 6 |  |  |
| dota2 | D | D |  |  | 15 | F05 | F01, F08, F28 |
| dragonquest | C | D | D, G |  | 8 | F33 |  |
| drawhelix | A | C | C | C, E | 7 | F10 |  |
| drugs | C (thin) | C (tie: C, G) | G |  | 3 |  |  |
| drumcorps | A | G | G, H | B, G | 7 | F01 | F03, F10 |
| duckgame | G | G |  |  | 7 |  |  |
| ducks | B | B |  |  | 5 |  |  |
| Dustforce | F (thin) | F (tie: F, G) | G | G | 4 | F09 | F10 |
| dwarffortress | E | E |  |  | 17 | F16 |  |
| eagles | B | G |  | A, D, E, G | 10 |  |  |
| earthbound | A | A (tie: A, G) | G |  | 12 | F10 | F26 |
| edboxes | A | H | H |  | 16 | F07 |  |
| eder | C (thin) | C |  | B, E | 2 | F20 |  |
| edmontonoilers | A | C | C | C | 12 |  |  |
| eesti | D | D (tie: D, F) | F |  | 8 | F08 |  |
| egypt | C (thin) | C |  |  | 4 | F22 |  |
| ElderScrolls | A | A | C |  | 6 | F01 | F32 |
| elitedangerous | A (thin) | H | H | B, H | 4 | F04 | F01 |
| ElSalvador | B | G |  | F, G | 5 |  |  |
| empiredidnothingwrong | A | C |  |  | 20 | F27 |  |
| england | B | D (tie: D, H) | D, H | C, D | 9 |  |  |
| enterthegungeon | B | F (tie: A, F, H) |  | A, F | 10 | F23 |  |
| epublica | D | G | G | G | 16 | F24 |  |
| EraseThePlace | B | D |  |  | 19 | F29 |  |
| esperanto | A | A (tie: A, C) |  | B, C, E | 11 | F12 | F11, F16 |
| ethereum | B | G |  | D | 16 | F01 |  |
| ethoslab | F | F (tie: F, G) | G |  | 5 | F01 |  |
| europe | B | E (tie: E, H) |  | A, E | 17 |  |  |
| eve | E | E |  |  | 12 | F07 | F16, F29 |
| evedreddit | G (thin) | G |  |  | 1 |  |  |
| evex | C | D |  | D | 13 | F08 | F10, F34 |
| factorio | D | D (tie: C, D) |  |  | 9 | F07 |  |
| faeria | A | G | G | G | 14 | F18 | F10, F17, F31 |
| falcons | A | H | H | B, C, D, E, F, G, H | 11 | F01 |  |
| farmcarrots | C | C |  |  | 12 | F07 | F34 |
| FaroeIslands | B | H |  |  | 10 | F09 |  |
| FederationPlace | C | A | A | A, D | 15 | F08 | F10 |
| feedthebeast | A | A |  |  | 10 | F14 | F01, F11, F24, F33 |
| Fez | A | A |  |  | 9 | F21 |  |
| FinalFantasy | B | A |  | A | 15 |  |  |
| finland | G | G |  |  | 6 |  |  |
| fireemblem | B | G |  | A, G | 10 |  |  |
| fivenightsatfreddys | A | H |  | B, E, F, H | 22 | F01 | F02, F07, F09, F10, F23, F29, F31 |
| FlaggyFlag | A | A | C, H |  | 7 | F07 | F35 |
| flashtv | F | F |  |  | 16 | F02 | F01, F07, F09 |
| FlipnoteStudio3D | H (thin) | H (tie: A, H) | A |  | 1 |  |  |
| floridagators | A | A |  | E | 5 |  |  |
| FloydVsVoid | E | G |  |  | 26 | F15 | F30, F31 |
| flyers | B | C | C |  | 14 | F18 | F17, F22 |
| formula1 | F | F (tie: C, F, H) |  |  | 6 | F02 | F01, F09 |
| forsen | B | H | H | A, E, H | 15 | F12 | F11, F16, F30 |
| foxes | A | B |  | B, D | 16 | F31 |  |
| foxstevenson | F (thin) | F |  |  | 3 |  |  |
| france | D | D |  |  | 6 |  |  |
| frankocean | A | A (tie: A, G) |  |  | 21 | F27 | F31 |
| frc | A | D | D | B, D, E | 10 | F24 | F25, F27 |
| freedomplanet | F | F |  |  | 6 | F19 | F09, F16, F17 |
| ftlgame | B | B |  |  | 7 | F18 | F15, F17 |
| fullcommunism | A | D (tie: C, D) | C, D | D | 6 | F17 |  |
| funhaus | G | G |  |  | 15 | F30 |  |
| furry | G | G |  | A, B | 16 | F26 |  |
| furry_irl | B | G |  | A | 10 | F05 | F01, F11, F12, F22 |
| futanari | B | C | C |  | 5 |  |  |
| futurama | A | A |  |  | 10 | F23 | F24, F27 |
| fxKorea | C | C |  |  | 9 | F18 | F07, F17 |
| GabrielDropout | C (thin) | C (tie: B, C) | B | D | 4 |  |  |
| gameattack | B | A (tie: A, H) |  |  | 11 | F21 |  |
| gameboy | F (thin) | F |  | B | 3 |  |  |
| gameofthrones | A | A (tie: A, C) |  |  | 10 | F02 | F01, F07, F17, F18, F28 |
| gamindustri | B | C |  |  | 20 | F12 | F11, F22 |
| gatech | C | C |  |  | 19 | F08 | F07, F11, F14, F23, F33 |
| genderfluid | A (thin) | A |  |  | 4 |  |  |
| geometrydash | B | H | H | H | 8 | F01 | F02 |
| germany | G | H | H | A, B, F, H | 5 |  |  |
| ghibli | B | B |  |  | 6 | F15 |  |
| giantbomb | D | D |  |  | 15 |  |  |
| giivasunner | B | F | F | F | 11 | F09 | F22 |
| glasgow | A | C | C |  | 6 |  |  |
| globaloffensive | A | D |  | B, D | 9 | F13 | F11 |
| Goodboye | A | A |  |  | 9 |  |  |
| gorillaz | A | C | C | C | 17 | F25 |  |
| GranColombia | E | E |  |  | 7 | F16 | F24, F30 |
| gratefuldead | F | F |  |  | 8 |  |  |
| gravityfalls | A | C | C | B | 9 | F12 | F11, F27 |
| greece | A | C | C | B, C | 11 | F27 |  |
| greenbaypackers | D | D |  |  | 11 |  |  |
| GreenCorner | A | A (tie: A, G) |  |  | 9 |  |  |
| GreenEmpire | K |  |  |  | 0 |  |  |
| greenland | K |  |  |  | 0 |  |  |
| greenlattice | B | A (tie: A, F) |  | A | 24 | F12 | F11 |
| greyblob | B | F | F | A, F | 9 | F12 | F09, F11, F23 |
| GrowTheTree | C (thin) | C (tie: C, G) | G | B, G | 4 |  |  |
| GuardiansOfDatBoi | B | H | H | H | 7 | F15 |  |
| guatemala | C | C |  |  | 6 |  |  |
| GuildWars2 | H | H | A |  | 9 | F01 | F35 |
| h3h3productions | B | H |  | F, H | 12 | F21 |  |
| habs | B | C |  |  | 15 | F32 |  |
| halo | B | D |  | A, D | 8 |  |  |
| harrypotter | C | C | G | G | 8 | F01 | F22, F26 |
| haskell | F (thin) | F (tie: D, F, G) |  | B, D, E | 3 |  |  |
| hatsune | A | F | F | B, F, G | 16 | F20 | F35 |
| hawks | A | A |  |  | 14 | F22 | F24, F27 |
| hearthstone | C | G |  | A, B, G | 13 | F10 |  |
| hellointernet | B | G | G | A, C, G | 12 | F27 | F33 |
| hentai | C | C |  |  | 10 | F07 | F22 |
| heroesofthestorm | A | A (tie: A, H) | H | B, E, H | 9 | F01 | F29 |
| heyyea | C | C |  |  | 7 | F11 |  |
| homelab | B | C |  |  | 12 |  |  |
| HomestarRunner | H | H |  |  | 15 |  |  |
| homestuck | A | A (tie: A, H) |  |  | 9 | F35 |  |
| Homura | E (thin) | E |  |  | 1 |  |  |
| Honduras | B | C | C | C | 5 |  |  |
| hongkong | C | C | G |  | 7 | F07 | F31 |
| hoodr | B (thin) | B |  | F, G | 3 |  |  |
| hsv | A | A |  |  | 13 |  |  |
| httyd | B | C |  | C, F | 8 | F32 |  |
| hungary | G (thin) | G |  | B | 4 | F23 | F28 |
| hunterxhunter | B | G | G | G | 8 | F03 | F01 |
| hyperlightdrifter | D | D |  |  | 12 | F07 | F08, F09, F15, F16, F24 |
| iastate | A | C | C | C | 10 |  |  |
| ibo | H (thin) | H |  | B | 4 |  |  |
| ice_poseidon | H | H | A |  | 11 | F21 |  |
| iceland | G (thin) | G |  |  | 1 |  |  |
| ik_ihe | E (thin) | E |  |  | 2 | F16 |  |
| india | D | D | C |  | 14 | F08 | F23, F33 |
| indieheads | F | C | C |  | 17 | F01 | F07, F09 |
| indonesia | B | C |  | C | 16 | F25 |  |
| ireland | C | C |  |  | 10 |  |  |
| israel | C | C |  | G | 7 | F07 | F10 |
| italy | D | D |  |  | 9 | F12 | F11 |
| Jamaica | B | B (tie: B, C) | C | A, C | 8 | F15 |  |
| japan | B | B |  |  | 11 | F15 | F32 |
| jerma985 | A | A |  |  | 16 | F09 | F29 |
| k_on | B | H | H |  | 8 |  |  |
| kamenrider | A | G |  |  | 11 | F15 | F21 |
| kanye | A | H |  | B, E | 14 | F06 | F01, F11 |
| katawashoujo | C | C |  |  | 6 | F07 |  |
| kcroyals | B | C |  | D | 10 | F18 | F08, F17 |
| kerbalspaceprogram | A | H | H | B | 10 | F01 | F02 |
| kilian | E | G | G |  | 5 | F16 |  |
| kindafunny | C | C |  |  | 6 | F34 |  |
| kingdomhearts | C | C (tie: C, G) |  | A, F, G | 9 | F09 |  |
| kirby | A | C | C | B | 7 | F18 | F01, F17, F25, F28 |
| konosuba | C | C |  |  | 5 | F33 |  |
| korea | G | C | C | B, C, F | 15 | F07 | F09, F10 |
| kpop | H | H | C |  | 7 | F01 |  |
| KState | D | D |  |  | 13 | F08 |  |
| kurdistan | B | H | H | G | 7 | F10 |  |
| kuwait | A | D |  | B, C, D, E | 10 | F33 |  |
| lakers | B | G |  | A, E | 13 | F16 | F27 |
| landry | G (thin) | G |  |  | 4 |  |  |
| latin | F | F |  |  | 9 |  |  |
| latvia | B | F (tie: C, F) |  | C, F | 8 |  |  |
| leafs | C | C (tie: C, G) | G |  | 7 |  |  |
| leagueoflegends | E | E (tie: C, E) | C |  | 7 |  |  |
| lebanon | A | G | G |  | 12 | F35 |  |
| lego | B | H |  |  | 12 | F13 | F11 |
| lexington | H (thin) | H (tie: A, H) | A |  | 2 |  |  |
| lifeisstrange | G | G |  |  | 10 | F26 |  |
| linux | D | D |  |  | 11 | F10 | F15, F16 |
| liquicity | A | B | B | B, E, F | 11 | F15 |  |
| lithuania | B | E (tie: E, G) |  | E, G | 8 | F16 |  |
| littlebusters | B (thin) | B |  |  | 1 |  |  |
| littlewitchacademia | A | A (tie: A, B) | B | B | 13 | F10 | F15, F30, F35 |
| livecounting | D (thin) | D |  |  | 4 | F08 |  |
| liverpoolfc | E | E | C |  | 6 | F29 |  |
| lofihiphop | E | B | B |  | 6 | F15 | F21, F30 |
| loliconsunite | E | E |  |  | 16 | F23 | F30 |
| loltyler1 | D | D |  |  | 10 | F08 |  |
| lost | B | C | C | A, C | 8 |  |  |
| lovelive | B | F |  | A, E, F | 9 | F13 | F11 |
| lsu | F | F |  |  | 13 | F09 | F28, F30 |
| luciomains | C | C |  |  | 9 | F19 | F07, F17, F32 |
| Lugarix | K |  |  |  | 0 |  |  |
| luxembourg | B | H | H | A, H | 11 | F32 |  |
| Madeon | C | C |  |  | 5 |  |  |
| madokamagica | E | H | H |  | 9 |  |  |
| magictcg | B | H | H |  | 16 | F01 | F03, F04 |
| malaysia | G | G |  |  | 11 | F09 | F28, F31 |
| malta | A | C | C | B, C, E, F | 5 |  |  |
| mamamoo | H (thin) | H (tie: A, H) | A |  | 1 | F35 |  |
| ManningPlace | G | G |  |  | 5 | F26 |  |
| Mario | B (thin) | B |  |  | 2 | F12 | F11 |
| mariokart | H (thin) | H |  |  | 4 | F03 | F01 |
| marvel | F | F | C |  | 7 | F34 |  |
| maryland | A | C (tie: C, H) | C, H | C | 8 | F22 | F26 |
| masseffect | F | F |  |  | 9 | F09 | F29 |
| math | A | G | G |  | 12 |  |  |
| mcgill | E (thin) | E |  |  | 1 | F16 |  |
| mcgillrobotics | K |  |  |  | 0 |  |  |
| mechanicalkeyboards | G | G |  |  | 14 | F26 |  |
| megaman | A | C | C | C | 15 | F07 |  |
| metalcore | A | A |  |  | 14 | F27 |  |
| metalgearsolid | C | C |  |  | 13 | F01 | F05, F07, F16 |
| metroid | C | G | G | B, D, F, G | 15 | F26 | F31 |
| mexico | D | D |  | E | 8 | F08 | F29 |
| miamidolphins | G | G |  |  | 6 | F26 |  |
| MiamiHurricanes | F | G (tie: F, G) | G | G | 6 |  |  |
| mindcrack | C | G (tie: D, G) | D, G | A, B, D, E, G | 14 | F24 | F28, F31 |
| minecraft | H | H |  |  | 15 | F01 | F03, F05 |
| minnesotavikings | D | D |  |  | 9 | F08 |  |
| miraculousladybug | F (thin) | F (tie: F, H) | H | B | 4 | F05 | F01, F11 |
| mit | A | C (tie: C, G) | C, G | C | 8 | F10 | F28, F33 |
| mizzou | A | A |  |  | 8 |  |  |
| mls | D | G |  | A, B | 17 | F06 | F01, F31 |
| MMA | B | H |  | H | 14 | F01 | F02 |
| monalisaclan | B | G |  | A, E, G | 17 | F15 | F16, F25, F26 |
| monero | D | D |  |  | 11 | F16 |  |
| MonkeyIsland | A | A |  |  | 10 | F15 |  |
| monstercat | D | H | H |  | 15 | F01 | F02, F04 |
| monsterhunter | A | A (tie: A, D, G) |  | B, D, E | 6 |  |  |
| montenegro | E (thin) | E (tie: C, E) | C |  | 3 | F16 |  |
| Moondye7 | G | G |  |  | 6 | F19 | F10, F15, F17 |
| mordhau | F (thin) | F | A |  | 3 |  |  |
| morrowind | B | C | C | A, C, G | 15 | F07 |  |
| msu | D | G | G | A, B, C, E, F, G | 7 | F09 | F10, F15 |
| muse | C | C |  |  | 6 | F07 |  |
| mylittlepony | B | D | D | A, D, E | 20 | F16 | F22, F25 |
| mysterydungeon | B | G (tie: C, G) |  | A, G | 9 |  |  |
| n64 | K |  |  |  | 0 |  |  |
| naruto | B | B (tie: A, B) |  |  | 11 | F02 | F01, F11, F12, F23 |
| nascar | G | G |  |  | 9 | F10 | F26 |
| natsume | A (thin) | C | C | B, C, E | 3 |  |  |
| nbaspurs | F | G | G | G | 21 | F01 | F04, F05, F09, F24, F31 |
| necrodancer | C | C |  |  | 8 | F09 | F28, F29, F33 |
| neopets | A | G |  | B, E, G | 16 | F29 |  |
| nerf | B | B |  | A, C | 10 | F15 |  |
| neu | D | G | G |  | 7 | F08 |  |
| neutralmilkhotel | G (thin) | G |  |  | 3 |  |  |
| NewMexico | C | G | G |  | 10 | F10 | F26, F33 |
| newzealand | A | H | H | B | 14 | F07 | F32 |
| NieR | H | H | C |  | 8 | F05 | F01 |
| nightinthewoods | B | B |  |  | 14 | F01 | F15 |
| nin | C | C |  | B | 20 | F18 | F17, F34 |
| nintendo | H | H |  |  | 16 | F01 |  |
| nlsscirclejerk | A | A | C |  | 11 | F34 |  |
| nonbinary | K |  |  |  | 0 |  |  |
| norge | H (thin) | H |  |  | 1 |  |  |
| Northwestern | F | F |  |  | 8 |  |  |
| norway | G | H | H | B | 13 |  |  |
| notredame | G | G |  |  | 9 | F07 | F10 |
| NovaScotia | K |  |  |  | 0 |  |  |
| npr | B | B | G | G | 9 |  |  |
| nuclearthrone | B | C |  | A | 10 | F33 |  |
| nVade | A | A | G |  | 14 |  |  |
| nyjets | B | F (tie: F, H) |  |  | 13 | F02 | F01, F09, F15 |
| nyu | B | A (tie: A, H) | A, C, H | A, F | 6 |  |  |
| ockytop | D | H | B, H | A, B, C, E, G, H | 9 | F15 | F23, F32 |
| ohio | E | G |  |  | 10 | F10 |  |
| Okami | B | C | C |  | 8 | F19 | F15, F17 |
| OKState | D | D |  |  | 7 | F08 | F24 |
| oltp | A (thin) | A |  |  | 1 |  |  |
| oman | H (thin) | F | F | B | 2 |  |  |
| OnePiece | B | C |  | A, C | 17 | F22 | F07, F27, F32 |
| oneplus | H | H | C |  | 6 | F01 |  |
| onepunchman | G (thin) | G | E |  | 4 | F10 |  |
| oneshot | B | G | G | A, E, G | 5 |  |  |
| OneTrueEmilia | A | A |  |  | 8 | F21 | F22, F27 |
| ontario | H | H |  |  | 5 | F01 | F02, F03, F05 |
| opticgaming | G | G |  |  | 16 | F19 | F17 |
| orderofthebluecorner | B | A (tie: A, F) | A, F | A, E, F | 6 |  |  |
| OrderOfTheKoi | E | F | F |  | 7 | F16 | F30 |
| osu | H | H (tie: C, H) | C |  | 14 | F07 | F21 |
| osugame | E | H |  | B | 20 | F29 |  |
| overwatch | E | H |  | A, B, C, D, F, G, H | 23 |  |  |
| pakistan | D | C (tie: C, G) |  | C | 12 | F08 | F28 |
| paladins | B | H |  | A | 25 | F01 | F06, F25, F30 |
| palestine | C | C |  | B | 5 | F34 |  |
| pansexual | G (thin) | G |  |  | 3 |  |  |
| parabola | A (thin) | A (tie: A, B) | B |  | 3 |  |  |
| paragon | H | H |  |  | 11 | F01 | F02, F33 |
| parahumans | E | H | H | A, B, H | 15 | F25 | F27 |
| paranatural | F | F |  |  | 10 |  |  |
| parrots | A | A |  |  | 10 | F13 | F11 |
| partyparrot | E | H |  | A, B, C, D, G, H | 15 |  |  |
| pathofexile | E | G | G | B, C, G | 12 |  |  |
| patriots | B | B (tie: B, D) |  | D | 10 | F21 |  |
| paydaytheheist | B (thin) | C | C | C | 4 | F32 |  |
| pcmasterrace | A | H |  | E, H | 17 | F25 | F01, F05, F16, F21, F27, F30 |
| pebble | F | F |  |  | 13 | F09 |  |
| penguins | F | F |  |  | 14 | F09 | F34 |
| pepe | D | D |  |  | 8 | F08 |  |
| Peru | G | G | C |  | 12 | F30 |  |
| peterdraws | G (thin) | G (tie: C, F, G) | C, F | F | 3 |  |  |
| pgang | K |  |  |  | 0 |  |  |
| philippines | B | B |  |  | 12 | F15 |  |
| phish | D | D |  |  | 11 | F01 | F08, F10, F23 |
| physical_removal | A (thin) | A (tie: A, F) |  | B | 3 | F23 |  |
| picturegame | H (thin) | H |  |  | 4 | F25 | F21 |
| Pigifs | B (thin) | C | C |  | 4 |  |  |
| PinkUnion | F | F (tie: F, G) |  |  | 9 |  |  |
| PinkVomitMonster | E | G | G | B, G | 5 |  |  |
| pitt | C | C |  |  | 9 | F14 | F07, F11 |
| placecanada | D | D |  |  | 13 |  |  |
| placeDE | H | D |  | B, C, D, E | 9 | F23 |  |
| placehearts | E | A | A |  | 6 |  |  |
| placehfarts | H (thin) | H |  | B | 1 |  |  |
| PlaceNL | D | D |  |  | 22 | F08 | F22, F25 |
| placeportalpattern | G | G |  |  | 9 | F23 | F24, F26 |
| placesnek | E | C | C | A, B, C, D, G | 13 |  |  |
| placestart | D | E (tie: C, E, F, G) |  | E | 12 | F15 | F29 |
| placetardis | G | G | A, H |  | 12 | F10 | F15, F26 |
| planetside | E | F | F | F | 20 | F03 | F01, F29, F30 |
| pokemon | A | A |  |  | 8 | F27 |  |
| PokemonSage | K |  |  |  | 0 |  |  |
| poland | G | G |  |  | 10 | F10 | F16, F24, F26 |
| polandball | H | C | C |  | 7 | F02 | F01 |
| polska | E | E (tie: C, E) | C |  | 10 | F12 | F07, F11 |
| polyamory | H | H | A |  | 5 | F35 |  |
| popheads | B | H |  | H | 10 | F01 | F05 |
| portal | F | F |  |  | 15 | F33 |  |
| porterrobinson | C | C |  | B | 17 | F07 | F24, F30 |
| portugal | E | G (tie: G, H) |  |  | 17 | F13 | F11, F29 |
| PORTUGALCARALHO | C (thin) | C |  |  | 3 | F34 |  |
| predators | D | H | H |  | 13 | F08 | F22 |
| prequelmemes | E | E (tie: E, G) |  |  | 25 | F13 | F11, F23, F24, F25, F30, F31 |
| Produce101 | F (thin) | F |  |  | 2 |  |  |
| ProfessorLayton | C | C |  |  | 8 |  |  |
| PUBATTLEGROUNDS | A | C | C | C | 14 | F03 | F01, F07 |
| purdue | D | D |  | A, B | 16 | F08 | F35 |
| purplecorner | B | G (tie: C, G) |  |  | 16 | F23 |  |
| PurplePixels | E | E (tie: E, G) |  |  | 13 | F16 |  |
| pusheen | F | F | C |  | 5 | F07 | F09 |
| puzzleanddragons | A | A (tie: A, C) |  |  | 12 | F07 |  |
| python | D | D | G |  | 12 | F08 | F26 |
| qotsa | F | F |  |  | 8 |  |  |
| quebec | A | E |  | B, D, E | 22 | F28 | F29 |
| quq | K |  |  |  | 0 |  |  |
| radiohead | A | A |  |  | 17 | F27 |  |
| Rainbow6 | A | G | G | B, G | 12 | F01 | F07, F20 |
| rainbowgrid | G | G |  | B | 10 |  |  |
| rangers | E | D (tie: D, E) |  | C, D | 14 | F29 | F33 |
| raocow | A | A | H |  | 9 | F35 |  |
| ravens | A | B | B | B | 16 | F15 | F26 |
| re_zero | E | C | C | C | 12 | F20 | F28, F29 |
| ReBoot | B (thin) | B |  | F, G | 2 |  |  |
| reddevils | A | F |  | E | 22 | F03 | F01, F29, F30 |
| redhotchilipeppers | E | A | A |  | 5 | F16 |  |
| Redox | K |  |  |  | 0 |  |  |
| redpandas | A | C |  | C | 11 | F22 |  |
| redvsblue | G (thin) | G |  |  | 3 |  |  |
| RelientK | B | G | G | A, F, G | 11 | F22 |  |
| rhythmheaven | B | G | G | C, G | 9 | F21 | F34 |
| rickandmorty | B | C | C | A, C | 12 | F32 |  |
| ripcity | G | G |  | E | 8 | F18 | F17, F28, F32 |
| riskofrain | G | G |  |  | 5 | F10 |  |
| rit | A | G | G, H | G | 10 |  |  |
| rocketbeans | A | B | B |  | 14 | F19 | F17 |
| rocketleague | B | G | G | F, G | 10 |  |  |
| rojava | A | A | C |  | 5 |  |  |
| romania | A | H | H | B, H | 15 | F01 | F11, F13, F21 |
| roosterteeth | B | B |  |  | 5 |  |  |
| rotmg | B | F |  |  | 20 | F23 |  |
| rpi | C | F (tie: D, F) |  | D, F | 11 | F08 |  |
| runescape | D | D | H |  | 11 | F01 | F06, F08 |
| rush | F | C | C |  | 8 | F02 | F01, F09, F22 |
| russia | F | F |  |  | 7 | F22 |  |
| Russiaclan | B | H |  |  | 13 |  |  |
| rust | D | D |  |  | 20 | F08 | F01, F06 |
| rutgers | B | D |  | A, D | 15 | F09 | F21, F22, F24 |
| rwby | F | G | G | B, G | 14 | F01 | F02, F09 |
| sabres | H | H |  |  | 8 | F12 | F11 |
| sadboys | B | A |  | A | 11 | F12 | F11, F31 |
| sakartvelo | K |  |  |  | 0 |  |  |
| sakuragakuin | A | C |  | B, C | 6 |  |  |
| samuraijack | E | G |  | A | 21 | F01 | F29 |
| satania | C | C |  |  | 10 | F07 |  |
| sbu | D | D |  |  | 7 | F08 |  |
| schoolidolfestival | B | G | G | G | 11 | F01 | F02, F05, F23 |
| scotland | H | H | C | C, D | 9 | F24 |  |
| ScottPilgrim | C | G | G | A, G | 5 |  |  |
| scp | F | A |  | A, B, E | 14 | F21 | F30 |
| seahawks | A | C | C | B, C, H | 16 | F01 | F07, F25, F31, F35 |
| seolhyun | G (thin) | G | F |  | 3 | F09 | F10 |
| serbia | D | H | H |  | 9 | F08 |  |
| seventeen | B (thin) | B |  | A, D, F, G, H | 2 |  |  |
| sheffield | C | C |  |  | 14 | F07 |  |
| shield | C | G | G | G | 10 | F07 |  |
| shishamo | B (thin) | B |  | F, G | 1 | F22 |  |
| shitredditsays | B | A (tie: A, H) | A, H | A, C, D, E, H | 11 | F24 |  |
| shrooms | A (thin) | A (tie: A, F) | F |  | 1 |  |  |
| signal | K |  |  |  | 0 |  |  |
| simonfraser | E | E |  |  | 5 | F22 | F30 |
| singapore | B | F |  | A, F | 13 |  |  |
| sips | D | F | F | F | 21 | F20 | F21, F24 |
| sixers | A | A |  |  | 13 | F27 |  |
| skyrim | C | G | G | A, G | 7 | F10 |  |
| Slovakia | G | G |  | B | 8 |  |  |
| slovenia | D | D |  |  | 6 | F08 |  |
| smashbros | E | E |  |  | 7 | F02 | F01 |
| smite | B (thin) | C | C | A | 2 | F22 |  |
| snsd | F | F |  |  | 11 |  |  |
| sonicthehedgehog | A | A (tie: A, F, G, H) |  | G | 6 |  |  |
| sooners | D | D |  |  | 10 | F08 |  |
| southafrica | C | G | G |  | 7 | F21 |  |
| southpark | A | A | H |  | 11 | F21 |  |
| soylent | A | A (tie: A, F) | F | F | 7 | F26 |  |
| spacex | H (thin) | H | C |  | 4 | F06 | F01, F17 |
| spacexmasterrace | D | C | C | C | 11 | F07 | F08 |
| spain | B | E |  | D, E | 17 | F16 |  |
| spelunky | H (thin) | H |  |  | 4 | F01 |  |
| splatoon | A | H | H | G | 15 | F17 |  |
| spongebob | B | E |  | E | 11 | F15 | F16, F30 |
| SquareSpiral | B | F | F | A, F | 11 | F09 | F23 |
| ss13 | C | B |  |  | 15 | F15 |  |
| ssbpm | E | E |  |  | 12 | F16 |  |
| starbound | A | G | G |  | 10 | F35 |  |
| starcitizen | B | D |  | D | 21 | F08 | F25 |
| starcraft | A | C | C | B, C, G, H | 15 | F01 | F06 |
| stardewvalley | F | F |  |  | 11 | F09 | F15, F21, F28, F32 |
| stardustcrusaders | E | C | C | C | 14 | F01 | F30 |
| stargate | B | H | F, H | F, H | 12 | F01 | F04, F09, F11, F12, F25, F35 |
| starlightstage | B | G | G | C, G | 14 | F10 | F21, F33, F34 |
| starryknights | B | B | E | A, E | 12 | F15 | F16 |
| startrek | K |  |  |  | 0 |  |  |
| starvstheforcesofevil | A | G | G | B, G | 6 | F23 | F32 |
| stevenuniverse | E | E |  |  | 19 | F01 | F16, F25, F26, F29 |
| stlouis | A | A |  |  | 12 | F20 |  |
| stlouisblues | B | G | G | A, C, G | 13 |  |  |
| strangerthings | C (thin) | C (tie: C, G, H) | G, H |  | 3 | F34 |  |
| straya | D | B | B | B, C, G | 7 |  |  |
| streetfighter | F | F |  |  | 9 | F03 | F01, F21 |
| Summit1G | G (thin) | G |  |  | 4 |  |  |
| suomi | C | H |  | A, B | 20 |  |  |
| superman | C (thin) | C |  |  | 2 | F33 |  |
| survivor | B | B | H | H | 11 | F02 | F01, F15 |
| sweden | E (thin) | E |  |  | 4 |  |  |
| SwissNeutralityZone | B | C | C | C, E, G | 7 | F19 | F15, F17, F28, F29 |
| switzerland | A | G | G | G | 11 | F10 |  |
| swordartonline | B | H |  |  | 12 | F18 | F01, F17 |
| SydneyFC | C (thin) | C |  | B | 2 |  |  |
| tagpro | E | E |  |  | 10 | F29 |  |
| taiwan | C | C |  |  | 7 | F18 | F17 |
| tampabaylightning | C | C |  |  | 6 | F07 |  |
| teamcube | C | C |  |  | 10 |  |  |
| TeamDignitas | A | A (tie: A, H) | H | H | 8 |  |  |
| TeamYellowPlace | G (thin) | G |  |  | 3 |  |  |
| telegram | A | A | G |  | 7 |  |  |
| Temple | D | D (tie: D, F) |  |  | 17 | F08 | F09, F25 |
| tenma | H (thin) | H (tie: A, H) | A |  | 1 | F35 |  |
| terraria | A | G | G | G | 12 | F01 | F02, F03, F25, F31 |
| teslamotors | A | C (tie: C, G) | C, G | C, D | 7 | F08 |  |
| tetris | C (thin) | C |  |  | 3 |  |  |
| texans | D | H |  | A, B, H | 15 | F02 | F01, F11, F14 |
| texas | C | G | G | D | 10 | F08 |  |
| texastech | B | H | D, H | C, D, G | 6 |  |  |
| tf2 | C | C |  |  | 5 | F33 |  |
| thailand | B | G | G, H | A, C, G, H | 14 | F26 |  |
| the_pack | A | H | H | B, H | 10 |  |  |
| THE_R | A (thin) | A |  |  | 1 | F27 |  |
| TheAdventuresofTintin | C (thin) | C |  |  | 3 |  |  |
| TheB1G | G (thin) | G |  |  | 4 |  |  |
| theblackvoid | D | A |  | A, B, E | 12 | F12 | F11 |
| thebluecorner | B | C |  | E | 20 | F23 | F25, F29 |
| theexpanse | E | G | G | A, B, G | 24 | F16 | F23 |
| TheFarLeftSide | B | A (tie: A, H) |  |  | 13 | F23 |  |
| Thegreatblackhole | B | H | H |  | 6 |  |  |
| TheGreatGreenBox | B (thin) | F |  | F | 4 |  |  |
| TheHulk | A | A (tie: A, C) | C | C | 13 | F07 | F32, F35 |
| TheID | K |  |  |  | 0 |  |  |
| theitalyplace | D | D |  |  | 9 |  |  |
| thenetherlands | B | H | H | A, G, H | 8 | F02 | F01 |
| thepointing | A | A (tie: A, C) | C |  | 10 | F09 |  |
| thesilphroad | B (thin) | D (tie: C, D, G) |  | D | 4 |  |  |
| thesimpsons | A | A (tie: A, C) |  |  | 7 | F01 |  |
| thetreesnetwork | A (thin) | C | C | B, C, E | 4 |  |  |
| timbers | C | C |  | A | 13 | F07 | F21 |
| tinytardis | A | A |  | B | 8 | F15 | F22, F25 |
| titanfall | B | H |  | G | 10 | F01 | F21 |
| tokyo | B (thin) | B |  |  | 3 | F20 |  |
| toolband | A | G (tie: A, G) | G | G | 10 | F09 | F27 |
| torontoraptors | C | C (tie: C, G) | G |  | 14 | F07 | F31, F33 |
| totallynotrobots | B | H | H | H | 17 | F01 | F02, F25 |
| touhou | E | G |  | B, G | 14 | F13 | F11, F23, F28 |
| traaaaaaannnnnnnnnns | A | A |  | G | 15 |  |  |
| TransFlagPlace | E | E |  |  | 5 | F16 |  |
| transformers | A | G | G, H | B, G | 13 | F10 | F21, F26 |
| transgender | H (thin) | H (tie: A, H) | A |  | 3 |  |  |
| TreePlace | F (thin) | F | C |  | 4 |  |  |
| trees | C | C |  |  | 6 |  |  |
| truestl | C | G | G | G | 5 |  |  |
| TsundereSharks | A | A |  |  | 10 | F07 |  |
| turkey | B | C |  | A | 17 | F09 | F27 |
| twentyonepilots | F | F |  |  | 16 | F25 |  |
| twice | E | G | G | G | 6 | F09 |  |
| twitch | F | F |  |  | 8 | F07 | F21 |
| twitchplayspokemon | B | H | H | A, F, H | 17 | F01 | F09, F27 |
| ubc | G (thin) | G |  |  | 3 | F22 |  |
| ubreddit | G | F | F, H | F | 10 | F09 |  |
| ucf | B | A | A | A | 11 | F15 |  |
| udub | B | B |  | C | 5 | F15 |  |
| ufl | B (thin) | A (tie: A, H) | A, H | A, D | 4 |  |  |
| uiowa | D | F | F |  | 11 |  |  |
| uiuc | F | F |  |  | 13 | F09 | F26 |
| ukplace | D | D |  |  | 7 | F08 |  |
| ukraine | D (thin) | D |  |  | 3 | F08 |  |
| ultrahardcore | H | H |  |  | 8 | F01 | F04 |
| UMiami | K |  |  |  | 0 |  |  |
| undertale | E | E |  |  | 9 | F32 |  |
| unitedkingdom | C | C | D | D | 7 | F07 |  |
| UNLincoln | K |  |  |  | 0 |  |  |
| unturned | C | C |  | A | 16 | F21 | F24, F32 |
| uofm | A | D |  | B, D | 12 | F08 | F15 |
| uofmn | D | B | B |  | 9 | F10 | F15 |
| uoft | A | G (tie: G, H) |  | B, C, D, G, H | 13 | F24 | F31 |
| UPenn | F | F |  |  | 7 | F09 |  |
| uruguay | B | C | C | A, C, E, F | 7 |  |  |
| utahjazz | F | F (tie: A, C, F) |  | A, B | 12 | F14 | F09, F11 |
| utaustin | B | G (tie: G, H) |  | D, F, G | 20 | F28 | F17, F18, F21 |
| uva | A | G | G | G | 9 |  |  |
| uvic | C | C |  |  | 8 | F07 |  |
| uwaterloo | B | H |  | A, H | 17 | F02 | F01 |
| vegan | A | A (tie: A, H) | H | B, H | 8 |  |  |
| VelvetUnderground | A (thin) | G | G | G | 2 |  |  |
| vermont | G | G | A | A, E | 8 |  |  |
| vietnam | C (thin) | C |  |  | 2 |  |  |
| Villanova | A | A |  |  | 5 |  |  |
| vim | H (thin) | H (tie: A, H) | A, C | B | 4 | F32 |  |
| vinesauce | F | F |  |  | 11 | F09 | F31 |
| virginiatech | D | D |  |  | 13 | F08 |  |
| vocaloid | B | C | C, E | C, E | 8 | F17 | F19 |
| wales | E | E |  |  | 8 |  |  |
| wallstreetbets | D | H | H |  | 13 | F08 |  |
| warframe | B | G | G | C, G | 21 | F01 | F02, F03, F21, F25 |
| wario | K |  |  |  | 0 |  |  |
| warriors | A | A |  |  | 9 | F13 | F11 |
| warthunder | F | F |  |  | 12 | F09 |  |
| watchmen | C (thin) | C |  |  | 1 |  |  |
| weezer | A | C | C | B, C, E, G | 15 | F18 | F17 |
| wholesomememes | A | A |  |  | 24 | F01 | F27 |
| wildhockey | D | D | F |  | 16 | F01 | F08, F09 |
| wine | C | C |  |  | 8 | F19 | F17, F22, F33 |
| winnipegjets | A | G | G, H | G | 8 |  |  |
| WisconsinBadgers | B (thin) | B |  | D | 4 | F15 |  |
| witcher | B | G | G | A, G | 13 | F27 | F31 |
| worldoftanks | B | G (tie: G, H) |  |  | 14 | F02 | F01 |
| worldpowers | D | A |  | A, B, E | 7 |  |  |
| wow | H | H | A |  | 11 | F01 | F35 |
| WPI | D (thin) | D (tie: D, G) | G |  | 3 | F08 | F10 |
| wsu | B (thin) | B |  |  | 3 |  |  |
| xcom | E | G | G |  | 14 | F30 |  |
| xenoblade_chronicles | B | G | G | A, G | 14 |  |  |
| yerbamate | K |  |  |  | 0 |  |  |
| yogscast | B | C | C | A | 9 | F19 | F01, F17, F22 |
| yugioh | H | F | F | B, C, F | 17 | F03 | F01, F34 |
| yumenikki | B | C |  | A | 6 |  |  |
| yuyuyu | B | C | C |  | 7 |  |  |
| zelda | H | H |  |  | 15 | F01 | F02, F03 |
| zootopia | C | D | D | D | 15 | F08 | F17 |

