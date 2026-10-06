#!/usr/bin/env python3
"""audit_fleet.py — the gate before the case lead's step 4, instrument v30.

Run in the case lead's run directory after `tools/fleet.py consolidate` and after the forest
is built. It checks the things a case lead cannot see by reading:

  1. every code in staging/codes_batch_*.jsonl is in package/codes.jsonl once, unchanged,
     and no code id is minted twice across batches
  2. every code's text is the record's text at its offsets; so is every pointer's and
     every excluded_quote (v30)
  3. no thread is disposed in two batches, every batch disposed exactly the threads its
     slice holds, and the slices are contiguous
  4. every thread with verdict `coded` in package/threads.jsonl has a forest entry
  5. every code id in package/codes.jsonl sits on a node in package/forest.jsonl
  6. trees/<sub>.md holds one THREAD block per forest entry
  7. out/_gate.json records branch B, the threshold, the two counts, one slice line with
     timestamps per batch, one coder line per slice, and the consolidation

Exit 0 only when every check passes. A check that could not run is reported as FAILED,
never as passed: a gate that cannot find its inputs has not opened.

    python3 tools/audit_fleet.py --run . --sub <sub> [--record coder_corpus.jsonl]

In branch A (`--branch A`, or a gate that says so) checks 1, 3 and 7 do not apply; 2, 4, 5
and 6 run over out/codes.jsonl and out/threads.jsonl.
"""
import argparse, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def jl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def citable(r):
    """The strings cite() may have measured offsets against (close_run.py has the same)."""
    if r.get("kind") != "post":
        return {"body": r.get("body") or ""}
    t = (r.get("title") or "")
    s = (r.get("selftext") or "")
    v = {"title": t}
    if s:
        v["selftext"] = s
        v["title+selftext"] = t + "\n\n" + s
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default=".")
    ap.add_argument("--sub", required=True)
    ap.add_argument("--record", default="coder_corpus.jsonl")
    ap.add_argument("--branch", choices=["A", "B"], default=None)
    a = ap.parse_args()
    R = a.run
    fails, notes = [], []

    def fail(msg):
        fails.append(msg)

    gate_path = os.path.join(R, "out", "_gate.json")
    gate = json.load(open(gate_path)) if os.path.exists(gate_path) else None
    branch = a.branch or (gate or {}).get("branch")
    if branch not in ("A", "B"):
        fail("no branch: out/_gate.json is missing or carries none, and --branch was not given")
        return report(fails, notes)
    notes.append("branch %s" % branch)

    if branch == "B":
        p_codes = os.path.join(R, "package", "codes.jsonl")
        p_threads = os.path.join(R, "package", "threads.jsonl")
    else:
        p_codes = os.path.join(R, "out", "codes.jsonl")
        p_threads = os.path.join(R, "out", "threads.jsonl")
    p_forest = os.path.join(R, "package", "forest.jsonl")
    p_tree = os.path.join(R, "trees", "%s.md" % a.sub)
    p_rec = os.path.join(R, a.record)
    need = [p_codes, p_threads, p_forest, p_tree, p_rec]
    for p in need:
        if not os.path.exists(p):
            fail("missing: %s" % os.path.relpath(p, R))
    if fails:
        return report(fails, notes)
    consolidated = jl(p_codes)
    threads = jl(p_threads)
    live = [c for c in consolidated if not c.get("retracted")]

    # 1. consolidation, branch B
    staging = sorted(glob.glob(os.path.join(R, "staging", "codes_batch_*.jsonl")))
    if branch == "B":
        if not staging:
            fail("no staging/codes_batch_*.jsonl; run tools/fleet.py consolidate")
        else:
            cons = {}
            for c in consolidated:
                cons.setdefault(c["code_id"], []).append(c)
            seen = {}
            n_staged = 0
            for s in staging:
                b = re.search(r"codes_batch_(\d+)", s).group(1)
                for c in jl(s):
                    n_staged += 1
                    if c["code_id"] in seen and seen[c["code_id"]] != b:
                        fail("code id %s minted in batch %s and batch %s"
                             % (c["code_id"], seen[c["code_id"]], b))
                    seen[c["code_id"]] = b
                    got = cons.get(c["code_id"], [])
                    if len(got) != 1:
                        fail("code %s appears %d times in package/codes.jsonl (want 1)"
                             % (c["code_id"], len(got)))
                    elif (got[0].get("text"), got[0].get("item_id"), got[0].get("start")) != \
                            (c.get("text"), c.get("item_id"), c.get("start")):
                        fail("code %s differs between staging and the pool" % c["code_id"])
            if len(consolidated) != n_staged:
                fail("pool has %d codes, staging has %d" % (len(consolidated), n_staged))
            notes.append("staged codes %d, pooled %d, batches %d" % (n_staged, len(consolidated),
                                                                     len(staging)))

    # 2. offsets against the record
    rec, ctx = {}, set()
    for it in jl(p_rec):
        iid = it.get("id")
        if iid is None:
            continue
        rec[iid] = citable(it)
        if it.get("_slice_context"):
            ctx.add(iid)
    def at_offsets(row):
        """True when row's text is a non-empty slice of a citable string of its item. A slice
        out of range is '' in Python, so the bounds are checked and empty text never passes."""
        cand = rec.get(row.get("item_id"))
        if cand is None:
            return None
        try:
            a_, b_ = int(row.get("start")), int(row.get("end"))
        except (TypeError, ValueError):
            return False
        text = row.get("text")
        if not isinstance(text, str) or not text.strip():
            return False
        return any(0 <= a_ < b_ <= len(v) and v[a_:b_] == text for v in cand.values())

    bad = 0
    for c in live:
        ok = at_offsets(c)
        if ok is None:
            fail("code %s names item %s not in the record" % (c["code_id"], c.get("item_id")))
            continue
        if not ok:
            bad += 1
            if bad <= 5:
                fail("code %s: text is not the record's text at [%s:%s] of item %s"
                     % (c["code_id"], c.get("start"), c.get("end"), c["item_id"]))
    if bad > 5:
        fail("... and %d more codes whose text is not at its offsets" % (bad - 5))
    notes.append("codes at their offsets: %d of %d live (%d retracted)"
                 % (len(live) - bad, len(live), len(consolidated) - len(live)))
    # 2b. pointers and exclusion quotes, the same way (v30)
    p_ptr = os.path.join(os.path.dirname(p_codes), "pointers.jsonl")
    ptrs = jl(p_ptr) if os.path.exists(p_ptr) else []
    badp = 0
    for p_ in ptrs:
        ok = at_offsets(p_)
        if not ok:
            badp += 1
            if badp <= 5:
                fail("pointer %s: text is not the record's text at [%s:%s] of item %s"
                     % (p_.get("pointer_id"), p_.get("start"), p_.get("end"), p_.get("item_id")))
    badq = 0
    for t in threads:
        q = t.get("excluded_quote")
        if not q:
            continue
        if not isinstance(q, dict) or not at_offsets(q):
            badq += 1
            if badq <= 5:
                fail("thread %s: excluded_quote is not what cite() returned, or not at its offsets"
                     % t.get("thread_id"))
    notes.append("pointers at their offsets: %d of %d; exclusion quotes verified: %d of %d"
                 % (len(ptrs) - badp, len(ptrs),
                    sum(1 for t in threads if t.get("excluded_quote")) - badq,
                    sum(1 for t in threads if t.get("excluded_quote"))))

    # 3. threads and slices, branch B
    if branch == "B" and gate:
        tb = {}
        for s in sorted(glob.glob(os.path.join(R, "staging", "threads_batch_*.jsonl"))):
            b = re.search(r"threads_batch_(\d+)", s).group(1)
            for t in jl(s):
                if t["thread_id"] in tb:
                    fail("thread %s disposed in batch %s and batch %s"
                         % (t["thread_id"], tb[t["thread_id"]], b))
                tb[t["thread_id"]] = b
        for sl in gate.get("slices", []):
            want = set(sl.get("threads") or [])
            got = {t for t, b in tb.items() if b == sl["batch"]}
            if not got and want:
                fail("batch %s disposed no thread" % sl["batch"])
            elif got != want:
                fail("batch %s disposed %d threads, its slice holds %d (%d not in the slice, "
                     "%d undisposed)" % (sl["batch"], len(got), len(want), len(got - want),
                                         len(want - got)))
        code_batch = {}
        for s in staging:
            b = re.search(r"codes_batch_(\d+)", s).group(1)
            for c in jl(s):
                code_batch.setdefault(b, set()).add(c["thread_id"])
        for b, tids in code_batch.items():
            stray = [t for t in tids if tb.get(t) != b]
            if stray:
                fail("batch %s coded threads it did not dispose: %s" % (b, stray[:6]))
        sls = gate.get("slices", [])
        for i in range(1, len(sls)):
            if sls[i]["start_utc"] < sls[i - 1]["last_opening_utc"]:
                fail("slice %s opens before slice %s's last opening"
                     % (sls[i]["batch"], sls[i - 1]["batch"]))
        notes.append("slices %d, threads disposed %d" % (len(sls), len(tb)))
        for c in live:
            if c.get("item_id") in ctx:
                fail("code %s sits on an earlier slice's opening given as context" % c["code_id"])

    # 4, 5. forest
    forest = jl(p_forest)
    forest_threads = {f["thread_id"] for f in forest if f.get("community") == a.sub}
    node_codes = set()

    def walk(n):
        for cid in n.get("code_ids", []):
            node_codes.add(cid)
        for ch in n.get("children", []):
            walk(ch)
    for f in forest:
        if f.get("community") == a.sub:
            walk(f["tree"])
    coded_threads = {t["thread_id"] for t in threads if t.get("verdict") == "coded"}
    for t in sorted(coded_threads - forest_threads):
        fail("thread %s has verdict coded and no forest entry" % t)
    for t in sorted(forest_threads - coded_threads):
        fail("forest entry %s belongs to no thread with verdict coded" % t)
    for c in live:
        if c["code_id"] not in node_codes:
            fail("code %s is on no forest node" % c["code_id"])
    notes.append("forest threads %d, coded threads %d, codes on nodes %d"
                 % (len(forest_threads), len(coded_threads), len(node_codes & {c["code_id"]
                                                                            for c in live})))

    # 6. the rendered forest
    md = open(p_tree, encoding="utf-8").read()
    n_blocks = md.count("\n=== THREAD ")
    if n_blocks != len(forest_threads):
        fail("trees/%s.md has %d THREAD blocks, the forest %d entries" % (a.sub, n_blocks,
                                                                          len(forest_threads)))
    m = re.search(r"with at least one code (\d+)", md)
    if not m or int(m.group(1)) != len(forest_threads):
        fail("the forest header's coded-thread count disagrees with package/forest.jsonl")

    # 7. the gate record, branch B
    if branch == "B":
        if not gate:
            fail("no out/_gate.json")
        else:
            for k in ("threshold", "items_in_window", "chars_by_people", "slices", "coders"):
                if k not in gate:
                    fail("_gate.json lacks %s" % k)
            for sl in gate.get("slices", []):
                for k in ("batch", "first_thread", "last_thread", "start_utc",
                          "last_opening_utc", "last_item_utc"):
                    if sl.get(k) is None:
                        fail("slice %s lacks %s" % (sl.get("batch"), k))
            sb = {s["batch"] for s in gate.get("slices", [])}
            cb = {c["batch"] for c in gate.get("coders", [])}
            if sb != cb:
                fail("slices %s and coders %s do not match" % (sorted(sb - cb), sorted(cb - sb)))
            for c in gate.get("coders", []):
                if not c.get("model"):
                    fail("coder line %s has no model" % c.get("batch"))
            if not gate.get("consolidated_utc"):
                fail("_gate.json has no consolidated_utc; run tools/fleet.py consolidate")

    return report(fails, notes)


def report(fails, notes):
    for n in notes:
        print("  " + n)
    if fails:
        print("FAILED (%d):" % len(fails))
        for f in fails:
            print("  - " + f)
        return 1
    print("PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
