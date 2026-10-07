# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of B1b-08, 2026-10-08: the eighth stretch of stage B1.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1 is closed (legs A1a to A1b-55 and A1c). All 705 rooms have a note. Stage B1, the third-order scheme, is open.

**B1a is closed.** `prior.md` was written first, before any second-order theme was opened: sections 1 to 6 filled and dated 2026-10-07, sections 7 and 8 empty until the return stage. The harness seals it; a change now is a departure (rule 10). The order is drawn: seed cd472a6087a223d4 in `out/seed.txt`; `python3 tools/saturation.py order --stage B1` prints it.

**B1b-01 to B1b-07 are closed.** Orders 1 to 157 (sixers to traaaaaaannnnnnnnnns). B1b-01's two process errors are on the record in `notes-B1.md`. B1b-03 and B1b-04 read rooms by headers and notes; their 52 rooms were reread whole at B1b-06, which also split the three largest kinds (T3-010, T3-014, T3-009) into T3-149 to T3-157 under J's "Go on both". B1b-07 added T3-160 to T3-164 and episodes E040 to E059.

**B1b-08 is closed.** Orders 158 (greece) to 182 (uofm), 25 rooms, about 0.99 MB, every room read whole through `b1_room.py`, large rooms in parts under 30 KB with the line count checked (pokemon and halo in four parts). 275 second-order themes read, 274 placed (452 placements), one unplaced (berserk t04, a title only). Nine new kinds: T3-165 debating friendship with a historic enemy and T3-166 arguing over the nation's historical record (greece), T3-167 timing a mass placement together (dbz), T3-168 editing scripts to spare neighbours (neu), T3-169 signing the sub's name and T3-170 mistaking friendly work for vandalism (halo), T3-171 spreading a colour over the canvas, T3-172 renewing the order's oaths and T3-173 holding elections for office (AprilKnights, order 170). Twenty-six episodes, E060 to E085, ten of them resting on a member writing in both rooms. 178 rule 0 lines and 59 bag records in 20 rooms: the coders' themes in this stretch are broad, and each bag lists the kinds it would need. The notes section was checked against the record before the close and three details corrected (diary B1-31). The report is in `notes-B1.md`, "Leg B1b-08, the eighth stretch".

**J's words for B1 (7 October 2026):** "national elements are very important here"; "we need to get as much variance on organizing behavior early on so that later we have enough to create the model". National, political and conflict content is study material: a theme about flags, borders, alliances or fights between national rooms is minted, placed and named as plainly as any other. **The handler's rule:** a choice to leave out or soften content for any reason other than the study's goes to J first with `mem.py ask`, and the content stays meanwhile. Nothing was left out or softened at B1b-08 (the greece and Turkey argument after the close, the hammer and sickle and swastikas, frankocean's anti-Danish slogans, the swastika on Pikachu, all placed plainly).

**QA1-003 is answered and done.** No question is open.

## How the B1 walk goes (the stage file, kept here for after a compaction)

- **Legs.** B1b-01, B1b-02 ...: one stretch of the order per leg, about 1 MB of second-order themes and concepts (`mem.py room <sub> --size`: codes plus themes, not the forest). Declare the stretch (first and last order) in the diary when the leg opens. Then B1c (the saturation test), B1d (the second pass), B1e (the scheme standing, handback, interview cut).
- **The next room is always `mem.py next --stage B1`**, at every leg start and after every compaction. It follows the order and the stopping rule. Never a room from memory.
- **Startup packet each leg:** this head, the stage file, the last five diary entries, `mem.py scheme --brief`, `validate.py --open B1`.
- **Per room.** Read the A1 note (`mem.py note`) and every theme's note and concept labels. Read the room on its own first, then against rooms already read that it is tied to (`mem.py neighbours`, any `leads-A1.jsonl` line naming it, `mem.py codes --grep "<name>" --by-room` filtered to read rooms). An episode needs both records to tell it, by one thread or one artwork in the same hours; a member writing in both rooms is strong evidence. For a room whose themes I cannot place, or whose A1 note marks it unsure, read the forest and case too, logged with `mem.py log --kind opened --ids <sub>` and why. A room is done when every second-order theme is placed or listed in `unplaced-B1.jsonl`; unplaced is only for a theme with no doing to read (a bare title, a test post). A theme that stands alone goes on the rare tier, not out.
- **Order of work in a room:** read every theme; log ideas and mint the room's new kinds first, while the room still has unplaced themes; then place the rest with `python3 out/_analysis/b1_place.py <sub> t01=T3-002 t02=T3-004,T3-103 ...`. A mint after the room's last placement is counted at the next room. Mint a kind on a trigger whose own placements stay at three or fewer; a bag's kept placement may be the new kind only when the new kind is its best gate.
- **Rule 0, single placement.** One third-order theme per second-order theme, the one whose gate it meets best. A second or third only where a concept of its own supports it and the primary cannot carry it. Write the leg's table as a `.psv` with the Write tool (header `sub|theme_id|primary|additional|codes|why_not_one`), convert with `tr '|' '\t'`, and run `python3 out/_analysis/b1_multiplace_write3.py <tsv> --leg <leg> [--bag "sub:tNN:T3-kept:T3-a,T3-b:why"] [--write]`; check and write in one call with a timeout of 500,000 ms, since the tool now runs over two minutes and a bag written twice is a duplicate. Beyond three: place once and record item-is-a-bag. `validate.py` warns once per multiple placement whatever the log says.
- **Reading a room (the handler, 7 October, 18:55):** read the room's whole print, every theme with every concept label, before placing any of its themes; grep finds things and does not replace reading. `python3 out/_analysis/b1_room.py <sub>` prints it through `mem.py`; a large room goes to `$TMPDIR` and is printed in parts under 30 KB with `sed -n`; check the file's line count (`grep -c ""`) against the printed range. The Read tool cannot open `$TMPDIR`. Each stretch-end line says how the rooms were read.
- **Verbs, never by hand.** `mem.py idea "<label>" --trigger <sub>:<tNN>`; `mem.py mint --label "..." --trigger <sub>:<tNN>`; `mem.py place`; `mem.py unplace`. There is no relabel verb. A move of members out of an existing theme: place, then unplace, then `b1_tier_line.py` (one destination) or `b1_split_line.py` (several), and a diary line (`--kind split` when a theme is split; it counts as a new kind for the rule). A merge or split of a theme with more than twenty members: `log --kind move` and `python3 tools/snap.py B1 move-<move>-<n>`.
- **Grouping.** Gioia's first-order consolidation: stay near the material, let the number explode, get lost before getting found. Kinds, not sizes: one third-order theme is one doing; never split by degree. When in doubt keep two. No ceiling; hundreds expected (prior §1: 250 to 450). A theme holding more than one in ten second-order themes is read again for kinds inside it. Names 2 to 5 words, gerund-led, near the material, never a construct's name and never one of the four problems.
- **The floor:** a kind seen in two rooms unlike each other (size: at least twice the items; side of the contrast; or form) enters the main scheme; one room only, the rare tier. Two rooms telling one episode count as one: `episodes-B1.jsonl`.
- **The stopping rule** (`saturation.py status --stage B1`; never count by hand): rounds begin after 10 average rooms and 10 rooms without a new kind; markers 1 and 2 after three empty rounds each; then the draw (marker 3); then the report and `done.sh B1 --pause` for the PI's decision. The check-in at 60% of the words read before marker 3. A round predicted longer than 10 average rooms is logged when it begins (`mem.py log --kind note "round <n>: <rooms>"`).
- **Reads allowed:** themes and codes room by room, `pairs --level second`, a room's forest and material on demand, my notes through `mem.py note` (a prior, never a source), `contrast.md`, `running-A1.md`, `lexicon-A1.md`, `leads-A1.jsonl`, `coordinating-rule-A1.md`, `organizing_end-A1.jsonl`, `handback-A1.md`, quotes through `cite.py` only. Forbidden: cutting fourth-order themes or dimensions; citing a note.
- **Safe stops:** after each room's themes are placed and logged; `ls .pause`.

## Stage A1, what B1 inherits

- J's rulings of 7 October: hour 0 is the canvas opening; the onset is the first coded turn at hour 0 or later; the organizing end is reported with and without calls after hour 73 (`organizing_end-to73-A1.jsonl`); `leads-outside-frame-A1.jsonl` may be read. QA1-002: organizing is counted before the freeze at hour 73.
- The catch-up pass read case.md and brief.md whole for 702 rooms; the forest is unread for 550. Rooms whose not-this line a member's own words weakened are listed by block in `running-A1.md`.
- The restore put back my pre-cut words in 447 rooms. Each A1 leg's choices are in `notes-A1.md`; `handback-A1.md` has "After A1c (7 October 2026)".

## Section 5 of A1

- `coordinating-rule-A1.md`, copied into `prior.md` §5: a turn counts when its leading act calls, assigns, plans, reports placement before hour 73, defends, makes or breaks a deal, or corrects another's placement. 44,116 of 115,388 concepts coordinate (0.382); measured agreement 79 of 100, precision 0.92, recall 0.66; nine rooms have no coordinating turn.

## The census, checks and figures

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04); the analysed set is 705. Concepts 115,388. Second-order themes 7,844, all to be placed in B1.
- Eight lines in `defects.jsonl`. QA1-001: the concept-reach threshold stays at 0 items.
- Log-log slopes on `items_in_window`: concepts 0.530, second-order themes 0.231. Mean `items_in_window` 3,022.

## The onset contrast

`contrast.md` and `prior.md` §6. Early (first coded turn hours 0 to before 3): 132. Late (after hour 48): 61. Neither: 512. The confound is size; held size (items 156 to 2770): 41 against 12.

## The three sentences written before reading, and what the reading found

Expected: one early burst of calls, then defence, ending near hour 73; border deals; the goal set by one call. Found against them: the artwork was often on the canvas before the room spoke; coordinating turns do not all end near hour 73; rivals often became partners; deals often did not bind the crowd. Patterns seen three or more times are in `running-A1.md`.

## Contrary rooms

Blocks 01 to 18 by name only: morrowind, megaman, heyyea, egypt, duckgame, AprilKnights, flashtv, PinkVomitMonster, FloydVsVoid, anime, watchmen, TheAdventuresofTintin, tagpro, qotsa, cfb, drugs, UNLincoln, yerbamate, Redox, azores, archlinux; homelab, hentai, kpop, ubc, norge, cirkeltrek, loltyler1, bobross, nonbinary, zelda; ukplace, SwissNeutralityZone, GuardiansOfDatBoi, minecraft, GuildWars2, bardmains, placeDE; theitalyplace, spacexmasterrace, tampabaylightning, aoe2, 4chan, ice_poseidon, korea, drawhelix; greenlattice, norway, utaustin, france, masseffect, ducks, mariokart, natsume; thebluecorner, germany, vim, furry_irl, placehfarts, Pigifs, TreePlace, evedreddit; falcons, formula1, slovenia, sweden, wine, btc, nin, uoft; ReBoot, nVade, epublica, lego, foxes, math, popheads, ockytop; sadboys, spacex, Fez, warthunder, nascar, israel, magictcg, tenma, ManningPlace; cgpgrey, EraseThePlace, dankmemes, anarcho_capitalism, twice, TeamYellowPlace, mcgill, PokemonSage; totallynotrobots, finland, udub, GreenEmpire, danganronpa, india; ontario, orderofthebluecorner, CelticFc, enterthegungeon, eve, anarchocapitalism, teamcube; counting; polandball, ubreddit, canucks, rust, fivenightsatfreddys, kanye, azerbaijan; theblackvoid, rainbowgrid, raocow, Slovakia, taiwan, oltp, asexual; PlaceNL, pcmasterrace, PinkUnion, streetfighter, aeskwadraat, Mario, wallstreetbets; placestart, starryknights, tf2, brasil, wholesomememes, Thegreatblackhole, GreenCorner, ibo, wario; destiny, Summit1G, Okami, 2007scape, lithuania, stardewvalley, planetside.

Block 19: ainbowroad, dota2, Braveryjerk, dofus, Russiaclan, rotmg.

The one room that fits nothing else, chosen at A1c: r/Summit1G. The second pass (B1d) reads the contrary rooms with the rooms the saturation test finds not fitting.

## Open distinctions, carried into B1

None is filed in `_questions/`. Most distinctions formed in A1 are now kinds in the scheme; bot rooms cutting their own targets to spare neighbours became T3-168 at B1b-08. Still open: who started the work (joining work begun elsewhere against starting it; a sighting made by others, yerbamate and TheAdventuresofTintin); members of both sides (kamenrider, canucks); deals that bound against deals that did not (rocketleague's rainbow agreement re-explained by about twelve members); wars told twice, each side blaming the other (texas and norge, skyrim and teslamotors, bakchodi and pakistan, clubpenguin and dbz, fireemblem and pokemon).

## Ledgers at this close

- A1: `lexicon-A1.md` 1,289 lines; `running-A1.md` 773; `leads-A1.jsonl` 2,478; `departures.jsonl` 9; `defects.jsonl` 8.
- B1: `prior.md`; `notes-B1.md`; `scheme/scheme_current.jsonl` (173 themes over 2,154 placed second-order themes, 3,135 placements); `theme_discovery.jsonl` and `ideas-B1.jsonl` (173 lines each); `kinds-B1.jsonl` (3,250); `multiplacement_log.jsonl` (1,094); `tier_history.jsonl` (48); `unplaced-B1.jsonl` (12); `episodes-B1.jsonl` (85). `validate.py B1`: 0 errors; its warning count prints as 200, a capped figure; the scheme holds 727 multiply placed second-order themes (254 of them three times, none over three), each on the record.
- Rules kept: fetch every id with `cite.py`; never type an id from memory; never log a placement or note in the same call that writes it before the tool answers; count a ledger's lines after appending; there is no `--kind close`, log the closing line as a note. Check a notes section against the diary's room notes and the store before closing; at B1b-07 and B1b-08 details written from memory were wrong and corrected.
- The permission check refuses "=w=", for and while loops, shell functions, heredocs, awk, a variable set from `$(...)`, and some `python3 -c` scripts that write files. Use the Write and Edit tools for file content; an Edit whose old text spans non-adjacent lines fails. The shell shows at most 30 KB per call; the overflow goes under CONTROL, which is read-denied.
- The diary rolls into new parts (B1 is in part B1-32). After a compaction the guard requires the head and stage file read again and the exact line "compacted; head reconciled" through `mem.py log --kind note`.

## The next comparison

Leg B1b-09 opens at the room `mem.py next --stage B1` names (shield, order 183). Declare the stretch (about 1 MB) in the diary. Stopping rule at this close: 182 of 705 rooms, 26.4% of the words, kinds 177 by the rule's count, coverage 0.9887, unseen 41.06; round 4 opened after gameofthrones (order 180), next kind predicted in 5.3 rooms, reading to 189.5 average rooms. Read every room whole; place onto the split kinds by their decide-when-both lines in `notes-B1.md`, and onto this leg's nine kinds as their lines there say. Episodes come in most rooms whose neighbours are read: search both records every time. The rooms waiting on a tie with B1b-07's and B1b-08's rooms are listed under "Leads carried forward" in those legs' sections of `notes-B1.md`.

## The scheme as it stands

173 third-order themes, the working grouping in `scheme/scheme_current.jsonl` (`mem.py scheme --brief`). Size distribution: 26 themes hold one second-order theme, 17 two, 14 three, 8 four, 7 five, 6 six, 6 seven, 4 eight; 30 are seen in one room only. The largest: T3-009 celebrating the finished work (119, 5.5%), T3-010 the space and border deals (117, 5.4%; its B1e name should say so), T3-017 the sub's usual talk (96), T3-001 members' April Fools (95), T3-002 calling members in (91). None holds one in ten. Kinds since B1b-05: T3-136 to T3-173, their names in `scheme --brief`. Gate notes for B1e are in `notes-B1.md`, leg by leg: T3-162 is the host's side of a permission regime, T3-035 the asker's; T3-169 is writing the sub's name to say whose the work is, not T3-004's design; T3-170 is harm to friendly work out of not knowing the plan, not T3-087's tracing of attackers; T3-171 is a colour field as the work itself. Leads for the second pass, with the second-order themes to place, are in `notes-B1.md`: T3-167 (falcons, radiohead, jerma985, minnesotavikings), T3-168 (rust t11), T3-169 and T3-170 (several, most inside bags), T3-171 (greenlattice, cirkeltrek), T3-160 (theitalyplace t11).

National kinds minted under J's words: T3-065 building the national flag (now with greece, NovaScotia and vietnam), T3-078 helping kin nations with their flags, T3-079 joining neighbouring marks with a heart, T3-080 arguing over a political symbol (vietnam's choice of flag, greece's hammer and sickle and swastikas), T3-081 casting fights as historic national wars, T3-085 weighing the room against the nations, T3-099 counting on a bigger neighbour's protection, T3-113 drawing national emblems beside the flag, T3-130 reading national politics into the canvas, T3-145 feeling national through the canvas, and at B1b-08 T3-165 debating friendship with a historic enemy and T3-166 arguing over the nation's historical record (greece).
