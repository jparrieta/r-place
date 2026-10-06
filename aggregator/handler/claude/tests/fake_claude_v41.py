#!/usr/bin/env python3
"""A stand-in for the claude CLI for acceptance_v41.sh in the harness test only: answers the platform
question from CONTROL/arm.json as a correct analyst would, keeps transcripts per project, and on a
resumed fork recalls the codeword from the copied transcript and reads note.txt."""
import json, os, re, sys
a = sys.argv[1:]
def opt(k): return a[a.index(k) + 1] if k in a else None
cfg = os.environ["CLAUDE_CONFIG_DIR"]; proj = os.path.join(cfg, "projects", os.environ.get("CLAUDE_CODE_PROJECT_DIR_NAME", "other"))
os.makedirs(proj, exist_ok=True)
import uuid
sid = opt("--session-id") or opt("--resume") or str(uuid.uuid4()); p = opt("-p") or ""
t = os.path.join(proj, sid + ".jsonl")
if "--fork-session" in a:
    src = os.path.join(proj, opt("--resume") + ".jsonl")
    if os.path.exists(src): open(t, "w").write(open(src).read())
out = "OK"
if "JSON object" in p:
    arm = json.load(open(os.path.join(os.path.dirname(cfg), "arm.json")))
    out = json.dumps({"platform": "claude", "a1_model": arm["A1"]["analyst"], "a1_effort": arm["A1"]["effort"], "b1_effort": arm["B1"]["effort"],
        "b2_reader_model": arm["B2"]["readers"]["model"], "b2_reader_route": "gateway (OpenRouter)", "b2_readers": arm["B2"]["readers"]["n"],
        "c2_reviewer_model": arm["C2"]["readers"]["model"], "c2_reviewer_route": "the Claude CLI on the subscription",
        "how_a_leg_continues": "each ordinary leg forks the last close's conversation", "how_to_pause": "the operator runs pause.sh",
        "d2_labelers": "GPT case leads in Codex, each resuming the room's original case lead", "codex_platform_file_present": False})
elif "what codeword" in p.lower():
    hist = open(t).read() if os.path.exists(t) else ""
    cw = (re.findall(r"codeword: (CW[0-9a-f]+)", hist) or ["none"])[0]
    note = open("note.txt").read().strip() if os.path.exists("note.txt") else "none"
    out = "CODEWORD=%s FILE=%s" % (cw, note)
with open(t, "a") as f: f.write(json.dumps({"type": "user", "sessionId": sid, "message": {"content": p}}) + "\n" + json.dumps({"type": "assistant", "sessionId": sid, "message": {"content": out}}) + "\n")
print(out)
