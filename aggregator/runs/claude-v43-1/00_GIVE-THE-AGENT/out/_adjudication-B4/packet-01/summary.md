# Packet 1, the figures (stage B4 section 9)

Written by `out/_analysis/b4_packet_summary.py` from `disagreements.jsonl`. Items ruled: 491.

## The taxonomy split

The next table counts the packet's rulings by taxonomy value, overall and by J's class of the item.

| taxonomy | all | class 3 | class 4 | class 5 |
|---|---|---|---|---|
| scheme-ambiguous | 121 | 87 | 32 | 2 |
| item-is-a-bag | 20 | 18 | 2 | 0 |
| reader-error | 77 | 77 | 0 | 0 |
| author-error | 99 | 0 | 91 | 8 |
| genuine-joint | 138 | 138 | 0 | 0 |
| author-disagrees | 36 | 0 | 28 | 8 |
| total | 491 | 320 | 153 | 18 |

- unresolved: 55 (11.2%)
- named_neither: 58 (11.8%)
- author-error: 99; author-disagrees: 36
- rulings corrected in place after writing: 38 (MMA t02, nlsscirclejerk t08, paladins t02, pcmasterrace t04, starcraft t03, totallynotrobots t06, totallynotrobots t08, OneTrueEmilia t01, weezer t13, twice t02, nbaspurs t17, polska t03, python t03, snsd t07, wow t09, warriors t04, criticalrole t02, formula1 t05, elitedangerous t01, chelseafc t02, redhotchilipeppers t12, overwatch t03, pcmasterrace t02, wow t07, borussiadortmund t02, PlaceNL t13, rainbowgrid t06, fivenightsatfreddys t03, flashtv t06, minecraft t12, liverpoolfc t11, canada t09, pcmasterrace t06, quebec t14, sweden t07, nerf t08, placecanada t10, russia t12)

## Fields by ambiguity

The next list counts the scheme-ambiguous rulings by the field whose sentence failed to decide.

- must_show: 76
- must_not_show: 2
- decide_when_both: 4
- discriminators: 39

## Third-order themes by ambiguity

The next table ranks the themes whose sentence failed to decide, with the fields.

| theme | rulings | must_show | must_not_show | decide_when_both | discriminators |
|---|---|---|---|---|---|
| T3-017 | 29 | 5 | 0 | 1 | 23 |
| T3-023 | 25 | 23 | 0 | 0 | 2 |
| T3-001 | 24 | 18 | 0 | 0 | 6 |
| T3-063 | 8 | 6 | 1 | 0 | 1 |
| T3-095 | 7 | 3 | 0 | 2 | 2 |
| T3-032 | 6 | 6 | 0 | 0 | 0 |
| T3-048 | 5 | 5 | 0 | 0 | 0 |
| T3-100 | 3 | 3 | 0 | 0 | 0 |
| T3-064 | 3 | 3 | 0 | 0 | 0 |
| T3-015 | 3 | 0 | 0 | 0 | 3 |
| T3-022 | 1 | 0 | 0 | 0 | 1 |
| T3-143 | 1 | 0 | 0 | 0 | 1 |
| T3-097 | 1 | 1 | 0 | 0 | 0 |
| T3-185 | 1 | 0 | 1 | 0 | 0 |
| T3-016 | 1 | 1 | 0 | 0 | 0 |
| T3-121 | 1 | 1 | 0 | 0 | 0 |
| T3-126 | 1 | 1 | 0 | 0 | 0 |
| T3-075 | 1 | 0 | 0 | 1 | 0 |

## Boundary pairs and their items

Each pair below is carried in `boundary_ruling` on the items listed. "Paragraph" says whether `boundaries.md` holds the pair's paragraph.

- **T3-001|T3-023** (30 items; paragraph yes; scheme-ambiguous 13, genuine-joint 10, reader-error 6, author-error 1): aceattorney t01, rit t02, totallynotrobots t06, totallynotrobots t08, AceOfAngels8 t01, clashroyale t03, enterthegungeon t02, flyers t05, furry t09, harrypotter t06, kilian t08, mylittlepony t08, porterrobinson t08, porterrobinson t09, ss13 t01, teslamotors t01, toolband t02, totallynotrobots t02, totallynotrobots t03, totallynotrobots t04, totallynotrobots t07, OneTrueEmilia t01, apocalypserising t01, formula1 t02, greece t07, polska t03, thetreesnetwork t02, totallynotrobots t01, ubc t02, zootopia t01
- **T3-001|T3-048** (20 items; paragraph yes; scheme-ambiguous 8, reader-error 8, genuine-joint 4): btc t04, bitcoin t06, feedthebeast t02, opticgaming t01, uofmn t01, baylor t02, GuildWars2 t01, GuildWars2 t10, runescape t07, rutgers t01, starlightstage t03, warframe t15, yugioh t10, yugioh t11, danganronpa t19, falcons t10, kamenrider t07, lego t07, simonfraser t02, ubreddit t02
- **T3-017|T3-031** (15 items; paragraph yes; scheme-ambiguous 15): cubers t30, ethereum t06, falcons t08, flashtv t04, freedomplanet t05, h3h3productions t06, h3h3productions t12, heyyea t07, indieheads t06, mls t07, PlaceNL t20, romania t22, SydneyFC t03, tf2 t09, torontoraptors t03
- **T3-001|T3-095** (8 items; paragraph yes; reader-error 6, scheme-ambiguous 2): linux t04, planetside t01, romania t12, swordartonline t03, thesimpsons t02, worldoftanks t02, fivenightsatfreddys t03, hearthstone t01
- **T3-023|T3-095** (7 items; paragraph yes; genuine-joint 4, author-disagrees 1, reader-error 1, scheme-ambiguous 1): paragon t08, hawks t07, smashbros t01, criticalrole t02, ElderScrolls t01, h3h3productions t23, transformers t01
- **T3-048|T3-095** (6 items; paragraph yes; reader-error 3, genuine-joint 2, scheme-ambiguous 1): clg t08, gameofthrones t09, paladins t01, thesilphroad t02, btc t01, loltyler1 t01
- **T3-063|T3-185** (6 items; paragraph yes; reader-error 3, genuine-joint 2, scheme-ambiguous 1): anime_irl t05, destiny t06, placecanada t10, ss13 t11, russia t12, leafs t12
- **T3-032|T3-097** (5 items; paragraph yes; scheme-ambiguous 3, item-is-a-bag 2): anime_irl t16, anime_irl t17, hunterxhunter t03, pcmasterrace t02, survivor t10
- **T3-001|T3-017** (4 items; paragraph yes; reader-error 2, genuine-joint 1, scheme-ambiguous 1): ohio t01, homelab t03, planetside t05, titanfall t03
- **T3-023|T3-051** (4 items; paragraph yes; reader-error 3, genuine-joint 1): partyparrot t16, titanfall t05, warframe t06, warriors t04
- **T3-015|T3-063** (4 items; paragraph yes; scheme-ambiguous 3, genuine-joint 1): fireemblem t08, futanari t06, serbia t15, stardustcrusaders t21
- **T3-031|T3-048** (3 items; paragraph yes; scheme-ambiguous 3): GuildWars2 t02, GuildWars2 t05, rocketleague t15
- **T3-001|T3-031** (1 items; paragraph yes; scheme-ambiguous 1): rwby t03
- **T3-023|T3-031** (1 items; paragraph yes; scheme-ambiguous 1): stardustcrusaders t10
- **T3-023|T3-048** (1 items; paragraph yes; reader-error 1): rit t01
- **T3-023|T3-100** (1 items; paragraph yes; scheme-ambiguous 1): wallstreetbets t03
- **T3-023|T3-185** (1 items; paragraph yes; scheme-ambiguous 1): redhotchilipeppers t04
- **T3-001|T3-051** (1 items; paragraph yes; reader-error 1): 4chan t12

## Agreement before and after

Before is the two readers against each other over the packet's 491 items. After is each reader against the ruling over the 436 items not unresolved. The figure after is not a reliability figure: it is agreement with an adjudication I performed.

| | mean Jaccard | primary match |
|---|---|---|
| before (reader against reader) | 0.486 | 0.578 |
| after (each reader against the ruling) | 0.656 | 0.717 |

## Stage B2's predicted pairs

The next list gives, for each of `confusions.md`'s nineteen pairs, the packet's items whose two readers put the pair's themes as their primaries.

- pair 1, T3-005|T3-021: 1
- pair 2, T3-010|T3-149: 0
- pair 3, T3-001|T3-023: 20
- pair 4, T3-028|T3-070: 0
- pair 5, T3-004|T3-020: 0
- pair 6, T3-002|T3-033: 0
- pair 7, T3-015|T3-075: 4
- pair 8, T3-004|T3-070: 0
- pair 9, T3-009|T3-073: 0
- pair 10, T3-004|T3-038: 0
- pair 11, T3-010|T3-151: 0
- pair 12, T3-010|T3-150: 0
- pair 13, T3-010|T3-024: 0
- pair 14, T3-009|T3-043: 0
- pair 15, T3-001|T3-095: 11
- pair 16, T3-087|T3-188: 0
- pair 17, T3-044|T3-082: 0
- pair 18, T3-014|T3-152: 0
- pair 19, T3-015|T3-063: 7

The packet's ten commonest primary splits, predicted or not:

- T3-001|T3-023: 20 (predicted)
- T3-017|T3-031: 17
- T3-001|T3-048: 13
- T3-001|T3-095: 11 (predicted)
- T3-023|T3-095: 11
- T3-001|T3-017: 8
- T3-015|T3-063: 7 (predicted)
- T3-048|T3-095: 6
- T3-001|T3-031: 5
- T3-032|T3-097: 5

## Unresolved items

- 4chan t11: scheme-ambiguous, T3-001 must_show
- bisexual t09: scheme-ambiguous, T3-001 must_show
- kurdistan t06: scheme-ambiguous, T3-095 discriminators
- lakers t07: scheme-ambiguous, T3-095 discriminators
- lebanon t09: author-disagrees,  
- schoolidolfestival t11: scheme-ambiguous, T3-001 must_show
- thesimpsons t03: scheme-ambiguous, T3-001 must_show
- 49ers t03: scheme-ambiguous, T3-001 must_show
- danganronpa t23: scheme-ambiguous, T3-001 must_show
- falcons t09: scheme-ambiguous, T3-001 must_show
- parahumans t07: scheme-ambiguous, T3-001 must_show
- weezer t13: scheme-ambiguous, T3-017 discriminators
- bardmains t09: scheme-ambiguous, T3-143 discriminators
- oneplus t09: scheme-ambiguous, T3-001 discriminators
- berserk t04: scheme-ambiguous, T3-001 must_show
- de t22: scheme-ambiguous, T3-017 must_show
- archlinux t12: author-disagrees,  
- flashtv t14: scheme-ambiguous, T3-023 must_show
- greenbaypackers t05: author-disagrees,  
- megaman t04: scheme-ambiguous, T3-023 must_show
- nbaspurs t17: author-disagrees,  
- ethereum t12: scheme-ambiguous, T3-032 must_show
- iastate t01: scheme-ambiguous, T3-023 must_show
- katawashoujo t02: scheme-ambiguous, T3-023 must_show
- winnipegjets t03: scheme-ambiguous, T3-023 must_show
- Braveryjerk t01: scheme-ambiguous, T3-023 must_show
- liverpoolfc t03: scheme-ambiguous, T3-023 must_show
- mindcrack t07: scheme-ambiguous, T3-095 must_show
- survivor t18: scheme-ambiguous, T3-100 must_show
- survivor t11: scheme-ambiguous, T3-100 must_show
- yugioh t06: scheme-ambiguous, T3-063 must_show
- yugioh t12: scheme-ambiguous, T3-063 must_show
- danganronpa t19: scheme-ambiguous, T3-001 discriminators
- GuildWars2 t07: scheme-ambiguous, T3-001 must_show
- halo t01: scheme-ambiguous, T3-048 must_show
- kamenrider t07: scheme-ambiguous, T3-001 discriminators
- lego t07: scheme-ambiguous, T3-001 discriminators
- ubreddit t02: scheme-ambiguous, T3-001 discriminators
- vim t01: scheme-ambiguous, T3-001 must_show
- rainbowgrid t06: scheme-ambiguous, T3-064 must_show
- bostonceltics t03: scheme-ambiguous, T3-023 must_show
- polandball t01: scheme-ambiguous, T3-095 must_show
- wholesomememes t14: scheme-ambiguous, T3-001 must_show
- python t09: author-disagrees,  
- stardustcrusaders t21: scheme-ambiguous, T3-015 discriminators
- 4chan t06: author-disagrees,  
- denverbroncos t02: scheme-ambiguous, T3-032 must_show
- portugal t15: scheme-ambiguous, T3-001 must_show
- FlipnoteStudio3D t02: author-disagrees,  
- morrowind t11: author-disagrees,  
- catalonia t04: author-disagrees,  
- metalcore t07: scheme-ambiguous, T3-063 must_show
- oneplus t05: scheme-ambiguous, T3-063 must_show
- twice t04: scheme-ambiguous, T3-063 must_show
- flashtv t10: scheme-ambiguous, T3-063 must_show

