#!/usr/bin/env python3
"""A stand-in for the claude CLI, for the harness test only. It writes a transcript the guard can
read, and, on a launch, plays an analyst who runs `bash tools/done.sh NN` and stops."""
import json, os, subprocess, sys, uuid
a = sys.argv[1:]
if a and a[0] == "--version":
    print("fake-claude 0.0"); sys.exit(0)
cfg = os.environ.get("CLAUDE_CONFIG_DIR", os.path.expanduser("~/.fakeclaude"))
proj = os.path.join(cfg, "projects", os.environ.get("CLAUDE_CODE_PROJECT_DIR_NAME", "other"))
os.makedirs(proj, exist_ok=True)
def opt(k):
    return a[a.index(k) + 1] if k in a else None
sid = opt("--session-id") or opt("--resume")
model = opt("--model") or "unknown"
prompt = opt("-p") if "-p" in a else (a[-1] if a and not a[-1].startswith("-") else "")
t = os.path.join(proj, sid + ".jsonl")
json.dump({"argv": a, "auto_memory_off": os.environ.get("CLAUDE_CODE_DISABLE_AUTO_MEMORY")},
          open(os.path.join(cfg, "last_call.json"), "w"))
if "--fork-session" in a and opt("--resume"):   # a fork carries its parent's history
    pt = os.path.join(proj, opt("--resume") + ".jsonl")
    if os.path.exists(pt) and not os.path.exists(t):
        open(t, "w").write(open(pt).read())
def row(kind, text, stop=None):
    m = {"role": kind, "content": text}
    if kind == "assistant":
        m.update(model=model, stop_reason=stop or "end_turn",
                 usage={"input_tokens": 100, "output_tokens": 20, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0})
    return json.dumps({"type": kind, "sessionId": sid, "uuid": str(uuid.uuid4()), "message": m})
with open(t, "a") as f:
    f.write(row("user", prompt) + "\n")
    if "-p" not in a:
        nn = open(".stage").read().strip()
        r = subprocess.run(["bash", "tools/done.sh", nn], capture_output=True, text=True)
        f.write(row("assistant", "closed: " + r.stdout[-200:]) + "\n")
    else:
        ans = "goal: whether case findings compose\nopen: none\nrooms: denmark\nchanged: none\nnext: none"
        f.write(row("assistant", ans) + "\n")
        print(ans)
