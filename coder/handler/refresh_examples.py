#!/usr/bin/env python3
"""refresh_examples.py: bring the example rooms in coder/rooms/ (and their case leads' saved sessions in
coder/lead-sessions/) up to date with the study's yard. Handler side. Reads the yard, never writes it.

    python3 coder/handler/refresh_examples.py                 # report only: what differs, room by room
    python3 coder/handler/refresh_examples.py --apply         # copy what differs from the yard
    python3 coder/handler/refresh_examples.py --add sub1,sub2 --apply   # add rooms to the examples

The yard is P("yard_rooms") (aggregator/handler/paths.py; set it in paths.json). A room is copied whole
as the yard keeps it (ROOM.md, STATE.json, run.tar.zst, materials.tar.zst, validation/), file by file,
only where the bytes differ. A room is copied only when the yard's STATE.json says stage "verified".
A file here that the yard no longer has is reported and left in place: nothing is deleted. Its lead
session is the archive STATE.json names (lead_archive), or its parts (.part00, .part01 ...) when it was
split under GitHub's 100 MB limit. Each --apply writes coder/rooms/EXAMPLES.tsv: one line per room with
its yard stage, codes, themes, the run archive's sha256 and when it was refreshed.
"""
import argparse, datetime, hashlib, json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "aggregator", "handler"))
from paths import P  # noqa: E402

ROOMS = os.path.join(REPO, "coder", "rooms")
LEADS = os.path.join(REPO, "coder", "lead-sessions")
SKIP = {".DS_Store"}


def sha(p, n=1 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(n), b""):
            h.update(b)
    return h.hexdigest()


def tree(root):
    out = {}
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if not x.startswith("_")]
        for f in files:
            if f not in SKIP:
                p = os.path.join(d, f)
                out[os.path.relpath(p, root)] = p
    return out


def lead_files(yard, state):
    """The lead session's files in the yard's _lead_sessions/: the named archive, or its parts."""
    name = os.path.basename(state.get("lead_archive") or "")
    if not name:
        return []
    src = os.path.join(os.path.dirname(yard), "_lead_sessions")
    if os.path.exists(os.path.join(src, name)):
        return [os.path.join(src, name)]
    return sorted(os.path.join(src, f) for f in os.listdir(src) if f.startswith(name + ".part"))


PART = 94371840   # 90 MiB: a lead session above it is kept as .part00, .part01 ... (GitHub refuses files over 100 MB)


def parts(dst):
    d, n = os.path.dirname(dst), os.path.basename(dst) + ".part"
    return sorted(os.path.join(d, f) for f in os.listdir(d) if f.startswith(n) and f[len(n):].isdigit()) if os.path.isdir(d) else []


def same_lead(src, dst):
    """The yard's archive against the copy here, whole or in parts."""
    if os.path.exists(dst):
        return os.path.getsize(src) == os.path.getsize(dst) and sha(src) == sha(dst)
    ps = parts(dst)
    if not ps or sum(os.path.getsize(p) for p in ps) != os.path.getsize(src):
        return False
    h = hashlib.sha256()
    for p in ps:
        with open(p, "rb") as f:
            for b in iter(lambda: f.read(1 << 20), b""):
                h.update(b)
    return h.hexdigest() == sha(src)


def split(src, dst):
    """Write the archive as parts beside dst; an old part beyond the new count is reported, not deleted."""
    old = parts(dst); k = 0
    with open(src, "rb") as f:
        while True:
            b = f.read(PART)
            if not b:
                break
            with open("%s.part%02d" % (dst, k), "wb") as o:
                o.write(b)
            k += 1
    for p in old[k:]:
        print("  left in place, no longer part of the archive: %s" % os.path.basename(p))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--apply", action="store_true", help="copy what differs (default: report only)")
    ap.add_argument("--add", default="", help="comma-separated rooms to add to the examples")
    a = ap.parse_args()
    yard = P("yard_rooms")
    if not os.path.isdir(yard):
        sys.exit("the yard is not at %s: set yard_rooms in aggregator/handler/paths.json" % yard)
    subs = sorted({d for d in os.listdir(ROOMS) if os.path.isdir(os.path.join(ROOMS, d))}
                  | {s.strip() for s in a.add.split(",") if s.strip()})
    rows, todo = [], 0
    for s in subs:
        ysrc = os.path.join(yard, s)
        if not os.path.isdir(ysrc):
            print("%-16s not in the yard; left as it is" % s); continue
        state = json.load(open(os.path.join(ysrc, "STATE.json"), encoding="utf-8"))
        stage = state.get("stage", "?")
        if stage != "verified":
            print("%-16s yard stage %s, not verified; left as it is" % (s, stage)); continue
        here = os.path.join(ROOMS, s)
        yt, ht = tree(ysrc), (tree(here) if os.path.isdir(here) else {})
        pairs = [(yt[r], os.path.join(here, r)) for r in sorted(yt)]
        diff = [(src, dst) for src, dst in pairs if not os.path.exists(dst) or os.path.getsize(src) != os.path.getsize(dst) or sha(src) != sha(dst)]
        for lp in lead_files(yard, state):
            dst = os.path.join(LEADS, os.path.basename(lp))
            if not same_lead(lp, dst):
                diff.append((lp, dst))
        extra = sorted(set(ht) - set(yt))
        todo += len(diff)
        print("%-16s %d file(s) differ%s%s" % (s, len(diff), "; here only: " + ", ".join(extra) if extra else "",
                                                 "" if not diff else ": " + ", ".join(os.path.basename(d) for _, d in diff[:6])))
        if a.apply:
            for src, dst in diff:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if dst.startswith(LEADS) and os.path.getsize(src) > PART:
                    split(src, dst)
                else:
                    shutil.copy2(src, dst)
        rows.append((s, stage, state.get("codes", ""), state.get("themes", ""), state.get("run_archive_sha256", "")))
    if a.apply:
        utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with open(os.path.join(ROOMS, "EXAMPLES.tsv"), "w", encoding="utf-8") as f:
            f.write("sub\tyard_stage\tcodes\tthemes\trun_archive_sha256\trefreshed_utc\n")
            for r in rows:
                f.write("\t".join(str(x) for x in r) + "\t" + utc + "\n")
        print("copied %d file(s); wrote coder/rooms/EXAMPLES.tsv" % todo)
    else:
        print("%d file(s) differ; nothing copied (pass --apply)" % todo)


if __name__ == "__main__":
    main()
