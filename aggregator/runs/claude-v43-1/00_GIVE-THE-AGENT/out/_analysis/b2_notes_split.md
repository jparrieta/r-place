
### QB2-010: the bags split (J approved, 2026-10-12 09:32 Berlin)

J approved the cut as proposed, at medium effort. The handler installed `mem.py split`. It writes `out/recut/themes.jsonl` and `out/recut/codes.jsonl` beside the read-only store and gives each child the room's next free tNN and a fleet id in `out/fleet_ids.jsonl`. The parent is superseded, never deleted. Each child names me ("analyst") as its author and names the parent it supersedes.

**How the cut was made.** I read every bag whole in one blind window (`mem.py blind on`, closed at 07:49:15), with B1's placements hidden. I grouped each bag's concepts into children by what the concepts do; each child has at least three concepts, and every concept is in one child. Each cut is written in `out/_analysis/b2_split_<sub>_<tNN>.txt` and was run by `out/_analysis/b2_split_run.py`. The helper checks coverage and the three-concept floor against the store before it calls `mem.py split`.

`mem.py theme` printed some concept lines blank (c0084, c0505, c0595 and c0960 of 2007scape t04, for example). I read the bags with `mem.py codes --sub S --second tNN`, and the helper's coverage check named every concept I had not yet assigned. Each one was read and assigned.

**The six hard-set bags became 54 children.** The next table lists each bag with its children and their sizes.

| bag | children | the children (concepts) |
|---|---|---|
| 2007scape t04 (349) | t15 to t28 | proposing what to make 48; the design's spot, size and look 20; building and reporting 85; coordinates and references 12; fixing misplaced pixels 22; defending the corner 11; covering others' art 13; refusing to give up the corner 6; dealing with neighbours 35; Trump politics with r/The_Donald 13; pride in working together 35; the flood of r/place posts 7; jokes and asides 38; pushing posts up 4 |
| sweden t01 (310) | t08 to t17 | building, cleaning and holding the flag 54; defending it and calling out vandals 18; taking over the Danish flag and neighbours 28; Swedish emblems on the flag 44; other rooms asking for space 51; other rooms asking for help 22; settling with neighbours and letting art stay 31; Nordic friendship 9; looking back and the Maryland friendship 27; off-topic talk 26 |
| theblackvoid t12 (335) | t16 to t25 | hailing the Void and its creed 88; calling it to consume named targets 71; keeping and defending the cores 43; arguing what the true Void is 30; leaving other colours for the Void 11; other rooms dealing with the Void 15; critics and taunts 21; looking back after its end 10; jokes and asides 36; new cores elsewhere 10 |
| ainbowroad t03 (326) | t14 to t21 | alarms and fighting the Void 59; alarms about other attacks and collisions 70; calls to attack other rooms' work 22; war and peace with Blue and others 33; dealing with the Void 38; other rooms asking for help or to be spared 61; routing the road and proposing designs 30; hostility and insults against the road 13 |
| ainbowroad t04 (327) | t22 to t27 | repairing the road itself 103; repairing and protecting other rooms' art 74; deciding to spare and share space 38; other rooms asking to be spared or helped 96; defending the road 12; looking back 4 |
| ainbowroad t07 (311) | t28 to t33 | extending the road and planning its course 50; proposing pictures and features for it 156; other rooms asking for space on it 38; working beside neighbours without harming their art 39; the Gilbert Baker memorial 5; shards, takeovers and disputes over its spread 23 |

The hostility child of ainbowroad t03 holds "KILL THE GAYS" (c1395), posted to the room; it is kept and served as it stands.

**The gold set's eight B1 bags.** One was cut: dankmemes t16 (12 concepts) became t18, pointing out drawings on the canvas (5), and t19, reporting the build failed and mourning the canvas (7). Seven were not cut:
- cuboulder t04 and ukraine t07 hold 5 concepts each, so no two children of three exist.
- Villanova t01 (building a logo together), tinytardis t06 (negotiating shared space), edboxes t02 (recruiting hands and arranging the next shift) and alberta t04 (arguing whether to attack the Quebec flag) each read as one doing.
- finland t06 holds one doing of 5 concepts (moderators gathering the canvas posts) and three single concepts that each do something different; a second child would mix doings.

These small themes were B1 bags because nearly every concept did something different. With a floor of three concepts per child, they cannot be cut.

**The children placed.** I placed the 56 children like any item after the window closed (`out/_analysis/b2_author_split.py`). The 54 hard-set children were appended to `author_items.jsonl` and the 2 gold children to `gold_items.jsonl`. Each line carries its parent, source "split", `support_by_theme` and its fleet theme id. 40 children take one theme and 16 take two; each second theme has concepts of its own, named on the line. No child needs more than three themes, so none is a bag. The parents' lines stay as written. `author_items.jsonl` now has 104 lines and `gold_items.jsonl` 42. Round 3's hard set is the 44 unsplit items and the 54 children: 98 items.

**The rechecks.** The children sit on themes that earlier edits changed, so 86 edits owed them 526 rechecks. I read each edit's changed sentence against the children it owes (`out/_analysis/b2_rechecks_split_show.txt`), and none moves a child. The closest call is ainbowroad t24's second theme, T3-010: three of its five concepts invoke agreements already made, which T3-195 names. It stays, because the trimming to the agreed size is itself the border being settled. The 526 records were written with `out/_analysis/b2_rechecks_split.py`, one reason per edit. `rechecks-B2.jsonl` has 1,413 records, and none is owed.

**What the split leaves for the check (QB2-011).** `validate.py B2` reports 698 errors in five shapes. All come from the split layer meeting records made before it:
- 56 items not in `package/store/themes.jsonl`: the item check reads the store, not the split layer.
- 186 round-2 return lines and 454 rechecks whose concepts now resolve to the children, not the parents they name.
- `pilot_rounds.jsonl` lines 1 and 2: n_items 40 and 50 against a hard set counted as 104, the parents included.

QB2-011 asks J whether the check should read the split layer for items, keep a parent's own concepts for records that name the parent, and count the hard set without the superseded parents. Meanwhile the leg stays open. No round-3 packet is built. The 846 B1 bags wait for J's word.
