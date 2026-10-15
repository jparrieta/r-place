#!/usr/bin/env python3
"""C5b: write each reader's own pages (stage C5 section 8, with J's ruling 4 of 15 October) and report the size each
packet will have, by the join packets.py `files` makes, against the 50 KB ceiling.

Per reader k (out/_analysis/c5b/rK/):
  0-read-me-first.md   the served sha256 of account.md, what the packet holds, the stage's instruction verbatim, and
                       the second reading J's ruling 4 asks for
  second-reading.md    the declaration prose rule (its reading parts, verbatim from where it was written before the
                       pass, with the C5a-02 extension); the sentences of the amended declarations that the rule puts
                       in question (c5b_in_question.json), a third of the declarations to each reader, whole
                       declarations kept together; the Stigmergy code definitions, verbatim; and the 24 records drawn
                       for one member theme (reader 1 T3-038, reader 2 T3-041, reader 3 T3-060), each through cite.py,
                       words, citation and hour only: no code of mine and no coder's label
The shared pages: account.md, figure-C5.md, propositions.jsonl, and out/_analysis/c5b/rooms.md.

    python3 out/_analysis/c5b_pages.py            report sizes only
    python3 out/_analysis/c5b_pages.py --write    write the pages
"""
import hashlib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DEST = os.path.join(OUT, "_analysis", "c5b")
CEILING = 50 * 1024
END = ("This is the end of the packet. Confirm you reached it by returning your lines and then the "
       "end marker the return specification names. END OF PACKET")   # packets.py's END, for the size only
THEMES = {1: "T3-038", 2: "T3-041", 3: "T3-060"}
INSTRUCTION = ("*Read the account as a stranger. Say where it carries what it means and where it does not, both ways: "
               "a sentence you cannot follow, a claim you cannot find the evidence for, a room you can name that the "
               "account does not fit, jargon a reader would not accept. Do not propose another model. A disagreement is "
               "never a verdict.*")
ROOMS_INSTRUCTION = ("*For each of the three rooms you were given, say whether the account describes what happened there "
                     "and, where it does not, what the room did instead, one paragraph per room.*")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


notes = open(os.path.join(OUT, "notes-C5.md"), encoding="utf-8").read()


def block(start, stop):
    """The text from the line starting `start` up to (not including) the line starting `stop`, verbatim."""
    i = notes.index(start)
    j = notes.index(stop, i)
    return notes[i:j].strip()


rule = block("**What the rule reads.**", "**What does not change.**")
ext = block("**The scope.**", "**What stays the same.**")   # the C5a-02 extension, its scope paragraph only
codes_def = block("**The codes.**", "**The decision rules.**")
iq = json.load(open(os.path.join(OUT, "_analysis", "c5b_in_question.json"), encoding="utf-8"))
iq = [d for d in iq if d["in_question"]]
sample = json.load(open(os.path.join(OUT, "_analysis", "c5_stigmergy_sample.json"), encoding="utf-8"))
# split whole declarations across the three readers, largest first, each to the reader with the fewest bytes so far,
# counting each reader's Stigmergy records in its load
load = {k: sum(len(r["text"]) + 40 for r in sample[THEMES[k]]["drawn"]) for k in (1, 2, 3)}
share = {1: [], 2: [], 3: []}
for d in sorted(iq, key=lambda d: (-sum(len(s["sentence"]) for s in d["in_question"]), d["id"])):
    k = min(load, key=lambda k: (load[k], k))
    share[k].append(d)
    load[k] += sum(len(s["sentence"]) + 20 for s in d["in_question"])


def cite(sub, code):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py"), "--room", sub, "--code", code, "--json"],
                       capture_output=True, text=True, cwd=ROOT)
    q = json.loads(p.stdout)["quotes"][0]
    return '- [%s/%s] h%.2f: "%s"' % (q["sub"], q["code_id"], q["hour"], q["text"].replace("\n", " "))


acc_sha = sha(os.path.join(OUT, "account.md"))
pages = {}
for k in (1, 2, 3):
    order = sorted(share[k], key=lambda d: (d["id"][0] != "T", d["id"]))
    n_sent = sum(len(d["in_question"]) for d in order)
    recs = sample[THEMES[k]]["drawn"]
    read_me = "\n".join([
        "# Packet C5-reader-%d: read this first" % k, "",
        "**Served:** `account.md`, sha256 `%s`. Copy this digest into `served`." % acc_sha, "",
        "The packet holds this page, `account.md`, `figure-C5.md`, `propositions.jsonl` (nine propositions, one JSON "
        "line each), `rooms.md` and `second-reading.md`, and nothing else of the analyst's. Return one JSON line as "
        "`RETURN-C5.md`, served beside the packet, says.", "",
        "Ids: an element is P, K, R or C with two digits; an arrow is A with two digits; a proposition is N with two "
        "digits; a finding is F- with three digits; a declaration is T4- with three digits, or D with two.", "",
        "## First task: the account", "", INSTRUCTION, "", ROOMS_INSTRUCTION, "",
        "## Second task: a second reading", "",
        "The account's constructs were declared earlier in the study and then amended under a rule. You are a second "
        "reader of that work. In `second-reading.md`:",
        "1. Read the rule. For each of the %d sentences under \"The sentences in question\", say whether it stands "
        "under the rule, and why, in one sentence. You do not hold the files the rule names; judge from what the "
        "sentence itself carries: a count, a finding id, a fact of the setting, or a member's words." % n_sent,
        "2. Read the code definitions. Give each of the %d records under \"The records to code\" one code. Read each "
        "record whole." % len(recs), ""])
    L = ["# The second reading", "", "## The rule", "",
         "Written before the declarations were amended. The rule was first written for the fourth-order themes; the "
         "paragraph after it extends it to the dimensions.", "", rule, "",
         ext, "",
         "## The sentences in question", "",
         "Each sentence below is quoted from an amended declaration and holds a word from the rule's lists. The field "
         "it comes from is in brackets.", ""]
    for d in order:
        L.append("**%s %s**" % (d["id"], d["name"]))
        for s in d["in_question"]:
            L.append("- (%s) %s" % (s["field"], s["sentence"]))
        L.append("")
    L += ["## The records to code", "", codes_def, "",
          "The records below are drawn from the record at random. Each is a member's words, verbatim, with its "
          "citation and its hour since the canvas opened.", ""]
    L += [cite(r["sub"], r["code_id"]) for r in recs]
    pages[k] = {"0-read-me-first.md": read_me, "second-reading.md": "\n".join(L) + "\n"}
shared = [os.path.join(OUT, "account.md"), os.path.join(OUT, "figure-C5.md"), os.path.join(OUT, "propositions.jsonl"),
          os.path.join(DEST, "shared", "rooms.md")]
for k in (1, 2, 3):
    texts = [("0-read-me-first.md", pages[k]["0-read-me-first.md"])]
    texts += [(os.path.basename(p), open(p, encoding="utf-8").read()) for p in shared]
    texts += [("second-reading.md", pages[k]["second-reading.md"])]
    L = ["# Packet C5-reader-%d" % k, ""]
    for name, t in texts:
        L += ["## %s" % name, "", t.strip(), ""]
    L += ["", END, ""]
    b = len("\n".join(L).encode("utf-8"))
    print("C5-reader-%d: %d bytes (ceiling %d, margin %d); declarations %s; sentences %d; records %d (%s)" % (
        k, b, CEILING, CEILING - b, ", ".join(d["id"] for d in share[k]),
        sum(len(d["in_question"]) for d in share[k]), len(sample[THEMES[k]]["drawn"]), THEMES[k]))
    if "--write" in sys.argv:
        os.makedirs(os.path.join(DEST, "r%d" % k), exist_ok=True)
        for name, t in pages[k].items():
            open(os.path.join(DEST, "r%d" % k, name), "w", encoding="utf-8").write(t)
if "--write" in sys.argv:
    print("pages written under %s" % DEST)
