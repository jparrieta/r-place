#!/usr/bin/env python3
"""E1 sections 6 and 7 (E1b-08): which stage was load-bearing, and the counts behind what the study cannot say.
Prints JSON.

    python3 out/audit-E1/load_limits.py > out/audit-E1/load_limits.json

The rule, declared before the run (E1b-08):
- A stage's outputs: the files of out/ (top level, model/, fourth/; not _views, _snap, _analysis, the read and pipe
  logs, rooms/ or diary/) that first appear in a snap of that stage. Read downstream: the file's name appears in a
  shell command of a later stage (out/_mem_pipes-NN.jsonl) or in a read of a later stage (out/_mem_reads-NN.jsonl,
  out/_cite_reads-NN.jsonl). A file no later stage names is listed, for reading by hand.
- tools/chunk_compare.py: its sha256 now against the engine_sha256 that departures.jsonl records, and its outputs
  present.
- The data-structure view (_views/data-structure.tsv): its hash at C2's last snap, at C5's last snap and now.
- The dimensions' work: lines naming a dimension id (D01 to D08) in branches.jsonl, model/arrows.jsonl,
  model/elements.jsonl and account.md, and the dimension names in account.md.
- For the limits: coder_conflicts.jsonl's lines; the arrows no proposition rests on; the third-order themes no standing
  element reaches (element_reach.json); findings whose statement says weak, absence or not found.
"""
import collections, glob, hashlib, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
ORDER = ["A1", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "C5", "D1", "D2", "D3", "D4", "D5", "D6", "E1"]
SKIP = re.compile(r"^(_views|_snap|_analysis|_mem_|_cite_|rooms/|diary/|_transcripts|_probe|_fleet_raw|audit-E1|_closes)")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def main():
    snaps = []
    for p in glob.glob(os.path.join(OUT, "_snap", "*.sha256")):
        with open(p, encoding="utf-8") as fh:
            m = re.search(r"^# snap (\S+) \S+ at (\S+)", fh.readline())
            files = {}
            for line in fh:
                parts = line.rstrip("\n").split("  ", 3)
                if len(parts) == 4:
                    files[parts[3]] = parts[0]
        if m:
            snaps.append((m.group(2), m.group(1), files))
    snaps.sort()
    first = {}
    for t, st, files in snaps:
        for f in files:
            if f not in first and not SKIP.match(f) and f.count("/") <= 1:
                first[f] = st
    text = {}
    for st in ORDER:
        parts = []
        for pat in ("_mem_pipes-%s.jsonl", "_mem_reads-%s.jsonl", "_cite_reads-%s.jsonl"):
            p = os.path.join(OUT, pat % st)
            if os.path.exists(p):
                parts.append(open(p, encoding="utf-8", errors="replace").read())
        text[st] = "\n".join(parts)
    by_stage = collections.defaultdict(lambda: {"outputs": 0, "named_later": 0, "never_named_later": []})
    for f, st in first.items():
        if st not in ORDER:
            continue
        later = ORDER[ORDER.index(st) + 1:]
        name = os.path.basename(f)
        hit = any(name in text[s] for s in later)
        b = by_stage[st]
        b["outputs"] += 1
        if hit:
            b["named_later"] += 1
        elif st not in ("E1",):
            b["never_named_later"].append(f)
    R = {"by_stage": {s: by_stage[s] for s in ORDER if s in by_stage}}
    tool = os.path.join(ROOT, "tools", "chunk_compare.py")
    sha = hashlib.sha256(open(tool, "rb").read()).hexdigest() if os.path.exists(tool) else None
    recs = [d for d in jl(os.path.join(OUT, "departures.jsonl")) if d.get("engine_sha256")]
    R["chunk_compare"] = {"present": bool(sha), "sha256_now": sha[:16] if sha else None,
                          "receipt": [(d.get("engine_version"), (d.get("engine_sha256") or "")[:16]) for d in recs],
                          "matches_receipt": any(sha == d.get("engine_sha256") for d in recs),
                          "outputs": {f: os.path.exists(os.path.join(OUT, f)) for f in ("chunk-share-D4.jsonl", "chunk-share-D4.md", "projections-D4.jsonl")}}
    def last_hash(stage):
        h = None
        for t, st, files in snaps:
            if st == stage and "_views/data-structure.tsv" in files:
                h = files["_views/data-structure.tsv"]
        return h
    now = hashlib.sha256(open(os.path.join(OUT, "_views", "data-structure.tsv"), "rb").read()).hexdigest()
    R["data_structure_view"] = {"C2_last": (last_hash("C2") or "")[:12], "C5_last": (last_hash("C5") or "")[:12], "now": now[:12],
                                "C5_file_present": os.path.exists(os.path.join(OUT, "data_structure-C5.md"))}
    dims = {d["id"]: d.get("name") for d in jl(os.path.join(OUT, "dimensions.jsonl"))}
    dre = re.compile(r"\bD0[1-8]\b")
    def count(path):
        if path.endswith(".jsonl"):
            return sum(1 for l in open(path, encoding="utf-8") if dre.search(l))
        return len(dre.findall(open(path, encoding="utf-8").read()))
    acc = open(os.path.join(OUT, "account.md"), encoding="utf-8").read()
    R["dimensions"] = {"ids": dims,
                       "lines_naming_one": {f: count(os.path.join(OUT, f)) for f in ("branches.jsonl", "model/arrows.jsonl", "model/elements.jsonl", "account.md")},
                       "names_in_account": {n: acc.count(n) for n in dims.values() if n}}
    R["coder_conflicts"] = sum(1 for l in open(os.path.join(OUT, "coder_conflicts.jsonl"), encoding="utf-8") if l.strip())
    used = set()
    for p in jl(os.path.join(OUT, "propositions.jsonl")):
        for r in p.get("rests_on") or []:
            used.add(r if isinstance(r, str) else r.get("id"))
    R["arrows_no_proposition_rests_on"] = sorted(a["id"] for a in jl(os.path.join(OUT, "model", "arrows.jsonl")) if a["id"] not in used)
    er = json.load(open(os.path.join(OUT, "audit-E1", "element_reach.json"), encoding="utf-8"))
    R["third_order_reached"] = {"reached_by_standing": er.get("third_order_reached_by_standing_elements"), "in_scheme": er.get("third_order_in_scheme")}
    F = jl(os.path.join(OUT, "findings.jsonl"))
    lastF = {}
    for f in F:
        lastF[f["id"]] = f
    R["absence_findings"] = sorted(i for i, f in lastF.items() if re.search(r"weak|absence|not found|no .* found", f.get("statement") or "", re.I))
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-08):")[1].strip(), **R}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
