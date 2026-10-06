# `harness/interview.sh`

Talks with the analyst at an interview point, in a folder of its own restored from that leg's checkpoint.

## What it holds

`interview.sh [LEG | NN.LEG | --list]`. It finds the closed interview point (default the last), checks its checkpoint is committed, records the fork in `CONTROL/interviews.tsv`, and has `protocol_guard.py interview` restore the leg's checkpoint: the analyst's folder, exactly as it stood at the close, into `interview-workspaces/<label>__<fork>/`, and the leg's sessions into a Claude project of the interview's own (`projects/iv-<fork>`). The copy's settings shut the live folder and every other interview's copy, and carry no hooks. It names the brief and the reply file, and opens `claude --resume <session> --fork-session` in the copy, with the line "This is an interview, not a leg." The analyst may read and, when asked, write; you may add files to the copy. Nothing reaches the live run, and no interview reuses another's folder (J, 29 September 2026). Afterwards it copies the fork's transcript to `interviews/<label>__<fork>.jsonl` beside the run and calls `publish.sh`; `.gitignore` keeps the transcript out of git unless the principal investigator commits it.

## Who writes it, and when

The principal investigator, after `close.sh` of a leg that ended with `--cut interview`. From the leg handler's chat, `legs.py interview` opens the same kind of fork (a copy of the saved folder, the leg's sessions in a project of its own, a row in `CONTROL/interviews.tsv`), and leaves its transcript in the run's Claude folder (`CONTROL/.cc/projects/iv-<fork>/`, not committed); both kinds reach the analyst at stage E2a.

## Why it exists

STANDING §2: "nothing said there enters the run unless it comes back as a reply", the brief's name with `-reply` added, which the next leg reads before its first write and answers under rule 13.

## Where

[harness/interview.sh](../../../aggregator/runs/claude-v43-1/CONTROL/harness/interview.sh).

Checked against: harness/interview.sh, STANDING-INSTRUCTIONS.md §2, harness/step.sh.
