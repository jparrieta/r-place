# Tool usage

*Kind of page: reference: counts, and where they stop.*

Which tools the agents called, and which they barely touched. The counts come from one file of tallies made from transcripts; this page reads them and says where they stop.

## Coder side

Source: 12 sample rooms, their case lead and fleet transcripts, 82 files. The file counts commands issued, by script and subcommand. It does not say which 12 rooms, which instrument version each ran, or how a command line was split into counts. In all, 61 script names and 5,935 commands.

The instrument's own tools, 5,348 of the 5,935:

| command | count |
|---|---:|
| `read.py corpus` | 2,782 |
| `cite.py coder` | 854 |
| `close_run.py` | 319 |
| `fleet.py dispatch` | 299 |
| `fleet.py collect` | 224 |
| `read.py` (no subcommand) | 208 |
| `tree_builder.py` | 137 |
| `audit_fleet.py` | 127 |
| `fleet.py consolidate` | 122 |
| `fleet.py plan` | 112 |
| `fleet.py redispatch` | 80 |
| `cite.py` (no subcommand) | 48 |
| `read.py coder` | 30 |
| `emit.py close` | 3 |
| `emit.py` (no subcommand) | 3 |

Scripts the agents wrote themselves, 587 commands over 46 names:

| group | names and counts |
|---|---|
| case lead helpers, `_lead_` prefix (13 names, 133) | `_lead_times.py` 57, `_lead_emit_themes.py` 15, `_lead_themes.py` 15, `_lead_counter_codes.py` 9, `_lead_citations.py` 9, `_lead_theme_step.py` 7, and seven more at 3 each |
| recording and coding helpers (32 names, 320) | `record_codes.py` 54, `code_batch.py` 42, `record_slice.py` 34, `code_slice.py` 26, `pointer_batch.py` 22, `record_pointers.py` 20, `pointers.py` 14, `emit_codes.py` 14, `record_dispositions.py` 12, `_work_emit.py` 10, `cite_batch.py` 8, and 21 more at 6 or fewer |
| `_scheduler_preflight.py` | 134 |

### Reading the coder counts

Reading dominates. `read.py corpus` alone is 47 per cent of all commands, and `cite.py coder` another 14 per cent. The fleet cycle (plan, dispatch, collect, consolidate, redispatch) shows up in every step, with 80 redispatches against 299 dispatches.

The agents wrote many helper scripts of their own. The case lead's `_lead_` scripts are sanctioned: the [case lead's contract](files/coder/contract-case-lead.md) says a helper script goes in the run directory "under a name beginning `_lead_`" and is not deleted. The other 32 are not named anywhere in the instrument. Their names (`record_codes.py`, `code_batch.py`, `record_pointers.py`, `record_dispositions.py`, `emit_codes.py`) point at the recording step: coders wrapped the recording of codes, pointers and thread dispositions in their own batch scripts. That suggests the official tools did not fit how the coders wanted to record, one call at a time. The counts cannot say why.

`emit.py`, the recording tool, appears only six times by name. One reading: `emit` is a Python API (`from emit import Emit`), and the contract has the coder call it from Python, so a command line would name the coder's own script, not `emit.py`. On that reading, many of the helper scripts above are how `emit` was called. The tally does not record imports, so this is not settled.

`_scheduler_preflight.py` is not an agent's helper. The yard's [codex_coder.py](../coder/handler/tools/codex_coder.py) copies its own [coder_preflight.py](../coder/handler/tools/coder_preflight.py) into each fleet batch under that name, and its prompt tells the fleet coder to run it before its final reply and to finish only when it prints PREFLIGHT PASSED. Its 134 runs are fleet coders checking their own work.

## Aggregator side

Source: the v37 run by a Sonnet analyst, the `mem.py` read logs of stages 01 to 17. These are v37's stage numbers, the older numbering, not v38's A1 to E2.

| verb | calls |
|---|---:|
| `theme` | 11,886 |
| `codes` | 2,210 |
| `room` | 1,661 |
| `forest` | 304 |
| `when` | 302 |
| `note` | 65 |
| `after` | 16 |
| `where` | 11 |
| `pairs` | 10 |
| `shelf` | 2 |
| `brief` | 1 |

### Reading the aggregator counts

Eleven verbs were used, 16,468 calls in all. The v37 `mem.py` kept in `_v37-source/tools/` offers eleven verbs, these same eleven, so every verb offered was used at least once. Use was lopsided: `theme` alone took 72 per cent of calls, and `theme`, `codes` and `room` together 96 per cent. The verbs that read across rooms (`where`, `pairs`, `after`) had 37 calls between them. `shelf`, the way into the literature, was called twice.

The logs cover `mem.py` only. Calls to `cite_case.py`, direct file reads and helper subagents are not in these counts.

## What no count covers

**Coder instrument v32.** `newrun.py`, `newbrief.py`, `read_brief.py`, `cut_window_v32.py`, `render_corpus_v32.py` and `render_openings_v32.py` build a run or a brief when the yard's tools set up a room; none appears in the counts. No brief writer's transcript is in the sample, so `read_brief.py`'s use is unmeasured. The yard's tools (`room.py`, `codex_lead.py`, `coding_queue.py`, `start_yard_lead.py`, the archive tools) are the handler's and appear in no count.

**Aggregator since v38.** No run of the v38 design has passed stage A1 (claude-v41-1 and claude-v42-1 stopped there when the instrument changed). The verbs new since v38 have not run past A1: `case`, `canvas`, `neighbours`, `compare`, `themes`, `facts`, `notes`, `progress`, `scheme`, `log`, `diary`, `mint`, `place`, `unplace`, `adjudicate`, `adaptations`, `rooms`, `contrast`, `finding`, `findings`, `question`, `contract`, `table`, `view`, `wiki`, `diff-scheme`, `diff-model` ([mem.py](files/aggregator/tool-mem-py.md), [new verbs](files/aggregator/tool-new-verbs-md.md)). Nor have the v38 tools beside it: `cite.py`, `validate.py`, `gen_views.py`, `links.py`, `probe.py`, `distance.py`, `handoff.py`, `ingest.py`, `rebuild.py`, `relations.py`, `packets.py`, `done.sh`. [TOOLS-STATUS.md](../aggregator/instrument/tools/TOOLS-STATUS.md) says which are tested on a fixture and which on the real store.

## What a proper analysis would need

- The list of the 12 rooms, and a sample drawn by a stated rule, with brief writers in it.
- The counting rule written down: what counts as a command, how pipes and chained commands split.
- Imports as well as command names, so `emit` calls made through helper scripts are counted.
- The source of each helper script, read, to say what each did that the official tools did not.
- Counts per role (lead, coder), per room size and per branch, not pooled.
- For v37, the `cite_case.py` log and the helper subagents beside `mem.py`, and counts per stage.
- For v38, the same tallies once a run exists, read against the stage files that ask for each verb.
