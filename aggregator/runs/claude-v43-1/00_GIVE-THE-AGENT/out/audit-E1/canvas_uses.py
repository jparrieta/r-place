#!/usr/bin/env python3
"""E1 section 1, rule 7's uses of the canvas, stage by stage, from the logs.

    python3 out/audit-E1/canvas_uses.py > out/audit-E1/canvas_uses.json

Declared before the run (E1a). From out/_mem_reads-NN.jsonl: `mem.py room` with the canvas shown (no `no_canvas`
option) and with `--no-canvas`; `--size` reads (which show the room's canvas size); `mem.py canvas` calls and the rooms
they name. From out/_mem_pipes-NN.jsonl (the shell commands): commands that name a canvas file or verb (package/canvas,
pixels.csv, artworks.jsonl, atlas, survival-D5, the canvas_ fields, mem.py canvas, --join-canvas; a first run also
matched "placements", which names theme placements, and is kept as canvas_uses.superseded-1.json). From the model and the tree: every field named canvas, or a ground or
evidence that says canvas, in elements, arrows, propositions, findings, branches.jsonl and branches-D5.jsonl; each
is listed with its id so that the audit section can say whether the use is declared.
The places the canvas may have shaped without a declaration are read by hand in the audit section.
"""
import collections, glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
CANVAS_FILE = re.compile(r"package/canvas|pixels\.csv|artworks\.jsonl|atlas|survival-D5|canvas_(area|centre|ring|entries|artwork)"
                         r"|mem\.py canvas|--join-canvas", re.I)


def jl(p):
    for l in open(p, encoding="utf-8"):
        if l.strip():
            try:
                yield json.loads(l)
            except ValueError:
                pass


def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + "." + k if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path)
    else:
        yield path, o


def main():
    reads = {}
    for p in sorted(glob.glob(os.path.join(OUT, "_mem_reads-*.jsonl"))):
        st = re.search(r"_mem_reads-(\w+)\.jsonl", p).group(1)
        c = collections.Counter()
        canvas_rooms = set()
        shown_rooms = set()
        for r in jl(p):
            v, o = r.get("verb"), r.get("opts") or {}
            if v == "room":
                if o.get("no_canvas"):
                    c["room --no-canvas"] += 1
                else:
                    c["room with canvas"] += 1
                    shown_rooms.add((r.get("args") or ["?"])[0])
                if o.get("size"):
                    c["room --size"] += 1
            elif v == "canvas":
                c["canvas"] += 1
                canvas_rooms.add(" ".join(str(a) for a in (r.get("args") or [])) or "(no args)")
        reads[st] = dict(c, canvas_rooms=len(canvas_rooms), canvas_args_sample=sorted(canvas_rooms)[:8],
                         rooms_shown_with_canvas=len(shown_rooms))
    pipes = {}
    for p in sorted(glob.glob(os.path.join(OUT, "_mem_pipes-*.jsonl"))):
        st = re.search(r"_mem_pipes-(\w+)\.jsonl", p).group(1)
        hits = [r for r in jl(p) if CANVAS_FILE.search(r.get("cmd") or "")]
        pipes[st] = {"commands": len(hits), "legs": sorted({r.get("leg") for r in hits if r.get("leg")}),
                     "sample": [(r.get("leg"), (r.get("cmd") or "")[:160]) for r in hits[:4]]}
    model = []
    for f in ("model/elements.jsonl", "model/arrows.jsonl", "propositions.jsonl", "findings.jsonl", "branches.jsonl",
              "branches-D5.jsonl"):
        p = os.path.join(OUT, f)
        if not os.path.exists(p):
            continue
        for r in jl(p):
            rid = r.get("id") or r.get("branch")
            fields = sorted({k for k, v in walk(r) if "canvas" in k.lower()
                             or (isinstance(v, str) and k.split(".")[-1] in ("ground", "grounding", "warrant", "basis")
                                 and "canvas" in v.lower())})
            if fields:
                model.append({"file": f, "id": rid, "fields": fields})
    print(json.dumps({"rule": __doc__.split("Declared before the run (E1a).")[1].strip(), "reads_by_log": reads,
                      "pipes_naming_canvas_files": pipes, "model_and_tree_fields_naming_canvas": model}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
