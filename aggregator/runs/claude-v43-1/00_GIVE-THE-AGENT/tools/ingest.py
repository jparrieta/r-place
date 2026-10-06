#!/usr/bin/env python3
"""ingest.py, v38: validate the labelers' returns for stage D, compile the ledger and the verdicts.

    python3 tools/ingest.py D [--root .] [--out out] [--drops DROPS/D]            compile (the harness runs it
                                                                                   before the D2 check leg)
    python3 tools/ingest.py D --recheck                                            compile the re-check (D3b)
    python3 tools/ingest.py D --check <sub> [--recheck]                            the handler's per-room check
    python3 tools/ingest.py D --relift                                             re-lift the ledger to the model
                                                                                   as it stands (D3c, before D4)

The rules are tools/dreturn.py's, the same the D2 close-check applies (SCHEMA-adaptations.md §4):
  1. schema: the op is known; the required fields for that op are present; no extra fields
  2. model version: the return's model_version equals the handoff's VERSION; element ids exist in
     VOCABULARY.json and are not withdrawn
  3. concept ids exist in the room's codes in the store; transition ids exist; a source is a theme or
     concept of the room
  4. how (or why) is one sentence, under forty words
  5. portability: condition, statement and how contain no census subreddit name and no proper name from
     the room's lines in out/lexicon-A1.md (relation aside); a failing line is kept with portable false
  6. the end marker {"end": true, "lines": N} matches the count; model-D.md ends with <!-- end -->
  and the room model's own rules (dreturn.model_problems): a grade line, concept citations of the room,
  ids of the vocabulary, every adapted element named; a none line is the whole return.

What the compile writes, under out/:
  adaptations.jsonl (adaptations-recheck.jsonl)   one line per accepted line: id (<sub>-NNN, or R-<sub>-<digest>-NNN
                                                  at the re-check), lift, kind, portable, origin, labeler_run
  rooms/<sub>/model-D.md, rooms/<sub>/run.json    copied from the drop
  verdicts-D.jsonl (verdicts-recheck-D.jsonl)     one line per room: the readers' validated lines from
                                                  _fleet_raw/D2v/ (D3v/ at the re-check) and the labeler's grade
  rooms/<sub>/verdict-D.jsonl                     the room's readers' lines
  ingest-D.md (ingest-D-recheck.md)               the report
and, in the folder root: DROPS/D/UNRETURNED.tsv gains every room the compile rejected, with the rules
it failed (a return is never edited; a rejected room is unreturned); RUN.json gains the D2 counts
(accepted, reissued, unreturned; reissued from run.json's "attempts" above one).
"""
import argparse, collections, datetime, glob, hashlib, json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dreturn

OPS, KIND = dreturn.OPS, dreturn.KIND
OPTIONAL = set(dreturn.OPTIONAL)
one_sentence = dreturn.one_sentence


def jl(p):
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def _run_json(d):
    try:
        r = json.load(open(os.path.join(d, "run.json"), encoding="utf-8"))
        return r if isinstance(r, dict) else {}
    except (OSError, ValueError):
        return {}


def jl_safe(p):
    out = []
    if os.path.exists(p):
        for l in open(p, encoding="utf-8"):
            try:
                r = json.loads(l)
            except ValueError:
                continue
            if isinstance(r, dict):
                out.append(r)
    return out


class Ingest:
    def __init__(self, root, out, drops, recheck):
        self.root, self.out, self.drops, self.recheck = root, out, drops, recheck
        hand = os.path.join(out, "handoff-D", "recheck" if recheck else "")
        self.hand = hand.rstrip("/")
        spec = os.path.join(self.hand, "RETURN-D.md")
        self.require_local = os.path.exists(spec) and "local_status:" in open(spec, encoding="utf-8").read()
        self.version = open(os.path.join(self.hand, "VERSION")).read().strip() \
            if os.path.exists(os.path.join(self.hand, "VERSION")) else None
        if self.version and self.version.startswith("sha256:"):
            self.version = self.version[7:]
        vocab = json.load(open(os.path.join(self.hand, "VOCABULARY.json"))) \
            if os.path.exists(os.path.join(self.hand, "VOCABULARY.json")) else {}
        self.elements = {e["id"]: e for e in list(vocab.get("elements", [])) + list(vocab.get("arrows", []))}
        self.dims = {d["id"] for d in vocab.get("dimensions", [])}
        S = os.path.join(root, "package", "store")
        self.codes = collections.defaultdict(dict)
        self.code_theme = {}
        for c in jl(os.path.join(S, "codes.jsonl")):
            self.codes[c["sub"]][c["code_id"]] = c
            self.code_theme[(c["sub"], c["code_id"])] = c.get("theme_id")
        self.themes = collections.defaultdict(dict)
        for t in jl(os.path.join(S, "themes.jsonl")):
            self.themes[t["sub"]][t["theme_id"]] = t
        self.transitions = collections.defaultdict(set)
        for r in jl(os.path.join(S, "transitions.jsonl")):
            self.transitions[r["sub"]].add(r.get("id"))
        self.rooms = {r["sub"] for r in jl(os.path.join(S, "rooms.jsonl"))}
        self.load_placements()
        self.names = set(s.lower() for s in self.rooms)

    def load_placements(self):
        self.placed = {}
        for r in jl(os.path.join(self.out, "assignments_final.jsonl")):
            so = r.get("third_order")
            self.placed[(r["sub"], r["theme_id"])] = so if isinstance(so, list) else [so]
        self.fourth_of = {}
        for r in jl(os.path.join(self.out, "fourth", "fourth.jsonl")):
            for m in r.get("members", []):
                self.fourth_of[m] = r["id"]
        self.dim_of = {}
        for r in jl(os.path.join(self.out, "dimensions.jsonl")):
            for m in r.get("members", []):
                self.dim_of[m] = r["id"]

    def lexicon(self, sub):
        """Proper names from the analyst's lexicon, out/lexicon-A1.md, this room's lines."""
        p = os.path.join(self.out, "lexicon-A1.md")
        words = set()
        if not os.path.exists(p):
            return words
        for line in open(p, encoding="utf-8"):
            parts = [x for x in re.split(r"\t|\s{2,}", line.strip()) if x]
            if len(parts) < 3 or parts[-2].lower() != sub.lower():
                continue
            m = re.match(r"^\s*[-*]?\s*([A-Za-z][\w'-]{2,})", parts[0])
            if m and m.group(1)[0].isupper():
                words.add(m.group(1).lower())
        return words

    def lift(self, sub, source):
        return dreturn.lift_of(sub, source, self.placed, self.fourth_of, self.dim_of, self.code_theme)

    def line_id(self, sub, index, line):
        if not self.recheck:
            return "%s-%03d" % (sub, index + 1)
        payload = json.dumps({"version": self.version, "line": line}, sort_keys=True, ensure_ascii=False)
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]
        return "R-%s-%s-%03d" % (sub, digest, index + 1)

    def check_room(self, sub):
        errs, lines = [], []
        d = os.path.join(self.drops, sub)
        lp, mp = os.path.join(d, "adaptations.jsonl"), os.path.join(d, "model-D.md")
        if not os.path.exists(lp) or not os.path.exists(mp):
            return ["missing return files"], []
        raw = [l for l in open(lp, encoding="utf-8").read().split("\n") if l.strip()]
        try:
            objs = [json.loads(l) for l in raw]
        except json.JSONDecodeError as e:
            return ["rule 1: invalid JSON: %s" % e], []
        if not all(isinstance(o, dict) for o in objs):
            return ["rule 1: a line is not a JSON object"], []
        if not objs or not objs[-1].get("end"):
            errs.append("rule 6: no end marker")
        else:
            end = objs.pop()
            if end.get("lines") != len(objs):
                errs.append("rule 6: end marker count %s, lines %d" % (end.get("lines"), len(objs)))
        run = _run_json(d)
        lex = self.lexicon(sub)
        if len(objs) > 1 and any(o.get("op") == "none" for o in objs):
            errs.append("rule 1: a none line beside %d other line(s); none is the whole return" % (len(objs) - 1))
        for i, o in enumerate(objs):
            tag = "line %d" % (i + 1)
            op = o.get("op")
            if op not in OPS:
                errs.append("%s: rule 1: unknown op %r" % (tag, op)); continue
            missing = [k for k in OPS[op] if not o.get(k)]
            if op not in ("none", "absent") and not (o.get("evidence") or {}).get("codes"):
                missing.append("evidence.codes")
            errs.extend("%s: rule 1: %s" % (tag, problem) for problem in dreturn.absence_problems(o))
            extra = [k for k in o if k not in OPTIONAL and k != "op"]
            if missing:
                errs.append("%s: rule 1: %s missing %s" % (tag, op, ",".join(missing)))
            if extra:
                errs.append("%s: rule 1: extra fields %s" % (tag, ",".join(extra)))
            mv = o.get("model_version") or run.get("model_version")
            mv = mv[7:] if isinstance(mv, str) and mv.startswith("sha256:") else mv
            if self.version and mv != self.version:
                errs.append("%s: rule 2: model_version %s, handoff %s" % (tag, mv, self.version))
            for key in ("element", "to"):
                v = o.get(key)
                if v and v not in self.elements and v not in self.dims:
                    errs.append("%s: rule 2: unknown id %s" % (tag, v))
                elif v in self.elements and self.elements[v].get("status") == "withdrawn":
                    errs.append("%s: rule 2: withdrawn element %s" % (tag, v))
            for cid in (o.get("evidence") or {}).get("codes", []):
                if str(cid).split(":")[-1] not in self.codes.get(sub, {}):
                    errs.append("%s: rule 3: concept %s not in r/%s" % (tag, cid, sub))
            for tid in (o.get("evidence") or {}).get("transitions", []):
                if tid not in self.transitions.get(sub, set()):
                    errs.append("%s: rule 3: transition %s not in r/%s" % (tag, tid, sub))
            src = o.get("source") or (o.get("from") if op == "link" else None)
            if src:
                node = src.split(":", 1)[1] if ":" in src else src
                if node not in self.themes.get(sub, {}) and node not in self.codes.get(sub, {}):
                    errs.append("%s: rule 3: source %s is not a theme or concept of r/%s" % (tag, src, sub))
            if op != "none" and not one_sentence(o.get("how") or o.get("why")):
                errs.append("%s: rule 4: how/why is not one sentence under forty words" % tag)
            text = " ".join(str(o.get(k) or "") for k in ("condition", "statement", "how", "why")).lower()
            hits = [n for n in self.names if n != sub.lower() and len(n) >= 3 and re.search(r"\b%s\b" % re.escape(n), text)]
            hits += [w for w in lex if re.search(r"\b%s\b" % re.escape(w), text)]
            if re.search(r"\b%s\b" % re.escape(sub.lower()), text):
                hits.append(sub)
            lines.append((o, not hits, sorted(set(hits))))
        model = open(mp, encoding="utf-8").read()
        adapted = {o.get("element") or (o.get("to") if o.get("op") == "link" else None)
                   for o, _p, _h in lines if o.get("op") != "none"}
        errs += dreturn.model_problems(model, sub, set(self.elements) | self.dims, set(self.codes.get(sub, {})),
                                       {x for x in adapted if x}, require_local=self.require_local)
        return errs, lines

    # ---- the compile ----------------------------------------------------------------------------
    def compile(self):
        tag = "-recheck" if self.recheck else ""
        report = ["# ingest-D%s, %s" % (tag, datetime.datetime.utcnow().isoformat(timespec="seconds")), ""]
        outp = os.path.join(self.out, "adaptations-recheck.jsonl" if self.recheck else "adaptations.jsonl")
        previous_lines = jl(outp)
        # Preserve every prior compile before replacement, including its return selection and grades.
        manifest = os.path.join(self.out, "adaptation-returns.jsonl")
        previous_records = jl(manifest)
        if os.path.exists(outp):
            prior = {"ledger": previous_lines, "returns": previous_records}
            digest = hashlib.sha256(json.dumps(prior, sort_keys=True).encode()).hexdigest()
            archive = os.path.join(self.out, "return-history", digest)
            os.makedirs(archive, exist_ok=True)
            for source in (outp, manifest):
                target = os.path.join(archive, os.path.basename(source))
                if os.path.isfile(source) and not os.path.exists(target):
                    shutil.copyfile(source, target)
        n_lines = n_np = 0
        accepted, unret, reissued = [], [], 0
        ops = collections.Counter(); per_room = []
        grades = {}
        return_records = []
        with open(outp, "w", encoding="utf-8") as f:
            for sub in sorted(os.listdir(self.drops)):
                d = os.path.join(self.drops, sub)
                if not os.path.isdir(d) or sub == "recheck":
                    continue
                errs, lines = self.check_room(sub)
                if errs:
                    unret.append((sub, errs)); continue
                accepted.append(sub); per_room.append(len(lines))
                run = _run_json(d)
                if (run.get("attempts") or 1) > 1:
                    reissued += 1
                labeler_run = run.get("session") or run.get("session_id") or run.get("model")
                # the room's copies beside its notes
                R = os.path.join(self.out, "rooms", sub)
                os.makedirs(R, exist_ok=True)
                old_files = [os.path.join(R, "model-D%s.md" % tag), os.path.join(R, "run%s.json" % tag)]
                existing = [path for path in old_files if os.path.isfile(path)]
                if existing:
                    content = b"".join(os.path.basename(path).encode() + b"\n" + open(path, "rb").read() for path in existing)
                    account_archive = os.path.join(self.out, "return-history", "accounts", sub, hashlib.sha256(content).hexdigest())
                    os.makedirs(account_archive, exist_ok=True)
                    for source in existing:
                        target = os.path.join(account_archive, os.path.basename(source))
                        if not os.path.exists(target):
                            shutil.copyfile(source, target)
                shutil.copyfile(os.path.join(d, "model-D.md"), os.path.join(R, "model-D%s.md" % tag))
                if os.path.exists(os.path.join(d, "run.json")):
                    shutil.copyfile(os.path.join(d, "run.json"), os.path.join(R, "run%s.json" % tag))
                model_text = open(os.path.join(d, "model-D.md"), encoding="utf-8").read()
                grades[sub] = dreturn.grade_of(model_text)
                return_records.append({"sub": sub, "phase": "recheck" if self.recheck else "initial",
                                       "status": "accepted", "model_version": self.version,
                                       "ids": [self.line_id(sub, i, obj) for i, (obj, _portable, _hits) in enumerate(lines)],
                                       "local_status": dreturn.local_status_of(model_text), "local_grade": grades[sub],
                                       "account_sha256": hashlib.sha256(open(os.path.join(d, "model-D.md"), "rb").read()).hexdigest()})
                for i, (o, portable, hits) in enumerate(lines):
                    op = o["op"]; ops[op] += 1
                    src = o.get("source") or (o.get("from") if op == "link" else None)
                    line = {"id": self.line_id(sub, i, o), "sub": sub, "op": op,
                            "element": o.get("element") or (o.get("to") if op == "link" else None),
                            "source": src, "lift": self.lift(sub, src) if src else None,
                            "condition": o.get("condition"), "statement": o.get("statement"),
                            "observation": o.get("observation"),
                            "how": o.get("how") or o.get("why"), "evidence": o.get("evidence") or {},
                            "relation": o.get("relation"), "portable": portable,
                            "nonportable_hits": hits, "kind": KIND[op],
                            "origin": "recheck" if self.recheck else "labeler", "labeler_run": labeler_run,
                            "model_version": self.version, "decision": "pending"}
                    if op == "link":
                        line["link_kind"] = o.get("kind")
                    f.write(json.dumps(line, ensure_ascii=False) + "\n")
                    n_lines += 1; n_np += 0 if portable else 1
        phase = "recheck" if self.recheck else "initial"
        if self.recheck:
            new_lines = jl(outp)
            new_ids = {line["id"] for line in new_lines}
            with open(outp, "w", encoding="utf-8") as f:
                for line in [line for line in previous_lines if line["id"] not in new_ids] + new_lines:
                    f.write(json.dumps(line, ensure_ascii=False) + "\n")
            records = previous_records + return_records
        else:
            records = [r for r in previous_records if r.get("phase") != phase] + return_records
        with open(manifest, "w", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        self.mark_unreturned(unret, accepted)
        n_v = self.compile_verdicts(grades)
        if not self.recheck:
            self.counts(len(accepted), reissued)
        report += ["rooms returned and accepted: %d" % len(accepted),
                   "rooms rejected, now in UNRETURNED.tsv: %d" % len(unret),
                   "rooms reissued by the handler: %d" % reissued,
                   "lines: %d; non-portable: %d" % (n_lines, n_np),
                   "lines per room: min %s median %s max %s" % (
                       min(per_room) if per_room else "-",
                       sorted(per_room)[len(per_room) // 2] if per_room else "-",
                       max(per_room) if per_room else "-"),
                   "ops: " + ", ".join("%s %d" % kv for kv in ops.most_common()),
                   "verdict lines compiled: %s" % (n_v if n_v is not None else "none yet (no verdict returns)"), "",
                   "## rejected rooms"]
        for sub, errs in unret:
            report.append("- %s: %s" % (sub, "; ".join(errs[:6]) + (" …" if len(errs) > 6 else "")))
        rp = os.path.join(self.out, "ingest-D%s.md" % tag)
        open(rp, "w", encoding="utf-8").write("\n".join(report) + "\n")
        print("\n".join(report[:9]))
        return 0

    def mark_unreturned(self, unret, accepted=()):
        """The handler's rows kept; this compile's rejections rewritten: a room rejected before and accepted now
        leaves the file, and a room rejected now enters it once."""
        p = os.path.join(self.drops, "UNRETURNED.tsv")
        rows = [l.rstrip("\n") for l in open(p, encoding="utf-8")] if os.path.exists(p) else []
        keep = [l for l in rows if l.strip() and not l.startswith("sub\t")
                and not (l.split("\t")[0].strip() in set(accepted) | {s for s, _e in unret}
                         and "rejected by ingest.py" in l)]
        have = {l.split("\t")[0].strip() for l in keep}
        keep += ["%s\trejected by ingest.py: %s" % (sub, "; ".join(errs[:3]).replace("\t", " "))
                 for sub, errs in unret if sub not in have]
        if keep or os.path.exists(p):
            with open(p, "w", encoding="utf-8") as f:
                f.write("sub\treason\n" + "".join(l + "\n" for l in keep))

    def unreturned(self):
        p = os.path.join(self.drops, "UNRETURNED.tsv")
        return {l.split("\t")[0].strip() for l in open(p, encoding="utf-8")
                if l.strip() and not l.startswith(("sub\t", "#"))} if os.path.exists(p) else set()

    def compile_verdicts(self, grades):
        """The verdict readers' validated lines, one room line each, with the labeler's grade beside them."""
        raw = os.path.join(self.out, "_fleet_raw", "D3v" if self.recheck else "D2v")
        p = os.path.join(self.out, "verdicts-recheck-D.jsonl" if self.recheck else "verdicts-D.jsonl")
        if not os.path.isdir(raw):
            if os.path.exists(p):              # never a verdicts file from an earlier compile
                os.replace(p, p + ".superseded")
            return None
        rows = []
        unret = self.unreturned()
        for d in sorted(glob.glob(os.path.join(raw, "*"))):
            if not os.path.isdir(d) or os.path.basename(d) in unret:
                continue
            sub = os.path.basename(d)
            readers = []
            for f in sorted(glob.glob(os.path.join(d, "r*.jsonl"))):
                rid = os.path.splitext(os.path.basename(f))[0]      # the reader's id is its file (fleet.py)
                for r in jl_safe(f):
                    if r.get("verdict") is not None:
                        readers.append(dict(r, sub=r.get("sub") or sub, reader=rid,
                                            model_version=self.version))
            if not readers:
                continue
            line = {"sub": sub, "readers": readers, "grade": grades.get(sub)}
            rows.append(line)
            R = os.path.join(self.out, "rooms", sub)
            os.makedirs(R, exist_ok=True)
            with open(os.path.join(R, "verdict-D%s.jsonl" % ("-recheck" if self.recheck else "")), "w", encoding="utf-8") as f:
                for r in readers:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
        with open(p, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        return len(rows)

    def counts(self, accepted, reissued):
        p = os.path.join(self.drops, "UNRETURNED.tsv")
        unret = 0
        if os.path.exists(p):
            unret = sum(1 for l in open(p, encoding="utf-8") if l.strip() and not l.startswith(("sub\t", "#")))
        rp = os.path.join(self.root, "RUN.json")
        run = json.load(open(rp)) if os.path.exists(rp) else {}
        run["D2"] = {"accepted": accepted, "reissued": reissued, "unreturned": unret,
                     "compiled_utc": datetime.datetime.utcnow().isoformat(timespec="seconds")}
        json.dump(run, open(rp, "w"), indent=1)

    # ---- the re-lift ----------------------------------------------------------------------------
    def relift(self):
        """Every ledger line's lift, recomputed through the placements, the fourth-order themes and the
        dimensions as they stand; a changed lift keeps the old one as lift_before."""
        self.load_placements()
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import vlib
        mh = vlib.model_hash(self.out)
        n = moved = 0
        for name in ("adaptations.jsonl", "adaptations-recheck.jsonl"):
            p = os.path.join(self.out, name)
            if not os.path.exists(p):
                continue
            rows = jl(p)
            for r in rows:
                if not r.get("source"):
                    continue
                new = self.lift(r["sub"], r["source"])
                if new != r.get("lift"):
                    r.setdefault("lift_before", r.get("lift"))
                    r["lift"] = new
                    moved += 1
                r["relifted_at"] = mh
                n += 1
            tmp = p + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                for r in rows:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
            os.replace(tmp, p)
        rp = os.path.join(self.root, "RUN.json")
        run = json.load(open(rp)) if os.path.exists(rp) else {}
        run["relift"] = {"model": mh, "lines": n, "moved": moved,
                         "utc": datetime.datetime.utcnow().isoformat(timespec="seconds")}
        json.dump(run, open(rp, "w"), indent=1)
        print("re-lifted %d ledger line(s) to the model as it stands (%s...); %d moved" % (n, (mh or "")[:12], moved))
        return 0


def relift_problems(root, out):
    """Ledger lines whose lift is not the path through the placements as they stand (the D3 and D4 checks)."""
    ing = Ingest.__new__(Ingest)
    ing.out = out
    ing.code_theme = {}
    for c in jl_safe(os.path.join(root, "package", "store", "codes.jsonl")):
        ing.code_theme[(c.get("sub"), c.get("code_id"))] = c.get("theme_id")
    ing.load_placements()
    bad = []
    for name in ("adaptations.jsonl", "adaptations-recheck.jsonl"):
        for r in jl_safe(os.path.join(out, name)):
            lift = r.get("lift")
            if r.get("source") and (not isinstance(lift, list) or lift[1:] != ing.lift(r["sub"], r["source"])[1:]):
                bad.append(r.get("id"))
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stage")
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default=None)
    ap.add_argument("--drops", default=None)
    ap.add_argument("--recheck", action="store_true")
    ap.add_argument("--check", default=None)
    ap.add_argument("--relift", action="store_true")
    a = ap.parse_args()
    out = a.out or os.path.join(a.root, "out")
    if a.stage != "D":
        print("ingest.py compiles stage D's returns only; got stage %s" % a.stage)
        return 2
    drops = a.drops or os.path.join(a.root, "DROPS", "D", "recheck" if a.recheck else "")
    if a.relift:
        return Ingest(a.root, out, drops.rstrip("/"), False).relift()
    if not os.path.isdir(drops):
        print("the drop folder %s is absent: no return has arrived, so there is nothing to ingest"
              % os.path.normpath(drops))
        return 1
    ing = Ingest(a.root, out, drops.rstrip("/"), a.recheck)
    if a.check:
        errs, lines = ing.check_room(a.check)
        for e in errs:
            print(e)
        print("%s: %d lines, %d non-portable, %s" % (a.check, len(lines),
              sum(1 for l in lines if not l[1]), "OK" if not errs else "FAIL"))
        return 1 if errs else 0
    return ing.compile()


if __name__ == "__main__":
    sys.exit(main())
