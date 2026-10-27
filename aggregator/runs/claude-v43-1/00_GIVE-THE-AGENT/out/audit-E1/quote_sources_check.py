#!/usr/bin/env python3
"""E1 section 1, logs against claims, fourth pass (E1b-01): the analyst's quotes of a named source that the earlier
passes did not find whole, set beside the closest passage of that source, so that each can be read by hand. Prints
JSON.

    python3 out/audit-E1/quote_sources_check.py > out/audit-E1/quote_sources_check.json

The rule, declared before the run (E1b-01):
- The quotes: the analyst-file spans of unresolved_hand.json whose sentence names a published source or a stage file
  (literature-C3.md and notes-C3.md quotes of the shelf, notes-C1.md's quote of the stage, notes-C1.md's quote of a
  discriminator), each with the source the sentence names.
- For each, the source's text is cut into windows the quote's length and compared with difflib after the quote and
  the window are lower-cased, with curly quotes made straight, hyphens at line ends joined and white space
  collapsed. The best window is printed with its ratio. A ratio of 1.0 is the words as written; under it, the two are
  read side by side and the difference is named in the audit section.
- J's ruling on reading (notes-B2.md line 5): the shortest distinctive part, "Stop cutting room reads", is looked for
  in every transcript and in the folder's .md files and out/_answers, and its first occurrence is printed with the
  record's type.
"""
import difflib, glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
SH = os.path.join(ROOT, "shelves", "read")
CHECK = [
    ("literature-C3.md", 31, "This prompts consideration of how temporary organizing can be successful in settings without a generalized role structure", "bechky-2006.md"),
    ("literature-C3.md", 36, "a set of contrarian beliefs", "felin-zenger-2017.md"),
    ("literature-C3.md", 36, "a key outcome of hierarchy is systematically advantaging one actor's theory of value over another", "felin-zenger-2017.md"),
    ("literature-C3.md", 51, "a specific set of solutions to the four universal problems that any organization must address in order to exist", "puranam-alexy-reitzig-2014.md"),
    ("literature-C3.md", 51, "goalless networks, and crowds (but not mobs)", "puranam-alexy-reitzig-2014.md"),
    ("literature-C3.md", 280, "is more likely to exist for well-understood goals", "puranam-alexy-reitzig-2014.md"),
    ("literature-C3.md", 15, "coordinating their efforts and managing interdependence grew problematic without the help of people managing the organizational structure", "omahony-ferraro-2007.md"),
    ("literature-C3.md", 44, "privileged groups that value the public good highly enough to contribute regardless of the (non) contributions of others", "puranam-alexy-reitzig-2014.md"),
    ("literature-C3.md", 188, "mapping a set of rewards (both monetary and nonmonetary) to the agents in the organization in order to motivate the agents to cooperate", "puranam-alexy-reitzig-2014.md"),
    ("notes-C3.md", 41, "Examining literature which conflicts with the emergent theory is important for two reasons. First, if researchers ignore conflicting findings, then confidence in the findings is reduced", "eisenhardt-1989.md"),
    ("notes-C3.md", 43, "The real danger of prior knowledge in grounded theory is not that it will contaminate a researcher's perspective, but rather that it will force the researcher into testing hypotheses, either overtly or unconsciously, rather than directly observing.", "suddaby-2006.md"),
    ("notes-C3.md", 44, "the analyst proposes several alternative interpretations of the same events based on different but internally coherent sets of a priori theoretical premises.", "langley-1999.md"),
    ("notes-C1.md", 144, "apply the amended rule, yourself, never a reader", "../../stages/STAGE-C1-model-structuring.md"),
    ("notes-C1.md", 453, "a rivalry from the community's own life", "../../out/scheme_final.jsonl"),
]


def norm(s):
    s = re.sub(r"-\s*\n\s*", "", s)
    for a, b in (("“", '"'), ("”", '"'), ("‘", "'"), ("’", "'"), ("ﬁ", "fi"), ("ﬂ", "fl")):
        s = s.replace(a, b)
    return " ".join(s.split()).lower()


def best(q, text):
    q, t = norm(q), norm(text)
    if q in t:
        return 1.0, q
    n, bs, bw = len(q), 0.0, ""
    step = max(1, n // 6)
    for i in range(0, max(1, len(t) - n + 1), step):
        w = t[i:i + n]
        m = difflib.SequenceMatcher(None, q, w)
        if m.quick_ratio() > bs:
            r = m.ratio()
            if r > bs:
                bs, bw = r, w
    return round(bs, 3), bw


def main():
    rows = []
    for f, line, q, src in CHECK:
        p = os.path.normpath(os.path.join(SH, src))
        text = open(p, encoding="utf-8", errors="replace").read()
        r, w = best(q, text)
        rows.append({"file": f, "line": line, "quote": q, "source": os.path.relpath(p, ROOT), "ratio": r, "closest": w})
    first = None
    for l in open(os.path.join(OUT, "_transcripts", "INDEX.md"), encoding="utf-8"):
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) >= 5 and cells[2].endswith(".jsonl"):
            p = os.path.join(OUT, "_transcripts", cells[2])
            text = open(p, encoding="utf-8", errors="replace").read()
            i = text.find("Stop cutting room reads")
            if i >= 0:
                a = text.rfind("\n", 0, i) + 1
                b = text.find("\n", i)
                rec = json.loads(text[a:b])
                first = {"leg": cells[0], "closed": cells[4], "type": rec.get("type"), "timestamp": rec.get("timestamp"),
                         "context": text[max(a, i - 300):i + 400]}
                break
    others = [os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "*.md")) + glob.glob(os.path.join(OUT, "_answers", "*"))
              if os.path.isfile(p) and "Stop cutting room reads" in open(p, encoding="utf-8", errors="replace").read()]
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-01):")[1].strip(),
                      "rows": rows, "reading_rule_first": first, "reading_rule_in_files": others},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
