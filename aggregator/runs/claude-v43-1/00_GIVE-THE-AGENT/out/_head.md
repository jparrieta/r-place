# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-10, 2026-10-06.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1, the reading. Leg A1a did the checks, the screen and the order. Legs A1b-01 to A1b-10 read blocks 01 to 10 whole (53, 48, 62, 44, 34, 37, 36, 30, 52 and 50 rooms). 445 of 705 rooms have a note in `out/rooms/`. 260 rooms remain, in blocks 11 to 19. The next leg is A1b-11. At this close `mem.py next` names r/danganronpa, the first room of block 11. Block 11 holds 21 rooms. Always take the next room from `mem.py next`, never from this file.

The order is in `out/order-A1.txt`, a seeded shuffle (seed 20261006) cut into blocks of about 3 MB by `mem.py`'s byte count. Block 13 is r/counting alone, at 11.17 MB.

`validate.py A1` at this close: 0 errors, 0 warnings. 445 notes over 705.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed when the themes are placed later in the run.

## What the checks found

Six defects are in `defects.jsonl`; none blocks the reading. In short: r/tenma has no canvas line; r/archlinux has a coded turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has an undocumented state `collapsed`; concept reach is 1.0 everywhere; r/yogscast's first coded turn is not about the canvas. Two departures are in `departures.jsonl`, both saved scripts in `out/_analysis/`.

A possible seventh defect, not yet filed: linked artworks with region placements before hour 0. Twelve cases: r/FloydVsVoid h-14.47, r/ProfessorLayton h-13.49, r/SwissNeutralityZone h-14.52, r/monalisaclan h-15.23, r/radiohead h-11.54, r/aoe2 h-0.66, r/thebluecorner h-12.34, r/globaloffensive h-13.62, r/GrowTheTree h-0.24, r/nin h-11.52, r/npr h-11.19, and in block 10 r/starcitizen (Star Citizen Ship, h-0.24). The canvas window runs from -16, so this may be by design. No `mem.py` verb found so far reads `package/DATA-manifest-canvas.md`. Check the manifest through the verbs before filing it.

## The principal investigator's answer QA1-001

The concept-reach threshold stays at 0 items. No substitute measure is to be invented. Every room is read at concept level in the later model-building stages, and unplaced concepts are read at the end too. `notes-A1.md` says that the measure gives no cut in this store.

## Figures I carry

- Log-log slopes on `items_in_window`: concepts 0.530, second-order themes 0.231.
- concept_reach_threshold: 0 items, kept by QA1-001.
- `n_off_platform`: median 4, max 88 (dankmemes, read in block 10: the canvas concepts name one Discord; the pointers are not canvas plans in what was read).
- `px_window_share`: median 0.111, max 0.547; null for tenma.
- Concentration is null in 3 rooms (nonbinary, oltp, wario).
- 79 rooms have their last coded turn before hour 73.

## The onset contrast

`out/contrast.md`. Early: first coded turn after hour 0 and before hour 3, 131 rooms. Late: first coded turn after hour 48, 61 rooms. The confound is size (median items 5067 against 33). A held-size comparison (items 156 to 2770, 41 against 12) travels with it. Expectation: late rooms organize around finding space on a full canvas; early rooms around claiming and holding it.

Block 10 early rooms, nine: r/dankmemes, r/puzzleanddragons, r/baylor, r/startrek, r/feedthebeast, r/patriots, r/leafs, r/EraseThePlace, r/suomi. As in block 09, the first coded turn is often April Fools talk: r/dankmemes, r/startrek, r/feedthebeast and r/baylor began canvas work hours or days later (r/baylor at h63.1). r/patriots, r/leafs, r/suomi and r/EraseThePlace called for canvas work within the first three hours, and all four then struck deals with neighbours.

Block 10 late rooms, five: r/COSI, r/UPenn, r/sheffield, r/Cornwall (h66.18), r/cgpgrey (h72.04). Against r/corridor, r/sooners and r/ManningPlace: r/COSI, r/UPenn and r/sheffield asked permission and moved when asked, as r/corridor did. r/Cornwall took a spot, refused once to move ("NEVERRRRRRR"), then shuffled behind a neighbour. r/cgpgrey is a fourth kind: it arrived in the last hour to defend a logo whose placements began at h2.44, in a sub with restricted posting; a member said they could have organized sooner if they could start their own threads. In all five the linked work was placed from the first hours, long before the room's first call. No size test yet.

## The three sentences written before reading, against ten blocks

The three sentences: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

1. The artwork was often there before the room spoke, and other subs often made it. Block 10: r/foxstevenson's logo was placed 63 hours before its first call, and r/liquicity offered to build it; r/PokemonSage found a Foliat shown on r/TheFarLeftSide; r/greenland's writers placed none of their flag; r/superman's symbol was kept by others while one member's figure was lost.
2. Coordinating turns end mostly between hours 68 and 73. Block 10: r/patriots h72.42, r/bakchodi h72.97, r/EraseThePlace h72.90, r/hatsune h72.97, r/TeamYellowPlace h72.00, r/suomi h72.20. Earlier ends: r/littlebusters h46.99, r/greenland h45.35, r/superman h52.32, r/worldpowers h56.03, r/gameattack h59.79.
3. Fights are with neighbours, and rivals often become partners. Block 10: r/starcitizen and r/elitedangerous built a joint logo and shared a script; r/hungary and r/denmark share a peace heart; r/puzzleanddragons was covered by r/masseffect and r/2007scape, and both helped rebuild.
4. Deals often do not bind the crowd. Block 10: r/denmark's visitors promised r/twice to keep its text, and Danish participants took the spot; r/bakchodi's treaty line with r/belgium was later called an invasion; r/TsundereSharks said r/NewMexico broke a compromise.
5. The goal is often set by one member. Block 10: r/superman, r/littlebusters, r/greenland, r/baylor.
6. April Fools makeovers by moderators filled early turns: r/startrek (CBS takeover), r/chelseafc (QPR), r/starcitizen (Wing Commander), r/warframe (theme swap with r/DestinyTheGame), r/dankmemes (wholesome mode), r/twice (JYP), r/AceOfAngels8 (Sistar), r/rangers.
7. Moderators: r/suomi's pulled canvas posts into a megathread and r/FinlandFlag; r/starcitizen's made one official thread and made help with Elite official; r/startrek's removed image posts for format and consolidated help requests; r/EraseThePlace's barred discriminatory posts.
8. The canvas fields name a work the room reports lost, failed or half done: r/dankmemes (Gnome Child, "We failed"), r/hatsune (bulldozed), r/twice (pink spot lost), r/foxstevenson (half a logo). They link a work the room never discusses: r/anarcho_capitalism (Smiling Ancap Meme, writers placed 0), r/AceOfAngels8 (AOA, not the Seolhyun heart it reports).

New in block 10, seen three or more times and logged in the diary:
- Green Lattice as the host whose leave rooms cite, and whose members disrupt work its own Discord allowed (stargate, Peru, warframe, gameattack, neu via Hong Kong's grant).
- The room that covered a work helps rebuild it (animalcrossing with TheFarLeftSide, puzzleanddragons, liquicity).
- A deal struck by ambassadors that the sub's own participants break (twice, bakchodi, TsundereSharks).
- r/placestart governing others' space (liquicity's template, hatsune's taskbar deal, cgpgrey).
- A room writing or running its own script because others use them (TsundereSharks, neu, coldplay, texas, liquicity), against members refusing scripts because the work should be built by hand (rangers, starcitizen's Hornet).
- A sub moving canvas talk to a second sub, megathread or diplomacy thread (greece, suomi, startrek, hatsune, NewMexico).
- The canvas field linking a work the room did not discuss or place (anarcho_capitalism, AceOfAngels8, greenland, PokemonSage).
- A small room giving way when larger neighbours ask (NewMexico, oneshot, Cornwall, neu).
Also in block 10: a national flag as permission office (hungary for Lebanon and Survivor); a room paying a neighbour five pixels (coldplay to Straya); rooms bargaining with the Void (mcgill, EraseThePlace, anarcho_capitalism); a sub made for the canvas hosting smaller works in return for upkeep (TeamYellowPlace for Snake, Batman and a mural).

Paired lead checks, both sides read, block 10: agree for cirkeltrek and greece, rit and COSI, xcom and rhythmheaven, korea and seolhyun, habs, ockytop and sabres with leafs, monsterhunter and liquicity, TheFarLeftSide and animalcrossing, spacexmasterrace and startrek, ireland and placehearts with feedthebeast, masseffect and puzzleanddragons, lebanon, denmark and survivor with hungary, rangers and bangladesh with bakchodi, elitedangerous and kerbalspaceprogram with starcitizen, norway, norge and maryland with texas, bostonbruins and NewMexico, kamenrider, python and NewMexico with TsundereSharks, batman and frc with TeamYellowPlace, texastech and KState with neu, anarchism and completeanarchy with anarcho_capitalism, falcons and patriots, seolhyun and AceOfAngels8. Agree in part: OKState and startrek; chicubs and coldplay; frankocean and hungary; miamidolphins and patriots; stargate, canada and linux with EraseThePlace; Dorset and Cornwall; babymetal and TeamYellowPlace; sooners and neu; southpark and TsundereSharks. Not found in the concepts read: epublica and ftlgame with startrek, ethereum and minecraft with feedthebeast, harrypotter with superman, korea with twice, mit and habs with mcgill, ethereum with suomi, ohio, giantbomb and MMA with texas, mexico with NewMexico, npr with Peru, japan with warframe, foxes with patriots, vocaloid and linux earlier.

## Contrary rooms

Block 01: morrowind and megaman said they were not organized; heyyea kept art it did not make; egypt's flag was a stranger's gift; duckgame mourned art the atlas lists as surviving; AprilKnights had an order with elections; flashtv's prank ran apart from canvas work; PinkVomitMonster called its lack of coordination its beauty; FloydVsVoid's founder regretted not compromising; anime mostly refused and argued credit; watchmen and TheAdventuresofTintin noticed art they did not visibly build; tagpro aimed at advertising; anime, qotsa, cfb and drugs disagree with the canvas fields. From the screen: UNLincoln, yerbamate, Redox, azores, archlinux.

Block 02: homelab, hentai, kpop and ubc, norge, cirkeltrek, loltyler1, bobross and nonbinary, zelda.

Block 03: ukplace, SwissNeutralityZone, GuardiansOfDatBoi, minecraft and GuildWars2, bardmains, placeDE.

Block 04: theitalyplace and spacexmasterrace; tampabaylightning; aoe2; 4chan; ice_poseidon; korea; drawhelix.

Block 05: greenlattice, norway, utaustin, france, masseffect, ducks and mariokart, natsume.

Block 06: thebluecorner, germany, vim, furry_irl, placehfarts, Pigifs, TreePlace, evedreddit.

Block 07: falcons, formula1, slovenia, sweden, wine, btc, nin, uoft.

Block 08: ReBoot, nVade, epublica, lego, foxes, math, popheads, ockytop.

Block 09: sadboys, spacex, Fez, warthunder, nascar, israel, magictcg, tenma, ManningPlace.

Block 10:
- cgpgrey: a late room that arrived in the last hour to defend a logo others built, under restricted posting.
- EraseThePlace: a sub made for the canvas to erase it to white, which argued what to spare and barred discriminatory posts.
- dankmemes: a large room with 88 off-platform pointers whose canvas calls were scattered raids and whose one Discord build failed.
- anarcho_capitalism: the canvas field links a meme it never discusses; its flag and snek were moved to small backups.
- twice: a deal Denmark's visitors promised was broken by Danish participants.
- TeamYellowPlace: a colour faction that hosted other works for upkeep.
- mcgill: members hailed the Void to spare a chicken.
- PokemonSage: two turns, a found Foliat, no coordinating turn.

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to watch in block 11:
- joining or finding work begun elsewhere, against starting it; and finding it only after the close;
- organizing in the thread, against organizing in Discord or a second sub and reporting back;
- deals that bind a room, against deals its own participants, outside loyalties or a later, larger deal undo;
- a treaty over the whole work, against one over a small part (a tail, a pixel column, a heart);
- a sub made for the canvas that governs others (greenlattice, thebluecorner, placehearts, TheFarLeftSide, placestart, TeamYellowPlace), against one that keeps a single work (nVade, epublica, ManningPlace), against one made to erase (EraseThePlace);
- a host's grant against its own members' disruption (warframe with Green Lattice);
- a national flag run as a permission office (sweden, denmark, hungary), against one run as a front line;
- one organiser with friends, against a room-wide effort;
- scripts written in self-defence, against scripts refused on principle;
- the moderator as organiser, obstacle, gatekeeper to a second sub, prankster, or enforcer;
- a large room with a large mark, against a large room with a small, late or failed mark;
- late rooms that ask at every site, take, refuse then shuffle, or arrive only to defend;
- the canvas fields linking the room's work, a neighbour's, a covered work, a lost work, or a work the room never names.

## The last rooms read

Block 10, in reading order: greece, UPenn, COSI, baylor, rhythmheaven, seolhyun, stargate, sheffield, rangers, bretagne, leafs, liquicity, animalcrossing, startrek, feedthebeast, PokemonSage, superman, littlebusters, puzzleanddragons, cgpgrey, hatsune, uofmn, coldplay, foxstevenson, hungary, suomi, bakchodi, starcitizen, dankmemes, mcgill, worldpowers, southpark, patriots, twice, texas, greenland, EraseThePlace, chelseafc, NewMexico, Cornwall, anarcho_capitalism, TsundereSharks, gameattack, AceOfAngels8, oneshot, cmu, TeamYellowPlace, Peru, neu, warframe.

## Ledgers at this close

- `lexicon-A1.md`: 816 lines. `running-A1.md`: 373 lines. `leads-A1.jsonl`: 1,613 lines. Every lead's `other` is in `order-A1.txt`, letter case aside; checked at this close with grep, sort and comm.
- Leads written for rooms outside the frame are not written: worldpowers' rival r/wallops_irl and r/quityourbullshit are logged in the diary instead.
- One note has only two concepts (PokemonSage); the hook requires three carrying ids, so the first id is repeated, and the diary says so.
- r/chelseafc's canvas line names no artwork row with pixels and placers; the note gives the area and region placements.
- Rule, kept: fetch every id with `cite.py` and check every lead's room with grep against the frame; append through a grep filter on the item id; never type an id from memory.
- The hook rejects notes of 350 words or more by its own count, which runs a few words above `wc -w`; keep `wc -w` at 345 or below. First drafts still run 360 to 415; draft the `doing` line at about 150 words and never log noted in the same call as the write.

## The next comparison

In block 11, for every room: did the artwork exist before the room's first call, and who built it? Do the canvas fields link the work the room describes, or name it covered, lost or unnamed? Was the deal struck in the thread, in Discord or in a second sub, and did the room's own participants keep it? Which side of the onset contrast is the room on, and is it a sub made for the canvas? Early-side rooms in block 11: r/leagueoflegends, r/thesilphroad, r/totallynotrobots, r/india, r/titanfall, r/GreenEmpire, r/danganronpa, r/DestinyTheGame, r/PurplePixels. Late-side rooms: r/udub, r/sakartvelo, r/UNLincoln; read them against r/cgpgrey, r/Cornwall and r/corridor. Read r/DestinyTheGame against r/warframe (the theme swap); r/straya against r/coldplay (five pixels); r/totallynotrobots against r/patriots; r/india against r/bakchodi; r/kurdistan against r/hungary; r/finland against r/suomi; r/clubpenguin against r/warframe; r/GreenEmpire and r/PurplePixels as colour subs against r/TeamYellowPlace; r/TransFlagPlace as a sub made for the canvas.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
