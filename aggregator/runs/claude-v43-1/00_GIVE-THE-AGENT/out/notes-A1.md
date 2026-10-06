# Notes, stage A1

Target length: under 3,500 words with the block lists. Written at leg A1a, 2026-10-06. The parts the stage file asks for at the end (what this material is, three things expected and not found, the one room that fits nothing, the canvas lines against the `doing` lines, the close reports of later legs) are appended at the last block and at A1c.

## Written before reading

### The order and the blocks

I read the rooms in a seeded random order: Python's `random.Random(20261006).shuffle` over the 705 room names sorted, cut into blocks of about 3 MB. The bytes are the ones `mem.py room --size` counts (forest, concept lines, second-order themes). A room above the cap is a block of its own, and only r/counting is. The script is `out/_analysis/a1_order.py`, declared in `departures.jsonl`. Its output, with input hashes, is `out/_analysis/a1_order-A1.txt`. The order as the tools read it is `out/order-A1.txt`.

Why this order. A sorted order puts capitalised and numeric names first and reads rooms with related names together by accident (placeX, uX, the K-pop rooms). An order by onset or by canvas area would build my prior from one side of the contrast or from the outcome. A shuffle spreads big and small rooms, early and late rooms, across every block, so the first blocks set a prior from a fair draw. The cost: a lead between two rooms (r/denmark and r/sweden, both in block 07) waits until both are read. `leads-A1.jsonl` carries a lead until then.

The census is 62,105,060 bytes by this count, in 19 blocks:

- 01, 2.93 MB, 53 rooms: anarchism, tokyo, buffalobills, greyblob, morrowind, megaman, AprilKnights, witcher, heyyea, furry, duckgame, egypt, riskofrain, flashtv, homestuck, ukraine, ik_ihe, churchofhelix, unitedkingdom, detroitredwings, terraria, calgaryflames, austria, jerma985, littlewitchacademia, necrodancer, httyd, liverpoolfc, monstercat, madokamagica, bahrain, mamamoo, strangerthings, babymetal, auburn, PinkVomitMonster, the_pack, anime, FloydVsVoid, wales, cfb, watchmen, ProfessorLayton, TheAdventuresofTintin, buffalowizards, lofihiphop, drugs, uva, qotsa, drumcorps, Dustforce, tagpro, uvic
- 02, 2.99 MB, 48 rooms: placecanada, konosuba, shield, minnesotavikings, completeanarchy, hellointernet, cloud9, Rainbow6, cirkeltrek, faeria, alberta, monsterhunter, DatBoi, stlouis, uwaterloo, OKState, homelab, monero, Redox, vocaloid, australia, hentai, DCFU, dwarffortress, signal, nuclearthrone, luciomains, czech, WPI, colorado, ubc, giantbomb, serbia, kpop, norge, ScottPilgrim, teslamotors, carletonu, earthbound, batman, kindafunny, nonbinary, mechanicalkeyboards, loltyler1, seahawks, zelda, bobross, phish
- 03, 2.97 MB, 62 rooms: texastech, frc, spelunky, ghibli, pepe, polska, linux, yerbamate, skyrim, dallasstars, ravens, iceland, GuardiansOfDatBoi, CryptoFR, GuildWars2, oman, columbia, ftlgame, twitchplayspokemon, Bravenewbies, ohio, darksouls, lovelive, Madeon, minecraft, battlecats, freedomplanet, Honduras, xcom, harrypotter, glasgow, uruguay, survivor, ukplace, sixers, Lugarix, aceattorney, hongkong, costa_rica, SwissNeutralityZone, maryland, aeon, sakuragakuin, mcgillrobotics, futurama, england, nyu, kerbalspaceprogram, evex, n64, latvia, placeportalpattern, MonkeyIsland, Homura, quq, toolband, peterdraws, placeDE, bardmains, lsu, AyyMD, malta
- 04, 2.95 MB, 44 rooms: anime_irl, iastate, chess, day9, wildhockey, monalisaclan, ElSalvador, partyparrot, catholicism, thesimpsons, SydneyFC, kamenrider, diablo, haskell, frankocean, ethereum, vermont, theitalyplace, factorio, placetardis, rush, rickandmorty, smite, hearthstone, drawhelix, ice_poseidon, compsoc, mexico, giivasunner, thepointing, 4chan, genderfluid, utahjazz, ssbpm, borderlands, physical_removal, Temple, radiohead, korea, tampabaylightning, spacexmasterrace, Clannad, aoe2, bees
- 05, 2.93 MB, 34 rooms: osu, samuraijack, Dorset, virginiatech, nightinthewoods, norway, chicago, ss13, greenlattice, paydaytheheist, uiuc, NieR, masseffect, ducks, colombia, albania, rit, mit, truestl, bostonceltics, roosterteeth, france, utaustin, mariokart, kcroyals, redpandas, natsume, osugame, hawks, TheGreatGreenBox, FlipnoteStudio3D, heroesofthestorm, indieheads, neopets
- 06, 3.00 MB, 37 rooms: wow, habs, MMA, placesnek, azores, k_on, eder, landry, polyamory, berkeley, katawashoujo, thebluecorner, naruto, parahumans, loliconsunite, ethoslab, Pigifs, globaloffensive, miamidolphins, chicubs, bangtan, gorillaz, germany, DiamondClub, pokemon, vim, TreePlace, evedreddit, gravityfalls, hunterxhunter, GrowTheTree, bih, placehfarts, furry_irl, spongebob, asktransgender, soylent
- 07, 2.95 MB, 36 rooms: porterrobinson, fullcommunism, placehearts, lexington, simonfraser, denmark, slovenia, texans, wine, halo, TheB1G, ripcity, flyers, bulgaria, wsu, japan, formula1, indonesia, bannedfromanime_irl, nin, btc, acecombat, canada, bostonbruins, crystalclear, sweden, luxembourg, bindingofisaac, h3h3productions, ChronoTrigger, davidbowie, uoft, transgender, picturegame, falcons, Jamaica
- 08, 3.00 MB, 30 rooms: TheFarLeftSide, scp, bisexual, ireland, stardustcrusaders, greenbaypackers, math, overwatch, metalgearsolid, rocketbeans, lost, metalcore, bangladesh, pansexual, opticgaming, rocketleague, ReBoot, sabres, lego, foxes, buffalo, ockytop, lebanon, nVade, vinesauce, GranColombia, gatech, edmontonoilers, popheads, epublica
- 09, 2.91 MB, 51 rooms: southafrica, nascar, schoolidolfestival, sonicthehedgehog, sadboys, python, KState, AMD, dbz, 49ers, ufl, FlaggyFlag, yumenikki, cardinals, Moondye7, asexuality, redhotchilipeppers, THE_R, israel, rojava, eesti, theexpanse, italy, pebble, elitedangerous, Fez, pgang, chile, mls, penguins, hyperlightdrifter, ManningPlace, torontoraptors, vegan, spacex, PORTUGALCARALHO, warthunder, thailand, touhou, redvsblue, magictcg, mordhau, achievement_hunter, metroid, corridor, npr, UMiami, warriors, sooners, tenma, timbers
- 10, 2.93 MB, 50 rooms: greece, UPenn, COSI, baylor, rhythmheaven, seolhyun, stargate, sheffield, rangers, bretagne, leafs, liquicity, animalcrossing, startrek, feedthebeast, PokemonSage, superman, littlebusters, puzzleanddragons, cgpgrey, hatsune, uofmn, coldplay, foxstevenson, hungary, suomi, bakchodi, starcitizen, dankmemes, mcgill, worldpowers, southpark, patriots, twice, texas, greenland, EraseThePlace, chelseafc, NewMexico, Cornwall, anarcho_capitalism, TsundereSharks, gameattack, AceOfAngels8, oneshot, cmu, TeamYellowPlace, Peru, neu, warframe
- 11, 2.86 MB, 21 rooms: danganronpa, stevenuniverse, india, thesilphroad, farmcarrots, TransFlagPlace, titanfall, xenoblade_chronicles, totallynotrobots, straya, UNLincoln, DestinyTheGame, udub, finland, clubpenguin, leagueoflegends, sakartvelo, GreenEmpire, malaysia, kurdistan, PurplePixels
- 12, 2.83 MB, 35 rooms: newzealand, de, hsv, MiamiHurricanes, dmt, ucf, NovaScotia, chibears, cubers, romania, gameofthrones, anarchocapitalism, pakistan, dragonquest, anaheimducks, armenia, donaldglover, SquareSpiral, nbaspurs, yugioh, aggies, telegram, orderofthebluecorner, enterthegungeon, teamcube, empiredidnothingwrong, ontario, worldoftanks, weezer, shitredditsays, kilian, eve, CelticFc, clashroyale, argentina
- 13, 11.17 MB, 1 room: counting
- 14, 2.68 MB, 32 rooms: rutgers, shishamo, belgium, croatia, onepunchman, paranatural, fivenightsatfreddys, kingdomhearts, archlinux, TheHulk, polandball, runescape, splatoon, armok, starcraft, satania, cuboulder, nerf, bitcoin, kanye, smashbros, ubreddit, vietnam, undertale, floridagators, Dominican, lifeisstrange, rust, canucks, PUBATTLEGROUNDS, mindcrack, azerbaijan
- 15, 2.95 MB, 37 rooms: theblackvoid, eagles, rainbowgrid, starlightstage, funhaus, fireemblem, FaroeIslands, nintendo, uiowa, mysterydungeon, CKCrusaders, tinytardis, berserk, twitch, kuwait, transformers, nyjets, thenetherlands, palestine, AmericanFlaginPlace, zootopia, CSUFoCo, tetris, asexual, oltp, switzerland, starbound, pitt, futanari, mizzou, Slovakia, raocow, singapore, TeamDignitas, taiwan, criticalrole, OnePiece
- 16, 2.98 MB, 46 rooms: mylittlepony, gamindustri, Mario, latin, paladins, sbu, quebec, poland, msu, stlouisblues, shrooms, ultrahardcore, portal, hoodr, trees, nlsscirclejerk, OneTrueEmilia, philippines, afip, livecounting, yuyuyu, paragon, AvoArmy, miraculousladybug, DevonUK, catalonia, muse, Produce101, starvstheforcesofevil, re_zero, VelvetUnderground, esperanto, wallstreetbets, calvinandhobbes, pcmasterrace, aeskwadraat, swordartonline, streetfighter, oneplus, OrderOfTheKoi, PlaceNL, PinkUnion, scotland, austriahungary, gratefuldead, thetreesnetwork
- 17, 2.44 MB, 35 rooms: detroitlions, portugal, Villanova, russia, FinalFantasy, pathofexile, adventuretime, araragi, HomestarRunner, sips, bdsm, purplecorner, spain, cavestory, placestart, geometrydash, guatemala, GabrielDropout, starryknights, ibo, rwby, wholesomememes, kirby, tf2, wario, twentyonepilots, brasil, purdue, montenegro, GreenCorner, unturned, Thegreatblackhole, cowchop, edboxes, turkey
- 18, 2.54 MB, 35 rooms: 2007scape, prequelmemes, yogscast, Goodboye, denverbroncos, lakers, bigbang, destiny, planetside, marvel, androidgaming, forsen, catalunya, Okami, notredame, TheID, ElderScrolls, Northwestern, parabola, uofm, borussiadortmund, apocalypserising, crusaderkings, aromantic, pusheen, blackmirror, Summit1G, AcePlace, daftpunk, lithuania, neutralmilkhotel, stardewvalley, parrots, europe, RelientK
- 19, 2.11 MB, 18 rooms: ainbowroad, dota2, Braveryjerk, WisconsinBadgers, FederationPlace, seventeen, rpi, traaaaaaannnnnnnnnns, rotmg, dofus, snsd, clg, reddevils, gameboy, fxKorea, winnipegjets, Russiaclan, predators

Block 13, r/counting, is 11.17 MB, almost four times the cap. One leg may not finish it. If it does not, I will close at a safe stop inside the room and say so. A room has one note, so its note waits for the room's end.

### The contrast

Written whole in `out/contrast.md`. Early side: first coded turn after hour 0 and before hour 3, 131 rooms. Late side: first coded turn after hour 48, 61 rooms. r/italy and r/yogscast stand on neither side, because their first coded turn comes before the canvas opened. The two sides differ a hundredfold in room size (median `items_in_window` 5067 against 33), so a held-size comparison travels with the contrast: rooms with 156 to 2770 items, 41 early against 12 late.

### Three sentences on what I expect

Most rooms will show one burst of calls, coordinates and reports in the first day or two, then a long tail of defence and of looking back, and the coordinating turns will stop near hour 73 with little after. The fights the rooms name will be with their canvas neighbours more than with distant rivals, and the deals will be about borders and space, struck in the open thread or sent off to Discord. The goal will be settled in the first hours by one person's call, a flag, a logo or a character, and changed afterwards only under pressure from a neighbour or a loss of ground, rarely by argument inside the room.

## The checks of section 1

### The tools

`mem.py help` ran, and every read verb ran once with `--stage A1` on r/denmark. They were room (with and without `--no-canvas`, `--size`, `--json`), case, brief, forest (whole and one thread), when, canvas, compare, note, codes (`--sub`, `--second`, `--grep --by-room`), theme, themes, after, pairs, facts (`--field`, `--summary`, `--where`, `--nulls`, `--slope`), notes, progress (and `--plan`), next, neighbours (one room and `--summary`), scheme, where, rooms, contrast, adaptations, finding, findings, question, table, view, wiki, shelf (and `--list`), contract, diff-scheme, diff-model, diary, asks and audit. Each returned a page, or refused with a reason because its file does not exist yet (scheme, where, rooms, adaptations, finding, question, table, diff-scheme, diff-model). mint, idea, place, unplace and adjudicate refuse at A1, as the stage file says. One `cite.py --room denmark --code c0002` call resolved the quote. No tool failed. The logs are `_mem_reads-A1.jsonl` and `_cite_reads-A1.jsonl`.

### The validator self-test

`validate.py --self-test` reports 0 failures in 137 checks. Every stage from A1 to E2 has a clean fixture that passes and planted defects that each fire once, so every stage of the run has a close-check. The full report is `out/_analysis/validate-self-test-A1.txt`, and its summary is pasted here:

```
A1 the clean fixture clean; fired: a room of the analysed set unnoted, a note lacking a fixed line, carrying names an unknown code, organizing_end short a room, work lost with nothing said, an end hour the store does not give, a drop outside the frame, a room opened and not logged, no concept_reach_threshold, a room skipped in the order, a room's concepts never read, a lead without why, the order short a room
B1 clean; 16 planted, all fired (exemplar a label; exemplar nobody said; family the index lacks; theme never minted; main theme on one room; member the store lacks; theme named for a problem; finding with a bad warrant; split without prompt; no saturation record; main theme on one episode seen twice; episode judged by likeness; no exemplar rule in prior.md; room skipped in the seeded order; floor unlike in no named way; placement the kinds ledger never met; walk unfinished)
B2 clean; 3 fired. B3 clean; 4 fired. B4 clean; 5 fired. C1 clean; 6 fired. C2 clean; 6 fired. C3 clean; 3 fired. C4 clean; 4 fired. C5 clean; 6 fired.
D1 clean; 5 fired. D2 clean; 5 fired. D3 clean; 7 fired. D4 clean; 10 fired. D5 clean; 8 fired. D6 clean; 4 fired.
E1 clean; 10 fired. E2 clean; 3 fired.
self-test: 0 failures
```

### The census

`package/FRAME.md` gives copy date 2026-10-04, 705 rooms, hash `51513b1e06415456d514918fe855d80d5e1aa99eb36bed7d9af7f2a7fd3cbe8d`. The count agrees across `store/rooms.jsonl` (705), the room folders under `package/` (705), the distinct rooms in `store/codes.jsonl` (705) and in `store/themes.jsonl` (705). N = 705. `mem.py audit` notes that the frame hash covers the handler's input forests, which the package does not hold, so the hash was not recomputed here.

### One run per room

All 705 room folders hold the six files (brief.md, case.md, codes.jsonl, themes.jsonl, threads.jsonl, pointers.jsonl) and a forest in `trees/` (`mem.py audit`).

### The canvas

All six canvas fields are on all 705 rooms in `rooms.jsonl`. `canvas_centre` and `canvas_ring` are null in one room, r/tenma. `canvas/artworks.jsonl` reads: 1,473 artworks, each with id, name, centre, pixels, placements, placements by hour 0 to 96, distinct placers, first and last hour, and its subreddits.

- **r/tenma** has `canvas_entries` 0, `canvas_area_px` 0, no linked artwork and no row in `pixels.csv`. A room in the census with no canvas line is a defect, and it is in `defects.jsonl`. Its coded record is a real call ("Come and help make history with us on /r/place!", thread 62xbmf at hour 34.68). The room stays in the analysed set. What it made cannot be read from the canvas.
- `canvas_area_px` over 705 rooms: min 0, q1 236, median 586, q3 1537, max 106,170.5, mean 1,795.6.
- The share of each room's own artwork placed by the people who wrote in it (`px_window_share`, from `pixels.csv`) over 704 rooms (null for r/tenma): min 0, q1 0.048, median 0.111, q3 0.185, max 0.547. The share placed by the room's pre-event members (`px_pre_share`): min 0, q1 0.003, median 0.026, q3 0.079, max 0.547. Contract section 5 says what these are: what the drawing left behind and who among the room's writers placed it. A per-room rate is sound. A canvas-wide total is not, because regions overlap. Neither is a score.

### The clocks

`onset_first_code_hour`, `onset_last_code_hour` and `items_in_window` have no nulls in 705 rooms. `onset_first_code_hour` runs from -18.58 to 72.6 (q1 3.76, median 9.51, q3 24.82). No room has a first coded turn after hour 73. Two rooms have one before hour 0: r/italy at -1.14, and r/yogscast at -18.58, where the turn is about streaming keys and not the canvas. The clock therefore dates the first coded turn, not the first canvas turn, wherever a coder coded talk from before the event. `onset_last_code_hour` runs from 5.36 to 100.9 (q1 78.91, median 89.98, q3 95.53). r/archlinux's last coded turn (archlinux/c0249) is at hour 100.9, past the window's end. That is in `defects.jsonl`.

The two clocks of ending: the last `last_hour` over a room's threads in `threads.jsonl` against `onset_last_code_hour`. No room has a null on either. The gap (last thread hour less last coded hour) has min 0.00, median 0.00 and max 9.87. No room's last code comes after its last thread hour. 79 rooms have their last coded turn before hour 73, and the same 79 have their last thread hour before 73. Two rooms have a thread whose last hour passes 97.

### Off the record

`n_off_platform` over 705 rooms: min 0, q1 2, median 4, q3 10, max 88, mean 7.857. 66 rooms have none. The rooms with the most: dankmemes 88, thesilphroad 78, overwatch 62, fivenightsatfreddys 59, pcmasterrace 53, smashbros 52, europe 50, prequelmemes 49, 2007scape 48, argentina 48, theblackvoid 48, MMA 47. It is a count of mentions the coder recorded, never a share of the work done elsewhere.

### The nulls

`coded_authors` is 0, and `top1_share` and `herfindahl` are null, in 3 rooms: r/nonbinary, r/oltp, r/wario. Each has one coded turn by a deleted author. Any claim that rests on concentration carries the denominator 702 of 705.

### The instrument's shape, recomputed

Over all 705 rooms (all have both values above 0), log-log OLS:

- First-order concepts on `items_in_window`: slope 0.530 (intercept 1.069, r² 0.722).
- Second-order themes on `items_in_window`: slope 0.231 (intercept 0.765, r² 0.555).
- Second-order themes on concepts: slope 0.429 (intercept 0.328, r² 0.745).

The six figures for the second-order theme count:

- Against `items_in_window`: raw Pearson r 0.352, log r 0.745, rank rho 0.733.
- Against the concept count: raw r 0.464, log r 0.863, rank rho 0.822.

A room a hundred times larger carries about eleven times the concepts and under three times the second-order themes. The second-order tier is close to a fixed-width summary, as contract section 5 says.

**Concept reach.** The stage file defines it as the share of a room's concepts with a `theme_id`. All 115,388 concepts carry a `theme_id` that names a theme of their room, and every one is listed in that theme's `code_ids` (`out/_analysis/a1_checks2-A1.txt`). The share is 1.000 in all 705 rooms. The smallest quartile by `items_in_window` (176 rooms, 1 to 151 items) has median 1.000, and no decile and no running cut falls below it. The measure as written cannot yield a threshold. That is in `defects.jsonl`, and I asked the principal investigator about it as QA1-001.

concept_reach_threshold: 0 (items_in_window). Every room is read at concept level, not only through its second-order themes, at C2 to D3 (`cite.py` reaches concepts in every room), and stage E1 reads unplaced concepts in every room. The reason: the measure gives no cut, and the slopes show the second-order tier compressing large rooms most (0.231 against 0.530). A cut at 0 is the setting that cannot miss a room. This rests on QA1-001. If the answer names another measure, I recompute it and declare the threshold again by a logged departure.

QA1-001 answered at leg A1b-02: the principal investigator confirms the reading and the threshold of 0. No substitute measure is to be invented. The concept reach measure gives no cut in this store: every concept carries a theme_id, so the share is 1.0 in all 705 rooms. Every room is read at concept level from C2 to D3, and E1 reads unplaced concepts too. The slopes and the six figures above stand as reported.

### The concepts and the themes

The sum of per-room `codes` in `rooms.jsonl` is 115,388. `store/codes.jsonl` has 115,388 lines, and `themes.jsonl` `n_codes` sums to 115,388. The coder's own count: the coders' `package/<sub>/codes.jsonl` lines number 115,563, and less the 175 retractions that is 115,388, which agrees. `n_codes_coder` in `themes.jsonl` sums to 115,455, and less 175 that is 115,280, 108 short. The field excludes retractions already in 32 rooms (fully in 30, partly in kcroyals and pcmasterrace) and includes them in the rest. That is in `defects.jsonl`. The coder's count holds when it is taken from the coders' files.

Second-order themes: 7,844 in total. No room has none, 15 have one and 14 have two (29 with one or two, as `counts.py` says). Per room, `rooms.jsonl` `themes` and `codes` agree with the store lines in every room.

### Retracted concepts

`README-store.md` says 175 were dropped at build. `store/_retracted.jsonl` has 175 lines, `_build.json` `codes_retracted_dropped` is 175, and the coders' own files carry 175 retracted lines. All agree (`mem.py audit`).

### The store against the package

`counts.py`: 115,388 concepts, 7,844 second-order themes and 705 coded rooms. These equal the collections exactly.

The store's build figures, recomputed (`mem.py audit`; `out/_analysis/a1_checks-A1.txt`):

- `_unjoined.jsonl` holds 38 lines. 38 concepts have an `item_id` that `items.jsonl` lacks, 38 have state `unjoined`, and the recomputed set equals the file's set. Agrees.
- Communities 705, codes 115,388, themes 7,844, threads 42,906, items 158,227, coded items 109,769, bridge items 26,830, pointers 20,110, briefs 705: `_build.json` and the store agree on each.
- The forest headers over `trees/`, summed: 42,906 threads given, all with a code. Items 531,851: coded 109,807, bridge 28,350, removed 617, dropped 393,077. These equal the sums of `rooms.jsonl` `forest.*` exactly. They do not equal `items.jsonl`. The store holds 158,227 items: coded 109,769, bridge 26,830, removed 617, and 21,011 in a state `collapsed` that `README-store.md` does not name. `README-store.md` says the store carries every item of each coded thread. The forests count 531,851. The forests' coded items exceed the store's by 38, the same number as the unjoined concepts. Their bridge items exceed the store's by 1,520.

What I compute wins: the forests hold 531,851 items, and the store holds 158,227 of them, without the 393,077 the forests mark as dropped. Both figures go to stage E1. The undocumented state is in `defects.jsonl`.

### The analysed set

`dropped.jsonl` is written and empty. The census is 705, the analysed set 705, dropped 0. `counts.py` was re-run after the screen: second-order themes to be placed at B3, 7,844. Nothing was dropped, so nothing fell.

## The screen (section 2)

I read the rooms whose coder coded one thread: 46 rooms, and none has zero. I read the forest of every one. I read the case account of r/wario, r/nonbinary, r/oltp, r/tenma and r/Bravenewbies, and the opening of r/wario's account in full. No room has a first coded turn after hour 73. Every one of the 46 wrote about the canvas while it was open: a call for help, coordinates, a report of placing, a fight over a border, or at least a notice of its own art. None is a room that wrote nothing about the event, so none is a negative screen. Contract section 5 says a room that tried and failed is a case. The 46: Bravenewbies, COSI, Clannad, Cornwall, DiamondClub, Dorset, FlipnoteStudio3D, OKState, PokemonSage, Produce101, ReBoot, Redox, RelientK, UMiami, UNLincoln, UPenn, VelvetUnderground, aromantic, azerbaijan, azores, bees, bigbang, buffalowizards, carletonu, cgpgrey, churchofhelix, crystalclear, fxKorea, k_on, littlebusters, mamamoo, natsume, nonbinary, oltp, parabola, paranatural, peterdraws, sakartvelo, seolhyun, signal, tenma, vermont, wario, watchmen, wsu, yerbamate.

These rooms were kept against a doubt:

- **r/tenma.** It has no canvas line, so how it entered the census is unclear. Its record holds a call and a location ("She is right next to Satania"). Kept. The doubt is about the frame, not the room.
- **r/UNLincoln.** Its one coded thread (637pti, hour 72.08) calls a blackened logo "ours". The one reply says the logo is Northeastern's. Its canvas line links the artwork "Nebraska Huskers". Kept. The record may show a room that mistook another's work for its own, which is a finding about attention to the canvas, not grounds for a drop.
- **r/yerbamate and r/watchmen.** Each has one post showing its art on the canvas and no coordination. Kept. These may be rooms that did not organize, and contract section 1 asks to record such rooms, not to drop them.
- **r/Redox and r/azores.** They report a place on the canvas made elsewhere, in r/rust and on a Discord. Kept as rooms whose organizing may have crossed room boundaries.
- **r/yogscast.** Its first coded turn (h -18.58) is not about the canvas. Kept. Its onset is read from its first canvas turn (h 5.03) wherever the clock matters.
- **r/archlinux.** It has a coded turn at hour 100.9, past the window. Kept. The turn is one participant recalling that the organizing was "almost completely on Discord".

I did not read all 705 case accounts for doubts at the screen. Doubts the accounts raise will show in the reading, and a drop made then is logged, with the order re-run under a departure.

## What I read in leg A1a, from the logs

`_mem_reads-A1.jsonl` holds 148 calls at the close of this part of the leg: forest 48 (46 rooms of the screen and r/denmark twice), facts 34, codes 7, case 6, room 3, when 3, canvas 3, and one or two of every other verb. `_cite_reads-A1.jsonl` holds one call. No room has been read whole for a note yet. The next room is r/anarchism, block 01 (`mem.py next`).

## Close reports

### A1a

`validate.py A1`, then `done.sh A1` (20261006T122850Z). The first `done.sh` run refused because the head named "D3" in prose, which the link check read as a dimension id. I reworded it, and the second run closed.

```
stage A1:
  frame 705, dropped 0, analysed 705 : dropped.jsonl is written and empty, so the screen ran and dropped nothing
  room notes 0 over an analysed set of 705
  705 room(s) still to note; the stage closes when every room of the analysed set has one
  departures.jsonl carries 2 line(s)
  defects.jsonl carries 6 line(s)
0 errors (0 distinct shapes), 0 warnings
links: 1 files checked, all ids resolve
views regenerated for stage A1: 115388 concepts, 705 rooms, 0 ledger lines
leg A1a closed.
```

## Close report, leg A1b-01 (block 01), 2026-10-06

Block 01 read whole: 53 of 53 rooms noted. `validate.py A1` before the close:

```
stage A1:
  frame 705, dropped 0, analysed 705 : dropped.jsonl is written and empty, so the screen ran and dropped nothing
  room notes 53 over an analysed set of 705
  652 room(s) still to note; the stage closes when every room of the analysed set has one
  departures.jsonl carries 2 line(s)
  defects.jsonl carries 6 line(s)

0 errors (0 distinct shapes), 0 warnings
```

`done.sh A1`:

```
done.sh A1 leg=A1b-01 cut=none 20261006T131256Z
links: 1 files checked, all ids resolve
views regenerated for stage A1: 115388 concepts, 705 rooms, 0 ledger lines
leg A1b-01 closed. Stop now; the harness takes the snap and runs the probe.
```

The first validate run of this close failed with 7 errors: lead lines naming rooms outside the frame. Three were retargeted to frame rooms (nbaspurs, minecraft, colombia). Four were removed (exmormon, the_fack, unc, nerdfighters); those ties stay in the room notes. The diary records the change.

## Close report, leg A1b-02 (block 02), 2026-10-06

Block 02 read whole: 48 of 48 rooms noted, 101 of 705 in all. `validate.py A1` before the close:

```
stage A1:
  frame 705, dropped 0, analysed 705 : dropped.jsonl is written and empty, so the screen ran and dropped nothing
  room notes 101 over an analysed set of 705
  604 room(s) still to note; the stage closes when every room of the analysed set has one
  departures.jsonl carries 2 line(s)
  defects.jsonl carries 6 line(s)


0 errors (0 distinct shapes), 0 warnings
```

`done.sh A1`:

```
done.sh A1 leg=A1b-02 cut=none 20261006T135814Z
links: 1 files checked, all ids resolve
views regenerated for stage A1: 115388 concepts, 705 rooms, 0 ledger lines
leg A1b-02 closed. Stop now; the harness takes the snap and runs the probe.
```

Every `other` in the 17 leads added at the end of block 02 was checked against `order-A1.txt` before the close. Every item id in those leads and in the 31 new lexicon lines was checked through `cite.py`.

## Close report, leg A1b-03 (block 03), 2026-10-06

Block 03 read whole: 62 of 62 rooms noted, 163 of 705 in all. `validate.py A1` before the close:

```
stage A1:
  frame 705, dropped 0, analysed 705 : dropped.jsonl is written and empty, so the screen ran and dropped nothing
  room notes 163 over an analysed set of 705
  542 room(s) still to note; the stage closes when every room of the analysed set has one
  departures.jsonl carries 2 line(s)
  defects.jsonl carries 6 line(s)


0 errors (0 distinct shapes), 0 warnings
```

`done.sh A1`:

```
done.sh A1 leg=A1b-03 cut=none 20261006T143729Z
links: 1 files checked, all ids resolve
views regenerated for stage A1: 115388 concepts, 705 rooms, 0 ledger lines
leg A1b-03 closed. Stop now; the harness takes the snap and runs the probe.
```

Every `other` in the block 03 leads was checked against `order-A1.txt` when written. Several item ids were first written before being checked through `cite.py` or `lex.py` and were then corrected: four polska leads, the linux archlinux lead, the frc TeamYellowPlace lead, the peterdraws lead, one skyrim and two ftlgame lexicon lines. The diary records the correction and the rule that followed it.

## Close report, leg A1b-04 (block 04), 2026-10-06

Block 04 read whole: 44 of 44 rooms noted, 207 of 705 in all. `validate.py A1` before the close:

```
stage A1:
  frame 705, dropped 0, analysed 705 : dropped.jsonl is written and empty, so the screen ran and dropped nothing
  room notes 207 over an analysed set of 705
  498 room(s) still to note; the stage closes when every room of the analysed set has one
  departures.jsonl carries 2 line(s)
  defects.jsonl carries 6 line(s)


0 errors (0 distinct shapes), 0 warnings
```

`done.sh A1`:

```
done.sh A1 leg=A1b-04 cut=none 20261006T151753Z
links: 1 files checked, all ids resolve
views regenerated for stage A1: 115388 concepts, 705 rooms, 0 ledger lines
leg A1b-04 closed. Stop now; the harness takes the snap and runs the probe.
```

Ledgers at the close: lexicon 455 lines, running file 209 lines, leads 614 lines. Every `other` in the block 04 leads was checked against `order-A1.txt` before it was written. One lead was written with a wrong item id: rickandmorty to AcePlace with dfr3tho, which is the Void's peace offer (c0389). A corrected line with dfs2915 (c0439) was appended, and the diary records it. Three more artworks show region placements before hour 0: monalisaclan (h-15.23), radiohead (h-11.54) and aoe2 (h-0.66). That makes six cases. The case stays unfiled until the canvas manifest is read through the verbs.

## Close report, leg A1b-05 (block 05), 2026-10-06

Block 05 read whole: 34 of 34 rooms noted, 241 of 705 in all. `validate.py A1` before the close:

```
stage A1:
  frame 705, dropped 0, analysed 705 : dropped.jsonl is written and empty, so the screen ran and dropped nothing
  room notes 241 over an analysed set of 705
  464 room(s) still to note; the stage closes when every room of the analysed set has one
  departures.jsonl carries 2 line(s)
  defects.jsonl carries 6 line(s)


0 errors (0 distinct shapes), 0 warnings
```

`done.sh A1`:

```
done.sh A1 leg=A1b-05 cut=none 20261006T154533Z
links: 1 files checked, all ids resolve
views regenerated for stage A1: 115388 concepts, 705 rooms, 0 ledger lines
leg A1b-05 closed. Stop now; the harness takes the snap and runs the probe.
```

Ledgers at the close: lexicon 542 lines, running file 226 lines, leads 774 lines. A mid-leg run of `validate.py A1` found three errors. Two lead lines named rooms outside the frame: roosterteeth to evangelion, and kcroyals to mariners. They were removed from `leads-A1.jsonl`, and their full content is kept in the diary. The r/FlipnoteStudio3D carrying line named two ids. That room has only two concepts, so the line now repeats c0001, and the diary says why. One lead line had a wrong item id: rit to COSI with 633u1i, which is the RIT tiger over the Bruins logo. A corrected line with dfqtlqx was appended. At this close a python check over the whole leads file finds every `other` in the frame. No new artworks with placements before hour 0 turned up in block 05; the count stays at six.

## Close report, leg A1b-06 (block 06), 2026-10-06

Block 06 read whole: 37 of 37 rooms noted, 278 of 705 in all. `validate.py A1` before the close:

```
stage A1:
  frame 705, dropped 0, analysed 705 : dropped.jsonl is written and empty, so the screen ran and dropped nothing
  room notes 278 over an analysed set of 705
  427 room(s) still to note; the stage closes when every room of the analysed set has one
  departures.jsonl carries 2 line(s)
  defects.jsonl carries 6 line(s)


0 errors (0 distinct shapes), 0 warnings
```

`done.sh A1`:

```
done.sh A1 leg=A1b-06 cut=none 20261006T162122Z
links: 1 files checked, all ids resolve
views regenerated for stage A1: 115388 concepts, 705 rooms, 0 ledger lines
leg A1b-06 closed. Stop now; the harness takes the snap and runs the probe.
```

Ledgers at the close: lexicon 619 lines, running file 254 lines, leads 955 lines. A grep, sort and comm check over the whole leads file finds every `other` in `order-A1.txt`. Five names differ from the frame only in letter case (Landry, LoveLive, MLS, Monero, RocketLeague, all from block 01), and the validator accepts them. Ten lexicon or lead lines were appended with a wrong item id: globaloffensive 2, miamidolphins 2, pokemon 2, bangtan, GrowTheTree, gravityfalls and asktransgender. In each case the id came from a different code, or a placeholder was typed before the id was fetched. A corrected line was appended for each, the wrong lines stay as superseded, and the diary names every one. The gorillaz lead to r/eve named the wrong room for the Dreddit sign; a gorillaz-to-evedreddit lead was appended. Three more artworks show region placements before hour 0: thebluecorner (h-12.34), globaloffensive (h-13.62) and GrowTheTree (h-0.24). That makes nine cases. The case stays unfiled until the canvas manifest is read through the verbs.

## Close report, leg A1b-07 (block 07), 2026-10-06

Block 07 read whole: 36 of 36 rooms noted, 314 of 705 in all. `validate.py A1` before the close:

```
stage A1:
  frame 705, dropped 0, analysed 705 : dropped.jsonl is written and empty, so the screen ran and dropped nothing
  room notes 314 over an analysed set of 705
  391 room(s) still to note; the stage closes when every room of the analysed set has one
  departures.jsonl carries 2 line(s)
  defects.jsonl carries 6 line(s)


0 errors (0 distinct shapes), 0 warnings
```

`done.sh A1`:

```
done.sh A1 leg=A1b-07 cut=none 20261006T165355Z
links: 1 files checked, all ids resolve
views regenerated for stage A1: 115388 concepts, 705 rooms, 0 ledger lines
leg A1b-07 closed. Stop now; the harness takes the snap and runs the probe.
```

Ledgers at the close: lexicon 638 lines, running file 275 lines, leads 1,133 lines. The first run of `validate.py A1` at this close found one error: a lead from r/acecombat named r/murica, which is not in the frame. The line was removed from `leads-A1.jsonl` and its full content is kept in the diary; the second run found 0 errors. A grep, sort and comm check finds every lead's `other` in the frame, letter case aside. Three lexicon lines carried wrong or invented item ids (denmark 2, texans 1); corrected lines were appended and the diary names each one. One more artwork shows region placements before hour 0: r/nin (h-11.52), beside r/radiohead (h-11.54). That makes ten cases. The case stays unfiled until the canvas manifest is read through the verbs.

## Close report, leg A1b-08 (block 08), 2026-10-06

Block 08 read whole: 30 of 30 rooms noted, 344 of 705 in all. `validate.py A1` before the close:

```
stage A1:
  frame 705, dropped 0, analysed 705 : dropped.jsonl is written and empty, so the screen ran and dropped nothing
  room notes 344 over an analysed set of 705
  361 room(s) still to note; the stage closes when every room of the analysed set has one
  departures.jsonl carries 2 line(s)
  defects.jsonl carries 6 line(s)


0 errors (0 distinct shapes), 0 warnings
```

`done.sh A1`:

```
done.sh A1 leg=A1b-08 cut=none 20261006T172709Z
links: 1 files checked, all ids resolve
views regenerated for stage A1: 115388 concepts, 705 rooms, 0 ledger lines
leg A1b-08 closed. Stop now; the harness takes the snap and runs the probe.
```

Ledgers at the close: lexicon 678 lines, running file 311 lines, leads 1,288 lines. A grep, sort and comm check finds every lead's `other` in the frame, letter case aside. Two lead lines were removed in this leg. A lead from r/bisexual named r/lgbt, which is not in the frame. A lead from r/edmontonoilers to r/rangers carried a typed id, dfpl0ns; it was re-appended with the fetched id, dfpknk3. The diary keeps the content of both. Six lexicon lines were superseded by appended corrections. Two carried a later or wrong item: vinesauce "Vineshroom" (62prks to 62p03c) and edmontonoilers "battle of Alberta" (dfolk9h to dfolktz). Four lacked the h prefix on the hour: one ReBoot line and three sabres lines. No block 08 artwork shows region placements before hour 0. The count stays at ten cases, and the case stays unfiled. Onset contrast, block 08: five early rooms (overwatch, ockytop, ireland, foxes, rocketleague) and one late room (nVade).

## Close report, leg A1b-09 (block 09), 2026-10-06

Block 09 read whole: 52 of 52 rooms noted, 395 of 705 in all. `validate.py A1` before the close:

```
stage A1:
  frame 705, dropped 0, analysed 705 : dropped.jsonl is written and empty, so the screen ran and dropped nothing
  room notes 395 over an analysed set of 705
  310 room(s) still to note; the stage closes when every room of the analysed set has one
  departures.jsonl carries 2 line(s)
  defects.jsonl carries 6 line(s)


0 errors (0 distinct shapes), 0 warnings
```

`done.sh A1`:

```
done.sh A1 leg=A1b-09 cut=none 20261006T181917Z
links: 1 files checked, all ids resolve
views regenerated for stage A1: 115388 concepts, 705 rooms, 0 ledger lines
leg A1b-09 closed. Stop now; the harness takes the snap and runs the probe.
```

Ledgers at the close: lexicon 755 lines, running file 342 lines, leads 1,496 lines. A grep, sort and comm check finds every lead's `other` in the frame, letter case aside. One lead was removed in this leg: a lead from r/redhotchilipeppers named r/jhinmains, which is not in the frame; the diary keeps its content. Two lexicon lines cited a later or differently spelled item than first use (sonicthehedgehog "savemilesprower", sadboys "wooden horse"); corrected lines were appended. Two rooms have only two concepts (r/UMiami, r/tenma); the note hook requires three carrying ids, so the first id is listed twice in each, and the diary says so. One note (r/pebble) was logged noted in a parallel call before it was trimmed under 350 words; the diary records the order. One more artwork shows region placements before hour 0: r/npr's two works at h-11.19, in the centre ring. That makes eleven cases; the case stays unfiled. r/tenma, defect 1, was read: its one post places the character next to Satania, and the canvas fields hold nothing for it. Onset contrast, block 09: nine early rooms (schoolidolfestival, mls, thailand, redhotchilipeppers, warthunder, touhou, nascar, asexuality, chile) and five late rooms (sooners, UMiami, corridor, ManningPlace, pgang).

## Close report, leg A1b-10 (block 10), 2026-10-06

Block 10 read whole: 50 of 50 rooms noted, 445 of 705 in all. `validate.py A1` before the close:

```
stage A1:
  frame 705, dropped 0, analysed 705 : dropped.jsonl is written and empty, so the screen ran and dropped nothing
  room notes 445 over an analysed set of 705
  260 room(s) still to note; the stage closes when every room of the analysed set has one
  departures.jsonl carries 2 line(s)
  defects.jsonl carries 6 line(s)


0 errors (0 distinct shapes), 0 warnings
```

`done.sh A1`:

```
done.sh A1 leg=A1b-10 cut=none 20261006T190402Z
links: 1 files checked, all ids resolve
views regenerated for stage A1: 115388 concepts, 705 rooms, 0 ledger lines
leg A1b-10 closed. Stop now; the harness takes the snap and runs the probe.
```

Ledgers at the close: lexicon 816 lines, running file 373 lines, leads 1,613 lines. A grep, sort and comm check finds every lead's `other` in the frame, letter case aside. No lead line was removed in this leg. Rooms named in the record but outside the frame got no lead line (r/wallops_irl and r/quityourbullshit for r/worldpowers); the diary says so. One room has only two concepts (r/PokemonSage); the note hook requires three carrying ids, so the first id is listed twice, and the diary says so. The context was compacted once in this leg; the head was re-read and reconciled with the diary before the next write, and the diary records it. One more artwork shows region placements before hour 0: r/starcitizen's Star Citizen Ship at h-0.24. That makes twelve cases; the case stays unfiled. r/chelseafc's canvas line gives no artwork row with pixels and placers; its note gives the area and the region placements. Onset contrast, block 10: nine early rooms (dankmemes, puzzleanddragons, baylor, startrek, feedthebeast, patriots, leafs, EraseThePlace, suomi) and five late rooms (COSI, UPenn, sheffield, Cornwall, cgpgrey).

## Close report, leg A1b-11 (block 11), 2026-10-06

Block 11 read whole: 21 of 21 rooms noted, 466 of 705 in all. `validate.py A1` before the close:

```
stage A1:
  frame 705, dropped 0, analysed 705 : dropped.jsonl is written and empty, so the screen ran and dropped nothing
  room notes 466 over an analysed set of 705
  239 room(s) still to note; the stage closes when every room of the analysed set has one
  departures.jsonl carries 2 line(s)
  defects.jsonl carries 6 line(s)


0 errors (0 distinct shapes), 0 warnings
```

`done.sh A1`:

```
done.sh A1 leg=A1b-11 cut=none 20261006T192522Z
links: 1 files checked, all ids resolve
views regenerated for stage A1: 115388 concepts, 705 rooms, 0 ledger lines
leg A1b-11 closed. Stop now; the harness takes the snap and runs the probe.
```

Ledgers at the close: lexicon 840 lines, running file 395 lines, leads 1,653 lines. A grep, sort and comm check finds every lead's `other` in the frame, letter case aside. No lead line was removed in this leg. One lexicon line for r/xenoblade_chronicles was written with a corrected spelling ("got" for the room's "go"); a line with the exact words was appended. One running line on Green Lattice carried a stray aside; a corrected line was appended. The diary records both. One room has only two concepts (r/UNLincoln, listed among the screen's doubts at A1a); the note hook requires three carrying ids, so the first id is listed twice, and the diary says so. No new artwork with placements before hour 0 was found; r/leagueoflegends links The Void Prism from h-14.47, a work already counted under r/FloydVsVoid, so the count stays at twelve and the case stays unfiled. Onset contrast, block 11: nine early rooms (leagueoflegends, thesilphroad, totallynotrobots, india, titanfall, GreenEmpire, danganronpa, DestinyTheGame, PurplePixels) and three late rooms (udub, sakartvelo, UNLincoln).
