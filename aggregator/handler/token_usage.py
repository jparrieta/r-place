"""Token use per leg and per stage of a run, each API call counted once.

Read-only. Reads the run's leg list (CONTROL/snapshots/INDEX.tsv, plus the open leg from
CONTROL/active_launch.json), the transcripts in CONTROL/.cc/projects/run/ (usage fields only,
subagents included) and the step order in 00_GIVE-THE-AGENT/tools/steps.tsv.
Writes memory/token-usage.tsv (one row per leg, in close order) and
memory/token-usage-by-stage.tsv (one row per stage, in the instrument's order).

A call is one message id. Claude Code writes one line per content block with the same usage,
and a forked leg copies its parent's lines; both are counted once, at the first leg that holds
them. Context = input + cache write + cache read of a call.
usage: python3 aggregator/handler/token_usage.py [RUN_DIR]
"""
import csv, glob, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "runs" / "claude-v43-1"
C = RUN / "CONTROL"; TDIR = C / ".cc" / "projects" / "run"; MEM = HERE / "memory"
K = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")

def legs():
    out = []; p = C / "snapshots" / "INDEX.tsv"
    if p.exists():
        for r in csv.DictReader(open(p), delimiter="\t"):
            out.append((r["label"], r.get("session_id") or "", r.get("closed_utc") or "", "closed"))
    a = C / "active_launch.json"
    if a.exists():
        d = json.load(open(a)); lab = d.get("label", ""); sid = d.get("requested_session_id", "")
        if lab and lab not in [x[0] for x in out]:
            out.append((lab, sid, "", "open"))
    return out

def calls(sid):
    """message id -> (usage, timestamp, model, is_sub), last line per id wins; compactions."""
    res = {}; comp = 0
    files = [TDIR / (sid + ".jsonl")] + [Path(x) for x in sorted(glob.glob(str(TDIR / sid / "**" / "*.jsonl"), recursive=True))]
    for f in files:
        if not f.exists(): continue
        sub = f.name != sid + ".jsonl"
        for line in open(f, encoding="utf-8", errors="replace"):
            try: d = json.loads(line)
            except ValueError: continue
            if not sub and (d.get("isCompactSummary") or d.get("subtype") == "compact_boundary"): comp += 1
            m = d.get("message") or {}
            if d.get("type") == "assistant" and isinstance(m, dict) and isinstance(m.get("usage"), dict) and m.get("model") != "<synthetic>":
                res[m.get("id") or line[:64]] = (m["usage"], d.get("timestamp", ""), m.get("model", ""), sub)
    return res, comp

seen = set(); rows = []
for label, sid, closed, state in legs():
    if not sid: continue
    cs, comp = calls(sid)
    new = {i: v for i, v in cs.items() if i not in seen}; seen |= set(cs)
    tot = {k: sum(int(v[0].get(k) or 0) for v in new.values()) for k in K}
    main = sorted((v for v in cs.values() if not v[3]), key=lambda v: v[1])
    ctx = [sum(int(v[0].get(k) or 0) for k in K[:3]) for v in main]
    rows.append({"leg": label, "stage": label.split(".")[0], "state": state, "closed_utc": closed,
                 "session": sid[:8], "calls": len(new), "sub_calls": sum(1 for v in new.values() if v[3]),
                 **tot, "context_end": ctx[-1] if ctx else 0, "context_peak": max(ctx) if ctx else 0,
                 "compactions": comp, "models": ",".join(sorted({v[2] for v in new.values()}))})

cols = ["leg", "stage", "state", "closed_utc", "session", "calls", "sub_calls", *K, "context_end", "context_peak", "compactions", "models"]
with open(MEM / "token-usage.tsv", "w", newline="") as f:
    w = csv.DictWriter(f, cols, delimiter="\t"); w.writeheader(); w.writerows(rows)

order = []
for r in csv.DictReader(open(RUN / "00_GIVE-THE-AGENT" / "tools" / "steps.tsv"), delimiter="\t"):
    if r["stage"] not in order: order.append(r["stage"])
scols = ["order", "stage", "legs", "open_legs", "calls", *K, "total_tokens", "context_peak", "compactions"]
with open(MEM / "token-usage-by-stage.tsv", "w", newline="") as f:
    w = csv.writer(f, delimiter="\t"); w.writerow(scols)
    for i, s in enumerate(order, 1):
        rs = [r for r in rows if r["stage"] == s]
        t = {k: sum(r[k] for r in rs) for k in K}
        w.writerow([i, s, len(rs), sum(r["state"] == "open" for r in rs), sum(r["calls"] for r in rs),
                    *[t[k] for k in K], sum(t.values()), max([r["context_peak"] for r in rs] or [0]),
                    sum(r["compactions"] for r in rs)])
for r in rows: print("\t".join(str(r[c]) for c in cols))
