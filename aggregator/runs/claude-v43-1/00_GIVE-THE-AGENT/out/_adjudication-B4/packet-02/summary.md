# Packet 2, the figures (stage B4 section 9)

Written by `out/_analysis/b4_packet_summary.py` from `disagreements.jsonl`. Items ruled: 447.

## The taxonomy split

The next table counts the packet's rulings by taxonomy value, overall and by J's class of the item.

| taxonomy | all | class 3 | class 4 | class 5 |
|---|---|---|---|---|
| scheme-ambiguous | 62 | 62 | 0 | 0 |
| item-is-a-bag | 44 | 36 | 8 | 0 |
| reader-error | 3 | 3 | 0 | 0 |
| author-error | 58 | 2 | 53 | 3 |
| genuine-joint | 215 | 215 | 0 | 0 |
| author-disagrees | 65 | 0 | 63 | 2 |
| total | 447 | 318 | 124 | 5 |

- unresolved: 10 (2.2%)
- named_neither: 155 (34.7%)
- author-error: 58; author-disagrees: 65
- rulings corrected in place after writing: 2 (bindingofisaac t02, clashroyale t02)

## Fields by ambiguity

The next list counts the scheme-ambiguous rulings by the field whose sentence failed to decide.

- must_show: 33
- must_not_show: 6
- decide_when_both: 6
- discriminators: 17

## Third-order themes by ambiguity

The next table ranks the themes whose sentence failed to decide, with the fields.

| theme | rulings | must_show | must_not_show | decide_when_both | discriminators |
|---|---|---|---|---|---|
| T3-002 | 12 | 0 | 2 | 3 | 7 |
| T3-033 | 9 | 9 | 0 | 0 | 0 |
| T3-014 | 6 | 1 | 0 | 0 | 5 |
| T3-062 | 3 | 1 | 0 | 0 | 2 |
| T3-152 | 2 | 2 | 0 | 0 | 0 |
| T3-104 | 2 | 2 | 0 | 0 | 0 |
| T3-091 | 2 | 0 | 0 | 0 | 2 |
| T3-016 | 2 | 1 | 0 | 0 | 1 |
| T3-107 | 1 | 1 | 0 | 0 | 0 |
| T3-153 | 1 | 1 | 0 | 0 | 0 |
| T3-015 | 1 | 1 | 0 | 0 | 0 |
| T3-090 | 1 | 1 | 0 | 0 | 0 |
| T3-044 | 1 | 1 | 0 | 0 | 0 |
| T3-196 | 1 | 1 | 0 | 0 | 0 |
| T3-084 | 1 | 1 | 0 | 0 | 0 |
| T3-065 | 1 | 0 | 0 | 1 | 0 |
| T3-082 | 1 | 0 | 0 | 1 | 0 |
| T3-070 | 1 | 1 | 0 | 0 | 0 |
| T3-004 | 1 | 1 | 0 | 0 | 0 |
| T3-124 | 1 | 1 | 0 | 0 | 0 |
| T3-074 | 1 | 1 | 0 | 0 | 0 |
| T3-021 | 1 | 1 | 0 | 0 | 0 |
| T3-059 | 1 | 0 | 1 | 0 | 0 |
| T3-018 | 1 | 1 | 0 | 0 | 0 |
| T3-117 | 1 | 0 | 1 | 0 | 0 |
| T3-036 | 1 | 0 | 1 | 0 | 0 |
| T3-043 | 1 | 1 | 0 | 0 | 0 |
| T3-073 | 1 | 1 | 0 | 0 | 0 |
| T3-136 | 1 | 0 | 0 | 1 | 0 |
| T3-170 | 1 | 1 | 0 | 0 | 0 |
| T3-148 | 1 | 0 | 1 | 0 | 0 |
| T3-137 | 1 | 1 | 0 | 0 | 0 |

## Boundary pairs and their items

Each pair below is carried in `boundary_ruling` on the items listed. "Paragraph" says whether `boundaries.md` holds the pair's paragraph.

- **T3-002|T3-033** (20 items; paragraph yes; genuine-joint 6, scheme-ambiguous 5, author-disagrees 4, author-error 4, item-is-a-bag 1): androidgaming t01, anime t01, chicago t01, clashroyale t02, criticalrole t03, drumcorps t05, nascar t06, onepunchman t01, polyamory t01, rutgers t03, seahawks t01, TheAdventuresofTintin t01, twentyonepilots t02, chess t07, nlsscirclejerk t01, nonbinary t01, opticgaming t03, uiowa t01, gameattack t03, bigbang t01
- **T3-002|T3-038** (19 items; paragraph yes; genuine-joint 13, author-disagrees 4, author-error 1, scheme-ambiguous 1): auburn t01, bindingofisaac t02, dallasstars t05, ghibli t01, gorillaz t03, newzealand t07, shrooms t06, streetfighter t04, transformers t02, bangtan t01, battlecats t05, cloud9 t03, FinalFantasy t02, foxstevenson t02, torontoraptors t04, traaaaaaannnnnnnnnns t01, rutgers t05, smashbros t04, xenoblade_chronicles t02
- **T3-014|T3-153** (18 items; paragraph yes; genuine-joint 10, scheme-ambiguous 5, author-disagrees 2, author-error 1): armenia t08, bangtan t04, belgium t03, dmt t03, eve t10, FederationPlace t06, giivasunner t12, GreenCorner t02, metalgearsolid t08, ohio t08, paladins t25, placehearts t06, rocketbeans t04, theitalyplace t07, AcePlace t06, aoe2 t07, araragi t03, iceland t05
- **T3-002|T3-070** (13 items; paragraph yes; genuine-joint 12, author-disagrees 1): bardmains t01, danganronpa t03, dankmemes t15, python t06, witcher t01, clg t01, harrypotter t15, cowchop t01, mysterydungeon t01, paragon t01, shield t01, Moondye7 t02, seventeen t01
- **T3-002|T3-005** (12 items; paragraph yes; genuine-joint 9, scheme-ambiguous 2, author-error 1): btc t02, Clannad t02, crusaderkings t01, FlaggyFlag t02, harrypotter t01, monalisaclan t02, ohio t03, czech t01, malta t02, nin t10, thetreesnetwork t01, prequelmemes t02
- **T3-070|T3-091** (7 items; paragraph yes; genuine-joint 5, author-error 1, scheme-ambiguous 1): stlouisblues t01, FloydVsVoid t02, heyyea t01, starryknights t02, ChronoTrigger t02, mylittlepony t04, PlaceNL t01
- **T3-004|T3-070** (6 items; paragraph yes; genuine-joint 6): berserk t06, foxstevenson t03, nyu t01, pitt t02, muse t02, suomi t06

## Agreement before and after

Before is the two readers against each other over the packet's 447 items. After is each reader against the ruling over the 437 items not unresolved. The figure after is not a reliability figure: it is agreement with an adjudication I performed.

| | mean Jaccard | primary match |
|---|---|---|
| before (reader against reader) | 0.537 | 0.678 |
| after (each reader against the ruling) | 0.603 | 0.706 |

## Stage B2's predicted pairs

The next list gives, for each of `confusions.md`'s nineteen pairs, the packet's items whose two readers put the pair's themes as their primaries.

- pair 1, T3-005|T3-021: 0
- pair 2, T3-010|T3-149: 0
- pair 3, T3-001|T3-023: 0
- pair 4, T3-028|T3-070: 0
- pair 5, T3-004|T3-020: 0
- pair 6, T3-002|T3-033: 8
- pair 7, T3-015|T3-075: 0
- pair 8, T3-004|T3-070: 6
- pair 9, T3-009|T3-073: 0
- pair 10, T3-004|T3-038: 0
- pair 11, T3-010|T3-151: 0
- pair 12, T3-010|T3-150: 0
- pair 13, T3-010|T3-024: 0
- pair 14, T3-009|T3-043: 0
- pair 15, T3-001|T3-095: 0
- pair 16, T3-087|T3-188: 0
- pair 17, T3-044|T3-082: 0
- pair 18, T3-014|T3-152: 0
- pair 19, T3-015|T3-063: 0

The packet's ten commonest primary splits, predicted or not:

- T3-002|T3-038: 10
- T3-002|T3-033: 8 (predicted)
- T3-002|T3-070: 8
- T3-002|T3-005: 7
- T3-004|T3-070: 6 (predicted)
- T3-014|T3-153: 5
- T3-070|T3-091: 5
- T3-002|T3-062: 4
- T3-062|T3-084: 4
- T3-002|T3-031: 3

## Unresolved items

- minecraft t17: author-disagrees,  
- Redox t02: scheme-ambiguous, T3-015 must_show
- popheads t01: author-disagrees,  
- h3h3productions t27: author-disagrees,  
- kuwait t09: author-disagrees,  
- minecraft t18: author-disagrees,  
- shield t07: author-disagrees,  
- orderofthebluecorner t02: scheme-ambiguous, T3-070 must_show
- THE_R t03: scheme-ambiguous, T3-018 must_show
- parrots t15: scheme-ambiguous, T3-073 must_show

