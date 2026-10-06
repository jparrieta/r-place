#!/usr/bin/env python3
"""gen_manual.py RUN: write the Manual, a wiki of Markdown pages that GitHub renders with working
links, from the run's own records. Regenerated at every close and every interview (publish.sh);
never edited by hand.

Where: the repository root is the folder holding aggregator/ (RUN is aggregator/runs/<run>, restructure
2026-10-02; the older aggregator-handler/run is still read); the Manual is <root>/Manual/. Outside those layouts
it goes to RUN/../Manual.

    Manual/README.md          the run at a glance, how to start a run, how to talk to any leg
    Manual/stages/<ST>.md     per stage: its card, its file, its handback, and every leg closed:
                              when, how it closed, its brief, its transcript, the command that
                              reopens it as a read-only fork you can talk to, and its interviews

Reads CONTROL/snapshots/INDEX.tsv, CONTROL/interviews.tsv, CONTROL/steps.tsv (or tools/), the
analyst's out/_closes/*.closed, out/_transcripts/, out/interview/, out/handback-*.md.
"""
import csv, glob, json, os, sys

RUN = os.path.abspath(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(HERE, "..", "tools"))
sys.path.insert(2, os.path.join(HERE, "..", "aggregator", "tools"))   # the harness beside the instrument, in the handler's folder
sys.path.insert(3, os.path.join(HERE, "..", "..", "instrument", "tools"))   # aggregator/handler/claude beside aggregator/instrument
import steps as S  # noqa: E402

AG = os.path.join(RUN, "00_GIVE-THE-AGENT")
C = os.path.join(RUN, "CONTROL")
parent = os.path.dirname(RUN)
if os.path.basename(parent) == "runs" and os.path.basename(os.path.dirname(parent)) == "aggregator":
    AGG = os.path.dirname(parent)                     # <repository>/aggregator/runs/<run> (restructure 2026-10-02)
    ROOT = os.path.dirname(AGG)
    INS = os.path.join(AGG, "instrument")
    HANDLER = os.path.join(AGG, "handler")
    HARNESS = os.path.join(HANDLER, "claude")
    INPUTD = os.path.join(AGG, "input")
    CODER = os.path.join(ROOT, "coder")
else:                                                 # the older layout, aggregator-handler/run, or a run elsewhere
    AGG = parent
    ROOT = os.path.dirname(parent) if os.path.basename(parent) == "aggregator-handler" else parent
    INS = os.path.join(parent, "aggregator")
    HANDLER = parent
    HARNESS = os.path.join(parent, "harness")
    INPUTD = os.path.join(RUN, "INPUT")
    CODER = os.path.join(ROOT, "yard-handler")
MAN = os.path.join(ROOT, "Manual")
TSV = next((p for p in (os.path.join(HERE, "steps.tsv"), os.path.join(HERE, "..", "tools", "steps.tsv"),
                         os.path.join(HERE, "..", "aggregator", "tools", "steps.tsv"),
                         os.path.join(HERE, "..", "..", "instrument", "tools", "steps.tsv")) if os.path.exists(p)), os.path.join(HERE, "steps.tsv"))


def rel(target, frm):
    return os.path.relpath(target, os.path.dirname(frm)).replace(os.sep, "/").replace(" ", "%20")


def repo_path(p):
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


def rows(p):
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def closed_cut(nn, leg):
    p = os.path.join(AG, "out", "_closes", "%s-%s.closed" % (nn, leg))
    if not os.path.exists(p):
        return None
    last = [l for l in open(p, encoding="utf-8").read().splitlines() if l.strip()]
    return last[-1].split()[1] if last and len(last[-1].split()) > 1 else "close"


def talk_command(transcript_rel, model, effort=None):
    """A command that reopens the leg as a read-only fork, from the repository root, on any account.
    Read-only by its own flags: plan mode, and the tools that run commands or write are disallowed,
    so it does not rest on the run's hooks (whose paths are the author's machine's)."""
    return ("cd \"$(git rev-parse --show-toplevel)/%s\" && claude --resume \"$PWD/%s\" --fork-session "
            "--permission-mode plan --model %s%s --strict-mcp-config "
            "--disallowedTools Bash Write Edit MultiEdit NotebookEdit"
            % (repo_path(AG), transcript_rel, model, " --effort %s" % effort if effort else ""))


def arm_of(arm, st, leg):
    """The leg's model and effort as the launch took them: the stage's entry, then the leg's override."""
    ent = dict(arm.get(st) or {})
    ent.update(((arm.get(st) or {}).get("legs") or {}).get(leg) or {})
    return ent.get("analyst") or "claude-opus-5-5", ent.get("effort")


def contract_rows():
    """Stage -> (model, produces) from the contract's stage table (section 4), for the stage pages."""
    out = {}
    for p in (os.path.join(AG, "CONTRACT-aggregator.md"), os.path.join(INS, "CONTRACT-aggregator.md")):
        if os.path.exists(p):
            for l in open(p, encoding="utf-8"):
                f = [x.strip() for x in l.strip().strip("|").split("|")]
                if len(f) == 5 and f[0].strip("*") and f[0].strip("*")[0] in "ABCDE" and len(f[0].strip("*")) == 2:
                    out[f[0].strip("*")] = (f[3], f[4])
            break
    return out


def main():
    table = S.table(TSV)
    stages = S.stages(table)
    snaps = rows(os.path.join(C, "snapshots", "INDEX.tsv"))
    ivs = []
    ip = os.path.join(C, "interviews.tsv")
    if os.path.exists(ip):
        for l in open(ip, encoding="utf-8"):
            f = l.rstrip("\n").split("\t")
            if len(f) >= 4:
                ivs.append({"t": f[0], "label": f[1], "sid": f[2], "fork": f[3]})
    try:
        arm = json.load(open(os.path.join(C, "arm.json")))
    except (OSError, ValueError):
        arm = {}
    try:
        version = json.load(open(os.path.join(C, "RUN.json"))).get("instrument_version") or "v43"
    except (OSError, ValueError):
        version = "v43"
    order = [l.split("\t")[0] for l in open(os.path.join(RUN, "DROPS", "ORDER.tsv")).read().splitlines()[1:]] \
        if os.path.exists(os.path.join(RUN, "DROPS", "ORDER.tsv")) else stages
    os.makedirs(os.path.join(MAN, "stages"), exist_ok=True)
    purposes = contract_rows()
    # the Manual's other pages are written in Manual/ itself; this script writes only the front page and stages/
    status = {}
    for st in stages:
        page = os.path.join(MAN, "stages", "%s.md" % st)
        srows = [r for r in table if r["stage"] == st]
        name = srows[0]["stage_name"]
        legs = [r for r in snaps if r.get("label", "").split(".")[0] == st]
        finished = os.path.exists(os.path.join(C, "stage-state", st, "FINISHED"))
        status[st] = "finished" if finished else ("%d leg%s closed" % (len(legs), "" if len(legs) == 1 else "s") if legs else "not started")
        L = ["# Stage %s. %s" % (st, name), "", "[Back to the Manual](%s)" % rel(os.path.join(MAN, "README.md"), page), ""]
        if st in purposes:
            L += ["**What it produces:** %s. **Model:** %s. (From the contract's stage table, section 4.)" % (
                purposes[st][1].rstrip("."), purposes[st][0]), ""]
        card = glob.glob(os.path.join(RUN, "STAGE CARDS", "Stage %s.*.md" % st))
        sf = glob.glob(os.path.join(RUN, "DROPS", st, "stages", "STAGE-%s-*.md" % st)) or \
            glob.glob(os.path.join(INS, "stages", "STAGE-%s-*.md" % st))
        hb = os.path.join(AG, "out", "handback-%s.md" % st)
        L.append("Status: **%s**. " % status[st] + " · ".join(x for x in (
            "[the card](%s)" % rel(card[0], page) if card else "",
            "[the stage file](%s)" % rel(sf[0], page) if sf else "",
            "[the handback](%s)" % rel(hb, page) if os.path.exists(hb) else "") if x))
        L += ["", "Steps: " + "; ".join("`%s%s` %s%s" % (st, r["step"], r["step_name"],
                                                         " (interview)" if r["interview"] in ("end", "mid") else "")
                                        for r in srows), ""]
        if not legs:
            L += ["No leg of this stage has closed yet. Once one has, it appears here with its transcript and the "
                  "command to talk with the analyst as it was at that close ([what the command does](%s))." % rel(
                      os.path.join(MAN, "9-resuming.md"), page), ""]
        for r in legs:
            label = r["label"]
            leg = label.split(".", 1)[1]
            model, effort = arm_of(arm, st, leg)
            try:
                lbl = "%s · %s" % (leg, S.parse(leg, table)["step_name"])
            except ValueError:
                lbl = leg
            cut = closed_cut(st, leg) or "-"
            L += ["## %s" % lbl, "",
                  "Closed %s; %s; %s out files; tokens in %s, out %s (summed over every turn of the leg)." % (
                      r.get("closed_utc", "?"), {"interview": "an interview point", "pause": "paused at a safe stop",
                                                  "packets-out": "closed at packets-out", "close": "closed"}.get(cut, "cut " + cut),
                      r.get("out_files", "?"), r.get("tokens_in", "?"), r.get("tokens_out", "?")), ""]
            links = []
            for b in sorted(glob.glob(os.path.join(AG, "out", "interview", "%s_*.md" % leg))):
                links.append("[%s](%s)" % ("the reply" if b.endswith("-reply.md") else "the brief", rel(b, page)))
            snapd = os.path.join(C, "snapshots", label)
            if os.path.isdir(snapd):
                links.append("[the checkpoint](%s)" % rel(snapd, page))
            tr = sorted(glob.glob(os.path.join(AG, "out", "_transcripts", "leg-%s-*.jsonl" % label)))
            if tr:
                links.append("[the transcript](%s)" % rel(tr[-1], page))
            if links:
                L += [" · ".join(links), ""]
            if tr:
                L += ["Talk with the analyst as it was at the end of this leg (a read-only fork; your account's usage; "
                      "the transcript in the repository is not changed; [what this command does](%s)):" % rel(os.path.join(MAN, "9-resuming.md"), page),
                      "", "```bash", talk_command(os.path.relpath(tr[-1], AG).replace(os.sep, "/"), model, effort), "```", ""]
            for iv in [i for i in ivs if i["label"] == label]:
                it = os.path.join(RUN, "interviews", "%s__%s.jsonl" % (label, iv["fork"]))
                L.append("- Interview %s: %s" % (iv["t"], "[transcript](%s)" % rel(it, page) if os.path.exists(it)
                                                   else "fork %s (transcript not archived)" % iv["fork"]))
                if os.path.exists(it):
                    L += ["", "  ```bash", "  " + talk_command(os.path.relpath(it, AG).replace(os.sep, "/"), model, effort), "  ```"]
            L.append("")
        open(page, "w", encoding="utf-8").write("\n".join(L) + "\n")
    idx = os.path.join(MAN, "README.md")
    L = ["# r/place: the Manual", "",
         "This repository holds a study of how communities organized on Reddit's r/place in 2017: the data, the "
         "instrument that coded each community (the coder), the instrument that builds a model across all of them "
         "(the aggregator), and the run of the aggregator, instrument %s, whose record grows here stage by stage. The stage "
         "table below says how far it has got; until a stage is finished, this repository offers a method and its "
         "evidence trail, not findings. Read in this order:" % version, "",
         "1. [Introduction](1-introduction.md): what the project aims to do, and how this Manual is laid out. Reviewing the "
         "method? Start with 10.",
         "2. [r/place and the data](2-rplace.md): the event, what we hold, what the data let us see, and a worked "
         "example (Armenia and the Dutch), down to one thread and its codes.",
         "3. [How it was built](3-how-it-was-built.md): why each kind of file came to exist.",
         "4. [The coder](4-the-coder.md) and 5. [the aggregator](5-the-aggregator.md): each instrument top down.",
         "6. [The handlers](6-the-handlers.md): who runs the agents, their files, their memory, how sessions are saved.",
         "7. [Tool usage](7-tool-usage.md): which tools the agents use, and which almost never.",
         "8. [The v37 run](8-the-v37-run.md): the previous aggregator run.",
         "9. [Talking with a leg, and continuing a run](9-resuming.md): what the talk command does, piece by piece, "
         "and what it can touch on your machine.",
         "10. [For reviewers](10-for-reviewers.md): the tiers against Gioia's, which model did each step, the "
         "departures the method names, and how to check one room yourself.", "",
         "Reference: [every kind of file](files/README.md), [how the aggregator remembers](memory/aggregator.md), "
         "[how the coder lead remembers](memory/coder-lead.md), the [glossary](glossary.md), "
         "[requirements and data](requirements-and-data.md) and [data and collection](data-and-collection.md).", "",
         "The population and the evidence: [the census](census.md), from 1,473 artworks to the communities the study "
         "counts; [trace one claim](trace-a-claim.md), from a case account down to the Reddit comment; and "
         "[the numbers](numbers.md), every count that moves, regenerated from the files at every close.", "",
         "Each page's first line names its kind: a tutorial to learn by doing, a how-to for a task, reference to look "
         "up, or explanation of why.", "",
         "The run below is generated from its records at every close (`CONTROL/harness/gen_manual.py`); do not edit "
         "this page by hand.", "",
         "## The run", "", "| stage | name | status |", "|---|---|---|"]
    for st in order:
        nm = next((r["stage_name"] for r in table if r["stage"] == st), "?")
        L.append("| [%s](stages/%s.md) | %s | %s |" % (st, st, nm, status.get(st, "?")))
    L += ["", "## The repository", "",
          "Two layers are the instrument: [`aggregator/`](%s) holds everything to run the aggregator "
          "(the analyst's instrument in `instrument/`, the handler in `handler/` with the Claude harness in `claude/` "
          "and the Codex runtime in `codex/`, the shared input in `input/`, and one folder per run in `runs/`), and "
          "[`coder/`](%s) everything to code communities (the case lead's instrument in `instrument/v32/`, the "
          "scheduler's contract, runbooks and tools in `handler/`, the census, and the example rooms). "
          "[`data/`](%s) holds how to get every piece of data, one folder per store, and [`archive/`](%s) earlier versions "
          "of the instruments." % (
              rel(os.path.join(HANDLER, "HANDLER.md"), idx), rel(os.path.join(CODER, "README.md"), idx),
              rel(os.path.join(ROOT, "data", "README.md"), idx), rel(os.path.join(ROOT, "archive"), idx)),
          "", "## What every file is, and why", "",
          "- [Every kind of file](files/README.md): the aggregator's and the coder's, each with what it holds, who "
          "writes it and when, why it exists, and a link to a real one.",
          "- How each side remembers: [the aggregator](memory/aggregator.md), [the coder lead](memory/coder-lead.md).",
          "- [The handler's protocol and scripts](files/handler/README.md): what whoever runs the study must do around "
          "the analyst, and the tools to do it.",
          "- The coding yard, ready to fill, with the case lead's instrument v32 and the fourteen coded rooms of "
          "the Armenia and Dutch example (twelve with their case lead's saved session), is in [`%s`](%s)." % (repo_path(CODER),
                                          rel(os.path.join(CODER, "README.md"), idx))]
    L += ["", "## Talk with the analyst at any leg", "",
          "Each closed leg on a stage page carries a command. Copy it into a terminal (macOS, Linux or WSL) inside a "
          "clone of this repository. It opens the leg's own conversation as a read-only fork: the analyst remembers "
          "everything it did up to that close and can open files to answer you; it cannot run commands or write. The "
          "fork is a new session on your own account and your own usage; nothing in the repository changes. No "
          "command appears until a leg has closed.", "",
          "You need Claude Code installed and logged in (`claude` once). The fork does not need the run's harness or "
          "python. Downloaded as a zip rather than cloned: replace `$(git rev-parse "
          "--show-toplevel)` with the folder you unzipped to. [Talking with a leg](9-resuming.md) explains every part of the "
          "command, the files it opens, what it cannot do on your machine, and how to check it before you run it.", "",
          "## Start a run of your own", "",
          "The analyst's instrument is in [`%s`](%s), the harness that runs it in [`%s`](%s), and the handler's "
          "protocol in [HANDLER.md](%s)." % (repo_path(INS), rel(os.path.join(INS, "CONTRACT-aggregator.md"), idx),
                                            repo_path(HARNESS), rel(os.path.join(HARNESS, "READ-ME-FIRST.md"), idx),
                                            rel(os.path.join(HANDLER, "HANDLER.md"), idx)), "",
          "Build it outside your clone. Built inside, its first close would regenerate this Manual over the published "
          "one and commit and push to your clone's remote (`publish.sh` commits whatever repository the run sits in).", "",
          "```bash", "REPO=\"$(git rev-parse --show-toplevel)\"; mkdir -p ~/runs/MYRUN",
          "cp -R \"$REPO/%s\" ~/runs/input         # the coders' files and the canvas, joined at build" % repo_path(INPUTD),
          "bash \"$REPO/%s/build.sh\" ~/runs/MYRUN --input-root ~/runs/input --input ~/runs/input/coders" % repo_path(HARNESS),
          "cd ~/runs/MYRUN && CLAUDE_CONFIG_DIR=\"$PWD/CONTROL/.cc\" claude   # log the run's own Claude in once, then /exit",
          "bash CONTROL/harness/acceptance.sh          # must end ALL CLEAR",
          "```", "", "Then follow `STAGE CARDS/`, one card per stage, in order. What you need first (Python, packages, "
          "keys, what the readers cost and where their packets go) is on [requirements and data](requirements-and-data.md); "
          "what each script does when it runs is on [talking with a leg, and continuing a run](9-resuming.md).", "",
          "## What is where", "",
          "- [`%s/READ-ME-FIRST.md`](%s): the handler's guide to the run" % (repo_path(RUN), rel(os.path.join(RUN, "READ-ME-FIRST.md"), idx)),
          "- [`%s`](%s): the analyst's folder, with everything it wrote in `out/`" % (repo_path(AG), rel(AG, idx)),
          "- [`%s`](%s): the harness, the checkpoints and the records" % (repo_path(C), rel(C, idx)),
          "- [`%s`](%s): the handler's protocol, its scripts, the harness and the Codex runtime" % (repo_path(HANDLER), rel(os.path.join(HANDLER, "HANDLER.md"), idx)),
          "- [`%s`](%s): the coder layer: the case lead's instrument, the scheduler's handler, the census and the rooms" % (
              repo_path(CODER), rel(os.path.join(CODER, "README.md"), idx)),
          "- [`%s`](%s): every earlier version of the instruments, in one archive" % ("archive", rel(os.path.join(ROOT, "archive"), idx)),
          ""]
    open(idx, "w", encoding="utf-8").write("\n".join(L) + "\n")
    numbers()
    print("Manual: %s (%d stage pages)" % (MAN, len(stages)))
    html()


def numbers():
    """Manual/numbers.md: the counts that move, each read from its file at generation time, with the file's date."""
    import datetime
    page = os.path.join(MAN, "numbers.md")

    def src(p):
        if not os.path.exists(p):
            return "absent"
        d = datetime.datetime.fromtimestamp(os.path.getmtime(p), datetime.timezone.utc).strftime("%Y-%m-%d")
        return "[`%s`](%s), %s" % (repo_path(p), rel(p, page), d)

    def lines(p):
        return sum(1 for l in open(p, encoding="utf-8") if l.strip()) if os.path.exists(p) else None

    def csvrows(p, delim=","):
        if not os.path.exists(p):
            return []
        with open(p, encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f, delimiter=delim))

    T = [("Figure", "Value", "From")]
    cen = os.path.join(CODER, "census", "MASTER-census.csv")
    cr = csvrows(cen)
    pop = {r["sub"] for r in cr if r.get("handable") == "1"}
    if cr:
        T.append(("communities with a venue record", "{:,}".format(len(cr)), src(cen)))
        T.append(("the population (`handable` = 1)", "{:,}".format(len(pop)), src(cen)))
        dis = {}
        for r in cr:
            dis[r["disposition"]] = dis.get(r["disposition"], 0) + 1
        T.append(("by disposition", ", ".join("%s %d" % kv for kv in sorted(dis.items(), key=lambda kv: -kv[1])), src(cen)))
    rt = os.path.join(INPUTD, "coders", "ROOMS.tsv")
    rooms = [r["sub"] for r in csvrows(rt, "\t")]
    T.append(("rooms in the v38 frame", "{:,}".format(len(rooms)), src(rt)))
    if cr:
        out = sorted(set(rooms) - pop)
        T.append(("frame rooms outside the population", "%d%s" % (len(out), (": " + ", ".join(out)) if out else ""), src(rt)))
    st = os.path.join(AG, "package", "store")
    for f, what in (("codes.jsonl", "first-order codes in the store"), ("themes.jsonl", "second-order themes in the store"),
                    ("threads.jsonl", "threads in the store"), ("transitions.jsonl", "transitions in the store"),
                    ("neighbours.jsonl", "neighbour pairs in the store")):
        n = lines(os.path.join(st, f))
        if n is not None:
            T.append((what, "{:,}".format(n), src(os.path.join(st, f))))
    cv = os.path.join(INPUTD, "canvas")
    n = lines(os.path.join(cv, "artworks.jsonl"))
    if n is not None:
        T.append(("atlas artworks", "{:,}".format(n), src(os.path.join(cv, "artworks.jsonl"))))
    px = csvrows(os.path.join(cv, "pixels.csv"))
    if px:
        T.append(("hourly pixel rows, and rooms they cover", "{:,} rows, {:,} rooms".format(len(px), len({r["sub"] for r in px})),
                  src(os.path.join(cv, "pixels.csv"))))
    act = os.path.join(RUN, "DROPS", "D4", "data", "activity-week-before.csv")
    ar = csvrows(act)
    if ar:
        T.append(("rooms in stage D4's activity table", "{:,}".format(len(ar)), src(act)))
    L = ["# The numbers", "", "*Kind of page: reference, generated by `gen_manual.py` at every close; do not edit by hand.*", "",
         "Counts the study quotes that change as coding goes on. Each is read from its file when this page is written; "
         "the date is the file's. Quote a figure from here with its file and date, or read the file.", "",
         "| %s | %s | %s |" % T[0], "|---|---:|---|"]
    L += ["| %s | %s | %s |" % r for r in T[1:]]
    open(page, "w", encoding="utf-8").write("\n".join(L) + "\n")


HTML_CSS = """body{max-width:52rem;margin:2rem auto;padding:0 1rem;font:16px/1.55 -apple-system,Helvetica,Arial,sans-serif;color:#1d1d1f;background:#fff}
a{color:#0b57d0}code,pre{font:13px/1.45 Menlo,Consolas,monospace;background:#f4f4f5;border-radius:4px}
code{padding:.1em .3em}pre{padding:.8em;overflow-x:auto}pre code{padding:0;background:none}
table{border-collapse:collapse;display:block;overflow-x:auto}th,td{border:1px solid #d4d4d8;padding:.3em .6em;vertical-align:top}
h1,h2,h3{line-height:1.25}nav{font-size:14px;margin-bottom:1.5rem;color:#555}
@media (prefers-color-scheme:dark){body{color:#e4e4e7;background:#18181b}a{color:#8ab4f8}code,pre{background:#27272a}th,td{border-color:#3f3f46}nav{color:#a1a1aa}}
"""


def html():
    """Manual-html/, beside Manual/: every page of the Manual as HTML, rendered by pandoc (GitHub
    Markdown, GitHub's heading anchors). A link to a page of the Manual points to its HTML twin
    (README becomes index.html); a link out of the Manual is kept, and works because Manual-html/
    sits at the same depth as Manual/. Without pandoc it says so and writes nothing."""
    import re, shutil, subprocess
    pandoc = shutil.which("pandoc")
    out = os.path.join(os.path.dirname(MAN), "Manual-html")
    if not pandoc:
        print("Manual-html: not written; pandoc is not installed (brew install pandoc)")
        return
    link = re.compile(r"(\]\()([^)\s#]+?\.md)(#[^)\s]*)?(\))")

    def twin(mdpath):
        r = os.path.relpath(mdpath, MAN)
        base = os.path.basename(r)
        r = os.path.join(os.path.dirname(r), "index.html" if base == "README.md" else base[:-3] + ".html")
        return os.path.join(out, r)
    import tempfile
    fd, head = tempfile.mkstemp(suffix=".html")      # the nav bar pandoc puts before each body
    os.close(fd)
    n, failed = 0, []
    # the Codex side publishes its own pages (aggregator/handler/codex/runtime/manual.py): the cards in
    # Manual/openai-stages/, OPENAI-MODELS.md and INSTRUMENT-v43.md, and their HTML twins; never rewritten here
    codex_pages = {"OPENAI-MODELS.md"} | {f for f in os.listdir(MAN) if f.startswith("INSTRUMENT-v")}
    for d, ds, fs in os.walk(MAN):
        ds[:] = [x for x in ds if not x.startswith(".") and x != "openai-stages"]
        for f in fs:
            if not f.endswith(".md") or (d == MAN and f in codex_pages):
                continue
            src = os.path.join(d, f)
            dst = twin(src)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            txt = open(src, encoding="utf-8").read()

            def fix(m):
                tgt = os.path.normpath(os.path.join(d, m.group(2)))
                if os.path.commonpath([tgt, MAN]) != MAN:
                    return m.group(0)                       # out of the Manual: kept as it is
                return m.group(1) + os.path.relpath(twin(tgt), os.path.dirname(dst)) + (m.group(3) or "") + m.group(4)
            txt = link.sub(fix, txt)
            title = next((l[2:].strip() for l in txt.splitlines() if l.startswith("# ")), f[:-3])
            css = os.path.relpath(os.path.join(out, "manual.css"), os.path.dirname(dst))
            home = os.path.relpath(os.path.join(out, "index.html"), os.path.dirname(dst))
            before = '<nav><a href="%s">The Manual</a> &middot; <a href="%s">Markdown source</a></nav>' % (
                home, os.path.relpath(src, os.path.dirname(dst)))
            with open(head, "w", encoding="utf-8") as h:
                h.write(before)
            r = subprocess.run([pandoc, "-f", "gfm", "-t", "html5", "--standalone", "--css", css,
                                "--metadata", "pagetitle=" + title, "-B", head, "-o", dst],
                               input=txt, capture_output=True, text=True)
            if r.returncode:
                failed.append("%s: %s" % (os.path.relpath(src, MAN), r.stderr.strip()[:120]))
            else:
                n += 1
    os.remove(head)                                   # the system temp file, not a file of the study
    open(os.path.join(out, "manual.css"), "w", encoding="utf-8").write(HTML_CSS)
    print("Manual-html: %s (%d pages%s)" % (out, n, "; failed: " + "; ".join(failed[:5]) if failed else ""))


main()
