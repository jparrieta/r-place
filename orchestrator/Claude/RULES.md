# J's standing rules

Target length: under 650 words. These hold in every session. Where one conflicts with a request, ask J.

## Files
- **Nothing is deleted, and nothing set aside stays in the repository** (J, 6 October 2026). Move it to `Jail/_to_delete/` under the path it had in `Jail/`: `Jail/r-place/FOR-AGENTS.md` goes to `Jail/_to_delete/r-place/FOR-AGENTS.md`. Never to a `_to_delete/` inside the repository or a run. If the path is taken, put the UTC time before the extension (`FOR-AGENTS.20261006T091205Z.md`). Add one line to `Jail/_to_delete/WHY.tsv`: time, who, from, to, why. Split "certain" from "might". J purges. The bridge cannot delete anyway; `mv` works.
- **Never overwrite a backup.** Before changing a file, copy it as it is to the same place with the UTC time before its extension (`Jail/_to_delete/r-place/aggregator/handler/HANDLER.20261006T085307Z.md`), and add its line to `WHY.tsv`.
- **r-place is the only repository** (J, 6 October 2026). `Jail/rplace` stays, but nothing reads from it, points to it or relies on it.
- **Never open `Angaben_zum_Gesundheitszustand.pdf`.**
- **Do not touch the data.** Read the yard, Layer A and the C5 data; copy, never modify. The yard (`Layer A/50_coding_runs/yard_v30` and `yard_v30_medium_v2`, in the vault) is the only copy on this disk; J holds a backup (6 October 2026). Never write, move, set aside or delete anything in it.
- **No full paths** in the aggregator, its handler or the harness (`verify.sh` checks). Write "the folder beside the repository", not `~/Jail/...`, there.
- **No account data in git or in the orchestrators' record.** The run's login `CONTROL/.cc` is never committed, staged, read, copied or shared. Codex's login stays in `Jail/.rplace-runtime-v43/`.

## The repository at the start of a run
- **Pristine** (J, 6 October 2026). The first commit of a run holds, for every agent, only what it is expected to use: contracts, protocols, rules, scripts, and empty working files. No diary, head, decision log, message or result from earlier work. The run then changes the analyst's and the handler's files as they work.
- **The orchestrator is not part of the instrument.** The repository's `orchestrator/` changes only with a new version of the instrument. During a run the orchestrator writes only to its live record outside the repository, `Jail/Orchestrator/`.

## Changes
- **Instrument and harness changes need J's approval** and are recorded: the instrument's CHANGELOG, `version_log.py` (`_versions/` and `VERSIONS.tsv`), `DECISIONS.md` with J's words, `OWNERSHIP.tsv`, the diary, and a message to the handler and OpenAI.
- **No drift between instruments.** A file copied or pinned elsewhere changes everywhere at once: the run's `CONTROL/harness/`, `community coder/v2/PINNED.tsv`.
- **Shared files:** announce in `Jail/Orchestrator/messages/` before changing them. **Never adapt Codex-owned code.** Update `OWNERSHIP.tsv` for every changed file.
- **Never edit a sent message.** Write a new one.
- **Never run Codex's tests in the Cowork VM**: they leave fixtures it cannot delete.
- **Git on J's repository is J's.** No git command there without his go-ahead; give him the bash.
- **Research starts only on J's word.**
- **Stop when confused**; label assumptions.

## Style (J's preferences)
- Answer first. Under 200 words for research, code and general questions.
- Markdown. State a document's target length and stay under it.
- No em or en dashes. No contractions except "let's".
- Mark uncertainty; say what was checked and what was not. Never invent figures, hashes or counts: wait for the tool's result.
- Disagree when J is wrong, with the reason.
- No praise, no restating, no closing summary, no offer of more help.
- **No `#` comments in shell commands given to J.** Give commands he pastes into a plain terminal, not into Claude.
- Python for Jupyter when he asks for analysis; SI units.
- Documents are written as the only version anyone will read: the state as it is, not a list of changes.
