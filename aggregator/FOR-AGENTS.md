# For agents: the aggregator layer

The handler's protocol is [HANDLER.md](handler/HANDLER.md); its rules that do not bend hold for you too. The analyst's instrument is `instrument/`; the handler is `handler/` (the Claude harness in `handler/claude/`, the Codex controller in `handler/codex/`); the input every run reads is `input/`; each run is a folder in `runs/` (today `runs/claude-v43-1/`). Below, `RUN` is one of them.

- **Reading a run.** `RUN/00_GIVE-THE-AGENT/` is the analyst's folder: `package/` is its input, `out/` what it wrote. `RUN/CONTROL/` is the harness's. Stage pages under `Manual/stages/` summarise each closed leg.
- **Running legs.** The leg handler, `handler/claude-adapter/legs.py` ([LEGS.md](handler/claude-adapter/LEGS.md)), opens, runs and closes legs headless through the harness; only the principal investigator talks to a leg, through it.
- **Talking to a closed leg.** The command is on its stage page; [Manual/9-resuming.md](../Manual/9-resuming.md) explains every flag. It is read-only by construction.
- **Before the run**: the steps of HANDLER.md, "Before the run": paths (`paths.py`), rooms (`extract_legacy.py`, then `import_rooms.py`), canvas (`build_outcome.py ATLAS ROOMS.tsv OUT`, `build_canvas.py`), shelves, build (`handler/claude/build.sh`), acceptance (`RUN/CONTROL/harness/acceptance.sh` and `acceptance_v41.sh`), the leg handler's live check (`handler/claude-adapter/probe_lifecycle.py`), the first commit. For a scratch run outside the repository set `RPLACE_RUN` to its folder (or `run` in `paths.json`); its Manual is written beside the run folder, in `<run>/../Manual`.
- **Checks.** `bash handler/claude/tests/run.sh runs/claude-v43-1/00_GIVE-THE-AGENT` and `python3 instrument/tools/validate.py --self-test`; `bash ../verify.sh` runs both.
- **Changing anything in `instrument/` or `handler/claude/`** needs the principal investigator's approval and is recorded three ways (HANDLER.md, "Changing the instrument"). Harness files have a second copy in `RUN/CONTROL/harness/`.
- **Memory.** `handler/memory/diary.md` (one line per action), `handler/memory/DECISIONS.tsv`, `handler/memory/open-items.md`. Read them first; append, never rewrite.

## A problem we had (2026-09-29): a part that outlived its reason

On the morning of 29 September the stopping rule was built for A1 and B1. A1 gained a unit to count: each note listed "kinds", entries of a running file with ids K001 on, so that `saturation.py` could estimate how many kinds were still unseen. At midday stage A2 was removed. It had structured the reading, and the method review showed a random order was best for B1. A1's kinds stayed. They served the structured reading A2 stood for, and nothing needed them any more.

The cost came in the afternoon. Each audit found new questions about the kinds: when a kind is met, how a merge counts, whether a note re-lists old kinds. Every ruling fixed one symptom and opened the next. The kinds looked like they were falling apart, when they should not have been there at all. The PI removed them: A1 is reading only, and the stopping rule is B1's alone.

What to do:

- **When a stage or a step is removed, list what it made or needed in the other stages, and ask the PI about each item.** A2's removal moved its order to B1 but left A1's kinds behind.
- **When a feature keeps producing rulings, ask what it is for before ruling again.** Three rulings on one concept in an afternoon was the sign.
- **Count only what a later stage uses.** A figure nothing reads still has to be kept consistent, and that upkeep is the cost.
- The stopping rule's design is not in question. Leave it whole at B1 (J, 2026-09-29).
