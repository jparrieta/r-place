# Packet 6, the figures (stage B4 section 9)

Written by `out/_analysis/b4_packet_summary.py` from `disagreements.jsonl`. Items ruled: 500.

## The taxonomy split

The next table counts the packet's rulings by taxonomy value, overall and by J's class of the item.

| taxonomy | all | class 3 | class 4 | class 5 |
|---|---|---|---|---|
| scheme-ambiguous | 71 | 58 | 12 | 1 |
| item-is-a-bag | 20 | 12 | 8 | 0 |
| reader-error | 19 | 19 | 0 | 0 |
| author-error | 83 | 0 | 80 | 3 |
| genuine-joint | 256 | 256 | 0 | 0 |
| author-disagrees | 51 | 0 | 34 | 17 |
| total | 500 | 345 | 134 | 21 |

- unresolved: 49 (9.8%)
- named_neither: 145 (29.0%)
- author-error: 83; author-disagrees: 51
- rulings corrected in place after writing: 32 (fivenightsatfreddys t08, philippines t08, suomi t10, turkey t06, rocketleague t05, empiredidnothingwrong t22, harrypotter t19, futurama t15, cfb t02, denmark t05, frankocean t05, metalcore t03, utaustin t05, chibears t10, EraseThePlace t06, kurdistan t04, starcitizen t11, TransFlagPlace t05, ukplace t04, elitedangerous t07, eagles t06, japan t05, purdue t07, greyblob t03, austria t01, indonesia t01, wholesomememes t17, belgium t05, azerbaijan t02, falcons t16, roosterteeth t08, anarcho_capitalism t17)

## Fields by ambiguity

The next list counts the scheme-ambiguous rulings by the field whose sentence failed to decide.

- must_show: 31
- must_not_show: 8
- decide_when_both: 0
- discriminators: 32

## Third-order themes by ambiguity

The next table ranks the themes whose sentence failed to decide, with the fields.

| theme | rulings | must_show | must_not_show | decide_when_both | discriminators |
|---|---|---|---|---|---|
| T3-017 | 24 | 0 | 0 | 0 | 24 |
| T3-001 | 8 | 0 | 0 | 0 | 8 |
| T3-018 | 5 | 5 | 0 | 0 | 0 |
| T3-004 | 4 | 0 | 4 | 0 | 0 |
| T3-052 | 4 | 4 | 0 | 0 | 0 |
| T3-030 | 2 | 2 | 0 | 0 | 0 |
| T3-020 | 2 | 0 | 2 | 0 | 0 |
| T3-086 | 2 | 2 | 0 | 0 | 0 |
| T3-122 | 1 | 1 | 0 | 0 | 0 |
| T3-141 | 1 | 1 | 0 | 0 | 0 |
| T3-002 | 1 | 1 | 0 | 0 | 0 |
| T3-163 | 1 | 1 | 0 | 0 | 0 |
| T3-013 | 1 | 1 | 0 | 0 | 0 |
| T3-019 | 1 | 1 | 0 | 0 | 0 |
| T3-031 | 1 | 1 | 0 | 0 | 0 |
| T3-066 | 1 | 1 | 0 | 0 | 0 |
| T3-172 | 1 | 1 | 0 | 0 | 0 |
| T3-033 | 1 | 0 | 1 | 0 | 0 |
| T3-021 | 1 | 0 | 1 | 0 | 0 |
| T3-113 | 1 | 1 | 0 | 0 | 0 |
| T3-142 | 1 | 1 | 0 | 0 | 0 |
| T3-182 | 1 | 1 | 0 | 0 | 0 |
| T3-046 | 1 | 1 | 0 | 0 | 0 |
| T3-005 | 1 | 1 | 0 | 0 | 0 |
| T3-115 | 1 | 1 | 0 | 0 | 0 |
| T3-147 | 1 | 1 | 0 | 0 | 0 |
| T3-023 | 1 | 1 | 0 | 0 | 0 |
| T3-057 | 1 | 1 | 0 | 0 | 0 |

## Boundary pairs and their items

Each pair below is carried in `boundary_ruling` on the items listed. "Paragraph" says whether `boundaries.md` holds the pair's paragraph.

- **T3-010|T3-149** (28 items; paragraph yes; genuine-joint 18, item-is-a-bag 6, author-disagrees 4): adventuretime t06, clashroyale t07, cubers t07, denverbroncos t08, DestinyTheGame t09, empiredidnothingwrong t13, fivenightsatfreddys t08, Goodboye t02, mcgill t06, ockytop t05, philippines t08, suomi t10, thesimpsons t10, twice t16, weezer t06, ainbowroad t05, anarcho_capitalism t12, berkeley t05, cfb t02, denmark t05, frankocean t05, hatsune t03, kilian t06, lebanon t04, theitalyplace t02, AprilKnights t04, smite t08, thailand t08
- **T3-017|T3-031** (24 items; paragraph yes; scheme-ambiguous 23, genuine-joint 1): canucks t13, eder t01, edmontonoilers t12, ibo t03, ibo t05, india t14, paladins t04, paladins t26, planetside t02, purdue t16, totallynotrobots t15, zootopia t16, lego t04, chicago t08, empiredidnothingwrong t19, flashtv t12, kpop t09, oneshot t11, puzzleanddragons t07, starlightstage t08, wholesomememes t23, croatia t07, 4chan t22, futurama t14
- **T3-001|T3-031** (9 items; paragraph yes; scheme-ambiguous 8, genuine-joint 1): danganronpa t18, GuildWars2 t18, spacexmasterrace t12, telegram t01, thesimpsons t04, twitchplayspokemon t09, wholesomememes t11, twentyonepilots t07, berserk t02
- **T3-010|T3-151** (6 items; paragraph yes; genuine-joint 5, item-is-a-bag 1): malaysia t07, stlouis t05, yogscast t03, floridagators t08, japan t05, metalgearsolid t07
- **T3-150|T3-151** (5 items; paragraph yes; genuine-joint 4, author-error 1): stlouisblues t03, nin t02, TeamYellowPlace t03, overwatch t22, starcraft t08
- **T3-023|T3-031** (5 items; paragraph yes; genuine-joint 2, reader-error 2, scheme-ambiguous 1): twitchplayspokemon t05, kerbalspaceprogram t02, kerbalspaceprogram t03, leagueoflegends t05, survivor t04
- **T3-018|T3-052** (5 items; paragraph yes; genuine-joint 3, scheme-ambiguous 2): twice t10, Mario t03, thailand t13, truestl t06, Redox t01
- **T3-031|T3-050** (4 items; paragraph yes; genuine-joint 3, author-error 1): udub t07, canucks t38, farmcarrots t15, southafrica t03
- **T3-018|T3-031** (1 items; paragraph yes; scheme-ambiguous 1): achievement_hunter t04

## Agreement before and after

Before is the two readers against each other over the packet's 500 items. After is each reader against the ruling over the 451 items not unresolved. The figure after is not a reliability figure: it is agreement with an adjudication I performed.

| | mean Jaccard | primary match |
|---|---|---|
| before (reader against reader) | 0.454 | 0.510 |
| after (each reader against the ruling) | 0.600 | 0.595 |

## Stage B2's predicted pairs

The next list gives, for each of `confusions.md`'s nineteen pairs, the packet's items whose two readers put the pair's themes as their primaries.

- pair 1, T3-005|T3-021: 0
- pair 2, T3-010|T3-149: 14
- pair 3, T3-001|T3-023: 0
- pair 4, T3-028|T3-070: 0
- pair 5, T3-004|T3-020: 0
- pair 6, T3-002|T3-033: 0
- pair 7, T3-015|T3-075: 0
- pair 8, T3-004|T3-070: 0
- pair 9, T3-009|T3-073: 0
- pair 10, T3-004|T3-038: 0
- pair 11, T3-010|T3-151: 3
- pair 12, T3-010|T3-150: 4
- pair 13, T3-010|T3-024: 0
- pair 14, T3-009|T3-043: 0
- pair 15, T3-001|T3-095: 0
- pair 16, T3-087|T3-188: 0
- pair 17, T3-044|T3-082: 0
- pair 18, T3-014|T3-152: 0
- pair 19, T3-015|T3-063: 0

The packet's ten commonest primary splits, predicted or not:

- T3-010|T3-149: 14 (predicted)
- T3-017|T3-031: 12
- T3-001|T3-031: 7
- T3-023|T3-031: 7
- T3-150|T3-151: 6
- T3-031|T3-050: 6
- T3-018|T3-031: 6
- T3-018|T3-052: 6
- T3-010|T3-150: 4 (predicted)
- T3-002|T3-065: 4

## Unresolved items

- futurama t15: scheme-ambiguous, T3-122 must_show
- orderofthebluecorner t12: scheme-ambiguous, T3-002 must_show
- romania t18: scheme-ambiguous, T3-113 must_show
- azerbaijan t02: author-disagrees,  
- anarcho_capitalism t17: author-disagrees,  
- costa_rica t10: scheme-ambiguous, T3-182 must_show
- samuraijack t14: author-disagrees,  
- cardinals t09: scheme-ambiguous, T3-052 must_show
- habs t13: scheme-ambiguous, T3-005 must_show
- danganronpa t18: scheme-ambiguous, T3-001 discriminators
- telegram t01: scheme-ambiguous, T3-001 discriminators
- thesimpsons t04: scheme-ambiguous, T3-001 discriminators
- wholesomememes t11: scheme-ambiguous, T3-001 discriminators
- albania t01: author-disagrees,  
- archlinux t13: author-disagrees,  
- kindafunny t03: author-disagrees,  
- mechanicalkeyboards t06: author-disagrees,  
- raocow t08: author-disagrees,  
- spacex t07: author-disagrees,  
- suomi t12: author-disagrees,  
- elitedangerous t10: author-disagrees,  
- mexico t19: author-disagrees,  
- tampabaylightning t16: scheme-ambiguous, T3-147 must_show
- india t14: scheme-ambiguous, T3-017 discriminators
- wallstreetbets t17: scheme-ambiguous, T3-052 must_show
- porterrobinson t18: scheme-ambiguous, T3-018 must_show
- Dustforce t02: scheme-ambiguous, T3-018 must_show
- survivor t04: scheme-ambiguous, T3-017 discriminators
- anarchism t09: author-disagrees,  
- empiredidnothingwrong t19: scheme-ambiguous, T3-017 discriminators
- flashtv t12: scheme-ambiguous, T3-017 discriminators
- ik_ihe t05: author-disagrees,  
- japan t14: author-disagrees,  
- landry t04: author-disagrees,  
- oneshot t11: scheme-ambiguous, T3-017 discriminators
- pakistan t27: author-disagrees,  
- porterrobinson t13: author-disagrees,  
- satania t01: author-disagrees,  
- satania t09: author-disagrees,  
- Slovakia t02: author-disagrees,  
- starlightstage t08: scheme-ambiguous, T3-017 discriminators
- twentyonepilots t07: scheme-ambiguous, T3-001 discriminators
- wholesomememes t23: scheme-ambiguous, T3-017 discriminators
- wow t05: author-disagrees,  
- 4chan t22: scheme-ambiguous, T3-017 discriminators
- berserk t02: scheme-ambiguous, T3-001 discriminators
- smite t11: author-disagrees,  
- futurama t11: scheme-ambiguous, T3-057 must_show
- GranColombia t10: author-disagrees,  

