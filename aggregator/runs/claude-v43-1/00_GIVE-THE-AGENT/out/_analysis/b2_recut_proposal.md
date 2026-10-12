
### The bag recut: a proposal to J (QB2-010), not yet acted on

J ruled (QB2-008) that a second-order theme whose concepts spread over 16 to 85 third-order themes was cut too coarse. One item should sit in one theme most of the time, a few in two or three. Nothing below is cut until J's word.

**How coarse the themes are** (`out/_analysis/b2_recut_survey.py`, one line per theme in `b2_recut_survey.tsv`):
- The store's 7,844 second-order themes hold a median of 8 concepts (90th percentile 31, 99th 111, maximum 798).
- B1 placed 3,977 on one kind, 1,972 on two and 1,837 on three. It recorded 846 as bags, themes needing more than three kinds.
- 98 themes hold 100 or more concepts, together 14.5% of all concepts; 49 of them are B1 bags.
- With J's floor applied to round 2's also_present (three concepts of the item's own), readers still name 14 to 43 kinds on 2007scape t04 and 21 to 24 on sweden t01.

**A cut by thread does not work.** The bags were gathered across threads by what the concepts do. On ainbowroad t03, 309 of 326 concepts are alone in their thread; on sweden t01, 202 of 310. A neutral cut by thread would leave hundreds of one-concept parts. The cut has to be by doing, which is coding work.

**The sibling citations.** Most of round 2's failing lines cite concepts of sibling themes of the same room. They split into two groups:
- In packets 3 and 5 the sibling was in the same packet: theblackvoid t09 beside t12, ainbowroad t11 beside t07. The reader mixed two items of one room.
- In packets 2 and 4 the room had one item in the packet (sweden t01, ainbowroad t04, dota2 t05, leagueoflegends t02), so the cited ids were never shown. Room ids run in sequence, and an invented number in range nearly always lands on a sibling.

So the citations are not evidence that sibling themes overlap, and the proposal does not regroup siblings. Fleet ids stop the second group. For the first group, the packet builder could keep one item per room in a packet, with J's agreement.

**The proposal.**
1. **Which items.**
   - At once, before round 3: the hard set's six author bags (2007scape t04, theblackvoid t12, ainbowroad t03, t04 and t07, sweden t01) and the gold set's bags.
   - Before B3, by the same rule: every B1 bag (846 themes), and every theme of 100 or more concepts that round 3 shows to need more than three kinds.
   - The round-1 items I placed as bags in round 1 (Goodboye t03, acecombat t05) follow the same rule if they still need more than three kinds.
2. **By what rule.**
   - I read the theme whole, in a blind window (`mem.py blind on`), so B1's working placements are hidden.
   - I group its concepts into children, each one doing in the room's own terms. Each child gets a label and a note written as a second-order theme, with no third-order ids and no scheme words.
   - A child needs at least three concepts (J's floor). A concept that fits no child of three joins the nearest child by its doing.
   - Every concept goes to exactly one child, and the parent's concept ids are kept.
   - Then, outside the window, each child is placed like any item, with a target of one third-order theme and at most three. A child that still needs more than three is cut again.
3. **With which verbs.** No verb cuts a second-order theme today: `package/store` is read-only, and `reassign` re-places a theme only after a recut. I propose J adds two verbs:
   - **A recut writer**, `mem.py recut <sub>:<tNN> --child "label|note|c1,c2,..." --reason ...`. It writes a recut layer beside the store (`out/recut/themes.jsonl`, the children with new room ids after the room's last tNN, and `out/recut/codes.jsonl`, each concept's child). It marks the parent superseded, never deletes it, and logs kind split.
   - **Store readers** (`mem.py theme`, `codes --sub`, `packets.py`'s Store) that read the layer.

   The children also need fleet ids. J's table maker would draw new T2 ids from the same space, so `fleet_ids.jsonl` covers them.
4. **What it reopens of B1.**
   - `scheme_current.jsonl`: the parents' placements are superseded by the children's (13,432 placements and 7,786 placed themes change by the cut).
   - `multiplacement_log.jsonl`: the parents' bag records and rule 0 lines are superseded.
   - F-001's within-room grain claim, which counts kinds per theme, is recomputed.
   - Each third-order theme's member counts are recomputed, so its tier (rare at under two unlike rooms) is checked again; rooms per theme do not change.
   - `confusions.md` rates are recomputed where they count parents.

   Not reopened: the codes themselves (episodes and exemplars cite concept ids, which stay), the third-order scheme's sentences, and the rooms' notes.
5. **What it changes in B2.** `author_items.jsonl` stays as written. The children are appended as new lines (source "recut", with their parent), and the parents leave the hard set from round 3, so round 3's set is not round 2's on those items. Round 3's comparison with round 2 is reported on the 40 unchanged round-1 items. J may also prefer that round 3 keeps the parents beside the children, for one round's comparison.

**Fleet ids.** Round 3 is the first round with fleet ids. `out/_analysis/b2_packets_fleet.py` builds the packets: room name plus `T2-` theme ids and `C` concept ids; no room id in an id position; J's caps of 15 items and 180,000 bytes. A dry run on the current hard set (seed 20261013) gives five packets of 7 to 13 items. `out/_analysis/b2_translate_fleet.py` translates returns back before scoring and reports every id the table lacks, or that belongs to another room or theme. RETURN-B2.md now asks for fleet ids, and it carries J's floor: a theme enters `also_present` only with at least three concepts of its own. Its round-2 text is kept as `out/_analysis/RETURN-B2_round2.md`. B3's specification does not exist yet; the head carries both rules for it.

Two points for J:
- `validate.py` checks returns against room ids in `_fleet_raw`, so a fleet-id round will fail its concept check unless the check reads the translated copies (`out/_analysis/b2_r<K>_returns/`) or the table.
- No round-3 packet is built until J's word on the recut.
