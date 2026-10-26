# Room forms, D4a-06: the top cut redone

Leg D4a-06, 26 October 2026, an addition after the 35 branches, as at D4a-05. J read my interview answers to his four questions after D4a-05 and said (19:50 Berlin, through the handler): "Go ahead this sounds good." This leg redoes the top cut with the fixes I proposed. The interview ran in a fork and is not in this folder, so the fixes are taken from the handler's list. The amendment is dated in `departures.jsonl` (line 13).

Nothing earlier is replaced. `branches.jsonl`, `crosslinks.jsonl`, `tree-D4.md`, the forms, `room-forms-D4a05.*` and every D5 file are unchanged; I checked 81 files against the D4a-05 close snap (`_analysis/d4a06_unchanged.py`). The leg stops at the top cut. The split below the forms waits for J's talk.

Files: `room-forms-D4a06.jsonl` (one line per form and the core, with members), `room-forms-D4a06.tsv` (one row per room), and this file. The computation is `_analysis/d4a06_room_forms.py`; its rule was logged before it ran.

## 1. What changed from D4a-05

The comparison is the same. A room's selected changes are its accepted restrict, add-step, add-condition, link and contradict lines, on elements and arrows. Each counts at its third-order theme, fourth-order theme and dimension; shares within each level; the levels count equally; Hellinger distance; Ward's method. Three things changed.

- **A floor on thin rooms.** A room helps define the forms only if it holds 5 or more selected changes. Below that its mix is too coarse: rooms with 4 or fewer changes reach a median of 2 fourth-order themes or fewer, rooms with 5 a median of 3. 558 rooms define the forms. The 126 thin rooms are placed afterwards. The 21 rooms with no selected change stay together as the core. At D4a-05 the smallest form (28 rooms, median 3 changes) was built from thin rooms; the floor removes that effect.
- **J's placement rule, taken literally.** Once the forms are defined, each room goes to the form whose signature holds most of its selected changes, by count. A form's signature is the fourth-order themes its defining members change at 1.5 times or more the defining population's share, in a third or more of them. A tie goes to the tied form whose centre the room's whole mix is nearest, and the tie is listed. A room with none of its changes on any signature is placed by its whole mix. Secondary forms are the other forms whose signatures hold 25 per cent or more of the room's changes. No room is placed twice.
- **The count from 4 to 8, by measures that do not favour more groups.** (a) The gap between Ward merge heights: how long the k-group cut lasts as the joining goes on, from the height where it begins to the height where it ends. (b) Stability on matched subsamples: 100 pairs of subsamples, each 80 per cent of the defining rooms drawn without replacement, cut by Ward, compared by the adjusted Rand index on the rooms both hold; the same on 20 copies of the data with each column shuffled across rooms; the margin is the real mean less the shuffled mean. The rule, logged before the run: carry the k with the largest stability margin; report the gap's k beside it; if they disagree, give both cuts in full.

## 2. The count: the two measures disagree

{{TABLE:count}}

**The gap carries k = 5.** The five-group cut lasts 0.323, more than twice any other count in the range (k = 7, 0.144). It is the one clear feature between 4 and 8.

**Stability carries k = 8.** The margin over the shuffled null rises from 0.059 at k = 4 to 0.088 at k = 8. The shuffled null's own stability rises with k as well, so the margin corrects for part of what more groups give. But every real stability is low (0.150 to 0.206), and at k = 4 the real mean lies below the shuffled null's 95th percentile.

**Why they disagree.** At k = 5 the largest Ward group holds 164 rooms and has no signature: no fourth-order theme its members change at 1.5 times the population's share in a third of them. It is three of the eight forms merged (B, G and H at k = 8). So the clearest gap separates a middle group with no shared lean from four groups that lean one way each. J ruled out a broad form whose rooms share no pattern beyond breadth, and that group is one. By the logged rule I carry k = 8, the stability cut, and give the k = 5 cut in full in section 5.

## 3. The eight forms, placed by J's rule

By Ward on the defining rooms the forms hold 151, 81, 78, 62, 57, 46, 43 and 40 rooms (ratio 3.78). After placement they hold 135, 84, 89, 50, 62, 64, 124 and 76 (ratio 2.70, within J's bound of 3).

{{TABLE:forms}}

**How many rooms move against the whole mix: 239 of 684** (229 defining rooms whose Ward form differs from their signature placement, and 10 thin rooms whose nearest centre differs). 181 placements are ties between two or more forms. 11 rooms have no change on any signature and are placed by their whole mix.

**Why G grows from 43 to 124.** The rule counts changes, and G's signature theme, the mark's design (collective representation), is one that 327 rooms change. A room with a few design changes among many others is drawn to G whatever the rest of its mix. 67 of G's 124 rooms have their whole mix in another form. The count rule favours forms whose signature themes are common.

## 4. The members, read as rooms

I read each form's best fits, the misfits the rule takes away, and the members with the smallest share on the signature, through their lines' how sentences (`_analysis/d4a06_read.py`). Best fits are taken among defining rooms, since a thin room reaches a full share with one or two changes.

{{TABLE:read}}

- **A, the terms between neighbours reworked: one kind.** The best fits change how rooms settle space with neighbours. In r/mechanicalkeyboards a call is followed by a contested overlap; in r/duckgame a threatened picture becomes a shared design as a peace term; in r/notredame a negotiation answers a collision expected during building. The misfits the rule moves out are rich rooms (24 and 25 changes) whose changes spread over many forms: r/babymetal goes to C, r/paladins to B, r/anime to H. They belong to several forms, and one placement per room hides that.
- **B, help traded, restraint and carrying on reworked: a mixture.** Three signatures, each held by fewer than half of the defining members. r/ElSalvador, r/httyd and r/germany change how help is traded and whether a protection bargain is delivered; r/AcePlace carries its work to another canvas. The lowest shares (r/romania, r/homestuck, r/purdue) are rooms tied across several forms.
- **C, keeping reworked: one kind.** The best fits change keeping under strain: in r/pokemon doubt and loss do not lead to a move; in r/wales members' sleep prompts proposed shifts and a chat for repair; in r/darksouls a negotiated incorporation preserves the art and a broken chat invitation is repaired. The large misfits (r/greenlattice, r/catalunya, r/portugal) go to B and A.
- **D, the plan and its venue reworked: one kind, with two means.** The template and the chat that carries it. In r/lofihiphop a corrective rebuild points to updates of the plan elsewhere; in r/straya the plan needs current versions and accurate geometry; in r/starryknights the chat's access and its sanctions are kept. The large misfits (r/prequelmemes, r/theexpanse, r/de) go to C and A.
- **E, the spot reworked: one kind.** In r/warthunder a proposed move returns to building, and permission is timed for when the host's members are awake; in r/pebble a missed relocation message and a request for space; r/twitch reports where an image stands. r/day9, the room that best supports the account, is placed here: all 3 of its changes are on the spot theme. The large misfits (r/FloydVsVoid, r/nbaspurs, r/indieheads) go to C, A and G.
- **F, machine hands reworked: mostly one kind.** Scripts are among the changes of 98 per cent of the defining members. In r/aeon runners are recruited for a tool made elsewhere; in r/rust a later target proposal threatens work marked for preservation. A minority's share comes from records of the end or from attack calls. Rooms where scripts are a smaller part (r/sips, r/rutgers, r/texans) go to E and B.
- **G, the mark's design and its marking reworked: one kind as cut, a mixture as placed.** The Ward members change how the design is settled and the start made public: in r/guatemala publicity is requested after the first placement; in r/kindafunny competing placements bring an invitation into the thread; in r/CSUFoCo helpers find a broken reference. As placed, G holds 124 rooms, 67 of them drawn from other forms by their design changes (section 3).
- **H, attack calls and mobilization reworked: a mixture, with a raiding core.** The best fits are raiding rooms: in r/completeanarchy members troll rivals with deceptive scripts; in r/HomestarRunner attack calls meet bare and reasoned refusals; in r/DatBoi peace offers come before later attack calls on the same neighbour. Thin rooms placed here change calls to place (r/transgender) or record how the work ended (r/tokyo, r/wsu). The large misfits (r/canucks, r/spain, r/anaheimducks) go to F, D and B.

## 5. The other cut: k = 5, the gap's choice

{{TABLE:alt}}

The five groups nest in the eight: k = 5's A is k = 8's B, G and H; its B is A; its C is C and D; its D is E; its E is F. Group A has no signature, so under J's rule its rooms go wherever their changes lie on the other signatures, and it keeps 66 rooms, those with no signature change (median 4 changes). After placement the sizes are 66, 185, 216, 84 and 133 (ratio 3.27), and 263 rooms move against the whole mix.

## 6. The raiding and takeover rooms, and the rich rooms the model fit without change

{{TABLE:sets}}

- **Raiding rooms** (102, those with at least one selected change on attack calls). For most, raiding is a small part of their changes (median 15 per cent), so they spread across the forms by the rest. Where raiding is a large part, the room sits in H: of the 27 rooms with a quarter or more of their changes on attack calls, 19 are in H and 6 in F.
- **Takeover rooms** (the 33 members of F02, the takeover run as a temporary regime). Their changes on the April Fools frame are a median 14 per cent of their selected changes, and no form's signature holds the frame. They spread over all eight forms, most in A, B and H (8, 7 and 7). The forms sort them by their canvas changes; the takeover is one part of their record, beside the canvas work.
- **Rich rooms the model fit without change.** The core holds r/startrek, with 137 coded concepts (the population median is 101) and 28 accepted lines, every one of which instantiates the model. The other 20 core rooms hold 1 to 22 coded concepts. Kept together as the instruction says, the core joins two kinds of room: one the model describes without change, and rooms with too little record to need a change.

{{TABLE:core}}

## 7. Kinds or a continuum, and the codes

**Still a continuum.** The stability of the eight forms is low and only a little above the shuffled null. 181 rooms tie between forms, 239 move against their whole mix, 319 have a secondary form, and 288 lie within 5 per cent of another form's centre. The floor and the placement rule change the forms a good deal: the adjusted Rand index against D4a-05's forms is 0.196.

**Against the codes**, which the tree does not use: the forms differ, weakly. A permutation test of the form labels on the rooms' code shares gives a pseudo-F of 8.25, against a null 95th percentile of 1.24 (p = 0.001); the forms explain 7.9 per cent of the variation. The codes come from the same coding scheme as the changes, so the check is not independent. The forms differ in room size: the median room has 68.5 coded concepts in E and 179 in F.

## 8. For the talk with J

- Five forms or eight: the gap and the stability disagree, and the five-form cut's largest group shares no pattern.
- The count rule draws rooms to forms whose signature themes are common (G). Counting a room's changes against each theme's commonness, or giving each theme to one form only, would curb that.
- The rooms the rule moves out are rich rooms whose changes spread over several forms. Should a room carry weights in several forms rather than one placement?
- Should r/startrek, a rich room the model fit without change, be read apart from the thin rooms of the core?

## 9. The room table

One row per room, in case-ignored order (also in `room-forms-D4a06.tsv`). *Placed by* says whether the signature decided, a tie was broken by the nearest centre, or the whole mix decided. The whole-mix form is the Ward form for a defining room and the nearest centre for a thin one. The branches are the 35 of D4, primary first.

{{TABLE:rooms}}
