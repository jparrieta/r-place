#!/usr/bin/env python3
"""D4a-01, J's answer to QD4-001 (option b): revert the two amendments made after the D3 freeze (move 198 on P05,
history lines 173 to 176; move 199 on A11, history lines 177 to 180) by restoring the frozen records and appending
history lines, so that the model is the D3 version again. The frozen records are taken byte for byte from the snap
taken at move 197 (out/_snap/D3-move-developing-197/model/), the last snap before the D3 freeze, after checking that
every other line of the snap's elements.jsonl and arrows.jsonl equals the current file's. Before writing, it computes
in memory the model hash the restored files would give (vlib's rule: MODEL_FILES, each preceded by its name) and
refuses unless it equals out/_closes/model-D3.sha256. Appends one history line per record (field 'record', was = the
amended record, now = the frozen record), stage D4, leg D4a-01, with reverts_lines, the move each amendment carried,
held_proposal true and the answer it follows. Without --write it prints the check and writes nothing.

    python3 out/_analysis/d4_revert.py [--write]
"""
import argparse, datetime, hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
SNAP = os.path.join(OUT, "_snap", "D3-move-developing-197", "model")
frozen_hash = open(os.path.join(OUT, "_closes", "model-D3.sha256"), encoding="utf-8").read().strip()
H = [json.loads(l) for l in open(os.path.join(OUT, "model", "history.jsonl"), encoding="utf-8") if l.strip()]
amend = {n: h for n, h in enumerate(H, 1) if h.get("stage") == "D4" and h.get("rechecked") is False}
assert sorted(amend) == list(range(173, 181)), sorted(amend)
assert {h["id"] for n, h in amend.items() if n <= 176} == {"P05"} and {h["id"] for n, h in amend.items() if n >= 177} == {"A11"}
new_files = {}
restored = {}
for name, rid in (("elements.jsonl", "P05"), ("arrows.jsonl", "A11")):
    cur = open(os.path.join(OUT, "model", name), encoding="utf-8").read().splitlines()
    snap = open(os.path.join(SNAP, name), encoding="utf-8").read().splitlines()
    if len(cur) != len(snap):
        sys.exit("%s: %d lines now, %d in the snap" % (name, len(cur), len(snap)))
    out = []
    for i, (c, s) in enumerate(zip(cur, snap)):
        cid, sid = json.loads(c)["id"], json.loads(s)["id"]
        if cid != sid:
            sys.exit("%s line %d: %s now, %s in the snap" % (name, i + 1, cid, sid))
        if cid == rid:
            restored[rid] = (json.loads(c), json.loads(s))
            out.append(s)
        else:
            if c != s:
                sys.exit("%s: %s differs from the snap, and only %s may" % (name, cid, rid))
            out.append(c)
    new_files["model/" + name] = ("\n".join(out) + "\n").encode("utf-8")
h = hashlib.sha256()
for name in vlib.MODEL_FILES:
    p = os.path.join(OUT, name)
    if name in new_files:
        h.update((name + "\n").encode("utf-8"))
        h.update(new_files[name])
    elif os.path.exists(p):
        h.update((name + "\n").encode("utf-8"))
        h.update(open(p, "rb").read())
after = h.hexdigest()
print("model hash now %s; after the revert %s; the D3 freeze %s; %s" % (
    vlib.model_hash(OUT)[:12], after[:12], frozen_hash[:12], "equal" if after == frozen_hash else "NOT EQUAL"))
if after != frozen_hash:
    sys.exit("refused: the restored files would not give the frozen hash")
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
lines = []
for rid, move, nums, mv in (("P05", "contrasting", [173, 174, 175, 176], 198),
                            ("A11", "dropping working hypotheses", [177, 178, 179, 180], 199)):
    amended, frozen = restored[rid]
    lines.append({
        "t": t, "stage": "D4", "leg": "D4a-01", "id": rid,
        "event": "amendment reverted (J, QD4-001, option b): the frozen D3 record restored, the amendment held as a "
                 "proposal",
        "move": "developing working hypotheses",
        "why": ("J's answer to QD4-001 (24 Oct 15:05 Berlin): revert the two amendments by appending history lines and "
                "restoring the frozen records, so the model is 46384686 again and the D4 check passes, and carry both "
                "as held proposals, stated in full with their rooms, lines and moves. This line restores %s as frozen "
                "at D3 (byte for byte from the snap of move 197) and reverts history lines %d to %d (move %d, %s). "
                "The amendment stays on record in those lines and in the 'was' of this one; it is a held proposal, "
                "never served to the rooms and not re-checked." % (rid, nums[0], nums[-1], mv, move)),
        "field": "record", "was": amended, "now": frozen, "reverts_lines": nums, "reverted_move": mv,
        "held_proposal": True, "rechecked": False, "frozen_version": frozen_hash,
        "adaptations": amend[nums[0]]["adaptations"], "rooms": amend[nums[0]]["rooms"]})
for l in lines:
    print("%s: was status %s, now status %s; reverts %s" % (l["id"], l["was"].get("status"), l["now"].get("status"),
                                                           l["reverts_lines"]))
if not a.write:
    print("dry run: nothing written")
    raise SystemExit(0)
for name, data in new_files.items():
    open(os.path.join(OUT, name), "wb").write(data)
with open(os.path.join(OUT, "model", "history.jsonl"), "a", encoding="utf-8") as f:
    for l in lines:
        f.write(json.dumps(l, ensure_ascii=False) + "\n")
print("restored P05 and A11; appended %d history lines (history now %d); model hash %s" % (
    len(lines), sum(1 for x in open(os.path.join(OUT, "model", "history.jsonl"), encoding="utf-8") if x.strip()),
    vlib.model_hash(OUT)))
