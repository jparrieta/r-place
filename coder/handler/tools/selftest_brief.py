#!/usr/bin/env python3
"""selftest_brief.py — the brief stage on a copy of one room, no model called.

    python3 _tools/selftest_brief.py --room rooms/<sub> [--out DIR] [--keep]

Copies the room (without its brief, run, snapshots and forks), builds brief/ with
`room.py brief`, lets simbrief.py play the writer when the corpus is nonempty, runs
`room.py check --brief`, and prints SELFTEST-BRIEF PASSED. Harness-generated empty briefs go
straight to validation: no simulated writer or fake transcript is attached to them.
"""
import argparse, json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
INSTRUMENT = os.path.abspath(os.path.join(HERE, "..", "_instrument", "v30"))


def sh(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--room", required=True)
    ap.add_argument("--out")
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    src = os.path.abspath(a.room)
    out = os.path.abspath(a.out) if a.out else tempfile.mkdtemp(prefix="selftest_brief_")
    room = os.path.join(out, os.path.basename(src))
    if os.path.exists(room):
        shutil.rmtree(room)
    shutil.copytree(src, room, ignore=shutil.ignore_patterns("brief", "run", "snapshots", "forks",
                                                              "__pycache__", "brief_failed_*"))
    # Test the coordinated canonical instrument rather than whichever frozen copy happens
    # to be in the source room. Only the disposable self-test copy is changed.
    room_instrument = os.path.join(room, "instrument")
    for name in ("newbrief.py", "read_brief.py", "cite.py", "render_corpus_v30.py",
                 "CONTRACT-brief-writer.v30.md"):
        destination = os.path.join(room_instrument, name)
        if os.path.exists(destination):
            os.chmod(destination, 0o644)
        shutil.copy2(os.path.join(INSTRUMENT, name), destination)

    T = os.path.join(HERE, "room.py")
    rc, o = sh(["python3", T, "brief", "--model", "scripted"], cwd=room)
    assert rc == 0, o
    manifest_path = os.path.join(room, "brief", "_manifest.json")
    with open(manifest_path, encoding="utf-8") as fh:
        manifest = json.load(fh)
    if manifest.get("kind") == "harness":
        print("  selftest: harness-generated empty brief; simulated writer skipped")
    else:
        rc, o = sh(["python3", os.path.join(HERE, "simbrief.py"),
                    os.path.join(room, "brief")], cwd=room)
        assert rc == 0, o
        print("  " + o.strip())
    rc, o = sh(["python3", T, "check", "--brief"], cwd=room)
    print("\n".join("  " + l for l in o.strip().splitlines()))
    assert rc == 0 and "PASSED" in o, o
    rc, o = sh(["python3", T, "status"], cwd=room)
    assert "brief            present" in o or "brief            harness" in o, o
    print("SELFTEST-BRIEF PASSED (%s)" % room)
    if not a.keep:
        shutil.rmtree(out, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
