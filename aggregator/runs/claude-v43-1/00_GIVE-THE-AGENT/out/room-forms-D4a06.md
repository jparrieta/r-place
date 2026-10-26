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

| k | Ward merge height: the cut begins | ends | lifetime (the gap) | stability: matched subsamples | shuffled null mean | null 95th percentile | margin |
|---|---|---|---|---|---|---|---|
| 4 | 2.8107 | 2.8644 | 0.0537 | 0.1495 | 0.0911 | 0.1627 | 0.0585 |
| 5 | 2.4875 | 2.8107 | 0.3233 | 0.1673 | 0.1000 | 0.1656 | 0.0673 |
| 6 | 2.3878 | 2.4875 | 0.0996 | 0.1784 | 0.1066 | 0.1665 | 0.0718 |
| 7 | 2.2444 | 2.3878 | 0.1435 | 0.1939 | 0.1115 | 0.1669 | 0.0823 |
| 8 | 2.2142 | 2.2444 | 0.0302 | 0.2055 | 0.1177 | 0.1735 | 0.0878 |

**The gap carries k = 5.** The five-group cut lasts 0.323, more than twice any other count in the range (k = 7, 0.144). It is the one clear feature between 4 and 8.

**Stability carries k = 8.** The margin over the shuffled null rises from 0.059 at k = 4 to 0.088 at k = 8. The shuffled null's own stability rises with k as well, so the margin corrects for part of what more groups give. But every real stability is low (0.150 to 0.206), and at k = 4 the real mean lies below the shuffled null's 95th percentile.

**Why they disagree.** At k = 5 the largest Ward group holds 164 rooms and has no signature: no fourth-order theme its members change at 1.5 times the population's share in a third of them. It is three of the eight forms merged (B, G and H at k = 8). So the clearest gap separates a middle group with no shared lean from four groups that lean one way each. J ruled out a broad form whose rooms share no pattern beyond breadth, and that group is one. By the logged rule I carry k = 8, the stability cut, and give the k = 5 cut in full in section 5.

## 3. The eight forms, placed by J's rule

By Ward on the defining rooms the forms hold 151, 81, 78, 62, 57, 46, 43 and 40 rooms (ratio 3.78). After placement they hold 135, 84, 89, 50, 62, 64, 124 and 76 (ratio 2.70, within J's bound of 3).

| form | the pattern of change | defining rooms (Ward) | placed rooms | of them thin | moved in | moved out | ties | with a secondary form | signature: fourth-order theme (share of members' changes; times the population; members holding it) | one kind or a mixture |
|---|---|---|---|---|---|---|---|---|---|---|
| A | the terms between neighbours reworked | 151 | 135 | 22 | 36 | 75 | 35 | 58 | T4-016 Negotiated order (0.28; 2.0; 97%) | one kind |
| B | help traded, restraint and carrying on reworked | 81 | 84 | 19 | 24 | 45 | 17 | 26 | T4-017 Reciprocity (0.10; 2.7; 36%); T4-028 Transition (0.09; 2.7; 42%); T4-015 Live and let live (0.07; 2.6; 38%) | a mixture |
| C | keeping reworked: defence, repair and the chat that arranges them | 78 | 89 | 13 | 28 | 31 | 28 | 42 | T4-013 Repair work (0.21; 2.4; 90%); T4-010 Backstage decision-making (0.09; 2.3; 41%) | one kind |
| D | the plan and its venue reworked: templates kept current and the chat's door kept | 62 | 50 | 8 | 11 | 31 | 27 | 28 | T4-008 Standardization of output (0.18; 4.6; 64%); T4-010 Backstage decision-making (0.15; 3.7; 64%) | one kind, with two means |
| E | the spot reworked: lost, chosen or yielded, and building again | 57 | 62 | 12 | 16 | 24 | 11 | 27 | T4-014 Territoriality (0.36; 5.2; 100%) | one kind |
| F | machine hands reworked, beside attack calls and records of the end | 46 | 64 | 4 | 27 | 13 | 15 | 37 | T4-009 Workarounds (0.29; 5.5; 98%); T4-020 Repertoire of contention (0.08; 2.7; 39%); T4-027 Collective memory (0.07; 1.6; 44%) | mostly one kind |
| G | the mark's design and its marking reworked | 43 | 124 | 28 | 67 | 6 | 13 | 46 | T4-006 Collective representation (0.39; 3.5; 98%); T4-026 Completion ritual (0.09; 1.8; 51%) | one kind as cut; a mixture as placed |
| H | attack calls and mobilization reworked, with records of the end | 40 | 76 | 20 | 30 | 14 | 35 | 55 | T4-020 Repertoire of contention (0.17; 5.8; 70%); T4-005 Mobilization (0.11; 2.6; 45%); T4-027 Collective memory (0.08; 1.9; 48%) | a mixture, with a raiding core |
| K | the core: no selected change | | 21 | | | | | | none | |

**How many rooms move against the whole mix: 239 of 684** (229 defining rooms whose Ward form differs from their signature placement, and 10 thin rooms whose nearest centre differs). 181 placements are ties between two or more forms. 11 rooms have no change on any signature and are placed by their whole mix.

**Why G grows from 43 to 124.** The rule counts changes, and G's signature theme, the mark's design (collective representation), is one that 327 rooms change. A room with a few design changes among many others is drawn to G whatever the rest of its mix. 67 of G's 124 rooms have their whole mix in another form. The count rule favours forms whose signature themes are common.

## 4. The members, read as rooms

I read each form's best fits, the misfits the rule takes away, and the members with the smallest share on the signature, through their lines' how sentences (`_analysis/d4a06_read.py`). Best fits are taken among defining rooms, since a thin room reaches a full share with one or two changes.

| form | best fits (defining rooms, largest share on the signature) | misfits the rule moves out (largest rooms), and where they go | members with the smallest share on the signature |
|---|---|---|---|
| A | r/mechanicalkeyboards (14 changes, 0.79), r/duckgame (7 changes, 0.71), r/notredame (9 changes, 0.67) | r/babymetal (25) to C, r/paladins (25) to B, r/anime (24) to H | r/costa_rica (0.12), r/ethereum (0.13), r/borussiadortmund (0.16) |
| B | r/ElSalvador (5 changes, 1.00), r/httyd (8 changes, 0.62), r/germany (5 changes, 0.60) | r/wholesomememes (24) to C, r/reddevils (22) to C, r/frankocean (21) to A | r/romania (0.07), r/homestuck (0.11), r/purdue (0.12) |
| C | r/darksouls (8 changes, 0.75), r/pokemon (8 changes, 0.75), r/wales (8 changes, 0.75) | r/greenlattice (24) to B, r/catalunya (18) to A, r/portugal (17) to A | r/uofm (0.17), r/monsterhunter (0.17), r/yumenikki (0.17) |
| D | r/lofihiphop (6 changes, 0.83), r/straya (7 changes, 0.71), r/starryknights (12 changes, 0.67) | r/prequelmemes (25) to C, r/theexpanse (24) to A, r/de (23) to A | r/ucf (0.18), r/armenia (0.20), r/cowchop (0.23) |
| E | r/warthunder (12 changes, 0.83), r/pebble (13 changes, 0.77), r/twitch (8 changes, 0.75) | r/FloydVsVoid (26) to C, r/nbaspurs (21) to A, r/indieheads (17) to G | r/utahjazz (0.17), r/sonicthehedgehog (0.17), r/kingdomhearts (0.22) |
| F | r/aeon (7 changes, 0.86), r/rust (20 changes, 0.75), r/eesti (8 changes, 0.75) | r/sips (21) to E, r/rutgers (15) to B, r/texans (15) to B | r/halo (0.12), r/ducks (0.20), r/rangers (0.21) |
| G | r/guatemala (6 changes, 1.00), r/kindafunny (6 changes, 1.00), r/CSUFoCo (5 changes, 1.00) | r/gamindustri (20) to B, r/parahumans (15) to B, r/4chan (13) to F | r/anime_irl (0.00), r/habs (0.13), r/crusaderkings (0.18) |
| H | r/DatBoi (5 changes, 0.80), r/completeanarchy (13 changes, 0.77), r/HomestarRunner (15 changes, 0.73) | r/canucks (25) to F, r/spain (17) to D, r/anaheimducks (16) to B | r/uwaterloo (0.25), r/swordartonline (0.25), r/orderofthebluecorner (0.25) |

- **A, the terms between neighbours reworked: one kind.** The best fits change how rooms settle space with neighbours. In r/mechanicalkeyboards a call is followed by a contested overlap; in r/duckgame a threatened picture becomes a shared design as a peace term; in r/notredame a negotiation answers a collision expected during building. The misfits the rule moves out are rich rooms (24 and 25 changes) whose changes spread over many forms: r/babymetal goes to C, r/paladins to B, r/anime to H. They belong to several forms, and one placement per room hides that.
- **B, help traded, restraint and carrying on reworked: a mixture.** Three signatures, each held by fewer than half of the defining members. r/ElSalvador, r/httyd and r/germany change how help is traded and whether a protection bargain is delivered; r/AcePlace carries its work to another canvas. The lowest shares (r/romania, r/homestuck, r/purdue) are rooms tied across several forms.
- **C, keeping reworked: one kind.** The best fits change keeping under strain: in r/pokemon doubt and loss do not lead to a move; in r/wales members' sleep prompts proposed shifts and a chat for repair; in r/darksouls a negotiated incorporation preserves the art and a broken chat invitation is repaired. The large misfits (r/greenlattice, r/catalunya, r/portugal) go to B and A.
- **D, the plan and its venue reworked: one kind, with two means.** The template and the chat that carries it. In r/lofihiphop a corrective rebuild points to updates of the plan elsewhere; in r/straya the plan needs current versions and accurate geometry; in r/starryknights the chat's access and its sanctions are kept. The large misfits (r/prequelmemes, r/theexpanse, r/de) go to C and A.
- **E, the spot reworked: one kind.** In r/warthunder a proposed move returns to building, and permission is timed for when the host's members are awake; in r/pebble a missed relocation message and a request for space; r/twitch reports where an image stands. r/day9, the room that best supports the account, is placed here: all 3 of its changes are on the spot theme. The large misfits (r/FloydVsVoid, r/nbaspurs, r/indieheads) go to C, A and G.
- **F, machine hands reworked: mostly one kind.** Scripts are among the changes of 98 per cent of the defining members. In r/aeon runners are recruited for a tool made elsewhere; in r/rust a later target proposal threatens work marked for preservation. A minority's share comes from records of the end or from attack calls. Rooms where scripts are a smaller part (r/sips, r/rutgers, r/texans) go to E and B.
- **G, the mark's design and its marking reworked: one kind as cut, a mixture as placed.** The Ward members change how the design is settled and the start made public: in r/guatemala publicity is requested after the first placement; in r/kindafunny competing placements bring an invitation into the thread; in r/CSUFoCo helpers find a broken reference. As placed, G holds 124 rooms, 67 of them drawn from other forms by their design changes (section 3).
- **H, attack calls and mobilization reworked: a mixture, with a raiding core.** The best fits are raiding rooms: in r/completeanarchy members troll rivals with deceptive scripts; in r/HomestarRunner attack calls meet bare and reasoned refusals; in r/DatBoi peace offers come before later attack calls on the same neighbour. Thin rooms placed here change calls to place (r/transgender) or record how the work ended (r/tokyo, r/wsu). The large misfits (r/canucks, r/spain, r/anaheimducks) go to F, D and B.

## 5. The other cut: k = 5, the gap's choice

| form at k = 5 | defining rooms (Ward) | placed rooms | signature: fourth-order themes |
|---|---|---|---|
| A | 164 | 66 | none |
| B | 151 | 185 | T4-016 Negotiated order |
| C | 140 | 216 | T4-013 Repair work; T4-010 Backstage decision-making; T4-008 Standardization of output |
| D | 57 | 84 | T4-014 Territoriality |
| E | 46 | 133 | T4-009 Workarounds; T4-020 Repertoire of contention; T4-027 Collective memory |

The five groups nest in the eight: k = 5's A is k = 8's B, G and H; its B is A; its C is C and D; its D is E; its E is F. Group A has no signature, so under J's rule its rooms go wherever their changes lie on the other signatures, and it keeps 66 rooms, those with no signature change (median 4 changes). After placement the sizes are 66, 185, 216, 84 and 133 (ratio 3.27), and 263 rooms move against the whole mix.

## 6. The raiding and takeover rooms, and the rich rooms the model fit without change

| set | rooms | A | B | C | D | E | F | G | H | core |
|---|---|---|---|---|---|---|---|---|---|---|
| raiding (a change on attack calls) | 102 | 15 | 7 | 5 | 6 | 4 | 21 | 11 | 33 | 0 |
| takeover (F02) | 33 | 8 | 7 | 1 | 2 | 2 | 2 | 4 | 7 | 0 |

- **Raiding rooms** (102, those with at least one selected change on attack calls). For most, raiding is a small part of their changes (median 15 per cent), so they spread across the forms by the rest. Where raiding is a large part, the room sits in H: of the 27 rooms with a quarter or more of their changes on attack calls, 19 are in H and 6 in F.
- **Takeover rooms** (the 33 members of F02, the takeover run as a temporary regime). Their changes on the April Fools frame are a median 14 per cent of their selected changes, and no form's signature holds the frame. They spread over all eight forms, most in A, B and H (8, 7 and 7). The forms sort them by their canvas changes; the takeover is one part of their record, beside the canvas work.
- **Rich rooms the model fit without change.** The core holds r/startrek, with 137 coded concepts (the population median is 101) and 28 accepted lines, every one of which instantiates the model. The other 20 core rooms hold 1 to 22 coded concepts. Kept together as the instruction says, the core joins two kinds of room: one the model describes without change, and rooms with too little record to need a change.

| room | coded concepts |
|---|---|
| r/startrek | 137 |
| r/n64 | 22 |
| r/pgang | 8 |
| r/quq | 8 |
| r/GreenEmpire | 7 |
| r/bannedfromanime_irl | 6 |
| r/mcgillrobotics | 6 |
| r/signal | 6 |
| r/Lugarix | 5 |
| r/sakartvelo | 5 |
| r/NovaScotia | 4 |
| r/Redox | 4 |
| r/greenland | 3 |
| r/churchofhelix | 2 |
| r/PokemonSage | 2 |
| r/TheID | 2 |
| r/UMiami | 2 |
| r/UNLincoln | 2 |
| r/nonbinary | 1 |
| r/wario | 1 |
| r/yerbamate | 1 |

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

| room | form | placed by | tied forms | secondary forms | whole-mix form | changes | primary branch | secondary branches |
|---|---|---|---|---|---|---|---|---|
| 2007scape | C | signature |  |  | C | 13 |  |  |
| 49ers | A | signature |  |  | A | 14 | F10 | F21 |
| 4chan | F | signature |  |  | G | 13 | F01 | F06, F08, F34 |
| aceattorney | H | signature |  |  | A | 15 |  |  |
| acecombat | H | signature |  | A, F | A | 9 | F02 | F01 |
| AceOfAngels8 | G | signature |  |  | B (thin) | 1 |  |  |
| AcePlace | B | signature |  |  | B | 9 | F17 | F25 |
| achievement_hunter | E | signature |  | C | E (thin) | 3 |  |  |
| adventuretime | E | signature |  |  | E | 13 | F09 | F25 |
| aeon | F | signature |  | H | F | 7 | F19 | F08, F17 |
| aeskwadraat | G | tie, nearest centre | B, F, G, H | B, F, H | G (thin) | 3 | F12 | F11, F34 |
| afip | F | tie, nearest centre | F, G, H | G, H | F (thin) | 3 | F19 | F17 |
| aggies | A | signature |  | F, G | A | 12 |  |  |
| ainbowroad | C | signature |  |  | C | 19 |  |  |
| albania | G | signature |  | F | G (thin) | 3 |  |  |
| alberta | G | signature |  |  | H | 9 |  |  |
| AMD | G | signature |  |  | G | 11 | F01 | F03, F04, F07 |
| AmericanFlaginPlace | C | signature |  |  | C | 23 | F08 | F23, F29 |
| anaheimducks | B | signature |  |  | H | 16 | F14 | F09, F11, F34 |
| anarchism | F | signature |  | H | F | 5 |  |  |
| anarcho_capitalism | E | signature |  | H | A | 12 |  |  |
| anarchocapitalism | C | signature |  |  | C (thin) | 1 |  |  |
| androidgaming | B | signature |  |  | B | 16 |  |  |
| animalcrossing | D | signature |  |  | D | 10 | F09 | F15 |
| anime | H | signature |  | A, F | A | 24 | F19 | F17 |
| anime_irl | G | whole mix (no signature change) |  |  | G | 5 | F01 | F04, F05 |
| aoe2 | G | tie, nearest centre | B, G | B | G (thin) | 2 | F34 |  |
| apocalypserising | G | tie, nearest centre | C, D, G | C, D | D | 6 |  |  |
| AprilKnights | D | tie, nearest centre | C, D | C | D | 6 | F16 | F29 |
| araragi | G | signature |  |  | B | 5 |  |  |
| archlinux | G | signature |  |  | A | 11 | F07 | F08 |
| argentina | H | tie, nearest centre | F, H | C, D, F | D | 8 |  |  |
| armenia | D | tie, nearest centre | B, D, G |  | B | 5 |  |  |
| armok | C | signature |  |  | C | 14 | F27 |  |
| aromantic | B | signature |  |  | B (thin) | 2 |  |  |
| asexual | H | tie, nearest centre | F, H | F | H | 6 |  |  |
| asexuality | B | signature |  | C, G | B | 15 | F17 |  |
| asktransgender | B | signature |  |  | B (thin) | 4 |  |  |
| auburn | A | signature |  | C | A (thin) | 4 |  |  |
| australia | G | signature |  | H | H | 7 | F07 |  |
| austria | A | signature |  |  | H | 16 |  |  |
| austriahungary | G | signature |  |  | G (thin) | 1 |  |  |
| AvoArmy | G | signature |  |  | G | 12 | F07 | F24 |
| AyyMD | G | signature |  |  | C | 14 | F07 | F34 |
| azerbaijan | H | tie, nearest centre | F, G, H | F, G | H (thin) | 3 | F19 | F17, F20 |
| azores | G | signature |  |  | B (thin) | 1 |  |  |
| babymetal | C | signature |  |  | A | 25 | F22 | F27 |
| bahrain | B | whole mix (no signature change) |  |  | B (thin) | 1 | F01 |  |
| bakchodi | F | signature |  |  | H | 5 | F08 |  |
| bangladesh | D | tie, nearest centre | C, D | C, E | D | 8 |  |  |
| bangtan | C | tie, nearest centre | C, E | E | C | 12 | F17 |  |
| bannedfromanime_irl | K |  |  |  |  | 0 |  |  |
| bardmains | G | signature |  |  | A | 16 | F07 | F23, F34 |
| batman | A | signature |  | C | A | 12 |  |  |
| battlecats | E | signature |  |  | E | 9 | F02 | F01 |
| baylor | G | signature |  |  | G | 5 | F33 |  |
| bdsm | G | signature |  |  | G (thin) | 2 |  |  |
| bees | H | tie, nearest centre | F, H | F | H (thin) | 1 |  |  |
| belgium | F | signature |  | H | H | 13 | F24 |  |
| berkeley | E | tie, nearest centre | E, G | G | E (thin) | 4 | F09 |  |
| berserk | E | signature |  |  | E | 18 | F09 | F16, F32 |
| bigbang | H | whole mix (no signature change) |  |  | H (thin) | 2 |  |  |
| bih | C | signature |  |  | C | 7 |  |  |
| bindingofisaac | B | signature |  |  | B | 23 | F01 | F02, F04, F11, F12, F23 |
| bisexual | A | signature |  |  | A | 23 | F07 | F31 |
| bitcoin | A | signature |  | F, G | A | 8 |  |  |
| blackmirror | G | signature |  | F, H | G (thin) | 4 |  |  |
| bobross | H | signature |  |  | H (thin) | 4 |  |  |
| borderlands | C | tie, nearest centre | C, G | G | C | 6 | F27 | F34 |
| borussiadortmund | A | tie, nearest centre | A, G, H |  | A | 19 | F21 | F35 |
| bostonbruins | A | tie, nearest centre | A, H | H | A | 7 | F32 |  |
| bostonceltics | E | signature |  |  | B | 8 | F04 | F01, F09, F17, F18 |
| brasil | D | tie, nearest centre | C, D | C | D | 10 |  |  |
| Bravenewbies | D | tie, nearest centre | C, D, G | C, G | D (thin) | 2 |  |  |
| Braveryjerk | H | tie, nearest centre | F, H | F | H (thin) | 1 |  |  |
| bretagne | G | signature |  | C | B | 6 |  |  |
| btc | A | signature |  |  | A (thin) | 4 | F28 |  |
| buffalo | B | tie, nearest centre | B, F | F | B | 10 | F12 | F11, F24 |
| buffalobills | A | signature |  |  | A | 17 | F10 | F26 |
| buffalowizards | C | signature |  |  | E | 5 | F09 |  |
| bulgaria | G | signature |  | B | A | 16 |  |  |
| calgaryflames | B | signature |  |  | H | 6 | F09 |  |
| calvinandhobbes | G | signature |  | A | A | 7 | F07 |  |
| canada | C | signature |  |  | C | 13 | F01 |  |
| canucks | F | signature |  |  | H | 25 | F01 | F03, F04, F20, F24, F30 |
| cardinals | H | tie, nearest centre | F, H | F | A | 11 |  |  |
| carletonu | A | signature |  | D | A (thin) | 3 |  |  |
| catalonia | F | tie, nearest centre | B, F | B | F | 8 | F08 |  |
| catalunya | A | signature |  | G | C | 18 | F07 | F10, F28 |
| catholicism | B | signature |  |  | B | 9 | F23 |  |
| cavestory | D | tie, nearest centre | B, C, D | B, C | A | 7 | F10 | F16 |
| CelticFc | A | signature |  |  | A (thin) | 1 | F28 |  |
| cfb | H | signature |  |  | A | 7 | F02 | F01 |
| cgpgrey | B | signature |  | H | B | 12 | F14 | F11, F23 |
| chelseafc | G | signature |  |  | D | 20 | F04 | F01, F31 |
| chess | H | tie, nearest centre | F, H | F | E | 9 | F33 |  |
| chibears | A | signature |  |  | A | 7 | F09 | F20 |
| chicago | G | signature |  |  | A | 19 | F07 | F21, F31 |
| chicubs | B | signature |  |  | A | 14 |  |  |
| chile | C | signature |  |  | C | 22 | F21 | F30 |
| ChronoTrigger | C | signature |  |  | C | 6 | F12 | F11 |
| churchofhelix | K |  |  |  |  | 0 |  |  |
| cirkeltrek | D | tie, nearest centre | A, C, D | A, C | D (thin) | 3 |  |  |
| CKCrusaders | H | signature |  | G | H | 8 |  |  |
| Clannad | C | tie, nearest centre | C, G | G | C (thin) | 2 |  |  |
| clashroyale | A | tie, nearest centre | A, H | H | A | 11 | F35 |  |
| clg | H | tie, nearest centre | F, H | F | D | 14 | F32 |  |
| cloud9 | A | tie, nearest centre | A, H |  | C | 10 | F12 | F11, F28 |
| clubpenguin | E | signature |  |  | E | 11 | F12 | F09, F11 |
| cmu | E | tie, nearest centre | A, E | A | F | 10 |  |  |
| coldplay | A | signature |  | G | A | 14 | F07 | F10, F33 |
| colombia | B | tie, nearest centre | B, G | G | B (thin) | 4 | F22 |  |
| colorado | C | tie, nearest centre | C, D, G | D, G | C (thin) | 3 | F15 |  |
| columbia | H | signature |  | A, F | A | 11 | F15 |  |
| completeanarchy | H | signature |  | F | F | 13 |  |  |
| compsoc | G | signature |  |  | B (thin) | 2 |  |  |
| Cornwall | A | signature |  |  | A (thin) | 1 |  |  |
| corridor | E | signature |  | B | E | 15 | F25 |  |
| COSI | E | signature |  |  | E (thin) | 1 |  |  |
| costa_rica | A | tie, nearest centre | A, E, F, G, H |  | C | 8 |  |  |
| counting | G | whole mix (no signature change) |  |  | G (thin) | 2 |  |  |
| cowchop | D | tie, nearest centre | A, D |  | D | 13 | F24 | F27, F28 |
| criticalrole | A | tie, nearest centre | A, D | D | A | 19 | F01 | F15 |
| croatia | A | signature |  | G | A (thin) | 4 | F07 |  |
| crusaderkings | G | tie, nearest centre | G, H |  | A | 11 | F08 |  |
| CryptoFR | B | whole mix (no signature change) |  |  | B (thin) | 3 |  |  |
| crystalclear | C | tie, nearest centre | C, G | G | C (thin) | 2 | F34 |  |
| CSUFoCo | G | signature |  |  | G | 5 | F33 |  |
| cubers | G | signature |  | B | G | 12 | F12 | F11 |
| cuboulder | H | tie, nearest centre | F, H | F | H (thin) | 1 |  |  |
| czech | A | signature |  |  | F | 14 | F07 | F08, F25 |
| daftpunk | A | tie, nearest centre | A, G | G | A | 9 |  |  |
| dallasstars | F | tie, nearest centre | E, F | E | F | 11 | F01 | F24 |
| danganronpa | B | signature |  |  | B | 16 | F02 | F01, F24 |
| dankmemes | H | signature |  | F | H | 10 | F01 | F02, F03, F04 |
| darksouls | C | signature |  | D | C | 8 | F16 |  |
| DatBoi | H | signature |  | F | H | 5 |  |  |
| davidbowie | C | tie, nearest centre | C, D, G, H | D, G, H | C (thin) | 4 | F15 |  |
| day9 | E | signature |  |  | E (thin) | 3 | F09 |  |
| dbz | A | signature |  | E | E | 14 | F01 |  |
| DCFU | G | signature |  | A | A | 6 | F22 |  |
| de | A | signature |  | D | D | 23 | F16 | F30 |
| denmark | C | tie, nearest centre | B, C | B | C | 8 | F11 |  |
| denverbroncos | A | tie, nearest centre | A, H |  | A | 20 | F03 | F01, F17, F18 |
| destiny | H | tie, nearest centre | F, H | B, F | H (thin) | 4 | F22 |  |
| DestinyTheGame | A | tie, nearest centre | A, B |  | A | 17 | F02 | F01, F23 |
| detroitlions | H | tie, nearest centre | F, H | F | H | 13 | F34 |  |
| detroitredwings | A | signature |  |  | E | 12 |  |  |
| DevonUK | A | signature |  |  | A (thin) | 2 |  |  |
| diablo | H | signature |  | E | E | 9 |  |  |
| DiamondClub | H | tie, nearest centre | F, H | F | H (thin) | 1 |  |  |
| dmt | H | signature |  |  | H (thin) | 2 |  |  |
| dofus | G | signature |  |  | G (thin) | 1 |  |  |
| Dominican | E | signature |  |  | E | 10 |  |  |
| donaldglover | E | signature |  | C | E | 12 | F11 |  |
| Dorset | A | signature |  |  | A | 6 |  |  |
| dota2 | F | signature |  |  | F | 15 | F05 | F01, F08, F28 |
| dragonquest | F | signature |  | A, G | A | 8 | F33 |  |
| drawhelix | C | tie, nearest centre | C, G | G | C | 7 | F10 |  |
| drugs | A | tie, nearest centre | A, G | G | A (thin) | 3 |  |  |
| drumcorps | A | signature |  |  | A | 7 | F01 | F03, F10 |
| duckgame | A | signature |  |  | A | 7 |  |  |
| ducks | F | tie, nearest centre | F, H |  | B | 5 |  |  |
| Dustforce | E | tie, nearest centre | A, E | A | E (thin) | 4 | F09 | F10 |
| dwarffortress | C | signature |  | D | C | 17 | F16 |  |
| eagles | B | signature |  | C | D | 10 |  |  |
| earthbound | C | signature |  | A | C | 12 | F10 | F26 |
| edboxes | H | signature |  |  | A | 16 | F07 |  |
| eder | G | tie, nearest centre | F, G, H | F, H | G (thin) | 2 | F20 |  |
| edmontonoilers | H | tie, nearest centre | F, H | F, G | B | 12 |  |  |
| eesti | F | signature |  | E, H | F | 8 | F08 |  |
| egypt | G | signature |  | B | G (thin) | 4 | F22 |  |
| ElderScrolls | C | signature |  | G | A | 6 | F01 | F32 |
| elitedangerous | C | tie, nearest centre | C, G | G | C (thin) | 4 | F04 | F01 |
| ElSalvador | B | signature |  |  | B | 5 |  |  |
| empiredidnothingwrong | C | tie, nearest centre | C, G | G | D | 20 | F27 |  |
| england | F | signature |  | B, H | F | 9 |  |  |
| enterthegungeon | H | signature |  |  | B | 10 | F23 |  |
| epublica | A | signature |  | B | A | 16 | F24 |  |
| EraseThePlace | B | signature |  |  | B | 19 | F29 |  |
| esperanto | B | signature |  |  | B | 11 | F12 | F11, F16 |
| ethereum | A | signature |  |  | A | 16 | F01 |  |
| ethoslab | A | signature |  |  | A | 5 | F01 |  |
| europe | C | tie, nearest centre | C, D | D | C | 17 |  |  |
| eve | C | signature |  | A, D | C | 12 | F07 | F16, F29 |
| evedreddit | A | signature |  |  | A (thin) | 1 |  |  |
| evex | A | signature |  |  | E | 13 | F08 | F10, F34 |
| factorio | F | tie, nearest centre | F, G | G | A | 9 | F07 |  |
| faeria | A | signature |  |  | A | 14 | F18 | F10, F17, F31 |
| falcons | B | tie, nearest centre | B, F | F | B | 11 | F01 |  |
| farmcarrots | G | signature |  | A | A | 12 | F07 | F34 |
| FaroeIslands | H | tie, nearest centre | F, H | F | H | 10 | F09 |  |
| FederationPlace | G | signature |  |  | C | 15 | F08 | F10 |
| feedthebeast | A | signature |  |  | A | 10 | F14 | F01, F11, F24, F33 |
| Fez | B | signature |  |  | B | 9 | F21 |  |
| FinalFantasy | B | signature |  |  | B | 15 |  |  |
| finland | A | signature |  | G | A | 6 |  |  |
| fireemblem | A | tie, nearest centre | A, C |  | A | 10 |  |  |
| fivenightsatfreddys | A | tie, nearest centre | A, H |  | A | 22 | F01 | F02, F07, F09, F10, F23, F29, F31 |
| FlaggyFlag | H | signature |  | C, G | H | 7 | F07 | F35 |
| flashtv | E | signature |  | B | B | 16 | F02 | F01, F07, F09 |
| FlipnoteStudio3D | H | signature |  |  | H (thin) | 1 |  |  |
| floridagators | C | signature |  |  | C | 5 |  |  |
| FloydVsVoid | C | signature |  | A, D | E | 26 | F15 | F30, F31 |
| flyers | B | tie, nearest centre | B, G | G | B | 14 | F18 | F17, F22 |
| formula1 | B | tie, nearest centre | B, E, G |  | B | 6 | F02 | F01, F09 |
| forsen | D | signature |  |  | D | 15 | F12 | F11, F16, F30 |
| foxes | D | tie, nearest centre | B, D | B | D | 16 | F31 |  |
| foxstevenson | E | signature |  |  | E (thin) | 3 |  |  |
| france | F | signature |  |  | D | 6 |  |  |
| frankocean | A | signature |  |  | B | 21 | F27 | F31 |
| frc | F | signature |  |  | B | 10 | F24 | F25, F27 |
| freedomplanet | E | signature |  | D | E | 6 | F19 | F09, F16, F17 |
| ftlgame | H | tie, nearest centre | F, H | D, F | H | 7 | F18 | F15, F17 |
| fullcommunism | C | tie, nearest centre | C, F, G | F, G | C | 6 | F17 |  |
| funhaus | A | signature |  |  | A | 15 | F30 |  |
| furry | A | tie, nearest centre | A, C | C | A | 16 | F26 |  |
| furry_irl | B | signature |  |  | B | 10 | F05 | F01, F11, F12, F22 |
| futanari | H | tie, nearest centre | F, H | F, G | A | 5 |  |  |
| futurama | C | tie, nearest centre | A, C, H |  | B | 10 | F23 | F24, F27 |
| fxKorea | G | signature |  |  | G | 9 | F18 | F07, F17 |
| GabrielDropout | G | tie, nearest centre | D, F, G | D, F | G (thin) | 4 |  |  |
| gameattack | B | signature |  |  | A | 11 | F21 |  |
| gameboy | E | tie, nearest centre | E, F, H | F, H | E (thin) | 3 |  |  |
| gameofthrones | C | tie, nearest centre | C, G |  | B | 10 | F02 | F01, F07, F17, F18, F28 |
| gamindustri | B | tie, nearest centre | B, G |  | G | 20 | F12 | F11, F22 |
| gatech | G | signature |  |  | A | 19 | F08 | F07, F11, F14, F23, F33 |
| genderfluid | C | signature |  |  | C (thin) | 4 |  |  |
| geometrydash | B | signature |  | H | B | 8 | F01 | F02 |
| germany | B | signature |  |  | B | 5 |  |  |
| ghibli | D | signature |  | F, H | H | 6 | F15 |  |
| giantbomb | F | signature |  |  | A | 15 |  |  |
| giivasunner | E | signature |  |  | B | 11 | F09 | F22 |
| glasgow | C | tie, nearest centre | C, G | G | C | 6 |  |  |
| globaloffensive | F | signature |  |  | C | 9 | F13 | F11 |
| Goodboye | C | signature |  |  | C | 9 |  |  |
| gorillaz | G | signature |  | B | G | 17 | F25 |  |
| GranColombia | C | signature |  | D | C | 7 | F16 | F24, F30 |
| gratefuldead | E | signature |  |  | E | 8 |  |  |
| gravityfalls | G | signature |  |  | C | 9 | F12 | F11, F27 |
| greece | G | signature |  |  | G | 11 | F27 |  |
| greenbaypackers | F | signature |  | H | F | 11 |  |  |
| GreenCorner | C | tie, nearest centre | B, C |  | C | 9 |  |  |
| GreenEmpire | K |  |  |  |  | 0 |  |  |
| greenland | K |  |  |  |  | 0 |  |  |
| greenlattice | B | signature |  |  | C | 24 | F12 | F11 |
| greyblob | B | tie, nearest centre | B, E | E | B | 9 | F12 | F09, F11, F23 |
| GrowTheTree | G | signature |  | A | A (thin) | 4 |  |  |
| GuardiansOfDatBoi | H | signature |  | D, F | H | 7 | F15 |  |
| guatemala | G | signature |  |  | G | 6 |  |  |
| GuildWars2 | H | signature |  |  | H | 9 | F01 | F35 |
| h3h3productions | H | signature |  |  | H | 12 | F21 |  |
| habs | G | tie, nearest centre | F, G, H |  | B | 15 | F32 |  |
| halo | F | signature |  |  | H | 8 |  |  |
| harrypotter | G | signature |  | A, B | A | 8 | F01 | F22, F26 |
| haskell | E | signature |  |  | E (thin) | 3 |  |  |
| hatsune | E | signature |  |  | E | 16 | F20 | F35 |
| hawks | B | signature |  |  | B | 14 | F22 | F24, F27 |
| hearthstone | A | signature |  |  | A | 13 | F10 |  |
| hellointernet | A | signature |  |  | A | 12 | F27 | F33 |
| hentai | G | signature |  |  | B | 10 | F07 | F22 |
| heroesofthestorm | C | signature |  |  | C | 9 | F01 | F29 |
| heyyea | G | signature |  |  | G | 7 | F11 |  |
| homelab | H | tie, nearest centre | F, H | F | H | 12 |  |  |
| HomestarRunner | H | signature |  | F | H | 15 |  |  |
| homestuck | B | tie, nearest centre | B, C, E, H |  | B | 9 | F35 |  |
| Homura | D | tie, nearest centre | C, D | C | D (thin) | 1 |  |  |
| Honduras | G | signature |  | B | B | 5 |  |  |
| hongkong | G | signature |  | A | A | 7 | F07 | F31 |
| hoodr | B | whole mix (no signature change) |  |  | B (thin) | 3 |  |  |
| hsv | C | signature |  |  | A | 13 |  |  |
| httyd | B | signature |  | G | B | 8 | F32 |  |
| hungary | B | signature |  | A, F, H | A (thin) | 4 | F23 | F28 |
| hunterxhunter | A | signature |  |  | A | 8 | F03 | F01 |
| hyperlightdrifter | F | tie, nearest centre | E, F | E | D | 12 | F07 | F08, F09, F15, F16, F24 |
| iastate | G | signature |  | C | C | 10 |  |  |
| ibo | H | signature |  | F | H (thin) | 4 |  |  |
| ice_poseidon | H | signature |  | F | H | 11 | F21 |  |
| iceland | A | signature |  |  | A (thin) | 1 |  |  |
| ik_ihe | D | tie, nearest centre | C, D | C | D (thin) | 2 | F16 |  |
| india | F | signature |  | G | F | 14 | F08 | F23, F33 |
| indieheads | G | signature |  |  | E | 17 | F01 | F07, F09 |
| indonesia | A | tie, nearest centre | A, B, G | B, G | C | 16 | F25 |  |
| ireland | G | signature |  |  | A | 10 |  |  |
| israel | A | tie, nearest centre | A, B, G | B, G | A | 7 | F07 | F10 |
| italy | F | signature |  |  | F | 9 | F12 | F11 |
| Jamaica | D | tie, nearest centre | A, D, G | A, G | C | 8 | F15 |  |
| japan | D | signature |  |  | B | 11 | F15 | F32 |
| jerma985 | H | signature |  |  | A | 16 | F09 | F29 |
| k_on | H | tie, nearest centre | F, H | F | H | 8 |  |  |
| kamenrider | A | signature |  |  | A | 11 | F15 | F21 |
| kanye | B | tie, nearest centre | B, C |  | B | 14 | F06 | F01, F11 |
| katawashoujo | G | signature |  |  | G | 6 | F07 |  |
| kcroyals | F | tie, nearest centre | F, G | G | A | 10 | F18 | F08, F17 |
| kerbalspaceprogram | A | signature |  |  | A | 10 | F01 | F02 |
| kilian | C | tie, nearest centre | A, C | A | C | 5 | F16 |  |
| kindafunny | G | signature |  |  | G | 6 | F34 |  |
| kingdomhearts | E | tie, nearest centre | A, E, G |  | A | 9 | F09 |  |
| kirby | B | tie, nearest centre | B, G | G | A | 7 | F18 | F01, F17, F25, F28 |
| konosuba | G | signature |  | B | G | 5 | F33 |  |
| korea | G | signature |  |  | A | 15 | F07 | F09, F10 |
| kpop | G | signature |  |  | G | 7 | F01 |  |
| KState | F | signature |  |  | F | 13 | F08 |  |
| kurdistan | H | tie, nearest centre | F, H | F | F | 7 | F10 |  |
| kuwait | F | signature |  |  | C | 10 | F33 |  |
| lakers | D | tie, nearest centre | C, D | C | D | 13 | F16 | F27 |
| landry | A | signature |  | B | A (thin) | 4 |  |  |
| latin | E | signature |  |  | E | 9 |  |  |
| latvia | E | tie, nearest centre | E, G | G | C | 8 |  |  |
| leafs | A | signature |  | G | A | 7 |  |  |
| leagueoflegends | G | tie, nearest centre | C, D, G | C, D | D | 7 |  |  |
| lebanon | A | signature |  |  | A | 12 | F35 |  |
| lego | B | signature |  |  | C | 12 | F13 | F11 |
| lexington | H | signature |  |  | H (thin) | 2 |  |  |
| lifeisstrange | A | signature |  |  | A | 10 | F26 |  |
| linux | D | signature |  | F | D | 11 | F10 | F15, F16 |
| liquicity | D | signature |  |  | D | 11 | F15 |  |
| lithuania | D | tie, nearest centre | A, C, D | A, C | C | 8 | F16 |  |
| littlebusters | D | signature |  |  | D (thin) | 1 |  |  |
| littlewitchacademia | D | signature |  |  | D | 13 | F10 | F15, F30, F35 |
| livecounting | F | signature |  | A | F (thin) | 4 | F08 |  |
| liverpoolfc | C | signature |  | D | C | 6 | F29 |  |
| lofihiphop | D | signature |  |  | D | 6 | F15 | F21, F30 |
| loliconsunite | C | signature |  | B, D | C | 16 | F23 | F30 |
| loltyler1 | F | signature |  | H | F | 10 | F08 |  |
| lost | G | signature |  | B, C | B | 8 |  |  |
| lovelive | B | signature |  |  | B | 9 | F13 | F11 |
| lsu | E | signature |  |  | E | 13 | F09 | F28, F30 |
| luciomains | G | signature |  |  | G | 9 | F19 | F07, F17, F32 |
| Lugarix | K |  |  |  |  | 0 |  |  |
| luxembourg | H | tie, nearest centre | F, H | F | H | 11 | F32 |  |
| Madeon | G | signature |  |  | G | 5 |  |  |
| madokamagica | D | tie, nearest centre | C, D | C | D | 9 |  |  |
| magictcg | B | tie, nearest centre | B, D, F, H |  | B | 16 | F01 | F03, F04 |
| malaysia | A | signature |  | F | E | 11 | F09 | F28, F31 |
| malta | G | signature |  |  | C | 5 |  |  |
| mamamoo | H | signature |  |  | H (thin) | 1 | F35 |  |
| ManningPlace | A | signature |  |  | A | 5 | F26 |  |
| Mario | B | tie, nearest centre | B, F, H | F, H | B (thin) | 2 | F12 | F11 |
| mariokart | B | signature |  |  | B (thin) | 4 | F03 | F01 |
| marvel | E | signature |  | G | E | 7 | F34 |  |
| maryland | A | tie, nearest centre | A, G | G | C | 8 | F22 | F26 |
| masseffect | E | signature |  |  | E | 9 | F09 | F29 |
| math | A | tie, nearest centre | A, F, H | C, F, H | A | 12 |  |  |
| mcgill | D | tie, nearest centre | C, D | C | D (thin) | 1 | F16 |  |
| mcgillrobotics | K |  |  |  |  | 0 |  |  |
| mechanicalkeyboards | A | signature |  |  | A | 14 | F26 |  |
| megaman | A | tie, nearest centre | A, G | G | C | 15 | F07 |  |
| metalcore | C | signature |  |  | B | 14 | F27 |  |
| metalgearsolid | G | signature |  |  | G | 13 | F01 | F05, F07, F16 |
| metroid | A | signature |  | E | E | 15 | F26 | F31 |
| mexico | F | signature |  | C, H | B | 8 | F08 | F29 |
| miamidolphins | A | tie, nearest centre | A, B | B | A | 6 | F26 |  |
| MiamiHurricanes | A | signature |  | E | E | 6 |  |  |
| mindcrack | A | tie, nearest centre | A, F | F | A | 14 | F24 | F28, F31 |
| minecraft | G | tie, nearest centre | B, G |  | B | 15 | F01 | F03, F05 |
| minnesotavikings | F | signature |  | A | F | 9 | F08 |  |
| miraculousladybug | B | signature |  | E | B (thin) | 4 | F05 | F01, F11 |
| mit | A | tie, nearest centre | A, G | C, G | C | 8 | F10 | F28, F33 |
| mizzou | C | tie, nearest centre | C, F, H | F, G, H | C | 8 |  |  |
| mls | A | signature |  |  | A | 17 | F06 | F01, F31 |
| MMA | H | tie, nearest centre | F, H | F | A | 14 | F01 | F02 |
| monalisaclan | D | signature |  |  | D | 17 | F15 | F16, F25, F26 |
| monero | F | tie, nearest centre | C, F | C, D | D | 11 | F16 |  |
| MonkeyIsland | C | signature |  |  | D | 10 | F15 |  |
| monstercat | F | tie, nearest centre | B, F | B | F | 15 | F01 | F02, F04 |
| monsterhunter | C | signature |  |  | C | 6 |  |  |
| montenegro | G | signature |  | C, D | G (thin) | 3 | F16 |  |
| Moondye7 | A | signature |  |  | C | 6 | F19 | F10, F15, F17 |
| mordhau | E | signature |  | C | E (thin) | 3 |  |  |
| morrowind | G | signature |  | A | A | 15 | F07 |  |
| msu | D | tie, nearest centre | A, D | A | D | 7 | F09 | F10, F15 |
| muse | G | signature |  |  | G | 6 | F07 |  |
| mylittlepony | B | signature |  | F | D | 20 | F16 | F22, F25 |
| mysterydungeon | A | tie, nearest centre | A, F, G, H |  | A | 9 |  |  |
| n64 | K |  |  |  |  | 0 |  |  |
| naruto | B | signature |  |  | B | 11 | F02 | F01, F11, F12, F23 |
| nascar | A | signature |  |  | A | 9 | F10 | F26 |
| natsume | C | tie, nearest centre | C, G | G | C (thin) | 3 |  |  |
| nbaspurs | A | signature |  |  | E | 21 | F01 | F04, F05, F09, F24, F31 |
| necrodancer | G | signature |  | E | G | 8 | F09 | F28, F29, F33 |
| neopets | B | signature |  |  | C | 16 | F29 |  |
| nerf | D | signature |  |  | D | 10 | F15 |  |
| neu | A | signature |  | F | F | 7 | F08 |  |
| neutralmilkhotel | A | signature |  | F, H | A (thin) | 3 |  |  |
| NewMexico | A | signature |  | G | E | 10 | F10 | F26, F33 |
| newzealand | G | signature |  |  | A | 14 | F07 | F32 |
| NieR | G | signature |  |  | G | 8 | F05 | F01 |
| nightinthewoods | B | signature |  | F, H | B | 14 | F01 | F15 |
| nin | G | signature |  |  | G | 20 | F18 | F17, F34 |
| nintendo | H | signature |  | F | H | 16 | F01 |  |
| nlsscirclejerk | C | tie, nearest centre | C, G | G | A | 11 | F34 |  |
| nonbinary | K |  |  |  |  | 0 |  |  |
| norge | B | whole mix (no signature change) |  |  | B (thin) | 1 |  |  |
| Northwestern | E | signature |  | D | E | 8 |  |  |
| norway | B | signature |  |  | B | 13 |  |  |
| notredame | A | signature |  |  | A | 9 | F07 | F10 |
| NovaScotia | K |  |  |  |  | 0 |  |  |
| npr | D | signature |  | A | D | 9 |  |  |
| nuclearthrone | B | signature |  |  | G | 10 | F33 |  |
| nVade | C | signature |  | A | B | 14 |  |  |
| nyjets | B | tie, nearest centre | B, E |  | B | 13 | F02 | F01, F09, F15 |
| nyu | H | tie, nearest centre | G, H | G | E | 6 |  |  |
| ockytop | D | signature |  |  | D | 9 | F15 | F23, F32 |
| ohio | C | signature |  |  | C | 10 | F10 |  |
| Okami | G | signature |  | D | D | 8 | F19 | F15, F17 |
| OKState | F | signature |  |  | F | 7 | F08 | F24 |
| oltp | C | signature |  |  | C (thin) | 1 |  |  |
| oman | H | whole mix (no signature change) |  |  | H (thin) | 2 |  |  |
| OnePiece | B | signature |  | G | B | 17 | F22 | F07, F27, F32 |
| oneplus | G | tie, nearest centre | F, G, H | F, H | G | 6 | F01 |  |
| onepunchman | A | signature |  | C, D | A (thin) | 4 | F10 |  |
| oneshot | A | signature |  |  | A | 5 |  |  |
| OneTrueEmilia | C | signature |  | B | B | 8 | F21 | F22, F27 |
| ontario | G | signature |  |  | G | 5 | F01 | F02, F03, F05 |
| opticgaming | A | signature |  |  | E | 16 | F19 | F17 |
| orderofthebluecorner | H | tie, nearest centre | C, E, F, H | C, E, F | H | 6 |  |  |
| OrderOfTheKoi | E | signature |  | C, D, F, H | D | 7 | F16 | F30 |
| osu | G | signature |  |  | B | 14 | F07 | F21 |
| osugame | B | signature |  |  | B | 20 | F29 |  |
| overwatch | B | signature |  | H | B | 23 |  |  |
| pakistan | F | signature |  | A, G, H | F | 12 | F08 | F28 |
| paladins | B | signature |  |  | A | 25 | F01 | F06, F25, F30 |
| palestine | G | tie, nearest centre | B, G | B | G | 5 | F34 |  |
| pansexual | A | signature |  |  | A (thin) | 3 |  |  |
| parabola | C | tie, nearest centre | A, C, D | A, D | C (thin) | 3 |  |  |
| paragon | G | signature |  |  | B | 11 | F01 | F02, F33 |
| parahumans | B | signature |  |  | G | 15 | F25 | F27 |
| paranatural | E | signature |  |  | E | 10 |  |  |
| parrots | C | signature |  |  | C | 10 | F13 | F11 |
| partyparrot | B | tie, nearest centre | A, B, F, G |  | A | 15 |  |  |
| pathofexile | A | signature |  |  | D | 12 |  |  |
| patriots | B | signature |  |  | F | 10 | F21 |  |
| paydaytheheist | A | tie, nearest centre | A, G | G | A (thin) | 4 | F32 |  |
| pcmasterrace | C | signature |  |  | A | 17 | F25 | F01, F05, F16, F21, F27, F30 |
| pebble | E | signature |  |  | E | 13 | F09 |  |
| penguins | H | signature |  | E, F | E | 14 | F09 | F34 |
| pepe | F | signature |  | H | F | 8 | F08 |  |
| Peru | A | signature |  | G | A | 12 | F30 |  |
| peterdraws | E | tie, nearest centre | A, E, G | A, G | E (thin) | 3 |  |  |
| pgang | K |  |  |  |  | 0 |  |  |
| philippines | D | signature |  |  | D | 12 | F15 |  |
| phish | F | signature |  |  | F | 11 | F01 | F08, F10, F23 |
| physical_removal | B | tie, nearest centre | B, C | C | B (thin) | 3 | F23 |  |
| picturegame | B | signature |  |  | B (thin) | 4 | F25 | F21 |
| Pigifs | G | signature |  |  | B (thin) | 4 |  |  |
| PinkUnion | E | signature |  |  | E | 9 |  |  |
| PinkVomitMonster | A | tie, nearest centre | A, F, H | F, H | D | 5 |  |  |
| pitt | G | signature |  |  | A | 9 | F14 | F07, F11 |
| placecanada | F | signature |  |  | D | 13 |  |  |
| placeDE | F | signature |  |  | G | 9 | F23 |  |
| placehearts | C | signature |  |  | C | 6 |  |  |
| placehfarts | H | tie, nearest centre | F, H | F | H (thin) | 1 |  |  |
| PlaceNL | F | signature |  | B | F | 22 | F08 | F22, F25 |
| placeportalpattern | A | signature |  |  | E | 9 | F23 | F24, F26 |
| placesnek | G | signature |  |  | G | 13 |  |  |
| placestart | D | signature |  |  | D | 12 | F15 | F29 |
| placetardis | A | signature |  | H | A | 12 | F10 | F15, F26 |
| planetside | E | signature |  | C, D | D | 20 | F03 | F01, F29, F30 |
| pokemon | C | signature |  |  | C | 8 | F27 |  |
| PokemonSage | K |  |  |  |  | 0 |  |  |
| poland | A | signature |  |  | A | 10 | F10 | F16, F24, F26 |
| polandball | G | signature |  |  | G | 7 | F02 | F01 |
| polska | C | tie, nearest centre | C, D, G | D, G | D | 10 | F12 | F07, F11 |
| polyamory | H | signature |  |  | H | 5 | F35 |  |
| popheads | H | tie, nearest centre | F, H | F | H | 10 | F01 | F05 |
| portal | E | signature |  | F, G, H | E | 15 | F33 |  |
| porterrobinson | G | signature |  |  | G | 17 | F07 | F24, F30 |
| portugal | A | signature |  |  | C | 17 | F13 | F11, F29 |
| PORTUGALCARALHO | G | signature |  | F, H | G (thin) | 3 | F34 |  |
| predators | F | tie, nearest centre | F, H | H | F | 13 | F08 | F22 |
| prequelmemes | C | signature |  |  | D | 25 | F13 | F11, F23, F24, F25, F30, F31 |
| Produce101 | E | signature |  |  | E (thin) | 2 |  |  |
| ProfessorLayton | G | signature |  | H | G | 8 |  |  |
| PUBATTLEGROUNDS | G | signature |  | A | A | 14 | F03 | F01, F07 |
| purdue | B | tie, nearest centre | B, E, F |  | B | 16 | F08 | F35 |
| purplecorner | B | signature |  |  | B | 16 | F23 |  |
| PurplePixels | C | signature |  |  | C | 13 | F16 |  |
| pusheen | E | signature |  | G | E | 5 | F07 | F09 |
| puzzleanddragons | B | signature |  | C, G | C | 12 | F07 |  |
| python | F | tie, nearest centre | A, F | A | F | 12 | F08 | F26 |
| qotsa | E | signature |  |  | E | 8 |  |  |
| quebec | C | signature |  | D | C | 22 | F28 | F29 |
| quq | K |  |  |  |  | 0 |  |  |
| radiohead | C | signature |  | B | B | 17 | F27 |  |
| Rainbow6 | A | signature |  |  | A | 12 | F01 | F07, F20 |
| rainbowgrid | A | signature |  |  | H | 10 |  |  |
| rangers | F | tie, nearest centre | C, D, F |  | D | 14 | F29 | F33 |
| raocow | H | signature |  |  | A | 9 | F35 |  |
| ravens | D | tie, nearest centre | D, H | H | A | 16 | F15 | F26 |
| re_zero | G | signature |  | A, F, H | G | 12 | F20 | F28, F29 |
| ReBoot | B | whole mix (no signature change) |  |  | B (thin) | 2 |  |  |
| reddevils | C | signature |  |  | B | 22 | F03 | F01, F29, F30 |
| redhotchilipeppers | C | signature |  |  | C | 5 | F16 |  |
| Redox | K |  |  |  |  | 0 |  |  |
| redpandas | G | signature |  |  | B | 11 | F22 |  |
| redvsblue | A | signature |  |  | A (thin) | 3 |  |  |
| RelientK | A | signature |  | B | E | 11 | F22 |  |
| rhythmheaven | A | signature |  |  | A | 9 | F21 | F34 |
| rickandmorty | G | signature |  |  | A | 12 | F32 |  |
| ripcity | D | tie, nearest centre | A, D, G, H | A, G, H | A | 8 | F18 | F17, F28, F32 |
| riskofrain | A | signature |  |  | A | 5 | F10 |  |
| rit | A | signature |  | H | A | 10 |  |  |
| rocketbeans | D | signature |  |  | D | 14 | F19 | F17 |
| rocketleague | A | signature |  |  | A | 10 |  |  |
| rojava | C | signature |  | G | C | 5 |  |  |
| romania | B | tie, nearest centre | B, C, G |  | B | 15 | F01 | F11, F13, F21 |
| roosterteeth | D | signature |  |  | D | 5 |  |  |
| rotmg | B | signature |  |  | B | 20 | F23 |  |
| rpi | E | signature |  | A | E | 11 | F08 |  |
| runescape | F | signature |  |  | A | 11 | F01 | F06, F08 |
| rush | G | signature |  | E | E | 8 | F02 | F01, F09, F22 |
| russia | E | signature |  |  | E | 7 | F22 |  |
| Russiaclan | H | tie, nearest centre | F, H | F | C | 13 |  |  |
| rust | F | signature |  |  | F | 20 | F08 | F01, F06 |
| rutgers | B | signature |  |  | F | 15 | F09 | F21, F22, F24 |
| rwby | A | signature |  |  | E | 14 | F01 | F02, F09 |
| sabres | F | signature |  | B, H | B | 8 | F12 | F11 |
| sadboys | B | signature |  |  | B | 11 | F12 | F11, F31 |
| sakartvelo | K |  |  |  |  | 0 |  |  |
| sakuragakuin | G | tie, nearest centre | B, G | B | C | 6 |  |  |
| samuraijack | C | signature |  |  | A | 21 | F01 | F29 |
| satania | G | signature |  |  | A | 10 | F07 |  |
| sbu | F | signature |  |  | F | 7 | F08 |  |
| schoolidolfestival | A | signature |  |  | A | 11 | F01 | F02, F05, F23 |
| scotland | G | signature |  |  | A | 9 | F24 |  |
| ScottPilgrim | A | tie, nearest centre | A, G | G | A | 5 |  |  |
| scp | C | signature |  |  | C | 14 | F21 | F30 |
| seahawks | G | signature |  | H | A | 16 | F01 | F07, F25, F31, F35 |
| seolhyun | A | signature |  | E | E (thin) | 3 | F09 | F10 |
| serbia | F | signature |  | H | F | 9 | F08 |  |
| seventeen | B | signature |  |  | B (thin) | 2 |  |  |
| sheffield | G | signature |  | E | G | 14 | F07 |  |
| shield | A | signature |  |  | A | 10 | F07 |  |
| shishamo | B | signature |  |  | B (thin) | 1 | F22 |  |
| shitredditsays | F | signature |  | C, H | H | 11 | F24 |  |
| shrooms | C | signature |  |  | C (thin) | 1 |  |  |
| signal | K |  |  |  |  | 0 |  |  |
| simonfraser | D | tie, nearest centre | B, C, D | B, C | D | 5 | F22 | F30 |
| singapore | H | tie, nearest centre | F, H | F | C | 13 |  |  |
| sips | E | signature |  | F, H | F | 21 | F20 | F21, F24 |
| sixers | C | signature |  |  | C | 13 | F27 |  |
| skyrim | A | signature |  | G | A | 7 | F10 |  |
| Slovakia | A | signature |  | B | A | 8 |  |  |
| slovenia | D | signature |  |  | D | 6 | F08 |  |
| smashbros | D | tie, nearest centre | C, D | C | D | 7 | F02 | F01 |
| smite | B | signature |  |  | B (thin) | 2 | F22 |  |
| snsd | E | signature |  |  | A | 11 |  |  |
| sonicthehedgehog | E | tie, nearest centre | A, B, C, E, G |  | B | 6 |  |  |
| sooners | F | signature |  |  | F | 10 | F08 |  |
| southafrica | A | tie, nearest centre | A, G | G | A | 7 | F21 |  |
| southpark | H | signature |  | C | E | 11 | F21 |  |
| soylent | E | tie, nearest centre | C, E | C | E | 7 | F26 |  |
| spacex | G | signature |  |  | B (thin) | 4 | F06 | F01, F17 |
| spacexmasterrace | G | signature |  | B | D | 11 | F07 | F08 |
| spain | D | tie, nearest centre | C, D |  | H | 17 | F16 |  |
| spelunky | G | signature |  |  | B (thin) | 4 | F01 |  |
| splatoon | G | signature |  | A | A | 15 | F17 |  |
| spongebob | B | signature |  | D | D | 11 | F15 | F16, F30 |
| SquareSpiral | E | signature |  | G | E | 11 | F09 | F23 |
| ss13 | A | tie, nearest centre | A, D, G | D, G | A | 15 | F15 |  |
| ssbpm | D | tie, nearest centre | C, D | C, H | D | 12 | F16 |  |
| starbound | A | signature |  | G | A | 10 | F35 |  |
| starcitizen | F | signature |  |  | B | 21 | F08 | F25 |
| starcraft | G | signature |  |  | A | 15 | F01 | F06 |
| stardewvalley | E | signature |  |  | E | 11 | F09 | F15, F21, F28, F32 |
| stardustcrusaders | G | signature |  |  | A | 14 | F01 | F30 |
| stargate | E | signature |  |  | B | 12 | F01 | F04, F09, F11, F12, F25, F35 |
| starlightstage | A | tie, nearest centre | A, G | G | A | 14 | F10 | F21, F33, F34 |
| starryknights | D | signature |  | C | D | 12 | F15 | F16 |
| startrek | K |  |  |  |  | 0 |  |  |
| starvstheforcesofevil | A | signature |  |  | A | 6 | F23 | F32 |
| stevenuniverse | C | signature |  | D | C | 19 | F01 | F16, F25, F26, F29 |
| stlouis | B | signature |  | C, F, H | B | 12 | F20 |  |
| stlouisblues | B | signature |  | D | D | 13 |  |  |
| strangerthings | A | tie, nearest centre | A, F, G, H | F, G, H | A (thin) | 3 | F34 |  |
| straya | D | signature |  |  | D | 7 |  |  |
| streetfighter | E | signature |  |  | E | 9 | F03 | F01, F21 |
| Summit1G | A | signature |  |  | A (thin) | 4 |  |  |
| suomi | A | tie, nearest centre | A, G |  | A | 20 |  |  |
| superman | G | signature |  |  | G (thin) | 2 | F33 |  |
| survivor | D | signature |  |  | A | 11 | F02 | F01, F15 |
| sweden | D | tie, nearest centre | C, D | C, F, G, H | D (thin) | 4 |  |  |
| SwissNeutralityZone | G | signature |  | D | D | 7 | F19 | F15, F17, F28, F29 |
| switzerland | A | signature |  |  | C | 11 | F10 |  |
| swordartonline | H | tie, nearest centre | F, H | F | H | 12 | F18 | F01, F17 |
| SydneyFC | G | signature |  |  | G (thin) | 2 |  |  |
| tagpro | C | signature |  | D | C | 10 | F29 |  |
| taiwan | G | signature |  | F | G | 7 | F18 | F17 |
| tampabaylightning | G | signature |  |  | A | 6 | F07 |  |
| teamcube | G | signature |  |  | G | 10 |  |  |
| TeamDignitas | H | signature |  |  | H | 8 |  |  |
| TeamYellowPlace | A | signature |  |  | A (thin) | 3 |  |  |
| telegram | C | signature |  | A | A | 7 |  |  |
| Temple | F | signature |  |  | F | 17 | F08 | F09, F25 |
| tenma | H | signature |  |  | H (thin) | 1 | F35 |  |
| terraria | A | signature |  |  | A | 12 | F01 | F02, F03, F25, F31 |
| teslamotors | A | tie, nearest centre | A, G | G | C | 7 | F08 |  |
| tetris | G | signature |  | F, H | G (thin) | 3 |  |  |
| texans | B | signature |  |  | F | 15 | F02 | F01, F11, F14 |
| texas | F | tie, nearest centre | A, F | A | E | 10 | F08 |  |
| texastech | F | signature |  | H | F | 6 |  |  |
| tf2 | G | signature |  |  | A | 5 | F33 |  |
| thailand | A | signature |  |  | A | 14 | F26 |  |
| the_pack | H | tie, nearest centre | B, H | B | B | 10 |  |  |
| THE_R | C | signature |  |  | C (thin) | 1 | F27 |  |
| TheAdventuresofTintin | G | signature |  |  | G (thin) | 3 |  |  |
| TheB1G | A | signature |  | B | A (thin) | 4 |  |  |
| theblackvoid | C | signature |  | B | B | 12 | F12 | F11 |
| thebluecorner | C | signature |  |  | B | 20 | F23 | F25, F29 |
| theexpanse | A | signature |  |  | D | 24 | F16 | F23 |
| TheFarLeftSide | B | signature |  |  | B | 13 | F23 |  |
| Thegreatblackhole | H | tie, nearest centre | F, H | F | H | 6 |  |  |
| TheGreatGreenBox | B | whole mix (no signature change) |  |  | B (thin) | 4 |  |  |
| TheHulk | G | tie, nearest centre | G, H | H | A | 13 | F07 | F32, F35 |
| TheID | K |  |  |  |  | 0 |  |  |
| theitalyplace | C | tie, nearest centre | A, C, F |  | F | 9 |  |  |
| thenetherlands | H | signature |  | F | A | 8 | F02 | F01 |
| thepointing | C | signature |  |  | C | 10 | F09 |  |
| thesilphroad | G | whole mix (no signature change) |  |  | G (thin) | 4 |  |  |
| thesimpsons | C | tie, nearest centre | C, G | G | C | 7 | F01 |  |
| thetreesnetwork | G | signature |  |  | C (thin) | 4 |  |  |
| timbers | G | signature |  |  | A | 13 | F07 | F21 |
| tinytardis | B | signature |  | C | D | 8 | F15 | F22, F25 |
| titanfall | B | signature |  |  | A | 10 | F01 | F21 |
| tokyo | H | tie, nearest centre | F, H | F | H (thin) | 3 | F20 |  |
| toolband | A | signature |  | C | A | 10 | F09 | F27 |
| torontoraptors | G | signature |  |  | A | 14 | F07 | F31, F33 |
| totallynotrobots | A | tie, nearest centre | A, B, F, G, H |  | A | 17 | F01 | F02, F25 |
| touhou | A | tie, nearest centre | A, C, D, F, H |  | D | 14 | F13 | F11, F23, F28 |
| traaaaaaannnnnnnnnns | H | signature |  | A | A | 15 |  |  |
| TransFlagPlace | D | tie, nearest centre | C, D | C | D | 5 | F16 |  |
| transformers | A | signature |  |  | A | 13 | F10 | F21, F26 |
| transgender | H | signature |  |  | H (thin) | 3 |  |  |
| TreePlace | E | signature |  | G | E (thin) | 4 |  |  |
| trees | G | signature |  |  | G | 6 |  |  |
| truestl | A | signature |  |  | A | 5 |  |  |
| TsundereSharks | C | signature |  |  | C | 10 | F07 |  |
| turkey | G | signature |  |  | C | 17 | F09 | F27 |
| twentyonepilots | E | signature |  | B | E | 16 | F25 |  |
| twice | A | tie, nearest centre | A, C | C | E | 6 | F09 |  |
| twitch | E | signature |  |  | E | 8 | F07 | F21 |
| twitchplayspokemon | C | signature |  |  | A | 17 | F01 | F09, F27 |
| ubc | A | tie, nearest centre | A, B, G | B, G | A (thin) | 3 | F22 |  |
| ubreddit | E | signature |  |  | B | 10 | F09 |  |
| ucf | D | tie, nearest centre | C, D, G, H |  | D | 11 | F15 |  |
| udub | D | signature |  |  | H | 5 | F15 |  |
| ufl | B | signature |  | H | B (thin) | 4 |  |  |
| uiowa | E | signature |  | F | F | 11 |  |  |
| uiuc | E | signature |  |  | E | 13 | F09 | F26 |
| ukplace | F | signature |  | B | F | 7 | F08 |  |
| ukraine | F | signature |  |  | F (thin) | 3 | F08 |  |
| ultrahardcore | H | tie, nearest centre | F, H | F | G | 8 | F01 | F04 |
| UMiami | K |  |  |  |  | 0 |  |  |
| undertale | C | signature |  |  | C | 9 | F32 |  |
| unitedkingdom | F | signature |  | G | F | 7 | F07 |  |
| UNLincoln | K |  |  |  |  | 0 |  |  |
| unturned | G | signature |  |  | A | 16 | F21 | F24, F32 |
| uofm | C | tie, nearest centre | C, D, F |  | F | 12 | F08 | F15 |
| uofmn | D | tie, nearest centre | A, D | A | D | 9 | F10 | F15 |
| uoft | H | signature |  |  | F | 13 | F24 | F31 |
| UPenn | E | signature |  |  | E | 7 | F09 |  |
| uruguay | B | signature |  | G | B | 7 |  |  |
| utahjazz | E | tie, nearest centre | A, D, E, G |  | D | 12 | F14 | F09, F11 |
| utaustin | F | signature |  | A | F | 20 | F28 | F17, F18, F21 |
| uva | A | signature |  |  | C | 9 |  |  |
| uvic | G | signature |  |  | G | 8 | F07 |  |
| uwaterloo | H | tie, nearest centre | F, H | F | A | 17 | F02 | F01 |
| vegan | H | signature |  | B, G | H | 8 |  |  |
| VelvetUnderground | C | tie, nearest centre | A, C | A | C (thin) | 2 |  |  |
| vermont | A | signature |  | C | A | 8 |  |  |
| vietnam | G | signature |  |  | G (thin) | 2 |  |  |
| Villanova | C | signature |  |  | C | 5 |  |  |
| vim | H | tie, nearest centre | G, H | G | H (thin) | 4 | F32 |  |
| vinesauce | E | tie, nearest centre | A, E | A | E | 11 | F09 | F31 |
| virginiatech | F | signature |  |  | F | 13 | F08 |  |
| vocaloid | G | signature |  | C, D | D | 8 | F17 | F19 |
| wales | C | signature |  | D | C | 8 |  |  |
| wallstreetbets | F | signature |  | H | F | 13 | F08 |  |
| warframe | A | signature |  |  | A | 21 | F01 | F02, F03, F21, F25 |
| wario | K |  |  |  |  | 0 |  |  |
| warriors | C | tie, nearest centre | C, H | H | A | 9 | F13 | F11 |
| warthunder | E | signature |  |  | E | 12 | F09 |  |
| watchmen | G | signature |  |  | G (thin) | 1 |  |  |
| weezer | A | signature |  | G | A | 15 | F18 | F17 |
| wholesomememes | C | signature |  | B | B | 24 | F01 | F27 |
| wildhockey | F | signature |  | E | F | 16 | F01 | F08, F09 |
| wine | G | signature |  |  | G | 8 | F19 | F17, F22, F33 |
| winnipegjets | A | signature |  | H | A | 8 |  |  |
| WisconsinBadgers | D | signature |  | B | D (thin) | 4 | F15 |  |
| witcher | A | signature |  |  | A | 13 | F27 | F31 |
| worldoftanks | F | tie, nearest centre | F, H | H | A | 14 | F02 | F01 |
| worldpowers | B | signature |  |  | B | 7 |  |  |
| wow | H | signature |  |  | H | 11 | F01 | F35 |
| WPI | F | tie, nearest centre | A, C, D, F | A, C, D | F (thin) | 3 | F08 | F10 |
| wsu | H | tie, nearest centre | F, H | F | H (thin) | 3 |  |  |
| xcom | C | signature |  |  | C | 14 | F30 |  |
| xenoblade_chronicles | A | signature |  |  | A | 14 |  |  |
| yerbamate | K |  |  |  |  | 0 |  |  |
| yogscast | G | signature |  |  | G | 9 | F19 | F01, F17, F22 |
| yugioh | E | signature |  |  | E | 17 | F03 | F01, F34 |
| yumenikki | C | tie, nearest centre | C, G |  | B | 6 |  |  |
| yuyuyu | G | signature |  | B | B | 7 |  |  |
| zelda | H | signature |  | F | H | 15 | F01 | F02, F03 |
| zootopia | F | signature |  |  | A | 15 | F08 | F17 |

