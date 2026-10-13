# Token usage, claude-v43-1

Target length: under 900 words. Handler log, kept in tokens only. First written 2026-10-13T08:55Z; update at each close.

## How the Claude figures are counted

Source: each leg's `CONTROL/snapshots/<leg>/transcript.jsonl`. One API call is written as several transcript rows (thinking, text, each tool call), and every row repeats the same usage block. The harness's `cost.json` sums every row, so it counts most calls two or three times; across the run it reports 22,878M cache-read and 65.4M output against 10,453M and 23.5M counted once per message id. Checked on B4a-05: 306 of 306 multi-row messages carry identical usage. The figures below count each message id once, in the first leg whose transcript holds it, so a resumed session's inherited calls are not counted again. Per-leg figures are in `2026-10-13-claude-tokens-dedup-per-leg.json`. Every figure the handler reported from `cost.json` before this date is about twice too high.

## Claude analyst (claude-opus-5-5), by stage step

| Step | Legs | Calls | Input | Cache write | Cache read | Output |
|---|---|---|---|---|---|---|
| A1a checks | 1 | 81 | 162 | 0.2M | 11.9M | 0.1M |
| A1b reading blocks | 55 | 7,196 | 14,390 | 19.4M | 3,462.9M | 4.9M |
| A1c close | 1 | 46 | 92 | 0.1M | 6.9M | 0.0M |
| B1a prior | 1 | 27 | 54 | 0.1M | 16.2M | 0.0M |
| B1b stretches | 34 | 10,389 | 20,754 | 29.4M | 5,248.3M | 11.7M |
| B1c saturation | 1 | 92 | 184 | 0.5M | 34.9M | 0.2M |
| B1d second pass | 7 | 1,046 | 2,090 | 6.3M | 514.8M | 1.0M |
| B1e scheme and interview | 1 | 325 | 650 | 1.1M | 146.9M | 0.5M |
| B2a builds (3 rounds) | 4 | 175 | 350 | 0.8M | 81.1M | 0.2M |
| B2b checks and freeze | 6 | 412 | 824 | 2.8M | 210.0M | 0.4M |
| B2c gold and stability build | 1 | 18 | 36 | 0.0M | 10.7M | 0.0M |
| B2d scoring | 1 | 46 | 92 | 0.2M | 32.4M | 0.1M |
| B3a build and gold check | 2 | 68 | 136 | 0.3M | 44.5M | 0.1M |
| B3b assemble and check | 1 | 93 | 186 | 0.3M | 18.8M | 0.1M |
| B4a adjudication, packets 1 to 7 | 7 | 1,926 | 3,852 | 13.7M | 928.1M | 6.2M |
| B4b blind-sample build (B4b, p2, p3, p4) | 4 | 152 | see json | see json | 106.3M | 0.2M |
| B4c blind-sample check | 1 | 87 | see json | see json | 31.4M | 0.2M |
| C1a structuring, passes 1 to 6 | 6 | 611 | see json | see json | 301.1M | 1.1M |
| **Total** | 134 | 22,790 | see json | see json | 11,207.0 M | 26.8M |

B4a per leg (cache read / output): B4a-01 88.5M / 0.5M; B4a-02 99.2M / 0.6M; B4a-03 139.0M / 0.8M; B4a-04 108.7M / 1.0M; B4a-05 177.8M / 1.3M; B4a-06 177.6M / 1.1M (369 calls); B4a-07 137.3M / 0.9M (257 calls).

## DeepSeek fleet on OpenRouter

Source: J's export `Orchestrator/Claude/openrouter_activity_2026-10-13.csv`, 1,573 calls from 2026-10-11 15:30Z to 2026-10-12 20:41Z. All on one key. Models: deepseek-v4-flash-0731 until round 2's rebuild (182 calls), deepseek-v4.1-flash-0910 after (1,391). The export carries no batch or stage label, so the stage is assigned by time window against the diary; treat the split as inferred. `Prompt` includes the cached part; fleet.py's own `in` figures are prompt minus cached (checked: B3 group 1 9.65M minus 7.95M = 1.69M, as fleet.py logged). `Reasoning` is part of `Completion`.

| Dispatch | Calls | Prompt | of which cached | Completion | of which reasoning | Cut at length | No finish |
|---|---|---|---|---|---|---|---|
| B2 round 1, early failed tries | 4 | 0.0M | 0.0M | 0.0M | 0.0M | 2 | 2 |
| B2 round 1 (incl. retries at max_tokens) | 47 | 2.4M | 0.6M | 0.9M | 0.8M | 16 | 20 |
| B2 round 2, first build, three tries (build discarded) | 130 | 7.6M | 4.0M | 0.1M | 0.1M | 2 | 65 |
| B2 round 2 (rebuilt) | 17 | 1.6M | 0.9M | 0.5M | 0.4M | 1 | 0 |
| B2 round 3 | 36 | 3.9M | 0.9M | 1.1M | 1.0M | 1 | 0 |
| B2c gold + stability 1 and 2 | 31 | 2.4M | 1.9M | 0.7M | 0.6M | 3 | 0 |
| B3 group 1 (100 batches) | 105 | 9.6M | 8.0M | 2.3M | 1.8M | 1 | 0 |
| B3 group 2 (1,110 batches, with reissues) | 1,178 | 109.7M | 89.5M | 38.3M | 32.8M | 1 | 0 |
| B3 resend of the 6 exhausted batches | 14 | 1.5M | 0.4M | 0.4M | 0.4M | 1 | 0 |
| B3 halves, room ids (superseded) | 5 | 0.4M | 0.2M | 0.1M | 0.1M | 1 | 0 |
| B3 halves, fleet ids | 6 | 0.5M | 0.2M | 0.2M | 0.2M | 1 | 0 |
| **Total** | 1,573 | 139.6M | 106.7M | 44.6M | 38.2M | 30 | 87 |

Clearly wasted fleet work: 134 calls (round 1's 4 early tries and round 2's discarded first build), 7.6M prompt and 0.1M completion, 5% of the fleet's prompt. Round 1's 47 calls also hold 16 cut at max_tokens and 20 with no finish; only 3 returns were valid (diary 2026-10-11T18:39Z). B3 is 88% of all fleet tokens (prompt plus completion); reasoning is 86% of all completion.

## B4 blind sample readers (13 October 2026)

685 items in 48 packets (U 250, A 250, R 185), two readings per packet in each arm. Arms reported apart.

| Arm | Calls | Input | of which cached | Output | of which reasoning |
|---|---|---|---|---|---|
| DeepSeek V4.1 Flash, medium, via fleet.py (OpenRouter) | 106 (96 valid, 10 failed and reissued) | 9.6M | 7.5M | 2.7M | 2.1M |
| OpenAI gpt-6-astra, medium, via Codex on J's Mac | 98 logged (96 valid, 1 failed fleet.py's code check, 1 interrupted with no reply) | 9.07M | 0.51M | 0.55M | not visible |

Source: `out/_fleet_raw/B4/log.jsonl` and `out/_fleet_raw/B4-openai-astra/DONE` (OpenAI total 9,618,690 known tokens; the interrupted call's usage is unknown).
