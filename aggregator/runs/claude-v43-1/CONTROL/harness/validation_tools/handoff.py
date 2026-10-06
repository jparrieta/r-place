#!/usr/bin/env python3
"""handoff.py, v38: stage D1's builder. Writes the handoff folder the labelers read in Codex and
the verdict packets the fleet reads on the gateway. It writes no judgement: the prose of the model
and the expectations are yours, and it copies them in.

    python3 tools/handoff.py D [--root .] [--out out]              the handoff folder and the packets
    python3 tools/handoff.py D --recheck sub1,sub2 [--root .]       handoff-D/recheck/ for D3
    python3 tools/handoff.py D --verdict-only                       the verdict packets alone
    python3 tools/handoff.py --hash [--out out]                      print the model version and stop

What you write before running it (stage D1 §1):
    out/MODEL-D1.md          the global model as prose with ids, cut to the ceiling you declare in
                              notes-D1.md; copied verbatim to handoff-D/MODEL.md
    out/EXPECTATIONS-D1.jsonl  one line per room of the analysed set: sub, expect_instantiate,
                              expect_absent, from, why, and not_testable_here where rule 6 says so;
                              copied to sealed/EXPECTATIONS.jsonl, outside every served folder

What it reads: out/model/{elements,arrows}.jsonl (the frozen model), the current scheme file,
out/fourth/fourth.jsonl, out/dimensions.jsonl, out/assignments_final.jsonl, out/dropped.jsonl,
prior.md §8, the store (rooms, themes, codes), the
coder documents in package/<sub>/, the forests in trees/<sub>.md, and the templates in
handoff/ (RETURN-D.md, TASK-template.md, HANDLER.md) and FLEET.md §3 for the criterion.

What it writes, under out/:
    handoff-D/VERSION            the model version: sha256 over model/elements.jsonl then
                                  model/arrows.jsonl, each file's bytes preceded by its name and a
                                  newline (the definition checks/stage_D1.py fixes)
    handoff-D/VOCABULARY.json    elements (id, kind, statement, tier, dimension) and arrows (id, kind, from,
                                  to, mechanism), each with status tentative where it is one,
                                  third, fourth, dimensions (id, name), version
    handoff-D/MODEL.md, LADDER.md, RETURN-D.md, HANDLER.md
    handoff-D/tasks/<sub>/       TASK.md, RETURN-D.md, VOCABULARY.json, VERSION, LADDER.md,
                                  MODEL.md (the global model with an entry, from the served fields only, for each element the
                                  room's themes were placed under, appended), case.md, codes.jsonl,
                                  themes.jsonl, brief.md, forest.md,
                                  placements.jsonl
    handoff-D/tasks/index.tsv    sub, items_in_window, payload_bytes, codes, themes; size ascending
    verdict-D/<sub>.md           per room: the criterion verbatim, the floor and the off-platform
                                  threshold from prior.md with the room's own figures beside them,
                                  the model, the room's second-order themes with notes and
                                  placements, the served digest, the end line
    verdict-D/RETURN-D2v.md      the verdict return specification, and RETURN-D2v.schema.json (tools/dreturn.py),
                                  which fleet.py validates every line against
    verdict-D/recheck/           the re-check's verdict packets (--recheck), from out/MODEL-D3.md
    sealed/FIELD.jsonl           the tentative entries and where they came from (stage C4), never served;
                                  stages D3 and E1 read it
    handoff-D.sha256             the folder hash (sha256 over "<path>  <sha256>" lines, recheck/
                                  excluded); also written to RUN.json under "handoff_D"

A room whose task cannot be built (no case.md, no codes) is not invented: it is listed in
handoff-D/UNBUILT.tsv and on stdout, and you carry it to handback-D1.md.
"""
import argparse, collections, hashlib, json, os, random, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vlib
PACKET_CEILING = 50 * 1024
ELEMENT_FIELDS = ("id", "kind", "statement", "tier", "dimension")
ARROW_FIELDS = ("id", "kind", "from", "to", "mechanism")
COPY_DOCS = ("case.md", "brief.md")
END_V = "END-OF-VERDICT"


def jl(p):
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def wjl(p, rows):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def wtxt(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def sha_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def model_hash(out):
    sys.path.insert(0, HERE)
    import vlib
    return vlib.model_hash(out)


def folder_hash(folder, exclude=("recheck",)):
    rows = []
    for d, dirs, files in os.walk(folder):
        dirs[:] = sorted(x for x in dirs if x not in exclude)
        for f in sorted(files):
            p = os.path.join(d, f)
            rows.append("%s  %s\n" % (os.path.relpath(p, folder), sha_file(p)))
    return hashlib.sha256("".join(rows).encode("utf-8")).hexdigest()


def template(root, name):
    for p in (os.path.join(root, "handoff", name), os.path.join(HERE, "..", "handoff", name)):
        if os.path.exists(p):
            return open(p, encoding="utf-8").read()
    sys.exit("no template %s in handoff/" % name)


def criterion(root):
    for p in (os.path.join(root, "FLEET.md"), os.path.join(HERE, "..", "FLEET.md")):
        if os.path.exists(p):
            t = open(p, encoding="utf-8").read()
            m = re.search(r"\*\*The verdict's criterion\.\*\*(.*?)`RETURN-D\.md` carries this text verbatim\.", t, re.S)
            if m:
                return " ".join(m.group(1).split())
    sys.exit("FLEET.md §3's verdict criterion was not found; the packets carry it verbatim")


def prior_s8(root, out):
    for p in (os.path.join(out, "prior.md"), os.path.join(root, "prior.md")):
        if os.path.exists(p):
            t = open(p, encoding="utf-8").read()
            m = re.search(r"##\s*8\..*?(?=\n##\s|\Z)", t, re.S)
            if m:
                return m.group(0).strip()
    return None


class Model:
    def __init__(self, root, out):
        self.root, self.out = root, out
        S = os.path.join(root, "package", "store")
        self.rooms = {r["sub"]: r for r in jl(os.path.join(S, "rooms.jsonl"))}
        dropped = {r["sub"] for r in jl(os.path.join(out, "dropped.jsonl"))}
        if not os.path.exists(os.path.join(out, "dropped.jsonl")):
            sys.exit("out/dropped.jsonl is absent: there is no analysed set (stage A1 §4)")
        self.analysed = sorted(set(self.rooms) - dropped)
        self.themes = collections.defaultdict(list)
        for t in jl(os.path.join(S, "themes.jsonl")):
            self.themes[t["sub"]].append(t)
        self.codes = collections.defaultdict(list)
        for c in jl(os.path.join(S, "codes.jsonl")):
            self.codes[c["sub"]].append(c)
        self.els = [e for e in jl(os.path.join(out, "model", "elements.jsonl")) if e.get("status") != "withdrawn"]
        self.ars = [a for a in jl(os.path.join(out, "model", "arrows.jsonl"))
                    if a.get("status") != "withdrawn" and (a.get("in_model", True) or a.get("status") == "tentative")]
        if not self.els:
            sys.exit("out/model/elements.jsonl is empty or absent: nothing to hand off")
        self.scheme = {}
        for f in ("scheme_v2.jsonl", "scheme_final.jsonl", "scheme_current.jsonl", "scheme.jsonl"):
            rows = jl(os.path.join(out, f))
            if rows:
                self.scheme = {r["id"]: r for r in rows}
                break
        self.fourth = {r["id"]: r for r in jl(os.path.join(out, "fourth", "fourth.jsonl"))}
        self.dims = {r["id"]: r for r in jl(os.path.join(out, "dimensions.jsonl"))}
        self.fourth_of = {m: f for f, r in self.fourth.items() for m in r.get("members", [])}
        self.dim_of = {m: d for d, r in self.dims.items() for m in r.get("members", [])}
        self.placed = {}
        for r in jl(os.path.join(out, "assignments_final.jsonl")):
            so = r.get("third_order") or []
            self.placed[(r["sub"], r.get("theme_id"))] = so if isinstance(so, list) else [so]
        if not self.placed:
            sys.exit("out/assignments_final.jsonl is empty or absent: no placements to lift")
        self.version = model_hash(out)

    @staticmethod
    def _served(r, fields):
        """What a labeler sees of an entry: the fields, and `status: tentative` where it is one; never where
        it came from (the from-field mark stays in out/sealed/FIELD.jsonl, J 2026-09-29)."""
        d = {k: r.get(k) for k in fields}
        if fields is ARROW_FIELDS and r.get("statement"):
            d["statement"] = r["statement"]
        if r.get("status") == "tentative":
            d["status"] = "tentative"
        return d

    def served_entry(self, i):
        """One entry as the labeler may read it: id, kind, statement, tier, dimension (an arrow: its ends and
        mechanism), and tentative where it is one."""
        e = next((x for x in self.els + self.ars if x.get("id") == i), None)
        if e is None:
            return None
        if e in self.ars:
            s = "## %s (%s arrow)\n\n%s -> %s. %s" % (i, e.get("kind"), e.get("from"), e.get("to"),
                                                     e.get("mechanism") or e.get("statement") or "")
        else:
            s = "## %s (%s)\n\n%s\n\ntier %s; dimension %s" % (i, e.get("kind"), e.get("statement"), e.get("tier"),
                                                            e.get("dimension"))
        return s + ("\n\ntentative" if e.get("status") == "tentative" else "")

    def tentative(self):
        return [e for e in self.els + self.ars if e.get("status") == "tentative"]

    def vocabulary(self):
        return {"elements": [self._served(e, ELEMENT_FIELDS) for e in self.els],
                "arrows": [self._served(a, ARROW_FIELDS) for a in self.ars],
                "third": [{"id": i, "name": r.get("name") or r.get("label")} for i, r in sorted(self.scheme.items())],
                "fourth": [{"id": i, "name": r.get("name") or r.get("label")} for i, r in sorted(self.fourth.items())],
                "dimensions": [{"id": i, "name": r.get("label") or r.get("name")} for i, r in sorted(self.dims.items())],
                "version": self.version}

    def lift(self, sub, tid):
        t3 = [x for x in self.placed.get((sub, tid), []) if x]
        t4 = sorted({self.fourth_of[x] for x in t3 if x in self.fourth_of})
        d = sorted({self.dim_of[x] for x in t4 if x in self.dim_of})
        return t3, t4, d

    def placements(self, sub):
        rows = []
        for t in sorted(self.themes.get(sub, []), key=lambda t: t["theme_id"]):
            t3, t4, d = self.lift(sub, t["theme_id"])
            rows.append({"sub": sub, "theme_id": t["theme_id"], "second_order": t.get("second_order"),
                         "third_order": t3 or None, "fourth_order": t4 or None, "dimension": d or None})
        return rows

    def room_elements(self, sub):
        """The entries appended to this room's MODEL.md: those on any tier the room's themes lift to
        (third, fourth or dimension), the arrows between them, and every tentative entry and every entry on a
        form-pass tier (FP-), which go to every room: no theme lifts to either (audit 2026-09-29b, H8)."""
        tiers = set()
        for t in self.themes.get(sub, []):
            t3, t4, d = self.lift(sub, t["theme_id"])
            tiers |= set(t3) | set(t4) | set(d)
        on = lambda e: any(x in tiers for x in (e.get("tier") if isinstance(e.get("tier"), list) else [e.get("tier")]))
        fp = lambda e: any(vlib.FORM_PASS.match(str(x)) for x in (e.get("tier") if isinstance(e.get("tier"), list) else [e.get("tier")]))
        ids = [e["id"] for e in self.els if on(e) or fp(e) or e.get("status") == "tentative"]
        ids += [a["id"] for a in self.ars if a.get("status") == "tentative" or (a.get("from") in ids and a.get("to") in ids)]
        return ids

    def ladder(self, per=3, seed=0):
        """Dimension > fourth > third, with `per` representative concepts per third-order theme,
        drawn at random under the seed across rooms (the words, the concept, the room's theme)."""
        rnd = random.Random(seed)
        by_t3 = collections.defaultdict(list)
        theme_by = {(t["sub"], t["theme_id"]): t for ts in self.themes.values() for t in ts}
        for sub, cs in self.codes.items():
            for c in cs:
                for t3 in self.placed.get((sub, c.get("theme_id")), []):
                    by_t3[t3].append(c)
        L = ["# LADDER: the coding table from quote to aggregate dimension", "",
             "Read it to know what each dimension is made of. Quotes are participants' words from several",
             "rooms; the room is named only so the quote can be traced, and you cite only your own room.", ""]
        dims = sorted(self.dims) or [None]
        seen4 = set()
        for d in dims:
            dn = (self.dims.get(d) or {}).get("label") or (self.dims.get(d) or {}).get("name") or ""
            L.append("## %s %s" % (d or "(no dimension)", dn))
            L.append("")
            for f4 in sorted(self.fourth):
                if (self.dim_of.get(f4) or None) != d:
                    continue
                seen4.add(f4)
                r4 = self.fourth[f4]
                L.append("### %s %s" % (f4, r4.get("name") or ""))
                L.append("")
                L.append("| third-order theme | quote | first-order concept | second-order theme |")
                L.append("|---|---|---|---|")
                for t3 in r4.get("members", []):
                    cs = by_t3.get(t3, [])
                    pick = rnd.sample(cs, min(per, len(cs))) if cs else []
                    name = (self.scheme.get(t3) or {}).get("name") or ""
                    if not pick:
                        L.append("| %s %s | (no concept placed) | | |" % (t3, name))
                    for c in pick:
                        t = theme_by.get((c["sub"], c.get("theme_id"))) or {}
                        q = " ".join(str(c.get("text") or "").split()).replace("|", "/")[:220]
                        L.append("| %s %s | \"%s\" [%s/%s] | %s | %s |" % (
                            t3, name, q, c["sub"], c["code_id"], (c.get("first_order") or "").replace("|", "/"),
                            (t.get("second_order") or "").replace("|", "/")))
                L.append("")
        return "\n".join(L) + "\n"


def build_task(M, sub, tdir, top, ret, vocab_txt, version, ladder, task_tpl):
    D = os.path.join(M.root, "package", sub)
    if not M.codes.get(sub) or not os.path.exists(os.path.join(D, "case.md")):
        return "no %s" % ("codes in the store" if not M.codes.get(sub) else "case.md in package/%s" % sub)
    os.makedirs(tdir, exist_ok=True)
    wtxt(os.path.join(tdir, "TASK.md"), task_tpl.replace("<sub>", sub))
    wtxt(os.path.join(tdir, "RETURN-D.md"), ret)
    wtxt(os.path.join(tdir, "VOCABULARY.json"), vocab_txt)
    wtxt(os.path.join(tdir, "VERSION"), version + "\n")
    wtxt(os.path.join(tdir, "LADDER.md"), ladder)
    pages = []
    for i in M.room_elements(sub):
        e = M.served_entry(i)          # from the served fields only: a wiki page carries other rooms' codes and
        if e:                          # adaptations, and a labeler reads its own room and nothing else (rule 7)
            pages.append(e)
    model = top.rstrip() + "\n"
    if pages:
        model += ("\n---\n\n# The elements this room's themes were placed under\n\n" + "\n\n".join(pages) + "\n")
    wtxt(os.path.join(tdir, "MODEL.md"), model)
    for f in COPY_DOCS:
        s = os.path.join(D, f)
        if os.path.exists(s):
            shutil.copyfile(s, os.path.join(tdir, f))
    fp = os.path.join(M.root, "trees", "%s.md" % sub)
    if os.path.exists(fp):
        shutil.copyfile(fp, os.path.join(tdir, "forest.md"))
    keep_c = ("sub", "code_id", "theme_id", "first_order", "text", "item_id", "thread_id", "coord", "hour", "author")
    wjl(os.path.join(tdir, "codes.jsonl"), [{k: c.get(k) for k in keep_c} for c in M.codes[sub]])
    keep_t = ("sub", "theme_id", "second_order", "theme_note", "n_codes", "first_hour", "last_hour")
    wjl(os.path.join(tdir, "themes.jsonl"), [{k: t.get(k) for k in keep_t} for t in M.themes.get(sub, [])])
    wjl(os.path.join(tdir, "placements.jsonl"), M.placements(sub))
    return None


def dir_bytes(d):
    return sum(os.path.getsize(os.path.join(a, f)) for a, _, fs in os.walk(d) for f in fs)


def return_D2v():
    return """# RETURN-D2v. What a verdict reader returns.

You read one community's second-order themes against a global model of how communities organized
during the event. Return one line of JSON, then the end marker on its own line, and nothing else.

`verdict` is one of `composes`, `composes-with-residue`, `does-not-compose`, `cannot-tell`, by the
criterion in your packet. `themes` lists the room's theme ids your verdict rests on, and
`concepts` the unused concept ids it rests on (an empty list when none). `residue` lists the
themes or concepts carrying organizing the model lacks, and is null unless the verdict is
`composes-with-residue`. `cannot_tell_under` is `coded-share`, `off-platform`, `both`,
`missing-decisive-evidence`, `conflicting-evidence` or `other-evidence-limit` when the
verdict is `cannot-tell`, and null otherwise. Thresholds are prompts for evidence review, not sufficient
conditions for cannot-tell. Explain the decisive missing or conflicting evidence in `sentence`. `sentence` is one sentence in the criterion's
terms. `served` is the digest printed at the end of your packet, copied exactly.

```
{"sub": "<room>", "reader": "<your reader id, or r1>", "verdict": "composes", "themes": ["t03", "t07"], "concepts": ["c0041"], "residue": null, "cannot_tell_under": null, "sentence": "The room restates in the model's terms and its unused concepts show nothing the model lacks.", "served": "<the digest>"}
%s
```
""" % END_V


def cited_codes(M):
    """Every concept id (sub:cNNNN) an element or arrow cites anywhere in its record."""
    blob = json.dumps(M.els + M.ars)
    return set(re.findall(r"([A-Za-z0-9_]+:c\d{3,5})", blob))


def verdict_packet(M, sub, crit, s8, top, cited=None, seed=0, sample=40):
    r = M.rooms.get(sub, {})
    n_codes = r.get("codes") or len(M.codes.get(sub, []))
    off = r.get("n_off_platform")
    L = ["# Verdict packet: one community", "",
         "## The criterion (FLEET.md §3, verbatim)", "", crit, "",
         "## The thresholds for cannot-tell (prior.md §8), and this room's figures", "",
         s8 or "(prior.md §8 was not found; say so in your sentence)", "",
         "This room: %d first-order concepts in the store; %s off-platform pointers. Read these "
         "figures; do not estimate them." % (n_codes, off), "",
         "## The model", "", top.strip(), "",
         "## This room's second-order themes and where each was placed", ""]
    unplaced = set()
    for p in M.placements(sub):
        if not (p["third_order"] or []):
            unplaced.add(p["theme_id"])
        L.append("- **%s** %s. Placed: third %s; fourth %s; dimension %s." % (
            p["theme_id"], p.get("second_order") or "",
            ",".join(p["third_order"] or []) or "none", ",".join(p["fourth_order"] or []) or "none",
            ",".join(p["dimension"] or []) or "none"))
    cited = cited if cited is not None else cited_codes(M)
    codes = M.codes.get(sub, [])
    a_ = [c for c in codes if c.get("theme_id") in unplaced]
    rest = [c for c in codes if c.get("theme_id") not in unplaced and "%s:%s" % (sub, c["code_id"]) not in cited]
    rnd = random.Random("%s:%s" % (seed, sub))
    b_ = sorted(rnd.sample(rest, min(sample, len(rest))), key=lambda c: c["code_id"])
    def line(c):
        return "- %s (theme %s) %s: \"%s\"" % (c["code_id"], c.get("theme_id"), c.get("first_order") or "",
                                               " ".join(str(c.get("text") or "").split())[:240])
    L += ["", "## The concepts the model did not use", "",
          "Of themes placed nowhere (%d concepts, all listed):" % len(a_), ""] + [line(c) for c in a_[:120]]
    if len(a_) > 120:
        L.append("- (%d more of these, not listed)" % (len(a_) - 120))
    L += ["", "Of placed themes, that no element cites (%d in all; a seeded sample of %d):" % (len(rest), len(b_)), ""]
    L += [line(c) for c in b_]
    body = "\n".join(L) + "\n"
    dig = hashlib.sha256(body.encode("utf-8")).hexdigest()
    body += ("\nYour `served` value: %s\n\nThis is the end of the packet. Confirm you reached it by "
             "returning the line and the end marker. END OF PACKET\n" % dig)
    return body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", nargs="?")
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default=None)
    ap.add_argument("--recheck", default=None, help="comma-separated rooms for handoff-D/recheck/")
    ap.add_argument("--verdict-only", action="store_true")
    ap.add_argument("--hash", action="store_true")
    ap.add_argument("--ladder-per", type=int, default=3)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    out = a.out or os.path.join(a.root, "out")
    if a.hash:
        print(model_hash(out) or "no model")
        return 0
    if a.stage != "D":
        sys.exit("handoff.py builds stage D's folder: python3 tools/handoff.py D")
    M = Model(a.root, out)
    top_p = os.path.join(out, "MODEL-D3.md" if a.recheck else "MODEL-D1.md")
    if not os.path.exists(top_p):
        sys.exit("out/%s is absent: write the model as prose with ids first (%s)" % (
            os.path.basename(top_p), "stage D3 §5: the revised model the re-check reads" if a.recheck else "stage D1 §1"))
    top = open(top_p, encoding="utf-8").read()
    absent = [e["id"] for e in M.els + M.ars if e["id"] not in top]
    if absent:
        print("warning: MODEL-D1.md never names %d element(s) or arrow(s): %s" % (len(absent), absent[:10]))
    crit = criterion(a.root)
    s8 = prior_s8(a.root, out)
    V = os.path.join(out, "verdict-D", "recheck") if a.recheck else os.path.join(out, "verdict-D")
    rooms = M.analysed if not a.recheck else [s for s in a.recheck.split(",") if s]
    if True:                       # the verdict packets: every room at D1, the re-check's rooms at D3 (§5)
        os.makedirs(V, exist_ok=True)
        wtxt(os.path.join(V, "RETURN-D2v.md"), return_D2v())
        sys.path.insert(0, HERE)
        import dreturn
        wtxt(os.path.join(V, "RETURN-D2v.schema.json"), json.dumps(dreturn.verdict_schema(), indent=1) + "\n")
        big = []
        cited = cited_codes(M)
        for sub in rooms:
            pk = verdict_packet(M, sub, crit, s8, top, cited=cited, seed=a.seed)
            wtxt(os.path.join(V, "%s.md" % sub), pk)
            if len(pk.encode("utf-8")) > PACKET_CEILING:
                big.append((sub, len(pk.encode("utf-8"))))
        # one verdict line per room: fleet.py validates the count against this (and never sends
        # RETURN-D2v.md as a packet)
        with open(os.path.join(V, "MANIFEST.json"), "w") as f:
            json.dump({sub: {"items": 1} for sub in rooms}, f, indent=1)
        print("%s/: %d packets%s" % (os.path.relpath(V, out), len(rooms), "; over 50 KB: %s" % big[:5] if big else ""))
        if a.verdict_only:
            return 1 if big else 0
    H = os.path.join(out, "handoff-D", "recheck") if a.recheck else os.path.join(out, "handoff-D")
    if os.path.exists(os.path.join(H, "tasks")):
        sys.exit("%s/tasks exists: a handoff is written once per version; move it aside by hand if you "
                 "mean to rebuild" % os.path.relpath(H, out))
    vocab = M.vocabulary()
    vocab_txt = json.dumps(vocab, ensure_ascii=False, indent=1)
    ret = template(a.root, "RETURN-D.md")
    task_tpl = template(a.root, "TASK-template.md")
    ladder = M.ladder(a.ladder_per, a.seed)
    wtxt(os.path.join(H, "VERSION"), M.version + "\n")
    wtxt(os.path.join(H, "VOCABULARY.json"), vocab_txt)
    wtxt(os.path.join(H, "MODEL.md"), top)
    wtxt(os.path.join(H, "LADDER.md"), ladder)
    wtxt(os.path.join(H, "RETURN-D.md"), ret)
    wtxt(os.path.join(H, "HANDLER.md"), template(a.root, "HANDLER.md"))
    # the field's entries, sealed: where a tentative entry came from never reaches a labeler (J, 2026-09-29);
    # stages D3 and E1 read it and report the field's entries apart
    os.makedirs(os.path.join(out, "sealed"), exist_ok=True)
    if not a.recheck and not os.path.exists(os.path.join(out, "sealed", "FIELD.jsonl")):
        wtxt(os.path.join(out, "sealed", "FIELD.jsonl"), "".join(
        json.dumps({"id": e.get("id"), "kind": e.get("kind"), "origin": e.get("origin"), "statement": e.get("statement"),
                        "field_support": e.get("field_support")}, ensure_ascii=False) + "\n" for e in M.tentative()))
    if not a.recheck:            # sealed beside the field's entries, out of the handler's and the labelers' reach
        ep = os.path.join(out, "EXPECTATIONS-D1.jsonl")
        if not os.path.exists(ep):
            sys.exit("out/EXPECTATIONS-D1.jsonl is absent: write the expectations before the handoff (stage D1 §1)")
        shutil.copyfile(ep, os.path.join(out, "sealed", "EXPECTATIONS.jsonl"))
    unbuilt, idx = [], []
    for sub in rooms:
        why = build_task(M, sub, os.path.join(H, "tasks", sub), top, ret, vocab_txt, M.version, ladder, task_tpl)
        if why:
            unbuilt.append((sub, why))
            continue
        r = M.rooms.get(sub, {})
        idx.append((sub, r.get("items_in_window") or 0, dir_bytes(os.path.join(H, "tasks", sub)),
                    len(M.codes.get(sub, [])), len(M.themes.get(sub, []))))
    idx.sort(key=lambda x: (x[1], x[2]))
    wtxt(os.path.join(H, "tasks", "index.tsv"), "sub\titems_in_window\tpayload_bytes\tcodes\tthemes\n" +
         "".join("%s\t%d\t%d\t%d\t%d\n" % x for x in idx))
    if unbuilt:
        wtxt(os.path.join(H, "UNBUILT.tsv"), "sub\twhy\n" + "".join("%s\t%s\n" % u for u in unbuilt))
    fh = folder_hash(H)
    name = "handoff-D-recheck.sha256" if a.recheck else "handoff-D.sha256"
    wtxt(os.path.join(out, name), fh + "\n")
    rp = os.path.join(a.root, "RUN.json")
    run = json.load(open(rp)) if os.path.exists(rp) else {}
    run.setdefault("handoff_D", {})["recheck" if a.recheck else "first"] = {
        "version": M.version, "folder_hash": fh, "tasks": len(idx), "unbuilt": len(unbuilt)}
    json.dump(run, open(rp, "w"), indent=1)
    pay = sorted(x[2] for x in idx)
    med = pay[len(pay) // 2] if pay else 0
    p90 = pay[int(0.9 * (len(pay) - 1))] if pay else 0
    print("%s: %d tasks, %d unbuilt; VERSION %s; folder hash %s" % (os.path.relpath(H, out), len(idx), len(unbuilt), M.version, fh))
    print("payload bytes: median %d, p90 %d, largest %d (write these in notes-D1.md §3)" % (med, p90, pay[-1] if pay else 0))
    for u in unbuilt:
        print("  unbuilt: %s (%s); carry it to handback-D1.md" % u)
    return 0


if __name__ == "__main__":
    sys.exit(main())
