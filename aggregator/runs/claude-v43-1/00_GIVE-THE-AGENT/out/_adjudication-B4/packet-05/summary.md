# Packet 5, the figures (stage B4 section 9)

Written by `out/_analysis/b4_packet_summary.py` from `disagreements.jsonl`. Items ruled: 409.

## The taxonomy split

The next table counts the packet's rulings by taxonomy value, overall and by J's class of the item.

| taxonomy | all | class 3 | class 4 | class 5 |
|---|---|---|---|---|
| scheme-ambiguous | 14 | 13 | 1 | 0 |
| item-is-a-bag | 3 | 2 | 1 | 0 |
| reader-error | 16 | 16 | 0 | 0 |
| author-error | 41 | 0 | 41 | 0 |
| genuine-joint | 291 | 291 | 0 | 0 |
| author-disagrees | 44 | 0 | 43 | 1 |
| total | 409 | 322 | 86 | 1 |

- unresolved: 3 (0.7%)
- named_neither: 131 (32.0%)
- author-error: 41; author-disagrees: 44
- rulings corrected in place after writing: 9 (Thegreatblackhole t06, sonicthehedgehog t04, aceattorney t09, AMD t13, archlinux t03, armenia t04, belgium t11, bindingofisaac t05, theitalyplace t11)

## Fields by ambiguity

The next list counts the scheme-ambiguous rulings by the field whose sentence failed to decide.

- must_show: 2
- must_not_show: 8
- decide_when_both: 0
- discriminators: 4

## Third-order themes by ambiguity

The next table ranks the themes whose sentence failed to decide, with the fields.

| theme | rulings | must_show | must_not_show | decide_when_both | discriminators |
|---|---|---|---|---|---|
| T3-006 | 5 | 0 | 1 | 0 | 4 |
| T3-137 | 1 | 0 | 1 | 0 | 0 |
| T3-058 | 1 | 1 | 0 | 0 | 0 |
| T3-150 | 1 | 0 | 1 | 0 | 0 |
| T3-010 | 1 | 1 | 0 | 0 | 0 |
| T3-046 | 1 | 0 | 1 | 0 | 0 |
| T3-194 | 1 | 0 | 1 | 0 | 0 |
| T3-078 | 1 | 0 | 1 | 0 | 0 |
| T3-013 | 1 | 0 | 1 | 0 | 0 |
| T3-115 | 1 | 0 | 1 | 0 | 0 |

## Boundary pairs and their items

Each pair below is carried in `boundary_ruling` on the items listed. "Paragraph" says whether `boundaries.md` holds the pair's paragraph.

- **T3-010|T3-149** (34 items; paragraph yes; genuine-joint 29, author-error 3, reader-error 2): Thegreatblackhole t06, AMD t13, archlinux t03, bindingofisaac t05, detroitlions t06, edboxes t04, faeria t04, FederationPlace t04, finland t02, forsen t03, gravityfalls t05, liverpoolfc t14, newzealand t05, phish t04, placeportalpattern t04, prequelmemes t08, singapore t08, ss13 t09, switzerland t03, teslamotors t10, uiuc t11, uoft t10, worldoftanks t07, cowchop t02, buffalo t04, czech t07, neopets t04, overwatch t19, placesnek t03, soylent t02, sweden t03, titanfall t07, VelvetUnderground t04, colombia t03
- **T3-010|T3-151** (31 items; paragraph yes; genuine-joint 26, author-disagrees 3, author-error 2): belgium t11, catalunya t05, chicago t10, chicubs t05, chile t04, Dorset t02, ElSalvador t02, europe t03, factorio t10, ftlgame t03, gameofthrones t13, hearthstone t13, kamenrider t04, littlewitchacademia t05, mls t10, Moondye7 t05, notredame t04, placestart t08, purdue t06, rwby t07, smashbros t08, timbers t03, unturned t05, uwaterloo t07, giivasunner t10, httyd t10, india t04, mylittlepony t07, placecanada t05, southafrica t04, theitalyplace t11
- **T3-010|T3-024** (26 items; paragraph yes; genuine-joint 26): 49ers t05, cirkeltrek t08, geometrydash t08, monsterhunter t04, PurplePixels t05, starcraft t10, TeamYellowPlace t02, asktransgender t03, python t08, aceattorney t09, armenia t04, bisexual t05, czech t06, esperanto t06, GrowTheTree t03, oneshot t03, PlaceNL t07, starbound t04, terraria t03, TransFlagPlace t02, babymetal t05, Fez t06, roosterteeth t05, stardustcrusaders t06, taiwan t06, theexpanse t04
- **T3-006|T3-061** (18 items; paragraph yes; genuine-joint 14, scheme-ambiguous 4): borderlands t05, armenia t05, brasil t05, cirkeltrek t07, ireland t06, newzealand t04, overwatch t25, ukraine t03, utaustin t03, wallstreetbets t06, costa_rica t03, kurdistan t02, polska t05, purdue t08, stlouis t04, thailand t06, PlaceNL t06, teamcube t02
- **T3-010|T3-011** (14 items; paragraph yes; genuine-joint 12, author-error 1, author-disagrees 1): sonicthehedgehog t04, cloud9 t09, formula1 t10, masseffect t05, minnesotavikings t12, pathofexile t11, samuraijack t03, sixers t06, transformers t06, Clannad t05, heroesofthestorm t10, nyjets t11, placeDE t04, quebec t04

## Agreement before and after

Before is the two readers against each other over the packet's 409 items. After is each reader against the ruling over the 406 items not unresolved. The figure after is not a reliability figure: it is agreement with an adjudication I performed.

| | mean Jaccard | primary match |
|---|---|---|
| before (reader against reader) | 0.467 | 0.623 |
| after (each reader against the ruling) | 0.612 | 0.677 |

## Stage B2's predicted pairs

The next list gives, for each of `confusions.md`'s nineteen pairs, the packet's items whose two readers put the pair's themes as their primaries.

- pair 1, T3-005|T3-021: 0
- pair 2, T3-010|T3-149: 10
- pair 3, T3-001|T3-023: 0
- pair 4, T3-028|T3-070: 0
- pair 5, T3-004|T3-020: 0
- pair 6, T3-002|T3-033: 0
- pair 7, T3-015|T3-075: 0
- pair 8, T3-004|T3-070: 0
- pair 9, T3-009|T3-073: 0
- pair 10, T3-004|T3-038: 0
- pair 11, T3-010|T3-151: 7
- pair 12, T3-010|T3-150: 1
- pair 13, T3-010|T3-024: 17
- pair 14, T3-009|T3-043: 0
- pair 15, T3-001|T3-095: 0
- pair 16, T3-087|T3-188: 0
- pair 17, T3-044|T3-082: 0
- pair 18, T3-014|T3-152: 0
- pair 19, T3-015|T3-063: 0

The packet's ten commonest primary splits, predicted or not:

- T3-010|T3-024: 17 (predicted)
- T3-010|T3-149: 10 (predicted)
- T3-006|T3-061: 8
- T3-010|T3-011: 7
- T3-010|T3-151: 7 (predicted)
- T3-006|T3-068: 4
- T3-011|T3-084: 4
- T3-010|T3-035: 3
- T3-011|T3-151: 3
- T3-005|T3-006: 2

## Unresolved items

- linux t03: scheme-ambiguous, T3-137 must_not_show
- survivor t26: scheme-ambiguous, T3-058 must_show
- PurplePixels t13: author-disagrees,  

