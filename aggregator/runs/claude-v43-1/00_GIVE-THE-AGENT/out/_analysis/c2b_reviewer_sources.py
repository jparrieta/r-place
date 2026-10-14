#!/usr/bin/env python3
"""C2b, the reviewer's build (stage C2 section 6): write the pages the one reviewer packet is made of, into
out/_analysis/c2b/, and print their sizes against the 50 KB ceiling. packets.py files then joins them.

The pages, in the order the packet serves them:
  0-instruction.md     the reviewer's instruction verbatim (stage C2 section 6), what the packet holds, which
                       sections of model-p3.md are served and which are not, the served sha256, how to return
  model-p3-sections.md the chosen sections of out/model-p3.md, verbatim, in the file's order
  story-p3.md          out/model/story-p3.md, whole (passed to packets.py as it stands, not copied)
  criterion.md         the criterion paragraph of notes-C2.md, verbatim
  tiers.md             the fourth-order themes and dimensions, rendered from fourth/fourth.jsonl, dimensions.jsonl
                       and scheme_v2.jsonl (third-order names), with the criterion for a fourth-order theme quoted
                       from stage C2 section 2
  verbs.md             the read verbs a reviewer with the run's tools may use, room always --no-canvas

Nothing else of the analyst's is served: no room note, no finding, no prior, no other notes (stage C2 section 6).

    python3 out/_analysis/c2b_reviewer_sources.py [--write] [--omit "<heading>;<heading>"] [--no-opening]
                                                  [--no-questions]

--omit drops the named '## ' sections of model-p3.md (by heading prefix); --no-opening drops the file's opening
block above its first '## ' heading; --no-questions drops the dimensions' questions from tiers.md.
"""
import argparse, hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DEST = os.path.join(OUT, "_analysis", "c2b")
CEILING = 50 * 1024
MODEL = os.path.join(OUT, "model-p3.md")
STORY = os.path.join(OUT, "model", "story-p3.md")

INSTRUCTION = ("*Find errors: a quote that does not show what it is said to show, a contradiction, a count that "
               "cannot be right, a loop no room runs the whole way round, an arrow whose instance does not show the "
               "order claimed. Separately, propose one partition of the third-order themes into fourth-order themes "
               "that meets the criterion you were given and differs from the analyst's, with what holds each "
               "together. A disagreement is never a verdict: your reading decides nothing.*")
T4_CRITERION = ("A fourth-order theme is a named group of third-order themes. No number is set for you. The count is "
                "whatever the material carries: enough that each answers a question no member answers alone, few "
                "enough that each is a step up in abstraction and not a rename of its members.")


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def sections(text):
    """[(heading or None, body)] split at '## ' headings; the title block comes first with heading None."""
    parts = re.split(r"(?m)^(## .*)$", text)
    out = [(None, parts[0])]
    for i in range(1, len(parts), 2):
        out.append((parts[i], parts[i + 1]))
    return out


ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
ap.add_argument("--omit", default="")
ap.add_argument("--no-opening", action="store_true")
ap.add_argument("--no-questions", action="store_true")
a = ap.parse_args()
omit = [x.strip() for x in a.omit.split(";") if x.strip()]

mtext = open(MODEL, encoding="utf-8").read()
secs = sections(mtext)
served, dropped = [], []
for h, body in secs:
    name = (h or "").lstrip("# ").strip()
    if h is None and a.no_opening:
        dropped.append("the opening above the first section (what pass 3 added, where the counts come from)")
    elif h is not None and any(name.startswith(o) for o in omit):
        dropped.append(name)
    else:
        served.append((h, body))
if a.no_opening:
    title = secs[0][1].strip().split("\n")[0]
    served.insert(0, (None, title + "\n\n"))
model_served = "".join((h + body) if h else body for h, body in served)
served_names = [(h or "").lstrip("# ").strip() for h, _ in served if h]

notes = open(os.path.join(OUT, "notes-C2.md"), encoding="utf-8").read()
m = re.search(r"(?ms)^## The criterion, written before pass 1[^\n]*\n(.*?)(?=^## )", notes)
if not m:
    sys.exit("the criterion paragraph was not found in notes-C2.md")
criterion = "# The criterion, written before pass 1\n\n" + m.group(1).strip() + "\n"

S = dict((r["id"], r) for r in jl(os.path.join(OUT, "scheme_v2.jsonl")))
T4 = jl(os.path.join(OUT, "fourth", "fourth.jsonl"))
D = jl(os.path.join(OUT, "dimensions.jsonl"))
t4 = dict((r["id"], r) for r in T4)
placed = set(x for r in T4 for x in r["members"])
L = ["# The tiers: fourth-order themes and dimensions", "",
     "From `fourth/fourth.jsonl`, `dimensions.jsonl` and `scheme_v2.jsonl`, by script: each dimension%s, its "
     "fourth-order themes (`*`: no standing element ties to it) and their third-order members: %d third-order "
     "themes, %d fourth-order, %d dimensions." % ("" if a.no_questions else " with its question", len(S), len(T4), len(D)), "",
     "**The criterion for a fourth-order theme** (stage C2, section 2): " + T4_CRITERION, ""]
seen = set()
for d in D:
    L += ["## %s %s" % (d["id"], d["label"]), ""] + ([] if a.no_questions else [d.get("question") or "", ""])
    for tid in d["members"]:
        r = t4[tid]
        seen.add(tid)
        L.append("**%s %s**%s: %s" % (tid, r["name"], "" if r.get("in_model") else "*",
                                     "; ".join("%s %s" % (x, S[x]["name"]) for x in r["members"])))
        L.append("")
rest = [r for r in T4 if r["id"] not in seen]
if rest:
    L += ["## In no dimension", ""]
    for r in rest:
        L.append("**%s %s**%s: %s" % (r["id"], r["name"], "" if r.get("in_model") else "*",
                                     "; ".join("%s %s" % (x, S[x]["name"]) for x in r["members"])))
        L.append("")
unp = sorted(set(S) - placed)
L += ["## Third-order themes in no fourth-order theme", "",
      "; ".join("%s %s" % (x, S[x]["name"]) for x in unp) + ".", ""]
tiers = "\n".join(L)

verbs = "\n".join([
    "# The read verbs",
    "",
    "If your session has the run's tools, you may check a quote, hour or order against the record "
    "(`metroid/c0001` is room metroid, concept c0001):",
    "",
    "- `python3 tools/cite.py --room <sub> --code <cNNNN>`: a concept's words.",
    "- `python3 tools/mem.py after <sub>/<cNNNN>`: what answered a concept, with intervals.",
    "- `python3 tools/mem.py forest <sub>`: a room's threads with each coded turn's hour (`--offset`, `--limit`).",
    "- `python3 tools/mem.py room <sub> --no-canvas`: a room on one page, always `--no-canvas`.",
    "",
    "Without them, the packet is complete in itself.",
    ""])

SHORT = [("the opening", "the opening"), ("Theorised", "theorised arrows"), ("The model on the dimensions",
         "the model on the dimensions"), ("Dynamics", "dynamics"), ("Ungrounded", "ungrounded relationships"),
         ("Looked for", "looked for and not found"), ("The tiers the arrows", "the tiers and the unused themes"),
         ("Where the model", "where the model should break"), ("The three strongest", "the strongest arrows read "
         "as artefacts"), ("Two tests", "two tests")]
short_dropped = [next((s for p, s in SHORT if d.startswith(p)), d) for d in dropped]
msha = sha(MODEL)
instr = "\n".join([
    "# The reviewer's instruction",
    "",
    INSTRUCTION,
    "",
    "A study's model of how the readers of 705 subreddits (rooms) organized to place pixels on Reddit's canvas "
    "r/place in April 2017; placement stopped at hour 73. The evidence is coders' concepts (`<room>/cNNNN`) grouped "
    "into 197 third-order themes (`T3-NNN`), 28 fourth-order themes (`T4-NNN`) and 8 dimensions (`DNN`). The model "
    "is typed: processes `P`, conditions `K`, a claim `C`, roles `R`, arrows `A`.",
    "",
    "1. `model-p3-sections.md`: sections of the model file `model-p3.md`, verbatim under its title: %s. Not "
    "served, for the 50 KB ceiling: %s." % ("; ".join(n.lower() if i else n for i, n in enumerate(served_names)),
                                           "; ".join(short_dropped) if short_dropped else "none"),
    "2. `story-p3.md`: the last story, whole; each arrow it uses is named in brackets.",
    "3. `criterion.md`: the criterion for preferring a later pass, written before pass 1.",
    "4. `tiers.md`: the tiers, every third-order theme by name, and the criterion your partition is judged against.",
    "5. `verbs.md`: read verbs, if your session has the run's tools.",
    "",
    "**The model served** is `model-p3.md`, sha256 `%s`; copy it into `served`. `model/loops.jsonl` is empty: "
    "no loop is claimed. **Return** as the return specification served with this packet says." % msha,
    ""])

pages = [("0-instruction.md", instr), ("model-p3-sections.md", model_served), ("criterion.md", criterion),
         ("tiers.md", tiers), ("verbs.md", verbs)]
story_b = len(open(STORY, encoding="utf-8").read().strip().encode("utf-8"))
total = story_b
for n, t in pages:
    b = len(t.strip().encode("utf-8"))
    total += b
    print("%-22s %6d bytes" % (n, b))
print("%-22s %6d bytes (served from out/model/story-p3.md)" % ("story-p3.md", story_b))
over = 6 * 12 + 120 + 200          # the packet's headings and END line, roughly
print("pages %d bytes; with the packet's headings and end line about %d; ceiling %d" % (total, total + over, CEILING))
print("served sections: %s" % "; ".join(served_names))
print("not served: %s" % ("; ".join(dropped) or "none"))
print("model-p3.md sha256 %s" % msha)
if a.write:
    os.makedirs(DEST, exist_ok=True)
    for n, t in pages:
        open(os.path.join(DEST, n), "w", encoding="utf-8").write(t.strip() + "\n")
    print("written to %s" % os.path.relpath(DEST, ROOT))
