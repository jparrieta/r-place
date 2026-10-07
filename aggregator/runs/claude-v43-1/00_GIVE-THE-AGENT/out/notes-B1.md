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
