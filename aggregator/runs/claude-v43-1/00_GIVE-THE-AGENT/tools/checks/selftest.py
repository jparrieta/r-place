"""The self-test: for every stage check, build a small fixture with one planted defect, run the
check, and report whether the planted defect fired. A check that does not fire on its own planted
defect is a defect in the package. Each stage module lists PLANTED = [(name, plant(outdir, root),
expected_substring)], where plant writes a minimal passing fixture plus the one defect.

The fixture is self-contained: every run writes its own store (the frame, three concepts, two
second-order themes, an empty transitions ledger), its own empty dropped.jsonl and FRAME.md into a
fresh temporary folder, and runs the check there with that folder as the working directory. It
never reads the folder it was started from, nor tools/tests/ (which the analyst's copy does not
ship), so the report is the same in the container, in an analyst's folder and anywhere else.
"""
import contextlib, importlib, io, json, os, shutil, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib

STAGES = ["A1", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "C5", "D1", "D2", "D3", "D4", "D5", "D6", "E1", "E2"]

STORE = {
    "rooms.jsonl": [{"sub": "denmark"}, {"sub": "asoiaf"}, {"sub": "sweden"}],
    "codes.jsonl": [
        {"sub": "denmark", "code_id": "c0117", "theme_id": "t07", "first_order": "calling for hands",
         "text": "we need more people at the border"},
        {"sub": "denmark", "code_id": "c0118", "theme_id": "t07", "first_order": "recruiting outside",
         "text": "posting on r/place for help"},
        {"sub": "asoiaf", "code_id": "c0011", "theme_id": "t02", "first_order": "defending",
         "text": "hold the line"}],
    "themes.jsonl": [{"sub": "denmark", "theme_id": "t07", "second_order": "recruiting outside placers"},
                     {"sub": "asoiaf", "theme_id": "t02", "second_order": "defending the border"}],
    "transitions.jsonl": [],
}


def write_fixture(root):
    """The package every planted check runs against, written fresh."""
    S = os.path.join(root, "package", "store")
    os.makedirs(S, exist_ok=True)
    for name, rows in STORE.items():
        with open(os.path.join(S, name), "w", encoding="utf-8") as f:
            f.write("".join(json.dumps(r) + "\n" for r in rows))
    os.makedirs(os.path.join(root, "package", "denmark"), exist_ok=True)
    with open(os.path.join(root, "package", "denmark", "lexicon.md"), "w", encoding="utf-8") as f:
        f.write("# lexicon\nDannebrog: the flag\n")
    with open(os.path.join(root, "package", "FRAME.md"), "w", encoding="utf-8") as f:
        f.write("# FRAME\nself-test fixture: 3 rooms (denmark, asoiaf, sweden)\n")
    out = os.path.join(root, "out")
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "dropped.jsonl"), "w").close()      # the analysed set is the frame
    return out


def run(here, summary=False):
    fails, lines, n = 0, [], 0
    cwd = os.getcwd()

    def say(m, failed=False):
        lines.append((m, failed))
    for s in STAGES:
        try:
            mod = importlib.import_module("checks.stage_%s" % s)
        except ImportError:
            say("%s: no check module" % s, True)
            fails += 1
            continue
        planted = getattr(mod, "PLANTED", [])
        if not planted:
            say("%s: no planted defect" % s, True)
            fails += 1
            continue
        # the clean fixture: the module's own base, with no defect planted, raises no error
        clean = next((getattr(mod, b) for b in ("check_base", "plant_base", "_check_base", "base", "_base", "_fixture")
                      if callable(getattr(mod, b, None))), None)
        if clean is not None:
            planted = [("the clean fixture", clean, None)] + list(planted)
        for name, plant, expect in planted:
            n += 1
            root = tempfile.mkdtemp(prefix="selftest-%s-" % s)
            out = write_fixture(root)
            vlib.E.clear(); vlib.W.clear()
            buf = io.StringIO()
            try:
                os.chdir(root)
                with contextlib.redirect_stdout(buf if summary else sys.stdout):
                    plant(out, root)
                    ctx = {"package": os.path.join(root, "package"), "root": root, "outdir": out, "stage": s}
                    vlib.rooms(ctx)
                    mod.check(root, out, ctx)
            except Exception as e:
                say("%s %s: check raised %s" % (s, name, e), True)
                fails += 1
                continue
            finally:
                os.chdir(cwd)
            msgs = "\n".join(m for m, _, _ in vlib.E)
            if expect is None:                     # the clean fixture passes
                ok = not vlib.E
                say("%s %-28s %s" % (s, name, "clean" if ok else "RAISED: " + msgs[:200]), not ok)
            else:
                ok = expect in msgs
                say("%s %-28s %s" % (s, name, "fired" if ok else "DID NOT FIRE"), not ok)
            if not ok:
                fails += 1
            shutil.rmtree(root, ignore_errors=True)
    vlib.E.clear(); vlib.W.clear()
    for m, failed in lines:
        if failed or not summary:
            print(m)
    print("\nself-test: %d failures%s" % (fails, " (of %d checks: the clean fixtures and the planted defects)" % n if summary else ""))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(run(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), summary="--summary" in sys.argv[1:]))
