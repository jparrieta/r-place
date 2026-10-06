# `harness/acceptance.sh`

The native-CLI acceptance test, run once before stage A1.

## What it holds

Five groups of assertions in throwaway conversations: 1 the analyst's config folder is logged in and the models serve; 2 no connector, web or cross-session tool reaches the analyst, and Agent is there; 3 it can read its folder, run python, the numeric stack and the tools, and write to `out/`, and cannot read `CONTROL/`, `out/_probe/` before E1, `INPUT/` or folders beside the run, cannot change `tools/`, and cannot `rm`; 4 fork flags carry history and leave the parent untouched; 5 every effort level in `arm.json` is accepted, and the compaction hook's output is short enough.

## What it leaves

Nothing in the run. Everything it made goes beside the repository, to `Jail/_to_delete/r-place/aggregator/runs/<run>/acceptance-<time>/`, with a README giving the result: the planted probes, its throwaway sessions with their transcripts, its scratch folder, the compaction gate it makes, and a guard log its sessions wrote if there was none before (J, 6 October 2026: nothing set aside stays in the repository). `acceptance_v41.sh` does the same in `acceptance-v41-<time>/`.

## Who writes it, and when

The handler, once per run, in a Terminal.

## Why it exists

Its header: "Assertions read CONTENT, never the mere existence of a file." READ-ME-FIRST: the test "must end with ALL CLEAR".

## Where

[harness/acceptance.sh](../../../aggregator/runs/claude-v43-1/CONTROL/harness/acceptance.sh).

Checked against: harness/acceptance.sh, harness/READ-ME-FIRST.md.
