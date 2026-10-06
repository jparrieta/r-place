#!/usr/bin/env python3
"""update_instrument.py — copy the reference instrument (_instrument/v31) into every room's
instrument/ directory, writing over files in place (no unlink), adding files that are new.
Prints the rooms whose fingerprint changed. Run after any change to the instrument and before
any room is started on the new version.

    python3 _tools/update_instrument.py [--rooms rooms] [--ref _instrument/v31]
"""
import argparse, os, sys, time


def write_file(path, data, aside=None):
    """Write data to path, replacing the file. On a mount that refuses to open an existing
    file for writing (some synced folders do), rename the old file aside (into `aside`, or
    beside it as .old) and write a new one."""
    mode = "wb" if isinstance(data, bytes) else "w"
    try:
        with open(path, mode, encoding=None if mode == "wb" else "utf-8") as fh:
            fh.write(data)
        return "written"
    except PermissionError:
        if not os.path.exists(path):
            raise
        if aside:
            os.makedirs(aside, exist_ok=True)
            dst = os.path.join(aside, os.path.basename(path) + ".%d" % int(time.time() * 1000))
        else:
            dst = path + ".old"
        os.replace(path, dst)
        with open(path, mode, encoding=None if mode == "wb" else "utf-8") as fh:
            fh.write(data)
        return "replaced"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rooms", default="rooms")
    ap.add_argument("--ref", default="_instrument/v31")
    ap.add_argument("--aside", default=None, help="where old files go when the mount refuses overwrites")
    a = ap.parse_args()
    files = []
    for dp, dn, fn in os.walk(a.ref):
        dn[:] = [d for d in dn if d != "__pycache__"]
        for f in fn:
            if f.endswith(".pyc"):
                continue
            rel = os.path.relpath(os.path.join(dp, f), a.ref)
            files.append((rel, open(os.path.join(dp, f), "rb").read()))
    n = changed = 0
    for r in sorted(os.listdir(a.rooms)):
        inst = os.path.join(a.rooms, r, "instrument")
        if not os.path.isdir(inst):
            continue
        n += 1
        touched = 0
        for rel, data in files:
            dst = os.path.join(inst, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(dst) and open(dst, "rb").read() == data:
                continue
            write_file(dst, data, a.aside)
            touched += 1
        if touched:
            changed += 1
    print("rooms %d, updated %d, files per room %d" % (n, changed, len(files)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
