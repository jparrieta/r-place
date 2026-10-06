# Changes the handler made, to hand the orchestrator

Target length: under 600 words, kept current. J, 2026-10-06 23:37 Berlin: "make all changes in a list to hand the orchestrator at some point". One entry per change to the instrument or the harness, newest last, with what was tested and what was not. Proposals the handler only raised are listed apart.

## Changes made

### 1. The tool guard skips quoted text (installed 2026-10-06 21:34:31Z)

- **Ruling.** J, 23:32 Berlin: "they should skip quoted text. add the amendment".
- **Why.** A1b-15, 21:21:17Z: `pretool_guard.py` refused `echo '{... "why": "... ops rm ..."}' >> out/leads-A1.jsonl` as a file delete, because the shell-word check `(^|[;&|\s(])(rm|rmdir|unlink)\s` ran over quoted text. The analyst reworded the lead to get past it.
- **Change.** In `aggregator/handler/claude/pretool_guard.py` and the run's copy `aggregator/runs/claude-v43-1/CONTROL/harness/pretool_guard.py` (same bytes): a new `deletes(cmd)`.
  - `rm`, `rmdir`, `unlink` count only outside quoted text (single and double quotes removed first).
  - Text quoted for a shell that runs it (`sh -c`, `bash -c`, `zsh -c`, `eval`) is still read.
  - Python's `shutil.rmtree` and `os.remove/unlink/rmdir(` are read everywhere, quoted or not, as before.
  - The shell word now also counts at the end of a command (`... | xargs rm`), and inside `bash -c "rm ..."`; the old guard missed both.
  - The other checks (read-only folders, tool-written files, the diary, `saturation.py decide`) are unchanged: they still read quoted text, because a quoted redirect target (`> "tools/x"`) must still be caught.
- **Tests added** to `aggregator/handler/claude/tests/run.sh`, after "the tool guard blocks rm": quoted `rm` passes; `bash -c "rm out/x"` is blocked.
- **Tested.** 21 hand cases against the old and new guard in a scratch folder in the Cowork VM: the new guard gets all 21 right; the old one blocked the quoted cases and missed `xargs rm`, `bash -c`, `sh -c`, `eval`. Harness test (`tests/run.sh` on the run's package and trees, in the VM): 49 of 82 checks ran, all ok, among them every tool-guard check and the two new ones; the VM shell stopped the script after about two minutes, so checks 50 to 82 (closes, interviews restored, fleet stages, validator imports, publication) did not run. **To do on the Mac: the full harness test and `validate.py --self-test`.** 
- **Not done.** No commit of its own (the handler runs no git from Cowork): the change rides in the next close's commit, `close A1.A1b-NN`. `validate.py --self-test` could not run in the VM (no scipy: 36 failures, all from that); it does not touch the guard. The run's fingerprint (`CONTROL/RUN.json`) is not rebuilt: after the first leg `build.sh` refuses, and `CONTROL/harness/` is the run's.
- **Effect on the live run.** The hook reads the file at every tool call, so A1b-16 (opened 21:30:04Z) got the new guard mid-leg, and its close commits it. It only lets through quoted text the old guard refused, and blocks two forms the old guard let through.

## Raised, not changed (the orchestrator's to propose to J)

- **Bash refusals in dontAsk mode** (`analysis/a1-refusals.md`; message `2026-10-06T12-29Z_from-handler_to-claude_a1a-refusals.md`): the run gives Bash no allow rule; calls with `==`, `<=`, `>=`, `===`, many loops and `awk` pipelines are refused. Options there.
- **A1a's six defects** (message `2026-10-06T13-17Z_from-handler_to-claude_a1a-defects.md`): store README (`collapsed`), onset fields not clipped to the window, `n_codes_coder`, concept reach.
- **The analyst's scratchpad root** is outside its allowed folder (one Read refused in A1a).
