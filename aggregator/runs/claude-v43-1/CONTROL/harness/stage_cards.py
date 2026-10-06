#!/usr/bin/env python3
"""stage_cards.py RUN: write STAGE CARDS/, one card per stage for J: what the stage is for, the
lines to type in order (every leg, every dispatch), when to stop, what to read. Generated from
steps.tsv (beside this file in CONTROL/harness/), the notes below and DROPS/ORDER.tsv; never
edited by hand."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(HERE, "..", "tools"))
sys.path.insert(2, os.path.join(HERE, "..", "aggregator", "tools"))
sys.path.insert(3, os.path.join(HERE, "..", "..", "instrument", "tools"))   # aggregator/handler/claude beside aggregator/instrument (2026-10-02)   # the harness beside the instrument, in the handler's folder   # the instrument's copy, when build.sh runs this from there
import steps as S  # noqa: E402
TSV = next((p for p in (os.path.join(HERE, "steps.tsv"), os.path.join(HERE, "..", "tools", "steps.tsv"),
                         os.path.join(HERE, "..", "aggregator", "tools", "steps.tsv"),
                         os.path.join(HERE, "..", "..", "instrument", "tools", "steps.tsv")) if os.path.exists(p)), os.path.join(HERE, "steps.tsv"))

RUN = os.path.abspath(sys.argv[1])
H = "bash CONTROL/harness"

WHAT = {
 "A1": "Every room read through its forest: room notes, the lexicon, the analysed set.",
 "B1": "The third-order scheme, drawn across rooms in a seeded random order under the stopping rule, then tested to saturation.",
 "B2": "The pilot: fresh readers test the scheme; the scheme is frozen.",
 "B3": "The fleet: every second-order theme placed by two readers.",
 "B4": "Adjudication, the blind sample and the codebook frozen.",
 "C1": "Structuring: scheme v2 and the fourth-order themes, the first story of how the bundles work.",
 "C2": "The loop, with one reviewer before the closing passes.",
 "C3": "The model against the literature.",
 "C4": "The field: the model against a sealed model of r/place, where the rooms met.",
 "C5": "The account with three readers: the Gioia table, the dynamic model, the figure.",
 "D1": "The return, built: the handoff folder and the verdict packets.",
 "D2": "The labelers in Codex and the verdict fleet, then the check.",
 "D3": "Adjudication by element, the model frozen and re-read.",
 "D4": "The tree of forms from the adaptations.",
 "D5": "The branch accounts.",
 "D6": "The retelling: the model told again with its forms inside it.",
 "E1": "The audit: the run as only the logs can tell it, then the analyst's own account.",
 "E2": "The feedback: how the analyst was handled, and the instrument it would build next.",
}
# lines printed before a step's own line
BEFORE = {
 ("B1", "c"): "If the analyst paused at a check-in or at marker 3, read `00_GIVE-THE-AGENT/out/stopping-B1.md` and "
              "decide: `cd 00_GIVE-THE-AGENT && python3 tools/saturation.py decide --stage B1 continue|finish|stop "
              "--why \"<your words>\"` (continue only at the check-in), then open the next B1b leg or, when the walk "
              "has ended, B1c",
 ("B2", "b"): "`%s/dispatch.sh B2 --round K` (the readers of round K; your Keychain; the analyst is not running)" % H,
 ("B2", "d"): "`%s/dispatch.sh B2 --round gold`, then `--round stab-1` and `--round stab-2` (the gold and stability "
              "readers on the frozen scheme)" % H,
 ("B3", "b"): "`%s/dispatch.sh B3` (the readers; your Keychain; the analyst is not running)" % H,
 ("B4", "c"): "`%s/dispatch.sh B4` (the blind sample's readers)" % H,
 ("C2", "c"): "`%s/dispatch.sh C2` (the reviewer, on your subscription)" % H,
 ("C5", "c"): "`%s/dispatch.sh C5` (the three readers, on your subscription)" % H,
 ("D2", "a"): "`%s/dispatch.sh D2` (the verdict readers); give the adaptation handler in Codex "
              "`00_GIVE-THE-AGENT/out/handoff-D/HANDLER.md` and wait for `DROPS/D/DONE`" % H,
 ("D3", "b"): "Only if the analyst built a re-check (a D3a leg closed at packets-out): `%s/dispatch.sh D3` "
              "prints the re-check brief for Codex and sends the re-check's verdict packets; wait for "
              "`DROPS/D/recheck/DONE` and `out/_fleet_raw/D3v/DONE`; step.sh then runs ingest.py D --recheck" % H,
 ("E1", "a"): "Before E1 opens: `python3 check_quotes.py` in the handler's folder (the yard's path in paths.json) "
              "writes `run/DROPS/E1/quote-check-E1.json`, which the stage reads",
 ("E1", "d"): "`%s/dispatch.sh E1` (the reconstruction readers)" % H,
 ("E2", "a"): "Put the study's proposal, as it stands now, in `DROPS/E2/handling/proposal.md` "
              "(`design-note.md` is already there; replace it if the design changed). E2 refuses to open without both",
}


def leg_example(st, r):
    rep = r["repeat"]
    base = st + r["step"]
    if rep == "yes":
        return base + "-01", "%s-01, %s-02, ... as many as the work needs" % (base, base)
    if rep == "round":
        return base + "-r1", "%s-r1, %s-r2, ... one per pilot round" % (base, base)
    if rep == "optional":
        return base, "%s, or %s-01, %s-02, ... if split into batches" % (base, base, base)
    return base, None


def card(st, rows, arm):
    a = arm.get(st, {})
    name = rows[0]["stage_name"]
    L = ["# Stage %s. %s" % (st, name), "", WHAT.get(st, ""), "",
         "Analyst: `%s`, effort %s. %s" % (a.get("analyst"), a.get("effort"), ("Readers: `%s`, %s, %s per packet." % (
             a["readers"]["model"], "on your subscription" if a["readers"]["route"] == "cli" else "through the gateway",
             a["readers"]["n"])) if a.get("readers") else "No readers."), "",
         "## What you type, in order", "",
         "Every line is typed in Terminal, in the run folder. A leg opens Claude with its first message already sent; "
         "when the analyst has closed the leg and stopped, quit Claude (`/exit`) and type the close line. A leg id "
         "is the stage, the step letter and a count where the step repeats.", ""]
    for r in rows:
        if (st, r["step"]) in BEFORE:
            L.append("- " + BEFORE[(st, r["step"])])
        ex, many = leg_example(st, r)
        iv = {"end": "  *Interview point: the stage's last leg of this step closes at it.*",
              "mid": "  *Interview point, mid-stage.*"}.get(r["interview"], "")
        L.append("- **%s%s %s**: `%s/step.sh %s`, then `%s/close.sh %s`%s%s" % (
            st, r["step"], r["step_name"], H, ex, H, ex, ("  (legs %s)" % many) if many else "", iv))
    if any(r["interview"] in ("end", "mid") for r in rows):
        L += ["", "## Interview point", "",
              "A leg marked above closes with `--cut interview` and leaves a brief named after the leg, the stage, the "
              "step and the minute, in `00_GIVE-THE-AGENT/out/interview/`. After that leg's close, talk with the "
              "analyst in a fork run in a copy of its folder as the leg closed (you may add material; nothing reaches the run): `%s/interview.sh` (the last interview point) or `%s/interview.sh <leg>`. "
              "To answer later, write the reply file interview.sh names; the next leg reads it. The run goes on with "
              "the next `step.sh` whether or not you interview." % (H, H)]
    L += ["", "## Pausing", "", "To stop cleanly (the subscription week ending, or any reason): `%s/pause.sh`. "
          "The analyst stops at its next safe stop and closes with `done.sh %s --pause`; quit Claude and run the "
          "close line as usual. `close.sh` prints the leg to resume with (the same id with `-p2`); it picks up from "
          "the head and the diary. To stop at once instead: quit Claude, then `close.sh <leg> --force`." % (H, st)]
    L += ["", "A close that refuses says why; tell the handler. A stage is finished when `close.sh` prints "
          "`stage %s finished`." % st, "", "## If you want to read", "",
          "`00_GIVE-THE-AGENT/out/handback-%s.md` when the stage finishes; `out/_head.md` at any time." % st,
          "", "## The one rule", "", "Inside a leg, say nothing to the analyst beyond what the harness sends; "
          "questions it has go into its files, and the handler answers them there. Talk freely in an interview: "
          "it is a fork and never a leg.", ""]
    return "\n".join(L)


if __name__ == "__main__":
    table = S.table(TSV)
    arm = json.load(open(os.path.join(RUN, "CONTROL", "arm.json")))
    d = os.path.join(RUN, "STAGE CARDS")
    os.makedirs(d, exist_ok=True)
    n = 0
    for line in open(os.path.join(RUN, "DROPS", "ORDER.tsv")).read().splitlines()[1:]:
        st = line.split("\t")[0]
        rows = [r for r in table if r["stage"] == st]
        if not rows:
            continue
        open(os.path.join(d, "Stage %s. %s.md" % (st, rows[0]["stage_name"].replace(":", " -"))), "w").write(card(st, rows, arm))
        n += 1
    print("STAGE CARDS/: %d cards" % n)
