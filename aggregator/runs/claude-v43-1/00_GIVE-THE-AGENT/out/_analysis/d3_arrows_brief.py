#!/usr/bin/env python3
"""D3: print each arrow of the model in brief (id, from, to, kind, status, strength, connection, bound,
mechanism), for ruling under G4a whether an arrow already states a line's condition or step.

  python3 out/_analysis/d3_arrows_brief.py
"""
import json

for ln in open("out/model/arrows.jsonl", encoding="utf-8"):
    if not ln.strip():
        continue
    a = json.loads(ln)
    print(f"{a['id']} {a.get('from')} -> {a.get('to')} [{a.get('kind')}, {a.get('status')}, {a.get('strength')}]")
    print(f"   connection: {a.get('connection')}")
    if a.get("bound"):
        print(f"   bound: {a.get('bound')}")
    if a.get("mechanism"):
        print(f"   mechanism: {a.get('mechanism')}")
