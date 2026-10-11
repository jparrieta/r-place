# Analyst-made B1 tools: candidates for a future instrument upgrade

Tag: [future instrument upgrade]. Logged 2026-10-08 on J's request (13:00 Berlin: "please log this tool the analyst made. tag for future instrument upgrade"). Copies of claude-v43-1's out/_analysis/b1_*.py as of 11:00Z, so a later edit by the analyst does not lose this version. Nothing here is installed in the instrument.

## The one flagged

- `b1_check_bags.py` (built in B1b-12, 05:44Z): checks every concept id named in a bag record's why against the theme it is cited for, before the close. It caught wrong citations that the close check missed (B1b-11 had four fixed after writing). Candidate: a mem.py verb or a check in tools/checks/stage_B1.py.

## Also worth a look

- `b1_room.py`: prints one room whole for B1 reading (header, theme note, every concept). The analyst reads every room through it; from B1b-13 it writes the print to a temp file and reads it in parts. Candidate: a mem.py verb (`mem.py room <sub>`), so reading depth can be measured from one known command.
- `b1_room_codes.py`: pages `mem.py codes --sub` past its hidden 80-line limit (open item). Candidate: fix the limit in mem.py instead.
- `b1_multiplace_write3.py`: writes rule 0 lines and bags from a TSV, with checks (third version). Candidate: a mem.py verb for rule 0 records.
- `b1_split_line.py`, `b1_tier_line.py`: append tier_history lines for splits and moves. Candidate: mem.py verbs, so tier history is never hand-written.

## All copied tools (sha256 first 12, first docstring line)

| file | sha256 | what it does |
|---|---|---|
| `b1_check_bags.py` | `6c1b940e8fb2` | Check every concept id named in a leg's bag records (multiplacement_log.jsonl, item_is_a_bag) |
| `b1_episode_writers.py` | `5b185043b24f` | For episode lines first..last (by number), say whether each line's evidence names a member writing |
| `b1_grep_rooms.py` | `710a33797450` | Concepts matching a regular expression (case-blind) in each of several rooms, read from each |
| `b1_kind_rooms.py` | `584b7a846c43` | For each named third-order theme, print its label, the number of second-order themes and of rooms |
| `b1_leg_figures.py` | `4605d37d8f3b` | Figures for one B1 leg's stretch-end line: rooms placed, second-order themes placed, |
| `b1_listing_pages.py` | `facc35b88688` | For each room-name search, the number of rooms `mem.py codes --grep <re> --by-room` lists, and |
| `b1_multiplace_write.py` | `0fd7604536da` | Rule 0 record for B1: check a TSV of second placements against scheme_current.jsonl, verify that |
| `b1_multiplace_write2.py` | `1fa4a029bd68` | Rule 0 record for B1, from leg B1b-02 on (supersedes b1_multiplace_write.py, whose bag text and |
| `b1_multiplace_write3.py` | `3b1e688cab79` | Rule 0 record for B1, from the T3-010 split in B1b-06 on (supersedes b1_multiplace_write2.py, which |
| `b1_place.py` | `6b9d6a39a728` | Place a room's second-order themes through mem.py place, in the order given (the verb writes |
| `b1_room.py` | `ced402c8fcfd` | Print one room's second-order themes for B1 reading: header, theme note and every concept |
| `b1_room_codes.py` | `8b7912e6a918` | Print every concept of a room, paging mem.py codes --sub past its 80-line limit. |
| `b1_room_placements.py` | `c3eb2a412d66` | Print each second-order theme of the named rooms with the third-order themes it is placed in, |
| `b1_scheme_figures.py` | `192c6b6b21df` | Scheme-wide figures for a close: themes, placed second-order themes, placements, size |
| `b1_shared_authors.py` | `cfeadde35298` | Writers who appear in two concept dumps (from b1_room_codes.py or mem.py codes), with the |
| `b1_shared_many.py` | `e5d703b4ff37` | Writers shared between one room's concept dump and each of several others, with the hours |
| `b1_show_codes.py` | `958a49fdfeda` | Print chosen concepts of a room (id, theme, hour, writer, label), read from its full concept |
| `b1_split_line.py` | `7449e6f05f13` | Append one tier_history.jsonl line for a split of an existing third-order theme into itself and |
| `b1_stretch_placed.py` | `ab38379c52d7` | Second-order themes placed, placements and unplaced lines for a stretch of the B1 order, |
| `b1_stretch_sizes.py` | `745aad1707b0` | Sizes of the next rooms in the B1 order (codes plus second-order themes, not the forest), |
| `b1_stretch_themes.py` | `d4177ff16248` | Codes and second-order themes per room for a stretch of the B1 order, with totals. |
| `b1_theme_members.py` | `d0ff0d2b2f7f` | Print every member of a third-order theme with its second-order theme note and concept labels, |
| `b1_tier_line.py` | `f80d8c05e875` | Append one tier_history.jsonl line for a move that took second-order themes out of an existing |
- `b1_dump_rooms.py` (B1b-15): dumps several rooms' concepts to compare one large room with many partners (added after the first copy).
- `b1_bags_from_file.py` (B1b-17): runs b1_multiplace_write3.py with one --bag per line of a bag file.
- `b1_episode_read_check.py` (B1b-17): lists episode lines naming a room that is unread or outside the order.
- `b1_episode_theme_check.py` (B1b-17): for a range of episode lines, reports listed themes no listed room holds. Found 108 such kinds on 81 of E001-E418.
- `b1_print_sizes.py` (B1b-17): b1_room.py print size per room for an order range, to note rooms read in parts.
- `b1_label_grep.py` (B1b-18): prints every placed second-order theme whose label matches a regex, with its third-order themes.
- `b1_bag_lists.py` (B1b-19-p2): Print the latest bag record of each sub:tNN as 'sub:tNN:kept:would_need (leg)'. Read-only.
- `b1_kind_labels.py` (B1b-19-p2): Print each member of the named third-order themes as one line: sub, theme id, second-order label,
- `b1_kind_overview.py` (B1b-19-p2): For each third-order theme named, print its members' count, rooms, and how often its members
- `b1_member_status.py` (B1b-19-p2): For each sub:tNN given, print its current kinds (scheme_current.jsonl), whether a bag record exists
- `b1_precheck_bagfile.py` (B1b-19-p2): Before writing, check every concept id cited in a bag file's why against the second-order theme
- `b1_review_tier_lines.py` (B1b-19-p2): Append tier_history.jsonl lines for one review of an oversized kind, read after the moves: the
- `b1_split_print.py` (B1b-19-p2): Cut a member print (b1_theme_members.py output) into part files under a byte limit, breaking
- `b1_both_acts.py` (B1b-20): List second-order themes whose label names both acts of a kind pair (two regexes) but which are
- `b1_members_changed_lines.py` (B1b-20): Append members_changed lines to tier_history.jsonl for a review that changed members of existing
- `b1_members_changed_lines2.py` (B1b-20): Append members_changed lines to tier_history.jsonl for a review that changed members of existing
- `b1_episode_join.py` (B1b-21): Add a joining room to existing episode lines, as the B1 walk records it: the room appended to
- b1_split_spec.py (B1b-23): applies several episode joins one at a time, since b1_episode_join.py keeps only the last entry when several rooms join one episode in a run.
- b1_shared_counts.py (B1b-26): counts members shared between rooms (for episode joins).
- b1_shared_detail.py (B1b-27): prints the codes of members who write in two rooms, sorted by hour.
- b1_multiplace_write4.py, b1_bags_from_file2.py (B1b-29, 41c76ff5): rule 0 and bag writes check only rows not yet in the log, one mem.py codes call per room; write3 called mem.py once per row of the leg's whole table and grew from 0.1 to 8.5 min a run within a leg. Written after J's word (2026-10-10 22:09 Berlin).
- b1c_sample.py (B1c, f8945bbb): seeded B1c sample draw / fresh-against-record totals.
- b1c_totals.py (B1c, f8945bbb): seeded B1c sample draw / fresh-against-record totals.
- b1d_hesitations.py (B1d-01, fb906885): second-pass helper.
- b1d_stretch_sizes.py (B1d-01, fb906885): second-pass helper.
- b1d_tier_rescope.py (B1d-01, fb906885): second-pass helper.
- b1d_forest_lengths.py (B1d-03, 62fa293e): second-pass helper.
- b1d_tier_unplace_fill.py (B1d-06, 690943a6): second-pass helper.
