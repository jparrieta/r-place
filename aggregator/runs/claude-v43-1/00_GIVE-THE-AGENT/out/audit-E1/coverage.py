#!/usr/bin/env python3
"""E1 section 1, coverage: rooms read whole, by stage and in total, counted from the read logs directly.

    python3 out/audit-E1/coverage.py > out/audit-E1/coverage.json

One record per read, from out/_mem_reads-NN.jsonl (NN is the log that was open, not the stage the reading served):
  - room: `mem.py room` records; forest: `mem.py forest` records; case, note, brief alongside;
  - a forest read whole: a room whose forest pages in that log cover every line (the union of offset to
    offset + lines reaches `total`), or a record that returned all its lines at once;
  - cite: out/_cite_reads-NN.jsonl records, and the distinct rooms they cite.
Apart, the readers that leave no read log: the fleet folders in out/_fleet_raw/ (entries per stage), the return's
rooms in DROPS/D/, the C2 reviewer and the C5 readers (out/readers-C5/, lines per reader).
"""
import collections, glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")


def jl(p):
    for l in open(p, encoding="utf-8"):
        if l.strip():
            try:
                yield json.loads(l)
            except ValueError:
                pass


def main():
    stages, tot = {}, collections.defaultdict(set)
    for p in sorted(glob.glob(os.path.join(OUT, "_mem_reads-*.jsonl"))):
        st = re.search(r"_mem_reads-(\w+)\.jsonl", p).group(1)
        n = collections.Counter()
        rooms = collections.defaultdict(set)
        pages = collections.defaultdict(list)
        totals = {}
        for r in jl(p):
            v = r.get("verb")
            if v not in ("room", "forest", "case", "note", "brief"):
                continue
            if r.get("refused"):
                n[v + " refused"] += 1
                continue
            sub = (r.get("args") or [None])[0]
            if not sub:
                continue
            sub = sub.split("/")[0]
            n[v] += 1
            rooms[v].add(sub)
            if v == "forest":
                off, ln, total = r.get("offset") or 0, r.get("lines") or 0, r.get("total")
                pages[sub].append((off, off + ln))
                if total is not None:
                    totals[sub] = max(totals.get(sub, 0), total)
        whole = set()
        for sub, ps in pages.items():
            t = totals.get(sub)
            if t is None:
                continue
            reach, cov = 0, 0
            for a, b in sorted(ps):
                if a <= reach:
                    reach = max(reach, b)
            if reach >= t:
                whole.add(sub)
        cp = os.path.join(OUT, "_cite_reads-%s.jsonl" % st)
        cite_n, cite_rooms = 0, set()
        if os.path.exists(cp):
            for r in jl(cp):
                cite_n += 1
                for c in r.get("cited") or []:
                    cite_rooms.add(str(c).split("/")[0])
        stages[st] = {"room_reads": n["room"], "room_rooms": len(rooms["room"]),
                      "forest_reads": n["forest"], "forest_rooms": len(rooms["forest"]),
                      "forest_read_whole_rooms": len(whole),
                      "case_reads": n["case"], "case_rooms": len(rooms["case"]),
                      "note_reads": n["note"], "brief_reads": n["brief"],
                      "refused": {k: v for k, v in n.items() if k.endswith("refused")},
                      "cite_reads": cite_n, "cite_rooms": len(cite_rooms)}
        tot["room"] |= rooms["room"]
        tot["forest"] |= rooms["forest"]
        tot["forest_whole"] |= whole
        tot["case"] |= rooms["case"]
        tot["cite"] |= cite_rooms
    fleet = {}
    fr = os.path.join(OUT, "_fleet_raw")
    for d in sorted(os.listdir(fr)):
        if d.startswith("."):
            continue
        q = os.path.join(fr, d)
        if os.path.isdir(q):
            ents = [e for e in os.listdir(q) if not e.startswith(".")]
            fleet[d] = {"entries": len(ents), "dirs": sum(1 for e in ents if os.path.isdir(os.path.join(q, e))),
                        "named": sorted(e for e in ents if not re.match(r"^(B\d{4}|S\d\d-\d\d)$", e))[:12]}
    drops = os.path.join(ROOT, "DROPS", "D")
    readers = {os.path.basename(p): sum(1 for _ in jl(p)) for p in sorted(glob.glob(os.path.join(OUT, "readers-C5", "*.jsonl")))}
    print(json.dumps({"rule": __doc__.split("directly.")[1].strip(), "by_log": stages,
                      "in_all_logs": {k: len(v) for k, v in tot.items()},
                      "analysed_set": 705,
                      "rooms_never_read_by_room_or_forest": sorted(
                          {json.loads(l)["sub"] for l in open(os.path.join(ROOT, "package", "store", "rooms.jsonl"))}
                          - tot["room"] - tot["forest"]),
                      "apart": {"fleet_raw": fleet,
                                "drops_D_rooms": len([e for e in os.listdir(drops) if os.path.isdir(os.path.join(drops, e))]) if os.path.isdir(drops) else None,
                                "readers_C5_lines": readers}}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
