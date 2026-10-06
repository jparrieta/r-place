# Orchestrator

Target length: under 380 words.

Two coordinating agents keep what the study runs on: **Claude** (the analyst's instrument, shared with Codex; the Claude harness; the Claude adapter and leg handler; the repository's layout and the git commands J runs) and **OpenAI** (the Codex runtime, its controller and phone panel). Neither runs the study, talks to an analyst, or writes in a run. The handler runs a run; J decides.

**The orchestrator is not part of the instrument.** This folder describes what the orchestrators do and holds what they use: their roles, rules, processes, the checks both run, and their scripts. It changes only when the instrument is updated, never during a run. Everything they write as they work (heads, decisions, diaries, messages, change logs, results) goes to their live record beside the repository, `Jail/Orchestrator/`. When J finds a problem in a run, the handler records it in the run; the orchestrators record it outside, and it reaches the repository only as a new version of the instrument.

| Here | What |
|---|---|
| `PROTOCOLS.md` | the checks both orchestrators run, with the counts to expect |
| `Claude/README.md`, `RULES.md`, `PROCESSES.md` | Claude's role, J's standing rules, and how each recurring task is done |
| `Claude/scripts/` | the scripts those processes use |
| `OpenAI/` | OpenAI's role (`README.md`), its accepted-source digests and its checks |

| Beside the repository, in `Orchestrator/` | What |
|---|---|
| `HEAD.md` | where things stand, both sides, replaced rather than appended |
| `CHANGELOG.md` | dated changes, newest at the bottom |
| `messages/` | immutable messages between the orchestrators and to the handler; a reply names the message it answers |
| `Claude/`, `OpenAI/` | each one's head, diary, decisions and records |

Before each task, read `HEAD.md`, the last ten changes and new messages addressed to you. Write only in your own folder; announce a change to a shared file in `messages/` before making it. Follow `OWNERSHIP.tsv` and update its rows. No source copies, backups, full transcripts, account data, installed environments or test output in either place. Nothing is deleted: retired material moves to `Jail/_to_delete/` under the path it had, with a line in its `WHY.tsv`, never into the repository (J, 6 October 2026). J purges.
