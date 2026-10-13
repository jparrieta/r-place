# Packet 3, the figures (stage B4 section 9)

Written by `out/_analysis/b4_packet_summary.py` from `disagreements.jsonl`. Items ruled: 500.

## The taxonomy split

The next table counts the packet's rulings by taxonomy value, overall and by J's class of the item.

| taxonomy | all | class 3 | class 4 | class 5 |
|---|---|---|---|---|
| scheme-ambiguous | 106 | 85 | 21 | 0 |
| item-is-a-bag | 76 | 57 | 19 | 0 |
| reader-error | 3 | 3 | 0 | 0 |
| author-error | 45 | 0 | 40 | 5 |
| genuine-joint | 231 | 231 | 0 | 0 |
| author-disagrees | 39 | 0 | 37 | 2 |
| total | 500 | 376 | 117 | 7 |

- unresolved: 7 (1.4%)
- named_neither: 280 (56.0%)
- author-error: 45; author-disagrees: 39
- rulings corrected in place after writing: 20 (hawks t05, stardustcrusaders t01, catalonia t07, bostonbruins t02, enterthegungeon t01, ethoslab t01, forsen t01, habs t02, nyjets t04, the_pack t01, winnipegjets t01, wow t17, bisexual t04, ManningPlace t05, KState t04, rainbowgrid t01, dofus t01, kpop t05, skyrim t03, teamcube t04)

## Fields by ambiguity

The next list counts the scheme-ambiguous rulings by the field whose sentence failed to decide.

- must_show: 54
- must_not_show: 26
- decide_when_both: 3
- discriminators: 23

## Third-order themes by ambiguity

The next table ranks the themes whose sentence failed to decide, with the fields.

| theme | rulings | must_show | must_not_show | decide_when_both | discriminators |
|---|---|---|---|---|---|
| T3-004 | 25 | 3 | 12 | 0 | 10 |
| T3-033 | 25 | 22 | 1 | 0 | 2 |
| T3-038 | 11 | 9 | 2 | 0 | 0 |
| T3-020 | 8 | 0 | 6 | 0 | 2 |
| T3-041 | 7 | 2 | 4 | 0 | 1 |
| T3-026 | 7 | 2 | 0 | 2 | 3 |
| T3-055 | 3 | 3 | 0 | 0 | 0 |
| T3-082 | 3 | 0 | 1 | 0 | 2 |
| T3-002 | 2 | 0 | 0 | 0 | 2 |
| T3-074 | 2 | 2 | 0 | 0 | 0 |
| T3-060 | 2 | 1 | 0 | 1 | 0 |
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

- **T3-033|T3-041** (25 items; paragraph yes; scheme-ambiguous 20, genuine-joint 3, item-is-a-bag 1, author-disagrees 1): truestl t02, cmu t01, metalgearsolid t04, muse t01, aoe2 t04, denmark t10, eagles t02, eve t03, gameofthrones t02, indieheads t13, KState t01, math t02, nuclearthrone t01, portal t02, purplecorner t03, rust t09, simonfraser t04, splatoon t03, suomi t02, touhou t08, ufl t01, blackmirror t05, borderlands t04, empiredidnothingwrong t11, winnipegjets t11
- **T3-038|T3-041** (16 items; paragraph yes; genuine-joint 7, scheme-ambiguous 7, item-is-a-bag 2): sakuragakuin t01, jerma985 t03, nuclearthrone t05, bobross t01, cavestory t01, dota2 t11, madokamagica t01, msu t02, parahumans t01, touhou t02, AyyMD t01, cubers t21, cubers t25, samuraijack t10, suomi t27, yumenikki t01
- **T3-004|T3-041** (14 items; paragraph yes; genuine-joint 8, scheme-ambiguous 6): ubreddit t03, ElderScrolls t05, funhaus t01, nin t03, radiohead t01, skyrim t02, bindingofisaac t03, DatBoi t04, factorio t09, placetardis t02, ProfessorLayton t02, starlightstage t12, borderlands t02, enterthegungeon t03
- **T3-002|T3-033** (10 items; paragraph yes; genuine-joint 7, item-is-a-bag 2, scheme-ambiguous 1): chicubs t09, DiamondClub t01, foxes t01, hawks t05, kanye t01, schoolidolfestival t04, stardustcrusaders t01, unturned t03, wallstreetbets t01, warframe t01
- **T3-004|T3-070** (9 items; paragraph yes; genuine-joint 8, scheme-ambiguous 1): crusaderkings t02, penguins t03, udub t01, drumcorps t06, kanye t05, Okami t06, pebble t04, placesnek t04, portal t03
- **T3-002|T3-038** (9 items; paragraph yes; item-is-a-bag 5, genuine-joint 4): bostonbruins t02, enterthegungeon t01, ethoslab t01, forsen t01, habs t02, nyjets t04, the_pack t01, winnipegjets t01, wow t17
- **T3-004|T3-169** (8 items; paragraph yes; genuine-joint 4, scheme-ambiguous 4): bisexual t03, greyblob t02, monstercat t06, unturned t09, drawhelix t05, farmcarrots t08, neopets t14, wine t08
- **T3-004|T3-038** (8 items; paragraph yes; genuine-joint 5, scheme-ambiguous 3): portal t01, timbers t02, AvoArmy t01, calgaryflames t01, uoft t08, bitcoin t02, detroitlions t04, paydaytheheist t02
- **T3-038|T3-070** (7 items; paragraph yes; genuine-joint 7): berkeley t03, gameattack t04, virginiatech t03, planetside t08, bdsm t01, re_zero t06, formula1 t06
- **T3-004|T3-020** (7 items; paragraph yes; genuine-joint 7): blackmirror t02, borussiadortmund t03, minecraft t04, kingdomhearts t12, oneshot t01, nightinthewoods t02, utaustin t01
- **T3-004|T3-033** (6 items; paragraph yes; scheme-ambiguous 3, genuine-joint 3): frc t01, nlsscirclejerk t02, WPI t01, redhotchilipeppers t03, starlightstage t09, yugioh t04
- **T3-020|T3-033** (1 items; paragraph yes; genuine-joint 1): tetris t01

## Agreement before and after

Before is the two readers against each other over the packet's 500 items. After is each reader against the ruling over the 493 items not unresolved. The figure after is not a reliability figure: it is agreement with an adjudication I performed.

| | mean Jaccard | primary match |
|---|---|---|
| before (reader against reader) | 0.475 | 0.598 |
| after (each reader against the ruling) | 0.473 | 0.535 |

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

