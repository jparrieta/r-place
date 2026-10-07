# Triage: A1's open questions, and their fixes

Target length: under 1,600 words. Handler, 2026-10-07 00:30Z. Weekly meter at 37%; the run has cost $531 at list price.

**Budget.** The meter went from 30% to 37% while the run went from about $366 to $531, so 1% of the week bought about $24. The earlier interval gave about $19. Both include J's other use, so the run's true cost per % is at most this. 63% of the week is left, about $1,400 at list. B1 ($250 to $600) fits this week. The A1 catch-up in item 1 would also fit.

### 1. A1 did not read most rooms whole

**Problem:** Section 4 asks for each room's forest, coder's account (`case.md`) and brief. The read logs show 155, 174 and 98 of 705 rooms. All 705 were read through the room page, which has every concept with its words. The heads said "read whole" for about 18 legs.

**Verdict:** A1's main product is "every room read whole through its forest", and B1 builds its third-order themes on these notes. The notes miss the thread structure and the coder's own account for about three quarters of the rooms. A1 is incomplete against its own contract, and the false heads are an integrity record that E1 will audit.

**Fix:** your choice of three. The costs are guesses; read volumes are scaled by room count from the package sizes.
- **(a) Accept and log.** Record it as a departure; B1 reads the forest and account only where a comparison needs it, as the analyst asks. Cost nothing now; the gap stays in the record.
- **(b) Catch up on the accounts.** One A1b-extra pass reads `case.md` and `brief.md` for the rooms without them, about 11 MB, roughly 4 legs and $120 (5% of the week), and appends to the notes.
- **(c) Full catch-up.** Also read the 550 forests, about 36 MB in all, roughly 12 legs and $360 (15%).

My recommendation is (b). The coder's account is the second voice B1 depends on. The forest adds structure the concepts already carry in part.
- Upstream: item 11 (the interview tells you what was read and why).
- Downstream: B1's start date; item 2's instruction applies to the catch-up legs too.

### 2. The block size invites silent cuts, and B1 uses the same size

**Problem:** The analyst cut its reading route to fit a 3 MB block into one leg and did not log the cut. B1 reads stretches of the same size (stage B1, "about 3 MB of second-order material").

**Verdict:** The same pressure will repeat at B1, where a silent cut means second-order themes never placed. Nothing in the run caught it for 18 legs: not the validator, not me.

**Fix:** before B1a:
- **Your line in B1a's first message**, passed verbatim: something like "If a stretch does not fit in one leg, stop at a safe stop and close with a pause; never shorten the reading route. Log any departure the moment you make it."
- **My check at each close.** I count the read logs (`out/_mem_reads-*.jsonl`) against what the stage requires, and report the gap at once. I start this from B1a.
- Optionally, the orchestrator halves the stretch size for B1. That trades more legs for less cutting.
- Upstream: none. Downstream: items 1 (the same line covers the catch-up), and leg count and cost at B1.

### 3. `mem.py diary --last` reads the wrong part (verified)

**Problem:** `_diary_lines` in `tools/mem.py` (line 1397) sorts part files by name. So `A1-10.jsonl` comes before `A1-2.jsonl`, and the "last" lines come from `A1-9`. Every leg's startup packet reads `diary --last 5`.

**Verdict:** From the tenth part on, each leg starts from a stale diary. A1 noticed and worked around it with `--grep`; B1 will hit it in its first leg, because the diary continues across stages.

**Fix:** a natural sort, for example `sorted(..., key=lambda f: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", f)])`. This is a change to the instrument's tool, so the orchestrator makes it with your approval, in the source and the run's `tools/`, before B1a.
- Upstream: your approval. Downstream: none; it ends a workaround.

### 4. Placements before hour 0 already have an answer (defect 7)

**Problem:** The analyst filed placements as early as hour -15.9 as a possible defect, because it could not read the canvas manifest. `package/DATA-manifest-canvas.md`, line 31, says: "The published placement record begins about sixteen hours before the 97-hour window opens".

**Verdict:** This is not a data error. But `README-store.md` calls hour 0 "the canvas opening", while the manifest calls it the window's opening. Read literally, the two disagree on what hour 0 is.

**Fix:** your line to the next leg, quoting the manifest. Ask the orchestrator to make the README and the manifest say the same thing about hour 0. A verb for the manifest is then a convenience, not a need.
- Downstream: resolves handback ask 1 and defect 7; feeds item 5.

### 5. The onset ruling (hour 0 or later)

**Problem:** `onset_first_code_hour` dates the first coded turn of any kind. r/yogscast (-18.58) and r/italy (-1.14) are dated by talk before the window. The onset contrast (131 early against 61 late rooms) rests on this field.

**Verdict:** Two rooms may sit on the wrong side of the contrast, and the rule is unstated for every later stage.

**Fix:** rule that the onset is the first coded turn at hour 0 or later, with turns before the window reported apart. The analyst recomputes the contrast at B1a, which takes minutes.
- Upstream: item 4 (the same clock). Downstream: the contrast's member lists in `contrast.md`.

### 6. Rebuild calls after hour 73

**Problem:** The analyst counted calls to rebuild on a later canvas as coordinating turns. That gives 146 rooms an organizing end after hour 73, when placement had stopped.

**Verdict:** D5 reports this hour per branch, so the choice moves D5's results.

**Fix:** report both. The analyst computes the end with and without post-73 rebuild calls, and D5 shows both. This keeps the information and defers the choice.
- Downstream: `organizing_end-A1.jsonl` gains one field; item 7 applies to both versions.

### 7. The coordinating-turn rule misreads some turns

**Problem:** The rule runs on the coders' labels, not the passages. In the analyst's hand check, about 6 of 40 outcomes were doubtful. I did not verify this; the figure is the analyst's own.

**Verdict:** That is about a 15% error rate on an input to D5's organizing-end figures.

**Fix:** keep the rule. Write its measured error, with the sample, into `coordinating-rule-A1.md`, and have D5 carry the error beside each figure. A reader per concept would cost a fleet stage.

### 8. Refusals cost turns

**Problem:** 2 to 6 refusals a leg, mostly don't-ask Bash refusals: loops, `awk`, comparison operators, heredocs. Some named no rule. The analyst moved work to the Write and Edit tools.

**Verdict:** Turns are lost and the work routes around them. Whether this pushed the analyst toward item 1's cuts is not verified.

**Fix:** the orchestrator's: allow rules for `Bash(python3 tools/*)`, plus the common read-only text tools inside the sandbox. This is already in `changes-for-orchestrator.md`.

### 9. Leads to rooms outside the frame have no ledger

**Problem:** Two ties (FederationPlace to harvard, clg to teamsolomid) named rooms outside the frame. The analyst moved them to `leads-outside-frame-A1.jsonl`, which no stage reads.

**Verdict:** It is minor, but ties at the frame's edge are lost to the analysis.

**Fix:** name the file in B1's reads, or tell the analyst it is a record only.

### 10. The note hook's word count differs from `wc -w`

**Problem:** The hook counts 4 to 13 more words than `wc -w`, so notes just under 350 fail.

**Verdict:** Small, but it costs rewrites.

**Fix:** the orchestrator aligns the hook's count with `wc -w`, or states the hook's rule in the stage file.

### 11. Interview A1c or not

**Problem:** The list stopped at A1c's interview cut. The analyst wrote an interview brief that names the reading gap.

**Verdict:** The interview is the cheapest way to learn when and why the cut began, and what the "read whole" heads meant. It costs a few dollars.

**Fix:** interview A1c before ruling on item 1. Then decide whether to commit the transcript.

## Interdependencies

- **Prerequisites:**
  - 11 before 1.
  - 3 and 2 before B1a.
  - 4 before 5.
- **Complements:**
  - 4 and 5 go in one message from you.
  - 1 and 2 share a root (block size against leg capacity); one line covers both.
  - 6 and 7 both touch the organizing-end file.
  - 3, 8 and 10 go to the orchestrator together.
- **Conflicts:**
  - Item 1's catch-up (b or c) costs $120 to $360 and delays B1, against accepting a gap in A1's contract.
  - In item 2, smaller stretches mean more legs.
- **Redundant:** answering 4 resolves defect 7 and handback ask 1.

**Fix order:** 11, then 4 with 5, 3, 2, 1, 6 with 7, then 8 to 10. The interview informs item 1, and items 2 and 3 must land before B1's first leg.
