# The handler's folder

`aggregator/handler/` holds what the handler of a run needs beyond the harness: its protocol, and the scripts it runs before and around the analyst's work. The harness (`step.sh`, `close.sh`, `dispatch.sh` and the rest) runs each leg, typed by the PI or driven by the leg handler below; the scripts here the handler runs itself.

**Start with [HANDLER.md](../../../aggregator/handler/HANDLER.md)**: who decides what, the rules that do not bend, how the handler remembers across sessions, its duties before and during the run, and how the instrument is changed. The coder side's handler has its own contract, [CONTRACT-scheduler.md](../coder/contract-scheduler.md).

## The scripts

Every script finds the repository's own folders from where it sits. Sources outside the repository come from [paths.py](../../../aggregator/handler/paths.py): set them once in `aggregator/handler/paths.json` (copy `paths.example.json`), or as `RPLACE_<KEY>` in the environment. `python3 aggregator/handler/paths.py` lists every key, its value and whether it exists.

| Script | When | What it reads | What it writes |
|---|---|---|---|
| [paths.py](../../../aggregator/handler/paths.py) | first | `paths.json`, the environment | nothing; prints where each source is |
| [extract_legacy.py](../../../aggregator/handler/extract_legacy.py) | before the build, once | the batch archives of rooms coded before the yard (`layer_a`) | each room's coder output, as written, into `aggregator/handler/_work/legacy/` |
| [import_rooms.py](../../../aggregator/handler/import_rooms.py) | before the build; again when rooms finish | the yard's verified rooms (`yard_rooms`), `aggregator/handler/_work/legacy/`, the coder-version table (`layer_a`) | `aggregator/input/coders/rooms/<sub>/` in the one layout every room has; `forests` re-renders every forest with one tree builder |
| [build_outcome.py](../../../aggregator/handler/build_outcome.py) | before the build | the placeAtlas 2017 file, `ROOMS.tsv` | `case_facts_outcome.jsonl`: six canvas fields per room (entries, area, centre, ring, artwork, source) |
| [build_canvas.py](../../../aggregator/handler/build_canvas.py) | before the build | the pixel record per artwork (`c5_data`), the hourly series (`hourly_pixels`, from `data/pixels-hourly/`) | `aggregator/input/canvas/`: `artworks.jsonl` and `pixels.csv` |
| [check_quotes.py](../../../aggregator/handler/check_quotes.py) | before stage E1 | a seeded sample of rooms and the record each coder read (`yard_rooms`, `aggregator/handler/_work/legacy/`) | `RUN/DROPS/E1/quote-check-E1.json`, which E1 reads |
| [gather_collection.py](../../../aggregator/handler/gather_collection.py) | when the collection code changes | the layers' code folders, given on the command line | a folder you name with `INVENTORY.tsv` and `CANDIDATES.md` |
| [bundle_history.py](../../../aggregator/handler/bundle_history.py) | once, then frozen | earlier instrument folders, given on the command line | `archive/instrument-history.tar.gz` and its manifest |

## The leg handler and the Claude adapter

`aggregator/handler/claude-adapter/` runs the analyst's legs headless through the harness and lets the PI talk to any leg ([LEGS.md](../../../aggregator/handler/claude-adapter/LEGS.md), [README.md](../../../aggregator/handler/claude-adapter/README.md)). It sits beside the harness, outside the run's fingerprint.

| File | What it does |
|---|---|
| [legs.py](../../../aggregator/handler/claude-adapter/legs.py) | `serve` on the Mac owns the sessions; `open`, `close`, `run`, `status`, `wait`, `chat`, `say`, `answer`, `interview`, `pause`, `stop`, and the branch commands |
| [actor.py](../../../aggregator/handler/claude-adapter/actor.py) | one leg or interview as an actor: prepare, one headless turn, messages mid-turn, save, the close through `close.sh` |
| [stream.py](../../../aggregator/handler/claude-adapter/stream.py), [inbox_hook.py](../../../aggregator/handler/claude-adapter/inbox_hook.py) | the CLI's stream turned into events; the hook that hands the PI's words to the analyst beside its next tool result |
| [branches.py](../../../aggregator/handler/claude-adapter/branches.py) | analysis branches: a new run from one verified close, on its own Git branch |
| [probe.py](../../../aggregator/handler/claude-adapter/probe.py), [probe_lifecycle.py](../../../aggregator/handler/claude-adapter/probe_lifecycle.py) | live checks of the CLI and of the actor, in a synthetic run |

Two more live with what they serve: [shelves/make_meta.py](../../../aggregator/instrument/shelves/make_meta.py) writes a metadata page for every shelved work, from Crossref and the PDFs; [tools/version_log.py](../../../aggregator/instrument/tools/version_log.py) keeps every earlier version of an instrument file before a change lands.

## Why a handler has its own files

The analyst is fenced: it sees one folder, cannot reach the web or the handler's files, and forgets everything between legs except what it wrote. Everything around it, from assembling the rooms to checking quotes before the audit, is the handler's, and a run is only as reproducible as that work. Until 26 September 2026 the handler's scripts sat among its working files, with paths fixed to one machine, and its duties were spread across notes. They are here now, so another team's handler, on another account, starts from the same protocol and the same scripts.
