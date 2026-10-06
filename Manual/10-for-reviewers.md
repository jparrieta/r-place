# For reviewers: the method, the models, and checking one room

*Kind of page: tutorial and explanation: check one room yourself, and how the method maps onto Gioia and Eisenhardt.*

For a reader who knows Gioia and Eisenhardt and wants to judge whether this is their method, who did each step, and how to check the agents' work without taking the Manual's word. Everything here is drawn from the instruments; the sources are linked.

## The tiers against Gioia's

The project's names for its tiers are not Gioia's. The coder's themes are Gioia's first-order concepts, consolidated within one case, although the files call them `second_order`. From [the aggregator's contract](../aggregator/instrument/CONTRACT-aggregator.md), section 2:

| This project | What it is | Who makes it | Gioia's name |
|---|---|---|---|
| code (first-order concept) | the participants' words, coded, with the quote | coder | first-order concept |
| second-order theme | a room's codes consolidated within that case | coder | first-order concepts, consolidated within a case |
| third-order theme | a kind of second-order theme found across cases; near the material, never a construct | analyst | first-order concepts, consolidated across cases |
| fourth-order theme | a named group of third-order themes; a construct | analyst | second-order theme |
| aggregate dimension | what those constructs are about | analyst | aggregate dimension |

The coder contract says the same from its side: "In Gioia's terms your themes are his *first-order concepts*", and Gioia's second-order themes "are made later, by a reader who sees every community" ([CONTRACT.v32.md](../coder/instrument/v32/CONTRACT.v32.md), section on themes). So a coder never abstracts beyond its case; all abstraction across cases is the aggregator's.

## Who did each step, on which model

| Step | Agent | Model | Record |
|---|---|---|---|
| brief (the room's ordinary week) | brief writer, one per room | GPT-5.6 Sol, effort medium, through Codex | the yard's records |
| codes, themes, account | coder, or a serial fleet of coders and a case lead | GPT-5.6 Sol, effort medium, through Codex | each room's `STATE.json`; `run/INPUT/coders/CODERS.tsv` |
| scheduling the yard | coordinator | GPT-5.6 Terra | the possibilities log |
| stages A1 to E2 | the analyst, one per leg | Claude Opus 5.5, effort by stage | [CONTROL/arm.json](../aggregator/runs/claude-v43-1/CONTROL/arm.json) |
| placing themes at B2 to B4; verdicts at D2 | reader fleets | `@preset/cheap` on OpenRouter | `arm.json`; [FLEET.md](files/aggregator/fleet.md) |
| the hostile reader at C2; three readers at C5 | readers | Claude Opus 5.5 | the contract's stage table |
| the return: each room's adaptations at D2 | labelers, each resuming the room's original case lead | GPT, in Codex | `arm.json`, D2 |

**Where the coding stands (26 September 2026).** Every room is coded by the one model above. The rooms coded before the yard existed, by Claude on instruments v16 to v27, are being recoded in the yard; until they are, 299 of the current frame's 659 rooms carry those earlier codings, and `CODERS.tsv` says which. The frame is taken again when coding closes, from yard codings only.

`@preset/cheap` is a preset in the author's OpenRouter account: it names no fixed model, so the readers cannot be reproduced exactly, and their packets of Reddit text go to OpenRouter's providers. The fleets are a prosthesis for scale, not a panel of judges: the analyst builds the scheme and rules on every disagreement (B4, D3), and B4 reports Krippendorff's alpha on a blind re-placement.

## The departures, as the method states them

[METHOD.md](../aggregator/instrument/METHOD.md) names four departures from Gioia and Eisenhardt and says what stands in for each:

- **The tier split.** Coders make the first two tiers; one analyst makes the rest. The coders never see another case.
- **No overlap between collection and analysis.** The analyst did not collect the data and cannot go back to informants.
- **A census in place of theoretical sampling.** The rooms arrived as a census. Sampling happens inside the corpus: every arrow in the model at C2 must be sampled, and the return (D1 to D3) names the rooms the model cannot compose.
- **An in-sample return, not a hold-out test.** The return is modelled on Eisenhardt's replication logic. It is in-sample at the tier the model was built from and out-of-sample below it, where the concepts and quotes the model never used can contradict it.

METHOD also says what to write in a methods section, and what is not promised: every prompt, input, output, transcript and model identifier is archived, so any claim can be traced; the study does not promise that a rerun reproduces it. The informant relationship is absent: the first tier is archived text, and the method says to claim informant voice nowhere.

## How stable is one reading?

The evidence is thin, and small:

- **Seven independent coders on r/dorset** (18 items, an early contract, v5, August 2026). Every run cited all 18 items. Codes ranged from 30 to 43; themes from 6 to 16, with six of the seven between 6 and 9.
- **Two readings of r/dorset** under different instruments and models (v20 on Claude Opus, v30 on GPT-6, September 2026). They agreed at the code layer, as the same reading at two grains, and parted at the theme layer, where one consolidated across exchanges and the other followed them one by one.
- **r/liverpoolfc**, read several times under several versions, fixed the 97-hour window: no reading found anything codeable beyond it.

These figures come from the project's working notes, which are not in this repository. No study of reliability across the census has been run. Treat a room's reading as one careful reading, checkable against its record, not as a measured consensus.

## Checking one room yourself

Every verified room carries its whole run. Taking Armenia, from the repository root:

```bash
mkdir -p /tmp/armenia && zstd -dc coder/rooms/armenia/run.tar.zst | tar -x -C /tmp/armenia
cd /tmp/armenia/run
python3 close_run.py . --record coder_corpus.jsonl --role lead
```

`close_run.py` is the gate the room passed, in the version the room ran (Armenia ran v30, whose gate has ten checks; v32's has twelve). Its output on Armenia:

```
  PASS C3  every code's text is byte-identical to the record (168 codes)
  PASS C6  no thread claims more reading than read.py served
  PASS C9  every live code and pointer sits on an item read.py served (123 threads whole, 127 single items)
10 of 10 checks passed.
```

What each check means is on [close_run.py's page](files/coder/close-run-py.md). Three things you can then check by hand:

- **A quote is in the record.** Take any line of `out/codes.jsonl`, copy its `text`, and search `coder_corpus.jsonl` for it. C3 did this for every code.
- **What the coder read.** `out/_read.jsonl` logs every service of the reading tool, in order. Compare it with the threads `case.md` discusses.
- **Its own words.** `out/_transcript.jsonl` is the coder's conversation; the account in `case.md` should follow from it.

`zstd` is a common package (`brew install zstd`, `apt install zstd`). A handler-side script, [check_quotes.py](../aggregator/handler/check_quotes.py), runs the quote check over a seeded sample of rooms before stage E1. It needs the full coding yard, which is outside this repository; set where yours is in `aggregator/handler/paths.json`, a copy of `paths.example.json` ([the handler's folder](files/handler/README.md)). Its result for the run is `run/DROPS/E1/quote-check-E1.json`.

**What the quote check found.** On 80 rooms sampled with seed 13, every code's quote was found in its item (share 1.0). Of the long quotes in the case accounts (strings of 25 characters or more in double quotes), 73 per cent were found in the room's corpus. A quote not found is not proved invented: an account may quote a brief, a thread title in other words, or join two passages; but the analyst meets the check at stage E1, and a claim that rests on a case account's quotation should be traced to a code, which is always exact ([trace one claim](trace-a-claim.md)).

## What the run has not yet shown

The analyst of this run has not started (the runs claude-v41-1 and claude-v42-1 stopped in stage A1 when the instrument changed; their legs are in the archive, not in this record). Until stage C5 closes there is no model, and until the return (D1 to D3) there is no test of it. The [front page](README.md) shows how far the run has got. What exists now is the method, the coders' readings of each room, and the trail that lets you check them.
