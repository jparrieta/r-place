# How the work is done

Target length: under 1,500 words. Paths are from the repository root, `Jail/r-place/`, unless named otherwise. `Orchestrator/` is the live record beside the repository, `Jail/Orchestrator/`.

## Where things are

- `aggregator/instrument/`: the analyst's instrument, v43, shared with Codex. `VERSIONS.tsv` and `_versions/` keep every version of its documents; `CHANGELOG-v37-to-v38.md` says why each changed. Platform files are generated (`aggregator/handler/claude/gen_platform.py`), never edited.
- `aggregator/handler/`: `HANDLER.md`, the handler's scripts and `paths.json`, `memory/` (the handler's, empty at a run's start: diary, `DECISIONS.tsv`, open items; the orchestrator does not write there), `claude/` (the harness; every file in it enters the run's fingerprint), `claude-adapter/` (the actor, the leg handler `legs.py`, branches, probes; outside the fingerprint), `codex/` (OpenAI's runtime and controller).
- `aggregator/input/`: coders/ (705 rooms), canvas/, raw/. Every run reads it.
- `aggregator/runs/claude-v43-1/`: the Claude run. `CONTROL/RUN.json` holds its fingerprint; `CONTROL/harness/` is the run's own copy of the harness.
- `coder/`: the case lead's instrument v32, the yard's handler, census, 14 example rooms, `lead-sessions/` (1.2 GB).
- `orchestrator/`: what the orchestrators use, unchanged during a run: `PROTOCOLS.md` (shared), `Claude/` (mine: README, RULES, this file, `scripts/`), `OpenAI/` (theirs).
- Beside the repository, in `Jail/`: `Orchestrator/` (the live record: `HEAD.md`, `CHANGELOG.md`, `messages/`, `Claude/` with my head, diary, decisions, next-instrument list and records, `OpenAI/`), `community coder/v2/` (the sibling contracts, below), `.rplace-runtime-v43/` (Codex's private state), `.rplace-claude-legs/` (the leg handler's lock and key, made by `serve`), `_to_delete/` (backups and set-aside files, each under the path it came from, with `WHY.tsv` and a README; `RULES.md`).
- Outside Jail: the yard (`Layer A/50_coding_runs/yard_v30`) and Layer A in the vault, needed only to add or refresh rooms; the yard's `_lead_sessions` (78 GiB by `du`, 6 October 2026), which Codex uses at D2: Codex runs the case aggregators and the labelers, and the Claude run only builds D2's packets and brief and reads the returns (J, 6 October 2026). The yard is the only copy on this disk; the Mac had 14 GiB free that day.

## Working through the bridge

- `device_bash` runs in a Linux VM on J's Mac (Python 3.10). Calls over about 45 s are risky; give long ones `timeout_ms` up to 180000. A background job dies when the call ends.
- `rm` is refused in connected folders; `mv` works. `sed -i` drops the exec bit: `chmod +x` after.
- To write a file onto the Mac: write it to a new folder under `/mnt/user-data/outputs/`, wait about 20 s, `device_commit_files` with `force: true`, then check its sha256 on the device and restore the exec bit if it was lost. Once, an older upload overwrote newer edits; the hash check catches that.
- `~/venv-test` has scipy (prepend `~/venv-test/bin` to PATH for `validate.py` and the verbs). `TMPDIR=~/tmp`.
- Never run Codex's tests here (`offline.py`, the runtime's unittest suites): they write fixtures into `Jail/.rplace-runtime-v43` and `Jail/`, which the VM cannot delete. OpenAI runs them on the Mac. OpenAI's `check_state.py` is read-only and safe here.
- `build.sh` runs here in place before a run's first leg. The live acceptance, the probes and `verify.sh` run on J's Mac: give J the commands.

## Tests, in order

1. Instrument: `python3 aggregator/instrument/tools/validate.py --self-test --summary` and `python3 aggregator/instrument/tools/tests/test_verbs.py` (both 0 failures; need scipy).
2. Platform files: `python3 aggregator/handler/claude/gen_platform.py --check`.
3. Harness: `bash orchestrator/Claude/scripts/harness_test_copy.sh .` here (it tests a copy in the VM's home, on a small store it makes from the tools' fixture; 80 checks), or on the Mac `bash aggregator/handler/claude/tests/run.sh aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT`.
4. Adapter and leg handler: `python3 aggregator/handler/claude-adapter/tests/test_adapter.py` and `tests/test_legs.py` (20 and 15).
5. OpenAI's source check: `python3 orchestrator/OpenAI/checks/check_state.py --corpus --fingerprint FP` (705 rooms, 115,388 codes, 7,844 themes; `passed: true`).
6. On the Mac, J: `bash verify.sh`; then, after any build, `bash aggregator/runs/claude-v43-1/CONTROL/harness/acceptance.sh` and `acceptance_v41.sh` (22 and 23, ALL CLEAR); after a CLI update, `python3 aggregator/handler/claude-adapter/probe_lifecycle.py --model claude-sonnet-5-5 --effort low` (14 checks). If acceptance says not logged in: `cd aggregator/runs/claude-v43-1 && CLAUDE_CONFIG_DIR="$PWD/CONTROL/.cc" claude`, `/login`, `/exit`.

## Rebuilding the run

Before the first leg only (`build.sh` refuses once `CONTROL/sessions.json` names a session), here or on the Mac:

```
bash aggregator/handler/claude/build.sh aggregator/runs/claude-v43-1
```

The login and the store are kept. Then J runs both acceptance scripts on the Mac. Record the new fingerprint in `Orchestrator/HEAD.md`, its `CHANGELOG.md`, `Orchestrator/Claude/_head.md`, and a message to the handler and to OpenAI in `Orchestrator/messages/`.

## Running legs

The handler's, not mine. J starts `legs.py serve` and `legs.py chat claude-v43-1`; the handler drives legs with `legs.py` (`aggregator/handler/claude-adapter/LEGS.md`, the `rplace-legs` skill). I do not open, close or talk to legs, and I never read or copy `CONTROL/.cc`.

## Changing the instrument or the harness

Only with J's approval. Then:
1. A backup of each file as it was, at its path under `Jail/_to_delete/` with the UTC time before its extension, and a line for each in `Jail/_to_delete/WHY.tsv` (`RULES.md`).
2. Edit. A harness file changes the fingerprint; rebuild the run if it has not begun, else copy the file into `CONTROL/harness/` too.
3. Tests above.
4. Record: an entry in `aggregator/instrument/CHANGELOG-v37-to-v38.md`, then from `aggregator/instrument/` `python3 tools/version_log.py --note "vNN.N (date): why" FILE...` (it copies each changed file to `_versions/` and adds its `VERSIONS.tsv` row); `OWNERSHIP.tsv` rows; in `Orchestrator/Claude/`, a row in `DECISIONS.md` with J's words and the diary line.
5. A message to the handler and to OpenAI in `Orchestrator/messages/`.

During a run, `orchestrator/` itself does not change: a problem found in a run is recorded outside, in `Orchestrator/`, and reaches the repository only as the next version of the instrument.

## Changing a shared or Codex file

1. A message in `Orchestrator/messages/` (UTC stamp, target length, what and why) before editing.
2. Edit a shared file; never adapt Codex-owned code. Record digests before and after (`Orchestrator/Claude/records/`).
3. Tests above. `OWNERSHIP.tsv` rows. An `Orchestrator/CHANGELOG.md` entry. Ask OpenAI to retest when its files are involved.
4. A file copied or pinned elsewhere changes everywhere at once: the run's `CONTROL/harness/` copy, and `community coder/v2/PINNED.tsv` (J: no drift between instruments).

## The sibling contracts (community coder/v2)

Beside the repository, `Jail/community coder/v2/` holds the contracts for the community coder's two siblings, written with Codex's coding handler: `room-model/CONTRACT.md` (one room), `field-model/CONTRACT.md` (r/place itself), `PROFILE.md` (files and IDs), `CROSSWALK.md` (against the global aggregator), and `PINNED.tsv` (the build lock). Codex reviews into `REVIEW-codex*.md`; I answer by editing the contracts, after a backup, and by writing a `PROMPT-coding-handler-*.md` note for J to paste into Codex's session. After every edit, check every pin:

```
cd ~/Jail && grep -v -e '^#' -e '^path' "community coder/v2/PINNED.tsv" | while IFS=$'\t' read -r p h u; do [ "$(shasum -a 256 "$p" | cut -d' ' -f1)" = "$h" ] || echo "MISMATCH $p"; done
```

## Moving or renaming paths

Fix code by hand with assertions, documents by a string map applied longest first (the 2 October map is `Orchestrator/Claude/scripts-retired/remap.py`). Then `scripts/links.py FILES...` for broken Markdown links, and the full-path check from `verify.sh`.

## Version snapshots

`scripts/snap.py OUT.tar.gz SRC NAME --prune a,b --only x,y --max MB`: a text-only archive of a state in its layout, with `_MANIFEST.tsv` (sha256 per file). Snapshots go to `rPlace/Layer A/60_aggregator/version-control/<vNN-date-label>/` with `_SOURCE.md`; the README there and `60_aggregator/README.md` get a row. Unpacked copies do not go in the vault.

## Before a push

Git commands on J's repositories are J's: give him the bash. `scripts/gitscope.sh REPO` (a bare probe repository in TMPDIR, so the repository's own `.git` is untouched) shows what the first commit would hold. GitHub: under 100 MB per file, under 2 GB per push; push the first time in two commits, `coder/lead-sessions/` second. `scripts/leadscan.sh coder/lead-sessions` counts credential-shaped strings (then inspect with values redacted). The first commit is pristine: every agent's contracts, protocols, rules and scripts, and empty working files.

## The scripts

Retired ones (the v41 merge, Codex's tests on Python 3.10, the 2 October path map) are in `Orchestrator/Claude/scripts-retired/`.

| Script | What it does |
|---|---|
| `gitscope.sh` | the first commit's files, sizes and suspicious names, under `.gitignore` |
| `leadscan.sh` | credential-shaped strings in the case-lead archives |
| `harness_test_copy.sh` | the harness tests in a copy in the VM's home |
| `links.py` | broken relative Markdown links |
| `snap.py` | a text-only snapshot with its manifest |

## Ending a turn of work

In `Orchestrator/Claude/`: a diary line, and `_head.md` replaced, not appended. A message in `Orchestrator/messages/` when OpenAI or the handler needs to know; a Project doc in claude.ai when the work is durable. Nothing in the repository.
