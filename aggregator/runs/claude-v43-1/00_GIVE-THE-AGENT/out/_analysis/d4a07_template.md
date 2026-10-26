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

{{TABLE:count}}

The merge-height gap is longest at k = 8 (0.149, against 0.140 at k = 5), and the stability margin rises to 0.101 at k = 8. The two measures agree. Every real stability is still low (0.13 to 0.20), though from k = 5 to 8 it lies above the shuffled null's 95th percentile.

## 4. The eight forms

By Ward on the defining rooms the forms hold 132, 131, 67, 60, 54, 44, 38 and 32 rooms (ratio 4.13). Placed by the whole mix they hold 148, 159, 87, 64, 60, 56, 59 and 51 (ratio 3.12). The ratio is above J's bound of 3 because the middle form B is the largest; without B it is 2.90. Every form has a signature, and none is set apart only by breadth. B's signature is weak, and I report it as a mixture.

{{TABLE:forms}}

Several signatures are now links:
- **C:** the design to the template (A11).
- **D:** keeping to scripts (A06), and borders to sparing (A05).
- **F:** judging hands too few to the move (A10), and the move to building again.
- **G:** borders to sparing (A05), and keeping to borders (A04).

## 5. The members, read as rooms, and whether a differing account could be written

I read each form's best fits and misfits through their lines' how sentences, with the members' lines on each signature column by op (`_analysis/d4a07_read.py`). Best fits and misfits are taken among defining rooms.

{{TABLE:read}}

- **A, keeping and calling.** r/warriors arranges coverage across members' sleep by handoff; r/FlaggyFlag keeps attribution provisional. The misfits (r/chelseafc, r/falcons, r/kuwait) have none of their changes on A's signature and lie near several forms.
- **B, the middle.** r/ghibli clarifies which corner an anchor marks; r/roosterteeth finds a template that no longer fits. The misfits are rich rooms whose changes spread over many forms (r/paladins, 25 changes; r/warframe; r/gamindustri).
- **C, the design.** r/guatemala asks for publicity after its first placement; r/CSUFoCo keeps trying to restore its spot despite fewer hands. In r/metroid, a misfit near G and others, a source sprite stays open to colour checks after it is posted.
- **D, machine hands.** In r/rust a later target proposal threatens work marked for preservation; r/ukplace needs working chat access to change script targets; r/minnesotavikings tests a promised exemption for a neighbour, finds it missing, and fixes it after a failed update.
- **E, the chat.** r/bangladesh asks that the chat link and goals go into a public sticky; r/TransFlagPlace screens who enters and reports a ban.
- **F, the spot.** r/warthunder times its request for space around when the host's members are awake; r/twitch reports where an image stands. r/day9, the account's best-supporting room, is a thin room (3 changes) and is placed here, all its changes on the signature.
- **G, the terms between neighbours.** r/mechanicalkeyboards meets a contested overlap after a call; r/riskofrain sends negotiation to a chat where a representative must ask for diplomatic status.
- **H, the host sub's play and the call.** r/GuildWars2 tolerates the temporary play but not an extended unreadable styling; r/ontario enacts the fake rules by bans and mock sanctions; r/anime_irl grants a holiday exception for a canvas post.

{{TABLE:accounts}}

## 6. The raiding and takeover rooms, and r/startrek

{{TABLE:sets}}

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

{{TABLE:rooms}}
