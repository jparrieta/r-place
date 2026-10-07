# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of B1a, 2026-10-07, the first leg of stage B1.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1 is closed (legs A1a to A1b-55 and A1c). All 705 rooms have a note. Stage B1, the third-order scheme, is open.

**B1a is closed.** `prior.md` was written first, before any second-order theme was opened: sections 1 to 6 filled and dated 2026-10-07, sections 7 and 8 empty until the return stage. The harness seals it; a change now is a departure (rule 10). The order is drawn: seed cd472a6087a223d4 in `out/seed.txt`; `python3 tools/saturation.py order --stage B1` prints it; the first room is sixers. `notes-B1.md` says what I expect of the order. `tier_history.jsonl` is opened empty. No theme is minted yet; `scheme/scheme_current.jsonl` does not exist until the first mint.

**J's words for B1 (7 October 2026):** "national elements are very important here"; "we need to get as much variance on organizing behavior early on so that later we have enough to create the model". National, political and conflict content is study material: a theme about flags, borders, alliances or fights between national rooms is minted, placed and named as plainly as any other. **The handler's rule:** a choice to leave out or soften content for any reason other than the study's goes to J first with `mem.py ask`, and the content stays meanwhile.

**Open question QA1-003:** bakchodi and dankmemes still hold back A1b-10 pre-cut lines after a safety stop in A1b-49; the lines stay in `out/_handling/pretrim-A1/review/`. Read the answer with `mem.py asks QA1-003` when it comes.

## How the B1 walk goes (the stage file, kept here for after a compaction)

- **Legs.** B1b-01, B1b-02 ...: one stretch of the order per leg, about 1 MB of second-order themes and concepts (`mem.py room <sub> --size`: codes plus themes, not the forest). Declare the stretch (first and last order) in the diary when the leg opens. Then B1c (the saturation test), B1d (the second pass), B1e (the scheme standing, handback, interview cut).
- **The next room is always `mem.py next --stage B1`**, at every leg start and after every compaction. It follows the order and the stopping rule. Never a room from memory.
- **Startup packet each leg:** this head, the stage file, the last five diary entries, `mem.py scheme --brief`, `validate.py --open B1`.
- **Per room.** Read its second-order themes and concepts (`mem.py theme <sub>/<tNN>`, `codes --sub`). Read the room on its own first, then against rooms already read that it is tied to (`mem.py neighbours`, `mem.py compare`, any `leads-A1.jsonl` line naming it). For a room whose themes I cannot place with confidence, or whose A1 note marks it unsettled or unsure, read the forest and case too (`mem.py forest`, `mem.py case`), logged with `mem.py log --kind opened --ids <sub>` and why. A room is done when every second-order theme is placed in `scheme_current.jsonl` or listed in `unplaced-B1.jsonl` (`{"sub","second_order","why"}`). A theme that stands alone goes on the rare tier, not out.
- **Verbs, never by hand.** `mem.py idea "<label>" --trigger <sub>:<tNN>` when a theme is first thought of; `mem.py mint --label "..." --trigger <sub>:<tNN>`; `mem.py place <sub>:<tNN> --theme T3-NNN`; `mem.py unplace`. Merges and splits: `mem.py log --kind merged|split --ids <T3 ids>` plus a `tier_history.jsonl` line with `move` and `prompted_by`. A merge or split of a theme with more than twenty members: `log --kind move` and `python3 tools/snap.py B1 move-<move>-<n>`.
- **Grouping.** Gioia's first-order consolidation: stay near the material, let the number explode, get lost before getting found. Kinds, not sizes: one third-order theme is one doing; never split by degree. When in doubt keep two (splitting later is a re-read). No ceiling; hundreds expected (prior §1: 250 to 450). A theme holding more than one in ten second-order themes is read again for kinds inside it. Names 2 to 5 words, gerund-led, near the material, never a construct's name and never one of the four problems.
- **The floor:** a kind seen in two rooms unlike each other (size: at least twice the items; side of the contrast; or form) enters the main scheme; one room only, the rare tier. Two rooms telling one episode (same thread, or same artwork in the same hours) count as one: `episodes-B1.jsonl`.
- **The stopping rule** (`saturation.py status --stage B1`; never count by hand): no estimate before 50 average rooms and 25 rooms; rounds after 10 without a new kind; markers 1 and 2 after three empty rounds each; then the draw (marker 3); then the report and `done.sh B1 --pause` for the PI's decision. The check-in at 60% of the words read before marker 3. A round predicted longer than 10 average rooms is logged when it begins.
- **Reads allowed:** themes and codes room by room, `pairs --level second`, a room's forest and material on demand, my notes through `mem.py note` (a prior, never a source), `contrast.md`, `running-A1.md`, `lexicon-A1.md`, `leads-A1.jsonl`, `coordinating-rule-A1.md`, `organizing_end-A1.jsonl`, `handback-A1.md`, quotes through `cite.py` only. Forbidden: cutting fourth-order themes or dimensions; citing a note.
- **Safe stops:** after each room's themes are placed and logged; `ls .pause`.

## Stage A1, what B1 inherits

- J's rulings of 7 October: hour 0 is the canvas opening (Reddit's tests from about hour -16); the onset is the first coded turn at hour 0 or later; the organizing end is reported with and without calls after hour 73 (`organizing_end-to73-A1.jsonl`); the coordinating rule's measured error is in `coordinating-rule-A1.md`; `leads-outside-frame-A1.jsonl` is a ledger B1 may read; the note length of about 350 words is a guide. QA1-002: organizing is counted before the freeze at hour 73.
- The catch-up pass (A1b-20 to A1b-48) read case.md and brief.md whole for 702 rooms, replaced every `coder unsure:` line from case.md and added dated `later:` lines. The forest is unread for 550 rooms.
- The restore (A1b-49 to A1b-53, and A1b-55) put back my pre-cut words in 447 rooms after the 350-word cap had cut 562 notes. 556 notes are over 350 words. Each leg's choices are in `notes-A1.md`.
- `handback-A1.md` has a section "After A1c (7 October 2026)" with what B1 should know.

## Section 5 of A1

- `coordinating-rule-A1.md`, copied into `prior.md` §5. A turn counts when its label's leading act calls, assigns, plans, reports placement before hour 73, defends, makes or breaks a deal, or corrects another's placement; not when it recounts, jokes, mourns, thanks, praises, apologizes, blames, or is a moderator's removal. After hour 73 only calls or plans for canvas work count.
- Figures: 44,116 of 115,388 concepts coordinate (0.382). Nine rooms have no coordinating turn: watchmen, Redox, yerbamate, Lugarix, azores, ReBoot, PokemonSage, UNLincoln, tetris. 146 rooms end after hour 73. work_remained: kept 347, lost 218, silent 140. Measured error: agreement 79 of 100, precision 0.92, recall 0.66. Median end h72.02 with calls after hour 73, h71.69 without.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04). Dropped 0; the analysed set is 705.
- Concepts 115,388. Second-order themes 7,844, all to be placed in B1.

## What the checks found

Eight lines in `defects.jsonl`. The first six: r/tenma has no canvas line; r/archlinux has a coded turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has an undocumented state `collapsed`; concept reach is 1.0 everywhere; r/yogscast's first coded turn is not about the canvas. The seventh (placements before hour 0 in 25 rooms) is answered by the eighth: they are Reddit's tests.

QA1-001: the concept-reach threshold stays at 0 items; every room is read at concept level in later stages.

## Figures I carry

- Log-log slopes on `items_in_window`: concepts 0.530, second-order themes 0.231.
- Mean `items_in_window` 3,022. `n_off_platform`: median 4, max 88 (dankmemes).
- `px_window_share`: median 0.111, max 0.547; null for tenma. Concentration null in 3 rooms (nonbinary, oltp, wario).

## The onset contrast

`contrast.md` and `prior.md` §6 (members named there). Early (first coded turn hours 0 to before 3): 132. Late (after hour 48): 61. Neither: 512. The confound is size (median items 5149 against 33); held size (items 156 to 2770): 41 against 12.

## The three sentences written before reading, and what the reading found

Expected: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure. Found against them: the artwork was often on the canvas before the room spoke; coordinating turns do not all end near hour 73; rivals often became partners; deals often did not bind the crowd.

Seen three or more times in A1 (rooms per block in `running-A1.md`):
- The brief shows words or habits the canvas work reused; a shared project ran the week before.
- Members saying the canvas did not belong in the sub, or dismissing it.
- Scripts, bots or extra accounts inside the room's own work.
- Members outside the Discord missed the plan or refused the venue; a venue or command could not bind every placer.
- The result disputed or doubted after the close.
- Green Lattice and Rainbow Road as host, permit office and border authority.
- A representative, Discord or deal that cannot bind the crowd.
- A room relocates or trims its work when a neighbour asks.
- Restraint named as the room's rule; qualified by conquest talk; attack talk beside restraint; restraint only after a neighbour objected.
- A neighbour protects the room's work, or a room that wrecked one helps it after.
- Decisions made in Discord, IRC, Telegram or a second sub, seen only as returned.
- One or two members carrying the work; credit as one member's claim.
- Members joining work already under way; a room credited with work another group started; outsiders defending the work.
- A canvas mark, call or label grown from something already running that week.
- Misread edits, and the room's own defenders, scripts or bots undoing its work.
- Bots or scripts deciding what stays, or named as makers.
- Members' own accounts of the same act disagreeing; blame never settled.
- The work called pointless, spam or tiring; the result recounted as partial.
- Moderators gathering, routing or turning the canvas work.
- The room's own April Fools switch or fake rules running beside the canvas.
- The event recruiting into the sub, or to the product.
- The work carried elsewhere after the close.

## Contrary rooms

Blocks 01 to 18 by name only: morrowind, megaman, heyyea, egypt, duckgame, AprilKnights, flashtv, PinkVomitMonster, FloydVsVoid, anime, watchmen, TheAdventuresofTintin, tagpro, qotsa, cfb, drugs, UNLincoln, yerbamate, Redox, azores, archlinux; homelab, hentai, kpop, ubc, norge, cirkeltrek, loltyler1, bobross, nonbinary, zelda; ukplace, SwissNeutralityZone, GuardiansOfDatBoi, minecraft, GuildWars2, bardmains, placeDE; theitalyplace, spacexmasterrace, tampabaylightning, aoe2, 4chan, ice_poseidon, korea, drawhelix; greenlattice, norway, utaustin, france, masseffect, ducks, mariokart, natsume; thebluecorner, germany, vim, furry_irl, placehfarts, Pigifs, TreePlace, evedreddit; falcons, formula1, slovenia, sweden, wine, btc, nin, uoft; ReBoot, nVade, epublica, lego, foxes, math, popheads, ockytop; sadboys, spacex, Fez, warthunder, nascar, israel, magictcg, tenma, ManningPlace; cgpgrey, EraseThePlace, dankmemes, anarcho_capitalism, twice, TeamYellowPlace, mcgill, PokemonSage; totallynotrobots, finland, udub, GreenEmpire, danganronpa, india; ontario, orderofthebluecorner, CelticFc, enterthegungeon, eve, anarchocapitalism, teamcube; counting; polandball, ubreddit, canucks, rust, fivenightsatfreddys, kanye, azerbaijan; theblackvoid, rainbowgrid, raocow, Slovakia, taiwan, oltp, asexual; PlaceNL, pcmasterrace, PinkUnion, streetfighter, aeskwadraat, Mario, wallstreetbets; placestart, starryknights, tf2, brasil, wholesomememes, Thegreatblackhole, GreenCorner, ibo, wario; destiny, Summit1G, Okami, 2007scape, lithuania, stardewvalley, planetside.

Block 19: ainbowroad, dota2, Braveryjerk, dofus, Russiaclan, rotmg.

Catch-up notes whose not-this line the account qualified: utaustin, miamidolphins, placehearts, chicubs, lego, lebanon, israel, vegan, touhou, magictcg, straya, farmcarrots, TransFlagPlace, titanfall, rust, funhaus, AmericanFlaginPlace, trees, starvstheforcesofevil, brasil, prequelmemes, phish, bardmains, osu, vim, TreePlace, bih, japan, PORTUGALCARALHO, npr, GreenEmpire, armenia, satania, nyjets, hoodr, muse, esperanto, araragi, twentyonepilots, GreenCorner, Thegreatblackhole, yogscast, forsen, AcePlace, lithuania, terraria, PinkVomitMonster, DatBoi, WPI, ubc, texastech, linux, dallasstars, oman, sixers, aceattorney, sakuragakuin, quq, lsu, vermont, norway, FlipnoteStudio3D, placesnek, TheB1G, bulgaria, nVade, cardinals, COSI, bretagne, hungary, ucf, donaldglover, aggies, lifeisstrange, mindcrack, CKCrusaders, pitt, taiwan, msu, portal, catalonia, PinkUnion, gratefuldead, cavestory, destiny, daftpunk, WisconsinBadgers, seventeen, Russiaclan.

The one room that fits nothing else, chosen at A1c: r/Summit1G.

## Open distinctions, carried into B1

None is filed in `_questions/`. Distinctions forming:
- Who started the work: joining or finding work begun elsewhere, against starting it; a linked region placed from the first hours, against the room's late first call; a work credited to another sub or its Discord; a work the room mourned as lost that the canvas keeps.
- Where organizing happened: in the thread, against Discord, IRC, Telegram, a second sub, a private sub (ockytop), a forum, or a stream; venues interleaved (esperanto); plans brought back for members outside the venue.
- Deals: binding, against not kept; truce against alliance; living on an ally's land by permission; hosting others' works for upkeep (TeamYellowPlace); leaders' deals against members' fights; a room kept by the stronger side's terms (Slovakia).
- A sub made for the canvas that governs others, polices purity, migrates, or claims a colour; or forms late around a pattern others repeated (rainbowgrid).
- Scripts: self-defence, refused, repairing a rival, joint, fighting the room's own plan, a neighbour's bot erasing an unregistered addition (yumenikki); hand defence against scripts (GabrielDropout).
- The moderator as organiser, obstacle, funnel, enforcer or permit office; a moderator who is also the main defender (oneplus).
- National rooms: flags built, hijacked, covered or merged into hearts; border fights and federations between nations; rival flags inside one nation; political symbols covered or drawn.
- The end of organizing: before hour 73, at the close, or in calls to rebuild after it; the work kept elsewhere after the close.

## Ledgers at this close

- A1: `lexicon-A1.md` 1,289 lines; `running-A1.md` 773; `leads-A1.jsonl` 2,478; `departures.jsonl` 9; `defects.jsonl` 8.
- B1: `prior.md`; `notes-B1.md`; `tier_history.jsonl` (empty). `validate.py B1` at this close: 0 errors, 0 warnings.
- Rules kept: fetch every id with `cite.py`; never type an id from memory; never log a placement or note in the same call that writes it before the tool answers; count a ledger's lines after appending; there is no `--kind close`, log the closing line as a note.
- The permission check refuses "=w=", for and while loops, shell functions, heredocs, awk, a variable set from `$(...)`, and some `python3 -c` scripts that write files. Use the Write and Edit tools for file content; an Edit whose old text spans non-adjacent lines fails. The shell shows at most 30 KB per call; the overflow goes under CONTROL, which is read-denied.
- The diary rolls into new parts (A1 is in part A1-58). After a compaction the guard requires the exact line "compacted; head reconciled" through `mem.py log --kind note`.

## The next comparison

Leg B1b-01 opens the walk at the room `mem.py next --stage B1` names (sixers). Declare the stretch (about 1 MB) in the diary. Read each room's second-order themes and concepts, log ideas before mints, mint and place through the verbs, record episodes and unplaced themes, and keep two when in doubt.

## Nothing changed in the scheme or the model

No third-order theme exists yet.
