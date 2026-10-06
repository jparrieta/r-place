# A1: why the analyst's tool calls are refused

Target length: under 250 words. Handler analysis, 2026-10-06; full note to the orchestrator in `Orchestrator/messages/2026-10-06T12-29Z_from-handler_to-claude_a1a-refusals.md`.

- The run's settings give Bash no allow rule; mode `dontAsk`; sandbox on, `allowUnsandboxedCommands: false`. A Bash call runs only if the CLI approves it as sandboxed; anything it would ask about is refused (`decision_reason_type: "mode"`), and J is never asked.
- In A1a all six refused Bash calls held `==`, `<=`, `>=` or `===`; none that held them passed. Later refusals in A1b are mostly `for` loops and `awk`/`sed` pipelines. Mechanism not checked against the CLI's code.
- One Read was refused (`outside_reads_blocked`): a file in the CLI scratchpad's root, outside the allowed slug folder.
- Counts per leg are in `diary.md`: 0 to 6 per leg, the analyst worked around each. No `guard.log` through A1b-13.
- Risk J named: the refusal texts ("don't ask mode", "ask the user ... /add-dir") could make the analyst think it cannot reach J. No such line seen through A1b-13; QA1-001 shows `mem.py ask` works.
