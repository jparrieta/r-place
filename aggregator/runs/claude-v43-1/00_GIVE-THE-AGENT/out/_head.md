# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of B1b-02, 2026-10-07, the second stretch of stage B1.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1 is closed (legs A1a to A1b-55 and A1c). All 705 rooms have a note. Stage B1, the third-order scheme, is open.

**B1a is closed.** `prior.md` was written first, before any second-order theme was opened: sections 1 to 6 filled and dated 2026-10-07, sections 7 and 8 empty until the return stage. The harness seals it; a change now is a departure (rule 10). The order is drawn: seed cd472a6087a223d4 in `out/seed.txt`; `python3 tools/saturation.py order --stage B1` prints it. `notes-B1.md` says what I expect of the order. `tier_history.jsonl` is opened.

**B1b-01 is closed.** Order 1 (sixers) to 17 (bitcoin): 197 second-order themes placed, 90 third-order themes (T3-001 to T3-090). Two process errors are on the record in `notes-B1.md`: twelve mints counted at the next room, and 88 themes multiply placed without the rule 0 record (cut to 53, each logged).

**B1b-02 is closed.** Order 18 (criticalrole) to 41 (norge), 24 rooms, about 1.03 MB: 289 second-order themes read, 285 placed, 4 in `unplaced-B1.jsonl`; 24 new kinds, T3-091 to T3-114, each logged as an idea and minted before its room's last placement. One split (T3-048 and T3-023 into T3-095), one move (minecraft t03 to T3-002), one episode (E001, drugs and mls). The report is in `notes-B1.md`. The next room is NewMexico (order 42).

**J's words for B1 (7 October 2026):** "national elements are very important here"; "we need to get as much variance on organizing behavior early on so that later we have enough to create the model". National, political and conflict content is study material: a theme about flags, borders, alliances or fights between national rooms is minted, placed and named as plainly as any other. **The handler's rule:** a choice to leave out or soften content for any reason other than the study's goes to J first with `mem.py ask`, and the content stays meanwhile.

**QA1-003 is answered and done.** J (16:48): try line by line, and the handler copies any line a safety stop cuts again. At the safe stop after minecraft I put back bakchodi's doing, week, named and made, and dankmemes' doing, one line per call with `out/_analysis/restore_put.py`. No safety stop came; no line is still out. No question is open.

## How the B1 walk goes (the stage file, kept here for after a compaction)

- **Legs.** B1b-01, B1b-02 ...: one stretch of the order per leg, about 1 MB of second-order themes and concepts (`mem.py room <sub> --size`: codes plus themes, not the forest). Declare the stretch (first and last order) in the diary when the leg opens. Then B1c (the saturation test), B1d (the second pass), B1e (the scheme standing, handback, interview cut).
- **The next room is always `mem.py next --stage B1`**, at every leg start and after every compaction. It follows the order and the stopping rule. Never a room from memory.
- **Startup packet each leg:** this head, the stage file, the last five diary entries, `mem.py scheme --brief`, `validate.py --open B1`.
- **Per room.** Read its second-order themes and concepts. Read the room on its own first, then against rooms already read that it is tied to (`mem.py neighbours`, `mem.py compare`, any `leads-A1.jsonl` line naming it). Where a tied room is read, search both rooms' concepts (`mem.py codes --sub <other> --limit 3000 | grep`) for the other's name or artwork: an episode needs both records to tell it. For a room whose themes I cannot place with confidence, or whose A1 note marks it unsure, read the forest and case too, logged with `mem.py log --kind opened --ids <sub>` and why. A room is done when every second-order theme is placed or listed in `unplaced-B1.jsonl` (`{"sub","second_order","why"}`); unplaced is only for a theme with no doing to read (a bare title, a test line). A theme that stands alone goes on the rare tier, not out.
- **Order of work in a room:** read every theme; log ideas and mint the room's new kinds first, while the room still has unplaced themes; then place the rest. A mint after the room's last placement is counted at the next room.
- **Rule 0, single placement.** One third-order theme per second-order theme, the one whose gate it meets best. A second or third only where a concept of its own supports it and the primary cannot carry it. Write the line when it is made in the leg's table (`out/_analysis/b1_multiplace_<leg>.tsv`: sub, theme_id, primary, additional, codes, why_not_one) and run `python3 out/_analysis/b1_multiplace_write2.py <tsv> --leg <leg> [--write]`. It checks every line against the scheme and the store, and appends only lines not yet in `multiplacement_log.jsonl`. Beyond three: place once and record item-is-a-bag (`--bag sub:tNN:T3-kept:T3-a,T3-b:why`). `validate.py` warns once per multiple placement whatever the log says.
- **Reading a room:** `python3 out/_analysis/b1_room.py <sub> [tNN ...]` prints every theme's note and every concept label through `mem.py` (a large room goes to `$TMPDIR` and is printed in parts under 30 KB with `sed -n`; the Read tool cannot open `$TMPDIR`).
- **Verbs, never by hand.** `mem.py idea "<label>" --trigger <sub>:<tNN>`; `mem.py mint --label "..." --trigger <sub>:<tNN>`; `mem.py place <sub>:<tNN> --theme T3-NNN`; `mem.py unplace`. A move of members out of an existing theme: place, then unplace, then `python3 out/_analysis/b1_tier_line.py --leg <leg> --id <from> --to <to> --moved sub:tNN,... --move <one of the eight> --event split|members_changed --prompted "..." --why "..."`, and a diary line (`--kind split` when a theme is split; it counts as a new kind for the rule). A merge or split of a theme with more than twenty members: `log --kind move` and `python3 tools/snap.py B1 move-<move>-<n>`.
- **Grouping.** Gioia's first-order consolidation: stay near the material, let the number explode, get lost before getting found. Kinds, not sizes: one third-order theme is one doing; never split by degree. When in doubt keep two (splitting later is a re-read). No ceiling; hundreds expected (prior §1: 250 to 450). A theme holding more than one in ten second-order themes is read again for kinds inside it. Names 2 to 5 words, gerund-led, near the material, never a construct's name and never one of the four problems.
- **The floor:** a kind seen in two rooms unlike each other (size: at least twice the items; side of the contrast; or form) enters the main scheme; one room only, the rare tier. Two rooms telling one episode count as one: `episodes-B1.jsonl`.
- **The stopping rule** (`saturation.py status --stage B1`; never count by hand): no estimate before 50 average rooms and 25 rooms; rounds after 10 average rooms and 10 rooms without a new kind; markers 1 and 2 after three empty rounds each; then the draw (marker 3); then the report and `done.sh B1 --pause` for the PI's decision. The check-in at 60% of the words read before marker 3. A round predicted longer than 10 average rooms is logged when it begins (`mem.py log --kind note "round <n>: <rooms>"`).
- **Reads allowed:** themes and codes room by room, `pairs --level second`, a room's forest and material on demand, my notes through `mem.py note` (a prior, never a source), `contrast.md`, `running-A1.md`, `lexicon-A1.md`, `leads-A1.jsonl`, `coordinating-rule-A1.md`, `organizing_end-A1.jsonl`, `handback-A1.md`, quotes through `cite.py` only. Forbidden: cutting fourth-order themes or dimensions; citing a note.
- **Safe stops:** after each room's themes are placed and logged; `ls .pause`.

## Stage A1, what B1 inherits

- J's rulings of 7 October: hour 0 is the canvas opening (Reddit's tests from about hour -16); the onset is the first coded turn at hour 0 or later; the organizing end is reported with and without calls after hour 73 (`organizing_end-to73-A1.jsonl`); the coordinating rule's measured error is in `coordinating-rule-A1.md`; `leads-outside-frame-A1.jsonl` is a ledger B1 may read; the note length of about 350 words is a guide. QA1-002: organizing is counted before the freeze at hour 73.
- The catch-up pass (A1b-20 to A1b-48) read case.md and brief.md whole for 702 rooms; the forest is unread for 550. The rooms whose not-this line a member's own words weakened are listed by block in `running-A1.md` (catch-up blocks 20 to 48).
- The restore (A1b-49 to A1b-53, and A1b-55) put back my pre-cut words in 447 rooms after the 350-word cap had cut 562 notes; bakchodi's and dankmemes' held-back lines followed at B1b-02 (QA1-003). Each A1 leg's choices are in `notes-A1.md`.
- `handback-A1.md` has a section "After A1c (7 October 2026)" with what B1 should know.

## Section 5 of A1

- `coordinating-rule-A1.md`, copied into `prior.md` §5. A turn counts when its label's leading act calls, assigns, plans, reports placement before hour 73, defends, makes or breaks a deal, or corrects another's placement; not when it recounts, jokes, mourns, thanks, praises, apologizes, blames, or is a moderator's removal. After hour 73 only calls or plans for canvas work count.
- Figures: 44,116 of 115,388 concepts coordinate (0.382). Nine rooms have no coordinating turn: watchmen, Redox, yerbamate, Lugarix, azores, ReBoot, PokemonSage, UNLincoln, tetris. 146 rooms end after hour 73. work_remained: kept 347, lost 218, silent 140. Measured error: agreement 79 of 100, precision 0.92, recall 0.66. Median end h72.02 with calls after hour 73, h71.69 without.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04). Dropped 0; the analysed set is 705.
- Concepts 115,388. Second-order themes 7,844, all to be placed in B1.

## What the checks found

Eight lines in `defects.jsonl`. The first six: r/tenma has no canvas line; r/archlinux has a coded turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has an undocumented state `collapsed`; concept reach is 1.0 everywhere; r/yogscast's first coded turn is not about the canvas. The seventh (placements before hour 0 in 25 rooms) is answered by the eighth: they are Reddit's tests. QA1-001: the concept-reach threshold stays at 0 items.

## Figures I carry

- Log-log slopes on `items_in_window`: concepts 0.530, second-order themes 0.231.
- Mean `items_in_window` 3,022. `n_off_platform`: median 4, max 88 (dankmemes).
- `px_window_share`: median 0.111, max 0.547; null for tenma. Concentration null in 3 rooms (nonbinary, oltp, wario).

## The onset contrast

`contrast.md` and `prior.md` §6 (members named there). Early (first coded turn hours 0 to before 3): 132. Late (after hour 48): 61. Neither: 512. The confound is size (median items 5149 against 33); held size (items 156 to 2770): 41 against 12.

## The three sentences written before reading, and what the reading found

Expected: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure. Found against them: the artwork was often on the canvas before the room spoke; coordinating turns do not all end near hour 73; rivals often became partners; deals often did not bind the crowd. The patterns seen three or more times in A1 are in `running-A1.md`, with rooms per block.

## Contrary rooms

Blocks 01 to 18 by name only: morrowind, megaman, heyyea, egypt, duckgame, AprilKnights, flashtv, PinkVomitMonster, FloydVsVoid, anime, watchmen, TheAdventuresofTintin, tagpro, qotsa, cfb, drugs, UNLincoln, yerbamate, Redox, azores, archlinux; homelab, hentai, kpop, ubc, norge, cirkeltrek, loltyler1, bobross, nonbinary, zelda; ukplace, SwissNeutralityZone, GuardiansOfDatBoi, minecraft, GuildWars2, bardmains, placeDE; theitalyplace, spacexmasterrace, tampabaylightning, aoe2, 4chan, ice_poseidon, korea, drawhelix; greenlattice, norway, utaustin, france, masseffect, ducks, mariokart, natsume; thebluecorner, germany, vim, furry_irl, placehfarts, Pigifs, TreePlace, evedreddit; falcons, formula1, slovenia, sweden, wine, btc, nin, uoft; ReBoot, nVade, epublica, lego, foxes, math, popheads, ockytop; sadboys, spacex, Fez, warthunder, nascar, israel, magictcg, tenma, ManningPlace; cgpgrey, EraseThePlace, dankmemes, anarcho_capitalism, twice, TeamYellowPlace, mcgill, PokemonSage; totallynotrobots, finland, udub, GreenEmpire, danganronpa, india; ontario, orderofthebluecorner, CelticFc, enterthegungeon, eve, anarchocapitalism, teamcube; counting; polandball, ubreddit, canucks, rust, fivenightsatfreddys, kanye, azerbaijan; theblackvoid, rainbowgrid, raocow, Slovakia, taiwan, oltp, asexual; PlaceNL, pcmasterrace, PinkUnion, streetfighter, aeskwadraat, Mario, wallstreetbets; placestart, starryknights, tf2, brasil, wholesomememes, Thegreatblackhole, GreenCorner, ibo, wario; destiny, Summit1G, Okami, 2007scape, lithuania, stardewvalley, planetside.

Block 19: ainbowroad, dota2, Braveryjerk, dofus, Russiaclan, rotmg.

The one room that fits nothing else, chosen at A1c: r/Summit1G. The second pass (B1d) reads the contrary rooms with the rooms the saturation test finds not fitting.

## Open distinctions, carried into B1

None is filed in `_questions/`. Distinctions forming:
- Who started the work: joining or finding work begun elsewhere, against starting it; a work credited to another sub or its Discord; members working for other rooms' art more than their own (minecraft).
- Where organizing happened: in the thread, against Discord, IRC, Telegram, a second sub, a stream; venues refused or argued over (archlinux, norge); a small room keeping the thread on purpose (samuraijack).
- Deals: binding, against not kept; truce against alliance; living on an ally's land by permission; sheltering under a stronger room's list (bretagne); a host's authority disputed (warframe, seahawks).
- A sub made for the canvas that governs others, polices purity, migrates, claims a colour, or looks for a purpose after the close (pgang).
- Scripts: self-defence, refused, joint across rooms (archlinux), fighting the room's own plan.
- The moderator as organiser, obstacle, funnel, enforcer or permit office; moderators' April Fools rules that hand members power (seahawks) or leave a lasting flair (mls).
- National rooms: flags built, hijacked, covered or merged into hearts; national emblems beside the flag; border fights and federations; fights retold as national history (lithuania, norge).
- The end of organizing: before hour 73, at the close, or in calls to rebuild after it; the work kept elsewhere after the close.

## Ledgers at this close

- A1: `lexicon-A1.md` 1,289 lines; `running-A1.md` 773; `leads-A1.jsonl` 2,478; `departures.jsonl` 9; `defects.jsonl` 8.
- B1: `prior.md`; `notes-B1.md`; `scheme/scheme_current.jsonl` (114 themes over 482 placed second-order themes, 584 placements); `theme_discovery.jsonl` and `ideas-B1.jsonl` (114 lines each); `kinds-B1.jsonl` (659); `multiplacement_log.jsonl` (103); `tier_history.jsonl` (38); `unplaced-B1.jsonl` (4); `episodes-B1.jsonl` (1). `validate.py B1` at this close: 0 errors, 85 warnings (the multiple placements, each on the record).
- Rules kept: fetch every id with `cite.py`; never type an id from memory; never log a placement or note in the same call that writes it before the tool answers; count a ledger's lines after appending; there is no `--kind close`, log the closing line as a note.
- The permission check refuses "=w=", for and while loops, shell functions, heredocs, awk, a variable set from `$(...)`, and some `python3 -c` scripts that write files. Use the Write and Edit tools for file content; an Edit whose old text spans non-adjacent lines fails. The shell shows at most 30 KB per call; the overflow goes under CONTROL, which is read-denied.
- The diary rolls into new parts (B1 is in part B1-6). After a compaction the guard requires the head and stage file read again and the exact line "compacted; head reconciled" through `mem.py log --kind note`.

## The next comparison

Leg B1b-03 opens at the room `mem.py next --stage B1` names (NewMexico, order 42). Declare the stretch (about 1 MB) in the diary. NewMexico is tied to pitt and bostonbruins, both read: check both rooms' concepts as a possible episode: pitt's t06 tells New Mexico asking not to crowd its Zia and one yellow line agreed (hour 70), and bostonbruins' t05 tells New Mexico's half Zia allowed on condition and a request to stop attacking it (hours 58 to 59). The 50-average-room condition will be met early in the stretch (now about 47); from then on a run of 10 average rooms and 10 rooms without a new kind starts the first round, and a round predicted longer than 10 average rooms is logged when it begins. The longest empty run so far is six rooms.

## The scheme as it stands

114 third-order themes, the working grouping in `scheme/scheme_current.jsonl` (`mem.py scheme --brief`). Size distribution: 32 themes hold one second-order theme, 21 two, 12 three; the largest are T3-010 making deals with neighbouring rooms (32, from 31 rooms, 6.6%), T3-001 staging April Fools fake news and T3-017 carrying on the sub's usual talk (24 each), T3-009 celebrating the finished work (22), T3-023 moderators staging an April Fools takeover (21). 35 themes are seen in one room only. T3-010's internal variation is written out in `notes-B1.md`; the first split to test if it passes one in ten is by the object of the bargain (space, help, protection). Boundaries still to draw at B1e are listed there (T3-002 and T3-033; T3-045, T3-094 and T3-046; T3-009, T3-104 and T3-105).

National kinds minted under J's words: T3-065 building the national flag (four rooms, bretagne's regional flag among them), T3-078 helping kin nations with their flags, T3-079 joining neighbouring flags with a heart (lithuania, norge), T3-080 arguing over a political symbol (lithuania, samuraijack, liquicity, norge), T3-081 casting canvas fights as historic national wars (lithuania, norge), T3-085 weighing the room against the nations, T3-099 counting on a bigger neighbour's protection (bretagne under France), T3-113 drawing national emblems beside the flag (norge).
