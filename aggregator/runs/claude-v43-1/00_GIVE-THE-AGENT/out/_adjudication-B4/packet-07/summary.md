# Packet 7, the figures (stage B4 section 9)

Written by `out/_analysis/b4_packet_summary.py` from `disagreements.jsonl`. Items ruled: 480.

## The taxonomy split

The next table counts the packet's rulings by taxonomy value, overall and by J's class of the item.

| taxonomy | all | class 3 | class 4 | class 5 |
|---|---|---|---|---|
| scheme-ambiguous | 30 | 22 | 8 | 0 |
| item-is-a-bag | 17 | 13 | 4 | 0 |
| reader-error | 19 | 19 | 0 | 0 |
| author-error | 89 | 0 | 88 | 1 |
| genuine-joint | 303 | 303 | 0 | 0 |
| author-disagrees | 22 | 0 | 18 | 4 |
| total | 480 | 357 | 118 | 5 |

- unresolved: 24 (5.0%)
- named_neither: 108 (22.5%)
- author-error: 89; author-disagrees: 22
- rulings corrected in place after writing: 2 (mindcrack t11, ChronoTrigger t06)

## Fields by ambiguity

The next list counts the scheme-ambiguous rulings by the field whose sentence failed to decide.

- must_show: 25
- must_not_show: 1
- decide_when_both: 0
- discriminators: 4

## Third-order themes by ambiguity

The next table ranks the themes whose sentence failed to decide, with the fields.

| theme | rulings | must_show | must_not_show | decide_when_both | discriminators |
|---|---|---|---|---|---|
| T3-052 | 4 | 4 | 0 | 0 | 0 |
| T3-009 | 3 | 3 | 0 | 0 | 0 |
| T3-164 | 3 | 3 | 0 | 0 | 0 |
| T3-037 | 2 | 2 | 0 | 0 | 0 |
| T3-111 | 2 | 2 | 0 | 0 | 0 |
| T3-117 | 2 | 2 | 0 | 0 | 0 |
| T3-082 | 1 | 1 | 0 | 0 | 0 |
| T3-131 | 1 | 1 | 0 | 0 | 0 |
| T3-038 | 1 | 0 | 0 | 0 | 1 |
| T3-127 | 1 | 1 | 0 | 0 | 0 |
| T3-017 | 1 | 0 | 1 | 0 | 0 |
| T3-011 | 1 | 1 | 0 | 0 | 0 |
| T3-021 | 1 | 1 | 0 | 0 | 0 |
| T3-029 | 1 | 0 | 0 | 0 | 1 |
| T3-156 | 1 | 0 | 0 | 0 | 1 |
| T3-044 | 1 | 1 | 0 | 0 | 0 |
| T3-054 | 1 | 1 | 0 | 0 | 0 |
| T3-087 | 1 | 0 | 0 | 0 | 1 |
| T3-063 | 1 | 1 | 0 | 0 | 0 |
| T3-154 | 1 | 1 | 0 | 0 | 0 |

## Boundary pairs and their items

Each pair below is carried in `boundary_ruling` on the items listed. "Paragraph" says whether `boundaries.md` holds the pair's paragraph.

- **T3-009|T3-043** (62 items; paragraph yes; genuine-joint 46, author-error 16): AceOfAngels8 t05, albania t11, animalcrossing t03, babymetal t06, bangtan t07, Clannad t01, coldplay t06, criticalrole t07, eesti t04, ElderScrolls t04, empiredidnothingwrong t16, europe t20, eve t14, furry_irl t03, fxKorea t07, Goodboye t10, hellointernet t03, hyperlightdrifter t09, kanye t16, lsu t07, luciomains t06, metalcore t02, oneshot t05, pathofexile t12, phish t06, placeDE t08, polska t04, Rainbow6 t13, redhotchilipeppers t09, rocketbeans t10, scotland t06, ScottPilgrim t06, singapore t11, smashbros t05, spacexmasterrace t04, stlouisblues t10, strangerthings t11, straya t07, theexpanse t06, toolband t10, touhou t07, TransFlagPlace t07, transformers t07, TsundereSharks t09, turkey t13, wildhockey t08, yumenikki t05, anaheimducks t08, gamindustri t05, greenlattice t19, GuardiansOfDatBoi t09, kingdomhearts t24, malaysia t11, ssbpm t18, theexpanse t12, ChronoTrigger t06, loliconsunite t08, rickandmorty t08, SquareSpiral t13, tagpro t08, yugioh t17, portugal t29
- **T3-009|T3-073** (29 items; paragraph yes; genuine-joint 25, scheme-ambiguous 2, author-error 2): denmark t09, FaroeIslands t05, hunterxhunter t09, leagueoflegends t18, norge t12, runescape t03, starcraft t11, vegan t10, vinesauce t02, androidgaming t02, blackmirror t07, day9 t06, dragonquest t08, flashtv t13, formula1 t13, gameboy t07, httyd t11, kamenrider t05, leafs t05, sheffield t08, smite t10, tampabaylightning t14, warframe t13, furry t18, yuyuyu t05, suomi t01, edboxes t08, k_on t07, spelunky t04
- **T3-029|T3-073** (18 items; paragraph yes; genuine-joint 14, author-error 2, reader-error 2): cuboulder t08, placetardis t08, PUBATTLEGROUNDS t10, splatoon t06, cubers t31, mindcrack t11, edmontonoilers t09, pebble t05, DatBoi t03, enterthegungeon t10, foxstevenson t07, Honduras t04, linux t19, metroid t10, ultrahardcore t09, dankmemes t16, frankocean t12, geometrydash t07
- **T3-009|T3-117** (10 items; paragraph yes; genuine-joint 9, author-error 1): halo t17, kcroyals t07, minnesotavikings t13, patriots t15, ss13 t07, titanfall t12, unitedkingdom t06, ibo t06, teslamotors t13, muse t11
- **T3-073|T3-105** (8 items; paragraph yes; genuine-joint 8): bindingofisaac t13, pathofexile t17, hungary t07, pakistan t15, rangers t13, straya t10, mylittlepony t15, ripcity t11
- **T3-009|T3-038** (5 items; paragraph yes; genuine-joint 4, author-error 1): miamidolphins t05, pathofexile t14, NieR t07, starryknights t01, startrek t10
- **T3-054|T3-111** (5 items; paragraph yes; genuine-joint 5): AmericanFlaginPlace t16, greenlattice t20, thebluecorner t10, PlaceNL t18, Goodboye t11
- **T3-057|T3-105** (3 items; paragraph yes; genuine-joint 2, reader-error 1): pcmasterrace t16, thenetherlands t12, aoe2 t12
- **T3-018|T3-031** (3 items; paragraph yes; genuine-joint 3): kerbalspaceprogram t12, ohio t11, osu t08
- **T3-009|T3-104** (3 items; paragraph yes; genuine-joint 3): ripcity t07, bobross t02, witcher t03
- **T3-105|T3-156** (3 items; paragraph yes; genuine-joint 3): ireland t14, uiuc t15, heroesofthestorm t08
- **T3-031|T3-135** (2 items; paragraph yes; genuine-joint 2): splatoon t07, transformers t04
- **T3-009|T3-026** (2 items; paragraph yes; genuine-joint 2): colorado t05, harrypotter t02
- **T3-038|T3-065** (2 items; paragraph yes; genuine-joint 2): malaysia t03, kuwait t04

## Agreement before and after

Before is the two readers against each other over the packet's 480 items. After is each reader against the ruling over the 456 items not unresolved. The figure after is not a reliability figure: it is agreement with an adjudication I performed.

| | mean Jaccard | primary match |
|---|---|---|
| before (reader against reader) | 0.500 | 0.650 |
| after (each reader against the ruling) | 0.669 | 0.731 |

## Stage B2's predicted pairs

The next list gives, for each of `confusions.md`'s nineteen pairs, the packet's items whose two readers put the pair's themes as their primaries.

- pair 1, T3-005|T3-021: 0
- pair 2, T3-010|T3-149: 0
- pair 3, T3-001|T3-023: 0
- pair 4, T3-028|T3-070: 0
- pair 5, T3-004|T3-020: 0
- pair 6, T3-002|T3-033: 0
- pair 7, T3-015|T3-075: 0
- pair 8, T3-004|T3-070: 0
- pair 9, T3-009|T3-073: 22
- pair 10, T3-004|T3-038: 0
- pair 11, T3-010|T3-151: 0
- pair 12, T3-010|T3-150: 0
- pair 13, T3-010|T3-024: 0
- pair 14, T3-009|T3-043: 10
- pair 15, T3-001|T3-095: 0
- pair 16, T3-087|T3-188: 0
- pair 17, T3-044|T3-082: 0
- pair 18, T3-014|T3-152: 0
- pair 19, T3-015|T3-063: 0

The packet's ten commonest primary splits, predicted or not:

- T3-009|T3-073: 22 (predicted)
- T3-009|T3-043: 10 (predicted)
- T3-029|T3-073: 7
- T3-009|T3-038: 4
- T3-009|T3-117: 4
- T3-073|T3-105: 4
- T3-073|T3-117: 4
- T3-031|T3-156: 3
- T3-009|T3-031: 3
- T3-009|T3-105: 3

## Unresolved items

- Summit1G t03: author-disagrees,  
- drugs t16: scheme-ambiguous, T3-052 must_show
- norge t09: scheme-ambiguous, T3-052 must_show
- polska t11: scheme-ambiguous, T3-052 must_show
- linux t13: scheme-ambiguous, T3-052 must_show
- nlsscirclejerk t07: scheme-ambiguous, T3-082 must_show
- thesimpsons t06: scheme-ambiguous, T3-131 must_show
- anime_irl t20: scheme-ambiguous, T3-009 must_show
- oman t06: scheme-ambiguous, T3-038 discriminators
- metalcore t14: scheme-ambiguous, T3-127 must_show
- weezer t16: scheme-ambiguous, T3-017 must_not_show
- anarchism t22: scheme-ambiguous, T3-011 must_show
- opticgaming t12: scheme-ambiguous, T3-029 discriminators
- survivor t01: author-disagrees,  
- quebec t17: author-disagrees,  
- shitredditsays t06: scheme-ambiguous, T3-037 must_show
- rangers t15: author-disagrees,  
- corridor t12: scheme-ambiguous, T3-117 must_show
- placehearts t14: author-disagrees,  
- paladins t21: scheme-ambiguous, T3-111 must_show
- touhou t17: scheme-ambiguous, T3-063 must_show
- rojava t03: scheme-ambiguous, T3-164 must_show
- TreePlace t02: scheme-ambiguous, T3-164 must_show
- AcePlace t13: scheme-ambiguous, T3-164 must_show

