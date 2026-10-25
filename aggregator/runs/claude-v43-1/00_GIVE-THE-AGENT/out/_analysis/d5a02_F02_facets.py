#!/usr/bin/env python3
"""D5a-02: my reading of F02's 43 key lines (forms/F02.md how sentences), by room:theme, into facets of the regime.
R real enforcement by removals, bots or moderators; P the regime performed by members or moderators as play;
U the styling made usable, avoided or switched off; E the end set or restored; L the play's limits contested;
O the regime turned to another activity. Checks every key against the ledger and counts members. Prints JSON.
"""
import collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import distance  # noqa: E402
from adaptation_ledger import shared_lines  # noqa: E402

READ = {
    "acecombat:t02": "P", "battlecats:t03": "R", "bindingofisaac:t11": "O", "cfb:t04": "U",
    "danganronpa:t12": "E", "dankmemes:t02": "RP", "DestinyTheGame:t02": "UE", "fivenightsatfreddys:t01": "L",
    "flashtv:t05": "P", "formula1:t05": "U", "gameofthrones:t06": "O", "geometrydash:t02": "U",
    "kerbalspaceprogram:t01": "R", "kerbalspaceprogram:t03": "P", "MMA:t06": "E", "MMA:t01": "U",
    "monstercat:t04": "P", "monstercat:t03": "R", "naruto:t03": "O", "nyjets:t01": "O", "ontario:t04": "P",
    "paragon:t11": "E", "paragon:t07": "P", "polandball:t04": "O", "rush:t01": "L", "rwby:t04": "U",
    "schoolidolfestival:t01": "O", "smashbros:t12": "PEL", "survivor:t27": "P", "survivor:t20": "P",
    "terraria:t04": "O", "texans:t06": "O", "texans:t05": "O", "thenetherlands:t01": "L",
    "totallynotrobots:t03": "P", "totallynotrobots:t07": "PE", "totallynotrobots:t04": "P",
    "uwaterloo:t04": "RL", "warframe:t03": "E", "worldoftanks:t01": "U", "zelda:t06": "R",
}
lines = [l for l in shared_lines(os.path.join(ROOT, "out")) if l["op"] == "add-step" and l["element"] == "K01"
         and distance.node_at(l, "3") == "T3-023"]
keys = {(l.get("lift") or [""])[0] for l in lines}
missing = sorted(keys - set(READ))
extra = sorted(set(READ) - keys)
room = collections.defaultdict(set)
for k, v in READ.items():
    room[k.split(":")[0]].update(v)
by = {f: sorted((s for s, fs in room.items() if f in fs), key=str.lower) for f in "RPUELO"}
print(json.dumps({"lines": len(lines), "lifts": len(keys), "missing": missing, "extra": extra, "members": len(room),
                  "by_facet": {f: [len(v), v] for f, v in by.items()},
                  "facets_per_member": dict(collections.Counter(len(fs & set("RPUEL")) for fs in room.values())),
                  "enforce_and_end": sorted((s for s, fs in room.items() if fs & set("RP") and "E" in fs), key=str.lower)},
                 ensure_ascii=False))
