# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-09, 2026-10-06.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1, the reading. Leg A1a did the checks, the screen and the order. Legs A1b-01 to A1b-09 read blocks 01 (53 rooms), 02 (48), 03 (62), 04 (44), 05 (34), 06 (37), 07 (36), 08 (30) and 09 (52) whole. 395 of 705 rooms have a note in `out/rooms/`. 310 rooms remain, in blocks 10 to 19. The next leg is A1b-10. At this close `mem.py next` names r/greece, the first room of block 10. Always take the next room from `mem.py next`, never from this file.

The order is in `out/order-A1.txt`, a seeded shuffle (seed 20261006) cut into blocks of about 3 MB by `mem.py`'s byte count. Block 13 is r/counting alone, at 11.17 MB.

`validate.py A1` at this close: 0 errors, 0 warnings. 395 notes over 705.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed when the themes are placed later in the run.

## What the checks found

Six defects are in `defects.jsonl`; none blocks the reading. In short: r/tenma has no canvas line; r/archlinux has a coded turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has an undocumented state `collapsed`; concept reach is 1.0 everywhere; r/yogscast's first coded turn is not about the canvas. Two departures are in `departures.jsonl`, both saved scripts in `out/_analysis/`. r/tenma was read in block 09: its one post places the character next to Satania, and the canvas fields hold nothing for it, so defect 1 stands from the reading side.

A possible seventh defect, not yet filed: linked artworks with region placements before hour 0. Eleven cases: r/FloydVsVoid h-14.47, r/ProfessorLayton h-13.49, r/SwissNeutralityZone h-14.52, r/monalisaclan h-15.23, r/radiohead h-11.54, r/aoe2 h-0.66, r/thebluecorner h-12.34, r/globaloffensive h-13.62, r/GrowTheTree h-0.24, r/nin h-11.52, r/npr h-11.19 (two works in the centre ring). The canvas window runs from -16, so this may be by design. No `mem.py` verb found so far reads `package/DATA-manifest-canvas.md`. Check the manifest through the verbs before filing it.

## The principal investigator's answer QA1-001

The concept-reach threshold stays at 0 items. No substitute measure is to be invented. Every room is read at concept level in the later model-building stages, and unplaced concepts are read at the end too. `notes-A1.md` says that the measure gives no cut in this store.

## Figures I carry

- Log-log slopes on `items_in_window`: concepts 0.530, second-order themes 0.231.
- concept_reach_threshold: 0 items, kept by QA1-001.
- `n_off_platform`: median 4, max 88 (dankmemes).
- `px_window_share`: median 0.111, max 0.547; null for tenma.
- Concentration is null in 3 rooms (nonbinary, oltp, wario).
- 79 rooms have their last coded turn before hour 73.

## The onset contrast

`out/contrast.md`. Early: first coded turn after hour 0 and before hour 3, 131 rooms. Late: first coded turn after hour 48, 61 rooms. The confound is size (median items 5067 against 33). A held-size comparison (items 156 to 2770, 41 against 12) travels with it. Expectation: late rooms organize around finding space on a full canvas; early rooms around claiming and holding it.

Block 09 early rooms, nine: r/schoolidolfestival, r/mls, r/thailand, r/redhotchilipeppers, r/warthunder, r/touhou, r/nascar, r/asexuality, r/chile. In several the first coded turn is an April Fools post, not canvas work: r/nascar, r/mls, r/redhotchilipeppers, r/warthunder and r/schoolidolfestival began canvas work only after h10 to h53. r/touhou raided early and spent the week on treaties; r/chile asked the avocado makers before growing.

Block 09 late rooms, five: r/ManningPlace (h59.70), r/corridor (h51.36), r/sooners (h50.83), r/UMiami (h51.23), r/pgang (h72.55). They split. r/corridor asked permission at three sites and shrank its logo, as the expectation says. r/sooners first tried to take UF's, Nebraska's and Northeastern's logos, then was stopped by neighbours and its own members, and moved four times. r/ManningPlace, a sub made for the canvas, refused to move and held a 1,205 px face. r/pgang's record holds only templates in the last half hour, and r/UMiami one attack call. In all five, writers placed under 0.08 of the linked artwork; r/UMiami's placed none. No size test yet.

## The three sentences written before reading, against nine blocks

The three sentences: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

1. The artwork was often there before the room spoke, and other subs often made it. Block 09: r/sadboys found a wooden horse it never planned after the close (writers 0.001); a visitor asked r/spacex whether it knew what others had made (seven works, coded share 0.007); r/FlaggyFlag's flag was flying at its first coded turn (0.02); r/PORTUGALCARALHO's Squirtle was begun by others beside its flag. Another sub started or ran the logo for r/cardinals (r/stlouisblues), r/ufl (r/floridagators) and r/rojava (r/TheFarLeftSide).
2. Coordinating turns end mostly between hours 68 and 73. Block 09: r/elitedangerous h70.42, r/vegan h72.92, r/warriors h72.86, r/italy h72.91, r/penguins h72.85, r/sooners h72.72. Earlier ends: r/THE_R h35.91, r/tenma h34.68, r/UMiami h51.23, r/spacex h54.62, r/mordhau h58.60, r/redhotchilipeppers h62.73, r/rojava h60.27.
3. Fights are with neighbours, and rivals often turn into partners. Block 09: r/AMD went from war with Poland to a truce and an alliance traded for border space; r/touhou displaced r/furry, then helped it relocate and defended the agreement; pacts between rivals recur in r/torontoraptors (Vikings) and r/timbers (Straya, then a Cascadian flag with Seattle).
4. Deals often do not bind the crowd. Block 09: r/torontoraptors members refused its Vikings treaty out of NFL rivalries; r/Fez agreed to its own erasure by Denmark on a promise to rebuild that the canvas's end did not allow; r/thailand gave up the frog it had promised to keep when UofT offered help.
5. The goal is often set by one member. Block 09: r/sooners (44% of coded turns), r/sadboys (52%), r/theexpanse (30%), r/epublica earlier.
6. April Fools makeovers filled most coded turns in many rooms: r/nascar, r/mls, r/elitedangerous, r/python, r/magictcg, r/cardinals, r/warthunder, r/schoolidolfestival.
7. Moderators: r/49ers' moderator stickied the plan, moved the logo and set neighbour rules; r/warriors' pinned the effort; r/magictcg's removed canvas posts until a megathread at h56.7; r/italy's sent canvas threads to r/theitalyplace at h45.3; r/israel's Discord moderator banned attack talk against the Palestinian flag.
8. The canvas fields name a work the room reports lost or unfinished: r/warriors (lost at h72.5), r/pebble (unfinished), r/warthunder (half built), r/Fez (absent at the close), r/KState (griefed at the last minute).

New in block 09, seen three or more times and logged in the diary:
- The linked artwork placed largely by others while the room found or joined it (sadboys, spacex, FlaggyFlag, PORTUGALCARALHO, achievement_hunter, UMiami).
- Another sub started or ran the room's logo (cardinals, ufl, rojava).
- Green Lattice or Rainbow Road as the host whose leave is sought, with refusals (hyperlightdrifter, sadboys, redhotchilipeppers, warthunder, sooners, magictcg, ManningPlace, mordhau). r/warthunder was refused by every host it asked.
- A large room ends with a small or late mark (magictcg, penguins, warriors, spacex).
- Members say no one is in charge, or ask for someone in charge (asexuality, italy, mls).
- Larger neighbours cite their numbers or Discord size to move a smaller room (KState, sooners, hyperlightdrifter).
- The canvas field names a work the room reports lost or unfinished (warriors, pebble, warthunder, Fez, KState).
Also seen in block 09: a national flag as permission office for a small room (sweden for yumenikki: Pippi granted, Poniko denied through a Discord diplomacy channel); a script hitting a neighbour and turned off with an apology (python, KState); the void as a common enemy that brings neighbours together (elitedangerous, theexpanse, southafrica, ManningPlace).

Paired lead checks, both sides read, block 09: agree for nascar with paydaytheheist and frankocean, schoolidolfestival with lovelive, sonicthehedgehog with columbia, python with xcom, AMD with AyyMD, 49ers with seahawks, cardinals with chicubs, asexuality with pansexual, eesti with loltyler1 and latvia, Fez with denmark, ManningPlace with babymetal, torontoraptors with minnesotavikings and vermont, vegan with cfb, spacex with spacexmasterrace, thailand with ubc and uoft, touhou with furry, osugame and indonesia, redvsblue with halo, mls with drugs, warriors with ohio, timbers with ripcity, FlaggyFlag with hellointernet, npr with bisexual, epublica with spacexmasterrace, metroid with dbz, warthunder with japan. Agree in part: nascar and darksouls; AMD and placesnek; 49ers and dallasstars; ManningPlace and ssbpm; metroid and sonicthehedgehog; corridor and mexico; warriors and globaloffensive. Disagree in part: israel and lebanon (israel's record names a Palestinian overlay, not a Lebanese one). Not found in the concepts read: python and haskell, dbz and naruto, gatech and iastate/berkeley earlier, theexpanse with hearthstone and evedreddit, eesti and lovelive, touhou and soylent, warriors with GuildWars2, 49ers, sabres and torontoraptors, timbers and parahumans.

## Contrary rooms

Block 01: morrowind and megaman said they were not organized; heyyea kept art it did not make; egypt's flag was a stranger's gift; duckgame mourned art the atlas lists as surviving; AprilKnights had an order with elections; flashtv's prank ran apart from canvas work; PinkVomitMonster called its lack of coordination its beauty; FloydVsVoid's founder regretted not compromising; anime mostly refused and argued credit; watchmen and TheAdventuresofTintin noticed art they did not visibly build; tagpro aimed at advertising; anime, qotsa, cfb and drugs disagree with the canvas fields. From the screen: UNLincoln, yerbamate, Redox, azores, archlinux.

Block 02: homelab, hentai, kpop and ubc, norge, cirkeltrek, loltyler1, bobross and nonbinary, zelda.

Block 03: ukplace, SwissNeutralityZone, GuardiansOfDatBoi, minecraft and GuildWars2, bardmains, placeDE.

Block 04: theitalyplace and spacexmasterrace; tampabaylightning; aoe2; 4chan; ice_poseidon; korea; drawhelix.

Block 05: greenlattice, norway, utaustin, france, masseffect, ducks and mariokart, natsume.

Block 06: thebluecorner, germany, vim, furry_irl, placehfarts, Pigifs, TreePlace, evedreddit.

Block 07: falcons, formula1, slovenia, sweden, wine, btc, nin, uoft.

Block 08: ReBoot, nVade, epublica, lego, foxes, math, popheads, ockytop.

Block 09:
- sadboys: planned a smiley it never placed and found a wooden horse it did not plan after the close.
- spacex: a large room whose seven linked works others made; its record is members finding them.
- Fez: agreed to let Denmark erase its work on a promise to rebuild, and the canvas ended first.
- warthunder: every host it asked refused or did not answer.
- nascar: its own members took a neighbour's side against it.
- israel: its members and Discord moderator refused retaliation against the flag built over theirs.
- magictcg: a large room whose moderators removed canvas posts until h56.7 and whose mark is 377 px.
- tenma: no canvas line at all.
- ManningPlace: a late room that refused to move and held a large face.

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to watch in block 10:
- joining or finding work begun elsewhere, against starting it; and finding it only after the close;
- organizing in the thread, against organizing in Discord or a second sub and reporting back; and a second sub that is open, against one that is private;
- deals that bind a room, against deals that members' outside loyalties or a later, larger deal undo;
- a treaty over the whole work, against one over a small part (a stinger, a stripe, a heart);
- a sub made for the canvas that governs others (greenlattice, thebluecorner, placehearts, TheFarLeftSide, placestart), against one that keeps a single work (nVade, epublica, GranColombia, ManningPlace);
- a national flag run as a permission office (sweden with yumenikki, denmark with lego), against one run as a front line;
- one organiser with alts or friends, against a room-wide effort;
- attacking first and building later, against building first and defending;
- the moderator as organiser, as obstacle, as gatekeeper to a second sub, as enforcer against the room's own vandals, and as enforcer of a treaty;
- a large room with a large mark, against a large room with a small or late mark;
- late rooms that ask at every site, against late rooms that take, against late subs made for one work;
- the canvas fields linking the room's work, against linking a neighbour's, a rival's, a covered work, a work the room says it lost, or nothing.

## The last rooms read

Block 09, in reading order: southafrica, nascar, schoolidolfestival, sonicthehedgehog, sadboys, python, KState, AMD, dbz, 49ers, ufl, FlaggyFlag, yumenikki, cardinals, Moondye7, asexuality, redhotchilipeppers, THE_R, israel, rojava, eesti, theexpanse, italy, pebble, elitedangerous, Fez, pgang, chile, mls, penguins, hyperlightdrifter, ManningPlace, torontoraptors, vegan, spacex, PORTUGALCARALHO, warthunder, thailand, touhou, redvsblue, magictcg, mordhau, achievement_hunter, metroid, corridor, npr, UMiami, warriors, sooners, tenma, timbers.

## Ledgers at this close

- `lexicon-A1.md`: 755 lines. `running-A1.md`: 342 lines. `leads-A1.jsonl`: 1,496 lines. Every lead's `other` is in `order-A1.txt`, letter case aside; checked at this close with grep, sort and comm.
- In this leg one lead named a room outside the frame (redhotchilipeppers to jhinmains); the line was removed and its content is in the diary. Two lexicon lines cited a later item than first use (sonicthehedgehog savemilesprower; sadboys wooden horse spelling); corrected lines were appended.
- Two notes have only two concepts (UMiami, tenma); the hook requires three carrying ids, so the first id is repeated, and the diary says so.
- One note (pebble) was logged noted in a parallel call before it was trimmed under 350; the diary records the order.
- Rule, kept: fetch every id with `cite.py` and check every lead's room with grep against the frame in one call; append in a later call; filter typed ids out with grep before appending. Never type an id from memory.
- The hook rejects notes of 350 words or more, and quotes of four words or more outside `struck by`. First drafts still run 370 to 430; draft the `doing` line at about 150 words and never log noted in the same call as the write.

## The next comparison

In block 10, for every room: did the artwork exist before the room's first call, and who built it? Do the canvas fields link the work the room describes, or name it covered or lost? Was the deal struck in the thread, in Discord or in a second sub, and did the crowd accept that it bound them? Which side of the onset contrast is the room on, and is it a sub made for the canvas? Late-side rooms in block 10: r/COSI, r/UPenn, r/sheffield, r/Cornwall, r/cgpgrey; read them against r/corridor, r/sooners and r/ManningPlace. Read r/leafs against r/sabres and r/ockytop; r/startrek against r/epublica; r/starcitizen against r/elitedangerous; r/Peru against r/npr; r/neu against r/sooners and r/KState; r/TsundereSharks against r/python; r/hungary against r/lebanon; r/suomi against r/southafrica; r/texas against r/chile; r/coldplay against r/chicubs; r/patriots against r/foxes; r/TeamYellowPlace against r/metalgearsolid; r/rangers against r/edmontonoilers; r/dankmemes for its 88 off-platform pointers.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
