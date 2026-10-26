# Room forms, D4a-05: the top cut

Leg D4a-05, 26 October 2026, an addition after stage D5, on J's instruction through the handler. J, 17:27 Berlin: "I need to tell it to make something with 4 to 8 big forms and then continue clustering down to 700." J, 18:01 Berlin: stage D6 builds on these forms, with the 35 branches as the level below. J, 18:35 Berlin: "I mean as a leg that happened after not instead." J, 18:36 Berlin: "Let the agent know that as the cut is made we will need to talk to it, so that we go over the clustering in a way it makes sense for us all."

So this file holds the top cut only: eight forms of rooms and the core. The split below the forms waits for the talk with J. Nothing of D4 or D5 is replaced. `branches.jsonl`, `crosslinks.jsonl`, `tree-D4.md`, the forms and every D5 file are unchanged; I checked them against the D5b close snap (78 files, all unchanged). The amendment is dated in `departures.jsonl` (lines 11 and 12). The model is the one frozen at D3 (46384686…).

Files: `room-forms-D4a05.jsonl` (one line per form and the core, with members), `room-forms-D4a05.tsv` (one row per room), and this file. The computation is `_analysis/d4a05_room_tree.py`; its rule was logged before it ran.

## 1. What is compared

**The unit is the room.** Each of the 705 rooms appears once.

**A room's selected changes** are its accepted ledger lines that change the model: restrict, add-step, add-condition, link and contradict. Lines that instantiate an element or record an absence change nothing and are left out. There are 6,637 selected lines, 2,126 of them on arrows. 684 rooms hold at least one; 21 hold none, and they form the core. Three lines carry no lift and cannot be placed.

**What counts.** Each line counts once at its third-order theme, once at its fourth-order theme and once at its dimension, as the ladder lifts it. An arrow counts through the third-order theme of its source, as an element does. The op and the element are not features. 23 lines have no third-order node and 77 have no fourth-order node or dimension (the two residue themes that no fourth-order theme gathers); each counts only where it has a node.

**Mix, not number.** Within each level a room's counts become shares, so a room with 20 changes and a room with 8 are compared by how their changes divide, not by how many they made. A room with 8 changes, 4 of them in the order between rooms, sits with the rooms whose changes lean the same way.

**Changes made by one room.** The 23 third-order themes that only one room changes are dropped at that level, so that no single room's change sets a column. At the fourth-order level and the dimension, every node is changed by more than one room.

**The distance.** The Hellinger distance between two rooms' shares at each level, the three levels counting equally. That leaves 147 third-order columns, 28 fourth-order and 8 dimensions. The rooms were joined by Ward's method, which seeks compact groups. Ward's method favours groups of similar size, so part of the size balance below comes from the method.

## 2. The count, and why eight

J set the range at 4 to 8 forms. The rule I logged before the run: take the k with the highest silhouette (how much nearer a room is to its own form than to the next), provided its bootstrap stability is 0.5 or more; otherwise the most stable k. The null permutes each column across rooms, which keeps how often each node is changed and breaks which changes go together.

| k | sizes | largest to smallest | silhouette | null 95th percentile | bootstrap adjusted Rand |
|---|---|---|---|---|---|
| 4 | 250, 213, 152, 69 | 3.62 | 0.0129 | 0.0107 | 0.122 |
| 5 | 213, 152, 147, 103, 69 | 3.09 | 0.0194 | 0.0088 | 0.138 |
| 6 | 152, 147, 125, 103, 88, 69 | 2.20 | 0.0230 | 0.0090 | 0.155 |
| 7 | 152, 125, 119, 103, 88, 69, 28 | 5.43 | 0.0277 | 0.0084 | 0.171 |
| 8 | 152, 119, 103, 88, 83, 69, 42, 28 | 5.43 | 0.0296 | 0.0074 | 0.182 |

The silhouette and the stability both rise steadily from 4 to 8, so no count in the range stands out. Every k has a stability below 0.5, so the rule takes the most stable k, which is also the one with the highest silhouette: k = 8. The best count lies at the edge of the range J set, and a higher k might score higher still; I did not look past 8.

**What the lower counts would join.** Ward's cuts nest, so each lower k joins forms of the eight (recomputed from the ledger, `_analysis/d4a05_top.py --what nesting`). At k = 7, E (design) joins G (scripts). At k = 6, H (the close) joins B (calls and the frame). At k = 5, D (templates and reports) joins E and G. At k = 4, C (space and exchange) joins B and H. Each join puts together two patterns that differ in what the rooms change.

**The sizes.** At k = 8 the largest form holds 152 rooms and the smallest 28, a ratio of 5.43, above J's bound of 3. The cause is H. Its 28 rooms make few changes (median 3), and 69 per cent of those changes are on the close (marking, recording and carrying on the work), against 15 per cent in the population. The ratio stays 5.43 at k = 7 and falls to 2.2 at k = 6, but only because H folds into B there, and B's rooms change calls and the April Fools frame. I keep H apart because its pattern differs from B's, and I report the cost. G, the next smallest (42), is the form whose signature its members share most widely: scripts are among the changes of 95 per cent of its rooms (A's border theme comes next, at 93). If J prefers forms of comparable size to the narrow patterns, k = 6 is the cut (sizes 152, 147, 125, 103, 88, 69).

## 3. The eight forms

The signature of a form is the fourth-order theme its members change far more often than the population does: at least 1.5 times the population's share, in at least a third of its members. Every form has one, so none of them is a broad form, set apart only by many or evenly spread changes. A room *fits two forms equally* when the centre of another form is within 5 per cent of its distance to its own. A room is *nearer another form* when another form's centre is closer than its own; Ward's method allows this. A *secondary form* is another form whose signature themes hold 25 per cent or more of the room's selected changes. The clusterwise Jaccard is Hennig's (2007) measure of how well a form survives resampling: 0.75 or more is stable, below 0.5 the form dissolves.

| form | rooms | the pattern of change | signature: fourth-order node (share of members' changes; times the population; members holding it) | median changes | fit two forms equally | nearer another form | none of its changes on the signature | with a secondary form | clusterwise Jaccard |
|---|---|---|---|---|---|---|---|---|---|
| A | 152 | the terms between neighbours reworked | T4-016 Negotiated order (0.33; 2.4; 93%) | 10 | 57 | 33 | 10 | 82 | 0.356 |
| B | 119 | the call and the April Fools frame reworked | T4-005 Mobilization (0.16; 3.4; 64%); T4-001 Keying (0.10; 2.8; 43%) | 10 | 63 | 37 | 20 | 36 | 0.292 |
| C | 103 | space and exchange between rooms reworked: spots lost, chosen or yielded, truces and help traded | T4-014 Territoriality (0.23; 3.5; 60%) | 9 | 56 | 36 | 41 | 51 | 0.286 |
| D | 88 | the template and the progress report reworked | T4-008 Standardization of output (0.18; 4.9; 61%); T4-007 Direct information sharing (0.14; 4.2; 41%) | 11 | 50 | 24 | 4 | 54 | 0.251 |
| E | 83 | the design reworked: what the mark shows argued, sized and taken into chat | T4-006 Collective representation (0.36; 3.1; 83%) | 7 | 38 | 27 | 14 | 48 | 0.282 |
| F | 69 | keeping reworked: defence and repair under conditions | T4-013 Repair work (0.30; 3.5; 90%); T4-010 Backstage decision-making (0.07; 1.8; 35%) | 8 | 20 | 11 | 7 | 26 | 0.324 |
| G | 42 | machine hands reworked: scripts installed, kept on target and argued over | T4-009 Workarounds (0.33; 7.1; 95%) | 11 | 7 | 5 | 2 | 21 | 0.324 |
| H | 28 | the marking and the record reworked, in rooms that change little else | T4-026 Completion ritual (0.36; 6.3; 71%); T4-027 Collective memory (0.25; 5.3; 43%) | 3 | 5 | 3 | 0 | 14 | 0.285 |
| K | 21 | the core: no selected change | none | 0 | | | | | |

**A, the terms between neighbours reworked (152).** Most of these rooms' changes sit where neighbours settle borders (in 92 per cent of members). They limit the model's arrows into and out of neighbour talk and sparing: negotiation can precede defence, and agreements are invoked but contested (restrict on A04, A05 and A13). They give deals steps and conditions (P08, P16). Counter-examples: 33 members are nearer another form, among them r/armok, r/babymetal, r/bostonbruins and r/DestinyTheGame; 10 have none of their changes on the border theme, among them r/counting, r/nin and r/parahumans.

**B, the call and the April Fools frame reworked (119).** These rooms change how a call is answered and when building follows it (restrict on A12, A01 and A02; add-step on P01). They also change how the sub's April Fools frame is tested, policed and ended (add-step and add-condition on K01). Calls to place are three and a half times as common in their changes as in the population's. B holds together loosely: in the median member only 18 per cent of the changes lie on its signature (in C, 17), 37 members are nearer another form, and 20 have none of their changes on it (among them r/buffalo, r/germany and r/lovelive).

**C, space and exchange between rooms reworked (103).** Half of these rooms' changes are in the order between rooms. They link the move back to building (P03), limit the move after a room judges its hands too few (A10), and change how a spot is chosen, yielded or lost (in 60 per cent of members). The rest of the form trades help and agrees truces, so 41 members have none of their changes on the spot theme; the form joins two kinds of change between rooms. 36 members are nearer another form, among them r/bakchodi, r/canucks and r/chess.

**D, the template and the progress report reworked (88).** These rooms change the model where members share coordinates, templates and how-to and report the mark's state. A template does not settle the design (restrict on A11); it needs upkeep of its own (add-step on P04); a report can come before the call or the upkeep. Only 4 members have none of their changes on its signature (r/belgium, r/frc, r/homelab, r/WPI); 24 are nearer another form.

**E, the design reworked (83).** These rooms change the model where the mark's design is settled (in 83 per cent of members): the design is argued and sized to the hands (P02), a template does not settle it (A11), and planning moves into a chat (P23). 27 members are nearer another form, among them r/aeskwadraat, r/brasil and r/cavestory.

**F, keeping reworked: defence and repair under conditions (69).** These rooms change the model where the work is watched, repaired and defended (in 90 per cent of members). Keeping gains conditions and steps (P05), the move after too few hands is limited (A10), and part of the keeping is arranged in a chat (P23). 11 members are nearer another form, among them r/epublica, r/portugal and r/PurplePixels.

**G, machine hands reworked (42).** Scripts for the work are among the changes of 95 per cent of these rooms. They give the machine hands steps and conditions (P14) and limit the arrow from strained upkeep to scripts (A06). Only 5 members are nearer another form (r/completeanarchy, r/czech, r/planetside, r/ssbpm, r/texans).

**H, the marking and the record reworked (28).** These rooms make few changes, and most sit at the close: celebrating, crediting and recording the work (P11, P12; restrict on A07 and A08). Every member has a change on its signature; 3 are nearer another form (r/AcePlace, r/kindafunny, r/magictcg).

**K, the core (21).** The rooms with no selected change: every accepted line of theirs instantiates an element or records an absence. They stay together, as the instruction says, and are not a form.

## 4. Kinds or cuts through a continuum

**The forms are cuts through a continuum of change mixes, not distinct kinds.** The evidence:
- **Separation.** The silhouette at k = 8 is 0.030. By Kaufman and Rousseeuw's reading, a silhouette below 0.25 shows no substantial structure. It is above the permutation null (0.0074), so the mixes are not random, but the forms barely separate.
- **Stability.** Redrawn on resampled rooms, the cut agrees with itself at an adjusted Rand of 0.18. Every form's clusterwise Jaccard lies between 0.25 and 0.36, below the 0.5 at which Hennig reads a cluster as dissolving.
- **Rooms between forms.** 296 of the 684 rooms fit two forms equally well, and 176 are nearer the centre of another form than their own. 332 have a secondary form.
- **Another linkage.** Average linkage on the same distance does not find these forms. It gives a chain, with 530 rooms in one group (adjusted Rand against the eight forms 0.05). Keeping the 23 single-room themes moves the cut a good deal too (adjusted Rand 0.46).

What does hold is each form's signature: a theme changed by most of the form's members and by few others. So the forms are best read as the eight directions in which the rooms' changes lean most, with most rooms leaning in more than one.

## 5. The forms against the rooms' codes

The tree does not use the rooms' first-order concepts. I read the forms against them afterwards. Each room's concepts were counted by the fourth-order themes their second-order themes are placed under, as shares. These codes are not independent of the changes: a ledger line lifts from the same second-order themes. So this check asks whether the forms differ in what the rooms talked about overall, not only where they changed the model.

- **They differ, weakly.** A permutation test of the form labels on the code shares gives a pseudo-F of 6.92, against a null 95th percentile of 1.22 (p = 0.001, 999 permutations). But the forms explain 6.7 per cent of the variation in the code shares. Assigned to the form whose code centre is nearest, 35.4 per cent of rooms land in their own form, against 11.6 per cent when the labels are shuffled.
- **Where they differ.** The over-represented code themes follow the signatures. A's codes lean to visibility returns and negotiated order, B's to collective efficacy and mobilization, C's to neo-tribes, territoriality and flagging the nation, D's to standardization of output and direct information sharing, E's to meta-organization and collective representation, F's to attribution and repair work, G's to workarounds (5.3 times the population), and H's to completion ritual, rivalry and collective memory.
- **Size.** The forms differ in room size. The median room has 26 coded concepts in H and 142.5 in D (Kruskal-Wallis H = 51.4). They differ in the number of selected changes too (H = 63.3; median 3 in H, 11 in D and G). The shares remove the number of changes from the distance, but a room with few changes has a sharper mix, so small rooms gather where one kind of change is enough: H.
- **The comparison's clusters.** The forms do not reproduce the code-based clusters of `chunk-share-D4` (adjusted Rand 0.012).

## 6. The 35 branches as the level below

J asked that stage D6 build on these forms with the 35 branches as the level below. The branches do not nest in the forms. A branch was cut on one shared key; a form gathers rooms by the mix of all their changes. Each branch's members spread across the forms. The share in its home form runs from 0.20 (F16) to 0.70 (F26). So a branch can be placed under the form holding most of its members, but most branches keep many members elsewhere. Each room's primary branch is the one whose key holds most of its selected lines (ties go to the subform, then to the branch cut first). Its other branches are listed as secondary in the room table.

| branch | members | home form | home share | members by form |
|---|---|---|---|---|
| F01 | 103 | B | 0.359 | A 13, B 37, C 6, D 13, E 16, F 5, G 10, H 3 |
| F02 | 33 | B | 0.485 | A 4, B 16, C 1, D 4, E 4, F 2, G 2 |
| F03 | 18 | B | 0.333 | A 4, B 6, C 3, D 1, E 2, G 1, H 1 |
| F04 | 13 | B | 0.385 | B 5, C 2, D 1, E 3, G 1, H 1 |
| F05 | 12 | B | 0.500 | A 2, B 6, C 1, D 1, E 1, G 1 |
| F06 | 8 | G | 0.375 | B 3, D 1, G 3, H 1 |
| F07 | 59 | A | 0.373 | A 22, B 9, C 3, D 3, E 13, F 6, G 2, H 1 |
| F08 | 50 | G | 0.520 | A 10, B 3, C 1, D 4, E 2, F 3, G 26, H 1 |
| F09 | 54 | C | 0.426 | A 6, B 11, C 23, D 3, E 7, F 3, G 1 |
| F10 | 38 | A | 0.684 | A 26, B 1, C 2, D 6, E 1, F 1, G 1 |
| F11 | 43 | B | 0.349 | A 8, B 15, C 3, D 3, E 7, F 4, G 2, H 1 |
| F12 | 22 | B | 0.455 | A 2, B 10, C 1, D 1, E 5, F 1, G 1, H 1 |
| F13 | 9 | E | 0.222 | A 2, B 2, D 1, E 2, F 2 |
| F14 | 7 | A | 0.429 | A 3, B 1, C 1, D 1, G 1 |
| F15 | 42 | D | 0.429 | A 8, B 7, C 3, D 18, E 2, F 2, H 2 |
| F16 | 35 | E | 0.200 | A 7, B 4, C 6, D 5, E 7, F 4, G 1, H 1 |
| F17 | 36 | A | 0.389 | A 14, B 1, C 4, D 5, E 2, F 3, G 1, H 6 |
| F18 | 15 | A | 0.533 | A 8, B 1, C 2, D 3, F 1 |
| F19 | 14 | H | 0.286 | A 4, C 1, D 2, E 2, G 1, H 4 |
| F20 | 10 | C | 0.300 | A 2, B 1, C 3, E 1, G 1, H 2 |
| F21 | 32 | B | 0.344 | A 10, B 11, C 3, D 2, E 2, F 3, G 1 |
| F22 | 30 | C | 0.267 | A 3, B 6, C 8, E 8, F 2, G 2, H 1 |
| F23 | 30 | A | 0.300 | A 9, B 8, C 5, D 1, E 1, F 3, G 2, H 1 |
| F24 | 27 | A | 0.333 | A 9, B 6, C 3, D 3, E 2, F 1, G 3 |
| F25 | 27 | B | 0.296 | A 7, B 8, C 5, D 2, E 2, G 2, H 1 |
| F26 | 23 | A | 0.696 | A 16, B 2, C 2, D 1, E 1, G 1 |
| F27 | 27 | A | 0.222 | A 6, B 5, C 5, D 6, F 5 |
| F28 | 22 | A | 0.545 | A 12, B 1, C 3, D 1, F 2, G 2, H 1 |
| F29 | 25 | F | 0.240 | A 6, B 4, C 1, D 2, E 4, F 6, G 2 |
| F30 | 24 | A | 0.208 | A 5, B 4, C 4, D 3, E 3, F 4, G 1 |
| F31 | 22 | A | 0.364 | A 8, B 4, C 4, D 4, E 2 |
| F32 | 21 | C | 0.238 | A 4, B 4, C 5, D 5, F 2, H 1 |
| F33 | 23 | A | 0.391 | A 9, B 1, C 3, D 1, E 5, F 1, G 2, H 1 |
| F34 | 22 | A | 0.273 | A 6, B 1, C 3, D 2, E 5, F 3, G 1, H 1 |
| F35 | 18 | B | 0.667 | A 1, B 12, C 2, D 1, E 1, F 1 |

## 7. For the talk with J

The split below the forms was computed before J's message of 18:36 arrived, and declared as moves 246 to 277. Move 278 withdrew those declarations; the computation is held in `_analysis/d4a05_tree3.json` as working material. One thing from it bears on the talk. Below the forms, the permutation null passed every split it tested, so I added a resampling test (logged before its run): a half is kept only if its clusterwise Jaccard is 0.6 or more. With it, splits hold in C, D, E and H, and none in A, B, F and G.

Questions I would bring:
- Is eight the count, or six, which keeps the sizes within J's bound at the cost of H and G?
- Should the three levels count equally? The third-order level has 147 columns and the dimension 8, so a common dimension can pull together rooms whose finer changes differ.
- Since the forms are cuts through a continuum, should a room carry weights in several forms rather than one membership?
- How should D6 relate branches that cut across the forms?

## 8. The room table

One row per room, in case-ignored order (also in `room-forms-D4a05.tsv`). *Secondary forms* hold 25 per cent or more of the room's changes on their signature themes. *Fits two equally with* names the other form whose centre lies within 5 per cent of the room's own. The branches are the 35 of D4, primary first.

| room | form | changes | secondary forms | fits two equally with | primary branch | secondary branches |
|---|---|---|---|---|---|---|
| 2007scape | F | 13 |  |  |  |  |
| 49ers | A | 14 |  |  | F10 | F21 |
| 4chan | G | 13 | B | B | F01 | F06, F08, F34 |
| aceattorney | B | 15 |  | A |  |  |
| acecombat | B | 9 | A, H | A | F02 | F01 |
| AceOfAngels8 | H | 1 |  |  |  |  |
| AcePlace | H | 9 |  | A | F17 | F25 |
| achievement_hunter | C | 3 | F |  |  |  |
| adventuretime | C | 13 |  |  | F09 | F25 |
| aeon | H | 7 | G |  | F19 | F08, F17 |
| aeskwadraat | E | 3 | H | H | F12 | F11, F34 |
| afip | G | 3 | B, H |  | F19 | F17 |
| aggies | A | 12 | G |  |  |  |
| ainbowroad | F | 19 |  |  |  |  |
| albania | H | 3 | E, G |  |  |  |
| alberta | B | 9 | E | E |  |  |
| AMD | E | 11 | B |  | F01 | F03, F04, F07 |
| AmericanFlaginPlace | F | 23 |  |  | F08 | F23, F29 |
| anaheimducks | B | 16 |  |  | F14 | F09, F11, F34 |
| anarchism | G | 5 |  |  |  |  |
| anarcho_capitalism | C | 12 |  |  |  |  |
| anarchocapitalism | F | 1 |  |  |  |  |
| androidgaming | C | 16 |  | B |  |  |
| animalcrossing | D | 10 |  |  | F09 | F15 |
| anime | A | 24 | H |  | F19 | F17 |
| anime_irl | B | 5 |  | E | F01 | F04, F05 |
| aoe2 | E | 2 |  | H | F34 |  |
| apocalypserising | H | 6 | F |  |  |  |
| AprilKnights | E | 6 | F |  | F16 | F29 |
| araragi | E | 5 |  |  |  |  |
| archlinux | A | 11 |  |  | F07 | F08 |
| argentina | E | 8 | F | B |  |  |
| armenia | D | 5 |  | E |  |  |
| armok | A | 14 | F | F | F27 |  |
| aromantic | E | 2 | D | D |  |  |
| asexual | B | 6 |  | F |  |  |
| asexuality | C | 15 | F | A | F17 |  |
| asktransgender | B | 4 |  | C |  |  |
| auburn | A | 4 | F |  |  |  |
| australia | B | 7 | E | E | F07 |  |
| austria | D | 16 | A | G |  |  |
| austriahungary | E | 1 |  |  |  |  |
| AvoArmy | E | 12 |  |  | F07 | F24 |
| AyyMD | F | 14 | E |  | F07 | F34 |
| azerbaijan | H | 3 |  |  | F19 | F17, F20 |
| azores | H | 1 |  |  |  |  |
| babymetal | A | 25 | F | F | F22 | F27 |
| bahrain | B | 1 |  |  | F01 |  |
| bakchodi | C | 5 |  | G | F08 |  |
| bangladesh | E | 8 | C, F |  |  |  |
| bangtan | F | 12 | C |  | F17 |  |
| bannedfromanime_irl | K | 0 |  |  |  |  |
| bardmains | A | 16 |  | B | F07 | F23, F34 |
| batman | A | 12 | F |  |  |  |
| battlecats | E | 9 | C |  | F02 | F01 |
| baylor | D | 5 | E | E | F33 |  |
| bdsm | H | 2 | E |  |  |  |
| bees | B | 1 |  | C |  |  |
| belgium | D | 13 |  | E | F24 |  |
| berkeley | E | 4 | C |  | F09 |  |
| berserk | C | 18 |  |  | F09 | F16, F32 |
| bigbang | B | 2 |  |  |  |  |
| bih | F | 7 |  |  |  |  |
| bindingofisaac | B | 23 |  |  | F01 | F02, F04, F11, F12, F23 |
| bisexual | B | 23 | A | A | F07 | F31 |
| bitcoin | A | 8 | E, G |  |  |  |
| blackmirror | E | 4 | H |  |  |  |
| bobross | D | 4 | B | E |  |  |
| borderlands | F | 6 | E |  | F27 | F34 |
| borussiadortmund | B | 19 |  |  | F21 | F35 |
| bostonbruins | A | 7 | B | B | F32 |  |
| bostonceltics | B | 8 | C | C | F04 | F01, F09, F17, F18 |
| brasil | E | 10 | F | F |  |  |
| Bravenewbies | H | 2 | F |  |  |  |
| Braveryjerk | B | 1 |  |  |  |  |
| bretagne | F | 6 | E |  |  |  |
| btc | C | 4 | A | A | F28 |  |
| buffalo | B | 10 | G | E | F12 | F11, F24 |
| buffalobills | D | 17 | A | A | F10 | F26 |
| buffalowizards | F | 5 |  |  | F09 |  |
| bulgaria | A | 16 | E |  |  |  |
| calgaryflames | C | 6 |  |  | F09 |  |
| calvinandhobbes | D | 7 | A, H | A | F07 |  |
| canada | D | 13 |  | F | F01 |  |
| canucks | C | 25 |  | D | F01 | F03, F04, F20, F24, F30 |
| cardinals | D | 11 | H |  |  |  |
| carletonu | D | 3 | A | A |  |  |
| catalonia | G | 8 |  |  | F08 |  |
| catalunya | A | 18 |  |  | F07 | F10, F28 |
| catholicism | B | 9 |  |  | F23 |  |
| cavestory | E | 7 | D, F | D | F10 | F16 |
| CelticFc | A | 1 |  |  | F28 |  |
| cfb | B | 7 | D |  | F02 | F01 |
| cgpgrey | C | 12 | B | B | F14 | F11, F23 |
| chelseafc | D | 20 | H |  | F04 | F01, F31 |
| chess | C | 9 | H | E | F33 |  |
| chibears | C | 7 | A, D |  | F09 | F20 |
| chicago | E | 19 |  | A | F07 | F21, F31 |
| chicubs | A | 14 |  | F |  |  |
| chile | F | 22 |  |  | F21 | F30 |
| ChronoTrigger | D | 6 | F | F | F12 | F11 |
| churchofhelix | K | 0 |  |  |  |  |
| cirkeltrek | D | 3 | A, F |  |  |  |
| CKCrusaders | F | 8 | B, E | B |  |  |
| Clannad | F | 2 | E |  |  |  |
| clashroyale | B | 11 | A |  | F35 |  |
| clg | D | 14 |  |  | F32 |  |
| cloud9 | B | 10 |  | A | F12 | F11, F28 |
| clubpenguin | C | 11 |  |  | F12 | F09, F11 |
| cmu | G | 10 | A, C |  |  |  |
| coldplay | A | 14 |  |  | F07 | F10, F33 |
| colombia | C | 4 | E | E | F22 |  |
| colorado | D | 3 | E, F | F | F15 |  |
| columbia | A | 11 | H | D | F15 |  |
| completeanarchy | G | 13 | B | B |  |  |
| compsoc | H | 2 |  |  |  |  |
| Cornwall | A | 1 |  |  |  |  |
| corridor | C | 15 |  |  | F25 |  |
| COSI | C | 1 |  |  |  |  |
| costa_rica | F | 8 |  | A |  |  |
| counting | A | 2 | D | D |  |  |
| cowchop | D | 13 |  |  | F24 | F27, F28 |
| criticalrole | A | 19 | D | D | F01 | F15 |
| croatia | A | 4 | E |  | F07 |  |
| crusaderkings | B | 11 |  |  | F08 |  |
| CryptoFR | A | 3 |  | H |  |  |
| crystalclear | F | 2 | E |  | F34 |  |
| CSUFoCo | E | 5 |  |  | F33 |  |
| cubers | E | 12 |  |  | F12 | F11 |
| cuboulder | H | 1 |  |  |  |  |
| czech | G | 14 | A | A | F07 | F08, F25 |
| daftpunk | A | 9 | H |  |  |  |
| dallasstars | G | 11 | B, C |  | F01 | F24 |
| danganronpa | B | 16 |  | G | F02 | F01, F24 |
| dankmemes | B | 10 |  |  | F01 | F02, F03, F04 |
| darksouls | F | 8 |  |  | F16 |  |
| DatBoi | B | 5 |  |  |  |  |
| davidbowie | F | 4 | B, D, E | B | F15 |  |
| day9 | C | 3 |  |  | F09 |  |
| dbz | C | 14 | A | A | F01 |  |
| DCFU | H | 6 | A | C | F22 |  |
| de | D | 23 | A | A | F16 | F30 |
| denmark | F | 8 |  |  | F11 |  |
| denverbroncos | C | 20 |  | B | F03 | F01, F17, F18 |
| destiny | C | 4 | H | B | F22 |  |
| DestinyTheGame | A | 17 |  | D | F02 | F01, F23 |
| detroitlions | D | 13 |  |  | F34 |  |
| detroitredwings | A | 12 |  |  |  |  |
| DevonUK | A | 2 |  |  |  |  |
| diablo | C | 9 | B | B |  |  |
| DiamondClub | H | 1 |  |  |  |  |
| dmt | B | 2 |  |  |  |  |
| dofus | E | 1 |  |  |  |  |
| Dominican | E | 10 | C | C |  |  |
| donaldglover | C | 12 | F |  | F11 |  |
| Dorset | A | 6 |  |  |  |  |
| dota2 | G | 15 |  |  | F05 | F01, F08, F28 |
| dragonquest | A | 8 | G |  | F33 |  |
| drawhelix | A | 7 | E, F | F | F10 |  |
| drugs | E | 3 | A, D | A |  |  |
| drumcorps | A | 7 | B | D | F01 | F03, F10 |
| duckgame | C | 7 | A |  |  |  |
| ducks | C | 5 |  | D |  |  |
| Dustforce | C | 4 | A |  | F09 | F10 |
| dwarffortress | F | 17 |  | E | F16 |  |
| eagles | C | 10 | F |  |  |  |
| earthbound | A | 12 | F | F | F10 | F26 |
| edboxes | B | 16 |  |  | F07 |  |
| eder | E | 2 | H | H | F20 |  |
| edmontonoilers | B | 12 | H | F |  |  |
| eesti | G | 8 | C, H |  | F08 |  |
| egypt | E | 4 |  |  | F22 |  |
| ElderScrolls | F | 6 | H |  | F01 | F32 |
| elitedangerous | E | 4 | B, F | F | F04 | F01 |
| ElSalvador | C | 5 |  |  |  |  |
| empiredidnothingwrong | D | 20 | F | F | F27 |  |
| england | G | 9 |  |  |  |  |
| enterthegungeon | B | 10 |  |  | F23 |  |
| epublica | F | 16 | A | C | F24 |  |
| EraseThePlace | D | 19 |  | C | F29 |  |
| esperanto | B | 11 |  |  | F12 | F11, F16 |
| ethereum | D | 16 |  |  | F01 |  |
| ethoslab | E | 5 | A | C | F01 |  |
| europe | D | 17 | F | F |  |  |
| eve | A | 12 | F | D | F07 | F16, F29 |
| evedreddit | A | 1 |  |  |  |  |
| evex | A | 13 |  |  | F08 | F10, F34 |
| factorio | D | 9 | G | G | F07 |  |
| faeria | A | 14 |  |  | F18 | F10, F17, F31 |
| falcons | B | 11 |  | G | F01 |  |
| farmcarrots | D | 12 | A, E | E | F07 | F34 |
| FaroeIslands | C | 10 |  |  | F09 |  |
| FederationPlace | A | 15 |  |  | F08 | F10 |
| feedthebeast | A | 10 |  |  | F14 | F01, F11, F24, F33 |
| Fez | B | 9 |  | F | F21 |  |
| FinalFantasy | C | 15 |  |  |  |  |
| finland | A | 6 | E |  |  |  |
| fireemblem | D | 10 |  | A |  |  |
| fivenightsatfreddys | B | 22 |  | A | F01 | F02, F07, F09, F10, F23, F29, F31 |
| FlaggyFlag | F | 7 | B, E | B | F07 | F35 |
| flashtv | B | 16 | C | C | F02 | F01, F07, F09 |
| FlipnoteStudio3D | B | 1 |  |  |  |  |
| floridagators | F | 5 |  |  |  |  |
| FloydVsVoid | C | 26 | A, F | A | F15 | F30, F31 |
| flyers | C | 14 | H | B | F18 | F17, F22 |
| formula1 | F | 6 |  | E | F02 | F01, F09 |
| forsen | B | 15 |  |  | F12 | F11, F16, F30 |
| foxes | D | 16 |  |  | F31 |  |
| foxstevenson | C | 3 |  |  |  |  |
| france | D | 6 | G | G |  |  |
| frankocean | A | 21 |  | B | F27 | F31 |
| frc | D | 10 | G | F | F24 | F25, F27 |
| freedomplanet | C | 6 |  |  | F19 | F09, F16, F17 |
| ftlgame | D | 7 | H |  | F18 | F15, F17 |
| fullcommunism | F | 6 | G, H |  | F17 |  |
| funhaus | A | 15 |  |  | F30 |  |
| furry | A | 16 | F |  | F26 |  |
| furry_irl | B | 10 |  | C | F05 | F01, F11, F12, F22 |
| futanari | H | 5 |  |  |  |  |
| futurama | B | 10 |  | F | F23 | F24, F27 |
| fxKorea | A | 9 | E |  | F18 | F07, F17 |
| GabrielDropout | A | 4 | D, E, G | G |  |  |
| gameattack | D | 11 |  |  | F21 |  |
| gameboy | D | 3 | C, H | C |  |  |
| gameofthrones | F | 10 |  |  | F02 | F01, F07, F17, F18, F28 |
| gamindustri | E | 20 |  | C | F12 | F11, F22 |
| gatech | A | 19 |  |  | F08 | F07, F11, F14, F23, F33 |
| genderfluid | F | 4 |  |  |  |  |
| geometrydash | B | 8 |  |  | F01 | F02 |
| germany | B | 5 |  | C |  |  |
| ghibli | D | 6 | H |  | F15 |  |
| giantbomb | D | 15 | G |  |  |  |
| giivasunner | B | 11 | C | C | F09 | F22 |
| glasgow | F | 6 | E |  |  |  |
| globaloffensive | E | 9 |  | G | F13 | F11 |
| Goodboye | A | 9 | F | F |  |  |
| gorillaz | E | 17 |  | B | F25 |  |
| GranColombia | A | 7 | F | F | F16 | F24, F30 |
| gratefuldead | C | 8 |  |  |  |  |
| gravityfalls | A | 9 | E |  | F12 | F11, F27 |
| greece | F | 11 | E |  | F27 |  |
| greenbaypackers | G | 11 |  |  |  |  |
| GreenCorner | F | 9 |  |  |  |  |
| GreenEmpire | K | 0 |  |  |  |  |
| greenland | K | 0 |  |  |  |  |
| greenlattice | A | 24 |  | C | F12 | F11 |
| greyblob | B | 9 | C | C | F12 | F09, F11, F23 |
| GrowTheTree | A | 4 | E, H |  |  |  |
| GuardiansOfDatBoi | D | 7 |  | B | F15 |  |
| guatemala | E | 6 |  |  |  |  |
| GuildWars2 | B | 9 |  |  | F01 | F35 |
| h3h3productions | C | 12 |  | B | F21 |  |
| habs | D | 15 | H |  | F32 |  |
| halo | C | 8 |  | F |  |  |
| harrypotter | E | 8 | A | A | F01 | F22, F26 |
| haskell | C | 3 |  | E |  |  |
| hatsune | C | 16 |  |  | F20 | F35 |
| hawks | B | 14 |  |  | F22 | F24, F27 |
| hearthstone | A | 13 |  |  | F10 |  |
| hellointernet | C | 12 | A | A | F27 | F33 |
| hentai | C | 10 | E | E | F07 | F22 |
| heroesofthestorm | F | 9 |  |  | F01 | F29 |
| heyyea | A | 7 | E, H | H | F11 |  |
| homelab | D | 12 | H | H |  |  |
| HomestarRunner | B | 15 |  |  |  |  |
| homestuck | B | 9 |  |  | F35 |  |
| Homura | E | 1 | F |  |  |  |
| Honduras | E | 5 |  | H |  |  |
| hongkong | A | 7 | E |  | F07 | F31 |
| hoodr | C | 3 |  |  |  |  |
| hsv | B | 13 | F | D |  |  |
| httyd | C | 8 |  |  | F32 |  |
| hungary | H | 4 | A |  | F23 | F28 |
| hunterxhunter | D | 8 | A | A | F03 | F01 |
| hyperlightdrifter | E | 12 | C, G | G | F07 | F08, F09, F15, F16, F24 |
| iastate | F | 10 | E |  |  |  |
| ibo | B | 4 | H |  |  |  |
| ice_poseidon | B | 11 |  |  | F21 |  |
| iceland | A | 1 |  |  |  |  |
| ik_ihe | E | 2 | D, F |  | F16 |  |
| india | G | 14 |  |  | F08 | F23, F33 |
| indieheads | E | 17 |  |  | F01 | F07, F09 |
| indonesia | A | 16 | E |  | F25 |  |
| ireland | A | 10 | E | E |  |  |
| israel | A | 7 | E |  | F07 | F10 |
| italy | G | 9 |  |  | F12 | F11 |
| Jamaica | D | 8 | A, E |  | F15 |  |
| japan | D | 11 |  |  | F15 | F32 |
| jerma985 | B | 16 |  | C | F09 | F29 |
| k_on | D | 8 | H | H |  |  |
| kamenrider | B | 11 | A | D | F15 | F21 |
| kanye | B | 14 |  |  | F06 | F01, F11 |
| katawashoujo | E | 6 |  |  | F07 |  |
| kcroyals | D | 10 | H | G | F18 | F08, F17 |
| kerbalspaceprogram | D | 10 | B | B | F01 | F02 |
| kilian | A | 5 | F | F | F16 |  |
| kindafunny | H | 6 | E | E | F34 |  |
| kingdomhearts | A | 9 |  | C | F09 |  |
| kirby | A | 7 | H | B | F18 | F01, F17, F25, F28 |
| konosuba | E | 5 |  |  | F33 |  |
| korea | A | 15 | E |  | F07 | F09, F10 |
| kpop | E | 7 |  |  | F01 |  |
| KState | G | 13 |  |  | F08 |  |
| kurdistan | A | 7 |  | C | F10 |  |
| kuwait | F | 10 |  |  | F33 |  |
| lakers | D | 13 | F |  | F16 | F27 |
| landry | A | 4 |  |  |  |  |
| latin | C | 9 |  | E |  |  |
| latvia | C | 8 | E | E |  |  |
| leafs | A | 7 | E |  |  |  |
| leagueoflegends | E | 7 | F |  |  |  |
| lebanon | C | 12 | A | B | F35 |  |
| lego | D | 12 |  | E | F13 | F11 |
| lexington | B | 2 |  |  |  |  |
| lifeisstrange | A | 10 |  |  | F26 |  |
| linux | D | 11 | G |  | F10 | F15, F16 |
| liquicity | D | 11 |  |  | F15 |  |
| lithuania | C | 8 | A, F | A | F16 |  |
| littlebusters | D | 1 |  |  |  |  |
| littlewitchacademia | D | 13 |  |  | F10 | F15, F30, F35 |
| livecounting | A | 4 | G | G | F08 |  |
| liverpoolfc | E | 6 | F | F | F29 |  |
| lofihiphop | D | 6 |  | E | F15 | F21, F30 |
| loliconsunite | F | 16 |  |  | F23 | F30 |
| loltyler1 | G | 10 |  |  | F08 |  |
| lost | C | 8 | E, F, H | F |  |  |
| lovelive | B | 9 |  | C | F13 | F11 |
| lsu | C | 13 |  |  | F09 | F28, F30 |
| luciomains | H | 9 | E |  | F19 | F07, F17, F32 |
| Lugarix | K | 0 |  |  |  |  |
| luxembourg | B | 11 |  |  | F32 |  |
| Madeon | E | 5 |  |  |  |  |
| madokamagica | E | 9 | F | A |  |  |
| magictcg | H | 16 |  | D | F01 | F03, F04 |
| malaysia | A | 11 | G |  | F09 | F28, F31 |
| malta | F | 5 | E | E |  |  |
| mamamoo | B | 1 |  |  | F35 |  |
| ManningPlace | A | 5 |  |  | F26 |  |
| Mario | H | 2 |  |  | F12 | F11 |
| mariokart | B | 4 |  |  | F03 | F01 |
| marvel | C | 7 | E |  | F34 |  |
| maryland | A | 8 | E |  | F22 | F26 |
| masseffect | E | 9 | D |  | F09 | F29 |
| math | C | 12 | A, F, H | F |  |  |
| mcgill | E | 1 | F |  | F16 |  |
| mcgillrobotics | K | 0 |  |  |  |  |
| mechanicalkeyboards | A | 14 |  |  | F26 |  |
| megaman | F | 15 | A, E | B | F07 |  |
| metalcore | C | 14 | F | F | F27 |  |
| metalgearsolid | A | 13 | E | E | F01 | F05, F07, F16 |
| metroid | A | 15 | C |  | F26 | F31 |
| mexico | F | 8 | G |  | F08 | F29 |
| miamidolphins | A | 6 |  |  | F26 |  |
| MiamiHurricanes | C | 6 | A | A |  |  |
| mindcrack | A | 14 | G |  | F24 | F28, F31 |
| minecraft | B | 15 |  |  | F01 | F03, F05 |
| minnesotavikings | G | 9 | A |  | F08 |  |
| miraculousladybug | B | 4 | C | C | F05 | F01, F11 |
| mit | A | 8 | E, F |  | F10 | F28, F33 |
| mizzou | F | 8 | E, H |  |  |  |
| mls | D | 17 | A |  | F06 | F01, F31 |
| MMA | D | 14 | H | H | F01 | F02 |
| monalisaclan | B | 17 | D | D | F15 | F16, F25, F26 |
| monero | D | 11 | F, G | G | F16 |  |
| MonkeyIsland | B | 10 | F | F | F15 |  |
| monstercat | G | 15 | B |  | F01 | F02, F04 |
| monsterhunter | D | 6 |  |  |  |  |
| montenegro | H | 3 | E, F | E | F16 |  |
| Moondye7 | D | 6 | A | A | F19 | F10, F15, F17 |
| mordhau | C | 3 | F |  |  |  |
| morrowind | A | 15 |  |  | F07 |  |
| msu | A | 7 | D | D | F09 | F10, F15 |
| muse | A | 6 | E | E | F07 |  |
| mylittlepony | C | 20 | G | B | F16 | F22, F25 |
| mysterydungeon | A | 9 | H | H |  |  |
| n64 | K | 0 |  |  |  |  |
| naruto | B | 11 |  | D | F02 | F01, F11, F12, F23 |
| nascar | A | 9 |  |  | F10 | F26 |
| natsume | F | 3 | E |  |  |  |
| nbaspurs | C | 21 | A | A | F01 | F04, F05, F09, F24, F31 |
| necrodancer | A | 8 | C, E, H | E | F09 | F28, F29, F33 |
| neopets | F | 16 |  | A | F29 |  |
| nerf | A | 10 | D | F | F15 |  |
| neu | G | 7 | A |  | F08 |  |
| neutralmilkhotel | A | 3 | H |  |  |  |
| NewMexico | A | 10 | E |  | F10 | F26, F33 |
| newzealand | B | 14 |  |  | F07 | F32 |
| NieR | E | 8 | B |  | F05 | F01 |
| nightinthewoods | H | 14 |  |  | F01 | F15 |
| nin | A | 20 | H | E | F18 | F17, F34 |
| nintendo | B | 16 |  |  | F01 |  |
| nlsscirclejerk | E | 11 | F | F | F34 |  |
| nonbinary | K | 0 |  |  |  |  |
| norge | B | 1 |  |  |  |  |
| Northwestern | C | 8 | D |  |  |  |
| norway | B | 13 |  | A |  |  |
| notredame | A | 9 |  |  | F07 | F10 |
| NovaScotia | K | 0 |  |  |  |  |
| npr | D | 9 | A |  |  |  |
| nuclearthrone | E | 10 |  | F | F33 |  |
| nVade | B | 14 | A, F | F |  |  |
| nyjets | B | 13 |  | D | F02 | F01, F09, F15 |
| nyu | B | 6 | H | C |  |  |
| ockytop | A | 9 | D | D | F15 | F23, F32 |
| ohio | F | 10 |  | A | F10 |  |
| Okami | H | 8 | D |  | F19 | F15, F17 |
| OKState | G | 7 |  |  | F08 | F24 |
| oltp | F | 1 |  |  |  |  |
| oman | B | 2 |  |  |  |  |
| OnePiece | C | 17 |  | F | F22 | F07, F27, F32 |
| oneplus | B | 6 | H | H | F01 |  |
| onepunchman | A | 4 | F |  | F10 |  |
| oneshot | D | 5 | A |  |  |  |
| OneTrueEmilia | B | 8 | F | F | F21 | F22, F27 |
| ontario | B | 5 |  | E | F01 | F02, F03, F05 |
| opticgaming | A | 16 |  |  | F19 | F17 |
| orderofthebluecorner | C | 6 | F | F |  |  |
| OrderOfTheKoi | E | 7 | C, F, H | C | F16 | F30 |
| osu | B | 14 |  |  | F07 | F21 |
| osugame | B | 20 |  | A | F29 |  |
| overwatch | B | 23 |  |  |  |  |
| pakistan | G | 12 | A |  | F08 | F28 |
| paladins | B | 25 |  |  | F01 | F06, F25, F30 |
| palestine | E | 5 |  |  | F34 |  |
| pansexual | C | 3 | A | A |  |  |
| parabola | D | 3 | A, F |  |  |  |
| paragon | B | 11 |  |  | F01 | F02, F33 |
| parahumans | A | 15 |  | B | F25 | F27 |
| paranatural | C | 10 |  |  |  |  |
| parrots | E | 10 | F | F | F13 | F11 |
| partyparrot | A | 15 |  |  |  |  |
| pathofexile | A | 12 |  |  |  |  |
| patriots | B | 10 |  | D | F21 |  |
| paydaytheheist | D | 4 | A, H |  | F32 |  |
| pcmasterrace | B | 17 | F |  | F25 | F01, F05, F16, F21, F27, F30 |
| pebble | C | 13 |  |  | F09 |  |
| penguins | C | 14 |  | B | F09 | F34 |
| pepe | G | 8 | B |  | F08 |  |
| Peru | A | 12 | H |  | F30 |  |
| peterdraws | C | 3 | A, H | A |  |  |
| pgang | K | 0 |  |  |  |  |
| philippines | D | 12 |  |  | F15 |  |
| phish | G | 11 |  |  | F01 | F08, F10, F23 |
| physical_removal | F | 3 |  | B | F23 |  |
| picturegame | B | 4 |  | H | F25 | F21 |
| Pigifs | H | 4 |  |  |  |  |
| PinkUnion | C | 9 |  |  |  |  |
| PinkVomitMonster | E | 5 | A | A |  |  |
| pitt | A | 9 |  |  | F14 | F07, F11 |
| placecanada | D | 13 | G |  |  |  |
| placeDE | E | 9 |  |  | F23 |  |
| placehearts | F | 6 |  |  |  |  |
| placehfarts | B | 1 |  | C |  |  |
| PlaceNL | G | 22 |  |  | F08 | F22, F25 |
| placeportalpattern | A | 9 |  |  | F23 | F24, F26 |
| placesnek | A | 13 | E | E |  |  |
| placestart | E | 12 | D | D | F15 | F29 |
| placetardis | A | 12 | B |  | F10 | F15, F26 |
| planetside | G | 20 | C, F | C | F03 | F01, F29, F30 |
| pokemon | F | 8 |  |  | F27 |  |
| PokemonSage | K | 0 |  |  |  |  |
| poland | A | 10 |  |  | F10 | F16, F24, F26 |
| polandball | E | 7 |  |  | F02 | F01 |
| polska | E | 10 | F |  | F12 | F07, F11 |
| polyamory | B | 5 |  |  | F35 |  |
| popheads | D | 10 | H |  | F01 | F05 |
| portal | C | 15 | E, H | E | F33 |  |
| porterrobinson | A | 17 |  | E | F07 | F24, F30 |
| portugal | F | 17 |  | A | F13 | F11, F29 |
| PORTUGALCARALHO | E | 3 | H |  | F34 |  |
| predators | G | 13 |  |  | F08 | F22 |
| prequelmemes | A | 25 |  |  | F13 | F11, F23, F24, F25, F30, F31 |
| Produce101 | C | 2 |  |  |  |  |
| ProfessorLayton | E | 8 | B |  |  |  |
| PUBATTLEGROUNDS | A | 14 | E |  | F03 | F01, F07 |
| purdue | B | 16 |  | C | F08 | F35 |
| purplecorner | C | 16 |  | E | F23 |  |
| PurplePixels | F | 13 |  | A | F16 |  |
| pusheen | E | 5 | C | C | F07 | F09 |
| puzzleanddragons | F | 12 |  |  | F07 |  |
| python | G | 12 | A |  | F08 | F26 |
| qotsa | C | 8 | D | E |  |  |
| quebec | F | 22 |  |  | F28 | F29 |
| quq | K | 0 |  |  |  |  |
| radiohead | C | 17 | F | F | F27 |  |
| Rainbow6 | A | 12 |  | D | F01 | F07, F20 |
| rainbowgrid | D | 10 | A | C |  |  |
| rangers | G | 14 |  |  | F29 | F33 |
| raocow | B | 9 |  |  | F35 |  |
| ravens | B | 16 | D | D | F15 | F26 |
| re_zero | A | 12 | E, H |  | F20 | F28, F29 |
| ReBoot | C | 2 |  |  |  |  |
| reddevils | B | 22 |  | F | F03 | F01, F29, F30 |
| redhotchilipeppers | F | 5 |  |  | F16 |  |
| Redox | K | 0 |  |  |  |  |
| redpandas | F | 11 | E |  | F22 |  |
| redvsblue | D | 3 | A | A |  |  |
| RelientK | C | 11 | A |  | F22 |  |
| rhythmheaven | A | 9 |  |  | F21 | F34 |
| rickandmorty | D | 12 |  |  | F32 |  |
| ripcity | A | 8 | H |  | F18 | F17, F28, F32 |
| riskofrain | A | 5 | H |  | F10 |  |
| rit | A | 10 |  |  |  |  |
| rocketbeans | D | 14 |  | F | F19 | F17 |
| rocketleague | D | 10 | A |  |  |  |
| rojava | F | 5 | E |  |  |  |
| romania | F | 15 | B |  | F01 | F11, F13, F21 |
| roosterteeth | D | 5 |  |  |  |  |
| rotmg | B | 20 |  | C | F23 |  |
| rpi | A | 11 | C | G | F08 |  |
| runescape | G | 11 | B |  | F01 | F06, F08 |
| rush | E | 8 | C |  | F02 | F01, F09, F22 |
| russia | E | 7 | C | C | F22 |  |
| Russiaclan | C | 13 |  | A |  |  |
| rust | G | 20 |  |  | F08 | F01, F06 |
| rutgers | B | 15 |  | D | F09 | F21, F22, F24 |
| rwby | C | 14 | A | A | F01 | F02, F09 |
| sabres | B | 8 |  |  | F12 | F11 |
| sadboys | B | 11 |  |  | F12 | F11, F31 |
| sakartvelo | K | 0 |  |  |  |  |
| sakuragakuin | E | 6 |  | F |  |  |
| samuraijack | D | 21 | F | F | F01 | F29 |
| satania | E | 10 |  | A | F07 |  |
| sbu | G | 7 |  |  | F08 |  |
| schoolidolfestival | A | 11 |  |  | F01 | F02, F05, F23 |
| scotland | A | 9 | E | E | F24 |  |
| ScottPilgrim | A | 5 |  |  |  |  |
| scp | F | 14 |  |  | F21 | F30 |
| seahawks | B | 16 | E | A | F01 | F07, F25, F31, F35 |
| seolhyun | C | 3 | A | A | F09 | F10 |
| serbia | G | 9 |  |  | F08 |  |
| seventeen | B | 2 |  | C |  |  |
| sheffield | A | 14 | C, E, H | E | F07 |  |
| shield | A | 10 |  |  | F07 |  |
| shishamo | C | 1 |  |  | F22 |  |
| shitredditsays | B | 11 | F | F | F24 |  |
| shrooms | F | 1 |  |  |  |  |
| signal | K | 0 |  |  |  |  |
| simonfraser | E | 5 | F |  | F22 | F30 |
| singapore | C | 13 | H |  |  |  |
| sips | G | 21 | C | B | F20 | F21, F24 |
| sixers | F | 13 |  |  | F27 |  |
| skyrim | A | 7 |  |  | F10 |  |
| Slovakia | C | 8 | A |  |  |  |
| slovenia | D | 6 |  | G | F08 |  |
| smashbros | E | 7 | F |  | F02 | F01 |
| smite | F | 2 |  | C | F22 |  |
| snsd | E | 11 | C, D | D |  |  |
| sonicthehedgehog | B | 6 |  | C |  |  |
| sooners | A | 10 |  | G | F08 |  |
| southafrica | A | 7 | E |  | F21 |  |
| southpark | B | 11 | F |  | F21 |  |
| soylent | C | 7 | F |  | F26 |  |
| spacex | H | 4 | B |  | F06 | F01, F17 |
| spacexmasterrace | E | 11 |  |  | F07 | F08 |
| spain | C | 17 |  | E | F16 |  |
| spelunky | B | 4 | H | H | F01 |  |
| splatoon | A | 15 |  |  | F17 |  |
| spongebob | C | 11 |  | D | F15 | F16, F30 |
| SquareSpiral | C | 11 |  |  | F09 | F23 |
| ss13 | A | 15 | D |  | F15 |  |
| ssbpm | G | 12 | F | E | F16 |  |
| starbound | A | 10 |  |  | F35 |  |
| starcitizen | D | 21 |  | G | F08 | F25 |
| starcraft | B | 15 |  | A | F01 | F06 |
| stardewvalley | C | 11 |  | D | F09 | F15, F21, F28, F32 |
| stardustcrusaders | E | 14 | D |  | F01 | F30 |
| stargate | E | 12 | B, C | B | F01 | F04, F09, F11, F12, F25, F35 |
| starlightstage | A | 14 | E |  | F10 | F21, F33, F34 |
| starryknights | D | 12 | F |  | F15 | F16 |
| startrek | K | 0 |  |  |  |  |
| starvstheforcesofevil | C | 6 | A | A | F23 | F32 |
| stevenuniverse | A | 19 | F | E | F01 | F16, F25, F26, F29 |
| stlouis | B | 12 | F | F | F20 |  |
| stlouisblues | D | 13 |  | A |  |  |
| strangerthings | A | 3 | E |  | F34 |  |
| straya | D | 7 |  |  |  |  |
| streetfighter | E | 9 | C | C | F03 | F01, F21 |
| Summit1G | A | 4 |  |  |  |  |
| suomi | A | 20 |  | F |  |  |
| superman | H | 2 | E |  | F33 |  |
| survivor | D | 11 | B |  | F02 | F01, F15 |
| sweden | E | 4 | F |  |  |  |
| SwissNeutralityZone | A | 7 | H | H | F19 | F15, F17, F28, F29 |
| switzerland | A | 11 |  |  | F10 |  |
| swordartonline | D | 12 |  |  | F18 | F01, F17 |
| SydneyFC | H | 2 | E |  |  |  |
| tagpro | A | 10 | F | F | F29 |  |
| taiwan | A | 7 | G, H |  | F18 | F17 |
| tampabaylightning | E | 6 |  |  | F07 |  |
| teamcube | E | 10 |  |  |  |  |
| TeamDignitas | B | 8 |  |  |  |  |
| TeamYellowPlace | A | 3 |  |  |  |  |
| telegram | A | 7 | F | F |  |  |
| Temple | B | 17 |  | G | F08 | F09, F25 |
| tenma | B | 1 |  |  | F35 |  |
| terraria | A | 12 |  |  | F01 | F02, F03, F25, F31 |
| teslamotors | A | 7 | E |  | F08 |  |
| tetris | E | 3 | H |  |  |  |
| texans | G | 15 |  | B | F02 | F01, F11, F14 |
| texas | A | 10 |  | G | F08 |  |
| texastech | A | 6 |  | G |  |  |
| tf2 | A | 5 | E | E | F33 |  |
| thailand | A | 14 |  |  | F26 |  |
| the_pack | B | 10 |  |  |  |  |
| THE_R | F | 1 |  |  | F27 |  |
| TheAdventuresofTintin | E | 3 |  |  |  |  |
| TheB1G | C | 4 | A |  |  |  |
| theblackvoid | F | 12 |  |  | F12 | F11 |
| thebluecorner | C | 20 |  | B | F23 | F25, F29 |
| theexpanse | A | 24 |  |  | F16 | F23 |
| TheFarLeftSide | D | 13 |  | B | F23 |  |
| Thegreatblackhole | D | 6 | H | B |  |  |
| TheGreatGreenBox | C | 4 |  |  |  |  |
| TheHulk | B | 13 |  | A | F07 | F32, F35 |
| TheID | K | 0 |  |  |  |  |
| theitalyplace | F | 9 |  |  |  |  |
| thenetherlands | B | 8 | H |  | F02 | F01 |
| thepointing | F | 10 |  | C | F09 |  |
| thesilphroad | D | 4 |  | E |  |  |
| thesimpsons | E | 7 | F | F | F01 |  |
| thetreesnetwork | F | 4 | E |  |  |  |
| timbers | A | 13 |  |  | F07 | F21 |
| tinytardis | B | 8 | F |  | F15 | F22, F25 |
| titanfall | A | 10 |  | C | F01 | F21 |
| tokyo | H | 3 |  |  | F20 |  |
| toolband | A | 10 | F | C | F09 | F27 |
| torontoraptors | E | 14 |  | C | F07 | F31, F33 |
| totallynotrobots | B | 17 |  | A | F01 | F02, F25 |
| touhou | A | 14 |  |  | F13 | F11, F23, F28 |
| traaaaaaannnnnnnnnns | A | 15 | B | B |  |  |
| TransFlagPlace | E | 5 | F | F | F16 |  |
| transformers | A | 13 | B | B | F10 | F21, F26 |
| transgender | B | 3 |  |  |  |  |
| TreePlace | C | 4 | H |  |  |  |
| trees | E | 6 |  |  |  |  |
| truestl | A | 5 |  |  |  |  |
| TsundereSharks | F | 10 |  |  | F07 |  |
| turkey | C | 17 |  | F | F09 | F27 |
| twentyonepilots | C | 16 |  |  | F25 |  |
| twice | C | 6 | A, F | A | F09 |  |
| twitch | C | 8 |  |  | F07 | F21 |
| twitchplayspokemon | D | 17 | B | F | F01 | F09, F27 |
| ubc | A | 3 | E |  | F22 |  |
| ubreddit | B | 10 | C | C | F09 |  |
| ucf | B | 11 |  |  | F15 |  |
| udub | D | 5 |  | E | F15 |  |
| ufl | C | 4 | B | B |  |  |
| uiowa | G | 11 | C |  |  |  |
| uiuc | C | 13 |  |  | F09 | F26 |
| ukplace | G | 7 |  |  | F08 |  |
| ukraine | G | 3 |  |  | F08 |  |
| ultrahardcore | B | 8 | H | H | F01 | F04 |
| UMiami | K | 0 |  |  |  |  |
| undertale | F | 9 |  | E | F32 |  |
| unitedkingdom | G | 7 | E |  | F07 |  |
| UNLincoln | K | 0 |  |  |  |  |
| unturned | A | 16 |  |  | F21 | F24, F32 |
| uofm | F | 12 |  | D | F08 | F15 |
| uofmn | D | 9 | A | A | F10 | F15 |
| uoft | C | 13 |  | G | F24 | F31 |
| UPenn | C | 7 |  |  | F09 |  |
| uruguay | C | 7 | E | E |  |  |
| utahjazz | D | 12 |  | C | F14 | F09, F11 |
| utaustin | A | 20 |  | G | F28 | F17, F18, F21 |
| uva | F | 9 | A | A |  |  |
| uvic | E | 8 |  |  | F07 |  |
| uwaterloo | B | 17 |  | A | F02 | F01 |
| vegan | B | 8 |  |  |  |  |
| VelvetUnderground | C | 2 | A, F | F |  |  |
| vermont | A | 8 | F |  |  |  |
| vietnam | E | 2 |  |  |  |  |
| Villanova | F | 5 | D |  |  |  |
| vim | B | 4 | H | H | F32 |  |
| vinesauce | C | 11 | A | A | F09 | F31 |
| virginiatech | G | 13 |  |  | F08 |  |
| vocaloid | A | 8 | F, H | H | F17 | F19 |
| wales | F | 8 |  |  |  |  |
| wallstreetbets | G | 13 | H |  | F08 |  |
| warframe | A | 21 |  |  | F01 | F02, F03, F21, F25 |
| wario | K | 0 |  |  |  |  |
| warriors | B | 9 | F | F | F13 | F11 |
| warthunder | C | 12 |  |  | F09 |  |
| watchmen | E | 1 |  |  |  |  |
| weezer | A | 15 |  |  | F18 | F17 |
| wholesomememes | B | 24 | F | F | F01 | F27 |
| wildhockey | G | 16 | C |  | F01 | F08, F09 |
| wine | E | 8 | H | C | F19 | F17, F22, F33 |
| winnipegjets | A | 8 | B | B |  |  |
| WisconsinBadgers | D | 4 |  |  | F15 |  |
| witcher | D | 13 | A | A | F27 | F31 |
| worldoftanks | D | 14 | H | A | F02 | F01 |
| worldpowers | B | 7 |  |  |  |  |
| wow | B | 11 |  |  | F01 | F35 |
| WPI | D | 3 | A, F, G | G | F08 | F10 |
| wsu | H | 3 |  |  |  |  |
| xcom | F | 14 |  | A | F30 |  |
| xenoblade_chronicles | D | 14 | A | A |  |  |
| yerbamate | K | 0 |  |  |  |  |
| yogscast | E | 9 |  | F | F19 | F01, F17, F22 |
| yugioh | C | 17 |  | E | F03 | F01, F34 |
| yumenikki | C | 6 |  |  |  |  |
| yuyuyu | C | 7 | H | H |  |  |
| zelda | B | 15 |  |  | F01 | F02, F03 |
| zootopia | A | 15 | G |  | F08 | F17 |

