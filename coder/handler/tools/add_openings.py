#!/usr/bin/env python3
"""add_openings.py — write record/openings*.md into every room that lacks them, from the
gzipped record, with the room's own instrument renderer. Resumable; --seconds stops cleanly.

    python3 _tools/add_openings.py [--rooms rooms] [--seconds 150]
"""
import argparse, json, os, re, sys, time, importlib.util


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
    ap.add_argument("--seconds", type=int, default=150)
    ap.add_argument("--aside", default=None)
    a = ap.parse_args()
    t0 = time.time()
    done = skipped = 0
    rooms = sorted(os.listdir(a.rooms), key=lambda r: os.path.getsize(os.path.join(a.rooms, r, "record", "coder_corpus.jsonl.gz")))
    for r in rooms:
        room = os.path.join(a.rooms, r)
        rec = os.path.join(room, "record", "coder_corpus.jsonl.gz")
        if os.path.exists(os.path.join(room, "record", "openings.md")):
            skipped += 1
            continue
        if time.time() - t0 > a.seconds:
            print("time budget reached; done %d, skipped %d, remaining %d" % (done, skipped, len(rooms) - done - skipped))
            return 2
        state = json.load(open(os.path.join(room, "STATE.json")))
        version = state.get("instrument", "v30")
        if not re.fullmatch(r"v\d+", version):
            raise SystemExit("%s has invalid instrument version %r" % (r, version))
        renderer = os.path.join(room, "instrument", "render_openings_%s.py" % version)
        spec = importlib.util.spec_from_file_location("RO", renderer)
        RO = importlib.util.module_from_spec(spec); spec.loader.exec_module(RO)
        st = RO.write(rec, r, os.path.join(room, "record"))
        cs_p = os.path.join(room, "record", "cut_stats.json")
        cs = json.load(open(cs_p)); cs["openings"] = st
        write_file(cs_p, json.dumps(cs, indent=1), a.aside)
        done += 1
        print("%s: %d threads, %s chars%s" % (r, st["threads"], "{:,}".format(st["chars_full"]),
                                            " (+titles, digest)" if len(st["files"]) > 1 else ""))
    print("all done: %d written, %d skipped" % (done, skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
