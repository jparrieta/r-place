"""Stage B3 in B2's packet shape (J, 2026-10-12): packets.py B3 writes one self-contained packet per batch line, at
most 15 items and 180,000 bytes of item text, a room spread over packets with its sibling block in each; fleet.py's
room-id guard reads id positions only, takes a packet with 0 lines due, and keeps the pass-2 lines of a return."""
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(HERE)
sys.path.insert(0, T)
import fleet

fails = []


def ok(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + ("" if cond else "\n     " + str(detail)[:600]))
    cond or fails.append(name)


def wjl(p, rows):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write("".join(json.dumps(r) + "\n" for r in rows))


def run(*args, cwd):
    r = subprocess.run([sys.executable] + list(args), capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout + r.stderr


# ---- packets.py B3 -------------------------------------------------------------------------------------------
d = tempfile.mkdtemp(); S = os.path.join(d, "package", "store"); O = os.path.join(d, "out")
codes, themes = [], []
for sub, n in (("denmark", 12), ("asoiaf", 6)):
    for i in range(1, n + 1):
        cid, tid = "c%04d" % i, "t%02d" % i
        codes.append({"sub": sub, "code_id": cid, "theme_id": tid, "first_order": "label %d" % i,
                      "text": "we held the t34 tank at the border, said a %s placer" % sub})
        themes.append({"sub": sub, "theme_id": tid, "second_order": "%s theme %d" % (sub, i), "theme_note": "a note",
                       "code_ids": [cid]})
big = "x" * 181000
codes.append({"sub": "asoiaf", "code_id": "c0099", "theme_id": "t99", "first_order": "long", "text": big})
themes.append({"sub": "asoiaf", "theme_id": "t99", "second_order": "huge", "code_ids": ["c0099"]})
half = "y" * 95000
for i in (97, 98):
    codes.append({"sub": "asoiaf", "code_id": "c00%d" % i, "theme_id": "t%d" % i, "first_order": "long", "text": half})
    themes.append({"sub": "asoiaf", "theme_id": "t%d" % i, "second_order": "half", "code_ids": ["c00%d" % i]})
wjl(os.path.join(S, "codes.jsonl"), codes)
wjl(os.path.join(S, "themes.jsonl"), themes)
wjl(os.path.join(S, "rooms.jsonl"), [{"sub": "denmark"}, {"sub": "asoiaf"}])
wjl(os.path.join(O, "scheme_final.jsonl"), [{"id": "T3-001", "name": "holding", "gloss": "g", "tier": "main"}])
wjl(os.path.join(O, "families.jsonl"), [{"family": "G01", "name": "f", "themes": ["T3-001"]}])
B = lambda bid, items, gold=(): {"batch": bid, "agent": "a" + bid[1:], "replicate": 1, "n_items": len(items),
                                 "items": items, "gold_items": list(gold), "rooms": sorted({x.split("/")[0] for x in items})}
dk = ["denmark/t%02d" % i for i in range(1, 13)]
# denmark spread over B001 and B002; B001 carries a gold copy of asoiaf/t01 in items and gold_items
wjl(os.path.join(O, "batches-B3.jsonl"), [B("B001", dk[:6] + ["asoiaf/t01"], ["asoiaf/t01"]),
                                          B("B002", dk[6:] + ["asoiaf/t02", "asoiaf/t03"])])
pk = os.path.join(O, "_packets-B3")
os.makedirs(pk)
open(os.path.join(pk, "B001-p1.md"), "w").write("# an old part\n")
rc, o = run(os.path.join(T, "packets.py"), "B3", cwd=d)
ok("packets B3 builds one packet per batch line", rc == 0 and os.path.exists(os.path.join(pk, "B001.md"))
   and os.path.exists(os.path.join(pk, "B002.md")), o)
man = json.load(open(os.path.join(pk, "MANIFEST.json")))
ok("MANIFEST: own items and item_bytes, no group/part/parts",
   man.get("B001", {}).get("items") == 7 and man["B002"]["items"] == 8 and isinstance(man["B001"].get("item_bytes"), int)
   and not any(k in e for e in man.values() for k in ("group", "part", "parts")), man)
ok("an old part is superseded, not served", not os.path.exists(os.path.join(pk, "B001-p1.md"))
   and "B001-p1" not in man, os.listdir(pk))
p1, p2 = (open(os.path.join(pk, n), encoding="utf-8").read() for n in ("B001.md", "B002.md"))
ok("a room spread over two packets carries its whole sibling block in each",
   all("sibling block, the labels of all 12 second-order themes" in p and "- t12 denmark theme 12" in p for p in (p1, p2)), p1[:400])
ok("the gold copy's room has its sibling block, and no gold tag shows", "## r/asoiaf" in p1 and "gold" not in p1.lower())
ok("item_bytes counts item text only (under the file's bytes)", man["B001"]["item_bytes"] < man["B001"]["bytes"])

before = json.load(open(os.path.join(pk, "MANIFEST.json")))
wjl(os.path.join(O, "batches-B3.jsonl"), [B("B003", dk + ["asoiaf/t01", "asoiaf/t02", "asoiaf/t03", "asoiaf/t04"])])
rc, o = run(os.path.join(T, "packets.py"), "B3", cwd=d)
ok("a 16-item batch is refused", rc != 0 and "REFUSING" in o and "15 items" in o and "B003 (16 items" in o, o)
ok("a refused build writes no packet", not os.path.exists(os.path.join(pk, "B003.md"))
   and json.load(open(os.path.join(pk, "MANIFEST.json"))) == before)
wjl(os.path.join(O, "batches-B3.jsonl"), [B("B004", ["asoiaf/t97", "asoiaf/t98"])])
rc, o = run(os.path.join(T, "packets.py"), "B3", cwd=d)
ok("a batch over 180,000 bytes of item text is refused", rc != 0 and "180000 bytes of item text" in o, o)
wjl(os.path.join(O, "batches-B3.jsonl"), [B("B005", ["asoiaf/t99"])])
rc, o = run(os.path.join(T, "packets.py"), "B3", cwd=d)
ok("an item alone over the cap stops the build: ask J", rc != 0 and "asoiaf/t99 alone" in o and "ask J" in o, o)

# ---- fleet.py: the room-id guard reads id positions only ------------------------------------------------
fleet_pkt = ("# Pilot round 3\n\n## The items\n\n### 1. T2-04512\n\nlabel: holding the line\n\n"
             "note: they held it with a t34 and c0006 in chat\n\n- C0781518  defending the t34\n"
             "    \"our t34 tank stood at c0006, we kept it\"\n\n")
rule = {"items": 1, "codes_by_item": {"T2-04512": ["C0781518"]}}
ok("t34 in the participants' words is not a leak", fleet.room_id_leaks(fleet_pkt, rule) == [],
   fleet.room_id_leaks(fleet_pkt, rule))
ok("c0006 as a concept id is a leak", fleet.room_id_leaks(fleet_pkt.replace("C0781518", "c0006"), rule) == ["c0006"])
ok("t05 in an item header is a leak", fleet.room_id_leaks(fleet_pkt.replace("T2-04512", "denmark/t05"), rule) == ["t05"])
ok("a room id in MANIFEST codes_by_item is a leak",
   fleet.room_id_leaks(fleet_pkt, {"codes_by_item": {"t05": ["C0781518", "c0006"]}}) == ["c0006", "t05"])
ok("a packet in room ids by design (no codes_by_item) is not scanned", fleet.room_id_leaks(fleet_pkt, {"items": 1}) == [])
fd = tempfile.mkdtemp()
open(os.path.join(fd, "RETURN-B2.md"), "w").write("# R\n\n```json\n{\"sub\": \"...\"}\nEND-OF-RETURN\n```\n")
open(os.path.join(fd, "P1.md"), "w").write(fleet_pkt)
json.dump({"P1": rule}, open(os.path.join(fd, "MANIFEST.json"), "w"))
rc, o = run(os.path.join(T, "fleet.py"), "B2", "--packets", fd, "--return", os.path.join(fd, "RETURN-B2.md"),
            "--raw", os.path.join(fd, "raw"), "--dry-run", cwd=fd)
ok("fleet.py dispatches a packet quoting t34", rc == 0 and "dry run" in o, o)
open(os.path.join(fd, "P1.md"), "w").write(fleet_pkt.replace("- C0781518", "- c0006"))
rc, o = run(os.path.join(T, "fleet.py"), "B2", "--packets", fd, "--return", os.path.join(fd, "RETURN-B2.md"),
            "--raw", os.path.join(fd, "raw"), "--dry-run", cwd=fd)
ok("fleet.py refuses c0006 as an item's concept id", rc != 0 and "REFUSING: room ids" in o and "c0006" in o, o)

# ---- fleet.py: 0 lines due, and pass 2 kept --------------------------------------------------------------
C = {"count_key": "position", "count_exclude": ["primary", "revises", "predicted_confusion"]}
ok("a self-contained packet with items 0 takes the end marker alone",
   fleet.validate("END-OF-RETURN", "END-OF-RETURN", None, 0, dict(C, items=0)) == ([], None))
ret = "\n".join(json.dumps(x) for x in (
    {"agent": "r1", "predicted_confusion": ["T3-001", "T3-002"]},
    {"sub": "s", "theme_id": "t01", "position": 1, "multiplacement_log": [{"additional": "T3-002",
                                                                            "support_additional": ["c0002"]}]},
    {"sub": "s", "theme_id": "t02", "position": 2},
    {"sub": "s", "theme_id": "t01", "position": 1, "revises": 1})) + "\nEND-OF-RETURN"
rows, why = fleet.validate(ret, "END-OF-RETURN", None, 2, dict(C, items=2))
ok("a pass-2 line counts toward no item and is kept in the return", why is None and len(rows) == 4
   and rows[-1].get("revises") == 1, why)
ok("a multiplacement record riding on its line (a list) is checked for foreign codes",
   fleet.foreign_codes({"theme_id": "T2-1", "multiplacement_log": [{"support_additional": ["C0000009"]}]},
                       {"codes_by_item": {"T2-1": ["C0000001"]}}) == ["C0000009"])

print("\nb3 packets: %d failed" % len(fails)); sys.exit(1 if fails else 0)
