#!/usr/bin/env python3
"""prior_runs.py — what was done to each room before the yard existed.

    python3 _tools/prior_runs.py [--yard .] [--runs ../..] [--no-stamp]

Reads every earlier coder run under Layer A/50_coding_runs (the batch tarballs and the run
folders), the hub runs, and 40_analysis/coder_version/coder_version.csv (which run sourced each
of the 300 rooms in the v35 aggregator package), and writes:

  PRIOR-RUNS.tsv            one line per (room, run): the instrument version and fingerprint,
                            the variant, the model that did the reading (from the manifest where
                            it was recorded, else from the transcript, else "unrecorded"), when
                            it ran, whether it completed, and whether it is the run whose codes
                            are in the v35 package;
  rooms/<sub>/STATE.json    a "prior_runs" list on every room that has one, which status.py
                            summarises into STATUS.tsv's coded_before / coded_under / coded_by /
                            in_v35_package columns.

Nothing here reads a room's record or runs an agent. The hub runs (h2, v25) are listed with
kind "hub" and are not counted as coding.
"""
import argparse, csv, glob, io, json, os, sys, tarfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from status import write_file  # the rename-aside writer the mount needs

SKIP_TGZ_PREFIX = ("brief", "briefs")


def iso(t):
    return time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(t)) if t else ""


def transcript_facts(fh, maxlines=100000):
    """First assistant model id, first and last timestamps, from a Claude Code transcript."""
    model, first, last = None, None, None
    for n, raw in enumerate(fh):
        try:
            d = json.loads(raw)
        except Exception:
            continue
        ts = d.get("timestamp")
        if ts:
            first = first or ts
            last = ts
        if model is None and d.get("type") == "assistant":
            model = (d.get("message") or {}).get("model")
        if n > maxlines:
            break
    return model, first, last


class RunDir:
    """One run directory, inside a tarball or on disk."""
    def __init__(self, source, path, files):
        self.source, self.path, self.files = source, path, files  # files: name -> (reader, mtime)

    def has(self, name):
        return name in self.files

    def read_json(self, name):
        if name not in self.files:
            return None
        try:
            return json.load(self.files[name][0]())
        except Exception:
            return None

    def mtime(self, name):
        return self.files[name][1] if name in self.files else None


def rundirs_from_tar(tgz):
    """Group tar members by run directory: the directory holding _manifest.json or out/_run.json."""
    out = {}
    with tarfile.open(tgz, "r:gz") as tf:
        members = [m for m in tf.getmembers() if m.isfile()]
        roots = set()
        for m in members:
            if m.name.endswith("/_manifest.json"):
                roots.add(m.name[:-len("/_manifest.json")])
            elif m.name.endswith("/out/_run.json"):
                roots.add(m.name[:-len("/out/_run.json")])
        nested = {r for r in roots if any(r.startswith(o + "/") for o in roots)}  # a fleet's batch dirs
        roots = sorted(roots, key=len, reverse=True)
        skip = tuple(r for r in roots if r in nested or "/briefs/" in r + "/" or os.path.basename(r).startswith("brief"))
        files_by_root = {r: {} for r in roots if r not in skip}
        for m in members:  # one sequential pass: a gzip tar cannot be read out of order cheaply
            root = next((r for r in roots if m.name.startswith(r + "/")), None)
            if root is None or root in skip:
                continue
            rel = m.name[len(root) + 1:]
            if rel.startswith("__pycache__") or rel.endswith((".pyc", "corpus.txt", "coder_corpus.jsonl")):
                continue  # not needed, and the corpora are the bulk of the archive
            data = tf.extractfile(m).read()
            files_by_root[root][rel] = (lambda b=data: io.BytesIO(b), m.mtime)
        for root, files in files_by_root.items():
            out[root] = RunDir(os.path.basename(tgz), root, files)
    return out


def rundirs_from_folder(folder):
    out = {}
    roots = set()
    for p in glob.glob(os.path.join(folder, "**", "_manifest.json"), recursive=True):
        roots.add(os.path.dirname(p))
    for p in glob.glob(os.path.join(folder, "**", "out", "_run.json"), recursive=True):
        roots.add(os.path.dirname(os.path.dirname(p)))
    for root in sorted(roots):
        if "/forks/" in root or "/snapshots/" in root or "/briefs/" in root + "/" or os.path.basename(root).startswith("brief"):
            continue
        # a v29 fleet keeps batch dirs under the run root; keep the root only
        if any(root.startswith(r + "/") for r in roots if r != root):
            continue
        files = {}
        for dp, dn, fn in os.walk(root):
            dn[:] = [d for d in dn if d not in ("__pycache__", "forks", "snapshots")]
            for f in fn:
                p = os.path.join(dp, f)
                rel = os.path.relpath(p, root)
                files[rel] = (lambda p=p: open(p, "rb"), os.path.getmtime(p))
        out[root] = RunDir(os.path.basename(folder), os.path.relpath(root, os.path.dirname(folder)), files)
    return out


def describe(rd):
    """One record per run directory."""
    man = rd.read_json("_manifest.json") or {}
    runj = rd.read_json("out/_run.json") or {}
    base = os.path.basename(rd.path)
    kind = "hub" if base.startswith("hub_") else "coder"
    sub = man.get("sub") or (base[4:] if base.startswith(("run_", "hub_")) else base)
    model = man.get("model_id") or None
    model_source = "manifest" if model else ""
    if not model and man.get("model") and str(man.get("model")).startswith("claude-"):
        model, model_source = man["model"], "manifest"
    first = last = None
    if rd.has("out/_transcript.jsonl"):
        tm, first, last = transcript_facts(rd.files["out/_transcript.jsonl"][0]())
        if not model and tm:
            model, model_source = tm, "transcript"
    if not model and man.get("model"):
        model, model_source = str(man["model"]), "manifest (name only)"
    if not model:
        model, model_source = "unrecorded", ""
    # complete: the deliverables exist (codes, case, themes), or the run was closed at least once
    complete = (rd.has("out/codes.jsonl") and rd.has("out/case.md") and rd.has("out/themes.jsonl")) \
        or bool(runj.get("verdict")) or (runj.get("close_calls") or 0) >= 1
    if kind == "hub":
        complete = rd.has("out/hub.md")
    if model == "unrecorded" and "_contaminated_opus_start" in rd.path:
        model, model_source = "opus", "folder name"
    started = first or iso(rd.mtime("_manifest.json"))
    finished = last or iso(rd.mtime("out/_run.json")) or ""
    return {
        "sub": sub, "run": rd.source, "path": rd.path, "kind": kind,
        "instrument": man.get("instrument") or runj.get("instrument") or "",
        "fingerprint": man.get("instrument_fingerprint") or "",
        "variant": man.get("variant") or "",
        "model": model, "model_source": model_source,
        "model_note": (man.get("model_note") or "").replace("\n", " ").strip(),
        "started_utc": started or "", "finished_utc": finished or "",
        "items": man.get("items") or "", "threads": man.get("threads") or "",
        "complete": "yes" if complete else "no",
        "verdict": runj.get("verdict") or "",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--yard", default=".")
    ap.add_argument("--runs", default=None, help="Layer A/50_coding_runs (default: the yard's parent)")
    ap.add_argument("--coder-version", default=None, help="coder_version.csv (default: ../../40_analysis/coder_version/)")
    ap.add_argument("--no-stamp", action="store_true")
    a = ap.parse_args()
    yard = os.path.abspath(a.yard)
    runs = os.path.abspath(a.runs or os.path.join(yard, ".."))
    cv = a.coder_version or os.path.join(runs, "..", "40_analysis", "coder_version", "coder_version.csv")

    records = []
    for tgz in sorted(glob.glob(os.path.join(runs, "*.tar.gz"))):
        if os.path.basename(tgz).startswith(SKIP_TGZ_PREFIX):
            continue
        for rd in rundirs_from_tar(tgz).values():
            records.append(describe(rd))
    for folder in sorted(glob.glob(os.path.join(runs, "*"))):
        if not os.path.isdir(folder) or os.path.basename(folder) in ("yard_v30", "v1_v2_superseded", "v3"):
            continue
        for rd in rundirs_from_folder(folder).values():
            records.append(describe(rd))

    # the v35 package's source run per room
    package = {}
    if os.path.exists(cv):
        for row in csv.DictReader(open(cv, encoding="utf-8")):
            package[row["sub"]] = row["batch"]
    for r in records:
        b = package.get(r["sub"])
        r["in_v35_package"] = "yes" if b and (r["run"].startswith(b) or r["path"].startswith(b) or b in r["run"] or b in r["path"]) and r["kind"] == "coder" and "_contaminated" not in r["path"] else "no"

    records.sort(key=lambda r: (r["sub"].lower(), r["started_utc"], r["run"]))
    cols = ["sub", "run", "path", "kind", "instrument", "fingerprint", "variant", "model", "model_source",
            "started_utc", "finished_utc", "items", "threads", "complete", "verdict", "in_v35_package", "model_note"]
    text = "\t".join(cols) + "\n" + "".join("\t".join(str(r.get(c, "")) for c in cols) + "\n" for r in records)
    write_file(os.path.join(yard, "PRIOR-RUNS.tsv"), text)

    stamped = 0
    if not a.no_stamp:
        by_sub = {}
        for r in records:
            by_sub.setdefault(r["sub"], []).append(r)
        for room in sorted(glob.glob(os.path.join(yard, "rooms", "*"))):
            sub = os.path.basename(room)
            sp = os.path.join(room, "STATE.json")
            if not os.path.exists(sp):
                continue
            st = json.load(open(sp, encoding="utf-8"))
            prior = [{k: r[k] for k in ("run", "path", "kind", "instrument", "fingerprint", "variant", "model",
                                        "model_source", "started_utc", "finished_utc", "complete", "verdict",
                                        "in_v35_package")} for r in by_sub.get(sub, [])]
            if prior or "prior_runs" in st:
                st["prior_runs"] = prior
                write_file(sp, json.dumps(st, indent=1))
                stamped += 1
    from collections import Counter
    print(len(records), "run records;", stamped, "rooms stamped")
    print("by run:", sorted(Counter(r["run"] for r in records).items()))
    print("by model:", sorted(Counter((r["model"], r["model_source"]) for r in records).items()))
    print("in v35 package:", sum(r["in_v35_package"] == "yes" for r in records))


if __name__ == "__main__":
    main()
