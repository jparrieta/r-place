#!/usr/bin/env python3
"""C5c-01: the field analyst's packages for the second reading of the declarations (QC5-001, J's ruling of
15 October 08:35 and 09:09 Amsterdam). No fleet ceiling binds them. Writes out/field-packages-C5/:

  00-READ-FIRST.md          who reads, what the study is, what to read first, what to judge, how to return
  01-the-rule.md            the declaration prose rule whole, as written before the declarations were amended, with
                            its C5a-02 extension to the dimensions, and the four setting facts
  02-D01-...md to 09-D08    one package per dimension: the dimension's declaration and those of the fourth-order themes
                            it gathers, as they stand now (fourth/fourth.jsonl, dimensions.jsonl), every sentence of the
                            fields the rule reads numbered; each declaration's members by name; the members' quotes it
                            rests on: every quote its fields cite and every quote its amendment rested on
                            (c5_prose_amend.json, c5_dim_amend.json), and 3 quotes per member theme drawn by cite.py
                            under seed 20261015, each through cite.py with its citation, hour and author
  10-findings.md            every finding a declaration cites, its statement and bound as the ledger holds them now
  11-stigmergy-records.md   the 72 records of the Stigmergy read, in a seeded order, with the code definitions, and with
                            no code of the analyst's and no coder's label: a third coding, blind
  RETURN-field-C5.md        the return format
  MANIFEST.json             each file's bytes and sha256

Nothing of the fleet readers' returns is served. The reader is told to judge against the members' quotes, not against
a model of its own.

    python3 out/_analysis/c5c_field_packages.py            sizes only
    python3 out/_analysis/c5c_field_packages.py --write    write the folder
"""
import hashlib, json, os, random, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DEST = os.path.join(OUT, "field-packages-C5")
SEED = 20261015
PER_MEMBER = 3


def jl(p):
    return [json.loads(l) for l in open(os.path.join(OUT, p), encoding="utf-8") if l.strip()]


def cite_json(args):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py")] + args + ["--json"],
                       capture_output=True, text=True, cwd=ROOT)
    try:
        return json.loads(p.stdout).get("quotes") or []
    except ValueError:
        return []


def qline(q):
    return '- [%s/%s] h%.2f, %s: "%s"' % (q["sub"], q["code_id"], q["hour"], q.get("author") or "?",
                                          q["text"].replace("\n", " ").strip())


QUOTED = re.compile(r"'[^\[]*?' \[[A-Za-z0-9_]+/c\d{4}\]")   # a member's quote with its citation, kept whole


def sentences(t):
    t = re.sub(r"\s+", " ", t or "").strip()
    held = []

    def hold(m):
        held.append(m.group(0))
        return "\x00%d\x00" % (len(held) - 1)

    t = QUOTED.sub(hold, t)
    out = [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'\[(\x00])", t) if s]
    return [re.sub(r"\x00(\d+)\x00", lambda m: held[int(m.group(1))], s) for s in out]


notes = open(os.path.join(OUT, "notes-C5.md"), encoding="utf-8").read()


def block(start, stop):
    i = notes.index(start)
    return notes[i:notes.index(stop, i)].strip()


fourth = {r["id"]: r for r in jl("fourth/fourth.jsonl")}
dims = {r["id"]: r for r in jl("dimensions.jsonl")}
names3 = {r["id"]: r["name"] for r in jl("scheme_v2.jsonl")}
amend4 = json.load(open(os.path.join(OUT, "_analysis", "c5_prose_amend.json"), encoding="utf-8"))
amendD = json.load(open(os.path.join(OUT, "_analysis", "c5_dim_amend.json"), encoding="utf-8"))
findings = {}
for r in jl("findings.jsonl"):
    findings[r["id"]] = r          # the last line of each id is the ledger's current one
cited_findings = set()
CITE = re.compile(r"\[?([A-Za-z0-9_]+)/(c\d{4})\]?")


def quotes_for(decl_id, fields, rests):
    keys = []
    for t in fields:
        for sub, code in CITE.findall(t or ""):
            keys.append((sub, code))
    for x in rests or []:
        m = re.match(r"^([A-Za-z0-9_]+):(c\d{4})$", x)
        if m:
            keys.append((m.group(1), m.group(2)))
    seen, out = set(), []
    for k in keys:
        if k in seen:
            continue
        seen.add(k)
        q = cite_json(["--room", k[0], "--code", k[1]])
        if q:
            out.append(q[0])
    return out


def numbered(decl_id, field, text, L, count):
    for n, s in enumerate(sentences(text), 1):
        L.append("- `%s.%s.%d` %s" % (decl_id, field, n, s))
        count[0] += 1
        cited_findings.update(re.findall(r"F-\d{3}", s))


def fourth_block(t4, L, count):
    r = fourth[t4]
    L += ["### %s %s" % (t4, r["name"]), "",
          "Declared %s. Source: %s." % (r.get("declared") or "?", r.get("source") or "none"),
          "Members (third-order themes): %s." % "; ".join("%s %s" % (m, names3.get(m, "?")) for m in r["members"]),
          "", "**The sentences to judge.**", ""]
    for f in ("prose", "changed", "mistaken_for"):
        if isinstance(r.get(f), str) and r[f].strip():
            numbered(t4, f, r[f], L, count)
    a = amend4.get(t4) or {}
    qs = quotes_for(t4, [r.get("prose"), r.get("changed"), r.get("mistaken_for")], a.get("rests_on"))
    L += ["", "**The quotes the declaration cites or rests on** (%d):" % len(qs), ""] + [qline(q) for q in qs]
    L += ["", "**Quotes drawn from each member theme** (%d per member, `cite.py --tier 3rd --id <member> --n %d "
              "--seed %d`):" % (PER_MEMBER, PER_MEMBER, SEED), ""]
    for m in r["members"]:
        L.append("%s %s:" % (m, names3.get(m, "?")))
        L += [qline(q) for q in cite_json(["--tier", "3rd", "--id", m, "--n", str(PER_MEMBER), "--seed", str(SEED)])]
    L.append("")


def dim_block(d, L, count):
    r = dims[d]
    c = r.get("construct") or {}
    L += ["## %s %s (dimension)" % (d, r["label"]), "",
          "Declared %s. Source: %s." % (c.get("status") or "?", c.get("source") or "none"),
          "Gathers: %s." % "; ".join("%s %s" % (m, fourth[m]["name"]) for m in r["members"]),
          "Question: %s" % (r.get("question") or ""), "", "**The sentences to judge.**", ""]
    for f in ("changed", "mistaken_for"):
        if isinstance(c.get(f), str) and c[f].strip():
            numbered(d, f, c[f], L, count)
    a = amendD.get(d) or {}
    qs = quotes_for(d, [c.get("changed"), c.get("mistaken_for")], a.get("rests_on"))
    if c.get("gloss_from") and "/" in c["gloss_from"]:
        sub, code = c["gloss_from"].split("/", 1)
        g = cite_json(["--room", sub, "--code", code])
        if g and all(not (x["sub"] == g[0]["sub"] and x["code_id"] == g[0]["code_id"]) for x in qs):
            qs = g + qs
    L += ["", "**The quotes the declaration cites or rests on, its gloss first** (%d):" % len(qs), ""]
    L += [qline(q) for q in qs] + [""]


READ_FIRST = """# The second reading of the declarations: read this first

Target length: about 1,000 words. J, the principal investigator, asked for this reading on 15 October (QC5-001).

## Who reads, and the one rule for you

You are the second reader of the analyst's declarations. You may be a fork of the analyst who modelled the r/place event from the r/place subreddit (the field model), or a fresh session given that field model as context. Either way, **judge each sentence against the members' quotes in these packages and the rule in `01-the-rule.md`, not against your own model of the event.** Where your model and the quotes disagree, the quotes decide. Do not propose another model. A disagreement is never a verdict: your reading decides nothing alone, and the analyst answers each point.

## The study, in brief

In April 2017, Reddit's r/place let any account place one pixel on a shared canvas every few minutes. Placement stopped at hour 73. This study reads the talk of 705 subreddits ("rooms") about the canvas. Coders cut members' words into first-order concepts. These were grouped into second-order themes in each room, then into third-order themes across rooms, fourth-order themes, and eight dimensions.

Each fourth-order theme and dimension is declared as a construct:
- **prose:** what members did, in how many rooms;
- **changed:** how the construct differs from its source in the literature, or why it was coined;
- **mistaken_for:** what a reader might take it for, and how it differs.

The declarations were amended under the rule in `01-the-rule.md`. Every sentence about the rooms should say what members did, in how many rooms, shown by members' quotes. A broader claim (universal, comparative, causal or cyclic) needs a count, a finding or a setting fact to support it.

## What to read, in order

1. This page.
2. `01-the-rule.md`.
3. The eight packages `02-D01` to `09-D08`. Each holds one dimension and the fourth-order themes it gathers: 36 declarations in all, with every sentence numbered.
4. `10-findings.md`, when a sentence cites a finding (F- and three digits).
5. `11-stigmergy-records.md`: 72 records to code.
6. `RETURN-field-C5.md`, the return format.

## What to judge, for each numbered sentence

1. **What is it about?** If it is about a source in the literature, or about the study's own procedure, its kind is `about the literature or the study`. It stands unless it also states something about the rooms.
2. **Is it a broader claim?** If it holds a universal, comparative, causal or cyclic word from the rule's lists, does a count, a finding or a setting fact support it? Take the counts of rooms as given, since the study's tables computed them. Judge whether a sentence that needs a count carries one.
3. **Is it a description?** If it says what members did, does at least one quote in the package show each act it names? Do the quotes show what the sentence says, or something else?

Each declaration comes with the quotes it cites or rested on, and 3 quotes drawn at random from each member theme. The drawn quotes let you see whether the description holds beyond the quotes the analyst chose. They are drawn from every concept whose coder's theme was placed on the member theme, and a coder's theme can hold concepts of other kinds. So some drawn quotes show other acts. Count such a quote against a sentence only where the sentence claims something of all its members' material, and say so in a note on the declaration.

## The records to code

`11-stigmergy-records.md` holds 72 records from the read the analyst made for the theme Stigmergy, with the code definitions written before that read. Give each record one code. Read each record whole. The analyst's codes are not given, and no other reader's are.

## How to return

Use the format in `RETURN-field-C5.md`: one JSON line per sentence, one per record, and any notes on a declaration as a whole. End with the end marker. Return one file for all packages, or one per package, as suits you. Key every line by the ids given.
"""

RETURN = """# RETURN-field-C5: the return format for the second reading of the declarations

Target length: about 300 words. One JSON object per line, in any order, then the end marker on a line of its own.

- **One line per numbered sentence,** each with:
  - `sentence`: the id, such as `T4-007.prose.3`;
  - `kind`: one of `claim in question` (it holds a word from the rule's lists), `description` (it says what members did), or `about the literature or the study`;
  - `stands`: `true` or `false`;
  - `rests_on`: what it stands on or fails for want of: the quote citations (`sub/cNNNN`), finding ids, `setting fact` or `count`; an empty list if nothing;
  - `why`: one sentence. Where it does not stand, say which part of the rule it fails, or what the quotes show instead.
- **One line per record** in `11-stigmergy-records.md`: `record` (the citation, copied exactly) and `code` (exactly one of `M`, `MP`, `P`, `O`).
- **Any number of lines on a declaration as a whole:** `declaration` (its id) and `note`. Use these, for example, for a member theme whose drawn quotes the declaration does not describe.

```json
{"sentence": "T4-007.prose.3", "kind": "description", "stands": true, "rests_on": ["bindingofisaac/c0181"], "why": "..."}
{"record": "sub/c0001", "code": "M"}
{"declaration": "T4-007", "note": "..."}
END-OF-FIELD-RETURN
```

A disagreement is never a verdict: your reading decides nothing alone.

After your lines, write the end marker `END-OF-FIELD-RETURN` on a line of its own. Confirm that you reached the end of the packages by writing that marker; a return without it is partial.
"""

files = {}
files["00-READ-FIRST.md"] = READ_FIRST
rule = block("**What the rule reads.**", "**How each amendment is recorded.**")
ext = block("**The scope.**", "\n## ")   # the C5a-02 extension, to the end of its section
files["01-the-rule.md"] = "\n".join([
    "# The declaration prose rule", "",
    "Target length: about 700 words. The analyst wrote this rule before amending the 28 fourth-order declarations, and "
    "extended it to the eight dimensions before amending them. It is given here as written. You do not hold the files "
    "it names. Judge from what each sentence carries and from the quotes and findings in these packages.", "",
    "## The rule, for the fourth-order themes", "", rule, "",
    "## The extension, for the dimensions", "", ext, "",
    "## The four setting facts", "",
    "- Each account could place one pixel per interval.", "- Anyone may change any pixel.",
    "- Placement stopped at hour 73.", "- No one holds authority over another's placing.", ""])
count_all = 0
for i, d in enumerate(sorted(dims), 2):
    L = ["# Package %02d: %s %s, and the fourth-order themes it gathers" % (i, d, dims[d]["label"]), "",
         "Every sentence to judge is numbered `<declaration>.<field>.<n>`. The quotes are members' words, verbatim, "
         "through the study's quoting tool, each with its citation, hour since the canvas opened, and author.", ""]
    count = [0]
    dim_block(d, L, count)
    for t4 in dims[d]["members"]:
        fourth_block(t4, L, count)
    L.insert(2, "Sentences to judge in this package: %d." % count[0])
    files["%02d-%s-%s.md" % (i, d, re.sub(r"[^A-Za-z]+", "-", dims[d]["label"]).strip("-"))] = "\n".join(L) + "\n"
    count_all += count[0]
F = ["# The findings the declarations cite", "",
     "Each finding as the study's ledger holds it now: its statement and its bound.", ""]
for f in sorted(cited_findings):
    r = findings.get(f)
    if r:
        F += ["## %s (%s)" % (f, r.get("status")), "", r.get("statement", ""), "", "Bound: %s" % (r.get("bound") or "none"), ""]
files["10-findings.md"] = "\n".join(F)
codes_def = block("**The codes.**", "**The decision rules.**")
sample = json.load(open(os.path.join(OUT, "_analysis", "c5_stigmergy_sample.json"), encoding="utf-8"))
recs = [(r["sub"], r["code_id"]) for th in sorted(sample) for r in sample[th]["drawn"]]
random.Random(SEED).shuffle(recs)
S = ["# The records to code", "",
     "72 records from the analyst's read for the theme Stigmergy, in a random order. The code definitions below were "
     "written before that read. Give each record one code, reading it whole. No one's codes are given.", "",
     codes_def, "", "## The records", ""]
for sub, code in recs:
    q = cite_json(["--room", sub, "--code", code])
    S.append('- [%s/%s] h%.2f: "%s"' % (sub, code, q[0]["hour"], q[0]["text"].replace("\n", " ").strip()))
files["11-stigmergy-records.md"] = "\n".join(S) + "\n"
files["RETURN-field-C5.md"] = RETURN
tot = 0
for n, t in sorted(files.items()):
    b = len(t.encode("utf-8"))
    tot += b
    print("%-44s %7d bytes" % (n, b))
print("sentences to judge: %d; findings cited: %s; records: %d; total %d bytes" % (
    count_all, ", ".join(sorted(cited_findings)), len(recs), tot))
if "--write" in sys.argv:
    os.makedirs(DEST, exist_ok=True)
    man = {}
    for n, t in files.items():
        p = os.path.join(DEST, n)
        open(p, "w", encoding="utf-8").write(t)
        man[n] = {"bytes": len(t.encode("utf-8")), "sha256": hashlib.sha256(t.encode("utf-8")).hexdigest()}
    json.dump({"built": "C5c-01", "seed": SEED, "sentences": count_all, "records": len(recs), "files": man},
              open(os.path.join(DEST, "MANIFEST.json"), "w"), indent=1)
    print("wrote %s" % DEST)
