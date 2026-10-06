# Stages of claude-v43-1: what each does, and what it may cost

Target length: under 1,100 words. Written by the handler, 2026-10-06 19:10Z, for J. Only A1 is measured; everything after it is an estimate from the stage cards' leg structure, marked as one.

## The yardstick (measured, A1, 2026-10-06)

Source: each turn's `result.json` in `CONTROL/legs/actors/` (outside `.cc`). Cost is list-price dollars from `total_cost_usd`, which adds up across legs, so the figures are increments.

| Leg | Minutes | List cost |
|---|---|---|
| A1a (checks) | 14 | $6 |
| A1b-01 to A1b-09 (reading blocks of about 3 MB) | 27 to 51, mean 37 | $23 to $46, mean $30 |

Two leg classes follow from this:
- **small** (a check, a build, a single pass): $6 to $15, 15 to 25 minutes;
- **full** (a reading or working leg): $25 to $45, 30 to 50 minutes.

**Your meter.** J read 25% weekly at 18:08Z and 30% at 20:09Z; the run cost about $97 between them, so 1% of a week buys about $19 of list cost ($16 to $24 with rounding), and a full leg uses about 1.5% of a week. The 5-hour window is a separate limit: about 8 full legs fit in one.

**Fleet dispatches** (B2, B3, B4, C2, C5, D2, D3, E1) run on OpenRouter from your Terminal, and D2's labelers in Codex. They are not on the Claude subscription and are not estimated here.

## The stages

Leg counts with NN are set by the data during the run; the ranges are guesses.

| Stage | What it does | Legs (guess) | List cost (guess) | Leg time (guess) |
|---|---|---|---|---|
| A1 Reading | every room read whole; notes, lexicon, the analysed set | 1 small, 19 blocks, A1c; 9 blocks done | **rest: $380 to $550** (block 13 is r/counting alone, 11 MB) | rest: 7 to 9 h |
| B1 Third-order scheme | third-order themes built from every second-order theme, read in a seeded order until the stopping rule | prior, 3 to 8 stretches of about 3 MB, saturation, 2 to 6 second-pass legs, scheme (interview): 8 to 17 | $250 to $600 | 5 to 11 h |
| B2 Pilot | the scheme tried on fresh readers, round by round, then frozen | build and check per round, 2 to 3 rounds, gold and stability: 6 to 8 | $120 to $250 | 3 to 5 h, plus dispatches |
| B3 Fleet | every second-order theme placed by R readers | build, check (may span legs): 2 to 3 | $50 to $120 | 1.5 to 3 h, plus the dispatch |
| B4 Adjudication | contested placements ruled, 500 per leg; blind sample; placements final (interview) | 2 to 6 packets, sample build and check: 4 to 8 | $120 to $300 | 2.5 to 6 h |
| C1 Structuring | scheme v2, fourth-order themes and a first story | 2 to 5 passes (interview at the last) | $60 to $200 | 1 to 4 h |
| C2 The loop | constructs, the typed model and its arrows, the story until it holds; one hostile reader | 3 to 8 passes, reviewer build and check (interview), 2 closing passes: 7 to 12 | $200 to $450 | 4 to 9 h |
| C3 Literature | the model against work that contradicts it and work that resembles it | 3 (interview) | $60 to $130 | 1.5 to 2.5 h |
| C4 The field | the model against the sealed field model of r/place | 1 (interview); needs the field analyst's model | $20 to $45 | under 1 h |
| C5 Account | the model as prose, the Gioia table, the dynamic model, the figure; three readers | 2 to 4 passes, readers build, 2 checks, table (interview): 6 to 8 | $150 to $300 | 3.5 to 6 h |
| D1 Return build | writes the handoff folder for the return | 1 | $15 to $45 | under 1 h |
| D2 Labelers and verdicts | per room, GPT labelers in Codex adapt the model; a verdict fleet | 1 check leg | $20 to $45 | under 1 h, plus Codex and the fleet |
| D3 Adjudication | every adaptation ruled by element; re-check (interview) | 3 to 8 element groups, recheck, freeze: 5 to 10 | $130 to $350 | 3 to 7 h |
| D4 The tree | branches cut by the ladder walk (interview at the last) | 2 to 5 cuts | $60 to $200 | 1 to 4 h |
| D5 Branch accounts | per branch: what it does differently, its codes, representative rooms | 4 to 10 branches, waterfall: 5 to 11 | $130 to $400 | 3 to 8 h |
| D6 Retelling | the model told again with the forms inside it (interview) | 3 to 6 dimensions, telling: 4 to 7 | $100 to $250 | 2.5 to 5 h |
| E1 Audit | scripts over transcripts, the probes, a reconstruction sample, the account of the run | scripts, 4 to 8 sections, reconstruction build and check, experience: 8 to 12 | $200 to $450 | 5 to 9 h |
| E2 Feedback | how the analyst was handled; the instrument it would build next (interview) | 2 | $40 to $90 | 1 to 1.5 h |

## Totals (guess)

- **After A1:** 67 to 114 legs, about $1,700 to $4,200 at list price, 40 to 75 hours of leg time.
- **With the rest of A1:** about $2,100 to $4,800, 47 to 84 hours.
- **On your meter:** at about $19 per weekly %, the rest of the run after A1 is about 90% to 220% of a week, one to two and a half weeks of subscription. Plan pauses at week ends (`legs.py pause`; HANDLER.md, "Pausing").

## How this estimate improves

- After each stage, replace its row with the measured figures (the handler logs each close's cost in `diary.md`).
- Each % reading you give against a close sharpens the % per leg.
- The NN counts become known at each stage's first leg: B1's stretch count from `mem.py progress --plan`, B4's packets from B3's inventory, D5's branches from D4.
