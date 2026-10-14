#!/usr/bin/env python3
"""C2 section 4, read-only: the third-order themes no element of model/elements.jsonl uses, directly or through its
fourth-order theme, by name, grouped under their fourth-order theme, as markdown lines for model.md. The same rule as
c2_dim_mass.py's count.

    python3 out/_analysis/c2_unused_t3.py
"""
import collections, json, os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def jl(p):
    with open(os.path.join(OUT, p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


t4 = jl(os.path.join("fourth", "fourth.jsonl"))
owner = dict((m, r["id"]) for r in t4 for m in r["members"])
name4 = dict((r["id"], r["name"]) for r in t4)
# elements in the model only: a candidate or withdrawn element uses no theme (pass 2; pass 1 had none)
els = [e for e in jl(os.path.join("model", "elements.jsonl")) if e.get("status") not in ("candidate", "withdrawn")]
used = set()
for e in els:
    used.update(e["tier"] if isinstance(e["tier"], list) else [e["tier"]])
scheme = jl("scheme_v2.jsonl")
name3 = dict((t["id"], t.get("name") or t.get("label")) for t in scheme)
unused = [t["id"] for t in scheme if t["id"] not in used and owner.get(t["id"]) not in used]
by4 = collections.defaultdict(list)
for t in unused:
    by4[owner.get(t, "unpicked")].append(t)
print("third-order themes the model does not use: %d of %d" % (len(unused), len(scheme)))
for k in sorted(by4):
    label = "unpicked by any fourth-order theme" if k == "unpicked" else "%s %s" % (k, name4[k])
    print("- **%s** (%d): %s." % (label, len(by4[k]), "; ".join("%s %s" % (t, name3[t]) for t in by4[k])))
