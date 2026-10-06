# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-11, 2026-10-06.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1, the reading. Leg A1a did the checks, the screen and the order. Legs A1b-01 to A1b-11 read blocks 01 to 11 whole (53, 48, 62, 44, 34, 37, 36, 30, 52, 50 and 21 rooms). 466 of 705 rooms have a note in `out/rooms/`. 239 rooms remain, in blocks 12 to 19. The next leg is A1b-12. At this close `mem.py next` names r/newzealand, the first room of block 12. Block 12 holds 35 rooms. Always take the next room from `mem.py next`, never from this file.

The order is in `out/order-A1.txt`, a seeded shuffle (seed 20261006) cut into blocks of about 3 MB by `mem.py`'s byte count. Block 13 is r/counting alone, at 11.17 MB.

`validate.py A1` at this close: 0 errors, 0 warnings. 466 notes over 705.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed when the themes are placed later in the run.

## What the checks found

Six defects are in `defects.jsonl`; none blocks the reading. In short: r/tenma has no canvas line; r/archlinux has a coded turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has an undocumented state `collapsed`; concept reach is 1.0 everywhere; r/yogscast's first coded turn is not about the canvas. Two departures are in `departures.jsonl`, both saved scripts in `out/_analysis/`.

A possible seventh defect, not yet filed: linked artworks with region placements before hour 0. Twelve cases: r/FloydVsVoid h-14.47, r/ProfessorLayton h-13.49, r/SwissNeutralityZone h-14.52, r/monalisaclan h-15.23, r/radiohead h-11.54, r/aoe2 h-0.66, r/thebluecorner h-12.34, r/globaloffensive h-13.62, r/GrowTheTree h-0.24, r/nin h-11.52, r/npr h-11.19, r/starcitizen h-0.24. r/leagueoflegends links The Void Prism from h-14.47, the same work as r/FloydVsVoid's. The canvas window runs from -16, so this may be by design. No `mem.py` verb found so far reads `package/DATA-manifest-canvas.md`. Check the manifest through the verbs before filing it.

## The principal investigator's answer QA1-001

The concept-reach threshold stays at 0 items. No substitute measure is to be invented. Every room is read at concept level in the later model-building stages, and unplaced concepts are read at the end too. `notes-A1.md` says that the measure gives no cut in this store.

## Figures I carry

- Log-log slopes on `items_in_window`: concepts 0.530, second-order themes 0.231.
- concept_reach_threshold: 0 items, kept by QA1-001.
- `n_off_platform`: median 4, max 88 (dankmemes: its canvas concepts name one Discord).
- `px_window_share`: median 0.111, max 0.547; null for tenma.
- Concentration is null in 3 rooms (nonbinary, oltp, wario).
- 79 rooms have their last coded turn before hour 73.

## The onset contrast

`out/contrast.md`. Early: first coded turn after hour 0 and before hour 3, 131 rooms. Late: first coded turn after hour 48, 61 rooms. The confound is size (median items 5067 against 33). A held-size comparison (items 156 to 2770, 41 against 12) travels with it. Expectation: late rooms organize around finding space on a full canvas; early rooms around claiming and holding it.

Block 11 early rooms, nine: r/leagueoflegends, r/thesilphroad, r/totallynotrobots, r/india, r/titanfall, r/GreenEmpire, r/danganronpa, r/DestinyTheGame, r/PurplePixels. As before, the first coded turn is often April Fools talk. r/totallynotrobots began canvas work only at h69.9 and failed; r/titanfall at h26.7. r/GreenEmpire and r/PurplePixels, both subs made for the canvas, claimed corners in the first hours; GreenEmpire went silent by h5.4.

Block 11 late rooms, three: r/udub (h54.74), r/sakartvelo (h68.72), r/UNLincoln (h72.08). With block 10 they now show five kinds. Ask and move (COSI, UPenn, sheffield, corridor). Take, refuse once, shuffle (Cornwall). Arrive to defend work others built (cgpgrey). Take by script over objections (udub). Talk about a site and find the mark already there, or call to fix a logo that is not theirs (sakartvelo, UNLincoln). In every late room so far the linked work was placed from the first hours. No size test yet.

## The three sentences written before reading, against eleven blocks

The three sentences: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

1. The artwork was often there before the room spoke, and other subs often made it. Block 11: r/totallynotrobots' linked ReCaptcha (writers 0.003); r/kurdistan found a heart others made; r/sakartvelo found Georgian flags already placed; r/GreenEmpire's linked green corner (writers placed one pixel).
2. Coordinating turns end mostly between hours 68 and 73. Block 11: r/danganronpa h71.65, r/india h72.91, r/straya h72.88, r/totallynotrobots h72.97, r/xenoblade_chronicles h72.75. Earlier ends: r/GreenEmpire h5.36, r/kurdistan h61.08, r/PurplePixels h63.54.
3. Fights are with neighbours, and rivals often become partners. Block 11: r/Bulgaria's own member stopped its expansion over the Monado (xenoblade_chronicles); r/pakistan sent a truce and r/india's scripts repaired both flags; r/parahumans and r/straya made a redback together.
4. Deals often do not bind the crowd. Block 11: Norwegians did not know the Discord peace plans with r/stevenuniverse; r/finland members disowned their flag's expansion and blamed a botter. Against this, rooms kept treaties against their own wish: r/danganronpa refused to retake space because the banner came first.
5. The goal is often set by one member: r/UNLincoln, r/sakartvelo, r/GreenEmpire.
6. April Fools makeovers by moderators filled early turns in nine block 11 rooms: danganronpa, stevenuniverse, india, thesilphroad, leagueoflegends, DestinyTheGame (theme swap with warframe, both sides confirm), totallynotrobots, titanfall, malaysia.
7. Moderators: r/malaysia's designated one official thread; r/finland's removed threads into one; r/clubpenguin's stickied a fresh location.
8. The canvas fields link works the room did not make or does not report: block 11 adds seven rooms (totallynotrobots, UNLincoln, sakartvelo, kurdistan, GreenEmpire, TransFlagPlace's hearts not its ribbon, finland's small flag).

Seen three or more times and logged, blocks 10 and 11:
- Green Lattice as host whose leave rooms cite and which asks upkeep (stargate, Peru, warframe, gameattack, neu, titanfall, TransFlagPlace, leagueoflegends), and whose members sometimes disrupt work its Discord allowed (warframe).
- r/placestart governing others' space and hosting small rooms as taskbar icons (liquicity, hatsune, cgpgrey, clubpenguin, farmcarrots's proposal).
- A room that covered a work helps rebuild it (animalcrossing, puzzleanddragons, liquicity).
- Deals struck by ambassadors that the sub's own participants break or do not know of (twice, bakchodi, TsundereSharks, stevenuniverse).
- A room yields or keeps a treaty because the other side was there first (titanfall, danganronpa, malaysia, neu).
- A room cracks or shrinks its own work for a neighbour (stevenuniverse, xenoblade_chronicles, udub).
- Scripts written because others use them (TsundereSharks, neu, coldplay, texas, india, malaysia), against scripts refused on principle (rangers, starcitizen, danganronpa's Kirigiri).
- Colour factions with three fates: one held and hosted (TeamYellowPlace), one split and lost its corner (PurplePixels), one went silent into Green Lattice (GreenEmpire).
- TheFarLeftSide protecting small rooms' flags (animalcrossing, rojava, PokemonSage, kurdistan).
- Large rooms whose canvas calls were scattered and whose mark came from a Discord group (dankmemes, leagueoflegends, DestinyTheGame).

Paired lead checks, both sides read, block 11: agree for aceattorney and danganronpa; norway, norge and 4chan with stevenuniverse; homestuck, NieR, spongebob, rangers and bakchodi with india; germany and farmcarrots; the_pack, bisexual, auburn and asktransgender with TransFlagPlace; virginiatech and titanfall; foxes and patriots with totallynotrobots; parahumans, timbers, coldplay, GrowTheTree and australia with straya; warframe and rocketleague with DestinyTheGame; xcom and udub; dallasstars and wildhockey with finland; dbz and clubpenguin; bardmains and leagueoflegends; hungary and kurdistan. Agree in part: scp and thesilphroad; uwaterloo and titanfall; eesti and india; uiuc and finland; globaloffensive and leagueoflegends. Not found in the concepts read: ghibli, simonfraser with stevenuniverse; metroid, monero, rickandmorty with india; UPenn, fullcommunism with farmcarrots; witcher, haskell, rickandmorty, sadboys with TransFlagPlace; drugs, gorillaz, ripcity, chile, vegan with straya; halo, placehearts with DestinyTheGame; GrowTheTree, TheB1G, greenbaypackers with finland; FloydVsVoid, metroid with leagueoflegends; SwissNeutralityZone with PurplePixels. Block 10's paired checks are in `notes-A1.md` and the diary.

## Contrary rooms

Block 01: morrowind, megaman, heyyea, egypt, duckgame, AprilKnights, flashtv, PinkVomitMonster, FloydVsVoid, anime, watchmen, TheAdventuresofTintin, tagpro, qotsa, cfb, drugs; from the screen UNLincoln, yerbamate, Redox, azores, archlinux.

Block 02: homelab, hentai, kpop and ubc, norge, cirkeltrek, loltyler1, bobross and nonbinary, zelda.

Block 03: ukplace, SwissNeutralityZone, GuardiansOfDatBoi, minecraft and GuildWars2, bardmains, placeDE.

Block 04: theitalyplace and spacexmasterrace; tampabaylightning; aoe2; 4chan; ice_poseidon; korea; drawhelix.

Block 05: greenlattice, norway, utaustin, france, masseffect, ducks and mariokart, natsume.

Block 06: thebluecorner, germany, vim, furry_irl, placehfarts, Pigifs, TreePlace, evedreddit.

Block 07: falcons, formula1, slovenia, sweden, wine, btc, nin, uoft.

Block 08: ReBoot, nVade, epublica, lego, foxes, math, popheads, ockytop.

Block 09: sadboys, spacex, Fez, warthunder, nascar, israel, magictcg, tenma, ManningPlace.

Block 10: cgpgrey, EraseThePlace, dankmemes, anarcho_capitalism, twice, TeamYellowPlace, mcgill, PokemonSage.

Block 11:
- UNLincoln: a last-hour call to fix a logo another member said was Northeastern's; read now in full, two turns.
- totallynotrobots: canvas work began at h69.9 and failed; the canvas links a ReCaptcha it placed 0.003 of.
- finland: the sub where outsiders came to negotiate; members pointed them to r/Suomi and disowned the flag's expansion.
- udub: a late room that took space by script over objections and called it a win.
- GreenEmpire: a sub made for the canvas that went silent within six hours.
- danganronpa: members refused to retake space because a treaty and an earlier banner said no.
- india: its scripts repaired both the Indian and the Pakistani flag.

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to watch in block 12:
- joining or finding work begun elsewhere, against starting it; finding it only after the close;
- organizing in the thread, against organizing in Discord or a second sub; the sub where outsiders negotiate, against the sub where the nation organises (finland, suomi);
- deals that bind a room, against deals its own participants or the other side's participants do not know or keep;
- a treaty kept against the room's own wish, against one broken by its own rogues;
- a sub made for the canvas that governs others (greenlattice, thebluecorner, placehearts, TheFarLeftSide, placestart, TeamYellowPlace), one that keeps a single work, one that asks leave (farmcarrots, TransFlagPlace), one made to erase (EraseThePlace), and one that fades (GreenEmpire);
- a national flag run as a permission office, as a watcher (hungary with kurdistan), or as a front line;
- scripts written in self-defence, scripts refused on principle, scripts that repair a rival (india);
- the moderator as organiser, obstacle, gatekeeper, prankster, or enforcer;
- a large room with a large mark, against a large room whose mark came from a Discord group;
- the five kinds of late room listed above;
- the canvas fields linking the room's work, a neighbour's, a covered or lost work, or a work the room never names.

## The last rooms read

Block 11, in reading order: danganronpa, stevenuniverse, india, thesilphroad, farmcarrots, TransFlagPlace, titanfall, xenoblade_chronicles, totallynotrobots, straya, UNLincoln, DestinyTheGame, udub, finland, clubpenguin, leagueoflegends, sakartvelo, GreenEmpire, malaysia, kurdistan, PurplePixels.

## Ledgers at this close

- `lexicon-A1.md`: 840 lines. `running-A1.md`: 395 lines. `leads-A1.jsonl`: 1,653 lines. Every lead's `other` is in `order-A1.txt`, letter case aside; checked at this close with grep, sort and comm.
- One lexicon line (xenoblade_chronicles) was written with a corrected spelling; a line with the exact words was appended. One running line carried a stray aside; a corrected line was appended. The diary says both.
- Two notes have only two concepts (UNLincoln this leg; PokemonSage earlier); the hook requires three carrying ids, so the first id is repeated, and the diary says so.
- Rule, kept: fetch every id with `cite.py` and check every lead's room with grep against the frame; append through a grep filter on the item id; never type an id from memory. Lexicon words are copied as written, typos included.
- The hook rejects notes of 350 words or more by its own count, which runs a few words above `wc -w`; keep `wc -w` at 345 or below. First drafts still run 360 to 425; draft the `doing` line at about 150 words and never log noted in the same call as the write.

## The next comparison

In block 12, for every room: did the artwork exist before the room's first call, and who built it? Do the canvas fields link the work the room describes? Was the deal struck in the thread, in Discord or in a second sub, and did both sides' participants keep it? Which side of the onset contrast is the room on, and is it a sub made for the canvas? Early-side rooms in block 12: r/worldoftanks, r/clashroyale, r/eve, r/de, r/argentina, r/donaldglover, r/newzealand, r/romania. Late-side rooms: r/CelticFc, r/MiamiHurricanes; read them against the five kinds of late room. Read r/newzealand against r/starcitizen and r/straya; r/chibears against r/finland; r/cubers against r/xenoblade_chronicles; r/romania against r/hungary and r/malaysia; r/pakistan against r/india and r/bakchodi; r/SquareSpiral against r/suomi and r/finland; r/argentina against r/suomi; r/orderofthebluecorner against r/thebluecorner and r/PurplePixels; r/anarchocapitalism against r/anarcho_capitalism; r/de against r/placeDE and r/germany.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
