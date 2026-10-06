# Head, claude-v43-1

Target length: under 3,000 words. Rewritten whole at every close. Last written at the close of A1b-08, 2026-10-06.

## The method question, in one sentence

Can independently reconstructed case histories be composed into a shared dynamic account that supports explanations at successive levels of specificity, from population-wide patterns, through forms and subforms, to particular organizational histories, while keeping access to the evidence from which those explanations were developed?

The theory question is unchanged: when strangers organize on a clock they did not set, with no way to compel anyone and no goal given to them, what forms does organizing take, how do they differ in their functioning, and which of them keep the work alive?

## Where the run stands

Stage A1, the reading. Leg A1a did the checks, the screen and the order. Legs A1b-01 to A1b-08 read blocks 01 (53 rooms), 02 (48), 03 (62), 04 (44), 05 (34), 06 (37), 07 (36) and 08 (30) whole. 344 of 705 rooms have a note in `out/rooms/`. 361 rooms remain, in blocks 09 to 19. The next leg is A1b-09. At this close `mem.py next` names r/southafrica, the first room of block 09. Always take the next room from `mem.py next`, never from this file.

The order is in `out/order-A1.txt`, a seeded shuffle (seed 20261006) cut into blocks of about 3 MB by `mem.py`'s byte count. Block 13 is r/counting alone, at 11.17 MB.

`validate.py A1` at this close: 0 errors, 0 warnings. 344 notes over 705.

## The census and the analysed set

- Census 705 rooms (`package/FRAME.md`, copy date 2026-10-04, hash 51513b1e...). Every count agrees across the frame, `rooms.jsonl`, the folders, the concepts and the themes.
- Screen: dropped 0, so the analysed set is 705. `dropped.jsonl` is written empty.
- Concepts 115,388. Second-order themes 7,844, all to be placed when the themes are placed later in the run.

## What the checks found

Six defects are in `defects.jsonl`; none blocks the reading. In short: r/tenma has no canvas line; r/archlinux has a coded turn at hour 100.9; `n_codes_coder` has two meanings; `items.jsonl` has an undocumented state `collapsed`; concept reach is 1.0 everywhere; r/yogscast's first coded turn is not about the canvas. Two departures are in `departures.jsonl`, both saved scripts in `out/_analysis/`. r/tenma comes in block 09.

A possible seventh defect, not yet filed: linked artworks with region placements before hour 0. Ten cases: r/FloydVsVoid h-14.47, r/ProfessorLayton h-13.49, r/SwissNeutralityZone h-14.52, r/monalisaclan h-15.23, r/radiohead h-11.54, r/aoe2 h-0.66, r/thebluecorner h-12.34, r/globaloffensive h-13.62, r/GrowTheTree h-0.24, r/nin h-11.52. No block 08 room added a case; all its placements start between h0.93 and h2.41. The canvas window runs from -16, so this may be by design. No `mem.py` verb found so far reads `package/DATA-manifest-canvas.md`. Check the manifest through the verbs before filing it.

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

Block 08 early rooms, five: r/overwatch, r/ockytop, r/ireland, r/foxes, r/rocketleague. r/ireland grew a flag that carried other subs' art. r/ockytop built a Power T at h1.6 and lost it to r/ukplace's script at h69. r/rocketleague moved its logo next to the Blue Corner and kept one rainbow stripe by deal. r/overwatch's moderators removed canvas calls while the work ran in Discord. r/foxes is early only by its first call at h2.7: its fox was built from h65, moved twice, and was covered at h72.8.

Block 08 late room, one: r/nVade (h52.86). It is a sub made at h54 as the new home of r/greenguys, with no pre-event members. Its turns are deals with Rainbow Road, a treaty border with the Duck, and a takeover by Scotland that ended in an apology. Its writers placed 0.146 of the linked artwork. Block 07's two late rooms (r/wsu, r/crystalclear) placed small marks in leftover space; r/nVade defended a large work begun before its sub existed. No size test yet.

## The three sentences written before reading, against eight blocks

The three sentences: one burst of calls in the first day or two, then defence and looking back, with coordinating turns ending near hour 73; fights with canvas neighbours and deals about borders, struck in the thread or sent to Discord; the goal set early by one call and changed only under pressure.

1. The artwork was often there before the room spoke, and other subs often made it. Block 08: r/ReBoot's logo had placements from h1.34, and its one call at h10.4 went unanswered until a member of r/TwoBestFriendsPlay brought that sub's effort at h68.7. r/GranColombia's flag had placements from h1.42, 42 hours before its first coded turn. A r/buffalo member found a Bills logo already there, and others thanked unknown makers. r/lego's logo stands where r/denmark planned it, and the artwork is shared with r/denmark.
2. Coordinating turns end mostly between hours 68 and 73. Block 08: r/rocketleague h72.88, r/sabres h72.97, r/lebanon h72.91, r/nVade h72.76, r/vinesauce h72.88, r/edmontonoilers h72.28, r/popheads h72.43, r/foxes h72.86, r/ockytop h72.04. Earlier ends: r/ReBoot h68.73, r/lego h68.61, r/GranColombia h68.04, r/gatech h70.59, r/buffalo h71.08, r/epublica h71.90. After the close r/sabres, r/buffalo and r/epublica moved to PlaceTwo; r/ockytop adopted a restored image.
3. Fights are with neighbours, and rivals often turn into partners. Block 08: r/edmontonoilers left the Flames logo alone so its own would not be wrecked back, then made a defence pact with Calgary, cursed after the close. r/sabres turned the Red Wings' scripted invasion into a deal giving them space. r/foxes' overwriter r/homelab stopped, repaired the fox and was offered help back. r/lebanon gave Austria one heart for peace. r/ockytop's Viking ship rivals let Tennessee go behind them.
4. Deals are struck in the thread, in Discord, or both, and they often do not bind the crowd. Block 08: r/gatech's stinger treaty with Mona Lisa held only after Mona Lisa members moved to remove the stinger and others restored it. r/rocketleague's own members kept removing the rainbow stripe the room agreed to keep. r/nVade's Rainbow Road deal did not hold on the canvas until the other side's moderators told their people to stop. r/lebanon's moderator messaged a placer who did not know of the Austrian treaty.
5. The goal is often set by one member. Block 08: r/epublica's flag, rules and deals came mostly from one member (57% of coded turns); r/math's identity was one member's; r/ReBoot's one call was one member's.
6. April Fools makeovers filled most coded turns in many rooms: r/lego (a bootleg brand allowed for a day), r/popheads (fake releases; its first saxophone call was part of the joke), r/rocketleague (vegetable ranks), r/edmontonoilers (a self-aware moderator bot).
7. Moderators: r/ireland's moderators declined a stance and herded talk into megathreads; r/overwatch's removed canvas calls; r/lebanon's ran a megathread and enforced a treaty; r/nVade's refused an outside call to attack under a no-politics policy.
8. The canvas fields name covered works or remains: r/edmontonoilers ("Edmonton Oilers (covered)"), r/popheads ("(Covered) Saxophone"), r/ockytop ("Remains of r/ockytop"). Each matches the room's own report of loss.

New in block 08, seen three or more times and logged in the diary:
- A regional or national room sends canvas talk to a second sub made for it (ireland to r/PlaceIreland, sabres and buffalo to r/716Place, colombia to r/GranColombia, ockytop to the private r/ProtectTheT). r/GranColombia served three nations. r/ProtectTheT shut out members who wanted to help.
- A room gets leave or recognised status from r/ainbowroad or its moderators (gatech, foxes, nVade, rocketleague).
- A treaty about one small part of a work: gatech's stinger, rocketleague's one stripe, lebanon's one heart. In two of them the other side's members tried to undo it.
- An invader apologises on behalf of its sub and helps repair (r/Scotland in nVade, r/homelab in foxes, r/totallynotrobots after the close).
- The room says it has too few people (sabres, vinesauce, popheads, lebanon, epublica, bangladesh).
- The work moved two or more times (foxes, vinesauce, scp, pansexual).
- The canvas field names the work covered or remains (edmontonoilers, popheads, ockytop).
Seen earlier in block 08 and logged: subs made for the canvas run protectorates (TheFarLeftSide); rooms join r/placestart's taskbar by treaty (rocketbeans, metalcore); pride flags move to avoid fights (pansexual, bisexual).

Paired lead checks, both sides read, block 08: agree for TheFarLeftSide, bisexual, ireland, greenbaypackers and minnesotavikings, math and heroesofthestorm, overwatch, lost, metalcore and TheGreatGreenBox, pansexual and kcroyals, rocketleague with hearthstone and lofihiphop, bostonbruins with sabres, lego with denmark and frankocean, foxes with redpandas, buffalo with sabres, ockytop with ukplace, lebanon with latvia and genderfluid, gatech with monalisaclan, virginiatech and frc, edmontonoilers with calgaryflames and globaloffensive, GranColombia with colombia, epublica with spacexmasterrace. Agree in part: foxes and homelab (homelab's note has a moderator-led banner takeover; foxes names homelab as the overwriter who repaired); buffalo and chicago (a chicken wing, not a declined offer); popheads with the habs lead about Buffalo's chicken wing on the sax. Not found in the concepts read: habs (on buffalo), ducks and utaustin (on ockytop), iastate and berkeley (on gatech).

## Contrary rooms

Block 01: morrowind and megaman said they were not organized; heyyea kept art it did not make; egypt's flag was a stranger's gift; duckgame mourned art the atlas lists as surviving; AprilKnights had an order with elections; flashtv's prank ran apart from canvas work; PinkVomitMonster called its lack of coordination its beauty; FloydVsVoid's founder regretted not compromising; anime mostly refused and argued credit; watchmen and TheAdventuresofTintin noticed art they did not visibly build; tagpro aimed at advertising; anime, qotsa, cfb and drugs disagree with the canvas fields. From the screen: UNLincoln, yerbamate, Redox, azores, archlinux.

Block 02: homelab, hentai, kpop and ubc, norge, cirkeltrek, loltyler1, bobross and nonbinary, zelda.

Block 03: ukplace, SwissNeutralityZone, GuardiansOfDatBoi, minecraft and GuildWars2, bardmains, placeDE.

Block 04: theitalyplace and spacexmasterrace; tampabaylightning; aoe2; 4chan; ice_poseidon; korea; drawhelix.

Block 05: greenlattice, norway, utaustin, france, masseffect, ducks and mariokart, natsume.

Block 06: thebluecorner, germany, vim, furry_irl, placehfarts, Pigifs, TreePlace, evedreddit.

Block 07: falcons, formula1, slovenia, sweden, wine, btc, nin, uoft.

Block 08:
- ReBoot: its one call went unanswered for 58 hours; the logo that held was another sub's effort.
- nVade: it refused an outsider's call to attack after a takeover, took an apology, and a member said its earlier concessions had invited the takeover.
- epublica: one member wrote most of its plans and deals, and it asked every neighbour before it grew.
- lego: a large room whose logo stands where another sub planned it, while members asked to ban canvas posts.
- foxes: the first call came at h2.7 but the fox was built only in the last eight hours.
- math: most calls drew one or two replies.
- popheads: its canvas call began as an April Fools joke.
- ockytop: its private planning sub shut out members who wanted to help.

## Open distinctions

None is filed in `_questions/`. Distinctions forming, to watch in block 09:
- joining or finding work begun elsewhere, against starting it;
- organizing in the thread, against organizing in Discord or a second sub and reporting back; and a second sub that is open, against one that is private;
- deals that bind a room, against deals made by a few that the crowd ignores;
- a treaty over the whole work, against one over a small part (a stinger, a stripe, a heart);
- a deal turned into a room rule, against a deal held only by the organiser;
- a sub made for the canvas that governs others (greenlattice, thebluecorner, placehearts, TheFarLeftSide), against one that keeps a single work (nVade, epublica, GranColombia);
- a national flag run as a permission office (sweden, denmark with lego), against one run as a front line;
- one organiser with alts or friends, against a room-wide effort;
- attacking first and building later, against building first and defending;
- rivals who stay rivals, against rivals who build together, against rivals who make a pact and curse it after;
- an invader who apologises and repairs, against one who does not;
- the room's April Fools practice, against its canvas practice;
- the moderator as organiser, as obstacle, as gatekeeper to a second sub, as enforcer against the room's own vandals, and as enforcer of a treaty;
- the canvas fields linking the room's work, against linking a neighbour's, a rival's, a covered work, or nothing it describes.

## The last rooms read

Block 08, in reading order: TheFarLeftSide, scp, bisexual, ireland, stardustcrusaders, greenbaypackers, math, overwatch, metalgearsolid, rocketbeans, lost, metalcore, bangladesh, pansexual, opticgaming, rocketleague, ReBoot, sabres, lego, foxes, buffalo, ockytop, lebanon, nVade, vinesauce, GranColombia, gatech, edmontonoilers, popheads, epublica.

## Ledgers at this close

- `lexicon-A1.md`: 678 lines. `running-A1.md`: 311 lines. `leads-A1.jsonl`: 1,288 lines. Every lead's `other` is in `order-A1.txt`, letter case aside; checked at this close with grep, sort and comm.
- In this leg one lead named a room outside the frame (bisexual to lgbt) and one carried a typed id (edmontonoilers to rangers); both lines were removed, the second re-appended with the fetched id, and the diary names each. Two lexicon lines carried a later or wrong item (vinesauce Vineshroom, edmontonoilers battle of Alberta), and four lacked the h prefix on the hour (ReBoot, sabres); corrected lines were appended for all six.
- Rule, kept from block 06 and broken once this leg: fetch every id with `cite.py` and check every lead's room with grep against the frame in one call; append in a later call. Never type an id from memory, and never pipe a mixed list of fetched and typed ids into a ledger.
- The hook rejects notes of 350 words or more, and quotes of four words or more outside `struck by`. First drafts still run 360 to 400; draft the `doing` line at about 150 words.

## The next comparison

In block 09, for every room: did the artwork exist before the room's first call, and who built it? Do the canvas fields link the work the room describes, or name it covered? Was the deal struck in the thread, in Discord or in a second sub, open or private, and did the crowd accept that it bound them? Which side of the onset contrast is the room on, and is it a sub made for the canvas? Read r/ManningPlace against r/falcons; r/israel against r/lebanon's call to build over the Israeli flag; r/asexuality against r/pansexual's dispute with the ace flag's builders; r/warriors against r/sabres' flash effort on the Warriors logo; r/italy against r/theitalyplace; r/spacex against r/spacexmasterrace and r/epublica; r/tenma against its missing canvas line (defect 1). Late-side rooms in block 09 to check against contrast.md line 42 include r/UMiami, r/sooners and r/corridor.

## Nothing changed in the scheme or the model

No scheme exists at A1, and none may be written in this stage.
