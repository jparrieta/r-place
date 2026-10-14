# Notes, stage C2 (the loop)

## The criterion, written before pass 1 (section 1)

I will prefer a later pass to an earlier one only when four things hold together. First, the later story tells more of the rooms drawn against it in their own terms: fewer `told-with-residue` and `not-told` verdicts among rooms drawn by a rule written before any room is opened, the three within-case rooms and one room from each size quartile among them, with no element loosened to make a room fit. Second, more of its in-model arrows rest on an instance a reader can be shown (a participant's words through `cite.py`, or two coded turns in one thread in order), each with `mechanism_fails_if` written before its strength and each sampled against rooms outside its own where it could fail. Third, its tiers stay a step up in abstraction: no fourth-order theme or dimension that renames its members, and every dimension answers a question none of its members answers alone. Fourth, it reaches the contract's four things (how a scattered readership becomes able to act, how it settles what to act on, what sends it back to the beginning, what it leaves behind) with an element for each or a stated absence. A pass that adds elements or arrows without improving the first two is not preferred, however much it explains on paper. A pass in which `told-with-residue` rises is a stopping failure, and its residues are the next pass's material. A tie goes to the earlier pass, so the loop does not ratchet. Every pass is numbered and every version kept (`structure.md` then `structure-p2.md`, `model.md` then `model-p2.md`, `model/story-pN.md`); the last pass says which one the model rests on. The stopping rule is contract section 6's guide: two consecutive passes with no `tier_history` event, no arrow added, bounded, demoted or withdrawn, and no story sentence naming an arrow or element changed.

## Pass 1 (C2a-01)

### Before the pass

- **Read:** `METHOD.md` whole; the read tier (Gioia, Corley and Hamilton whole); the contract's section 1; `prior.md`; `contrast.md`. The explanation literature stays shut until C3.
- **The ledger** (`mem.py pairs`, third, fourth and second level). 62,838 coded turns answer coded turns. Most stay inside one theme. Across fourth-order themes, the rooms with a transition run, for example, Completion ritual then Repair work (274), Repair work then Negotiated order (264), Mobilization then Repair work (195), Mobilization then Collective representation (155), Collective representation then Stigmergy (146), Mobilization then Stigmergy (127). The ledger is elapsed order: "a reply is a reply: posted after, not caused by". It is never, on its own, an arrow.
- **What the handler's interview carried in** (a fork; nothing from it reached the run). My own words there, set beside the stage file here: decided order looked rare and mostly real; `also_present` read as a second layer, never pooled; FP-04 and FP-08 as conditions, never weights; where to start the model: the spine from calls to emblem, trace and template, then repair, then the close, ordered by the clock and grounded in cited concepts, then the hinge from attribution to restraint or contention; test T3-076 first among the forced placements, then T3-141 with FP-03. I take these as working hypotheses to test, not as findings.

### The three within-case rooms, named before any was read (section 4)

They were drawn by `out/_analysis/c2_within_case_pick.py`. All three come from the middle half of rooms by `items_in_window` (156 to 2,770, the held-size band of `contrast.md`, 353 rooms), so size does not pick them, and each was drawn with `random.Random(20261014)` from its candidate list.
- **The ordinary room: ubc.** Rule: its placements reach all four of the most widely reached fourth-order themes (Repair work, Completion ritual, Mobilization, Collective representation), and its organizing end (stage A1) lies inside the corpus's interquartile range, h68.70 to h72.93. 53 candidates. ubc has 1,475 items and 45 coordinating turns, and its organizing ends at h72.75.
- **The room whose form the scheme could not have predicted: ultrahardcore.** Rule: the share of its placed lines carrying a third-order theme placed in fewer than ten rooms is in the top tenth of the band. Such a room's form rests on kinds the scheme holds only thinly. 36 candidates. ultrahardcore has 918 items; 2 of its 10 placed lines carry such a theme.
- **The room that stopped early: day9.** The first rule (organizing end before hour 24, with five coordinating turns or more) found no room in the band. I restated it before any room was read: an organizing end in the lowest tenth of all 705 rooms (at or before h58.79), with five coordinating turns or more. 14 candidates. day9 has 361 items and 23 coordinating turns, and its organizing ends at h53.28.

I read each through `mem.py` with placements hidden (`--blind`), from its concepts, forest and timeline, and write them with no theme above the second tier.

### Part A, pass 1: the tiers

- **The fourth-order tier: 28 themes, no recut at pass 1.** The material carries 28 because each answers a question its members do not answer alone, and none renames its members (stage C1, pass 10; `fourth/fourth.md`). At this pass each line gained `changed`, `mistaken_for`, `in_model` and `pass`, with the old line kept as `was` in `tier_history.jsonl` (28 lines). 17 are in the model and 11 are not. The forced placements are tested against rooms before any recut. Pass 1's story rooms point to two places a recut may come: attack as a room's own work, and exchange between rooms (below).
- **Seven dimensions**, cut one at a time with their pairwise separation (7 `tier_history` lines; snaps C2-move-*-1 to 7, each named merging or relating): D01 Critical mass, D02 Coordination without command, D03 Maintenance, D04 Order without law, D05 Collective identity, D06 Host framing, D07 Imprinting. Five are adapted, two coined. Each gathers two fourth-order themes or more and answers a question none answers alone. Seven, because the four things and the material split there: the hands, their alignment, the keeping of the work, the order between rooms, the membership carried in, the host's frame, and what is left.
- **Part A's return** is at the head of `structure.md`. Third-order themes per fourth-order theme and fourth-order themes per dimension are in its first table. The two dimensions I am least sure of are Maintenance and Host framing (two members each). The rejected alternative is a separate contention dimension, now open as `_questions/contention-dimension.md`. 72 of 72 coder conflicts reached `structure.md`. The fourth-order theme I am least sure of is Stigmergy.
- **Consistency, computed** (`structure.md`): every third-order theme placed in `assignments_final.jsonl` is defined in `scheme_v2.jsonl` (194 placed, 197 defined). Each sits in a fourth-order theme's members or in the unpicked list (T3-017, T3-133). Every fourth-order theme sits in a dimension's members (28 of 28). Every dimension used is defined. The three counts sum to 705 for every third-order theme, under the opportunity gates declared before counting.

### The onset contrast, pass 1 verdict

The next table repeats the shares that decide stage A1's expectations at held size (`items_in_window` 156 to 2,770). The late side has 12 rooms at held size, so every late share is thin.

| what | held early (n=41) | held late (n=12) |
|---|---|---|
| choosing a canvas spot | 0.22 | 0.33 |
| asking a host for space | 0.05 | 0.08 |
| relocating after losing the spot | 0.20 | 0.00 |
| extending the room's work | 0.27 | 0.25 |
| defending the work against attackers | 0.66 | 0.42 |
| calling to deface rivals' work | 0.41 | 0.08 |
| trading taunts with rivals | 0.15 | 0.08 |
| Host framing (dimension) | 0.83 | 0.25 |

- **First expectation** (late rooms organize around finding room; early rooms around claiming, enlarging and holding): it held in part. Late rooms choose a spot more often. Asking a host for space is rare on both sides. The extension gap vanishes at held size, but the defence gap stays. Relocation runs against the expectation: early rooms move, and no held late room does.
- **Third expectation** (early rooms name rivals and keep fights going; most of this was expected to vanish at held size): it did not vanish. Calls to deface rivals' work stay at 0.41 against 0.08, and taunts at 0.15 against 0.08.
- **Host framing** (0.83 against 0.25) differs largely by construction. Late rooms first wrote after hour 48, when the April Fools frame was over.
- **On the arrows:** the late side holds A04 in 6 of 15 rooms (talk with neighbours before upkeep, a bound) and A08 in 8 of 15. A06 and A09 have three late rooms each, too few to read.

### Part B, pass 1

`concept.md`: the one-line enrolment (FP-01), chosen provisionally. It is in the model as P15 and arrow A12, never counted. Its nearest concept is slacktivism, which substitutes for action; the enrolment comes before action and is the room's head count. It appears in 337 of 705 communities under the form pass's declared gate, as a floor. The candidate I came closest to choosing instead is organizing without decided order (C01). The rejected candidates are kept in the file.

### Part C, pass 1: the model

- **20 elements:** 15 processes, 2 conditions, 1 claim, 2 roles. 17 are named for what they do. Why 20: the four things and the concept need 17 (`model.md`, "Why 20"). Three more (attribution, attack, the envoy) carry the hinge the interview asked me to test; the hinge was not grounded, and the within-case rooms need the three elements.
- **12 arrows:** 10 order and 2 transition. 5 are strong, 3 fair, 4 thin. All are grounded `codes-read`, and each rests on quotes and a transition in one thread. 10 beat a permutation null (500 shuffles within each room, seed 20261014). A11's order is at chance, so it is kept as a transition. A12 is never counted. Connection statement: "in a room carrying both, the first concept of FROM comes before the first concept of TO".
- **Theorised arrows**, listed apart: A11 and A12. The thin arrows that beat the null are A05 and A10. `model.md` shows the model without each set.
- **Tested and not grounded** (`model.md`, "Looked for and not found"):
  - attribution before restraint (0.452 against 0.456) and before attack (0.194 against 0.408, reversed);
  - attack before repair (0.444 against a 95th percentile of 0.449) and before a move (0.561 against 0.610);
  - calls and building after a move, below chance (finding F-002);
  - doubt before calls (0.175 against 0.352, reversed);
  - machine hands before upkeep (0.202 against 0.375, reversed; replaced by A06).
- **No loop is grounded.** `model/loops.jsonl` is empty.
- **The relationship I most expected and could not ground:** attribution as the hinge between restraint and contention.
- **Findings at pass 1:** F-002 to F-006 (`findings.jsonl`). They were written late in the leg (see the slips).

### The story, pass 1, and the rooms read against it

`model/story-p1.md` names all 12 arrows in brackets (A01 to A12). The 20 rooms were drawn before any was opened, by the rule in the first line of `story_rooms-p1.jsonl` (`out/_analysis/c2_story_draw_p1.py`, seed 20261014). Each was read whole, room page then forest. The saturation line holds: told 0, told-with-residue 20, not-told 0.

The story's spine shows in every room. No room needed a recut to be told in part. Every room also did something the story does not tell. The residues cluster as follows; they are pass 2's material:
- **Help and exchange between rooms** (9 rooms): ubc, xenoblade_chronicles, catalunya, texans, sweden, ripcity, MiamiHurricanes, yuyuyu, edmontonoilers. Help given, help received, space traded for repairs, a parent coalition's work kept, a host for others' marks. Reciprocity and Meta-organization are outside the model. Pass 2 should test one element of exchange.
- **Attack as a room's own work** (6 rooms): anarcho_capitalism, canucks, edmontonoilers, catalunya, sweden, unitedkingdom. P09 has no arrow, and the story tells attack only as something done to a room. Open in `_questions/contention-dimension.md`.
- **Calls renewed after a loss** (4 rooms): day9, texas, scp, worldoftanks. This is against the story's sentence that a move does not send a room back to recruiting. Open in `_questions/relocation-renewed-calls.md`. `model.md`'s relocation sentences are corrected in place; the story's sentence stands as read.
- **Border talk before any upkeep** (4 rooms): unitedkingdom, sweden, yuyuyu, worldoftanks, plus MiamiHurricanes as A04's bound.
- **The template arriving with the first call** (3 rooms): empiredidnothingwrong, texas, totallynotrobots (A11's bound).
- **The close marking an unfinished work** (2 rooms): ultrahardcore, totallynotrobots. The play frame also set what totallynotrobots made, not only when it started.
- **Membership carried in, and the host's policing of canvas talk** (3 rooms): unitedkingdom, texas, sweden.
- **Decided elements by vote or role** (4 rooms): edmontonoilers, sweden, ripcity, empiredidnothingwrong. This bounds C01 and F-006, which count placed themes.

**What the structure showed that my notes did not predict.** Exchange between rooms is the most frequent thing the story cannot tell: 9 of 20 rooms. Attack is often a room's first canvas act, not only something it suffers.

### The criterion, applied to pass 1

Pass 1 is the baseline:
- told-with-residue 20 of 20;
- 10 of 12 arrows beat a null, and 12 of 12 rest on an instance;
- the tiers are unchanged above the third order;
- each of the four things has elements, though "what sends a room back" rests on one thin arrow (A10) and a contested finding.

A later pass is preferred if it lowers told-with-residue on a fresh draw, without loosening any element. The stopping rule cannot stop at pass 1: 35 `tier_history` events, 12 arrows added, and a first story.

### Slips, pass 1

- An empty heredoc no-op ran before the compaction. It changed nothing, but it broke the head's rule against no-ops in a command.
- After the compaction, the first draft of `model.md` was written before the line "compacted; head reconciled" was logged. The guard then required the head and the stage file to be read again; reads with offset and limit did not register, and a plain read did. Every number in the draft was then checked against the evidence files. One was wrong: A08's late side holds in 8 of 15 rooms, not 7. A further error was found later: the draft cited F-001 for decided order, but F-001 is the stage B1 claim.
- The findings F-002 to F-005, cited by elements P10 to P14 and K02, were planned before the compaction and never written to `findings.jsonl`. They were written late in the leg, with F-006, and C01's evidence was corrected (`c2_findings_p1.py`; one history line; snap C2-move-relating-22).
- Errors found before compaction and fixed then:
  - in `within_case.md`, "182 of 212 concepts before h41" became "193 of its 212 coded items fall before h40";
  - the early-stop rule found 0 candidates and was restated before any room was read;
  - a leftover line was removed from `c2_dim_mass.py` before it ran.

### The close-check, pass 1

`python3 tools/validate.py C2`, run before the head was rewritten:

```
stage C2:
  1 pass(es) so far; a declared stop comes from the third pass on (stage C2 section 1)
  elements 20, arrows 12 (12 in the model), fourth-order themes 28, dimensions 7, passes 1, findings 6

0 errors (0 distinct shapes), 0 warnings
```

`done.sh C2` runs the same check at the close. Its report is in the leg's closing diary line.
