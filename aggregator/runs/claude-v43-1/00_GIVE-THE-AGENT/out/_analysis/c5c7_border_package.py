#!/usr/bin/env python3
"""C5c-07: build the package for the second coding of border talk (J, 13:45 Amsterdam, 15 October), in the form of
out/field-packages-C5/, into out/field-packages-C5b/:

  00-READ-FIRST.md          who codes, the one rule, the study in brief, where the records come from, what to do
  01-the-codes.md           the codes as written in notes-C5.md before the analyst's read at C5a-02, verbatim
  02-border-records.md      the 40 records of that read (c5_p08_sample.json), each the room's first border-talk
                            concept, through cite.py with its citation, hour, author, the coder's label and the
                            member's words, in a seeded order; no one's codes
  RETURN-border-C5b.md      the return format
  MANIFEST.json             each file's bytes and sha256

Nothing of c5_p08_codes.json (the analyst's codes and doubts) is served.

    python3 out/_analysis/c5c7_border_package.py            sizes only
    python3 out/_analysis/c5c7_border_package.py --write    write the folder; refuses if it exists
"""
import hashlib, json, os, random, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DEST = os.path.join(OUT, "field-packages-C5b")
SEED = 20261015


def cite_json(args):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py")] + args + ["--json"],
                       capture_output=True, text=True, cwd=ROOT)
    try:
        return json.loads(p.stdout).get("quotes") or []
    except ValueError:
        return []


notes = open(os.path.join(OUT, "notes-C5.md"), encoding="utf-8").read()
sec = notes.index("## Pass 2: the P08 question, rules written before the read")
sec_end = notes.index("## Pass 2 (C5a-02): what the pass did", sec)
section = notes[sec:sec_end]
codes_def = section[section.index("**The codes.**"):section.index("**The rule.**")].strip()

sample = json.load(open(os.path.join(OUT, "_analysis", "c5_p08_sample.json"), encoding="utf-8"))
recs = [(sub, v["P08"].split()[0]) for sub, v in sorted(sample["drawn"].items())]
random.Random(SEED).shuffle(recs)

R = ["# The records to code", "",
     "40 records, in a random order. Each is one room's first concept of border talk. Give each record one code from "
     "`01-the-codes.md`, reading it whole. No one's codes are given.", "",
     "Each record shows its citation (room/concept id), the hour since the canvas opened, the author as the record "
     "carries it, the first-order coder's one-line label for the concept, and the member's words. The label is the "
     "coder's summary, not a code of this read; where the label and the words differ, the words decide.", ""]
missing = []
for sub, code in recs:
    q = cite_json(["--room", sub, "--code", code])
    if not q:
        missing.append("%s/%s" % (sub, code))
        continue
    q = q[0]
    R += ["- [%s/%s] h%.2f, %s" % (sub, code, q["hour"], q.get("author") or "?"),
          "  - label: %s" % q["first_order"].replace("\n", " ").strip(),
          '  - words: "%s"' % q["text"].replace("\n", " ").strip()]
if missing:
    sys.exit("cite.py did not resolve: %s" % ", ".join(missing))

CODES = "\n".join([
    "# The codes", "",
    "The analyst wrote these codes at C5a-02, before reading any record, in `notes-C5.md` (section \"Pass 2: the P08 "
    "question, rules written before the read\"). They are copied here verbatim. The analyst read each record whole "
    "and gave it one code.", "",
    codes_def, ""])

READ = "\n".join([
    "# The second coding of border talk: read this first", "",
    "Target length: about 600 words. J, the principal investigator, asked for this coding on 15 October.", "",
    "## Who codes, and the one rule for you", "",
    "You are the second coder of 40 records of border talk. You may be a fork of the analyst who modelled the r/place "
    "event from the r/place subreddit (the field model), or a fresh session. Either way, **code each record against "
    "its own words and the codes in `01-the-codes.md`, not against what you know of the event.** If you know from "
    "elsewhere that a room's work was damaged, but the record does not name it, code what the record says. Do not "
    "propose another coding scheme. Your codes decide nothing alone: each record takes the code at least two coders "
    "gave.", "",
    "## The study, in brief", "",
    "In April 2017, Reddit's r/place let any account place one pixel on a shared canvas every few minutes. Placement "
    "stopped at hour 73. This study reads the talk of 705 subreddits (\"rooms\") about the canvas. Coders cut "
    "members' words into first-order concepts, each with a one-line label. The concepts were grouped into themes "
    "within each room, then across rooms. The analyst's model names the elements those themes carry.", "",
    "## What border talk is here, and where the records come from", "",
    "- **Border talk** is the model's element in which rooms propose, settle and contest borders, truces and deals "
    "with neighbouring rooms by talk.",
    "- **Upkeep** is the model's element in which members keep the placed work against erosion: they watch it, "
    "repair changed pixels and rally to defend it.",
    "- **The rooms.** 401 rooms carry both elements. In 166 of them, the first concept of border talk does not come "
    "after the first concept of upkeep. 40 of these 166 rooms were drawn at random (seed 20261015).",
    "- **The records.** Each record is the first concept of border talk in one of the 40 rooms, served whole.", "",
    "## What to read, in order", "",
    "1. This page.",
    "2. `01-the-codes.md`: three codes, T, D and O.",
    "3. `02-border-records.md`: the 40 records.",
    "4. `RETURN-border-C5b.md`: the return format.", "",
    "## What to do", "",
    "Give each record exactly one code. Read the member's words whole. Where a record could take two codes, choose "
    "the one its words carry more plainly, and mark the record as doubtful with the reason in one clause. Return one "
    "line per record and the end marker.", ""])

RETURN = "\n".join([
    "# RETURN-border-C5b: the return format for the second coding of border talk", "",
    "Target length: about 150 words. One JSON object per record, in any order, then the end marker on a line of "
    "its own.", "",
    "- `record`: the citation, copied exactly (`sub/cNNNN`);",
    "- `code`: exactly one of `T`, `D`, `O`;",
    "- `why`: one clause, naming the words that decide the code;",
    "- `doubtful`: `true` or `false`; where `true`, `why` says what the other code would rest on.", "",
    "```json",
    '{"record": "sub/c0001", "code": "T", "why": "...", "doubtful": false}',
    "END-OF-BORDER-RETURN",
    "```", "",
    "Your codes decide nothing alone. After your 40 lines, write the end marker `END-OF-BORDER-RETURN` on a line of "
    "its own. Confirm that you reached the end of the records by writing that marker; a return without it is "
    "partial.", ""])

files = {"00-READ-FIRST.md": READ, "01-the-codes.md": CODES, "02-border-records.md": "\n".join(R) + "\n",
         "RETURN-border-C5b.md": RETURN}
tot = 0
for n, t in sorted(files.items()):
    b = len(t.encode("utf-8"))
    tot += b
    print("%-26s %6d bytes" % (n, b))
print("records: %d of %d drawn; total %d bytes" % (len(recs), len(sample["drawn"]), tot))
if "--write" in sys.argv:
    if os.path.exists(DEST):
        sys.exit("%s exists; supersede it with a new name" % DEST)
    os.makedirs(DEST)
    man = {}
    for n, t in files.items():
        open(os.path.join(DEST, n), "w", encoding="utf-8").write(t)
        man[n] = {"bytes": len(t.encode("utf-8")), "sha256": hashlib.sha256(t.encode("utf-8")).hexdigest()}
    json.dump({"built": "C5c-07", "seed": SEED, "records": len(recs), "source": "out/_analysis/c5_p08_sample.json",
               "files": man}, open(os.path.join(DEST, "MANIFEST.json"), "w"), indent=1)
    print("wrote %s" % DEST)
