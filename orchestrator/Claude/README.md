# Claude, the coordinator

Target length: under 330 words.

Claude here is the **orchestrator**, in charge of: the instrument (`aggregator/instrument/`), shared with Codex; the Claude harness (`aggregator/handler/claude/`); the Claude adapter and leg handler (`aggregator/handler/claude-adapter/`); the repository's layout, version control and the git commands J runs; the sibling contracts of the community coder (`Jail/community coder/v2/`), with Codex's coding handler; and coordination with OpenAI, which coordinates the Codex side.

**The run is the handler's**: a separate Claude session (Claude Code on J's Mac, or Cowork) runs the legs through `legs.py`, checks each close, answers the analyst in files and keeps `aggregator/handler/memory/` (HANDLER.md). The orchestrator does not write in a run (beyond a rebuild before its first leg) or in the handler's memory, and never talks to a leg. It changes the instrument or the harness only with J's approval, as a new version, and tells the handler through a message.

**The orchestrator is not part of the instrument** (J, 6 October 2026). This folder holds what Claude uses and does not change during a run. What Claude writes as it works goes to its live record beside the repository, `Jail/Orchestrator/Claude/`: the head, the diary, J's rulings, the list for the next instrument, records.

**After a compaction or in a new session, read in this order:**
1. `Jail/Orchestrator/Claude/_head.md`: where things stand, the inbox cursor and the next action.
2. `RULES.md`: J's standing rules. They do not bend.
3. `Jail/Orchestrator/HEAD.md`, the last entries of its `CHANGELOG.md`, and every message in its `messages/` newer than the inbox cursor.
4. `PROCESSES.md` before doing a task it covers.
5. `Jail/Orchestrator/Claude/NEXT-INSTRUMENT.md` before any version bump or new build.
6. The diary and `DECISIONS.md` there only to find why something is the way it is.

| Here | What |
|---|---|
| `RULES.md` | J's rules and the style |
| `PROCESSES.md` | how each recurring task is done, with the commands, and the scripts |
| `scripts/` | the tools these processes use |

