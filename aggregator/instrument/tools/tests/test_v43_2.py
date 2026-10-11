#!/usr/bin/env python3
"""test_v43_2.py: the changes of 2026-10-11 (J: "Do all changes and audit them before giving them"), from the
B1e interview: blind reads, a logged page width, the gate check, gate changes and their rechecks, and the
concepts behind every placement. One assertion per behaviour, over test_verbs.py's three-room store.

    python3 tools/tests/test_v43_2.py
"""
import json, os, random, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import test_verbs as tv          # build(), run(), check(), wjl(), FAILS
import vlib


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


def main():
    root = tempfile.mkdtemp(prefix="v43-2-")
    out = tv.build(root)
    c = lambda *a: tv.mem(*a, cwd=root)
    check = tv.check
    reads = lambda: jl(os.path.join(out, "_mem_reads-B1.jsonl"))

    # ---- 1. blind reads --------------------------------------------------------------------------
    rc, o = c("blind")
    check("blind with no argument says the window is closed", rc == 0 and "closed" in o, o)
    rc, o = c("theme", "denmark/t01")
    check("a plain theme read shows where it is placed", rc == 0 and "placed: T3-001" in o, o)
    rc, o = c("theme", "denmark/t01", "--blind")
    check("theme --blind hides the placement", rc == 0 and "hidden (blind read)" in o and "T3-001" not in o, o)
    check("the read log marks a --blind read", reads()[-1].get("blind") is True and reads()[-1]["opts"].get("blind") is True,
          reads()[-1])
    rc, o = c("log", "placed denmark:t01 in T3-001", "--kind", "placed", "--ids", "T3-001")
    rc, o = c("blind", "on")
    check("blind on needs a reason", rc == 1 and "--reason" in o, o)
    rc, o = c("blind", "on", "--reason", "re-place ten items blind")
    st = json.load(open(os.path.join(out, "_blind.json")))
    check("blind on opens a window in out/_blind.json", rc == 0 and st.get("on") is True and st.get("reason"), o)
    rc, o = c("blind", "on", "--reason", "again")
    check("a second blind on is refused", rc == 1 and "already open" in o, o)
    rc, o = c("theme", "denmark/t01")
    check("in the window a plain theme read hides the placement", rc == 0 and "hidden (blind read)" in o and "T3-0" not in o, o)
    rc, o = c("room", "denmark")
    check("in the window room hides its themes' placements", rc == 0 and "-> hidden (blind read)" in o and "T3-0" not in o, o)
    rc, o = c("themes", "--rooms", "denmark,sweden")
    check("in the window themes hides placements", rc == 0 and "T3-0" not in o, o)
    rc, o = c("where", "T3-001")
    check("in the window where refuses", rc == 1 and "blind" in o, o)
    rc, o = c("codes", "--third", "T3-001")
    check("in the window codes --third refuses", rc == 1 and "blind" in o, o)
    rc, o = c("codes", "--sub", "denmark")
    check("in the window codes --sub reads", rc == 0 and "c0001" in o, o)
    rc, o = c("pairs", "--level", "third")
    check("in the window pairs above level second refuses", rc == 1 and "blind" in o, o)
    rc, o = c("scheme", "T3-001")
    check("in the window scheme <id> withholds members", rc == 0 and "withheld" in o and "members (" not in o, o)
    rc, o = c("scheme")
    rows = [l for l in o.splitlines() if l.startswith("T3-001")]
    check("in the window the scheme list shows no member counts", rc == 0 and rows and rows[0].split()[2] == "-", o)
    rc, o = c("diary", "--last", "20")
    check("in the window the diary drops placed lines and masks ids", rc == 0 and "placed denmark" not in o and "T3-001" not in o, o)
    check("every read in the window is marked blind", all(r.get("blind") for r in reads()[-9:]), reads()[-9:])
    rc, o = c("blind")
    check("blind reports the open window", rc == 0 and "open since" in o, o)
    rc, o = c("blind", "off")
    st = json.load(open(os.path.join(out, "_blind.json")))
    check("blind off closes the window and keeps its times", rc == 0 and st.get("on") is False and st.get("until"), o)
    rc, o = c("theme", "denmark/t01")
    check("after the window the placement shows again", rc == 0 and "placed: T3-001" in o, o)
    rc, o = c("blind", "off")
    check("blind off with no window is refused", rc == 1 and "no blind window" in o, o)

    # ---- 2. a logged width -----------------------------------------------------------------------
    rc, o = c("theme", "denmark/t01", "--width", "30")
    page = o.split("[end:")[0].splitlines()
    r = reads()[-1]
    check("--width clips each line and marks it", rc == 0 and all(len(l) <= 30 for l in page) and any(l.endswith("…") for l in page), o)
    check("the read log records the width and the lines clipped", r.get("width") == 30 and r.get("clipped", 0) > 0, r)
    rc, o = c("theme", "denmark/t01", "--width", "5")
    check("--width under 20 is refused", rc == 1 and "too narrow" in o, o)
    rc, o = c("theme", "denmark/t01")
    check("without --width nothing is clipped and nothing logged", rc == 0 and "width" not in reads()[-1], reads()[-1])

    # ---- 3. the gate check -----------------------------------------------------------------------
    sch = [{"id": "T3-001", "name": "calling", "must_show": "a call for hands",
            "must_not_show": "Holding a line (T3-002).", "decide_when_both": "the call leads: T3-001",
            "discriminators": [{"vs": "T3-002", "question": "Is it a call (T3-001) or a line held (T3-002)?"}],
            "is_not": "", "exemplars": [{"sub": "denmark", "code_id": "c0001", "quote": "q"}]},
           {"id": "T3-002", "name": "holding", "must_show": "a line held",
            "must_not_show": "Calling (T3-001); attacking (T3-009).", "decide_when_both": "",
            "discriminators": [], "is_not": ""}]
    tv.wjl(os.path.join(out, "scheme.jsonl"), sch)
    rc, o = c("gates")
    check("gates finds a one-way discriminator", rc == 0 and "run one way: 1" in o and "T3-001 has one against T3-002" in o, o)
    check("gates finds a must_not_show with no discriminator", "no discriminator against it: 1" in o and "T3-002 -> T3-001" in o, o)
    check("gates finds an id the scheme lacks", "lacks: 1" in o and "T3-009" in o, o)
    rc, o = c("gates", "T3-001", "T3-002")
    check("gates A B prints both sides and the defect", rc == 0 and "defect:" in o and "discriminator against T3-001: NONE" in o
          and "must_not_show naming T3-002" in o, o)
    rc, o = c("gates", "T3-001", "T3-002", "--confirm", "--reason", "read")
    check("--confirm is refused while the pair has a defect", rc == 1 and "fix the pair" in o, o)
    sch[1]["discriminators"] = [{"vs": "T3-001", "question": "Is it a line held (T3-002) or a call (T3-001)?"}]
    sch[1]["must_not_show"] = "Calling (T3-001)."
    tv.wjl(os.path.join(out, "scheme.jsonl"), sch)
    rc, o = c("gates")
    check("a fixed pair leaves no defect", rc == 0 and "run one way: 0" in o and "no discriminator against it: 0" in o and "lacks: 0" in o, o)
    rc, o = c("gates", "T3-001", "T3-002", "--confirm", "--reason", "both sides agree")
    gc = jl(os.path.join(out, "gate_checks.jsonl"))
    check("--confirm records the pair with a hash", rc == 0 and gc and gc[-1]["pair"] == ["T3-001", "T3-002"] and gc[-1]["hash"], o)
    rc, o = c("gates", "T3-001")
    check("gates <id> lists its pairs with their status", rc == 0 and "T3-002" in o and "confirmed" in o, o)
    sch[0]["must_show"] = "a call for hands from outside"
    tv.wjl(os.path.join(out, "scheme.jsonl"), sch)
    rc, o = c("gates", "T3-001")
    check("a confirmation goes stale when a gate changes", rc == 0 and "stale" in o, o)
    rc, o = c("scheme", "T3-001", "--blind")
    check("scheme --blind withholds exemplars", rc == 0 and "exemplars:" not in o and "must_show" in o, o)

    # ---- 4. gate changes and rechecks after the freeze (C1) --------------------------------------
    af = os.path.join(out, "assignments_final.jsonl")
    tv.wjl(af, [{"sub": "denmark", "theme_id": "t01", "third_order": ["T3-001"], "support": ["c0001"]},
                {"sub": "denmark", "theme_id": "t02", "third_order": ["T3-002"], "support": ["c0002"]},
                {"sub": "sweden", "theme_id": "t01", "third_order": ["T3-001"], "support": ["c0001"]}])
    tv.wjl(os.path.join(out, "scheme_v2.jsonl"), sch)
    rc, o = c("gate", "T3-001", "--field", "must_show", "--now", "a call for hands beyond the room", "--reason", "r", "--stage", "B2")
    check("gate refuses at B2 (scheme_edits.jsonl is the record there)", rc == 1 and "scheme_edits.jsonl" in o, o)
    rc, o = c("gate", "T3-001", "--field", "must_show", "--now", "a call for hands beyond the room", "--reason", "readers split",
              "--stage", "C1")
    gh = jl(os.path.join(out, "gate_history.jsonl"))
    check("gate at C1 records the change with what it could move", rc == 0 and gh and gh[-1]["ref"] == "gate:1"
          and gh[-1]["candidates"] == 2 and len(gh[-1]["owed"]) == 2 and gh[-1]["was"] == "a call for hands from outside", o)
    rc, o = c("rechecks", "--owed", "--stage", "C1")
    check("rechecks --owed lists the two placements owed", rc == 0 and "owed: denmark:t01" in o and "owed: sweden:t01" in o, o)
    rc, o = c("recheck", "denmark:t02", "--change", "gate:1", "--theme", "T3-002", "--codes", "c0002", "--reason", "x", "--stage", "C1")
    check("recheck refuses a placement the change could not move", rc == 1 and "could move" in o, o)
    rc, o = c("recheck", "denmark:t01", "--change", "gate:9", "--theme", "T3-001", "--codes", "c0001", "--reason", "x", "--stage", "C1")
    check("recheck refuses a change that does not exist", rc == 1 and "no gate change gate:9" in o, o)
    rc, o = c("recheck", "denmark:t01", "--change", "gate:1", "--theme", "T3-001", "--codes", "c0002", "--reason", "x", "--stage", "C1")
    check("recheck refuses a concept of another second-order theme", rc == 1 and "not of t01" in o, o)
    rc, o = c("recheck", "denmark:t01", "--change", "gate:1", "--theme", "T3-001", "--codes", "c0001", "--reason", "still a call",
              "--stage", "C1")
    check("recheck records an unchanged placement", rc == 0 and "unchanged" in o, o)
    rc, o = c("recheck", "sweden:t01", "--change", "gate:1", "--theme", "T3-002", "--codes", "c0001", "--reason", "a line held",
              "--stage", "C1")
    check("recheck records a moved placement and says to reassign it", rc == 0 and "moved" in o and "reassign" in o, o)
    rc, o = c("recheck", "sweden:t01", "--change", "gate:1", "--theme", "T3-002", "--codes", "c0001", "--reason", "again",
              "--stage", "C1")
    check("a recheck is recorded once", rc == 1 and "already rechecked" in o, o)
    rc, o = c("rechecks", "--stage", "C1")
    check("rechecks shows the change done: 2 done, 1 moved, 0 missing", rc == 0 and "2 done (1 moved), 0 missing" in o, o)
    del vlib.E[:]
    vlib.recheck_errors(out, "C1", vlib.code_themes(jl(os.path.join(root, "package", "store", "codes.jsonl"))), {"T3-001", "T3-002"})
    check("the checks find nothing owed and every recheck well formed", not vlib.E, vlib.E)
    rc, o = c("gate", "T3-002", "--field", "is_not", "--now", "a call (T3-001)", "--reason", "r2", "--stage", "C1")
    del vlib.E[:]
    vlib.recheck_errors(out, "C1", None, None)
    check("a change with its rechecks missing is an error for the checks", len(vlib.E) == 1 and "gate:2" in vlib.E[0][0], vlib.E)

    # ---- 5. the sample rule and its escalation ---------------------------------------------------
    cands = [("r%02d" % i, "t01") for i in range(40)]
    owed, sampled = vlib.draw_owed(cands, "C1", "gate:7")
    owed2, _ = vlib.draw_owed(list(reversed(cands)), "C1", "gate:7")
    check("above thirty a seeded sample of thirty, the same every time", sampled and len(owed) == 30 and owed == owed2, owed)
    o2, s2 = vlib.draw_owed(cands[:30], "C1", "gate:7")
    check("thirty or fewer are all owed", not s2 and len(o2) == 30, o2)
    d2 = tempfile.mkdtemp(prefix="v43-2-esc-")
    tv.wjl(os.path.join(d2, "gate_history.jsonl"), [{"stage": "C1", "theme": "T3-001", "field": "must_show",
                                                     "candidates_list": [list(k) for k in cands],
                                                     "owed": [list(k) for k in owed]}])
    tv.wjl(os.path.join(d2, "rechecks-C1.jsonl"), [{"change": "gate:1", "sub": k[0], "theme_id": k[1],
                                                    "now": ["T3-001"], "changed": i < 4} for i, k in enumerate(owed)])
    O = vlib.owed_rechecks(d2, "C1")[0]
    check("more than one in ten of the sample moved: every candidate is owed", O["escalated"] and len(O["owed"]) == 40
          and len(O["missing"]) == 10, {k: O[k] for k in ("escalated", "sampled", "moved")})
    tv.wjl(os.path.join(d2, "rechecks-C1.jsonl"), [{"change": "gate:1", "sub": k[0], "theme_id": k[1],
                                                    "now": ["T3-001"], "changed": i < 3} for i, k in enumerate(owed)])
    O = vlib.owed_rechecks(d2, "C1")[0]
    check("three in thirty moved: the sample stands", not O["escalated"] and not O["missing"], O["missing"])
    shutil.rmtree(d2, ignore_errors=True)

    # ---- 6. stage B2: the edits of scheme_edits.jsonl and your own placements ---------------------
    tv.wjl(os.path.join(out, "author_items.jsonl"), [{"sub": "denmark", "theme_id": "t01", "third_order": ["T3-001"],
                                                      "confidence": "clear"}])
    tv.wjl(os.path.join(out, "gold_items.jsonl"), [{"sub": "sweden", "theme_id": "t02", "third_order": ["T3-002"],
                                                    "confidence": "clear", "reason": "r"}])
    tv.wjl(os.path.join(out, "scheme_edits.jsonl"), [
        {"round": 1, "theme": "T3-002", "field": "must_not_show", "caused_by": ["denmark/t01"], "was": "x",
         "now": "a call goes to T3-001", "why": "w", "kind": "scheme-ambiguous"}])
    rc, o = c("rechecks", "--owed", "--stage", "B2")
    check("an edit at B2 owes your placements on the themes it names", rc == 0 and "owed: denmark:t01" in o
          and "owed: sweden:t02" in o and "edit:1" in o, o)
    rc, o = c("recheck", "denmark:t01", "--change", "edit:1", "--theme", "T3-002", "--codes", "c0001", "--reason", "author-error",
              "--stage", "B2")
    check("a recheck at B2 that moves your placement leaves author_items as written", rc == 0 and "stays as you wrote it" in o
          and jl(os.path.join(out, "author_items.jsonl"))[0]["third_order"] == ["T3-001"], o)
    rc, o = c("recheck", "sweden:t02", "--change", "edit:1", "--theme", "T3-002", "--codes", "c0002", "--reason", "holds",
              "--stage", "B2")
    with open(os.path.join(out, "scheme_edits.jsonl"), "a") as f:
        f.write(json.dumps({"round": 1, "theme": "T3-001", "field": "must_show", "caused_by": ["denmark/t01"], "was": "a",
                            "now": "b", "why": "w", "kind": "scheme-ambiguous"}) + "\n")
    O = {o_["ref"]: o_ for o_ in vlib.owed_rechecks(out, "B2")}
    check("a later edit starts from the rechecked placements", O["edit:2"]["candidates"] == [], O["edit:2"]["candidates"])
    check("the earlier edit is done", not O["edit:1"]["missing"] and O["edit:1"]["moved"] == 1, O["edit:1"])

    # ---- 7. the concepts behind a placement --------------------------------------------------------
    tv.wjl(af, [{"sub": "denmark", "theme_id": "t01", "third_order": ["T3-001"], "support": ["c0001"]}])
    rc, o = c("reassign", "denmark:t01", "--theme", "T3-001,T3-002", "--codes", "T3-001=c0001;T3-002=c0001", "--reason", "x",
              "--stage", "C2")
    check("reassign refuses a second theme with no concept of its own", rc == 1 and "no concept of its own" in o, o)
    rc, o = c("reassign", "denmark:t01", "--theme", "T3-001,T3-002", "--codes", "T3-001=c0001", "--reason", "x", "--stage", "C2")
    check("reassign refuses a theme with no concepts", rc == 1 and "T3-002 names no concept" in o, o)
    rc, o = c("reassign", "denmark:t01", "--theme", "T3-001,T3-002", "--codes", "T3-001=c0001;T3-002=c0003", "--reason", "joint",
              "--stage", "C2")
    row = jl(af)[0]
    check("reassign keeps the concepts behind each theme on the line and the move", rc == 0
          and row["support_by_theme"] == {"T3-001": ["c0001"], "T3-002": ["c0003"]} and row["support"] == ["c0001"]
          and row["moves"][-1]["support"] == {"T3-001": ["c0001"], "T3-002": ["c0003"]}, json.dumps(row))
    rc, o = c("mint", "--label", "x", "--trigger", "denmark:t01", "--codes", "c0001")
    check("mint refuses without a provisional gate", rc == 1 and "--gate" in o, o)
    rc, o = c("mint", "--label", "x", "--trigger", "denmark:t01", "--gate", "g")
    check("mint at B1 refuses a trigger without its concepts", rc == 1 and "--codes" in o, o)
    rc, o = c("mint", "--label", "edge", "--trigger", "denmark:t02", "--gate", "a border held", "--codes", "c0002")
    sc = jl(os.path.join(out, "scheme", "scheme_current.jsonl"))
    new = [r for r in sc if r.get("label") == "edge"]
    check("mint at B1 writes the provisional gate and the trigger's concepts", rc == 0 and new
          and new[0].get("provisional_gate") == "a border held" and new[0]["members"][0].get("support") == ["c0002"], o)
    tid = new[0]["theme"] if new else "T3-003"
    rc, o = c("place", "denmark:t01", "--theme", tid, "--codes", "c0002")
    check("place refuses a concept of another second-order theme", rc == 1 and "not concepts of denmark:t01" in o, o)
    rc, o = c("place", "denmark:t01", "--theme", tid, "--codes", "c0001")
    check("place records the concepts", rc == 0 and any(m.get("support") == ["c0001"] for r in jl(os.path.join(out, "scheme", "scheme_current.jsonl"))
                                                       if r.get("theme") == tid for m in r["members"]), o)
    rc, o = c("gate", tid, "--field", "provisional_gate", "--now", "a border held against a neighbour", "--reason", "relabel")
    sc = {r["theme"]: r for r in jl(os.path.join(out, "scheme", "scheme_current.jsonl"))}
    gh = jl(os.path.join(out, "gate_history.jsonl"))
    check("gate at B1 rewrites the provisional gate and records the change", rc == 0
          and sc[tid]["provisional_gate"] == "a border held against a neighbour" and gh[-1]["stage"] == "B1"
          and gh[-1]["candidates"] == 2, o)

    shutil.rmtree(root, ignore_errors=True)
    print("\nv43.2: %d failed" % len(tv.FAILS))
    return 1 if tv.FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
