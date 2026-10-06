"""Stage A1 section 1, second pass: concept reach through themes' code_ids, and n_codes_coder by room.

Run from the folder root: python3 out/_analysis/a1_checks2.py > out/_analysis/a1_checks2-A1.txt
Declared in departures.jsonl (A1a), with a1_checks.py.
"""
import hashlib, json, os, statistics
from collections import Counter, defaultdict

P = {"codes": "package/store/codes.jsonl", "themes": "package/store/themes.jsonl",
     "rooms": "package/store/rooms.jsonl", "retracted": "package/store/_retracted.jsonl"}
for k, p in P.items():
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    print(f"{p}  {os.path.getsize(p)} bytes  sha256 {h}")


def jl(p):
    return [json.loads(l) for l in open(p) if l.strip()]


codes, themes, rooms, retr = jl(P["codes"]), jl(P["themes"]), {r["sub"]: r for r in jl(P["rooms"])}, jl(P["retracted"])
print(f"retracted line keys {sorted(retr[0].keys())}")
print(f"theme keys {sorted(themes[0].keys())}")
in_codes = {(c["sub"], c["code_id"]) for c in codes}
listed = set()
for t in themes:
    for cid in t.get("code_ids") or []:
        listed.add((t["sub"], cid))
print(f"concepts {len(in_codes)}; listed in a theme's code_ids {len(listed & in_codes)}; listed but not in store {len(listed - in_codes)}; "
      f"in store but listed by no theme {len(in_codes - listed)}")
null_theme = sum(1 for c in codes if not c.get("theme_id"))
print(f"concepts with no theme_id {null_theme}")
tid = {(t["sub"], t["theme_id"]) for t in themes}
orphan = sum(1 for c in codes if (c["sub"], c.get("theme_id")) not in tid)
print(f"concepts whose theme_id names no theme of the room {orphan}")

coder = Counter(); store = Counter(); retr_by = Counter(r.get("sub") for r in retr)
for t in themes:
    coder[t["sub"]] += t.get("n_codes_coder") or 0
    store[t["sub"]] += t.get("n_codes") or 0
diff = [(s, coder[s], store[s], retr_by[s], rooms[s].get("codes_retracted")) for s in rooms
        if coder[s] - retr_by[s] != store[s]]
print(f"rooms where sum n_codes_coder less retracted differs from store concepts: {len(diff)}")
print("  sub, n_codes_coder sum, store concepts, retracted lines, rooms.codes_retracted")
for d in sorted(diff, key=lambda d: d[1] - d[3] - d[2])[:40]:
    print("  ", d, "gap", d[1] - d[3] - d[2])
tdiff = [(t["sub"], t["theme_id"], t.get("n_codes_coder"), t.get("n_codes"), len(t.get("code_ids") or [])) for t in themes
         if t.get("n_codes_coder") is not None and t.get("n_codes_coder") < (t.get("n_codes") or 0)]
print(f"themes with n_codes_coder below n_codes: {len(tdiff)}; first {tdiff[:8]}")
