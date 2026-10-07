# Changes the handler made, to hand the orchestrator

Target length: under 1,200 words, kept current. J, 2026-10-06 23:37 Berlin: "make all changes in a list to hand the orchestrator at some point". One entry per change to the instrument or the harness, newest last, with what was tested and what was not. Proposals the handler only raised are listed apart.

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
- **Not done.** No commit of its own (the handler runs no git from Cowork): the change rode in the commit `close A1.A1b-16` (2026-10-06 22:08Z, pushed). `validate.py --self-test` could not run in the VM (no scipy: 36 failures, all from that); it does not touch the guard. The run's fingerprint (`CONTROL/RUN.json`) is not rebuilt: after the first leg `build.sh` refuses, and `CONTROL/harness/` is the run's.
- **Effect on the live run.** The hook reads the file at every tool call, so A1b-16 (opened 21:30:04Z) got the new guard mid-leg, and its close commits it. It only lets through quoted text the old guard refused, and blocks two forms the old guard let through.

### 2. Diary parts sorted by number (2026-10-07 00:41Z)

- **Ruling.** J, 02:38 Berlin: triage item 3, "ok".
- **Why.** `mem.py` sorted `out/diary/` parts by name, so `A1-10` came between `A1-1` and `A1-2`. `diary --last` read the end of `A1-9`, and `_diary_path` kept writing to `A1-10` without rolling over (956 lines, against about 1,500 words a part). `vlib.diary_lines` (the validator) and `probe.py` (the close-time probe, "the last next: line") had the same sort.
- **Change.** A numeric key in `mem.py` (`_part_key`, used by `_diary_path` and `_diary_lines`), in `vlib.py` `diary_lines` and in `probe.py`. Installed in `aggregator/instrument/tools/`, the run's `00_GIVE-THE-AGENT/tools/` and `CONTROL/harness/validation_tools/` (same bytes each); `version_log.py` rows in `VERSIONS.tsv`.
- **Tested.** Read-only against the run's diary: the last line is now A1c's (23:53:01Z), where it was A1b-12's (19:34:18Z); the next A1 line goes to `A1-11`. Not run: the instrument's tests and the validator self-test (no scipy in the Cowork VM).

### 3. README-store: hour 0 and the pre-open tests (2026-10-07)

- **Ruling.** J, 02:38 Berlin: "Canvas opens at 0. Reddit made some pre open tests before while closed".
- **Change.** One sentence added to "The clock" in `tools/build_store.py` (the README's source) and in the run's `package/store/README-store.md`: hour 0 is the canvas opening; the placement record also holds Reddit's tests before it, from about hour -16, while the canvas was closed. `DATA-manifest-canvas.md` left as it is (it agrees).

### 4. Bash allow rules (2026-10-07 00:43Z)

- **Ruling.** J, 02:38 Berlin: triage item 8, "allow yourself".
- **Change.** In `aggregator/handler/claude/settings.template.json` and the run's `CONTROL/settings.template.json`: allow `Bash(python3:*)`, `Bash(bash out/_analysis/:*)` and `grep`, `awk`, `sed`, `cut`, `head`, `tail`, `sort`, `uniq`, `wc`, `ls`, `cat`, `echo`, `printf`, `tr`. The sandbox, its denyWrite and the guard still apply; `step.sh` renders them into the next leg's settings.
- **Not verified.** Whether an allow rule lifts the CLI's own asks (comparison operators, loops); the next leg's refusal count will tell.

### 5. B1 stretch about 1 MB (2026-10-07)

- **Ruling.** J, 03:51 Berlin: "I think 1mb is fine. Keep two stretches still as stopping".
- **Change.** `stages/STAGE-B1-coding-third-order-scheme.md`, B1b: "about 3 MB" to "about 1 MB", with the dates; in the instrument and in the run's `DROPS/B1/stages/` (same bytes); `STAGES-full.md` regenerated; `VERSIONS.tsv` rows. The stopping rule is unchanged (two stretches in a row, each of at least twenty rooms, with no new third-order theme).
- **Consequence.** By file sizes (the handler's measure, not `mem.py room --size`) a 1 MB stretch holds about 8 rooms. The two-stretch rule is B1d's (the second pass); B1b stops by `saturation.py`'s rule, which counts rooms in words and does not depend on stretch size. Item 6 replaces B1d's rule.

### 6. B1d stops after thirty rooms in a row (2026-10-07)

- **Ruling.** J, 03:58 Berlin: "After 30 rooms in a row without new concepts" (read as: no new third-order theme).
- **Change.** B1d's stop in the stage card: "thirty rooms in a row of this pass have added no new third-order theme", in place of two stretches of at least twenty rooms each; the closing summary line to match; `checks/stage_B1.py`'s message to match (its test, "added no new", unchanged). Card in the instrument and `DROPS/B1/`; the check in the instrument, the run's `tools/checks/` and `CONTROL/harness/validation_tools/checks/` (copied from the instrument; not compared before the copy). `STAGES-full.md` regenerated; `VERSIONS.tsv` rows.
- **Not changed.** `saturation.py` (B1b's rule).

### 7. A close check on whole reads, for the A1 catch-up (installed 2026-10-07 02:04:24Z)

- **Ruling.** J, 04:01 Berlin: "Do the harness change" (the analyst's proposal in the A1c interview: compare lines served with the file's total at the close).
- **Change.** `checks/stage_A1.py`: `_check_catchup_reads`, called from `check()`. When the open leg (`.leg`) is A1b-20 or later, every room with a note line in that leg must have `mem.py case` and `mem.py brief` reads in the catch-up pass whose served spans cover the file (`_covered`), and covered before the note line; otherwise an error (`catchup:not-whole`, `catchup:late`). Block rooms (`#NN<TAB>sub` lines in `order-A1.txt`) with no note line in the leg get a warning (`catchup:pending`). Legs before A1b-20 and the self-test (no `.leg`) are untouched. Installed in the instrument, the run's `tools/checks/` and `CONTROL/harness/validation_tools/checks/` (same bytes); `VERSIONS.tsv` row.
- **Tested.** Against the run's records: A1b-20 and A1b-21 pass (0 errors); with babymetal's `case` reads cut to 10 lines in a copy, it reports one error. Not run: the validator self-test (no scipy in the VM); no planted defect added for it, since the self-test runs without a `.leg`.
- **What it cannot see.** Output piped through `head` or `cut` after `mem.py` served it whole (the A1 interview's second cause). The read log records what was served, not what was read.
- **For later stages.** The same comparison for B1 (each room's themes and concepts served whole) is not built.

### Not changed: the note hook's word count (triage 10)

- J said "fix yourself". On all 705 notes the hook's count (`len(t.split())`) equals `wc -w` (C locale, Linux); no note holds a non-ASCII space. The gap the analyst saw is not reproduced, so nothing was changed.

## Raised, not changed (the orchestrator's to propose to J)

- **Bash refusals in dontAsk mode** (`analysis/a1-refusals.md`; message `2026-10-06T12-29Z_from-handler_to-claude_a1a-refusals.md`): the run gives Bash no allow rule; calls with `==`, `<=`, `>=`, `===`, many loops and `awk` pipelines are refused. Options there.
- **A1a's six defects** (message `2026-10-06T13-17Z_from-handler_to-claude_a1a-defects.md`): store README (`collapsed`), onset fields not clipped to the window, `n_codes_coder`, concept reach.
- **The analyst's scratchpad root** is outside its allowed folder (one Read refused in A1a).

## 8. The handler's role (J, 7 October 2026, 08:56 Berlin)

HANDLER.md amended: after each close the handler checks substance, not only the validator (step 0), and the handler is in charge of changes to the instrument and the scripts, as amendments, with the most authority among the agents. The orchestrator is asked for advice (for example, B1's stopping rule) and the handler implements. Not yet committed: the next close's publish.sh commits it.

## 9. Writing rules are guides (J, 7 October 2026, 09:01 Berlin)

- **Change.** `pretool_guard.py --post` refuses a room note only for errors (`err`); warnings (`warn`: length over 350, quoting) return as advice through `additionalContext`, exit 0. In `handler/claude/` and the run's `CONTROL/harness/` (same bytes). Stage A1's note line now reads "about 350 words is a guide, not a limit", in the instrument, `DROPS/A1/stages/` and the analyst's `stages/`; `STAGES-full.md` regenerated; `VERSIONS.tsv` rows.
- **Tested.** By hand on a scratch copy: a 420-word note (advice, exit 0) and a placeholder (refused, exit 2). The harness test is owed on the Mac; it has no case for the note hook, and one should be added.
- **Why.** J: the notes are the analyst's, for its own later use; pass/fail rules stand; length and wording are its judgement, with J to ask. Across the catch-up so far, 145 notes were cut to fit 350 words.

## 10. B1d's stop tied to marker 1 (J, 7 October 2026, 09:23 Berlin: "continue as designed")

- **Change.** On your advice of 07:20Z, built as proposed, with one addition. `saturation.py`: marker 1 records `run_x`, `run_rooms`, `last_new_x`, `last_new_rooms`; `status` and `report` print them; a new verb `pass2` replays the second pass from `out/pass2-chosen-B1.txt` and `out/pass2-B1.jsonl` (state: no chosen list | chosen | beyond the chosen rooms | met | list ended; next room). A kind of the pass is a `kinds-B1.jsonl` line from a B1d leg, new when no earlier line names it, and belongs to the first pass-2 room recorded at or after its time. `mem.py reread <sub>` (B1d legs only) records a room; it refuses a non-chosen room while chosen ones are unread, an overflow room out of the seeded order, a room already recorded, and any room once the rule is met. Each line carries the chosen list as it stood, so a room taken off the list later is caught (`pass2:dropped`). `checks/stage_B1.py` `_check_pass2` at the last leg: `pass2:absent`, `pass2:short`, `pass2:dropped`. Card: B1d paragraph, outputs list, moments to log; `STAGES-full.md` regenerated.
- **The addition.** Your plan read B1d's rooms from `kinds-B1.jsonl`, but that file has a line only when a kind is met; a room read with nothing new leaves no trace there. Hence `pass2-B1.jsonl` and `mem.py reread`.
- **Tests.** `tools/tests/test_pass2.py`, 8 cases, in `run.sh`; two planted defects in the B1 self-test. Validator self-test 139 of 139 and the instrument's fixture run passed in the container; `test_pass2.py` passed on the device. The harness test is owed on the Mac.
- **Installed.** Instrument; the run's `00_GIVE-THE-AGENT/tools/`, `CONTROL/harness/validation_tools/`, `DROPS/B1/stages/` (B1 not yet handed over). `VERSIONS.tsv`, 7 rows. B1 has not begun, so no departure.
