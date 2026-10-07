# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of B1b-05, 2026-10-07, the fifth stretch of stage B1.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1 is closed (legs A1a to A1b-55 and A1c). All 705 rooms have a note. Stage B1, the third-order scheme, is open.

**B1a is closed.** `prior.md` was written first, before any second-order theme was opened: sections 1 to 6 filled and dated 2026-10-07, sections 7 and 8 empty until the return stage. The harness seals it; a change now is a departure (rule 10). The order is drawn: seed cd472a6087a223d4 in `out/seed.txt`; `python3 tools/saturation.py order --stage B1` prints it.

**B1b-01 to B1b-04 are closed.** Orders 1 to 93 (sixers to chile): 90, 24, 17 and 4 new kinds. B1b-01's two process errors (twelve mints counted at the next room; 88 multiple placements without the rule 0 record, cut to 53) are on the record in `notes-B1.md`. In B1b-03 and B1b-04 I read rooms by theme headers and notes and grepped concepts for a few themes, while the read log counts them as read whole (the handler, 18:55). J decides whether they are reread.

**B1b-05 is closed.** Order 94 (minnesotavikings) to 118 (theitalyplace), 25 rooms, about 1.05 MB, every room read whole: 320 second-order themes read, 318 placed, 2 bare titles unplaced. 10 new kinds, T3-136 to T3-145, the last at theitalyplace (order 118). Nine episodes (E014 to E022), one move (albania t03 to T3-136), 90 rule 0 lines and 13 bag records. The report is in `notes-B1.md`. The next room is PinkVomitMonster (order 119).

**J's words for B1 (7 October 2026):** "national elements are very important here"; "we need to get as much variance on organizing behavior early on so that later we have enough to create the model". National, political and conflict content is study material: a theme about flags, borders, alliances or fights between national rooms is minted, placed and named as plainly as any other. **The handler's rule:** a choice to leave out or soften content for any reason other than the study's goes to J first with `mem.py ask`, and the content stays meanwhile.

**QA1-003 is answered and done:** bakchodi's and dankmemes' five held-back lines were restored line by line at B1b-02 and checked equal at B1b-03. No question is open.

## How the B1 walk goes (the stage file, kept here for after a compaction)

- **Legs.** B1b-01, B1b-02 ...: one stretch of the order per leg, about 1 MB of second-order themes and concepts (`mem.py room <sub> --size`: codes plus themes, not the forest; `xargs -I{} python3 tools/mem.py room {} --size --stage B1 < list` sizes a list). Declare the stretch (first and last order) in the diary when the leg opens. Then B1c (the saturation test), B1d (the second pass), B1e (the scheme standing, handback, interview cut).
- **The next room is always `mem.py next --stage B1`**, at every leg start and after every compaction. It follows the order and the stopping rule. Never a room from memory.
- **Startup packet each leg:** this head, the stage file, the last five diary entries, `mem.py scheme --brief`, `validate.py --open B1`.
- **Per room.** Read the A1 note (`mem.py note`) and every theme's note and concept labels. Read the room on its own first, then against rooms already read that it is tied to (`mem.py neighbours`, any `leads-A1.jsonl` line naming it). Where a tied room is read, search both rooms' concepts (`mem.py codes --sub <other> --limit 3000 | grep`) for the other's name or artwork: an episode needs both records to tell it, by one thread or one artwork in the same hours; a member writing in both rooms is strong evidence. For a room whose themes I cannot place, or whose A1 note marks it unsure, read the forest and case too, logged with `mem.py log --kind opened --ids <sub>` and why. A room is done when every second-order theme is placed or listed in `unplaced-B1.jsonl` (`{"sub","second_order","why"}`); unplaced is only for a theme with no doing to read (a bare title, a test post). A theme that stands alone goes on the rare tier, not out.
- **Order of work in a room:** read every theme; log ideas and mint the room's new kinds first, while the room still has unplaced themes; then place the rest with `python3 out/_analysis/b1_place.py <sub> t01=T3-002 t02=T3-004,T3-103 ...` (it calls `mem.py place` in order). A mint after the room's last placement is counted at the next room.
- **Rule 0, single placement.** One third-order theme per second-order theme, the one whose gate it meets best. A second or third only where a concept of its own supports it and the primary cannot carry it. Write the line in the leg's table (`out/_analysis/b1_multiplace_<leg>.tsv`: sub, theme_id, primary, additional, codes, why_not_one) and run `python3 out/_analysis/b1_multiplace_write2.py <tsv> --leg <leg> [--write]`; it checks every cited concept against the store (it caught one wrong concept at B1b-03) and appends only new lines. Beyond three: place once and record item-is-a-bag. `validate.py` warns once per multiple placement whatever the log says.
- **Reading a room (the handler, 7 October, 18:55):** read the room's whole print, every theme with every concept label, before placing any of its themes; grep finds things and does not replace reading. `python3 out/_analysis/b1_room.py <sub>` prints it through `mem.py`; a large room goes to `$TMPDIR` and is printed in parts under 30 KB with `sed -n`; check the file's line count (`grep -c ""`) against the printed range. The Read tool cannot open `$TMPDIR`. Each stretch-end line says how the rooms were read.
- **Verbs, never by hand.** `mem.py idea "<label>" --trigger <sub>:<tNN>`; `mem.py mint --label "..." --trigger <sub>:<tNN>`; `mem.py place`; `mem.py unplace`. There is no relabel verb. A move of members out of an existing theme: place, then unplace, then `python3 out/_analysis/b1_tier_line.py --leg <leg> --id <from> --to <to> --moved sub:tNN,... --move <one of the eight> --event split|members_changed --prompted "..." --why "..."`, and a diary line (`--kind split` when a theme is split; it counts as a new kind for the rule). A merge or split of a theme with more than twenty members: `log --kind move` and `python3 tools/snap.py B1 move-<move>-<n>`.
- **Grouping.** Gioia's first-order consolidation: stay near the material, let the number explode, get lost before getting found. Kinds, not sizes: one third-order theme is one doing; never split by degree. When in doubt keep two. No ceiling; hundreds expected (prior §1: 250 to 450). A theme holding more than one in ten second-order themes is read again for kinds inside it. Names 2 to 5 words, gerund-led, near the material, never a construct's name and never one of the four problems.
- **The floor:** a kind seen in two rooms unlike each other (size: at least twice the items; side of the contrast; or form) enters the main scheme; one room only, the rare tier. Two rooms telling one episode count as one: `episodes-B1.jsonl`.
- **The stopping rule** (`saturation.py status --stage B1`; never count by hand): the 50-average-room and 25-room conditions are met; rounds begin after 10 average rooms and 10 rooms without a new kind; markers 1 and 2 after three empty rounds each; then the draw (marker 3); then the report and `done.sh B1 --pause` for the PI's decision. The check-in at 60% of the words read before marker 3. A round predicted longer than 10 average rooms is logged when it begins (`mem.py log --kind note "round <n>: <rooms>"`).
- **Reads allowed:** themes and codes room by room, `pairs --level second`, a room's forest and material on demand, my notes through `mem.py note` (a prior, never a source), `contrast.md`, `running-A1.md`, `lexicon-A1.md`, `leads-A1.jsonl`, `coordinating-rule-A1.md`, `organizing_end-A1.jsonl`, `handback-A1.md`, quotes through `cite.py` only. Forbidden: cutting fourth-order themes or dimensions; citing a note.
- **Safe stops:** after each room's themes are placed and logged; `ls .pause`.

## Stage A1, what B1 inherits

- J's rulings of 7 October: hour 0 is the canvas opening (Reddit's tests from about hour -16); the onset is the first coded turn at hour 0 or later; the organizing end is reported with and without calls after hour 73 (`organizing_end-to73-A1.jsonl`); the coordinating rule's measured error is in `coordinating-rule-A1.md`; `leads-outside-frame-A1.jsonl` is a ledger B1 may read. QA1-002: organizing is counted before the freeze at hour 73.
- The catch-up pass read case.md and brief.md whole for 702 rooms; the forest is unread for 550. Rooms whose not-this line a member's own words weakened are listed by block in `running-A1.md`.
- The restore put back my pre-cut words in 447 rooms. Each A1 leg's choices are in `notes-A1.md`; `handback-A1.md` has "After A1c (7 October 2026)".

## Section 5 of A1

- `coordinating-rule-A1.md`, copied into `prior.md` §5. A turn counts when its label's leading act calls, assigns, plans, reports placement before hour 73, defends, makes or breaks a deal, or corrects another's placement; not when it recounts, jokes, mourns, thanks, praises, apologizes, blames, or is a moderator's removal. After hour 73 only calls or plans for canvas work count.
- Figures: 44,116 of 115,388 concepts coordinate (0.382). Nine rooms have no coordinating turn: watchmen, Redox, yerbamate, Lugarix, azores, ReBoot, PokemonSage, UNLincoln, tetris. Measured error: agreement 79 of 100, precision 0.92, recall 0.66.

## The census, checks and figures

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04); the analysed set is 705. Concepts 115,388. Second-order themes 7,844, all to be placed in B1.
- Eight lines in `defects.jsonl` (tenma has no canvas line; archlinux has a turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has a state `collapsed`; concept reach is 1.0; yogscast's first turn is not about the canvas; placements before hour 0 are Reddit's tests). QA1-001: the concept-reach threshold stays at 0 items.
- Log-log slopes on `items_in_window`: concepts 0.530, second-order themes 0.231. Mean `items_in_window` 3,022.

## The onset contrast

`contrast.md` and `prior.md` §6. Early (first coded turn hours 0 to before 3): 132. Late (after hour 48): 61. Neither: 512. The confound is size; held size (items 156 to 2770): 41 against 12.

## The three sentences written before reading, and what the reading found

Expected: one burst of calls early, then defence and looking back, ending near hour 73; fights and border deals with neighbours; the goal set early by one call. Found against them: the artwork was often on the canvas before the room spoke; coordinating turns do not all end near hour 73; rivals often became partners; deals often did not bind the crowd. Patterns seen three or more times are in `running-A1.md`.

## Contrary rooms

Blocks 01 to 18 by name only: morrowind, megaman, heyyea, egypt, duckgame, AprilKnights, flashtv, PinkVomitMonster, FloydVsVoid, anime, watchmen, TheAdventuresofTintin, tagpro, qotsa, cfb, drugs, UNLincoln, yerbamate, Redox, azores, archlinux; homelab, hentai, kpop, ubc, norge, cirkeltrek, loltyler1, bobross, nonbinary, zelda; ukplace, SwissNeutralityZone, GuardiansOfDatBoi, minecraft, GuildWars2, bardmains, placeDE; theitalyplace, spacexmasterrace, tampabaylightning, aoe2, 4chan, ice_poseidon, korea, drawhelix; greenlattice, norway, utaustin, france, masseffect, ducks, mariokart, natsume; thebluecorner, germany, vim, furry_irl, placehfarts, Pigifs, TreePlace, evedreddit; falcons, formula1, slovenia, sweden, wine, btc, nin, uoft; ReBoot, nVade, epublica, lego, foxes, math, popheads, ockytop; sadboys, spacex, Fez, warthunder, nascar, israel, magictcg, tenma, ManningPlace; cgpgrey, EraseThePlace, dankmemes, anarcho_capitalism, twice, TeamYellowPlace, mcgill, PokemonSage; totallynotrobots, finland, udub, GreenEmpire, danganronpa, india; ontario, orderofthebluecorner, CelticFc, enterthegungeon, eve, anarchocapitalism, teamcube; counting; polandball, ubreddit, canucks, rust, fivenightsatfreddys, kanye, azerbaijan; theblackvoid, rainbowgrid, raocow, Slovakia, taiwan, oltp, asexual; PlaceNL, pcmasterrace, PinkUnion, streetfighter, aeskwadraat, Mario, wallstreetbets; placestart, starryknights, tf2, brasil, wholesomememes, Thegreatblackhole, GreenCorner, ibo, wario; destiny, Summit1G, Okami, 2007scape, lithuania, stardewvalley, planetside.

Block 19: ainbowroad, dota2, Braveryjerk, dofus, Russiaclan, rotmg.

The one room that fits nothing else, chosen at A1c: r/Summit1G. The second pass (B1d) reads the contrary rooms with the rooms the saturation test finds not fitting.

## Open distinctions, carried into B1

None is filed in `_questions/`. Distinctions forming:
- Who started the work: joining or finding work begun elsewhere, against starting it; members working for other rooms' art (minecraft); a sighting of the room's subject made by others (yerbamate, TheAdventuresofTintin).
- Where organizing happened: thread, Discord, IRC, Telegram, a second sub, a stream; venues refused or argued over (archlinux, norge, germany); a small room keeping the thread on purpose (samuraijack); the plan hidden from rival infiltrators (lakers); rooms saying they wing it (southafrica).
- Deals and who speaks for a room: binding against not kept; sheltering under a stronger room's list (bretagne); a host's authority disputed (warframe, seahawks); who may make a deal for a room (harrypotter); a former attacker turned helper (albania).
- Command and sanction: a member put in charge (mls); a moderator banning the room's own vandals (uoft); an outside streamer's call relayed as an order (ice_poseidon).
- Scripts: self-defence, joint across rooms (archlinux), fighting the room's own plan (slovenia, southafrica), accounts lent to another's bot (albania).
- National rooms: flags built, merged into hearts or unions, emblems beside them; politics read into the canvas (scotland); fights retold as national history; the Union Jack, the Serbian flag, the hammer and sickle and The_Donald's wall argued over.
- After the close: the canvas mourned, carried to new canvases, preserved, sold and argued over (donaldglover).
- Conflict around venues: spies in a rival's Discord (babymetal), a hacked moderator account (PUBATTLEGROUNDS), a rival chat flooding a thread (Summit1G); wars between rooms told twice, each side blaming the other (texas and norge, skyrim and teslamotors).
- Strength and standing: rooms doubting they can build (araragi, nyu); members of both sides (kamenrider, canucks); moderators disowning the canvas (japan); quiet recruiting by a condemned room (loliconsunite); night shifts (canucks, uiuc); national feeling from the work (theitalyplace); ethnic jokes and where taunts stop (canucks).

## Ledgers at this close

- A1: `lexicon-A1.md` 1,289 lines; `running-A1.md` 773; `leads-A1.jsonl` 2,478; `departures.jsonl` 9; `defects.jsonl` 8.
- B1: `prior.md`; `notes-B1.md`; `scheme/scheme_current.jsonl` (145 themes over 1,432 placed second-order themes, 1,674 placements); `theme_discovery.jsonl` and `ideas-B1.jsonl` (145 lines each); `kinds-B1.jsonl` (1,753); `multiplacement_log.jsonl` (256); `tier_history.jsonl` (42); `unplaced-B1.jsonl` (10); `episodes-B1.jsonl` (22). `validate.py B1` at this close: 0 errors, 200 warnings (the multiple placements, each on the record).
- Rules kept: fetch every id with `cite.py`; never type an id from memory; never log a placement or note in the same call that writes it before the tool answers; count a ledger's lines after appending; there is no `--kind close`, log the closing line as a note.
- The permission check refuses "=w=", for and while loops, shell functions, heredocs, awk, a variable set from `$(...)`, and some `python3 -c` scripts that write files. Use the Write and Edit tools for file content; an Edit whose old text spans non-adjacent lines fails. The shell shows at most 30 KB per call; the overflow goes under CONTROL, which is read-denied.
- The diary rolls into new parts (B1 is in part B1-16). After a compaction the guard requires the head and stage file read again and the exact line "compacted; head reconciled" through `mem.py log --kind note`.

## The next comparison

Leg B1b-06 opens at the room `mem.py next --stage B1` names (PinkVomitMonster, order 119). Declare the stretch (about 1 MB) in the diary. Read every room whole, as above. The last new kind came at order 118; round 1 opened after order 94 and every new kind since has reset it; the rule's estimate of unseen kinds is 28. A round predicted longer than 10 average rooms is logged when it begins (`mem.py log --kind note "round <n>: <rooms>"`). Episodes come in about one room in three: search both records every time a tied room is read (`mem.py neighbours` and `leads-A1.jsonl`).

## The scheme as it stands

145 third-order themes, the working grouping in `scheme/scheme_current.jsonl` (`mem.py scheme --brief`). Size distribution: 27 themes hold one second-order theme, 20 two, 9 three; the largest are T3-010 making deals with neighbouring rooms (105, from 89 rooms, 7.3%), T3-009 celebrating the finished work (77), T3-001 staging April Fools fake news (64) and T3-017 carrying on the sub's usual talk (60). 30 themes are seen in one room only. B1b-05's new kinds: T3-136 doubting the room is strong enough, T3-137 joining an outside group's build, T3-138 staying neutral between two rooms, T3-139 pleading with attackers to stop, T3-140 moderators disowning the canvas work, T3-141 covering the night shift, T3-142 making ethnic jokes about rivals, T3-143 arguing whether a taunt goes too far, T3-144 recruiting quietly to avoid attackers, T3-145 feeling national through the canvas. T3-010's internal variation is written out in `notes-B1.md`; the first split to test if it passes one in ten is by the object of the bargain (space, help, protection). Boundaries and gate notes for B1e are listed there, leg by leg (T3-115 any refused request against T3-123 ground kept; T3-065 the land's flag, nation, region or state; T3-079 hearts between any two marks).

National kinds minted under J's words: T3-065 building the national flag (14 rooms), T3-078 helping kin nations with their flags, T3-079 joining neighbouring marks with a heart (6 rooms, sports logos among them), T3-080 arguing over a political symbol (9 rooms: the Union Jack, the Savoy crest, meat against GO VEGAN), T3-081 casting fights as historic national wars (9 rooms: the Alamo, 1971, Caporetto, Philip II), T3-085 weighing the room against the nations, T3-099 counting on a bigger neighbour's protection (2 rooms), T3-113 drawing national emblems beside the flag (8 rooms), T3-130 reading national politics into the canvas (5 rooms: MH17, the PYD flag over a Turkish one), T3-145 feeling national through the canvas.
