# Audit, section 1, part 5: the diary, the probes and the unplaced (E1b-05)

Written at E1b-05, 27 October 2026. This part covers three items of stage E1 section 1: the diary against the transcript, the recall probes (whose full tables are in `probes-E1.md`), and the unplaced, read. The new scripts are `diary_tool_lines.py`, `probes_notes.py` and `unplaced_kinds.py`. E1a's `diary_transcript.py`, `probes_score.py` and `unplaced.py` are read here.

## 1. The diary against the transcript

`diary_transcript.py` (E1a) drew 17 legs by seed (`cd472a6087a223d4`): one per stage, and one more among the extra legs D6a-09 to D6a-18. They are A1b-16, B1b-30-p2, B2b-r1, B3a-p2, B4a-05, C1a-07, C2a-02, C3a, C4a, C5c-02-p2, D1a, D2a, D3a-15, D4a-03, D5a-31, D6a-10 and D6a-17. Every drawn leg has its transcript.

Of their 905 diary lines, 392 are found word for word in the leg's transcript. The other 513 are lines a tool writes from its own arguments ("placed", "opened", moves, asks, adjudication notes), so their words are not the command typed. Each was read against the tool calls of its leg:

| how it is borne out | lines |
|---|---|
| a tool call or output within ten minutes holds the line's ids (`diary_tool_lines.py`) | 185 |
| a row of the files that B1b-30-p2's `b1_multiplace_write4.py` runs read (`b1_multiplace_b1b30.tsv`, `b1_multiplace_b1b30p2.tsv`) | 282 |
| a single placement in that leg's `b1_place.py` commands (`<sub> t07=T3-043` and the like), all 19 matched | 19 |
| the 27 move lines of C5c-02-p2, written in 41 seconds by `c5c2_decl_amend.py` from `c5c2_decl_spec.json`, both written and dry-run in the transcript a minute before | 27 |

**All 905 diary lines are borne out by the transcript, and no entry is a defect.** The loosest test is the one for the 282 TSV rows. It shows each row in a file the leg's script read, not a time-matched call for each line.

## 2. The recall probes

`probes-E1.md` holds the tables. The figures:
- **300 answer files.** As filed, `probe.py` could not read 283 of them, which are written in bold markdown, so goal is right 17 times and missing 283 times.
- **Re-read** by `probe.py`'s own rules against the expected values stored at each close:
  - goal: right 298, wrong 2;
  - open: right 26, wrong 135;
  - rooms: right 48, wrong 125;
  - changed: right 50, wrong 13;
  - next: right 11, wrong 12.
- **n/a**: 780 answers, apart and never counted as recall.
- **The wrong answers**: 269 are notes, because the head, the diary or the question files held the answer at the close. **18 are defects**, because none did: the rooms of 13 B1 legs and one D5 leg, and the changed ids of D4a-06, D4a-07, D4a-08 and D6a-01.
- **A second count for rooms.** The declared test read rooms in the leg's own diary lines, and gave 101 defects on rooms. But the harness's expected rooms are the last three on record, which repeat across legs that opened none. Read over the stage's diary up to the close, 14 of those remain defects. Both counts are on file.

## 3. The unplaced, read

| what | count | what each was |
|---|---|---|
| second-order themes with no placement | 151 of 7,844, holding 407 concepts | the sub's own April Fools play 42 (165 concepts); talk about the event with no organizing act, such as asking what an effort is, admiring, reacting or arguing about the canvas, 72 (186); lost posts whose body is gone, or of which only a title or marker is left, 18 (24, all of them in `unplaced-B1.jsonl`); labels that name an act, 19 (32) |
| concepts unreachable from any theme | 0 | every concept has its theme |
| third-order themes no fourth-order theme took | 2 | T3-017, "carrying on ordinary sub talk" (334 themes placed), outside the model's scope by design (rule G59 at D3a-55); T3-133, "recovering a hacked sub" (1 theme, rare tier), a host sub's act that could have sat with Boundary work |
| fourth-order themes no dimension gathered | 0 | |

The kinds come from a keyword rule declared in `unplaced_kinds.py` and were then read.

**Whether any should have been a member.** Of the 19 labels that name an act, 10 name one the scheme holds, and they should have been placed:
- germany/t19, a build report;
- h3h3productions/t27, welcoming people into the drawing;
- h3h3productions/t30, arguing over duplicate logo proposals;
- hungary/t05, a call to turn a neighbour's flag;
- linux/t03, writing a bot;
- oman/t06, telling a late helper the work was done;
- opticgaming/t12, mourning the lost work;
- orderofthebluecorner/t02, planning the sign;
- rainbowgrid/t06, taking the grid to other canvases;
- romania/t18, the flag's design.

Six of the ten hold one concept each. The other nine of the 19 are jokes, ordinary sub talk or a bare message. The other 132 unplaced themes are rightly outside: play, talk about the event, or posts with nothing left to read.

## 4. Defects named at this leg

Two lines were appended to `defects.jsonl` (lines 115 and 116, stage E1, leg E1b-05), both the instrument's:
- the 18 probe misses that no record answered;
- the 10 unplaced themes that should have been placed (sure false, a reading of short labels).

No earlier file is changed.

## What this part cannot say

- Whether each of the 282 TSV-borne diary lines was written at the moment of its row's run. The check matches the row, not the second.
- Whether the 10 themes would change any count of the model. Each holds one to five concepts, and none was placed.
