#!/usr/bin/env python3
"""D5a-40, form E: the propose lines of the form's defining members (current ledger, particular lines included, as
d5f_model.py counts them), by fourth-order theme, against the 558 defining rooms; and every line's how sentence for the
form, so that they can be read whole. Prints JSON to stdout.

    python3 out/_analysis/d5a40_propose.py > out/_analysis/d5a40_propose.json
"""
import collections, json, os, sys

AN = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0]]
sys.path.insert(0, AN)
import d4a08_embed as E  # noqa: E402

sys.path.insert(0, os.path.join(E.ROOT, "tools"))
from adaptation_ledger import effective_lines  # noqa: E402

MEM = set(E.FORMS["E"]["members"])
dset, aset = {s for s in MEM if s in E.IDX}, set(E.DEF)
form, pop = [], collections.Counter()
form_rooms_t4, pop_rooms_t4 = collections.defaultdict(set), collections.defaultdict(set)
for l in effective_lines(E.OUT, include_particular=True):
    if l["op"] != "propose":
        continue
    t4 = l.get("t4") or "none"
    if l["sub"] in aset:
        pop[t4] += 1
        pop_rooms_t4[t4].add(l["sub"])
    if l["sub"] in dset:
        form.append({"sub": l["sub"], "t4": t4, "how": l.get("how") or ""})
        form_rooms_t4[t4].add(l["sub"])
fc = collections.Counter(x["t4"] for x in form)
out = {"lines": len(form), "rooms": len({x["sub"] for x in form}), "defining": len(dset),
       "by_t4": [{"t4": t, "lines": n, "rooms": len(form_rooms_t4[t]), "pop_lines": pop[t], "pop_rooms": len(pop_rooms_t4[t])}
                 for t, n in fc.most_common()],
       "pop_lines": sum(pop.values()),
       "rows": sorted(form, key=lambda x: (x["t4"], x["sub"].lower()))}
json.dump(out, sys.stdout, indent=1, ensure_ascii=False)
sys.stdout.write("\n")
