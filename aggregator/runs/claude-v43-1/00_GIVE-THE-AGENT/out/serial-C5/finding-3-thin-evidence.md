# Finding 3: thin evidence (C5c-09, pass 12)

Target length: about 1,800 words. Problem 3 of the serial work. It is worked second in the order revised at C5c-08, and keeps its number by problem, as the plan says.

Scripts and codes: `c5c9_border_score.py`, `c5c9_a10_codes.json`, `c5c9_a10_rule6.py`, `c5c9_a10_reverse.py`, `c5c9_a10_reverse_codes.json`, `c5c9_a05_codes.json`, `c5c9_a14_codes.json`, `c5c9_order_tally.py`, `c5c9_findings.py` and `c5c9_model_spec.json`. The reads are `c5c9_a10_read.txt`, `c5c9_a10_reverse_read.txt`, `c5c9_a05_read.txt` and `c5c9_a14_read.txt`.

## 1. The question

J's advice (C5c-07): thin is not bad, because crucial things happen rarely. When should a count weigh more than my reading of the material, and when not? The leg applies the answer to two cases:
- **the move after doubt** (A10, from K02 to P10);
- **border talk and what follows it:** A05, to sparing; A14, to help; and A04's first-turn reading.

How the question serves the study's two questions:
- **The theory question.** The move after doubt answers the contract's "what sends a group back to that beginning". Border talk is organizing that crossed room boundaries.
- **The method question.** A thin arrow at the population level may be strong inside a form. Where it belongs is a question of composition.

## 2. The stance and the rules, written first

The stance was logged with `--kind abductive` before I read either source or any room (diary, C5c-09).
1. **There are two kinds of thin.**
   - *Rare-thin:* few rooms can carry the claim, because the event is rare by its nature.
   - *Weak-thin:* many rooms carry both elements, but the order barely beats its null.
2. **A count decides a claim about a distribution or an order across rooms,** when its denominator is large enough for a null. A weak-thin order is stated as a tendency near its null, whatever I believe. The words may still show the mechanism in the rooms that run it, and that is a separate claim, read with codes written first.
3. **My reading decides a rare-thin claim, with the count beside it,** when three things hold:
   - the event is rare by nature;
   - the step shows in members' words;
   - no room shows the reverse.

   Then the claim stands as a mechanism shown in N rooms, labelled thin (rule 8), not as a tendency (rule 16).
4. **For composition,** a rare-thin arrow's rooms are named for the return.

**The sources, read after the stance and cited from the page** (`sources-from-J/`):
- **Gioia, Corley and Hamilton 2013:**
  - the study of social construction focuses "less on the number or frequency of measureable occurrences" (p. 16);
  - qualitative work is suspected of theorizing "on the basis of rather thin evidence", and the answer is to show the evidence: "Where is the evidence for your assertions?" (p. 18);
  - the data structure is that answer, and attention goes to "nascent concepts that don't seem to have adequate theoretical referents" (p. 20).
- **Grodal, Anteby and Holm 2021:**
  - "Not all information is equally important in the categorization process" (p. 597);
  - negative and unusual cases matter in theorizing "even if there is 'only one case'" (p. 598, quoting Emerson, Fretz and Shaw);
  - a category "abundant in the data" was dropped as peripheral to the theory (p. 599);
  - propositions are held loosely, with each conjecture rated "strong, qualified, neutral, or contradictory" as a safeguard against premature closure (p. 604, quoting Miles et al.).

**What the sources add.** The stance stands: frequency does not set importance, but a thin claim must show its evidence and carry its rating. The ratings are used in section 7.

**The codes** (logged before each read):
- **A10:**
  - J: the judgment of too few hands or too little space comes before a move after a loss;
  - M: the move comes first;
  - C: the move is by choice or a coalition's plan;
  - N: no move.
- **The added rule 6 read** (logged before it ran):
  - G: the room gives the work up;
  - F: it keeps fighting;
  - S: the doubt comes before any loss;
  - O: other.
- **A05:**
  - L: the first sparing names a border, truce, deal, policy or agreement;
  - T: it names none;
  - O: other.
- **A14:**
  - C: the first help names a deal, border, truce, alliance, an exchange or the neighbour relation;
  - H: it names none;
  - O: other.
- **The rule for A05 and A14:**
  - the line or channel share, where the order holds, is at least half: the mechanism shows in words;
  - it is under a third: the mechanism is theorised.

## 3. What was read, with counts

**The border second coding.** The return has 40 records and its end marker. It was scored by the rule logged at C5c-07 (`c5c9_border_score.py`).
- **My codes:** T 34, D 4, O 2. **The field analyst's:** T 21, D 5, O 14.
- **Agreement:** we agree on 23 of 40, with Cohen's kappa 0.19.
- **The splits:**
  - 12 are T/O: the field analyst read reports of contact, diplomacy or thanks as O.
  - 5 split between terms and damage.
- **The result:** T of T plus D runs from 19 of 26 (0.73) to 36 of 38 (0.95). The field analyst's codes alone give 21 of 26.
- **Judged by the C5a-02 rule** (T at least half), the claim holds at both ends of the range. My 34 of 38 was too high, and agreement is slight. We differ on what counts as offering terms, not on terms against damage.

**A10, all 21 rooms carrying both elements, read whole** (the first three concepts of each):
- **Codes:** J 10, M 10, N 1 (texas: repair and fighting back).
- **J is 10 of 20,** exactly at the rule's line.
- **Who voices the judgment:** the room in 7 rooms, and one member apart in 3 (FloydVsVoid, halo, shield).
- **An example of J:** "We just don't have the people." [anarcho_capitalism/c0031], then "Buildling ancap flag somewhere else would be a good idea" [anarcho_capitalism/c0077] (the record's spelling, restored at C5c-12). Another: "We are going to die out" [greenlattice/c0318], then "should we retreat and relocate" [greenlattice/c0349].
- **In the M rooms, the loss itself prompts the move:** "We will have to start over from someplace else" [aceattorney/c0036]. In five rooms the judgment is said inside the move turns, so the coders placed it under the move.
- **One mixed room.** MiamiHurricanes voiced its own doubt ("i don't think this sub is big enough to sustain it") an hour before a move that came by a coalition's plan. Read as a coalition's move, J is 9 of 20, and the rule does not decide. The pass 2 bound had said it had "no doubt of its own"; that reading is corrected.

**Rule 6 for A10:**
- K02 is in 89 rooms and P10 in 124.
- 218 rooms' records say their work was lost. Of these, 36 voiced doubt, and 10 of those 36 moved.
- The 26 with no move were read whole:
  - G 11, the work given up: "we're not doing this anymore don't do it" [raocow/c0062];
  - S 7, the doubt came before any loss;
  - O 8;
  - F 0.

**A05, all 158 rooms, read whole:**
- **Codes:** L 17, T 107, O 34.
- **Where border talk comes first:** L is 11 of 81 (0.14). **Where it does not:** 6 of 43 (0.14).
- **What the T rooms show instead:** a norm of the room ("Don't ruin other people work" [czech/c0062]; "We want to avoid consuming another community's project" [starcraft/c0062]), a refused raid, or an apology.

**A14, all 214 rooms, read whole:**
- **Codes:** C 86, H 108, O 20.
- **Where border talk comes first:** C is 63 of 127 (0.496). **Where help comes first:** 23 of 67 (0.34).
- **Examples of C:**
  - "As per the terms, we will help with the triangle" [TeamYellowPlace/c0047];
  - "they put their flag underneath our oryx when we asked them to, so at least we should return the favour and help them" [rotmg/c0098];
  - "we must help /r/virginiatech with moving their art as per agreement" [titanfall/c0203].

## 4. What changed, by ledger id

- **F-019, written.** After a loss, a room that judges its hands too few either moves or gives the work up.
- **F-020, written.** Sparing a neighbour rests mostly on the room's own norm. Help between rooms rests on a deal about as often as not, and more often where border talk came first.
- **Four arrows amended** (`model/history.jsonl`, 128 to 132 lines; C5-move-developing-164 to 167):
  - **A04's bound** takes the two-coder range, the agreement and the kind of split.
  - **A05's bound and grounding note** take the read, and its mechanism is marked theorised. The arrow stands as an order near its null.
  - **A10's bound** takes the whole read, the mixed room, and giving up as the other outcome. The arrow holds for the rooms that move.
  - **A14's bound** takes the read. 0.496 falls between the rule's two lines, so the rule does not decide. I judge the mechanism shown in words, on the contrast between the two groups of rooms, and the bound says so.
- **Pass 12** is recorded in `account_passes.jsonl`.

## 5. What did not change, and why

- **No order count, strength or element.**
  - All three arrows stay thin: A10 is rare-thin; A05 and A14 are weak-thin.
  - A05's order still beats its null, so the arrow stays. Only its mechanism loses its claim to show in words.
- **A10's mechanism sentence.** "Stops fighting for it" holds in both outcomes. "And moves" is the arrow itself. The other outcome is a bound, not a new element, which C5 forbids.
- **No proposition, account sentence or declaration.** These are listed below for the fold-in, as the plan says.

## 6. What the fold-in must carry

**The account:**
- *Other rooms:*
  - "(34 of 38 read)" becomes the range: 19 of 26 to 36 of 38 by two coders, kappa 0.19.
  - A05's line is theorised: sparing rests mostly on the room's own norm (F-020).
  - A14's channel shows in about half the rooms where border talk comes first (F-020).
- *Loss and a move:* add the other outcome. In 11 rooms that voiced doubt and lost their work, the room gave the work up (F-019).

**The propositions:**
- **N08** takes F-019 as evidence. Its rival or boundary names giving up as the other outcome.
- **N09 is narrowed.** The stage file says to narrow a proposition to the subset its arrows carry. A settled border opens a channel through which two rooms trade help (A14, shown in words in about half). Whether it also gives a line for sparing (A05) is theorised.

**The prose test's four flagged names:**
- **Live and let live:** F-020 shows restraint mostly with no agreement named, which is the tacit part of the name. Its reciprocal part shows in a few: "let's not touch minecraft, they've done nothing to us" [indonesia/c0019].
- **Reciprocity:** F-020 shows exchange in words: "in return", "return the favour".
- **Collective efficacy:** F-019 shows the room's judgment of its hands before a move in 10 rooms, 7 voiced for the room.
- **Critical mass:** not touched by this read.

**C5d again:**
- Implications expectation 2 takes the range.
- Expectation 4 adds giving up as the other outcome after doubt and a loss.
- A new expectation for the return: where a room meets a neighbour, sparing comes with the room's norm, and help comes with a deal.

**For composition at stage D:**
- Moving and giving up after doubt and a loss are a candidate branch. The rooms are in `c5c9_a10_codes.json` and `c5c9_a10_reverse_codes.json`.
- This is the contract's two kinds of ending, read in the record:
  - the move sends the room back to a start;
  - giving up ends the organizing, not the room.

## 7. How sure I am, and when the count weighed more than my reading

Each claim is rated in Miles et al.'s terms (Grodal et al. 2021, p. 604):
- **A10, qualified.** Rare by nature. The step shows in the room's words in 10 rooms, 9 if the mixed room is read the other way. Giving up is the other outcome, not the reverse. My reading decides here, with the count beside it, as the stance says. This is what J called thin and important.
- **A05's mechanism, neutral.** I believed a settled border was what members spared by. Read whole, the first sparing named a line in 17 of 124 rooms. The rooms state their own norm instead. Here the count weighed more than my belief, as the stance says it must for a common act. The reading corrected my intuition, not only bolstered it.
- **A14, qualified.** The channel shows in about half the rooms where border talk comes first, and in a third where help comes first. The rule I wrote did not decide the middle. The judgment is mine, and it is said where it is made.
- **A04's first-turn reading, qualified.** It holds at both ends of the two-coder range. With agreement this slight, the claim is "mostly terms", not a count.
- **The limits.** I coded every read alone, under rules written first. Only the border read has a second coder. Every read took the first concept of each element in each room, and a later concept may name what the first does not.
