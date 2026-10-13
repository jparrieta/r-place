# Packet 3, the figures (stage B4 section 9)

Written by `out/_analysis/b4_packet_summary.py` from `disagreements.jsonl`. Items ruled: 500.

## The taxonomy split

The next table counts the packet's rulings by taxonomy value, overall and by J's class of the item.

| taxonomy | all | class 3 | class 4 | class 5 |
|---|---|---|---|---|
| scheme-ambiguous | 94 | 85 | 9 | 0 |
| item-is-a-bag | 71 | 55 | 16 | 0 |
| reader-error | 4 | 4 | 0 | 0 |
| author-error | 55 | 0 | 50 | 5 |
| genuine-joint | 232 | 232 | 0 | 0 |
| author-disagrees | 44 | 0 | 42 | 2 |
| total | 500 | 376 | 117 | 7 |

- unresolved: 7 (1.4%)
- named_neither: 173 (34.6%)
- author-error: 55; author-disagrees: 44
- rulings corrected in place after writing: 208 (ubreddit t03, DiamondClub t01, foxes t01, hawks t05, kanye t01, schoolidolfestival t04, stardustcrusaders t01, unturned t03, wallstreetbets t01, AMD t05, AvoArmy t06, berkeley t03, catalonia t07, chile t02, eesti t12, ElderScrolls t05, frc t01, funhaus t01, GranColombia t06, greyblob t02, HomestarRunner t01, iastate t03, ireland t04, kindafunny t05, minecraft t04, monstercat t06, ohio t04, placeDE t10, prequelmemes t03, skyrim t02, texas t04, theitalyplace t10, timbers t02, twice t08, unturned t09, uwaterloo t01, weezer t02, oneshot t01, cuboulder t04, de t10, giantbomb t01, TheFarLeftSide t02, truestl t02, AvoArmy t01, tf2 t05, uoft t08, vinesauce t01, pebble t04, placesnek t04, esperanto t03, OnePiece t07, argentina t07, theitalyplace t03, rickandmorty t11, farmcarrots t08, starlightstage t12, thepointing t04, bretagne t01, dallasstars t04, denverbroncos t07, flashtv t01, frc t03, portal t06, romania t02, singapore t06, cmu t01, hongkong t02, metalgearsolid t04, planetside t08, tetris t01, spacexmasterrace t13, bostonceltics t04, WisconsinBadgers t02, 2007scape t03, brasil t02, eagles t02, eve t03, gameofthrones t02, indieheads t13, leagueoflegends t03, loliconsunite t07, math t02, nuclearthrone t01, overwatch t13, rust t07, starlightstage t09, starvstheforcesofevil t02, stevenuniverse t01, trees t03, warthunder t10, yugioh t04, palestine t03, norge t03, unitedkingdom t11, TheHulk t04, Villanova t03, greenlattice t06, bostonbruins t02, enterthegungeon t01, ethoslab t01, forsen t01, habs t02, nyjets t04, the_pack t01, winnipegjets t01, wow t17, bisexual t04, fullcommunism t10, furry t02, gratefuldead t04, placetardis t09, DestinyTheGame t07, ManningPlace t05, sakuragakuin t01, borderlands t02, pcmasterrace t08, stevenuniverse t02, anime t06, drumcorps t09, ethoslab t05, ice_poseidon t05, qotsa t06, spacex t05, bdsm t01, vietnam t04, KState t04, ufl t01, borderlands t04, empiredidnothingwrong t11, placehearts t03, turkey t08, rainbowgrid t01, achievement_hunter t03, adventuretime t04, batman t01, bitcoin t02, bobross t01, borderlands t01, brasil t04, catholicism t05, cavestory t01, counting t02, CSUFoCo t01, cubers t03, detroitlions t04, detroitlions t08, dofus t01, dota2 t11, drugs t01, EraseThePlace t03, faeria t01, farmcarrots t02, FinalFantasy t07, flashtv t08, flyers t01, frc t04, gravityfalls t01, kcroyals t03, kpop t05, lost t02, madokamagica t01, minnesotavikings t06, MMA t07, monero t01, monsterhunter t03, parahumans t01, paydaytheheist t02, schoolidolfestival t06, sips t10, snsd t01, starcitizen t14, stardustcrusaders t05, suomi t07, touhou t02, warthunder t13, wildhockey t01, AyyMD t01, buffalo t02, samuraijack t10, yumenikki t01, skyrim t03, philippines t07, hentai t02, israel t01, ainbowroad t12, placestart t13, peterdraws t01, AmericanFlaginPlace t10, argentina t05, bulgaria t03, dota2 t06, Jamaica t10, japan t08, kingdomhearts t21, minnesotavikings t07, newzealand t09, placeDE t06, placeportalpattern t03, placestart t09, teamcube t04, texas t05, uoft t06, southafrica t09, partyparrot t03, day9 t04, ucf t10, mylittlepony t06, baylor t05)

## Fields by ambiguity

The next list counts the scheme-ambiguous rulings by the field whose sentence failed to decide.

- must_show: 51
- must_not_show: 24
- decide_when_both: 3
- discriminators: 16

## Third-order themes by ambiguity

The next table ranks the themes whose sentence failed to decide, with the fields.

| theme | rulings | must_show | must_not_show | decide_when_both | discriminators |
|---|---|---|---|---|---|
| T3-033 | 23 | 21 | 1 | 0 | 1 |
| T3-004 | 21 | 3 | 10 | 0 | 8 |
| T3-038 | 11 | 9 | 2 | 0 | 0 |
| T3-020 | 7 | 0 | 6 | 0 | 1 |
| T3-041 | 7 | 2 | 4 | 0 | 1 |
| T3-026 | 5 | 1 | 0 | 2 | 2 |
| T3-074 | 2 | 2 | 0 | 0 | 0 |
| T3-055 | 2 | 2 | 0 | 0 | 0 |
| T3-060 | 2 | 1 | 0 | 1 | 0 |
| T3-082 | 2 | 0 | 1 | 0 | 1 |
| T3-002 | 1 | 0 | 0 | 0 | 1 |
| T3-017 | 1 | 1 | 0 | 0 | 0 |
| T3-049 | 1 | 1 | 0 | 0 | 0 |
| T3-098 | 1 | 1 | 0 | 0 | 0 |
| T3-011 | 1 | 1 | 0 | 0 | 0 |
| T3-003 | 1 | 1 | 0 | 0 | 0 |
| T3-181 | 1 | 1 | 0 | 0 | 0 |
| T3-021 | 1 | 1 | 0 | 0 | 0 |
| T3-005 | 1 | 1 | 0 | 0 | 0 |
| T3-086 | 1 | 0 | 0 | 0 | 1 |
| T3-052 | 1 | 1 | 0 | 0 | 0 |
| T3-092 | 1 | 1 | 0 | 0 | 0 |

## Boundary pairs and their items

Each pair below is carried in `boundary_ruling` on the items listed. "Paragraph" says whether `boundaries.md` holds the pair's paragraph.

- **T3-033|T3-041** (25 items; paragraph yes; scheme-ambiguous 19, genuine-joint 3, item-is-a-bag 1, author-disagrees 1, author-error 1): truestl t02, cmu t01, metalgearsolid t04, muse t01, aoe2 t04, denmark t10, eagles t02, eve t03, gameofthrones t02, indieheads t13, KState t01, math t02, nuclearthrone t01, portal t02, purplecorner t03, rust t09, simonfraser t04, splatoon t03, suomi t02, touhou t08, ufl t01, blackmirror t05, borderlands t04, empiredidnothingwrong t11, winnipegjets t11
- **T3-038|T3-041** (16 items; paragraph yes; genuine-joint 7, scheme-ambiguous 7, item-is-a-bag 2): sakuragakuin t01, jerma985 t03, nuclearthrone t05, bobross t01, cavestory t01, dota2 t11, madokamagica t01, msu t02, parahumans t01, touhou t02, AyyMD t01, cubers t21, cubers t25, samuraijack t10, suomi t27, yumenikki t01
- **T3-004|T3-041** (15 items; paragraph yes; genuine-joint 9, scheme-ambiguous 5, author-disagrees 1): ubreddit t03, funhaus t01, greyblob t02, nin t03, radiohead t01, skyrim t02, unturned t09, bindingofisaac t03, DatBoi t04, factorio t09, placetardis t02, ProfessorLayton t02, starlightstage t12, borderlands t02, enterthegungeon t03
- **T3-002|T3-033** (10 items; paragraph yes; genuine-joint 7, item-is-a-bag 2, scheme-ambiguous 1): chicubs t09, DiamondClub t01, foxes t01, hawks t05, kanye t01, schoolidolfestival t04, stardustcrusaders t01, unturned t03, wallstreetbets t01, warframe t01
- **T3-004|T3-070** (9 items; paragraph yes; genuine-joint 8, scheme-ambiguous 1): crusaderkings t02, penguins t03, udub t01, drumcorps t06, kanye t05, Okami t06, pebble t04, placesnek t04, portal t03
- **T3-002|T3-038** (9 items; paragraph yes; item-is-a-bag 5, genuine-joint 4): bostonbruins t02, enterthegungeon t01, ethoslab t01, forsen t01, habs t02, nyjets t04, the_pack t01, winnipegjets t01, wow t17
- **T3-004|T3-038** (8 items; paragraph yes; genuine-joint 5, scheme-ambiguous 3): portal t01, timbers t02, AvoArmy t01, calgaryflames t01, uoft t08, bitcoin t02, detroitlions t04, paydaytheheist t02
- **T3-038|T3-070** (7 items; paragraph yes; genuine-joint 7): berkeley t03, gameattack t04, virginiatech t03, planetside t08, bdsm t01, re_zero t06, formula1 t06
- **T3-004|T3-020** (7 items; paragraph yes; genuine-joint 7): blackmirror t02, borussiadortmund t03, minecraft t04, kingdomhearts t12, oneshot t01, nightinthewoods t02, utaustin t01
- **T3-004|T3-169** (6 items; paragraph yes; genuine-joint 3, scheme-ambiguous 3): bisexual t03, monstercat t06, drawhelix t05, farmcarrots t08, neopets t14, wine t08
- **T3-004|T3-033** (6 items; paragraph yes; scheme-ambiguous 3, genuine-joint 3): frc t01, nlsscirclejerk t02, WPI t01, redhotchilipeppers t03, starlightstage t09, yugioh t04
- **T3-020|T3-022** (1 items; paragraph yes; genuine-joint 1): frc t03
- **T3-020|T3-033** (1 items; paragraph yes; genuine-joint 1): tetris t01

## Agreement before and after

Before is the two readers against each other over the packet's 500 items. After is each reader against the ruling over the 493 items not unresolved. The figure after is not a reliability figure: it is agreement with an adjudication I performed.

| | mean Jaccard | primary match |
|---|---|---|
| before (reader against reader) | 0.475 | 0.598 |
| after (each reader against the ruling) | 0.583 | 0.637 |

## Stage B2's predicted pairs

The next list gives, for each of `confusions.md`'s nineteen pairs, the packet's items whose two readers put the pair's themes as their primaries.

- pair 1, T3-005|T3-021: 0
- pair 2, T3-010|T3-149: 0
- pair 3, T3-001|T3-023: 0
- pair 4, T3-028|T3-070: 0
- pair 5, T3-004|T3-020: 5
- pair 6, T3-002|T3-033: 10
- pair 7, T3-015|T3-075: 0
- pair 8, T3-004|T3-070: 6
- pair 9, T3-009|T3-073: 0
- pair 10, T3-004|T3-038: 9
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

- T3-004|T3-041: 12
- T3-033|T3-041: 11
- T3-002|T3-033: 10 (predicted)
- T3-004|T3-033: 9
- T3-004|T3-038: 9 (predicted)
- T3-002|T3-038: 9
- T3-020|T3-033: 7
- T3-038|T3-041: 7
- T3-038|T3-070: 7
- T3-004|T3-070: 6 (predicted)

## Unresolved items

- tampabaylightning t09: scheme-ambiguous, T3-017 must_show
- h3h3productions t30: scheme-ambiguous, T3-049 must_show
- quebec t16: author-disagrees,  
- davidbowie t04: scheme-ambiguous, T3-033 must_show
- AMD t20: scheme-ambiguous, T3-003 must_show
- bahrain t09: author-disagrees,  
- samuraijack t25: scheme-ambiguous, T3-052 must_show

