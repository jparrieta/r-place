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

{{TABLE:k}}

The silhouette and the stability both rise steadily from 4 to 8, so no count in the range stands out. Every k has a stability below 0.5, so the rule takes the most stable k, which is also the one with the highest silhouette: k = 8. The best count lies at the edge of the range J set, and a higher k might score higher still; I did not look past 8.

**What the lower counts would join.** Ward's cuts nest, so each lower k joins forms of the eight (recomputed from the ledger, `_analysis/d4a05_top.py --what nesting`). At k = 7, E (design) joins G (scripts). At k = 6, H (the close) joins B (calls and the frame). At k = 5, D (templates and reports) joins E and G. At k = 4, C (space and exchange) joins B and H. Each join puts together two patterns that differ in what the rooms change.

**The sizes.** At k = 8 the largest form holds 152 rooms and the smallest 28, a ratio of 5.43, above J's bound of 3. The cause is H. Its 28 rooms make few changes (median 3), and 69 per cent of those changes are on the close (marking, recording and carrying on the work), against 15 per cent in the population. The ratio stays 5.43 at k = 7 and falls to 2.2 at k = 6, but only because H folds into B there, and B's rooms change calls and the April Fools frame. I keep H apart because its pattern differs from B's, and I report the cost. G, the next smallest (42), is the form whose signature its members share most widely: scripts are among the changes of 95 per cent of its rooms (A's border theme comes next, at 93). If J prefers forms of comparable size to the narrow patterns, k = 6 is the cut (sizes 152, 147, 125, 103, 88, 69).

## 3. The eight forms

The signature of a form is the fourth-order theme its members change far more often than the population does: at least 1.5 times the population's share, in at least a third of its members. Every form has one, so none of them is a broad form, set apart only by many or evenly spread changes. A room *fits two forms equally* when the centre of another form is within 5 per cent of its distance to its own. A room is *nearer another form* when another form's centre is closer than its own; Ward's method allows this. A *secondary form* is another form whose signature themes hold 25 per cent or more of the room's selected changes. The clusterwise Jaccard is Hennig's (2007) measure of how well a form survives resampling: 0.75 or more is stable, below 0.5 the form dissolves.

{{TABLE:forms}}

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

{{TABLE:branches}}

## 7. For the talk with J

The split below the forms was computed before J's message of 18:36 arrived, and declared as moves 246 to 277. Move 278 withdrew those declarations; the computation is held in `_analysis/d4a05_tree3.json` as working material. One thing from it bears on the talk. Below the forms, the permutation null passed every split it tested, so I added a resampling test (logged before its run): a half is kept only if its clusterwise Jaccard is 0.6 or more. With it, splits hold in C, D, E and H, and none in A, B, F and G.

Questions I would bring:
- Is eight the count, or six, which keeps the sizes within J's bound at the cost of H and G?
- Should the three levels count equally? The third-order level has 147 columns and the dimension 8, so a common dimension can pull together rooms whose finer changes differ.
- Since the forms are cuts through a continuum, should a room carry weights in several forms rather than one membership?
- How should D6 relate branches that cut across the forms?

## 8. The room table

One row per room, in case-ignored order (also in `room-forms-D4a05.tsv`). *Secondary forms* hold 25 per cent or more of the room's changes on their signature themes. *Fits two equally with* names the other form whose centre lies within 5 per cent of the room's own. The branches are the 35 of D4, primary first.

{{TABLE:rooms}}
