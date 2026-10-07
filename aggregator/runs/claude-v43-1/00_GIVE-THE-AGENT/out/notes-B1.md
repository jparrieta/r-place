# Notes, stage B1

## Leg B1a, the prior and the order, 2026-10-07

`prior.md` was written first, before any second-order theme was opened. Sections 1 to 6 are filled and dated 2026-10-07. Sections 7 and 8 stay empty until stage D1. Section 1 records J's words for this stage: national, political and conflict content is study material, and the scheme should get as much variance on organizing behaviour as it can early on.

After the prior I read METHOD.md's paragraph on Grodal, Anteby and Holm: categorization is eight moves (asking questions, focusing on puzzles, dropping, merging, splitting, relating or contrasting, sequencing, developing or dropping working hypotheses), and every move is logged with its name.

### The order

`mem.py next --stage B1` drew the order. The seed is in `out/seed.txt` (cd472a6087a223d4), from the sha256 of the store's `rooms.jsonl`, tag B1. `python3 tools/saturation.py order --stage B1` prints all 705 rooms in order. The first ten: sixers, edmontonoilers, chess, lifeisstrange, worldpowers, leagueoflegends, rutgers, drugs, thailand, undertale.

What the start of the order holds, by items in the window (the analysed set's mean is 3,022 items per room; the stopping rule counts words, so these figures are a guide only):
- The first 25 rooms hold about 47 average rooms of items. Several large rooms come early (leagueoflegends, the largest room, is sixth; bitcoin, minecraft and drugs are in the first 25).
- Of the first 50 rooms, 8 are on the early side of the onset contrast and 2 on the late side. Of the first 100, 17 and 7. The contrast's sides are 132 and 61 of 705, so the start of the order is close to their shares.

What I expect of it:
1. **The rule's first estimate will come early in rooms.** No estimate is made before 50 average rooms and 25 rooms are read. With large rooms early, the 25-room condition will bind first, at about 47 average rooms by items. The first rounds will begin after about 25 to 30 rooms.
2. **New kinds will come fast at the front and keep coming.** The first rooms are mixed: sports teams (sixers, edmontonoilers, seahawks, nyjets, bostonbruins, warriors), games (leagueoflegends, undertale, Mario, minecraft, warframe), a national room (thailand, lithuania), a regional one (bretagne), canvas-born rooms (monalisaclan), music, universities. That mix should give variance early, as J asks, without my choosing it. Large rooms early will give many second-order themes each, and many of them will be the April Fools and off-canvas talk that the scheme must place too.
3. **Neighbours will be far apart in the order.** Rooms tied to each other (the hockey rooms, the national rooms around a border) are scattered. The ties will come back through `mem.py neighbours`, `compare` and `leads-A1.jsonl` when the second room of a pair is read, not by reading them together.
4. **The walk will not reach marker 1 quickly.** The coding is near fixed-width per room (second-order themes grow with the 0.231 power of items), so each room adds about the same number of second-order themes whatever its size. With hundreds of kinds expected, I expect new themes to keep coming for well over a hundred rooms.

### Files opened

`tier_history.jsonl` is opened empty at this leg. `ideas-B1.jsonl`, `episodes-B1.jsonl`, `unplaced-B1.jsonl`, `theme_discovery.jsonl`, `kinds-B1.jsonl` and `scheme/scheme_current.jsonl` are written by the verbs or by me as the walk goes. `findings.jsonl` is opened with the scheme's claim at B1e, when the claim exists.

The next leg, B1b-01, opens the walk at the room `mem.py next --stage B1` names (sixers), with its stretch declared in the diary when it opens.

## Leg B1b-01, the first stretch, 2026-10-07

**The stretch.** Order 1 (sixers) to 17 (bitcoin), about 1.05 MB of concepts and second-order themes. Every room was the one `mem.py next --stage B1` named. 197 second-order themes were placed; none is in `unplaced-B1.jsonl`. 90 third-order themes were minted, T3-001 to T3-090. Each was logged as an idea before it was minted.

**How I read.** For each room: my A1 note, then every second-order theme with its note and every concept label, through `out/_analysis/b1_room.py`, which calls `mem.py themes` and `mem.py theme`. leagueoflegends t02 (798 concepts, the moderators' Merrill makeover) was read by its note and a spread of its labels; the note and the labels show one performance. I checked rpi's neighbours; none of them was read yet. No room's forest or case was opened; no theme needed it to be placed.

**New kinds by room.** sixers 19, edmontonoilers 11, chess 7, lifeisstrange 6, worldpowers 4, leagueoflegends 7, rutgers 5, drugs 5, thailand 4, undertale 7, rpi 1, Mario 1, lithuania 4, batman 1, RelientK 2, faeria 0, bitcoin 6. faeria is the first room with no new kind.

**Two process errors, both on the record.**
1. Twelve mints carry the next room in `kinds-B1.jsonl`'s `at` field: I placed a room's last unplaced theme before minting its last kinds, so `mem.py` had moved on. The stopping rule counts those kinds one room late; the four bitcoin kinds (T3-087 to T3-090) will count at criticalrole. The file is never rewritten. From now on every new kind of a room is minted before its last placement.
2. Rule 0. I first placed 88 second-order themes under two to five third-order themes with no record. I unplaced 70 of those placements. 53 themes keep two or three placements, each additional one in `multiplacement_log.jsonl` with concepts of its own, a `why_not_one` and the dispensable placement (66 lines, checked by `out/_analysis/b1_multiplace_write.py` against the store). sixers t06 would need five kinds; it is placed once and recorded `item-is-a-bag`. 35 `tier_history.jsonl` lines record the changed memberships. `validate.py` still warns once per remaining multiple placement; the warning does not read the log.

**What the scheme holds now.** 90 themes over 197 placed second-order themes. Size distribution (second-order themes per theme): 34 hold one, 19 two, 14 three, 7 four, 4 five, 5 six, 3 seven, 1 eight, and one each of 13, 14 and 15. 36 themes are seen in one room only so far. The largest: T3-001 staging April Fools fake news (15), T3-010 making deals with neighbouring rooms (14), T3-017 carrying on the sub's usual talk (13). None holds more than one in ten. T3-010 will be read again for the kinds inside it (truces, borders, protection pacts, help traded for help) when it grows.

**Recurring pairs in the multiplacement log**, the boundaries the scheme has not drawn: T3-027 and T3-028 (arguing over scripts and running them, four rooms); T3-010 with T3-039 (deals and yielding space); T3-009 with T3-043 (celebrating and crediting); T3-014 with T3-013 and T3-015 (Discord, hub subs and official threads).

**What the second-order themes showed that the notes did not predict.** The notes name April Fools jokes as beside the canvas; the themes show they are often most of a room's coded talk, of three kinds (members' fake news, moderators' takeovers, the company's own jokes). leagueoflegends organised on a second surface, the front page, with vote drives and slogans spelled across posts. lithuania spent its work on kin nations' flags, which the notes said, and cast canvas fights as historic national wars, which they did not stress. bitcoin set itself against the national flags.

**Episodes.** None recorded. faeria says r/drugs overran its Yak; r/drugs' own record does not tell it, so it is not one episode told twice.

**Leads carried forward**, for when the other room is read: r/norge hosting the chess knight; r/kanye's pact with sixers; Calgary and edmontonoilers; HunterXHunter, Wales and FaroeIslands beside the butterfly; r/Dota2 with leagueoflegends; Purdue, Boston University and the Big Ten with rutgers; r/MLS and Electric Forest over BOOF IT; the frog's builder, UofT, UBC, Cambodia and Norway with thailand; r/ireland adopting undertale's Temmie; WPI, Purdue, Green Lattice, the Predators and Texas A&M with rpi; theexpanse, Latvia, Belarus and Estonia with lithuania; r/harrypotter with batman; Quebec, r/heyyea and r/edBoxes with RelientK; r/btc, r/ainbowroad, r/CaveStory and r/monero with bitcoin.

**The stopping rule.** `saturation.py status --stage B1`: 17 of 705 rooms read, 3.3% of the words, kinds 86 by the rule's count (the four late-counted bitcoin kinds are not yet in it), coverage 0.904, no rounds, no markers. No estimate is made before 50 average rooms and 25 rooms.
