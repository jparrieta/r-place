# OpenAI runtime supplement

This file governs runtime operations in the OpenAI migration. Scientific stage rules, evidence standards, reader counts, stopping rules and return schemas remain in force.

The analyst runs on GPT-6 Astra. Exact effort by stage and step comes from `harness/arm.json`. Routine packet readers use GPT-6 Sol medium. D2 and D3 resume the original case leads on their recorded model and effort; no fresh labeler or model substitution is allowed. C2 and C5 reviewers use GPT-6 Astra high. Names and effort in older stage prose are superseded by that manifest. No model or provider fallback is allowed.

The shell starts in `out/`. Use `cd ..` before the existing instrument commands. Inputs, instrument scripts and delivered stage cards are read-only. Write scientific work in `out/`. `RUN.json` is the one writable metadata file in the workspace root. The controller writes `.stage`, `.leg`, `.session` and `.stagefile`.

Every ordinary leg forks the preceding completed native checkpoint, retaining its conversation and filesystem. Controller deliveries are added with an inventory record. The head, current stage and diary orient continued work; they are not a replacement for native history. Missing checkpoints block progression. Interview forks remain separate from the run.

The investigator may talk with you while work runs. Record substantive interventions in the diary, with their effect on the work. A separate interview fork changes only its own files. Handler discussion does not enter your context unless explicitly delivered.

Save `out/_head.md` and the diary as you work. Check `out/PAUSE` at safe boundaries. On a pause request, log the working hypothesis and next action with `mem.py`, then run `bash tools/done.sh STAGE --pause`. To close normally, use `done.sh` and the cut required by the stage. Stop after the leg.

Closing with `--cut packets-out` requests dispatch. The controller validates and archives the leg, then runs the declared independent readers. You do not execute `fleet.py`, choose reader identities, change the arm or inspect other readers. The check leg begins only after validated returns arrive. Transport, capacity and runtime failures retain their native stores and are not coding defects.

The controller, outside your permissions, holds native transcripts, recall probes and future drops. Those audit records are delivered at E1. Model access and a compatible runtime are required to resume; a checkpoint is not a frozen inference process.
