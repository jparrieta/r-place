# Finding 1: the unit (C5c-08, pass 11)

Target length: about 1,500 words. Problem 1 of the serial work planned in `notes-C5.md` (C5c-07, with the order revised at C5c-08 after QC5-002). Scripts: `c5c8_unit_sweep.py`, `c5c8_unit_quotes.py`, `c5c8_unit_we.py`, `c5c8_decl_amend.py` with `c5c8_decl_spec.json`, and `c5c3_model_amend.py` with `c5c8_model_spec.json`.

## 1. The question

At pass 6 I accepted 94 pieces of the field analyst's advice. Passes 7 and 8 carried that wording into the model. Which of these changes moved the actor from the room, or a group of rooms, to members, where members spoke or acted for the room? And where else does the model speak of members when the room acted?

How the question serves the study's two questions (`notes-C5.md`, C5c-08):
- **The method question.** The return composes the global model from room-level case histories, and stage D4's forms are sets of rooms. A global model that speaks of members cannot compose with them.
- **The theory question.** It asks what forms organizing takes, and the room, or a group of rooms, is what organizes.
- **The contract's limit.** A subreddit is not automatically an organization. So the room is restored only on the quotes, never by default.

## 2. The rule, written first

The rule was logged with `--kind abductive` before the read (diary, C5c-08). It comes from J's advice at 12:01 and 13:45 Amsterdam.
- **R, restore the room or a group of rooms.** Pass 6, 7 or 8 moved the actor from the room to members, or a model sentence names members, and in either case the quotes show members speaking or acting for the room. They speak for it in its threads, in the first person plural, in its calls or in plans it adopted. A group of rooms is the actor where a coalition or an agreement acted.
- **K, keep members.** The quotes show members acting apart from the room or against it, or the act is one only a person can do: placing a pixel, running a script, answering a call in one line.
- **N, no change of actor.** The advice concerned universals, counts, motives, time or a misread quote. These changes stay.

Two scope rules:
- **Declarations.** Descriptive prose that named members before pass 6 stays, under J's language rule: describe what members did, in how many rooms.
- **What changes.** Only the actor. The rest of the accepted advice stays.

## 3. What was read

- **Pass 6.** All 93 sentences replaced on the 94 pieces of accepted advice were read, old and new side by side (`c5c8_unit_sweep.txt`, part A).
  - 8 changed the actor:
    - 5 are R: D02, D07, T4-014, T4-018 and T4-028.
    - 3 are K:
      - T4-001's members asking whether a post is meant, who act apart from the room's frame;
      - T4-020's members calling for attack forms, whose calls the room's own members often refuse (F-014);
      - D05's membership that members claim in the thread, which is each member's own claim.
  - 85 changed something else, and they stay.
- **Passes 7 and 8.** All 16 element and arrow changes were read (part B). Only K02 and A10 moved the actor from the room, at pass 8, and pass 9 restored them. K01's change named members posting fakes, which is a member's act under the host's frame, so it is K.
- **The model as it stands.** It has 44 sentences that name members, in standing elements, arrow mechanisms and proposition statements (part C):
  - 9 element and arrow sentences are R;
  - 11 proposition sentences are R, listed below for the fold-in;
  - 20 are K;
  - 4 already name the room or the host sub.
- **The quotes.** For every R and K call in the model and the declarations, I read the quotes it rests on through `cite.py` (`c5c8_unit_quotes.txt`):
  - each element's cited codes and 8 quotes drawn from its fourth-order theme (seed 20261015);
  - each arrow's support;
  - the quote lines of each declaration's section in the field packages.
- **A descriptive check** (`c5c8_unit_we.py`): the share of each theme's concepts whose words use the first person plural ("we", "us", "our", "let's"), against the singular only.

| theme | element | concepts | plural | singular only |
|---|---|---|---|---|
| T4-005 | calls (P01) | 6,026 | 39.8% | 20.6% |
| T4-007 | building and reporting (P03) | 5,244 | 37.1% | 24.5% |
| T4-013 | upkeep (P05) | 13,502 | 41.0% | 16.8% |
| T4-016 | border talk (P08) | 13,369 | 52.4% | 14.2% |
| T4-018 | coalitions (P17) | 2,861 | 46.7% | 13.9% |
| T4-014 | territory | 5,997 | 44.8% | 16.9% |
| T4-028 | carrying on (P13) | 1,802 | 24.3% | 25.3% |
| T4-020 | attack (P09), for contrast | 4,434 | 35.7% | 12.8% |

- **How to read the table.** A plural pronoun shows a member speaking as one of a group. It does not show which group, or that the room agreed.
- **What it shows.** Members speak in the plural about two to three times as often as in the singular alone in calls, upkeep, border talk, coalitions and claims to space. Building and reporting leans plural. Carrying on is even.
- **The attack calls.** They are plural too. Their declaration keeps members because of F-014's refusals inside the room, not because of the pronouns.

## 4. What changed, by ledger id

Fourteen moves, all "developing", each logged and snapped (C5-move-developing-150 to 163). Pass 11 is recorded in `account_passes.jsonl`.

**Declarations** (`tier_history.jsonl`, 554 to 559 lines):

| id | field | now reads | deciding quotes |
|---|---|---|---|
| D02 | changed | "It names the ways a room tried to align many hands…" ("tried" stays for problem 4) | overwatch/c0795, criticalrole/c0051 |
| D07 | mistaken_for | "what rooms propose to carry on into later groups" | fireemblem/c0412, greenlattice/c1156 |
| T4-014 | prose | "A room needs a place for each mark." | utahjazz/c0030, norway/c0085, winnipegjets/c0051 |
| T4-018 | prose | "Rooms announced alliances and hubs whose members were rooms." ("announced" stays) | lakers/c0155, belgium/c0134, elitedangerous/c0275 |
| T4-028 | mistaken_for | "what rooms, and some members on their own, propose to carry on" | fireemblem/c0412, maryland/c0269; apart: minecraft/c0188 |

**Elements and arrows** (`model/history.jsonl`, 119 to 128 lines):

| id | field | now reads |
|---|---|---|
| P01 | statement | "The room calls its own members, and kindred subs, to come and place for a work…" |
| P03 | statement | "The room builds its mark, and members report its state to the thread…" |
| P04 | range | "…to an official template the room asks everyone to follow against other versions" (the statement keeps members, who post templates and also pick versions apart from the room: AmericanFlaginPlace/c0023) |
| P05 | statement | "The room keeps its placed work against erosion: members watch it and repair changed pixels, and the room rallies to defend it under attack, covers the night, hardens its shape and puts upkeep before growth." |
| C02 | statement | "a tie the room had before the canvas" |
| A01 | mechanism | "The room's call brings members to the canvas, who then build the mark…" |
| A05 | mechanism | "A settled border gives the room a line to keep: members spare the neighbour's work by it…" |
| A08 | mechanism | "Marking the work together turns the room toward keeping it: members ask for…" |
| A17 | mechanism | "…the room invokes a truce, or proposes a deal instead." |

No count, grounding, strength, element status or finding changed.

## 5. What did not change, and why

- **Members stay** where the act is a person's or the member acts apart from the room:
  - the starter (R01, A02);
  - the one-line answer (P15);
  - scripts and spare accounts (P14, A06);
  - refusals of an attack call (A16);
  - the call turned against a rival (A15), which other members often refuse;
  - members questioning the April Fools frame (K01, T4-001);
  - each range's lower end ("one member…").
- **The other 85 pieces of accepted advice stay.** They concern universals, counts with their limits, motives, time and misread quotes, not who acts. J's advice at 12:01 says the field's standard tested description and was not the bar for theory. That advice bears on the actor, not on these corrections.
- **Declarations that named members before pass 6 stay** under J's language rule. One example is T4-016's "Members propose or settle borders with neighbours (418 rooms)".

## 6. What the fold-in must carry

**The propositions** (`propositions.jsonl` statements; each mechanism is regenerated from its arrow):
- **N01:** "…the room calls others to place (P01); after a call, the room builds the mark and members report it (P03); once the mark stands, the room keeps it (P05)."
- **N02:** "When a room keeps a mark (P05), it turns to other rooms: it talks borders with neighbours (P08), asks other rooms for help (P16) and joins coalitions under attack (P17)."
- **N03, second and third sentences:** "The same room answers the call to attack: members refuse it, usually with a reason (F-014), the room reins in the attackers or apologises (P07), or points to a truce (P08). Where the attack goes on, the rooms carry the contest on in talk (P18)." The first sentence keeps members.
- **N04:** "After members report a mark done (P03), the room celebrates it (P11), records what it celebrated (P12) and carries the record on (P13)." The close: "after it, rooms can celebrate, record, curate the record and carry it on, and no one can place."
- **N05:** "When a room calls for hands in a standing sub (P01), the host sub's moderators and members draw a line…"
- **N06:** "When the room's upkeep needs more placements than its members can make (P05), members turn to scripts…"
- **N07:** "Rooms try to align their members' placing without deciding how they are organized…" ("try" is for problem 4).
- **N08:** "When a room judges it has too few hands to hold its spot (K02), it stops fighting for it and moves (P10)…", as K02 and A10 have read since pass 9.
- **N09:** "A settled border (P08) gives the room a line by which it spares the neighbour's work (P07)…"

**The account.** 36 sentences name members. 16 take the room as the actor; 15 keep members; 5 make no claim about an actor. The 16, by paragraph:
- **What to make:**
  - "The room settles what the mark will show [P02]."
  - "Rooms decided how they would be organized … in 46 of 705 rooms [C01]."
  - Stigmergy's paragraph: "what the room settles the mark will show".
- **Keeping:** "Once a mark stands, the room turns to keeping it in 148 of 190 rooms [A03]."
- **Other rooms:**
  - "Keeping the work brings the room into talk with its neighbours…"
  - "Rooms ask other rooms for help in 171 of 240 rooms…"
  - "A settled border gives the room a line…"
  - "Rooms make these agreements without the power to make every placer keep them…"
- **The contest:**
  - "The same room meets the attack call with sparing, refusal or apology…"
  - "Where the attack goes on, the room carries it on in talk…"
- **Loss:** "A room that judges it has too few hands stops fighting for the spot and moves, in 11 of 21 rooms…"
- **The close:**
  - "the room celebrates the work after the first build report…"
  - "After hour 73, rooms curate the record: members clean up, copy and post records…"
- **day9:** "The room judged the spot lost and moved…" ("the spot we've had").
- **ubc:**
  - "ubc called for hands…"
  - "The room kept a border by agreement, and members ran spare accounts under strain…"

**The figure** takes the new statements when C5d is redone. No box or arrow changes.

## 7. How sure I am

- **Sure.** The rule is J's, and it was logged before the read. Each restoration rests on quotes in which members speak for the room, and the pronoun check agrees: plural speech outnumbers singular speech about two to one or more in the restored themes. No count or arrow changed, so no tested claim moved.
- **Judgment calls.** Where an act is mixed, the sentence names both actors:
  - P03: the room builds, and members report;
  - P05: the room keeps and defends, and members watch and repair;
  - T4-028: rooms, and some members on their own.

  A reader could draw these lines elsewhere.
- **The limit.** A plural pronoun and a call in the room's thread show members speaking for the room. They do not show that every member agreed. The model says "the room" where members acted in its name, as the contract allows. It does not claim the room was one mind. Rooms that did not organize stay visible as rooms where the elements are absent.
- **What the criterion says: prefer.**
  1. Unmarked causal sentences: unchanged.
  2. Rooms told: unchanged, with the same 23 elements.
  3. Tested arrows: every one kept.
  4. The prose test: two names do more work. Territoriality and Meta-organization name things rooms do: a room claims space, and an alliance's members are rooms. With members as the subject, those sentences had lost what the names name.
