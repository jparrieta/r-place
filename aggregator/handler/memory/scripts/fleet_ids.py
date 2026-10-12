"""fleet_ids.py STORE OUT SEED: one opaque fleet id for every first-order code and every second-order theme
(J, 2026-10-12): readers see only these ids, so no id carries its room, and an id a reader invents lands on a
real code or theme with a known small chance (the share of the id space in use). Ids are drawn without
replacement from the space, so no two collide; the table is fixed by SEED."""
import json, os, random, sys
store, out, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
jl = lambda p: [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
codes = sorted({(o["sub"], o["code_id"], o.get("theme_id")) for o in jl(os.path.join(store, "codes.jsonl"))})
themes = sorted({(o["sub"], o["theme_id"]) for o in jl(os.path.join(store, "themes.jsonl"))})
if len({(s, c) for s, c, _ in codes}) != len(codes):
    sys.exit("a code id appears under two themes in one room; refusing")
R = random.Random(seed)
C_DIGITS, T_DIGITS = 7, 5
C_SPACE = round(len(codes) / 0.075)            # J: a made-up id lands 5 to 10 % of the time; 7.5 %
T_SPACE = 10 ** T_DIGITS                         # 7,844 themes in 100,000: 7.8 %
cid = R.sample(range(C_SPACE), len(codes))
tid = R.sample(range(T_SPACE), len(themes))
with open(out, "w", encoding="utf-8") as f:
    for (s, c, t), n in zip(codes, cid):
        f.write(json.dumps({"kind": "c", "fleet": "C%0*d" % (C_DIGITS, n), "sub": s, "id": c, "theme": t}) + "\n")
    for (s, t), n in zip(themes, tid):
        f.write(json.dumps({"kind": "t", "fleet": "T2-%0*d" % (T_DIGITS, n), "sub": s, "id": t}) + "\n")
meta = {"seed": seed, "codes": len(codes), "themes": len(themes),
        "c_format": "C + %d digits" % C_DIGITS, "t_format": "T2- + %d digits" % T_DIGITS,
        "c_space": C_SPACE, "c_hit_chance": round(len(codes) / C_SPACE, 4), "t_hit_chance": round(len(themes) / 10 ** T_DIGITS, 4)}
json.dump(meta, open(out.replace(".jsonl", ".meta.json"), "w"), indent=1)
print(json.dumps(meta))
