#!/usr/bin/env python3
"""tokens.py: token sizes, measured where they can be (J, 2026-10-11, from the B1e interview).

    python3 tools/tokens.py FILE [FILE ...]          the size of each file in the readers' tokens
    python3 tools/tokens.py --dispatched             the tokens every dispatched packet actually cost

No tokenizer of the readers' model can be installed in your Python, and the run has no network. The
exact count exists anyway: every reader call the dispatch made left its usage in
out/_fleet_raw/<NN>/<round>/<packet>/<reader>.meta.json (input tokens, from the gateway) beside the bytes
it sent (the shared pages, the packet and the return specification). This tool reads those pairs:

  --dispatched  each packet's input tokens per reader, as the gateway counted them;
  FILE ...      bytes, words, and tokens estimated at the measured tokens per byte of the model that
                served (median over single-part calls, with the spread); before any dispatch, at four
                bytes a token, and it says so. An estimate is never written as a count.
"""
import argparse, glob, json, os, statistics, sys

TAIL = ("\n\nReturn only the lines the return specification asks for, one JSON object per line, then the "
        "end marker on its own line. No prose before, between or after.")


def calls(out):
    """(served model, input tokens, bytes sent, where) for each single-part reader call with usage."""
    rows = []
    for meta in sorted(glob.glob(os.path.join(out, "_fleet_raw", "*", "**", "*.meta.json"), recursive=True)):
        try:
            m = json.load(open(meta, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(m, list) or not isinstance(m, dict):
            continue                                 # a multi-part conversation: later turns carry the thread
        tin = (m.get("usage") or {}).get("input_tokens")
        raw = os.path.dirname(os.path.dirname(meta))
        try:
            arm = json.load(open(os.path.join(raw, "arm.json"), encoding="utf-8"))
        except (OSError, ValueError):
            arm = {}
        rel = os.path.relpath(raw, os.path.join(out, "_fleet_raw"))
        stage = rel.split(os.sep)[0]
        cand = [os.path.join(out, "_packets-%s" % stage, *rel.split(os.sep)[1:]), os.path.join(out, "_packets-%s" % stage)]
        pk = next((d for d in cand if os.path.exists(os.path.join(d, "%s.md" % m.get("packet")))), None)
        spec = os.path.join(out, "RETURN-%s.md" % stage)
        if not tin or not pk or not os.path.exists(spec):
            continue
        n = 0
        for name in arm.get("shared") or []:
            p = os.path.join(pk, name)
            if os.path.exists(p):
                n += len(("<<< %s >>>\n" % name).encode()) + os.path.getsize(p) + 2
        n += len(("<<< %s >>>\n" % m.get("packet")).encode()) + os.path.getsize(os.path.join(pk, "%s.md" % m["packet"])) + 2
        n += len("<<< RETURN >>>\n".encode()) + os.path.getsize(spec) + len(TAIL.encode())
        rows.append((m.get("served") or arm.get("served") or "?", int(tin), n, os.path.relpath(meta, out)))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--out", default="out")
    ap.add_argument("--dispatched", action="store_true")
    a = ap.parse_args(argv)
    C = calls(a.out)
    if a.dispatched:
        if not C:
            print("no dispatched call with its usage under %s/_fleet_raw/" % a.out)
            return 0
        print("%-52s %-30s %10s %10s %8s" % ("call", "served", "in tokens", "bytes", "tok/B"))
        for served, tin, n, where in C:
            print("%-52s %-30s %10d %10d %8.3f" % (where[:52], served[:30], tin, n, tin / float(n)))
        return 0
    if not a.files:
        ap.print_usage()
        return 2
    by = {}
    for served, tin, n, _ in C:
        by.setdefault(served, []).append(tin / float(n))
    if by:
        served, rs = max(by.items(), key=lambda kv: len(kv[1]))
        rate = statistics.median(rs)
        how = "measured: %s, median of %d calls, %.3f tokens a byte (range %.3f to %.3f)" % (
            served, len(rs), rate, min(rs), max(rs))
    else:
        rate, how = 0.25, "NOT measured: no dispatched call yet, so four bytes a token (an assumption)"
    print("tokens per byte, " + how)
    tot_b = tot_t = 0
    for f in a.files:
        b = os.path.getsize(f)
        w = len(open(f, encoding="utf-8", errors="replace").read().split())
        t = int(round(b * rate))
        tot_b += b
        tot_t += t
        print("%-50s %9d bytes %8d words  ~%d tokens (estimate)" % (f[-50:], b, w, t))
    if len(a.files) > 1:
        print("%-50s %9d bytes %8s        ~%d tokens (estimate)" % ("total", tot_b, "", tot_t))
    return 0


if __name__ == "__main__":
    sys.exit(main())
