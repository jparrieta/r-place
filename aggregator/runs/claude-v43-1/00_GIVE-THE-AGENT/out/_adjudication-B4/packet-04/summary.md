# Packet 4, the figures (stage B4 section 9)

Written by `out/_analysis/b4_packet_summary.py` from `disagreements.jsonl`. Items ruled: 461.

## The taxonomy split

The next table counts the packet's rulings by taxonomy value, overall and by J's class of the item.

| taxonomy | all | class 3 | class 4 | class 5 |
|---|---|---|---|---|
| scheme-ambiguous | 84 | 78 | 6 | 0 |
| item-is-a-bag | 53 | 45 | 8 | 0 |
| reader-error | 13 | 13 | 0 | 0 |
| author-error | 75 | 0 | 74 | 1 |
| genuine-joint | 219 | 219 | 0 | 0 |
| author-disagrees | 17 | 0 | 17 | 0 |
| total | 461 | 355 | 105 | 1 |

- unresolved: 10 (2.2%)
- named_neither: 222 (48.2%)
- author-error: 75; author-disagrees: 17
- rulings corrected in place after writing: 1 (MonkeyIsland t03)

## Fields by ambiguity

The next list counts the scheme-ambiguous rulings by the field whose sentence failed to decide.

- must_show: 39
- must_not_show: 32
- decide_when_both: 11
- discriminators: 2

## Third-order themes by ambiguity

The next table ranks the themes whose sentence failed to decide, with the fields.

| theme | rulings | must_show | must_not_show | decide_when_both | discriminators |
|---|---|---|---|---|---|
| T3-021 | 24 | 2 | 22 | 0 | 0 |
| T3-005 | 10 | 6 | 0 | 3 | 1 |
| T3-073 | 9 | 9 | 0 | 0 | 0 |
| T3-027 | 7 | 1 | 0 | 6 | 0 |
| T3-022 | 5 | 4 | 1 | 0 | 0 |
| T3-087 | 4 | 3 | 1 | 0 | 0 |
| T3-038 | 3 | 1 | 2 | 0 | 0 |
| T3-006 | 2 | 1 | 1 | 0 | 0 |
| T3-058 | 2 | 1 | 0 | 0 | 1 |
| T3-126 | 2 | 1 | 1 | 0 | 0 |
| T3-089 | 2 | 2 | 0 | 0 | 0 |
| T3-088 | 2 | 0 | 0 | 2 | 0 |
| T3-033 | 1 | 1 | 0 | 0 | 0 |
| T3-082 | 1 | 1 | 0 | 0 | 0 |
| T3-041 | 1 | 0 | 1 | 0 | 0 |
| T3-042 | 1 | 0 | 1 | 0 | 0 |
| T3-065 | 1 | 1 | 0 | 0 | 0 |
| T3-105 | 1 | 1 | 0 | 0 | 0 |
| T3-020 | 1 | 0 | 1 | 0 | 0 |
| T3-139 | 1 | 1 | 0 | 0 | 0 |
| T3-049 | 1 | 1 | 0 | 0 | 0 |
| T3-068 | 1 | 1 | 0 | 0 | 0 |
| T3-192 | 1 | 1 | 0 | 0 | 0 |
| T3-149 | 1 | 0 | 1 | 0 | 0 |

## Boundary pairs and their items

Each pair below is carried in `boundary_ruling` on the items listed. "Paragraph" says whether `boundaries.md` holds the pair's paragraph.

- **T3-005|T3-021** (67 items; paragraph yes; genuine-joint 54, author-error 9, scheme-ambiguous 3, author-disagrees 1): aggies t03, aoe2 t05, austria t05, bangtan t06, bostonbruins t06, clg t04, cubers t10, earthbound t04, factorio t07, flashtv t09, frankocean t10, furry_irl t12, gorillaz t06, gravityfalls t02, GreenCorner t03, hellointernet t02, HomestarRunner t03, homestuck t04, leafs t02, leagueoflegends t16, nyjets t08, parrots t09, PinkVomitMonster t02, placestart t14, placetardis t03, portal t07, reddevils t15, rocketbeans t05, roosterteeth t04, shield t03, ss13 t06, stardewvalley t03, tf2 t12, TheFarLeftSide t03, TransFlagPlace t03, warriors t08, androidgaming t03, ChronoTrigger t03, clubpenguin t09, FinalFantasy t05, gameofthrones t14, jerma985 t04, metroid t09, MonkeyIsland t03, muse t05, necrodancer t05, oneshot t04, partyparrot t02, placeportalpattern t06, ScottPilgrim t03, simonfraser t09, stlouisblues t08, tagpro t03, tampabaylightning t03, TeamDignitas t04, redhotchilipeppers t08, anaheimducks t09, animalcrossing t04, AyyMD t02, bisexual t06, cloud9 t07, DestinyTheGame t08, dragonquest t02, kingdomhearts t20, sheffield t02, starcraft t07, theexpanse t05
- **T3-002|T3-005** (9 items; paragraph yes; scheme-ambiguous 5, genuine-joint 3, item-is-a-bag 1): masseffect t01, sooners t08, redpandas t06, smite t06, cavestory t02, anarcho_capitalism t04, feedthebeast t07, loliconsunite t02, tf2 t11
- **T3-005|T3-073** (9 items; paragraph yes; scheme-ambiguous 7, genuine-joint 2): apocalypserising t05, masseffect t06, mindcrack t02, terraria t08, daftpunk t05, 4chan t08, anime t11, neutralmilkhotel t03, texastech t03
- **T3-020|T3-022** (5 items; paragraph yes; genuine-joint 3, scheme-ambiguous 2): mordhau t04, rutgers t04, toolband t04, dallasstars t13, detroitredwings t04
- **T3-027|T3-028** (4 items; paragraph yes; scheme-ambiguous 4): pakistan t08, giantbomb t07, placecanada t12, placeDE t07
- **T3-027|T3-087** (4 items; paragraph yes; genuine-joint 2, scheme-ambiguous 2): shitredditsays t05, sooners t10, tampabaylightning t15, foxes t04
- **T3-021|T3-038** (3 items; paragraph yes; genuine-joint 3): nerf t02, pitt t03, telegram t03
- **T3-089|T3-168** (2 items; paragraph yes; scheme-ambiguous 2): afip t05, malaysia t05
- **T3-005|T3-006** (1 items; paragraph yes; genuine-joint 1): rocketbeans t07

## Agreement before and after

Before is the two readers against each other over the packet's 461 items. After is each reader against the ruling over the 451 items not unresolved. The figure after is not a reliability figure: it is agreement with an adjudication I performed.

| | mean Jaccard | primary match |
|---|---|---|
| before (reader against reader) | 0.519 | 0.675 |
| after (each reader against the ruling) | 0.562 | 0.671 |

## Stage B2's predicted pairs

The next list gives, for each of `confusions.md`'s nineteen pairs, the packet's items whose two readers put the pair's themes as their primaries.

- pair 1, T3-005|T3-021: 37
- pair 2, T3-010|T3-149: 0
- pair 3, T3-001|T3-023: 0
- pair 4, T3-028|T3-070: 2
- pair 5, T3-004|T3-020: 0
- pair 6, T3-002|T3-033: 0
- pair 7, T3-015|T3-075: 0
- pair 8, T3-004|T3-070: 0
- pair 9, T3-009|T3-073: 0
- pair 10, T3-004|T3-038: 0
- pair 11, T3-010|T3-151: 0
- pair 12, T3-010|T3-150: 0
- pair 13, T3-010|T3-024: 0
- pair 14, T3-009|T3-043: 0
- pair 15, T3-001|T3-095: 0
- pair 16, T3-087|T3-188: 1
- pair 17, T3-044|T3-082: 0
- pair 18, T3-014|T3-152: 0
- pair 19, T3-015|T3-063: 0

The packet's ten commonest primary splits, predicted or not:

- T3-005|T3-021: 37 (predicted)
- T3-021|T3-038: 6
- T3-005|T3-038: 5
- T3-005|T3-073: 5
- T3-005|T3-006: 4
- T3-058|T3-073: 4
- T3-021|T3-087: 3
- T3-027|T3-028: 3
- T3-027|T3-087: 3
- T3-002|T3-005: 2

## Unresolved items

- linux t01: scheme-ambiguous, T3-005 must_show
- osu t15: scheme-ambiguous, T3-005 must_show
- cavestory t06: scheme-ambiguous, T3-087 must_show
- Dominican t09: scheme-ambiguous, T3-087 must_show
- kpop t13: scheme-ambiguous, T3-139 must_show
- DestinyTheGame t14: scheme-ambiguous, T3-058 discriminators
- notredame t10: scheme-ambiguous, T3-058 must_show
- hungary t05: scheme-ambiguous, T3-068 must_show
- dallasstars t01: scheme-ambiguous, T3-192 must_show
- tampabaylightning t15: scheme-ambiguous, T3-027 decide_when_both

