# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-07, 2026-10-06.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1, the reading. Leg A1a did the checks, the screen and the order. Legs A1b-01 to A1b-07 read blocks 01 (53 rooms), 02 (48), 03 (62), 04 (44), 05 (34), 06 (37) and 07 (36) whole. 314 of 705 rooms have a note in `out/rooms/`. 391 rooms remain, in blocks 08 to 19. The next leg is A1b-08. At this close `mem.py next` names r/TheFarLeftSide, the first room of block 08. Always take the next room from `mem.py next`, never from this file.

The order is in `out/order-A1.txt`, a seeded shuffle (seed 20261006) cut into blocks of about 3 MB by `mem.py`'s byte count. Block 13 is r/counting alone, at 11.17 MB.

`validate.py A1` at this close: 0 errors, 0 warnings. 314 notes over 705.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed when the themes are placed later in the run.

## What the checks found

Six defects are in `defects.jsonl`; none blocks the reading. In short: r/tenma has no canvas line; r/archlinux has a coded turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has an undocumented state `collapsed`; concept reach is 1.0 everywhere; r/yogscast's first coded turn is not about the canvas. Two departures are in `departures.jsonl`, both saved scripts in `out/_analysis/`.

A possible seventh defect, not yet filed: linked artworks with region placements before hour 0. Ten cases now: r/FloydVsVoid h-14.47, r/ProfessorLayton h-13.49, r/SwissNeutralityZone h-14.52, r/monalisaclan h-15.23, r/radiohead h-11.54, r/aoe2 h-0.66, r/thebluecorner h-12.34, r/globaloffensive h-13.62, r/GrowTheTree h-0.24, r/nin h-11.52. r/nin and r/radiohead sit side by side and share the same early start, which points to the canvas window rather than to the rooms. The canvas window runs from -16, so this may be by design. No `mem.py` verb found so far reads `package/DATA-manifest-canvas.md`. Check the manifest through the verbs before filing it.

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

Block 07 early rooms, nine: r/halo, r/texans, r/formula1, r/fullcommunism, r/bindingofisaac, r/sweden, r/h3h3productions, r/transgender, r/denmark. Most of them claimed space within hours and then spent the week on treaties, permissions and repairs; r/sweden became a permission office. Block 07 late rooms, two: r/wsu (h50.9, a small WSU on top of the RWBY sign, chosen as one of the few areas that would not start a war) and r/crystalclear (h61.7, a small tag inside another work's border, because the room is small). Both late rooms placed small marks in leftover space, and in both the writers placed almost none of the linked artwork. No size test yet.

## The three sentences written before reading, against seven blocks

The three sentences: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

1. The artwork was often there before the room spoke, and other subs often made it. In block 07 nearly every linked artwork has placements hours or days before the room's first call. The room's writers placed almost none of it in r/lexington (0.002), r/wsu (0), r/transgender (0.01), r/wine (0.015), r/davidbowie (0.02) and r/TheB1G (0.029). r/wine's own member agreed the French made the wine glass beside its tag.
2. Coordinating turns end mostly between hours 62 and 73. Block 07: r/denmark h71.6, r/japan h69.5, r/formula1 h70.0, r/canada h72.2, r/sweden h72.9, r/texans h72.8. Earlier ends: r/TheB1G (planning moved to PlaceTwo), r/acecombat h72.5, r/lexington h52.9, r/crystalclear h62.9, r/wsu h63.0. After the close r/fullcommunism, r/bulgaria and r/bindingofisaac moved to clone canvases.
3. Fights are with neighbours, and rivals often turn into partners. Block 07: r/simonfraser turned a fight with Turkey into a deal to defend Turkey's flag; r/indonesia and r/dwarffortress negotiated a move south after retaliation; r/formula1 apologised for its checkers eating r/ftlgame's Lanius; r/bostonbruins apologised for wiping out Crash and promised to help rebuild it.
4. Deals are struck in the thread, in Discord, or both, and they often do not bind the crowd. Block 07: r/sweden planned in a Discord of over a hundred and voted plans there; r/denmark's members said its Discord could not be stopped and apologised after for breaking every alliance at the end; r/indonesia and r/bulgaria disowned expansions made by a few while others slept; r/flyers met r/shyvanamains' complaint that one user's agreement cannot bind every lurker.
5. The goal is often set by one member. Block 07: r/davidbowie's portrait began with one member's call at the chin; r/wsu's two attempts were one member's; r/bannedfromanime_irl's record holds only the result.
6. April Fools makeovers filled most coded turns in many rooms: r/halo, r/acecombat (HAWX), r/formula1 (Kimi day), r/uoft (a swap with Waterloo), r/texans (Katawa Shoujo), r/hunterxhunter earlier.
7. Moderators: r/canada's and r/sweden's moderators sent canvas talk to second subs (r/placecanada, r/SwedenOnPlace); r/uoft's moderator banned members caught vandalising the room's own work; r/japan's moderators distanced themselves and asked members not to brigade.
8. The atlas names relocated or covered works: r/indonesia ("Relocated Indonesian Flag"), r/picturegame ("Remnants of the /r/PictureGame Kiwi").

New in block 07, seen in three or more rooms and logged in the diary:
- A national sub's moderators send canvas talk to a second sub made for it (norway, germany, canada, sweden).
- Plans voted in Discord and brought back to the sub (sweden, denmark, bulgaria).
- Rooms trade space for help: two pixels for help, a spot given up for help rebuilding (ripcity and compsoc, acecombat and habs, simonfraser and Turkey).
- Members disown an expansion made by a few (indonesia, denmark, bulgaria).

Paired lead checks, both sides read, block 07: agree for ubc and simonfraser, korea and japan, Honduras and canada, habs and acecombat, heroesofthestorm and bindingofisaac, earthbound and sixers with ChronoTrigger, compsoc, utahjazz and seahawks with ripcity, osu and uiuc with TheB1G, radiohead and toolband with nin, dwarffortress, minecraft and MMA with indonesia, ftlgame, placesnek and soylent with formula1, partyparrot and fullcommunism, katawashoujo, miamidolphins and placehearts with texans, thebluecorner, france and placehfarts with placehearts, Pigifs and halo, asktransgender and transgender, maryland, norge, denmark, berkeley and hunterxhunter with sweden, norge, survivor and frankocean with denmark. Disagree in part: r/uvic says r/uoft planned to replace its logo; r/uoft's record shows the plan proposed and rejected. Not found in the concepts read: r/latvia, r/germany (on denmark), r/catholicism (on flyers), r/rit (on bostonbruins), r/placeportalpattern (on indonesia).

## Contrary rooms

Block 01: morrowind and megaman said they were not organized; heyyea kept art it did not make; egypt's flag was a stranger's gift; duckgame mourned art the atlas lists as surviving; AprilKnights had an order with elections; flashtv's prank ran apart from canvas work; PinkVomitMonster called its lack of coordination its beauty; FloydVsVoid's founder regretted not compromising; anime mostly refused and argued credit; watchmen and TheAdventuresofTintin noticed art they did not visibly build; tagpro aimed at advertising; anime, qotsa, cfb and drugs disagree with the canvas fields. From the screen: UNLincoln, yerbamate, Redox, azores, archlinux.

Block 02: homelab, hentai, kpop and ubc, norge, cirkeltrek, loltyler1, bobross and nonbinary, zelda.

Block 03: ukplace, SwissNeutralityZone, GuardiansOfDatBoi, minecraft and GuildWars2, bardmains, placeDE.

Block 04: theitalyplace and spacexmasterrace; tampabaylightning; aoe2; 4chan; ice_poseidon; korea; drawhelix.

Block 05: greenlattice, norway, utaustin, france, masseffect, ducks and mariokart, natsume.

Block 06: thebluecorner, germany, vim, furry_irl, placehfarts, Pigifs, TreePlace, evedreddit.

Block 07:
- falcons: its canvas work was against a rival's taunt, and the canvas fields link that taunt, shared with patriots.
- formula1: its own checkers spread over neighbours until its members called them a new void and stopped them.
- slovenia: its own scripts fought each other over a linden leaf no one agreed.
- sweden: ran the largest flag as a permission office, sparing rooms that asked.
- wine: a member agreed the French made the wine glass beside the room's tag.
- btc: the two Bitcoin factions fought over the label on a shared logo; the canvas fields link a small mark far from it.
- nin: one member attacked the room's own logo to protest canvas posts.
- uoft: a moderator banned members for vandalising the room's own work.

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to watch in block 08:
- joining or finding work begun elsewhere, against starting it;
- organizing in the thread, against organizing in Discord or a second sub and reporting back;
- deals that bind a room, against deals made by a few that the crowd ignores;
- a deal turned into a room rule, against a deal held only by the organiser;
- a sub made for the canvas that governs others (greenlattice, thebluecorner, placehearts), against one that only keeps a small piece (TreePlace, GrowTheTree);
- a national flag run as a permission office (sweden), against one run as a front line (denmark);
- one organiser with alts or friends, against a room-wide effort;
- attacking first and building later, against building first and defending;
- rivals who stay rivals, against rivals who build together;
- the room's April Fools practice, against its canvas practice;
- the moderator as organiser, as obstacle, as gatekeeper to a second sub, and as enforcer against the room's own vandals;
- the canvas fields linking the room's work, against linking a neighbour's, a rival's, or nothing it describes.

## The last rooms read

Block 07, in reading order: porterrobinson, fullcommunism, placehearts, lexington, simonfraser, denmark, slovenia, texans, wine, halo, TheB1G, ripcity, flyers, bulgaria, wsu, japan, formula1, indonesia, bannedfromanime_irl, nin, btc, acecombat, canada, bostonbruins, crystalclear, sweden, luxembourg, bindingofisaac, h3h3productions, ChronoTrigger, davidbowie, uoft, transgender, picturegame, falcons, Jamaica.

## Ledgers at this close

- `lexicon-A1.md`: 638 lines. `running-A1.md`: 275 lines. `leads-A1.jsonl`: 1,133 lines. Every lead's `other` is in `order-A1.txt`, letter case aside; checked at this close with grep, sort and comm.
- In this leg one lead named a room outside the frame (acecombat to murica); validate caught it, the line was removed, and its content is in the diary. Three lexicon lines carried wrong or invented ids (denmark 2, texans 1); corrected lines were appended and the diary names each one.
- Rule, kept from block 06 and broken twice this leg: fetch every id with `cite.py` and check every lead's room with grep against the frame in one call; append in a later call. Never type an id from memory.
- The hook rejects notes of 350 words or more, and quotes of four words or more outside `struck by`. First drafts still run 360 to 430; aim for 300.

## The next comparison

In block 08, for every room: did the artwork exist before the room's first call, and who built it? Do the canvas fields link the work the room describes? Was the deal struck in the thread, in Discord or in a second sub, and did the crowd accept that it bound them? Which side of the onset contrast is the room on, and is it a sub made for the canvas? Block 08 opens with r/TheFarLeftSide, the organising sub r/fullcommunism sent its planning to: read it against r/fullcommunism, r/partyparrot and r/completeanarchy. Read r/overwatch against r/globaloffensive and r/porterrobinson's neighbours, r/edmontonoilers against r/globaloffensive, r/ireland against r/placehearts and r/germany, r/lego against r/denmark. r/ManningPlace, read against r/falcons, comes in block 09.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
