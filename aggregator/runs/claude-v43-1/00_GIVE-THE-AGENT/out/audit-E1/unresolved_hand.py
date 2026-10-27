#!/usr/bin/env python3
"""E1 section 1, logs against claims, third pass (E1b-01): where the spans that unresolved_read.py left "near" or
"nothing" first appear in the run's transcripts, so that each can be read for what it is. Reads unresolved_read.json;
prints JSON.

    python3 out/audit-E1/unresolved_hand.py > out/audit-E1/unresolved_hand.json

The rule, declared before the run (E1b-01). Two earlier runs searched with grep, one search per span and then one
pass for all; both were stopped as too slow, and their empty outputs are kept as unresolved_hand.superseded-1.json
and -2.json. The rule is unchanged; the search is now Python's, in the order below.
- For each span, a needle: its longest run of letters, digits, spaces and the marks , . ; : ! ? ( ) -, cut to 48
  characters at a word end; a span whose longest run is under 12 characters gets no needle and is read by hand only.
- The transcripts (out/_transcripts/) are read in the order of their leg's close (INDEX.md). A needle is looked for, as
  a fixed string, leg by leg, until the first leg that holds it. In that leg, each line holding the needle is typed by
  its record: a message to the analyst (a user record whose text is not a tool's result: the leg message, the
  principal investigator's or the handler's words), a tool's output (a user record holding a tool_result: what a read,
  a command or a file returned), the analyst's text, or the analyst's tool input (a command or a file the analyst
  wrote). The earliest line of each type in that leg is kept, by timestamp.
- The needle is also looked for in trees/*.md and package/<sub>/case.md and brief.md.
- What the span is follows from the earliest line: a message to the analyst means the operator's or the harness's
  words; a tool's output earlier than any analyst line means words the analyst read; the analyst's own text or input
  first means the analyst's words. trees/ or package/ holding the needle means participant or coder words.
"""
import glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
TR = os.path.join(OUT, "_transcripts")
RUN = re.compile(r"[A-Za-z0-9 ,.;:!?()\-]+")


def needle(span):
    runs = sorted((r.strip() for r in RUN.findall(span)), key=len, reverse=True)
    if not runs or len(runs[0]) < 12:
        return None
    n = runs[0]
    if len(n) > 48:
        n = n[:48].rsplit(" ", 1)[0]
    return n if len(n) >= 12 else None


def kind(rec):
    t = rec.get("type")
    msg = rec.get("message") or {}
    c = msg.get("content")
    if t == "user":
        if isinstance(c, list) and any(isinstance(p, dict) and p.get("type") == "tool_result" for p in c):
            return "tool output"
        return "message to the analyst"
    if t == "assistant":
        if isinstance(c, list) and any(isinstance(p, dict) and p.get("type") == "tool_use" for p in c):
            return "analyst tool input"
        return "analyst text"
    return t or "other"


def lines_holding(text, n):
    i = text.find(n)
    while i >= 0:
        a = text.rfind("\n", 0, i) + 1
        b = text.find("\n", i)
        b = len(text) if b < 0 else b
        yield text[a:b]
        i = text.find(n, b)


def main():
    d = json.load(open(os.path.join(OUT, "audit-E1", "unresolved_read.json"), encoding="utf-8"))
    legs = []
    for l in open(os.path.join(TR, "INDEX.md"), encoding="utf-8"):
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) >= 5 and cells[2].endswith(".jsonl"):
            legs.append((cells[4], cells[0], cells[2]))
    legs.sort()
    recs = []
    for r in d["read_by_hand"]:
        rec = {k: r[k] for k in ("file", "line", "quote", "class") if k in r}
        rec["needle"] = needle(r["quote"])
        recs.append(rec)
    todo = {r["needle"] for r in recs if r["needle"]}
    found = {}
    for _closed, leg, f in legs:
        if not todo:
            break
        p = os.path.join(TR, f)
        if not os.path.exists(p):
            continue
        text = open(p, encoding="utf-8", errors="replace").read()
        for n in [n for n in todo if n in text]:
            first = {}
            for line in lines_holding(text, n):
                try:
                    j = json.loads(line)
                except ValueError:
                    continue
                k, ts = kind(j), j.get("timestamp") or ""
                if k not in first or ts < first[k]:
                    first[k] = ts
            found[n] = (leg, dict(sorted(first.items(), key=lambda kv: kv[1])))
            todo.discard(n)
    src = sorted(glob.glob(os.path.join(ROOT, "trees", "*.md")) + glob.glob(os.path.join(ROOT, "package", "*", "case.md")) +
                 glob.glob(os.path.join(ROOT, "package", "*", "brief.md")))
    where = {}
    allneed = {r["needle"] for r in recs if r["needle"]}
    for p in src:
        text = open(p, encoding="utf-8", errors="replace").read()
        for n in allneed:
            if n in text:
                where.setdefault(n, []).append(os.path.relpath(p, ROOT))
    for rec in recs:
        n = rec["needle"]
        if not n:
            continue
        rec["in_trees_or_package"] = where.get(n, [])[:5]
        if n in found:
            rec["first_leg"], rec["first_by_type"] = found[n]
            rec["earliest_type"] = next(iter(rec["first_by_type"]), None)
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-01).")[1].strip(),
                      "n": len(recs), "spans": recs}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
