# B1 at 1 MB: the stopping rule

2026-10-07T07:20Z. From the orchestrator (Claude) to the handler. Target length: under 650 words. Advice, at J's request (09:18 Berlin). It replaces `Jail/Orchestrator/messages/2026-10-07T07-15Z_from-claude_to-handler_b1-stopping-rule-advice.md`. Put section 2 to J before building it: it turns his "thirty" into a floor.

## 1. B1b, the first pass: no change

Its rule counts words, in average rooms, and rooms, never legs (stage card, "When to stop"; `tools/saturation.py`), so no constant of it changes. A 1 MB stretch moves where a leg ends, not where the walk stops: the store holds about 113 kB of codes and themes a room, so a stretch is about nine rooms.

Your DECISIONS row of 03:51 reads "the stopping rule stays two stretches in a row with no new third-order theme". That clause was B1d's, not B1b's; your `changes-for-orchestrator.md` item 5 has it right. Say so in the next DECISIONS line.

## 2. B1d, the second pass: tie the run to marker 1

J wants the stop to follow the literature, not a value he sets. The literature gives its form, a run with nothing new after a base (Francis et al. 2010: ten interviews, then three in a row; Guest, Namey and Chen 2020: a run of two or three), but lengths only for 10 to 30 interviews. B1d's rooms are chosen, not random, so the first pass's estimates (Chao et al. 2014) do not hold there. The first pass has measured how long a run of nothing new had to be before that estimate let it stop: the empty run at marker 1.

**Proposal.** B1d stops when both hold:

- every room chosen for the pass is read; and
- the rooms read since the pass's last new third-order theme are at least as many as the first pass's empty run at marker 1, counted both in average rooms and in rooms, and never fewer than thirty rooms.

The first pass's empty run at marker 1 is measured from its last new kind before marker 1 to marker 1: `x(marker 1) - x(last new)` average rooms and `n(marker 1) - n(last new)` rooms. If the first pass stopped before marker 1 (the list's end, or the PI's stop at the check-in), the run is thirty rooms and thirty average rooms. If the chosen rooms run out before the run is met, the pass goes on down the seeded order (`saturation.py order`) with rooms not yet read in this pass; say so in the card, which is silent on it today.

For scale: thirty rooms in random order hold a median of 29.6 average rooms of words in this store (10th percentile 23.4), so the two floors agree.

**Cost, for J.** Marker 1's run is 10 average rooms plus three empty rounds of at most 25 each: about 13 to 85 average rooms, read at twice the depth. A ceiling would be J's value, and the card should say so.

## 3. To build, once J agrees

- `saturation.py`: when marker 1 is set, record `run_x` and `run_rooms` in it; print them in `status` and `report`. A B1d status from `kinds-B1.jsonl` lines whose `leg` starts `B1d`: rooms and average rooms since the pass's last new kind, against the target.
- The card's B1d paragraph: the rule above in place of "thirty rooms in a row", in the instrument, `DROPS/B1/stages/` and the analyst's `stages/` if B1 has been handed over; `STAGES-full.md` regenerated.
- `checks/stage_B1.py`: at B1d's last leg, test the run against `saturation.py`'s numbers, not the words of `saturation-B1.md`.
- Tests: a replay case; a planted short run for the check.
- Records: the CHANGELOG, `version_log.py`, DECISIONS with J's words, `changes-for-orchestrator.md`.

References, from memory, not checked online: Chao et al. 2014, *Ecological Monographs* 84(1), 45-67; Francis et al. 2010, *Psychology & Health* 25(10), 1229-1245; Guest, Namey and Chen 2020, *PLOS ONE* 15(5), e0232076.
