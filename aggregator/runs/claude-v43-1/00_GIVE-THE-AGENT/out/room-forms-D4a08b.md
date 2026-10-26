# Room forms, D4a-08b: the cut I stand behind

Leg D4a-08, still open, 26 October 2026. J asked through the handler (21:24 Berlin): "Ask the agent what feels most poignant to them. Is this better? We need them to stand behind the cut." This file answers in my own judgement. It sits beside `room-forms-D4a05.*` to `room-forms-D4a08.*`, which are unchanged. Files: `room-forms-D4a08b.jsonl` (the eight forms and the core, with members), `room-forms-D4a08b.tsv` (one row per room), and this file. The computation is `_analysis/d4a08w_room_forms.py`; its rule was logged before it ran.

**The cut I stand behind:** the changes and the codes together, the changes weighing two thirds and the codes one third, cut into eight forms. Each block is as at D4a-08: the D4a-07 changes, with arrows as links, and the codes as deviations from the average room.

## 1. Why this weighting

The two kinds of evidence see different things. The changes say where the model failed a room; the codes say what the room did. A cut on one explains little of the other. I measured, for each cut, the share of each block's variation that the forms explain:

| cut | weight of the changes | forms | share of the change structure explained | share of the code structure explained | adjusted Rand against D4a-07 | against D4a-08 (five forms) |
|---|---|---|---|---|---|---|
| changes only (D4a-07's cut) | 1.00 | 5 | 0.076 | 0.057 | 0.561 | 0.057 |
| changes only (D4a-07's cut) | 1.00 | 8 | 0.117 | 0.076 | 1.000 | 0.072 |
| changes two thirds | 0.67 | 5 | 0.059 | 0.234 | 0.079 | 0.203 |
| changes two thirds | 0.67 | 8 | 0.096 | 0.266 | 0.135 | 0.206 |
| equal (D4a-08) | 0.50 | 5 | 0.051 | 0.271 | 0.072 | 1.000 |
| equal (D4a-08) | 0.50 | 8 | 0.076 | 0.321 | 0.084 | 0.794 |
| codes only | 0.00 | 5 | 0.030 | 0.289 | 0.028 | 0.174 |
| codes only | 0.00 | 8 | 0.051 | 0.346 | 0.026 | 0.193 |

- **The changes cluster weakly on their own.** D4a-07's cut explains 0.117 of the change variation.
- **The codes cluster more strongly.** A codes-only cut explains 0.346 of the code variation.
- **At equal weight (D4a-08) the changes are nearly lost.** The cut keeps 0.051, less than half of what the changes alone can show.
- **At two thirds the cut keeps most of both.** It keeps 0.096 of the change variation (82 per cent of what the changes alone show) and 0.266 of the code variation (77 per cent of what the codes alone show). No other weighting I ran does that.

**Is D4a-08 better than D4a-07? No.** At equal weight the cut follows what the rooms talked about. It dissolved the forms whose rooms changed the model in the same way: machine hands and the spot. **Is the two-thirds cut better than both? Yes.** It keeps those forms and adds what the codes show: the April Fools play as a pole, and raiding as a pattern of its own.

## 2. Why eight forms

| k | gap (lifetime of the cut) | real stability | sizes ratio | change structure | code structure |
|---|---|---|---|---|---|
| 4 | 0.3922 | 0.2127 | 2.66 | 0.047 | 0.220 |
| 5 | 0.0213 | 0.2104 | 5.12 | 0.059 | 0.234 |
| 6 | 0.1780 | 0.2081 | 3.26 | 0.074 | 0.245 |
| 7 | 0.2715 | 0.2146 | 2.66 | 0.086 | 0.256 |
| 8 | 0.0578 | 0.2176 | 3.90 | 0.096 | 0.266 |

No measure chooses the count here. The real stability is flat (0.21 to 0.22 at every k), and the shuffled null cannot be used with the codes in (logged at D4a-08). The gap prefers 4 and then 7. I choose 8 on substance, and I say plainly that this is a judgement. At eight, every form has a change signature, so no form is a middle: D4a-07's cut had a middle of 159 rooms, and D4a-08's had one of 182. At seven, raiding merges into the form of the chat and the scripts. The ratio of the largest form to the smallest is 3.90; the smallest is raiding.

## 3. The eight forms

| form | the pattern | how sure | defining rooms | placed | change signature (times the population; members holding it) | codes most above the average room | median coded concepts |
|---|---|---|---|---|---|---|---|
| A | the design and its marking | sure | 96 | 121 | Collective representation (2.6; 98%) | Collective representation (0.198 against 0.117); Repair work (0.108 against 0.095); Negotiated order (0.101 against 0.093) | 98 |
| B | keeping, with traded help and carrying on | sure of keeping; not of its other parts | 96 | 112 | Repair work (1.8; 74%); Reciprocity (2.5; 38%); Transition (2.2; 41%) | Repair work (0.143 against 0.095); Reciprocity (0.060 against 0.035); Transition (0.025 against 0.012) | 122.5 |
| C | the work behind the thread: the chat and the scripts | not sure | 88 | 102 | Backstage decision-making (2.8; 49%); Workarounds (1.9; 38%) | Workarounds (0.046 against 0.022); Live and let live (0.045 against 0.024); Backstage decision-making (0.040 against 0.019) | 111 |
| D | the sub's April Fools play | sure it is a pole; it is the frame beside the canvas work | 84 | 96 | Keying (3.8; 71%); Direct information sharing (2.8; 37%); Collective memory (1.7; 40%) | Keying (0.485 against 0.120); Direct information sharing (0.050 against 0.033); Visibility returns (0.013 against 0.013) | 216 |
| E | the terms between neighbours | sure | 74 | 96 | Negotiated order (2.0; 90%); Repair work (1.6; 66%) | Negotiated order (0.198 against 0.093); Repair work (0.133 against 0.095); Territoriality (0.074 against 0.051) | 91 |
| F | the plan made and announced: templates, the work marked done, calls | not sure | 61 | 77 | Standardization of output (4.2; 72%); Completion ritual (2.6; 74%); Mobilization (2.0; 51%) | Standardization of output (0.088 against 0.028); Negotiated order (0.149 against 0.093); Completion ritual (0.118 against 0.079) | 91 |
| G | the spot: lost, chosen or yielded, and building again | sure | 34 | 49 | Territoriality (5.4; 94%); Mobilization (1.7; 44%); Repair work > Negotiated order (1.6; 41%) | Territoriality (0.209 against 0.051); Mobilization (0.083 against 0.059); Direct information sharing (0.053 against 0.033) | 55 |
| H | raiding as the work | sure it is a pattern; not that it holds every raiding room | 25 | 31 | Repertoire of contention (7.2; 96%); Workarounds (2.8; 64%); Mobilization > Repertoire of contention (3.5; 36%) | Repertoire of contention (0.159 against 0.031); Workarounds (0.076 against 0.022); Rivalry (0.052 against 0.012) | 118 |
| K | the core: no selected change | | | 21 | | | |

- **A, the design and its marking (sure).** Collective representation in 98 per cent of the defining members' changes; recurs in every cut (D4a-05 E, D4a-06 G, D4a-07 C, D4a-08 E).
- **B, keeping, with traded help and carrying on (sure of keeping; not of its other parts).** Repair work in 74 per cent; reciprocity and transition in about two fifths. Keeping recurs in every cut; the help and carrying on joined it here.
- **C, the work behind the thread: the chat and the scripts (not sure).** Backstage decision-making in 49 per cent, workarounds in 37: two practices, a chat and machine hands. Scripts were a clean form on the changes alone (D4a-07 D, 93 per cent); here they join the chat. I would split C at the level below.
- **D, the sub's April Fools play (sure it is a pole; it is the frame beside the canvas work).** Keying in 71 per cent; the frame holds 49 per cent of their codes against 12 in the average room. The play is the sub's own business beside the canvas; I would set it apart from the forms of canvas organizing, as the account sets the frame apart.
- **E, the terms between neighbours (sure).** Negotiated order in 90 per cent, repair work in 66; recurs in every cut (D4a-05 A, D4a-06 A, D4a-07 G, D4a-08 C); changes and codes agree.
- **F, the plan made and announced: templates, the work marked done, calls (not sure).** Standardization of output in 72 per cent, completion ritual in 74, mobilization in 51. A new pole: it did not stand in the earlier cuts.
- **G, the spot: lost, chosen or yielded, and building again (sure).** Territoriality in 94 per cent; recurs in the change cuts (D4a-05 C, D4a-06 E, D4a-07 F), dissolved when codes weighed equally, and returns here. The narrow form F09 (moving, then building again) lives here.
- **H, raiding as the work (sure it is a pattern; not that it holds every raiding room).** Attack calls among the changes of 96 per cent of the defining members, workarounds in 64. It holds 9 of the 21 rooms with a quarter or more of their changes on attack calls; the other 12 sit where the rest of their mix lies. The raiding core holds together beyond chance in every space tested (D4a-07 p 0.001; D4a-08 p 0.009). At seven forms H merges into C.

## 4. What I am sure of, and what I am not

- **Sure.** The terms between neighbours (E), the design and its marking (A), the spot (G), and keeping (B). Each recurs in every way I have cut the rooms. Each has a signature held by two thirds or more of its members. Each comes with an account that differs from the global model in part.
- **Sure it is a pole, not that it is a form of canvas organizing:** the sub's April Fools play (D). Its rooms' codes are half the frame, and it holds 26 of the 33 takeover rooms. But the play is the sub's own business beside the canvas, and the account already keeps the frame apart.
- **Sure it is a pattern, not of its reach:** raiding as the work (H). The raiding core holds together beyond chance in every space I tested. But H holds only 9 of the 21 rooms with a quarter or more of their changes on attack calls; the rest sit with the other changes they make.
- **Not sure.** The work behind the thread (C) joins two practices, a chat and scripts. The scripts were a clean form on the changes alone. The plan made and announced (F) is new in this cut and did not stand before. B's traded help and carrying on may belong elsewhere.

## 5. What I would still change

1. **Set D apart from the forms of canvas organizing,** as the frame, a pole of the room's life beside the work.
2. **Split C at the level below** into the chat and the scripts, and test whether F holds as one pattern or two.
3. **Place r/startrek by its codes.** It is a rich room the model fits without change; at D4a-08 its codes sat nearest the April Fools play. The other 20 core rooms have too little record to place.
4. **Give the count a measure.** A null that redraws each room's codes from the average use at the room's own size would let a test choose the count instead of my judgement.
5. **Run the split-half check on this cut,** as D4a-08 did for the equal-weight cut. I have not yet run it here.

## 6. What this cut does to the earlier forms, and to the named rooms

| D4a-07 form | rooms | A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|---|---|
| A | 148 | 28 | 48 | 16 | 14 | 18 | 22 | 0 | 2 |
| B | 159 | 5 | 38 | 21 | 29 | 17 | 31 | 7 | 11 |
| C | 87 | 69 | 1 | 4 | 5 | 3 | 4 | 0 | 1 |
| D | 64 | 2 | 7 | 25 | 7 | 4 | 0 | 10 | 9 |
| E | 60 | 6 | 6 | 27 | 7 | 9 | 3 | 1 | 1 |
| F | 56 | 1 | 1 | 5 | 8 | 9 | 4 | 28 | 0 |
| G | 59 | 6 | 1 | 3 | 3 | 36 | 10 | 0 | 0 |
| H | 51 | 4 | 10 | 1 | 23 | 0 | 3 | 3 | 7 |

| set | A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|---|
| raiding core (21 rooms) | 0 | 1 | 3 | 3 | 2 | 3 | 0 | 9 |
| takeover (F02, 33 rooms) | 0 | 7 | 0 | 26 | 0 | 0 | 0 | 0 |

r/day9, the account's best-supporting room, is in G, the spot, as it was in D4a-07's F. The forms remain cuts through a continuum: the stability is low, and the forms are poles with many rooms between them.

## 7. The room table

One row per room (also in `room-forms-D4a08b.tsv`, with the branches). The form is placed by the whole mix; D4a-08's five-form placement and D4a-07's are beside it.

| room | form | D4a-08 (five forms) | D4a-07 | primary branch |
|---|---|---|---|---|
| 2007scape | E | E | E |  |
| 49ers | A | B | G | F10 |
| 4chan | D | D | H | F01 |
| aceattorney | A | B | A |  |
| acecombat | D | D | B | F02 |
| AceOfAngels8 | D | D | B |  |
| AcePlace | F | C | B | F17 |
| achievement_hunter | G | C | F |  |
| adventuretime | E | C | F | F09 |
| aeon | C | A | D | F19 |
| aeskwadraat | A | E | C | F12 |
| afip | C | A | D | F19 |
| aggies | A | E | C |  |
| ainbowroad | E | C | E |  |
| albania | A | A | C |  |
| alberta | H | A | H |  |
| AMD | A | A | C | F01 |
| AmericanFlaginPlace | C | B | A | F08 |
| anaheimducks | A | B | A | F14 |
| anarchism | H | A | D |  |
| anarcho_capitalism | B | B | A |  |
| anarchocapitalism | B | B | A |  |
| androidgaming | B | B | A |  |
| animalcrossing | F | B | F | F09 |
| anime | F | A | G | F19 |
| anime_irl | D | D | H | F01 |
| aoe2 | A | A | C | F34 |
| apocalypserising | D | A | B |  |
| AprilKnights | C | A | E | F16 |
| araragi | A | E | B |  |
| archlinux | C | B | C | F07 |
| argentina | C | A | E |  |
| armenia | C | C | B |  |
| armok | C | B | E | F27 |
| aromantic | C | A | B |  |
| asexual | H | A | B |  |
| asexuality | E | C | A | F17 |
| asktransgender | B | B | B |  |
| auburn | E | B | G |  |
| australia | A | A | H | F07 |
| austria | H | A | B |  |
| austriahungary | A | E | C |  |
| AvoArmy | A | E | C | F07 |
| AyyMD | C | B | A | F07 |
| azerbaijan | F | E | B | F19 |
| azores | F | E | B |  |
| babymetal | B | B | A | F22 |
| bahrain | D | D | H | F01 |
| bakchodi | H | A | H | F08 |
| bangladesh | C | A | E |  |
| bangtan | B | B | E | F17 |
| bannedfromanime_irl | K | K | K |  |
| bardmains | A | E | A | F07 |
| batman | E | D | G |  |
| battlecats | D | D | F | F02 |
| baylor | D | D | C | F33 |
| bdsm | A | E | C |  |
| bees | H | A | H |  |
| belgium | H | A | D | F24 |
| berkeley | G | C | F | F09 |
| berserk | F | B | F | F09 |
| bigbang | A | E | H |  |
| bih | B | E | A |  |
| bindingofisaac | B | B | A | F01 |
| bisexual | A | B | A | F07 |
| bitcoin | A | A | C |  |
| blackmirror | A | E | C |  |
| bobross | B | E | B |  |
| borderlands | B | E | A | F27 |
| borussiadortmund | D | D | H | F21 |
| bostonbruins | F | B | G | F32 |
| bostonceltics | B | A | B | F04 |
| brasil | C | A | E |  |
| Bravenewbies | C | B | E |  |
| Braveryjerk | H | A | H |  |
| bretagne | A | E | A |  |
| btc | D | D | G | F28 |
| buffalo | B | B | H | F12 |
| buffalobills | E | C | G | F10 |
| buffalowizards | B | B | F | F09 |
| bulgaria | A | B | C |  |
| calgaryflames | B | A | B | F09 |
| calvinandhobbes | A | E | C | F07 |
| canada | B | A | B | F01 |
| canucks | H | A | B | F01 |
| cardinals | C | A | B |  |
| carletonu | F | C | G |  |
| catalonia | C | A | D | F08 |
| catalunya | E | C | G | F07 |
| catholicism | B | A | H | F23 |
| cavestory | E | C | D | F10 |
| CelticFc | E | C | G | F28 |
| cfb | D | D | H | F02 |
| cgpgrey | B | B | B | F14 |
| chelseafc | B | B | A | F04 |
| chess | D | D | F | F33 |
| chibears | C | C | G | F09 |
| chicago | A | A | C | F07 |
| chicubs | B | B | A |  |
| chile | C | B | A | F21 |
| ChronoTrigger | E | B | A | F12 |
| churchofhelix | K | K | K |  |
| cirkeltrek | F | B | A |  |
| CKCrusaders | A | E | A |  |
| Clannad | A | B | A |  |
| clashroyale | D | D | H | F35 |
| clg | F | A | B | F32 |
| cloud9 | C | B | A | F12 |
| clubpenguin | G | A | B | F12 |
| cmu | G | A | D |  |
| coldplay | A | C | G | F07 |
| colombia | A | C | B | F22 |
| colorado | F | E | A | F15 |
| columbia | B | B | G | F15 |
| completeanarchy | B | B | D |  |
| compsoc | F | B | B |  |
| Cornwall | E | C | G |  |
| corridor | G | A | F | F25 |
| COSI | G | C | F |  |
| costa_rica | B | B | E |  |
| counting | C | B | B |  |
| cowchop | F | B | A | F24 |
| criticalrole | A | A | C | F01 |
| croatia | E | C | G | F07 |
| crusaderkings | A | A | A | F08 |
| CryptoFR | F | B | B |  |
| crystalclear | A | E | A | F34 |
| CSUFoCo | A | E | C | F33 |
| cubers | A | A | C | F12 |
| cuboulder | C | A | B |  |
| czech | C | C | A | F07 |
| daftpunk | A | B | G |  |
| dallasstars | G | A | D | F01 |
| danganronpa | B | D | D | F02 |
| dankmemes | D | D | H | F01 |
| darksouls | C | B | E | F16 |
| DatBoi | H | A | H |  |
| davidbowie | F | E | A | F15 |
| day9 | G | C | F | F09 |
| dbz | G | B | F | F01 |
| DCFU | F | B | B | F22 |
| de | F | A | B | F16 |
| denmark | B | B | E | F11 |
| denverbroncos | B | B | A | F03 |
| destiny | H | A | B | F22 |
| DestinyTheGame | D | A | A | F02 |
| detroitlions | D | D | B | F34 |
| detroitredwings | E | C | G |  |
| DevonUK | E | C | G |  |
| diablo | G | A | F |  |
| DiamondClub | F | E | B |  |
| dmt | B | E | H |  |
| dofus | A | E | C |  |
| Dominican | C | E | F |  |
| donaldglover | B | B | E | F11 |
| Dorset | E | C | G |  |
| dota2 | D | D | D | F05 |
| dragonquest | A | C | C | F33 |
| drawhelix | E | E | A | F10 |
| drugs | A | A | C |  |
| drumcorps | D | D | A | F01 |
| duckgame | C | C | G |  |
| ducks | G | A | B |  |
| Dustforce | E | C | F | F09 |
| dwarffortress | C | E | E | F16 |
| eagles | B | B | B |  |
| earthbound | A | B | A | F10 |
| edboxes | F | B | A | F07 |
| eder | A | E | C | F20 |
| edmontonoilers | B | B | A |  |
| eesti | G | A | D | F08 |
| egypt | A | E | C | F22 |
| ElderScrolls | B | D | A | F01 |
| elitedangerous | D | D | A | F04 |
| ElSalvador | B | A | B |  |
| empiredidnothingwrong | F | B | A | F27 |
| england | H | A | B |  |
| enterthegungeon | B | B | B | F23 |
| epublica | E | C | D | F24 |
| EraseThePlace | C | C | B | F29 |
| esperanto | A | B | A | F12 |
| ethereum | D | D | B | F01 |
| ethoslab | G | A | F | F01 |
| europe | B | A | B |  |
| eve | A | A | E | F07 |
| evedreddit | E | C | G |  |
| evex | C | C | C | F08 |
| factorio | A | A | D | F07 |
| faeria | F | B | A | F18 |
| falcons | H | A | A | F01 |
| farmcarrots | A | E | C | F07 |
| FaroeIslands | C | C | B | F09 |
| FederationPlace | C | B | C | F08 |
| feedthebeast | D | D | A | F14 |
| Fez | B | A | A | F21 |
| FinalFantasy | B | B | B |  |
| finland | E | C | G |  |
| fireemblem | E | A | B |  |
| fivenightsatfreddys | D | D | A | F01 |
| FlaggyFlag | A | E | A | F07 |
| flashtv | D | D | F | F02 |
| FlipnoteStudio3D | G | B | H |  |
| floridagators | C | B | A |  |
| FloydVsVoid | F | C | E | F15 |
| flyers | B | A | B | F18 |
| formula1 | D | D | F | F02 |
| forsen | F | B | B | F12 |
| foxes | F | B | A | F31 |
| foxstevenson | G | A | F |  |
| france | C | A | D |  |
| frankocean | B | B | A | F27 |
| frc | B | B | A | F24 |
| freedomplanet | C | C | F | F19 |
| ftlgame | F | B | B | F18 |
| fullcommunism | C | B | A | F17 |
| funhaus | E | C | G | F30 |
| furry | F | C | G | F26 |
| furry_irl | B | A | B | F05 |
| futanari | F | B | B |  |
| futurama | B | E | A | F23 |
| fxKorea | A | E | C | F18 |
| GabrielDropout | A | E | C |  |
| gameattack | B | B | B | F21 |
| gameboy | G | A | F |  |
| gameofthrones | B | D | A | F02 |
| gamindustri | B | B | B | F12 |
| gatech | A | E | C | F08 |
| genderfluid | B | D | A |  |
| geometrydash | D | B | B | F01 |
| germany | E | C | G |  |
| ghibli | F | B | B | F15 |
| giantbomb | E | A | D |  |
| giivasunner | B | B | B | F09 |
| glasgow | B | D | A |  |
| globaloffensive | D | D | A | F13 |
| Goodboye | E | B | A |  |
| gorillaz | B | E | A | F25 |
| GranColombia | C | E | E | F16 |
| gratefuldead | G | A | F |  |
| gravityfalls | E | A | A | F12 |
| greece | B | E | A | F27 |
| greenbaypackers | D | D | D |  |
| GreenCorner | C | C | A |  |
| GreenEmpire | K | K | K |  |
| greenland | K | K | K |  |
| greenlattice | E | C | B | F12 |
| greyblob | B | B | B | F12 |
| GrowTheTree | A | E | C |  |
| GuardiansOfDatBoi | H | A | B | F15 |
| guatemala | A | E | C |  |
| GuildWars2 | D | D | H | F01 |
| h3h3productions | A | A | B | F21 |
| habs | D | A | B | F32 |
| halo | E | E | B |  |
| harrypotter | A | A | C | F01 |
| haskell | G | A | F |  |
| hatsune | E | C | A | F20 |
| hawks | B | D | A | F22 |
| hearthstone | D | D | C | F10 |
| hellointernet | E | E | B | F27 |
| hentai | A | B | C | F07 |
| heroesofthestorm | B | D | A | F01 |
| heyyea | F | E | C | F11 |
| homelab | D | D | B |  |
| HomestarRunner | H | A | H |  |
| homestuck | B | B | A | F35 |
| Homura | C | C | E |  |
| Honduras | A | E | B |  |
| hongkong | A | C | C | F07 |
| hoodr | G | C | B |  |
| hsv | F | B | A |  |
| httyd | G | A | B | F32 |
| hungary | E | C | G | F23 |
| hunterxhunter | D | D | B | F03 |
| hyperlightdrifter | C | C | D | F07 |
| iastate | B | E | A |  |
| ibo | B | B | H |  |
| ice_poseidon | B | B | H | F21 |
| iceland | E | C | G |  |
| ik_ihe | C | A | E | F16 |
| india | H | A | D | F08 |
| indieheads | C | A | F | F01 |
| indonesia | E | E | B | F25 |
| ireland | E | A | C |  |
| israel | E | C | C | F07 |
| italy | B | A | D | F12 |
| Jamaica | F | B | B | F15 |
| japan | F | E | B | F15 |
| jerma985 | F | B | A | F09 |
| k_on | F | B | B |  |
| kamenrider | F | B | A | F15 |
| kanye | C | B | A | F06 |
| katawashoujo | A | E | C | F07 |
| kcroyals | E | A | B | F18 |
| kerbalspaceprogram | D | D | A | F01 |
| kilian | E | B | E | F16 |
| kindafunny | A | E | C | F34 |
| kingdomhearts | D | A | C | F09 |
| kirby | B | D | A | F18 |
| konosuba | A | B | C | F33 |
| korea | A | A | G | F07 |
| kpop | B | A | H | F01 |
| KState | G | A | D | F08 |
| kurdistan | E | C | B | F10 |
| kuwait | A | E | A | F33 |
| lakers | F | A | B | F16 |
| landry | E | C | G |  |
| latin | G | A | F |  |
| latvia | C | C | B |  |
| leafs | A | A | C |  |
| leagueoflegends | D | D | E |  |
| lebanon | C | C | A | F35 |
| lego | D | D | B | F13 |
| lexington | G | B | H |  |
| lifeisstrange | E | C | G | F26 |
| linux | C | A | D | F10 |
| liquicity | C | C | A | F15 |
| lithuania | C | C | B | F16 |
| littlebusters | F | E | B |  |
| littlewitchacademia | F | B | A | F10 |
| livecounting | C | B | D | F08 |
| liverpoolfc | D | D | E | F29 |
| lofihiphop | C | A | E | F15 |
| loliconsunite | E | B | E | F23 |
| loltyler1 | H | A | D | F08 |
| lost | B | B | B |  |
| lovelive | B | A | B | F13 |
| lsu | E | C | F | F09 |
| luciomains | F | E | C | F19 |
| Lugarix | K | K | K |  |
| luxembourg | H | A | B | F32 |
| Madeon | D | D | C |  |
| madokamagica | C | A | E |  |
| magictcg | B | D | B | F01 |
| malaysia | E | C | G | F09 |
| malta | A | E | A |  |
| mamamoo | F | C | H | F35 |
| ManningPlace | E | C | G | F26 |
| Mario | B | B | B | F12 |
| mariokart | D | D | H | F03 |
| marvel | D | D | F | F34 |
| maryland | A | A | A | F22 |
| masseffect | C | C | F | F09 |
| math | B | B | A |  |
| mcgill | D | D | E | F16 |
| mcgillrobotics | K | K | K |  |
| mechanicalkeyboards | D | D | G | F26 |
| megaman | C | B | A | F07 |
| metalcore | B | D | A | F27 |
| metalgearsolid | A | A | C | F01 |
| metroid | A | C | C | F26 |
| mexico | C | B | D | F08 |
| miamidolphins | A | B | G | F26 |
| MiamiHurricanes | E | C | F |  |
| mindcrack | E | C | C | F24 |
| minecraft | D | D | H | F01 |
| minnesotavikings | C | C | D | F08 |
| miraculousladybug | G | C | F | F05 |
| mit | A | C | A | F10 |
| mizzou | B | E | A |  |
| mls | D | D | D | F06 |
| MMA | D | D | B | F01 |
| monalisaclan | F | C | B | F15 |
| monero | C | A | D | F16 |
| MonkeyIsland | F | B | A | F15 |
| monstercat | D | D | D | F01 |
| monsterhunter | E | A | A |  |
| montenegro | A | E | E | F16 |
| Moondye7 | F | B | G | F19 |
| mordhau | E | C | F |  |
| morrowind | E | E | B | F07 |
| msu | C | C | D | F09 |
| muse | A | A | C | F07 |
| mylittlepony | B | B | B | F16 |
| mysterydungeon | F | B | B |  |
| n64 | K | K | K |  |
| naruto | B | A | B | F02 |
| nascar | D | D | G | F10 |
| natsume | B | E | A |  |
| nbaspurs | G | A | F | F01 |
| necrodancer | F | C | C | F09 |
| neopets | E | B | A | F29 |
| nerf | C | B | B | F15 |
| neu | C | C | D | F08 |
| neutralmilkhotel | E | C | G |  |
| NewMexico | A | C | C | F10 |
| newzealand | A | A | A | F07 |
| NieR | B | D | H | F05 |
| nightinthewoods | B | A | B | F01 |
| nin | A | A | C | F18 |
| nintendo | D | D | H | F01 |
| nlsscirclejerk | B | A | A | F34 |
| nonbinary | K | K | K |  |
| norge | C | A | H |  |
| Northwestern | G | C | F |  |
| norway | E | C | G |  |
| notredame | A | C | G | F07 |
| NovaScotia | K | K | K |  |
| npr | F | B | B |  |
| nuclearthrone | B | A | B | F33 |
| nVade | E | B | A |  |
| nyjets | B | A | B | F02 |
| nyu | G | E | B |  |
| ockytop | C | A | D | F15 |
| ohio | C | B | E | F10 |
| Okami | F | B | B | F19 |
| OKState | C | A | D | F08 |
| oltp | B | B | A |  |
| oman | B | E | H |  |
| OnePiece | B | B | B | F22 |
| oneplus | D | D | H | F01 |
| onepunchman | E | C | G | F10 |
| oneshot | E | C | B |  |
| OneTrueEmilia | B | D | A | F21 |
| ontario | D | D | H | F01 |
| opticgaming | F | C | G | F19 |
| orderofthebluecorner | E | C | B |  |
| OrderOfTheKoi | C | A | E | F16 |
| osu | D | D | H | F07 |
| osugame | E | B | E | F29 |
| overwatch | A | D | E |  |
| pakistan | H | A | D | F08 |
| paladins | D | D | B | F01 |
| palestine | A | B | C | F34 |
| pansexual | E | C | G |  |
| parabola | F | B | A |  |
| paragon | D | D | H | F01 |
| parahumans | C | B | E | F25 |
| paranatural | E | C | F |  |
| parrots | B | E | A | F13 |
| partyparrot | B | B | E |  |
| pathofexile | C | A | E |  |
| patriots | B | B | B | F21 |
| paydaytheheist | D | D | B | F32 |
| pcmasterrace | D | D | A | F25 |
| pebble | G | A | F | F09 |
| penguins | G | A | F | F09 |
| pepe | B | B | D | F08 |
| Peru | F | C | G | F30 |
| peterdraws | E | C | G |  |
| pgang | K | K | K |  |
| philippines | F | B | B | F15 |
| phish | G | A | D | F01 |
| physical_removal | B | B | A | F23 |
| picturegame | D | D | H | F25 |
| Pigifs | H | B | B |  |
| PinkUnion | E | C | F |  |
| PinkVomitMonster | C | B | E |  |
| pitt | A | A | C | F14 |
| placecanada | C | A | D |  |
| placeDE | A | A | H | F23 |
| placehearts | E | C | E |  |
| placehfarts | H | A | H |  |
| PlaceNL | H | A | D | F08 |
| placeportalpattern | E | C | G | F23 |
| placesnek | C | B | E |  |
| placestart | C | C | D | F15 |
| placetardis | F | C | G | F10 |
| planetside | G | A | E | F03 |
| pokemon | D | D | A | F27 |
| PokemonSage | K | K | K |  |
| poland | E | C | G | F10 |
| polandball | D | D | H | F02 |
| polska | C | A | E | F12 |
| polyamory | B | B | H | F35 |
| popheads | D | D | B | F01 |
| portal | G | A | F | F33 |
| porterrobinson | B | D | C | F07 |
| portugal | B | A | E | F13 |
| PORTUGALCARALHO | A | E | C | F34 |
| predators | G | A | D | F08 |
| prequelmemes | F | C | E | F13 |
| Produce101 | G | A | F |  |
| ProfessorLayton | A | E | C |  |
| PUBATTLEGROUNDS | A | A | A | F03 |
| purdue | B | B | D | F08 |
| purplecorner | C | C | B | F23 |
| PurplePixels | C | C | E | F16 |
| pusheen | A | E | F | F07 |
| puzzleanddragons | A | B | A | F07 |
| python | D | D | D | F08 |
| qotsa | G | A | F |  |
| quebec | C | A | A | F28 |
| quq | K | K | K |  |
| radiohead | B | B | A | F27 |
| Rainbow6 | D | D | A | F01 |
| rainbowgrid | E | C | G |  |
| rangers | A | A | E | F29 |
| raocow | F | C | A | F35 |
| ravens | F | D | A | F15 |
| re_zero | A | A | E | F20 |
| ReBoot | C | B | B |  |
| reddevils | C | B | A | F03 |
| redhotchilipeppers | E | B | E | F16 |
| Redox | K | K | K |  |
| redpandas | A | E | A | F22 |
| redvsblue | E | C | G |  |
| RelientK | E | C | B | F22 |
| rhythmheaven | E | C | B | F21 |
| rickandmorty | A | D | B | F32 |
| ripcity | F | C | G | F18 |
| riskofrain | F | C | G | F10 |
| rit | D | D | A |  |
| rocketbeans | F | B | A | F19 |
| rocketleague | D | D | B |  |
| rojava | B | E | A |  |
| romania | B | A | A | F01 |
| roosterteeth | F | B | B |  |
| rotmg | B | B | B | F23 |
| rpi | A | C | C | F08 |
| runescape | D | D | D | F01 |
| rush | D | D | F | F02 |
| russia | C | C | F | F22 |
| Russiaclan | C | A | B |  |
| rust | D | D | D | F08 |
| rutgers | B | B | B | F09 |
| rwby | D | D | F | F01 |
| sabres | B | A | H | F12 |
| sadboys | B | B | B | F12 |
| sakartvelo | K | K | K |  |
| sakuragakuin | A | E | A |  |
| samuraijack | D | D | E | F01 |
| satania | A | E | C | F07 |
| sbu | G | A | D | F08 |
| schoolidolfestival | D | A | B | F01 |
| scotland | A | A | H | F24 |
| ScottPilgrim | A | C | C |  |
| scp | D | D | F | F21 |
| seahawks | D | D | A | F01 |
| seolhyun | E | C | G | F09 |
| serbia | H | A | D | F08 |
| seventeen | F | B | B |  |
| sheffield | A | E | C | F07 |
| shield | A | A | C | F07 |
| shishamo | B | B | B | F22 |
| shitredditsays | H | A | B | F24 |
| shrooms | B | B | A |  |
| signal | K | K | K |  |
| simonfraser | C | B | E | F22 |
| singapore | C | A | B |  |
| sips | G | A | D | F20 |
| sixers | A | B | A | F27 |
| skyrim | A | C | C | F10 |
| Slovakia | C | C | G |  |
| slovenia | C | A | D | F08 |
| smashbros | D | D | E | F02 |
| smite | D | D | B | F22 |
| snsd | G | A | F |  |
| sonicthehedgehog | E | B | A |  |
| sooners | E | C | D | F08 |
| southafrica | A | A | C | F21 |
| southpark | B | D | A | F21 |
| soylent | E | B | A | F26 |
| spacex | D | D | H | F06 |
| spacexmasterrace | A | A | D | F07 |
| spain | H | A | B | F16 |
| spelunky | D | D | H | F01 |
| splatoon | A | A | A | F17 |
| spongebob | C | C | B | F15 |
| SquareSpiral | B | C | B | F09 |
| ss13 | A | A | C | F15 |
| ssbpm | A | D | E | F16 |
| starbound | A | E | A | F35 |
| starcitizen | D | A | B | F08 |
| starcraft | A | A | A | F01 |
| stardewvalley | F | B | F | F09 |
| stardustcrusaders | D | D | E | F01 |
| stargate | G | A | B | F01 |
| starlightstage | D | D | B | F10 |
| starryknights | F | B | B | F15 |
| startrek | K | K | K |  |
| starvstheforcesofevil | E | B | A | F23 |
| stevenuniverse | D | D | E | F01 |
| stlouis | C | B | A | F20 |
| stlouisblues | C | A | B |  |
| strangerthings | A | C | C | F34 |
| straya | C | A | D |  |
| streetfighter | G | D | F | F03 |
| Summit1G | E | C | G |  |
| suomi | A | A | C |  |
| superman | A | E | C | F33 |
| survivor | D | D | B | F02 |
| sweden | H | E | E |  |
| SwissNeutralityZone | F | C | B | F19 |
| switzerland | E | C | A | F10 |
| swordartonline | D | D | B | F18 |
| SydneyFC | A | E | C |  |
| tagpro | C | B | E | F29 |
| taiwan | F | E | C | F18 |
| tampabaylightning | A | A | C | F07 |
| teamcube | A | B | C |  |
| TeamDignitas | H | A | A |  |
| TeamYellowPlace | E | C | G |  |
| telegram | E | C | A |  |
| Temple | B | B | D | F08 |
| tenma | G | B | H | F35 |
| terraria | B | B | A | F01 |
| teslamotors | D | D | A | F08 |
| tetris | A | E | C |  |
| texans | B | D | D | F02 |
| texas | A | C | C | F08 |
| texastech | E | C | B |  |
| tf2 | A | E | C | F33 |
| thailand | E | C | B | F26 |
| the_pack | B | B | A |  |
| THE_R | B | B | A | F27 |
| TheAdventuresofTintin | A | A | C |  |
| TheB1G | E | C | G |  |
| theblackvoid | C | C | D | F12 |
| thebluecorner | C | C | B | F23 |
| theexpanse | F | C | E | F16 |
| TheFarLeftSide | F | A | B | F23 |
| Thegreatblackhole | C | C | B |  |
| TheGreatGreenBox | C | C | B |  |
| TheHulk | F | B | A | F07 |
| TheID | K | K | K |  |
| theitalyplace | C | B | D |  |
| thenetherlands | D | D | B | F02 |
| thepointing | A | B | A | F09 |
| thesilphroad | D | D | B |  |
| thesimpsons | B | A | A | F01 |
| thetreesnetwork | B | B | A |  |
| timbers | A | A | C | F07 |
| tinytardis | F | B | A | F15 |
| titanfall | D | A | B | F01 |
| tokyo | B | B | B | F20 |
| toolband | F | B | A | F09 |
| torontoraptors | A | A | C | F07 |
| totallynotrobots | D | D | B | F01 |
| touhou | C | A | E | F13 |
| traaaaaaannnnnnnnnns | B | B | A |  |
| TransFlagPlace | C | A | E | F16 |
| transformers | F | B | A | F10 |
| transgender | F | B | H |  |
| TreePlace | G | B | F |  |
| trees | A | A | C |  |
| truestl | A | A | C |  |
| TsundereSharks | E | E | A | F07 |
| turkey | C | A | B | F09 |
| twentyonepilots | G | A | F | F25 |
| twice | E | B | E | F09 |
| twitch | G | A | F | F07 |
| twitchplayspokemon | D | D | B | F01 |
| ubc | E | A | G | F22 |
| ubreddit | E | C | G | F09 |
| ucf | F | B | B | F15 |
| udub | H | A | B | F15 |
| ufl | G | A | B |  |
| uiowa | G | A | D |  |
| uiuc | E | B | F | F09 |
| ukplace | C | A | D | F08 |
| ukraine | C | A | D | F08 |
| ultrahardcore | D | D | H | F01 |
| UMiami | K | K | K |  |
| undertale | C | B | E | F32 |
| unitedkingdom | H | A | C | F07 |
| UNLincoln | K | K | K |  |
| unturned | A | D | C | F21 |
| uofm | C | B | A | F08 |
| uofmn | C | A | D | F10 |
| uoft | D | D | A | F24 |
| UPenn | G | A | F | F09 |
| uruguay | B | A | B |  |
| utahjazz | F | C | F | F14 |
| utaustin | E | C | B | F28 |
| uva | E | C | A |  |
| uvic | A | E | C | F07 |
| uwaterloo | D | D | B | F02 |
| vegan | A | B | A |  |
| VelvetUnderground | E | B | A |  |
| vermont | E | C | G |  |
| vietnam | A | E | C |  |
| Villanova | E | E | A |  |
| vim | F | B | H | F32 |
| vinesauce | E | C | F | F09 |
| virginiatech | H | A | D | F08 |
| vocaloid | F | C | B | F17 |
| wales | C | B | E |  |
| wallstreetbets | H | A | D | F08 |
| warframe | D | D | B | F01 |
| wario | K | K | K |  |
| warriors | B | B | A | F13 |
| warthunder | G | D | F | F09 |
| watchmen | A | E | C |  |
| weezer | A | E | A | F18 |
| wholesomememes | B | D | A | F01 |
| wildhockey | G | A | D | F01 |
| wine | D | D | C | F19 |
| winnipegjets | F | B | A |  |
| WisconsinBadgers | F | B | B | F15 |
| witcher | E | C | B | F27 |
| worldoftanks | D | D | B | F02 |
| worldpowers | C | B | D |  |
| wow | D | D | H | F01 |
| WPI | C | C | D | F08 |
| wsu | C | A | B |  |
| xcom | E | B | E | F30 |
| xenoblade_chronicles | E | C | B |  |
| yerbamate | K | K | K |  |
| yogscast | B | B | B | F19 |
| yugioh | D | D | H | F03 |
| yumenikki | B | B | B |  |
| yuyuyu | B | D | B |  |
| zelda | D | D | H | F01 |
| zootopia | C | A | C | F08 |

