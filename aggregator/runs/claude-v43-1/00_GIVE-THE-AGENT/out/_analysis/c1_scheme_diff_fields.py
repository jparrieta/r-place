#!/usr/bin/env python3
"""C1, read-only: which fields of scheme_v2.jsonl differ from the frozen scheme_final.jsonl, and in which themes.
Prints, per field, the count of themes that differ; then the themes that differ in any field outside the member and
count fields (the gate and tier changes).

    python3 out/_analysis/c1_scheme_diff_fields.py
"""
import collections, json, os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(p):
    with open(os.path.join(OUT, p), encoding="utf-8") as f:
        return dict((t["id"], t) for t in map(json.loads, (l for l in f if l.strip())))


a = load("scheme_final.jsonl")
b = load("scheme_v2.jsonl")
per = collections.defaultdict(set)
pairs = [(k, f) for k in b for f in set(a.get(k, {})) | set(b[k]) if a.get(k, {}).get(f) != b[k].get(f)]
list(map(lambda kf: per[kf[1]].add(kf[0]), pairs))
print("themes in scheme_v2 %d; in scheme_final %d; differing in any field %d" % (
    len(b), len(a), len(set(k for k, _ in pairs))))
print("\n".join("  %-28s %3d" % (f, len(v)) for f, v in sorted(per.items(), key=lambda kv: -len(kv[1]))))
count_fields = set(f for f in per if f.startswith("n_") or any(w in f for w in ("member", "exemplar", "count", "rooms")))
core = sorted(set(k for k, f in pairs if f not in count_fields))
print("fields read as member or count fields: %s" % ", ".join(sorted(count_fields)) or "none")
print("themes differing outside them: %d: %s" % (len(core), ", ".join(core)))
