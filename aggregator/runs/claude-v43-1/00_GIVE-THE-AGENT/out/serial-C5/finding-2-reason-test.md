# Finding 2: the reason test (C5c-11, pass 14)

Target length: about 1,500 words. Problem 2 of the serial work, worked last in the revised order. It is framed as J asked: omission against commission. An acceptance can be done by placing without writing, and what is heard less may simply have survived less in the record. So I weigh survivor bias before reading the asymmetry.

Scripts: `c5c11_survival.py`, `c5c11_place_pairs.py` (with `c5c11_place_sample.json` and `c5c11_place_read.txt`), `c5c11_place_codes.json`, `c5c11_place_tally.py`, `c5c11_findings.py`, and `c5c3_model_amend.py` with `c5c11_model_spec.json`.

## 1. The question

F-014 found that in replies to attack calls, refusals gave a reason in 23 of 38 and acceptances in 2 of 14. The question has two parts:
- How much of that asymmetry is what members did, and how much is what the written record kept?
- Do replies to calls to place show the same asymmetry?

How the question serves the study's two questions:
- **The theory question.** It is about how a room settles what to act on. A refusal with a reason contests the room's goal, and an acceptance settles it, often by doing rather than saying.
- **The method question.** It is a check that evidence of the record's kind (written, coded replies) is not read as evidence of what members did.

## 2. The rules, written first

The rules were logged with `--kind abductive` before any reply was read (diary, C5c-11).

**A. Survival, counted before any text is read.** The count covers every item carrying a calls concept (P01) and every item carrying an attack concept (P09).
- *What is counted:* the direct replies to each item by another author.
- *By state:*
  - coded: the text survives in the coded record and can be read;
  - bridge: uncoded, kept because a coded reply sits below it;
  - collapsed: uncoded, with no text in the record;
  - removed.
- *Also counted:* replies whose author is "[deleted]".

**B. The test on calls to place.**
- *The pair:* one per room. The first part is the earliest call item in the room that has a coded direct reply by another author. The reply is the earliest such reply, its coded passages joined in text order.
- *The draw:* 80 rooms, with seed 20261015.
- *What counts:* a pair counts only if its first part calls or invites members to place for a work.
- *The codes, as in `c3b_ca_codes.json`:*
  - stance: accept, refuse, mixed or other;
  - account: a reason or ground given, or not.
- *The test:* one-sided Fisher's exact test.
- *Who coded:* I coded alone.

**C. What a result can change:**
- F-014's bound;
- a new finding for calls to place;
- A12's mechanism, the bare answer;
- the account's reading of the asymmetry, as a fact about written replies.

## 3. What was read, with counts

**Survival** (`c5c11_survival.json`):

| | calls to place (P01) | attack calls (P09) |
|---|---|---|
| call items | 1,949 | 1,565 |
| with a direct reply by another member | 920 (0.47) | 682 (0.44) |
| with a coded direct reply | 756 | 520 |
| direct replies | 2,858 | 1,271 |
| of these coded (readable) | 2,258 (0.79) | 942 (0.74) |
| bridge, collapsed, removed | 306, 283, 11 | 100, 227, 2 |
| uncoded, author [deleted] | 35 (0.012) | 14 (0.011) |

The store's "removed" state is mostly AutoModerator posts (594 of 617 overall), so it does not measure lost replies.

**What survival shows, before the asymmetry is read:**
- **Most calls get no written reply.** More than half of calls of either kind carry no written reply by another member. Whatever most members did with a call, they did not write it here. This is J's omission point. Placing leaves no line in the thread, and neither does a silent refusal.
- **Some written replies cannot be read.** A fifth of the written replies to calls to place carry no coded text, and a quarter of those to attack calls. Their stance cannot be read, and the store holds no text for them.
- **Deletion is small.** About one reply in a hundred has a deleted author, under either kind of call.
- **The filter is much the same for both kinds of call.** What survives is mostly cut by what was never written or never coded, not by later removal.

**The read: 80 pairs on calls to place** (`c5c11_place_codes.json`). 285 rooms had a pair, and 80 were drawn.
- **Set aside: 17.** In these, the first part is a report, an acceptance, or outreach to other subs.
- **Kept: 63.**

| stance | replies | give a reason |
|---|---|---|
| accept | 31 | 6 |
| refuse | 3 | 3 |
| mixed | 2 | 2 |
| other (questions, reports, jokes, notices) | 27 | 0 |

- **The test.** Refusals gave a reason more often than acceptances: 3 of 3 against 6 of 31, one-sided Fisher p 0.014.
- **The bare answers.** 25 acceptances are bare, with a median of 9 words: "I'll help." [PUBATTLEGROUNDS/c0050]; "Count me in!" [wow/c0246].
- **The refusals:**
  - "I've seen too much /r/place spam today already. So...no thanks." [polyamory/c0002];
  - ":( But I was drawing a fox there" [ScottPilgrim/c0002];
  - "Hi can you move please I'm drawing something there." [sbu/c0009].
- **The draws compared.** F-014's 38 against 14 was set by its draw, up to 40 rooms per kind (`c3b_ca_pairs.py`), not by the rooms. Here the draw takes the first coded reply of any kind, so 31 against 3 is the ratio among written, coded first replies.

## 4. What changed, by ledger id

- **F-023, written.** Written replies to calls to place show the same asymmetry, on few refusals, and most calls get no written reply at all. Its bound says that the stance ratio in writing is not the room's, and that the refusal side rests on 3 replies.
- **F-014, superseded by a bounded line:**
  - its first sentence now reads: "In written, coded replies to attack calls, refusals mostly carry a reason and acceptances mostly come bare";
  - its bound adds that the draw set the 38 against 14, the survival counts, and F-023.
- **A12** (C5-move-developing-170):
  - *bound:* takes the read count (25 of 31 acceptances bare, 3 of 3 refusals with a reason) and the survival limit;
  - *mechanism:* the answer due is "given in the thread or by placing". The last sentence now says that a bare join is the ordinary way a call is accepted in the written record, and that "a member can also accept by placing and write nothing, which the record cannot show".
- **Pass 14** is recorded in `account_passes.jsonl`. `model/history.jsonl` now has 133 lines.

## 5. What did not change, and why

- **No order count, element or arrow strength.**
  - A12 stays thin. Its reply form now has a read count, but the order from call to bare answer has none.
  - A16's mechanism keeps F-014's count. The fold-in may add "written".
- **The conversation-analysis mechanism stays as the arrow's source.** The read gives it a count. J asked that the study argue from organization, so the organizational reading is in section 6.
- **No attack-call draw by first reply was made.** The plan named calls to place only. A draw of the first coded reply to attack calls would give their written stance ratio as this read does for calls to place. It is left for the return if the fold-in wants it.

## 6. What the fold-in must carry

**The account:**
- *The bare answer:*
  - "A12 rests on such replies in 3 rooms; it has no order count" becomes "in 80 seeded first replies to calls to place, acceptances came bare in 25 of 31, and refusals gave a reason in 3 of 3 (F-023)";
  - "replies to calls to place were not counted this way" is removed;
  - add that more than half of calls carry no written reply, so the asymmetry is a fact about written replies.
- *The contest:* "in replies to attack calls a refusal usually gives a reason (F-014)" becomes "in written replies".

**The propositions:**
- **N07:** A12's reply form now has a read count. The fold-in decides whether the proposition still rests wholly on theorised arrows. A11 stays theorised.
- **N03:** its refusal clause takes "in written replies".

**The implications:** expectation 3 takes "in written replies", and adds that most calls get no written reply.

**The organizational reading, for the account's paragraph on what members settle.** A call proposes what the room will act on.
- **Accepting is mostly done, or said bare.** That is how a room settles a goal without deciding how it is organized.
- **Refusing is said with a ground.** A refusal contests the goal, and it is said in the room's own terms: its norm, the attack's cost, or a prior claim on the space.
- **The two are not alike in writing.** Refusing a call to place is rare in writing, and refusing an attack call is common. A call to place is mostly accepted or left alone, and an attack call is contested inside the room (F-014, A16). This fits the contract's demand that the model say how each room's goal was contested and changed.

## 7. How sure I am

- **The survival counts: firm,** as counts of what the record holds. They cannot say what the unwritten answers were.
- **The asymmetry on calls to place: qualified.** It points the same way as F-014 and is significant on its own, but the refusal side rests on 3 replies. I coded it alone.
- **J's framing: holds in part.**
  - *What the record supports:* most answers to calls are not in the writing, and later removal is too small to explain the asymmetry.
  - *What it cannot show:* whether acceptances or refusals were written or coded less often. A reply with no coded text has no readable stance.
- **The reading I keep.** Among the replies members wrote and coders coded, refusals carry a reason and acceptances mostly do not. That is a fact about what members chose to write. The account should say it that way.
