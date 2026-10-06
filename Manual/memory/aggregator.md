# How the aggregator remembers

*Kind of page: reference.*

The analyst holds nothing between legs except what is on disk: "the file, not your recollection, is what the run trusts" (the contract). Each part links to its file's page.

## A fresh session per leg

Every leg is a new Claude session. [step.sh](../files/aggregator/harness-step-sh.md) writes the leg's first message and [launch.sh](../files/aggregator/harness-launch-sh.md) starts `claude` with a new session id and auto memory switched off, "no memory carried between legs". What carries the work is the startup packet that [AGENT.md](../files/aggregator/agent-md.md) and [CLAUDE.md](../files/aggregator/claude-md.md) name: the head, the stage file, the last five diary entries, and `validate.py --open NN`. Nothing else is read by default.

## The head

[_head.md](../files/aggregator/out-head-md.md) is the narrative of the argument, at most 3,000 words, read first at every leg and rewritten at every close and before every cut. [done.sh](../files/aggregator/tool-done-sh.md) keeps a leg open when the head runs over 3,200 words, and [links.py](../files/aggregator/tool-links-py.md) fails the next launch when an id in it does not resolve.

## The diary

[The diary](../files/aggregator/out-diary.md) is the record under the head. It is written only through `mem.py log`, stamped with the time and the leg, in parts of 1,500 words. Each line has a kind: opened, dropped, merged, split, kept, move, abductive, question, comparison, note, helper, minted, placed, unplaced, pause, or one a stage file names. Rule 20: a diary written at the close from memory "is not a diary." A leg reads its tail or greps it by id; E1 computes over it.

## Read logs and the verbs

Every call to [mem.py](../files/aggregator/tool-mem-py.md) and [cite.py](../files/aggregator/tool-cite-py.md) leaves a line in [the read logs](../files/aggregator/out-read-logs.md). Rule 1: where the analyst's account of its reading and the log disagree, the log is right. The verbs serve reading one page at a time, generated [views](../files/aggregator/out-views.md) and [wiki pages](../files/aggregator/out-wiki.md) included. The [room notes](../files/aggregator/out-rooms-notes.md) written at A1 are the run's prior, queried one at a time and never read as a list.

## The recall probe at close

After `done.sh`, [close.sh](../files/aggregator/harness-close-sh.md) asks five questions in a fork of the leg's session, with tools disallowed: the method question, the open distinctions, the last three rooms opened, what changed and why, the next comparison. [probe.py](../files/aggregator/tool-probe-py.md) scores the answers against the questions, the read log and the history files,; [_probe/](../files/aggregator/out-probe.md) keeps them. A miss the head or the diary answers is a note; a miss neither answers is a defect.

## Snaps and checkpoints

[snap.py](../files/aggregator/tool-snap-py.md) hashes every file in `out/` under a name, once. `close.sh` takes one at every close; each categorization move gets one too, so a reviewer can see the state before and after it ([_snap/](../files/aggregator/out-snap.md)). `close.sh` then publishes a checkpoint of the folder and the transcript, committed once.

## Compaction

A long leg will compact unseen. CLAUDE.md tells the compactor what to keep. The hook [after_compact.sh](../files/aggregator/harness-after-compact-sh.md) then has the analyst re-read the head and the stage file, read the diary's tail, reconcile the two, and log that it did.

## Pauses

[pause.sh](../files/aggregator/harness-pause-sh.md) writes `.pause`. At the next safe stop the analyst logs its working hypothesis and the next room or item as a `pause` line and closes with `done.sh NN --pause`, which refuses without that line. The next leg (`-p2`) picks up from the head and the diary.

## Interview forks and transcripts

At eleven interview points a leg ends with a brief, and [interview.sh](../files/aggregator/harness-interview-sh.md) opens a read-only fork of that session. Nothing said there enters the run unless a reply file comes back, which the next leg reads before its first write. `interview.sh` copies the fork's transcript beside the run, and `close.sh` copies each leg's transcript into [_transcripts/](../files/aggregator/out-transcripts.md). Session files in the run's config folder are kept for 36,500 days ([.claude/settings.json](../files/aggregator/claude-settings-json.md)).

## What the analyst cannot see before E1

`_probe/` and `_transcripts/` are closed to the analyst until stage E1, by the permission rules and the sandbox and not only by the stage file. `_snap/` holds hashes only and stays open throughout. Until its stage is handed over, the analyst also has no later stage file and no later shelf ([stages/](../files/aggregator/stages-folder.md), [shelves/](../files/aggregator/shelves-folder.md)).

Checked against: CONTRACT-aggregator.md, STANDING-INSTRUCTIONS.md §2, CLAUDE.md, AGENT.md, tools/mem.py, tools/done.sh, tools/probe.py, tools/snap.py, harness/*.sh, harness/protocol_guard.py, harness/settings.template.json, stages/STAGE-E1-formalizing-audit.md.
