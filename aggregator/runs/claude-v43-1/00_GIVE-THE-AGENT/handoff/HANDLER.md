# HANDLER. The adaptation handler's brief for stage D2.

You run the labelers. You are outside the analyst's run and you never read or write anything
in it except this folder and the drop folder.

1. **What you have.** `handoff-D/`: `RETURN-D.md`, `VOCABULARY.json`, `MODEL.md`, `LADDER.md`,
   `HANDLER.md`, and `tasks/<sub>/` for every room, each holding `TASK.md` and the room's
   documents. The folder is hashed; do not edit any file in it.
2. **How to run a labeler.** Fork the verified checkpoint of the lead that coded this exact room snapshot.
   Retain its conversation and filesystem, then deliver the return task in a separate folder.
   Use the recorded model and effort. Missing or mismatched history blocks this room; never
   substitute a fresh reader. D3 rechecks continue the room's D2 return checkpoint. Record the model,
   the session id and the number of attempts in `DROPS/D/<sub>/run.json`
   (`{"model": "...", "session": "...", "attempts": 1}`); ingest counts a room with more than one
   attempt as reissued.
3. **Order.** Rooms by size ascending (`items_in_window` in `tasks/index.tsv`), so that failures
   surface early on small rooms.
4. **Where returns go.** `DROPS/D/<sub>/model-D.md` and `DROPS/D/<sub>/adaptations.jsonl`,
   plus `run.json`. Nothing else.
5. **Validation and repair.** After each room, from the run's root folder (the one holding
   `out/`, `DROPS/` and `tools/`), run `python3 tools/ingest.py D --check <sub>` (at the re-check,
   add `--recheck`); it names any failing rule. Ask the same resumed session to repair with the failing rule named. Preserve interrupted
   stores; mechanical failures do not consume scientific retries. Completion comes before any limit: keep returning rooms; mark a room
   `unreturned` in `DROPS/D/UNRETURNED.tsv` with the reason only when you cannot return it.
6. **What never to do.** Do not open `out/`, the analyst's files, other rooms' folders from a
   labeler, or the vocabulary for editing. Do not merge rooms or share a session between rooms.
   Do not summarise the model for a labeler; it reads `MODEL.md` itself.
7. **When done.** Write `DROPS/D/DONE` with the count of rooms returned and unreturned. The
   analyst's run resumes from there.

The re-check (stage D3) uses the same brief with `handoff-D/recheck/` and `DROPS/D/recheck/`.
