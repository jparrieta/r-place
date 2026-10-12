"""tools/assemble.py B3 (the handler's brief, 2026-10-12; J's rulings of 12 October via the orchestrator's note of
19:00Z): the fleet's accepted returns read back into room ids, copy_kind tagged from batches-B3.jsonl, the B1 grouping
joined by label, every item of the analysed set given its class 1 to 5; and checks/stage_B3.py's check_raw accepting
what it writes. The fixture: two returned packets and one exhausted, a gold copy, a duplicate, one item of each class,
one item missing a replicate, and the refusals (an id the fleet table cannot resolve, a typed sub off the theme's room,
a packet with two accepted returns, an output already there)."""
import collections, glob, json, os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(HERE)
sys.path.insert(0, T)
import vlib
from checks import stage_B3

fails = []


def ok(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + ("" if cond else "\n     " + str(detail)[:900]))
    cond or fails.append(name)


def wjl(p, rows):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write("".join(json.dumps(r) + "\n" for r in rows))


def rd(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def run(d, *extra):
    r = subprocess.run([sys.executable, os.path.join(T, "assemble.py"), "B3", "--root", d] + list(extra),
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


FT = lambda k: "T2-%05d" % k             # fleet theme id of denmark/t0k
FC = lambda c: "C%07d" % c               # fleet concept id of denmark/c00cc

# the placements: (rep-1 list, rep-2 list); t06's rep 2 sits in the exhausted packet, its gold copy in B002
PLACE = {1: (["T3-001"], ["T3-001"]),                       # class 1
         2: (["T3-002"], ["T3-002"]),                       # class 2: B1 {1, 2, 3}
         3: (["T3-001", "T3-002"], ["T3-002", "T3-001"]),   # class 3: the same themes in another order
         4: (["T3-003"], ["T3-003"]),                       # class 4: B1 {2}; G02 opened by neither reader
         5: (["T3-001"], ["T3-001"]),                       # class 5: no B1 grouping
         6: (["T3-001"], None)}                             # missing replicate
FAM = {"T3-001": "G01", "T3-002": "G02", "T3-003": "G02"}


def line(bid, rep, pos, k, so):
    multi = len(so) > 1
    sup = [FC(k), FC(10 + k)][:len(so)]
    ml = [{"sub": "r/denmark", "theme_id": FT(k), "key": "r/denmark/%s" % FT(k), "batch": bid, "agent": "r1",
           "replicate": rep, "position": pos, "primary": so[0], "additional": so[1],
           "why_not_one": "the single placement would drop the material's call for outside hands",
           "why_this_one": "the second concept carries it", "support_primary": [FC(k)], "support_additional": [FC(10 + k)],
           "dispensable": so[1]}] if multi else []
    fo = ["G01"] if k == 4 else sorted({FAM[t] for t in so})
    return {"sub": "r/denmark", "theme_id": FT(k), "batch": bid, "agent": "r1", "replicate": rep, "position": pos,
            "third_order": so, "multi": multi, "why": {t: "material" for t in so}, "confidence": "clear",
            "read": "whole", "exemplar_read": None, "families_opened": fo, "bag": False,
            "t_start": "2026-05-09T00:00:00Z", "t": "2026-05-09T00:00:01Z", "support": sup, "also_present": {},
            "multiplacement_log": ml}


def build():
    d = tempfile.mkdtemp(prefix="assemble-")
    S, O = os.path.join(d, "package", "store"), os.path.join(d, "out")
    wjl(os.path.join(S, "rooms.jsonl"), [{"sub": "denmark"}])
    wjl(os.path.join(S, "themes.jsonl"), [{"sub": "denmark", "theme_id": "t%02d" % k, "second_order": "denmark theme %d" % k,
                                           "code_ids": ["c%04d" % k, "c%04d" % (10 + k)]} for k in range(1, 7)])
    wjl(os.path.join(S, "codes.jsonl"), [{"sub": "denmark", "code_id": "c%04d" % c, "theme_id": "t%02d" % (c % 10),
                                          "first_order": "concept %d" % c, "text": "words"}
                                         for k in range(1, 7) for c in (k, 10 + k)])
    wjl(os.path.join(O, "dropped.jsonl"), [])
    wjl(os.path.join(O, "fleet_ids.jsonl"),
        [{"kind": "t", "fleet": FT(k), "sub": "denmark", "id": "t%02d" % k} for k in range(1, 7)] +
        [{"kind": "c", "fleet": FC(c), "sub": "denmark", "id": "c%04d" % c, "theme": "t%02d" % (c % 10)}
         for k in range(1, 7) for c in (k, 10 + k)])
    mem = lambda *ks: [{"sub": "denmark", "theme_id": "t%02d" % k, "second_order": "denmark theme %d" % k} for k in ks]
    wjl(os.path.join(O, "scheme", "scheme_current.jsonl"), [
        {"theme": "T3-001", "label": "one", "members": mem(1, 2, 3, 6)},
        {"theme": "T3-002", "label": "two", "members": mem(2, 3, 4)},
        {"theme": "T3-003", "label": "three", "members": mem(2)}])
    wjl(os.path.join(O, "families.jsonl"), [{"family": "G01", "themes": ["T3-001"]},
                                            {"family": "G02", "themes": ["T3-002", "T3-003"]}])
    wjl(os.path.join(O, "gold_items.jsonl"), [{"sub": "denmark", "theme_id": "t06", "third_order": ["T3-001"]}])
    K = lambda *ks: ["denmark/t%02d" % k for k in ks]
    bl = lambda bid, agent, rep, items, gold=(), dup=(), **kw: dict(
        {"batch": bid, "agent": agent, "n_items": len(items), "replicate": rep, "rooms": ["denmark"],
         "exemplar_items": [], "gold_items": list(gold), "duplicate_items": list(dup), "warmup_items": [], "reissue": 0,
         "original_agent": None, "seed": 1, "items": items}, **kw)
    batches = [bl("B001", "a001", 1, K(1, 2, 3, 1, 4, 5, 6), dup=K(1)),
               bl("B002", "a002", 2, K(3, 1, 6, 2, 5, 4), gold=K(6)),
               bl("B003", "a003", 2, K(6), coverage_short=True)]
    wjl(os.path.join(O, "batches-B3.jsonl"), batches)
    rule = {"count_key": "position", "count_exclude": ["primary", "revises", "predicted_confusion"]}
    os.makedirs(os.path.join(O, "_packets-B3"))
    json.dump({b["batch"]: dict(rule, items=b["n_items"]) for b in batches},
              open(os.path.join(O, "_packets-B3", "MANIFEST.json"), "w"))
    raw = os.path.join(O, "_fleet_raw", "B3")
    for b in batches[:2]:
        rep = b["replicate"]
        rows = [{"agent": "r1", "predicted_confusion": ["T3-001", "T3-002"], "why": "close"}]
        for pos, it in enumerate(b["items"], 1):
            k = int(it[-2:])
            so = PLACE[k][rep - 1] if PLACE[k][rep - 1] is not None else ["T3-001"]   # t06 in B002 is the gold copy
            rows.append(line(b["batch"], rep, pos, k, so))
        rows += [{"pass": 2, "revises": pos, "batch": b["batch"], "agent": "r1", "third_order": rows[pos]["third_order"],
                  "changed": False, "why_changed": None} for pos in range(1, len(b["items"]) + 1)]
        wjl(os.path.join(raw, b["batch"], "r1.jsonl"), rows)
        json.dump({"packet": b["batch"], "reader": "r1", "reissue": 0, "elapsed_s": 10.0, "valid": True},
                  open(os.path.join(raw, b["batch"], "r1.meta.json"), "w"))
        open(os.path.join(raw, b["batch"], "r1.raw.txt"), "w").write("not JSON, the reply as received\n")
    os.makedirs(os.path.join(raw, "B003"))
    open(os.path.join(raw, "B003", "r2.failed.txt"), "w").write("cites a foreign code\n{\"sub\": \"x\"}\n")
    json.dump({"packet": "B003", "reader": "r2", "reissue": 2, "valid": False},
              open(os.path.join(raw, "B003", "r2.meta.json"), "w"))
    open(os.path.join(raw, "EXHAUSTED.tsv"), "w").write("packet\tlast_reader\twhy\nB003\tr2\tforeign code\n")
    open(os.path.join(raw, "DONE"), "w").write("{}\n")
    return d


# ---- the clean run ---------------------------------------------------------------------------------------------
d = build(); O = os.path.join(d, "out")
rc, o = run(d)
ok("assemble runs clean on the fixture", rc == 0, o)
ok("prints the classes and the missing replicate", "classes: 1: 1, 2: 1, 3: 2, 4: 1, 5: 1" in o and
   "missing_replicate 1" in o and "unopened-family flags 1" in o, o)
ok("prints gold and duplicate copy counts and lines per file",
   "corpus 11, gold 1, duplicate 1" in o and "wrote assign_raw.jsonl: 13 lines" in o and
   "wrote assign_pass2.jsonl: 13 lines" in o and "wrote multiplacement_log.jsonl: 2 lines" in o, o)
raw = rd(os.path.join(O, "assign_raw.jsonl"))
r0 = raw[0]
ok("ids in room form, the fleet's beside them, r/ stripped",
   r0["sub"] == "denmark" and r0["theme_id"] == "t01" and r0["fleet_theme_id"] == FT(1) and r0["fleet_sub"] == "r/denmark"
   and r0["support"] == ["c0001"] and r0["fleet_support"] == [FC(1)], r0)
ok("agent and replicate are the batch's, the reader id kept apart, the reissue and elapsed time from meta",
   r0["agent"] == "a001" and r0["replicate"] == 1 and r0["reader"] == "r1" and r0["fleet_agent"] == "r1"
   and r0["reissue"] == 0 and r0["packet_elapsed_s"] == 10.0, r0)
ok("the readers' t_start and t are dropped", not any("t_start" in r or "t" in r for r in raw))
ck = {(r["batch"], r["position"]): r["copy_kind"] for r in raw}
ok("copy_kind: the duplicate's first copy corpus, its second duplicate, the gold copy gold",
   ck[("B001", 1)] == "corpus" and ck[("B001", 4)] == "duplicate" and ck[("B002", 3)] == "gold"
   and sum(1 for v in ck.values() if v == "corpus") == 11, ck)
mp = rd(os.path.join(O, "multiplacement_log.jsonl"))
ok("multiplacement records translated, keyed to the line",
   all(m["key"] == "denmark/t03" and m["support_additional"] == ["c0013"] and m["fleet_support_additional"] == [FC(13)]
       and m["agent"] in ("a001", "a002") for m in mp), mp)
p2 = rd(os.path.join(O, "assign_pass2.jsonl"))
ok("pass 2 apart, position = the cell it revises, item named",
   len(p2) == 13 and p2[0]["position"] == 1 and p2[0]["theme_id"] == "t01" and "revises" in p2[0], p2[:1])
ok("predictions kept", len(rd(os.path.join(O, "predicted_confusion-B3.jsonl"))) == 2)
cl = {r["theme_id"]: r for r in rd(os.path.join(O, "b3_classes.jsonl"))}
ok("one class line per item of the analysed set", len(cl) == 6, cl.keys())
ok("class 1, 2, 3 (order), 4, 5", [cl["t%02d" % k]["class"] for k in range(1, 6)] == [1, 2, 3, 4, 5],
   [(k, v["class"]) for k, v in cl.items()])
ok("class 2: the readers' list then B1's other themes by id, tagged",
   cl["t02"]["final"] == ["T3-002", "T3-001", "T3-003"] and cl["t02"]["source"] == "b1_grouping_kept", cl["t02"])
ok("a missing replicate is class 3, flagged, and a gold copy does not fill it",
   cl["t06"]["class"] == 3 and cl["t06"]["flags"]["missing_replicate"] and cl["t06"]["r2"] is None, cl["t06"])
ok("a placement in a family neither reader opened is flagged",
   cl["t04"]["flags"]["unopened_family"] is True and cl["t04"]["flags"]["unopened_themes"] == ["T3-003"]
   and cl["t01"]["flags"]["unopened_family"] is False, cl["t04"])
ok("the B1 grouping is recorded with the scheme's sha256",
   cl["t02"]["b1"] == ["T3-001", "T3-002", "T3-003"] and cl["t05"]["b1"] == []
   and cl["t01"]["b1_scheme_sha256"] == vlib.sha(os.path.join(O, "scheme", "scheme_current.jsonl"))[:16], cl["t02"])

# checks/stage_B3.py's check_raw reads what assemble wrote without an error
vlib.E.clear(); vlib.W.clear()
ctx = {"package": os.path.join(d, "package"), "root": d, "outdir": O, "stage": "B3"}
vlib.rooms(ctx)
by_batch = {b["batch"]: b for b in rd(os.path.join(O, "batches-B3.jsonl"))}
cur = vlib.current_themes(ctx)
stage_B3.check_raw(O, ctx, {"T3-001", "T3-002", "T3-003"}, by_batch, 2, {("denmark", "t06")}, ({"denmark"}, set(cur)))
ok("check_raw accepts assemble's files", not vlib.E, [m for m, _, _ in vlib.E])
vlib.E.clear()

# an output already there: refused without --supersede, renamed with it
rc, o = run(d)
ok("an existing assign_raw.jsonl is refused", rc == 1 and "already exist" in o, o)
rc, o = run(d, "--supersede")
ok("--supersede renames the old files, never deletes", rc == 0 and
   len(glob.glob(os.path.join(O, "assign_raw.jsonl.superseded-*"))) == 1 and os.path.exists(os.path.join(O, "assign_raw.jsonl")), o)

# ---- the refusals ----------------------------------------------------------------------------------------------
def edit_return(d, bid, fn):
    p = os.path.join(d, "out", "_fleet_raw", "B3", bid, "r1.jsonl")
    rows = rd(p)
    fn(rows)
    wjl(p, rows)


d = build()
edit_return(d, "B001", lambda rows: rows[2]["support"].append("C9999999"))
rc, o = run(d)
ok("an unresolvable fleet id is refused, the line named, nothing written",
   rc == 1 and "C9999999" in o and "B001/r1.jsonl line 3" in o and "REFUSING" in o
   and not os.path.exists(os.path.join(d, "out", "assign_raw.jsonl")), o)

d = build()
edit_return(d, "B002", lambda rows: rows[1].update(theme_id="T2-77777"))
rc, o = run(d)
ok("an unresolvable theme id is refused", rc == 1 and "T2-77777" in o and "does not resolve" in o, o)

d = build()
edit_return(d, "B001", lambda rows: rows[2].update(sub="r/denmrak"))
rc, o = run(d)
ok("a typed sub off the theme's room is refused", rc == 1 and "denmrak" in o and "B001/r1.jsonl line 3" in o, o)
rc, o = run(d, "--accept-sub-label")
ok("--accept-sub-label carries it where the cell and the id agree, as sub_typed",
   rc == 0 and any(r.get("sub_typed") == "denmrak" and r["sub"] == "denmark" for r in rd(os.path.join(d, "out", "assign_raw.jsonl"))), o)

d = build()
edit_return(d, "B001", lambda rows: rows[2].update(theme_id=FT(4)))
rc, o = run(d, "--accept-sub-label")
ok("a theme id off its cell is refused", rc == 1 and "the cell is the key" in o, o)

d = build()
shutil.copy(os.path.join(d, "out", "_fleet_raw", "B3", "B001", "r1.jsonl"), os.path.join(d, "out", "_fleet_raw", "B3", "B001", "r4.jsonl"))
rc, o = run(d)
ok("a packet with two accepted returns is refused by name", rc == 1 and "packet B001 has 2 accepted returns" in o, o)

d = build()
rc, o = run(d, "--dry-run")
ok("--dry-run writes nothing", rc == 0 and "dry run" in o and not os.path.exists(os.path.join(d, "out", "assign_raw.jsonl")), o)

print("assemble: %d failed" % len(fails))
sys.exit(1 if fails else 0)
