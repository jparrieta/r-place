#!/usr/bin/env python3
"""E1 section 1, logs against claims: every quote in every output, resolved as cite.py --resolve resolves it.

    python3 out/audit-E1/quotes_resolve.py > out/audit-E1/quotes_resolve.json

The rule, declared before the run (E1a):
- Outputs: every .md file under out/ written by the analyst, and the string fields of the analyst's ledgers (out/*.jsonl,
  out/model/*.jsonl, out/fourth/*.jsonl). Left out, as not the analyst's: _probe, _transcripts, _snap, _views and _wiki
  (generated), _fleet_raw, _packets-*, handoff-D*, field-packages-*, readers-C5 (fleet and harness), _answers and
  sources-from-J (the principal investigator), _analysis (working files), audit-E1 (this audit), and the read and pipe
  logs (_mem_*, _cite_*), which record commands, not claims.
- A quote: a span between paired double quotes on one line (straight quotes pair in turn; a curly opening quote pairs
  with the next closing one), 6 to 400 characters. A cited quote has a citation within 80 characters after it:
  [sub/cNNNN] (or sub:cNNNN) for a concept, or `itemid` for a case-account moment. In .md files an uncited span is
  counted when it has five words or more; in ledgers only cited spans are counted.
- Resolution, in order, on the span with white space collapsed and curly quotes made straight (exact), then
  lower-cased with end punctuation trimmed (lenient); an ellipsis or a bracketed insertion splits the span into parts
  that must all be found in one text: (1) the participant's words of a concept (codes.jsonl `text`), the cited concept
  first; (2) a label or note (first_order, second_order, note, theme_note): cite.py's REJECT; (3) the coder's case
  account (package/<sub>/case.md); (4) the instrument's own texts (scheme, model, fourth-order themes, dimensions,
  findings, propositions, branches, D6 proposals); (5) the operator's and the instrument's instructions (stages,
  contract, method, standing instructions, writing, fleet, schema, asks, the principal investigator's answers and
  sources, the shelves' text files); (6) nothing.
- A defect: a cited concept quote whose words the cited concept does not hold (another concept's, a label's, or
  nothing). Uncited spans that resolve to nothing are listed for reading, not counted as defects by script.
- The five spot-checks: drawn with random.Random(int(out/seed.txt, 16)) from cited concept quotes that resolve to their
  cited concept, then checked by hand with cite.py --room --code in the audit section.
"""
import collections, glob, json, os, random, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
SKIP = re.compile(r"^(_probe|_transcripts|_snap|_views|_wiki|_fleet_raw|_packets-|handoff-D|field-packages-|readers-C5|"
                  r"_answers|sources-from-J|_analysis|audit-E1|DROPS|_mem_|_cite_)")
OPEN, CLOSE = "\"“", "\"”"
CITE_C = re.compile(r"^[^\n]{0,80}?[\[(`\s]([A-Za-z0-9_]{2,})[/:](c\d{4,5})\b")
CITE_I = re.compile(r"^[^\n]{0,80}?\(`([a-z0-9]{6,7})`\)")
SPLIT = re.compile(r"\.\.\.|…|\[[^\]]*\]")
TOK = re.compile(r"[a-z0-9]+")


def quotes(line):
    """Pair the line's straight double quotes in turn, and each curly opening quote with the next curly closing one
    (so a quote nested in another of the other kind is found too); yield (start, end, span), 6 to 400 characters."""
    for op, cl in (('"', '"'), ("“", "”")):
        i, n = 0, len(line)
        while i < n:
            if line[i] == op:
                j = line.find(cl, i + 1)
                if j < 0:
                    break
                if 6 <= j - i - 1 <= 400:
                    yield i, j + 1, line[i + 1:j]
                i = j + 1
            else:
                i += 1


def tail_of(line, e):
    """The 90 characters after a quote, cut at the next double quote: a citation belongs to the quote it follows."""
    t = line[e:e + 90]
    k = min([x for x in (t.find('"'), t.find("“"), t.find("”")) if x >= 0] or [len(t)])
    return t[:k]


def norm(s):
    s = s.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    return " ".join(s.split())


def lenient(s):
    return norm(s).lower().strip(" ,.;:!?'\"()")


class Index:
    """docs: list of (key, text). Finds the docs whose text holds a span, by the rarest interior token."""
    def __init__(self, docs):
        self.keys = [k for k, _t in docs]
        self.pos = {}
        for i, k in enumerate(self.keys):
            self.pos.setdefault(k, i)
        self.exact = [norm(t) for _k, t in docs]
        self.low = [x.lower() for x in self.exact]
        self.post = collections.defaultdict(list)
        for i, t in enumerate(self.low):
            for w in set(TOK.findall(t)):
                self.post[w].append(i)

    def find(self, span, only=None):
        parts = [p for p in SPLIT.split(span) if TOK.search(p.lower())]
        if len(parts) <= 1:
            return self.find1(parts[0] if parts else span, only)
        lvl, keys = self.find1(max(parts, key=len), only)
        if not lvl:
            return None, []
        keep = [k for k in keys if all(self.find1(p, [self.pos[k]])[0] for p in parts)]
        return (lvl + " (in parts)", keep) if keep else (None, [])

    def find1(self, span, only=None):
        ex, le = norm(span), lenient(span)
        toks = TOK.findall(le)
        inner = toks[1:-1] if len(toks) > 2 else []
        if only is not None:
            cand = only
        elif inner:
            cand = min((self.post.get(w, []) for w in inner), key=len)
        else:
            cand = range(len(self.keys))
        hits = [i for i in cand if ex in self.exact[i]]
        if hits:
            return "exact", [self.keys[i] for i in hits]
        hits = [i for i in cand if le and le in self.low[i]]
        return ("lenient", [self.keys[i] for i in hits]) if hits else (None, [])


def jl(p):
    out = []
    for l in open(p, encoding="utf-8"):
        if l.strip():
            try:
                out.append(json.loads(l))
            except ValueError:
                pass
    return out


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


def main():
    codes = jl(os.path.join(ROOT, "package", "store", "codes.jsonl"))
    themes = jl(os.path.join(ROOT, "package", "store", "themes.jsonl"))
    words = Index([("%s/%s" % (c["sub"], c["code_id"]), c.get("text") or "") for c in codes])
    lower_key = {k.lower(): k for k in words.keys}
    labels = Index([("%s/%s:%s" % (c["sub"], c["code_id"], f), c.get(f) or "") for c in codes
                    for f in ("first_order", "second_order", "note") if c.get(f)] +
                   [("%s/%s:theme_note" % (t["sub"], t["theme_id"]), t.get("theme_note") or "") for t in themes])
    cases = Index([(os.path.basename(os.path.dirname(p)), open(p, encoding="utf-8").read())
                   for p in sorted(glob.glob(os.path.join(ROOT, "package", "*", "case.md")))])
    inst_files = ["scheme_final.jsonl", "model/elements.jsonl", "model/arrows.jsonl", "fourth/fourth.jsonl",
                  "dimensions.jsonl", "findings.jsonl", "propositions.jsonl", "branches.jsonl", "branches-D5.jsonl",
                  "proposals-D6.jsonl", "adaptations.jsonl", "adaptations-recheck.jsonl"]
    inst = Index([(f, s) for f in inst_files if os.path.exists(os.path.join(OUT, f))
                  for r in jl(os.path.join(OUT, f)) for s in strings(r)])
    op_paths = (glob.glob(os.path.join(ROOT, "stages", "*.md")) + glob.glob(os.path.join(ROOT, "*.md")) +
                glob.glob(os.path.join(OUT, "_answers", "*.md")) + glob.glob(os.path.join(OUT, "sources-from-J", "*")) +
                glob.glob(os.path.join(ROOT, "shelves", "**", "*.md"), recursive=True) +
                glob.glob(os.path.join(ROOT, "shelves", "**", "*.txt"), recursive=True) + [os.path.join(OUT, "asks.jsonl")])
    ops = Index([(os.path.relpath(p, ROOT), open(p, encoding="utf-8", errors="replace").read())
                 for p in op_paths if os.path.isfile(p)])

    files = []
    for p in sorted(glob.glob(os.path.join(OUT, "**", "*.md"), recursive=True)):
        rel = os.path.relpath(p, OUT)
        if not SKIP.match(rel):
            files.append((rel, "md"))
    for pat in ("*.jsonl", "model/*.jsonl", "fourth/*.jsonl"):
        for p in sorted(glob.glob(os.path.join(OUT, pat))):
            rel = os.path.relpath(p, OUT)
            if not SKIP.match(rel):
                files.append((rel, "jsonl"))

    per_file = {}
    defects, unresolved, good = [], [], []
    for rel, kind in files:
        cnt = collections.Counter()
        p = os.path.join(OUT, rel)
        if kind == "md":
            units = [(n, line) for n, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1)]
        else:
            units = [(n, s) for n, r in enumerate(jl(p), 1) for s in strings(r)]
        for n, line in units:
            for _s, e, span in quotes(line):
                tail = tail_of(line, e)
                mc, mi = CITE_C.match(tail), CITE_I.match(tail)
                if kind == "jsonl" and not mc:
                    continue
                if not mc and not mi and len(TOK.findall(span.lower())) < 5:
                    continue
                rec = {"file": rel, "line": n, "quote": span}
                if mc:
                    cite = "%s/%s" % (mc.group(1), mc.group(2))
                    rec["cite"] = cite
                    key = lower_key.get(cite.lower())
                    lvl, hits = words.find(span, only=[words.pos[key]]) if key else (None, [])
                    if lvl:
                        rec["class"] = "concept (cited)" if lvl == "exact" else "concept (cited, %s)" % lvl
                        good.append(rec)
                    else:
                        lvl, hits = words.find(span)
                        if lvl:
                            rec["class"], rec["held_by"] = "concept (another)", hits[:3]
                        else:
                            l2, h2 = labels.find(span)
                            if l2:
                                rec["class"], rec["held_by"] = "label or note", h2[:3]
                            else:
                                l3, h3 = cases.find(span)
                                l4, h4 = (None, []) if l3 else inst.find(span)
                                rec["class"] = ("case account" if l3 else
                                                "instrument text beside a concept citation" if l4 else "nothing")
                                if l3 or l4:
                                    rec["held_by"] = (h3 or h4)[:3]
                        rec["unknown_citation"] = key is None
                        defects.append(rec)
                    cnt[rec["class"]] += 1
                    continue
                if mi:
                    rec["cite"] = "`%s`" % mi.group(1)
                order = (("concept", words), ("label or note", labels), ("case account", cases),
                         ("instrument text", inst), ("instructions or operator", ops))
                for name, ix in order:
                    lvl, hits = ix.find(span)
                    if lvl:
                        rec["class"], rec["held_by"] = name + ("" if lvl == "exact" else " (%s)" % lvl), hits[:3]
                        break
                else:
                    rec["class"] = "nothing"
                    unresolved.append(rec)
                cnt[("item-cited " if mi else "uncited ") + rec["class"]] += 1
        if cnt:
            per_file[rel] = dict(cnt)
    tot = collections.Counter()
    for c in per_file.values():
        tot.update(c)
    seed = open(os.path.join(OUT, "seed.txt")).read().split()[0]
    rnd = random.Random(int(seed, 16))
    five = rnd.sample(good, 5) if len(good) >= 5 else good
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1a):")[1].strip(),
                      "files_scanned": len(files), "files_with_quotes": len(per_file), "totals": dict(sorted(tot.items())),
                      "cited_concept_quotes": len(good) + len(defects), "cited_resolving_to_cited": len(good),
                      "defects_n": len(defects), "defects_by_class": dict(collections.Counter(d["class"] for d in defects)),
                      "defects": defects,
                      "uncited_unresolved_n": len(unresolved), "uncited_unresolved": unresolved,
                      "spot_check_seed": seed, "spot_check_five": five, "per_file": per_file},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
