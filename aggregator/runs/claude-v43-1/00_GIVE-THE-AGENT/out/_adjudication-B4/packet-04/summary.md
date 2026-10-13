# Packet 4, the figures (stage B4 section 9)

Written by `out/_analysis/b4_packet_summary.py` from `disagreements.jsonl`. Items ruled: 461.

## The taxonomy split

The next table counts the packet's rulings by taxonomy value, overall and by J's class of the item.

| taxonomy | all | class 3 | class 4 | class 5 |
|---|---|---|---|---|
| scheme-ambiguous | 59 | 58 | 1 | 0 |
| item-is-a-bag | 48 | 42 | 6 | 0 |
| reader-error | 14 | 14 | 0 | 0 |
| author-error | 78 | 1 | 76 | 1 |
| genuine-joint | 240 | 240 | 0 | 0 |
| author-disagrees | 22 | 0 | 22 | 0 |
| total | 461 | 355 | 105 | 1 |

- unresolved: 10 (2.2%)
- named_neither: 137 (29.7%)
- author-error: 78; author-disagrees: 22
- rulings corrected in place after writing: 179 (Northwestern t01, aggies t03, archlinux t04, argentina t04, armenia t02, austria t05, blackmirror t04, chelseafc t13, croatia t05, danganronpa t08, darksouls t09, de t02, donaldglover t07, drawhelix t04, Fez t05, fireemblem t03, frankocean t10, funhaus t02, germany t06, giantbomb t02, globaloffensive t11, Goodboye t04, gorillaz t06, GreenCorner t03, homestuck t04, india t13, indieheads t12, japan t04, leagueoflegends t16, lebanon t03, linux t11, malaysia t04, masseffect t06, mexico t14, mindcrack t02, nVade t04, nyjets t08, ohio t05, palestine t04, pcmasterrace t09, Peru t07, placestart t14, portal t07, PORTUGALCARALHO t02, purdue t04, rangers t05, ravens t07, reddevils t15, redpandas t06, rickandmorty t04, rocketbeans t05, roosterteeth t04, samuraijack t02, satania t05, scotland t05, serbia t08, smite t06, soylent t03, ss13 t04, stardewvalley t03, stevenuniverse t06, sweden t02, taiwan t05, Temple t06, terraria t08, theblackvoid t06, TheFarLeftSide t03, TheGreatGreenBox t02, theitalyplace t01, titanfall t10, transformers t05, unturned t04, warriors t08, anarchism t02, afip t04, androidgaming t03, canada t03, cavestory t02, chile t03, clubpenguin t09, daftpunk t05, dota2 t08, harrypotter t03, heroesofthestorm t11, israel t02, jerma985 t04, korea t09, miamidolphins t04, MonkeyIsland t03, necrodancer t05, oneshot t04, overwatch t20, pakistan t05, runescape t14, ScottPilgrim t03, simonfraser t09, stlouisblues t08, straya t03, texas t02, GranColombia t05, osugame t01, bakchodi t06, rutgers t11, stlouisblues t07, hentai t03, Goodboye t07, RelientK t05, 2007scape t08, aceattorney t08, bindingofisaac t08, bisexual t06, cloud9 t07, costa_rica t06, cowchop t03, edmontonoilers t04, empiredidnothingwrong t14, feedthebeast t07, furry t03, ice_poseidon t02, Jamaica t07, kanye t03, liquicity t03, loliconsunite t02, luciomains t03, mylittlepony t05, nbaspurs t14, newzealand t06, OnePiece t02, placeDE t03, predators t06, prequelmemes t07, Rainbow6 t10, romania t04, starvstheforcesofevil t04, tf2 t11, theexpanse t05, thenetherlands t04, touhou t04, traaaaaaannnnnnnnnns t02, warriors t06, witcher t04, konosuba t03, opticgaming t06, pitt t03, taiwan t04, hatsune t04, nyjets t06, pusheen t03, rpi t04, rush t04, sooners t06, SquareSpiral t12, turkey t02, undertale t06, GreenCorner t09, clubpenguin t01, penguins t07, gameofthrones t17, kpop t07, DCFU t04, opticgaming t10, phish t11, frc t09, spain t09, natsume t04, anarcho_capitalism t09, newzealand t13, smite t07, theitalyplace t08, vegan t14, brasil t07, chile t12, argentina t12, yogscast t11, japan t13, enterthegungeon t07, pcmasterrace t14, spacexmasterrace t05, bakchodi t09)

## Fields by ambiguity

The next list counts the scheme-ambiguous rulings by the field whose sentence failed to decide.

- must_show: 34
- must_not_show: 8
- decide_when_both: 15
- discriminators: 2

## Third-order themes by ambiguity

The next table ranks the themes whose sentence failed to decide, with the fields.

| theme | rulings | must_show | must_not_show | decide_when_both | discriminators |
|---|---|---|---|---|---|
| T3-005 | 11 | 3 | 0 | 7 | 1 |
| T3-073 | 8 | 8 | 0 | 0 | 0 |
| T3-027 | 7 | 1 | 0 | 6 | 0 |
| T3-021 | 5 | 2 | 3 | 0 | 0 |
| T3-087 | 4 | 3 | 1 | 0 | 0 |
| T3-022 | 3 | 3 | 0 | 0 | 0 |
| T3-058 | 2 | 1 | 0 | 0 | 1 |
| T3-126 | 2 | 1 | 1 | 0 | 0 |
| T3-089 | 2 | 2 | 0 | 0 | 0 |
| T3-088 | 2 | 0 | 0 | 2 | 0 |
| T3-033 | 1 | 1 | 0 | 0 | 0 |
| T3-082 | 1 | 1 | 0 | 0 | 0 |
| T3-010 | 1 | 0 | 1 | 0 | 0 |
| T3-038 | 1 | 1 | 0 | 0 | 0 |
| T3-042 | 1 | 0 | 1 | 0 | 0 |
| T3-065 | 1 | 1 | 0 | 0 | 0 |
| T3-105 | 1 | 1 | 0 | 0 | 0 |
| T3-139 | 1 | 1 | 0 | 0 | 0 |
| T3-006 | 1 | 1 | 0 | 0 | 0 |
| T3-049 | 1 | 1 | 0 | 0 | 0 |
| T3-068 | 1 | 1 | 0 | 0 | 0 |
| T3-192 | 1 | 1 | 0 | 0 | 0 |
| T3-149 | 1 | 0 | 1 | 0 | 0 |

## Boundary pairs and their items

Each pair below is carried in `boundary_ruling` on the items listed. "Paragraph" says whether `boundaries.md` holds the pair's paragraph.

- **T3-005|T3-021** (90 items; paragraph yes; genuine-joint 74, author-error 9, scheme-ambiguous 6, author-disagrees 1): aggies t03, aoe2 t05, archlinux t04, austria t05, bangtan t06, bostonbruins t06, clg t04, cubers t10, earthbound t04, factorio t07, flashtv t09, frankocean t10, furry_irl t12, gorillaz t06, gravityfalls t02, GreenCorner t03, hellointernet t02, HomestarRunner t03, homestuck t04, india t13, leafs t02, leagueoflegends t16, malaysia t04, mindcrack t02, nyjets t08, palestine t04, parrots t09, Peru t07, PinkVomitMonster t02, placestart t14, placetardis t03, portal t07, PORTUGALCARALHO t02, reddevils t15, rocketbeans t05, roosterteeth t04, serbia t08, shield t03, smite t06, ss13 t06, stardewvalley t03, taiwan t05, tf2 t12, TheFarLeftSide t03, theitalyplace t01, TransFlagPlace t03, warriors t08, afip t04, androidgaming t03, cavestory t02, chile t03, ChronoTrigger t03, clubpenguin t09, daftpunk t05, FinalFantasy t05, gameofthrones t14, israel t02, jerma985 t04, korea t09, metroid t09, MonkeyIsland t03, muse t05, necrodancer t05, oneshot t04, pakistan t05, partyparrot t02, placeportalpattern t06, ScottPilgrim t03, simonfraser t09, stlouisblues t08, tagpro t03, tampabaylightning t03, TeamDignitas t04, texas t02, redhotchilipeppers t08, anaheimducks t09, animalcrossing t04, AyyMD t02, cloud9 t07, DestinyTheGame t08, dragonquest t02, feedthebeast t07, kingdomhearts t20, placeDE t03, sheffield t02, starcraft t07, tf2 t11, theexpanse t05, thenetherlands t04, touhou t04
- **T3-005|T3-073** (7 items; paragraph yes; scheme-ambiguous 6, genuine-joint 1): apocalypserising t05, terraria t08, 4chan t08, anime t11, bakchodi t06, neutralmilkhotel t03, texastech t03
- **T3-020|T3-022** (5 items; paragraph yes; genuine-joint 3, scheme-ambiguous 2): mordhau t04, rutgers t04, toolband t04, dallasstars t13, detroitredwings t04
- **T3-027|T3-028** (4 items; paragraph yes; scheme-ambiguous 4): pakistan t08, giantbomb t07, placecanada t12, placeDE t07
- **T3-027|T3-087** (4 items; paragraph yes; genuine-joint 2, scheme-ambiguous 2): shitredditsays t05, sooners t10, tampabaylightning t15, foxes t04
- **T3-002|T3-005** (3 items; paragraph yes; scheme-ambiguous 2, genuine-joint 1): masseffect t01, sooners t08, anarcho_capitalism t04
- **T3-021|T3-038** (3 items; paragraph yes; genuine-joint 3): nerf t02, pitt t03, telegram t03
- **T3-089|T3-168** (2 items; paragraph yes; scheme-ambiguous 2): afip t05, malaysia t05
- **T3-005|T3-006** (1 items; paragraph yes; genuine-joint 1): rocketbeans t07

## Agreement before and after

Before is the two readers against each other over the packet's 461 items. After is each reader against the ruling over the 451 items not unresolved. The figure after is not a reliability figure: it is agreement with an adjudication I performed.

| | mean Jaccard | primary match |
|---|---|---|
| before (reader against reader) | 0.519 | 0.675 |
| after (each reader against the ruling) | 0.640 | 0.726 |

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

