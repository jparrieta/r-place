#!/usr/bin/env python3
"""E1 section 1, logs against claims, second pass (E1b-01): what the 2,042 quote spans that quotes_resolve.py resolved
to nothing are. Reads quotes_resolve.json; prints JSON.

    python3 out/audit-E1/unresolved_read.py > out/audit-E1/unresolved_read.json

The rule, declared before the run (E1b-01):
- A span is first tested for its place: on a JSON line or inside a ```json fence of a .md file it is a JSON field
  value, not a quote ("json field").
- Every other span is looked for in six groups of sources, in this order, and takes the first group that holds it:
  (1) the participant's words of a concept (package/store/codes.jsonl `text`); (2) the forest (trees/<sub>.md, whose
  item text is clipped); (3) the coder's case account or brief (package/<sub>/case.md, brief.md); (4) the readers'
  and the coders' returns (out/rooms/, out/_fleet_raw/, out/verdicts*.jsonl, out/adaptation*.jsonl,
  out/coder_conflicts.jsonl); (5) the operator's texts (stages/*.md, the folder's *.md, out/_answers/,
  out/sources-from-J/, out/asks.jsonl, shelves/); (6) the run's own other files (out/ apart from _transcripts, _snap,
  _probe, audit-E1 and the read and pipe logs; the span's own file is never a source).
- Text is compared after curly quotes are made straight, backslashes, asterisks and backticks removed, white space
  collapsed and case lowered, as word triples (single words where the span has fewer than three). An ellipsis or a
  bracketed insertion splits a span into parts; every part's triples count. "whole": every triple of the span is in
  one source file. "near": at least 0.6 of them are, in one file, the best such file named with its share. "nothing":
  under 0.6 everywhere. Spans of "near" and "nothing" are read by hand in the audit section.
"""
import collections, glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
TOK = re.compile(r"[a-z0-9]+")
SPLIT = re.compile(r"\.\.\.|…|\[[^\]]*\]")
SKIP_OWN = re.compile(r"^(_transcripts|_snap|_probe|audit-E1|_mem_|_cite_)")
EXT = (".md", ".jsonl", ".json", ".txt", ".tsv")
GROUPS = ["concept words", "forest", "case account or brief", "returns (readers and coders)", "operator's texts",
          "the run's own files"]


def norm(s):
    for a, b in (("“", '"'), ("”", '"'), ("‘", "'"), ("’", "'"), ("\\", ""), ("*", ""), ("`", "")):
        s = s.replace(a, b)
    return " ".join(s.split()).lower()


def grams(s):
    out = set()
    for part in SPLIT.split(s):
        t = TOK.findall(norm(part))
        if len(t) >= 3:
            out.update(tuple(t[i:i + 3]) for i in range(len(t) - 2))
        elif t:
            out.add(tuple(t))
    return out


def in_json(path, line_no, cache={}):
    if path not in cache:
        flags, fence = [], False
        for line in open(path, encoding="utf-8", errors="replace"):
            s = line.strip()
            if s.startswith("```"):
                flags.append(True)
                fence = (not fence) and s[3:].strip().lower() in ("json", "jsonl")
                continue
            flags.append(fence or s.startswith('{"') or s.startswith('["'))
        cache[path] = flags
    f = cache[path]
    return 0 < line_no <= len(f) and f[line_no - 1]


def sources():
    """Yield (group, key, text) over every source file, one file at a time."""
    for c in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"):
        if c.strip():
            r = json.loads(c)
            yield 0, "%s/%s" % (r["sub"], r["code_id"]), r.get("text") or ""
    for p in sorted(glob.glob(os.path.join(ROOT, "trees", "*.md"))):
        yield 1, os.path.relpath(p, ROOT), open(p, encoding="utf-8", errors="replace").read()
    for p in sorted(glob.glob(os.path.join(ROOT, "package", "*", "case.md")) +
                    glob.glob(os.path.join(ROOT, "package", "*", "brief.md"))):
        yield 2, os.path.relpath(p, ROOT), open(p, encoding="utf-8", errors="replace").read()
    ret = (glob.glob(os.path.join(OUT, "rooms", "**", "*"), recursive=True) +
           glob.glob(os.path.join(OUT, "_fleet_raw", "**", "*"), recursive=True) +
           glob.glob(os.path.join(OUT, "verdicts*.jsonl")) + glob.glob(os.path.join(OUT, "adaptation*.jsonl")) +
           [os.path.join(OUT, "coder_conflicts.jsonl")])
    seen = set()
    for p in sorted(ret):
        if os.path.isfile(p) and p.endswith(EXT):
            seen.add(p)
            yield 3, os.path.relpath(p, OUT), open(p, encoding="utf-8", errors="replace").read()
    ops = (glob.glob(os.path.join(ROOT, "stages", "*.md")) + glob.glob(os.path.join(ROOT, "*.md")) +
           glob.glob(os.path.join(OUT, "_answers", "**", "*"), recursive=True) +
           glob.glob(os.path.join(OUT, "sources-from-J", "**", "*"), recursive=True) +
           glob.glob(os.path.join(ROOT, "shelves", "**", "*"), recursive=True) + [os.path.join(OUT, "asks.jsonl")])
    for p in sorted(ops):
        if os.path.isfile(p) and p.endswith(EXT):
            seen.add(p)
            yield 4, os.path.relpath(p, ROOT), open(p, encoding="utf-8", errors="replace").read()
    for p in sorted(glob.glob(os.path.join(OUT, "**", "*"), recursive=True)):
        rel = os.path.relpath(p, OUT)
        if p in seen or SKIP_OWN.match(rel) or not os.path.isfile(p) or not p.endswith(EXT):
            continue
        if os.path.getsize(p) > 60_000_000:
            continue
        yield 5, rel, open(p, encoding="utf-8", errors="replace").read()


def main():
    qr = json.load(open(os.path.join(OUT, "audit-E1", "quotes_resolve.json"), encoding="utf-8"))
    spans = qr["uncited_unresolved"]
    recs, need = [], collections.defaultdict(list)
    for i, x in enumerate(spans):
        r = dict(x)
        r["first_pass"] = r.pop("class", None)
        if in_json(os.path.join(OUT, x["file"]), x["line"]):
            r["class"] = "json field"
        else:
            g = grams(x["quote"])
            r["_n"] = len(g)
            for t in g:
                need[t].append(i)
        recs.append(r)
    best = {}  # span index -> (group, share, key), the first group reaching 1.0, else the best share
    lens = sorted({len(g) for g in need}, reverse=True)
    for grp, key, text in sources():
        t = TOK.findall(norm(text))
        hits = collections.defaultdict(set)
        for n in lens:
            for j in range(len(t) - n + 1):
                g = tuple(t[j:j + n])
                if g in need:
                    for i in need[g]:
                        hits[i].add(g)
        for i, gs in hits.items():
            if grp == 5 and key == recs[i]["file"]:
                continue
            if grp == 3 and key == recs[i]["file"]:
                continue
            share = len(gs) / recs[i]["_n"]
            cur = best.get(i)
            if cur is None or (cur[1] < 1.0 and (share > cur[1] or (share == 1.0))):
                best[i] = (grp, share, key)
    for i, r in enumerate(recs):
        if r.get("class"):
            continue
        b = best.get(i)
        if b and b[1] >= 0.999:
            r["class"], r["source"] = "whole: " + GROUPS[b[0]], b[2]
        elif b and b[1] >= 0.6:
            r["class"], r["source"], r["share"] = "near: " + GROUPS[b[0]], b[2], round(b[1], 3)
        else:
            r["class"] = "nothing"
            if b:
                r["best"], r["share"] = b[2], round(b[1], 3)
        r.pop("_n", None)
    by_class = collections.Counter(r["class"] for r in recs)
    by_group = collections.defaultdict(collections.Counter)
    for r in recs:
        top = r["file"].split("/")[0]
        by_group[re.sub(r"\d+", "N", top)][r["class"]] += 1
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-01):")[1].strip(),
                      "spans": len(recs), "by_class": dict(by_class.most_common()),
                      "by_file_group": {k: dict(v) for k, v in sorted(by_group.items(), key=lambda kv: -sum(kv[1].values()))},
                      "read_by_hand": [r for r in recs if r["class"] == "nothing" or r["class"].startswith("near")],
                      "all": recs}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
