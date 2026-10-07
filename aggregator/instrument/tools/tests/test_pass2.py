"""B1d's stop (J, 2026-10-07): marker 1's empty run in saturation.py, the second pass's replay, mem.py reread.
Synthetic and offline: 200 rooms of 100 words each, so an average room is one room."""
import contextlib, io, json, os, sys, tempfile, unittest
from pathlib import Path
TOOLS = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(TOOLS))
import saturation, mem

N = 200                 # the check-in (60% of the words) falls past the first pass's 100 rooms


def writejl(p, rows):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))


def appendjl(p, rows):
    with open(p, "a") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


class Pass2(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name); self.out = self.root / "out"
        self.out.mkdir()
        subs = ["r%03d" % i for i in range(N)]
        writejl(self.root / "package/store/rooms.jsonl", [{"sub": s} for s in subs])
        writejl(self.root / "package/store/codes.jsonl",
                [{"sub": s, "code_id": "c0001", "text": " ".join(["w"] * 99)} for s in subs])
        writejl(self.root / "package/store/themes.jsonl",
                [{"sub": s, "theme_id": "t01", "second_order": "x"} for s in subs])
        self.order = saturation.shuffled(subs, saturation.seed(str(self.root)), "B1")
        (self.root / ".stage").write_text("B1\n")

    def tearDown(self):
        self.tmp.cleanup()

    def first_pass(self, read, last_new_at=40):
        """The first `read` rooms of the order read; kinds K1..K5 each in two rooms, the last new at room 40."""
        o = self.order
        writejl(self.out / "unplaced-B1.jsonl", [{"sub": s, "second_order": "x", "why": "test"} for s in o[:read]])
        rows, k = [], 0
        for i in range(1, last_new_at + 1, 8):          # a new kind at rooms 1, 9, 17, 25, 33, then 40
            k += 1
            rows.append({"t": "2026-10-01T00:%02d:00Z" % k, "leg": "B1b-01", "at": o[i - 1], "sub": o[i - 1],
                         "kind": "K%d" % k, "event": "minted"})
            rows.append({"t": "2026-10-01T00:%02d:30Z" % k, "leg": "B1b-01", "at": o[i], "sub": o[i],
                         "kind": "K%d" % k, "event": "placed"})
        k += 1
        rows.append({"t": "2026-10-01T01:00:00Z", "leg": "B1b-02", "at": o[last_new_at - 1], "sub": o[last_new_at - 1],
                     "kind": "K%d" % k, "event": "minted"})
        rows.append({"t": "2026-10-01T01:00:30Z", "leg": "B1b-02", "at": o[last_new_at + 1], "sub": o[last_new_at + 1],
                     "kind": "K%d" % k, "event": "placed"})
        writejl(self.out / "kinds-B1.jsonl", rows)

    def reread(self, subs, start=0, leg="B1d-01"):
        appendjl(self.out / "pass2-B1.jsonl", [{"t": "2026-10-02T%02d:%02d:00Z" % ((start + i) // 60, (start + i) % 60),
                                                "leg": leg, "sub": s, "chosen": []} for i, s in enumerate(subs)])

    def P(self):
        return saturation.pass2(str(self.root), str(self.out))

    def test_marker1_records_its_empty_run(self):
        self.first_pass(100)
        R = saturation.replay(str(self.root), str(self.out), "B1")
        m1 = R["markers"][1]
        self.assertEqual((m1["rooms_read"], m1["x"]), (80, 80.0))
        self.assertEqual((m1["run_rooms"], m1["run_x"], m1["last_new_rooms"]), (40, 40.0, 40))
        self.assertIn("marker 1's empty run: 40.0 average rooms, 40 rooms", "\n".join(saturation.status_lines(R)))
        T = saturation.pass2_target(R)
        self.assertEqual((T["rooms"], T["x"]), (40, 40.0))

    def test_floor_and_no_marker1(self):
        self.first_pass(30)                              # the list stops before any round: no marker 1
        T = saturation.pass2_target(saturation.replay(str(self.root), str(self.out), "B1"))
        self.assertEqual((T["rooms"], T["x"]), (30, 30.0))
        self.assertEqual(saturation.pass2_target({"markers": {1: {"run_rooms": 13, "run_x": 13.0}}})["rooms"], 30)

    def test_no_chosen_list(self):
        self.first_pass(100)
        self.assertEqual(self.P()["state"], "no chosen list")

    def test_chosen_then_seeded_order_then_met(self):
        self.first_pass(100)
        chosen = [self.order[90], self.order[5], self.order[60]]
        (self.out / "pass2-chosen-B1.txt").write_text("# the test's misfits\n" + "\n".join("r/" + s for s in chosen) + "\n")
        P = self.P()
        self.assertEqual((P["state"], P["next"]), ("chosen", self.order[5]))    # chosen rooms in the seeded order
        self.reread(chosen)
        P = self.P()
        self.assertEqual((P["state"], P["run_rooms"]), ("beyond the chosen rooms", 3))
        self.assertEqual(P["next"], [s for s in self.order if s not in chosen][0])
        rest = [s for s in self.order if s not in chosen][:36]
        self.reread(rest, start=3)
        P = self.P()
        self.assertEqual((P["state"], P["run_rooms"]), ("beyond the chosen rooms", 39))
        self.reread([[s for s in self.order if s not in chosen][36]], start=39)
        P = self.P()
        self.assertEqual((P["state"], P["run_rooms"], P["run_x"]), ("met", 40, 40.0))

    def test_new_kind_resets_and_an_old_one_does_not(self):
        self.first_pass(100)
        chosen = self.order[:35]
        (self.out / "pass2-chosen-B1.txt").write_text("\n".join(chosen) + "\n")
        self.reread(chosen[:10])
        appendjl(self.out / "kinds-B1.jsonl", [       # an old kind placed in room 5 of the pass, a new one in room 8
            {"t": "2026-10-02T00:04:30Z", "leg": "B1d-01", "at": None, "sub": chosen[4], "kind": "K1", "event": "placed"},
            {"t": "2026-10-02T00:06:30Z", "leg": "B1d-01", "at": None, "sub": chosen[7], "kind": "K99", "event": "minted"}])
        P = self.P()
        self.assertEqual((P["last_new"], P["new_kinds"], P["run_rooms"]), (chosen[7], ["K99"], 2))
        appendjl(self.out / "kinds-B1.jsonl", [
            {"t": "2026-10-02T00:20:00Z", "leg": "B1d-02", "at": None, "sub": chosen[11], "kind": "K100", "event": "split"}])
        self.assertEqual(self.P()["pending"], ["K100"])  # met on the room in hand, before its reread line

    def test_list_ended(self):
        self.first_pass(30)                              # no marker 1: the run is 30 rooms and 30 average rooms
        (self.out / "pass2-chosen-B1.txt").write_text(self.order[0] + "\n")
        self.reread(self.order[:181])
        appendjl(self.out / "kinds-B1.jsonl", [          # a new kind on the 181st room: 19 rooms after it, short of 30
            {"t": "2026-10-02T03:00:00Z", "leg": "B1d-04", "at": None, "sub": self.order[180], "kind": "K77", "event": "minted"}])
        self.reread(self.order[181:N], start=181)
        P = self.P()
        self.assertEqual((P["state"], P["next"], P["run_rooms"], P["last_new"]), ("list ended", None, 19, self.order[180]))
        self.assertIn("the list has ended", "\n".join(saturation.pass2_lines(P)))

    def test_dropped_from_the_chosen_list(self):
        self.first_pass(100)
        writejl(self.out / "pass2-B1.jsonl", [{"t": "2026-10-02T00:00:00Z", "leg": "B1d-01", "sub": self.order[0],
                                                "chosen": [self.order[0], self.order[1]]}])
        (self.out / "pass2-chosen-B1.txt").write_text(self.order[0] + "\n")
        P = self.P()
        self.assertEqual(P["dropped"], [self.order[1]])
        self.assertIn(self.order[1], P["chosen"])          # still counted as chosen

    def mem(self, *argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            rc = mem.main(list(argv) + ["--root", str(self.root)])
        return rc, buf.getvalue()

    def test_mem_reread(self):
        self.first_pass(100)
        (self.root / ".leg").write_text("B1b-09\n")
        rc, txt = self.mem("reread", self.order[3])
        self.assertEqual(rc, 1); self.assertIn("second pass's (B1d legs)", txt)
        (self.root / ".leg").write_text("B1d-01\n")
        rc, txt = self.mem("reread", self.order[3])
        self.assertEqual(rc, 1); self.assertIn("pass2-chosen-B1.txt first", txt)
        (self.out / "pass2-chosen-B1.txt").write_text(self.order[3] + "\n" + self.order[7] + "\n")
        rc, txt = self.mem("reread", self.order[50])
        self.assertEqual(rc, 1); self.assertIn("the chosen rooms come first", txt)
        rc, txt = self.mem("reread", self.order[7])
        self.assertEqual(rc, 0, txt); self.assertIn("recorded in the second pass", txt)
        rc, txt = self.mem("reread", self.order[7])
        self.assertEqual(rc, 1); self.assertIn("already recorded", txt)
        rc, txt = self.mem("reread", self.order[3])
        self.assertEqual(rc, 0, txt)
        rest = [s for s in self.order if s not in (self.order[3], self.order[7])]
        rc, txt = self.mem("reread", rest[1])
        self.assertEqual(rc, 1); self.assertIn("follows the seeded order: next is r/%s" % rest[0], txt)
        line = json.loads((self.out / "pass2-B1.jsonl").read_text().splitlines()[0])
        self.assertEqual((line["leg"], line["sub"], line["chosen"]), ("B1d-01", self.order[7], [self.order[3], self.order[7]]))


if __name__ == "__main__":
    r = unittest.main(exit=False, verbosity=1).result
    print("pass2: %d failed" % (len(r.failures) + len(r.errors)))
    sys.exit(1 if r.failures or r.errors else 0)
