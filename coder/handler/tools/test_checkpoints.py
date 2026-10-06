#!/usr/bin/env python3
"""Behavioral regression tests, no models or account required."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from checkpoints import (CheckpointError, capture, digest, encoded, inventory, json_write,
                         load, locked, read_json, recover_restore, restore)
import room
from codex_lead import native_export, restored_configuration


class CheckpointsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Path(self.tmp.name).resolve()
        (self.store / "workspace" / "room" / "run" / "out").mkdir(parents=True)
        (self.store / "native" / "lead").mkdir(parents=True)
        (self.store / "state").mkdir()
        self.file = self.store / "workspace" / "room" / "run" / "out" / "case.md"
        self.file.write_bytes(b"original\n")
        self.file.chmod(0o640)
        (self.store / "native" / "lead" / "session.jsonl").write_text('{"native":"complete"}\n')
        (self.store / "native" / "lead" / "auth.json").write_text("DO_NOT_ARCHIVE_AUTH")
        (self.store / "state" / "lead.json").write_text('{"turn":"one"}')

    def tearDown(self):
        self.tmp.cleanup()

    def test_roundtrip_restores_bytes_modes_mtimes_hidden_files_and_empty_dirs(self):
        root = self.store / "workspace"
        (root / ".hidden").write_text("also captured")
        (root / "empty").mkdir()
        cid = capture(self.store, {"kind": "completed"}, "base")
        old = inventory(self.store)
        self.file.write_bytes(b"mutated")
        (root / "stray").write_text("future")
        (self.store / "native" / "lead" / "session.jsonl").unlink()
        restore(self.store, cid)
        self.assertEqual(inventory(self.store), old)
        self.assertFalse((root / "stray").exists())
        self.assertFalse((self.store / "native" / "lead" / "auth.json").exists())
        self.assertTrue(any((self.store / "displaced").iterdir()))

    def test_independent_branches_never_change_parent_objects(self):
        base = capture(self.store, {"kind": "completed"}, "base")
        self.file.write_text("branch A")
        a = capture(self.store, {"kind": "completed"}, "A")
        restore(self.store, base)
        self.file.write_text("branch B")
        b = capture(self.store, {"kind": "completed"}, "B")
        restore(self.store, a)
        self.assertEqual(self.file.read_text(), "branch A")
        restore(self.store, b)
        self.assertEqual(self.file.read_text(), "branch B")
        restore(self.store, base)
        self.assertEqual(self.file.read_bytes(), b"original\n")

    def test_credentials_are_not_in_objects(self):
        capture(self.store, {"kind": "completed"})
        for p in (self.store / "objects").rglob("*"):
            if p.is_file():
                self.assertNotIn(b"DO_NOT_ARCHIVE_AUTH", p.read_bytes())

    def test_corruption_fails_before_touching_working_files(self):
        cid = capture(self.store, {"kind": "completed"})
        _, obj = load(self.store, cid)
        sha = obj["entries"][self.file.relative_to(self.store).as_posix()]["sha256"]
        blob = self.store / "objects" / sha[:2] / sha[2:]
        blob.chmod(0o600)
        blob.write_text("corrupt")
        self.file.write_text("precious live work")
        with self.assertRaises(CheckpointError):
            restore(self.store, cid)
        self.assertEqual(self.file.read_text(), "precious live work")

    def test_dedup_and_immutable_label(self):
        cid = capture(self.store, {"kind": "completed"}, "base")
        n = len([p for p in (self.store / "objects").rglob("*") if p.is_file()])
        capture(self.store, {"kind": "completed"}, "same")
        self.assertEqual(n, len([p for p in (self.store / "objects").rglob("*") if p.is_file()]))
        head = (self.store / "HEAD.json").read_bytes()
        with self.assertRaises(CheckpointError):
            capture(self.store, {"kind": "completed"}, "base")
        self.assertEqual(head, (self.store / "HEAD.json").read_bytes())
        self.assertEqual(load(self.store, "base")[0], cid)

    def test_symlink_rejected(self):
        (self.store / "workspace" / "escape").symlink_to("/etc")
        with self.assertRaises(CheckpointError):
            capture(self.store, {"kind": "completed"})

    def test_lock_blocks_another_process(self):
        code = "from checkpoints import locked; import sys\nwith locked(sys.argv[1]): pass"
        with locked(self.store):
            r = subprocess.run([sys.executable, "-B", "-c", code, str(self.store)],
                               cwd=Path(__file__).parent, capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("busy", r.stderr)

    def test_moving_store_refused(self):
        cid = capture(self.store, {"kind": "completed"})
        data = read_json(self.store / "checkpoints" / (cid + ".json"))
        data["store_path"] += "-elsewhere"
        body = encoded(data)
        other = digest(body)
        (self.store / "checkpoints" / (other + ".json")).write_bytes(body)
        with self.assertRaisesRegex(CheckpointError, "original store path"):
            load(self.store, other)

    def test_interrupted_restore_recover_retains_live_work(self):
        tx = self.store / "displaced" / "test"
        tx.mkdir(parents=True)
        json_write(self.store / "HEAD.json", {"checkpoint": "old-head"})
        json_write(self.store / "RESTORE.json", {"transaction": str(tx),
                   "previous_head": {"checkpoint": "old-head"},
                   "had": {r: True for r in ("workspace", "native", "state")}})
        (self.store / "workspace").rename(tx / "workspace")
        (self.store / "workspace").mkdir()
        (self.store / "workspace" / "partial").write_text("incomplete restore")
        json_write(self.store / "HEAD.json", {"checkpoint": "new-head"})
        recover_restore(self.store)
        self.assertEqual(read_json(self.store / "HEAD.json"), {"checkpoint": "old-head"})
        self.assertEqual(self.file.read_bytes(), b"original\n")
        self.assertTrue((tx / "workspace.incomplete" / "partial").exists())


class SchedulerMessagesTest(unittest.TestCase):
    def test_last_collect_stops_and_finish_does_not_recollect(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / "run" / "out").mkdir(parents=True)
            (p / "STATE.json").write_text('{"sub":"test"}')
            (p / "run" / "_manifest.json").write_text('{"model":"test"}')
            (p / "run" / "out" / "_gate.json").write_text(json.dumps({
                "branch": "B", "slices": [{"batch": "01"}, {"batch": "02"}], "coders": []}))
            before = (p / "STATE.json").read_bytes()
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                room.message(tmp, "collect", nn="02")
            self.assertIn("then STOP", buf.getvalue())
            self.assertIn("Do not consolidate", buf.getvalue())
            self.assertEqual(before, (p / "STATE.json").read_bytes())
            self.assertIn("Do not collect the last batch again", room.MSG["finish"])
            self.assertIn("NOT been consolidated", room.MSG["fork"])

    def test_after_fleet_snapshot_rejects_unready_room(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "STATE.json").write_text('{"sub":"test"}')
            with self.assertRaises(SystemExit):
                room.snapshot(tmp, "after-fleet")
            self.assertFalse((Path(tmp) / "snapshots").exists())


class NativeHistoryTest(unittest.TestCase):
    def test_fork_exports_native_ancestor_and_refuses_missing_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp).resolve()
            home = store / "native" / "lead" / "sessions"
            home.mkdir(parents=True)
            out = store / "workspace" / "room" / "run" / "out"
            out.mkdir(parents=True)
            parent = home / "rollout-date-parent.jsonl"
            parent_data = b'{"type":"session_meta","payload":{"id":"parent"}}\n' + \
                b'{"type":"event_msg","payload":{"type":"task_complete","turn_id":"turn-one"}}\n'
            parent.write_bytes(parent_data)
            child = home / "rollout-date-child.jsonl"
            child.write_bytes(encoded({"type": "session_meta", "payload": {"id": "child",
                "history_base": {"thread_id": "parent", "end_byte_offset": len(parent_data)}}}).replace(b"\n", b"") + b"\n")
            # Evidence export includes both segments, but the raw native child is untouched.
            original_child = child.read_bytes()
            evidence = native_export(store, {"path": str(child)}, "turn-one")
            self.assertEqual((out / "_transcript.jsonl").read_bytes(), parent_data + original_child)
            self.assertEqual(len(evidence["segments"]), 2)
            self.assertEqual(child.read_bytes(), original_child)
            parent.unlink()
            with self.assertRaisesRegex(CheckpointError, "ancestor missing"):
                native_export(store, {"path": str(child)}, "turn-one")

    def test_unfinished_native_turn_cannot_be_committed(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp).resolve() / "native" / "lead"
            home.mkdir(parents=True)
            p = home / "rollout-test.jsonl"
            p.write_text('{"type":"session_meta","payload":{"id":"test"}}\n')
            with self.assertRaisesRegex(CheckpointError, "task_complete"):
                native_export(Path(tmp).resolve(), {"path": str(p)}, "unfinished")

    def test_external_host_policy_reapplied_without_masking_other_drift(self):
        startup = {"model": "test", "sandbox": {"type": "workspaceWrite", "writableRoots": [],
            "networkAccess": False, "excludeTmpdirEnvVar": True, "excludeSlashTmp": True}}
        wanted = {"model": "test", "sandbox": {"type": "externalSandbox", "networkAccess": "restricted"}}
        self.assertEqual(restored_configuration(startup, {"configuration": wanted}, {"host_sandbox": True}), wanted)
        with self.assertRaises(CheckpointError):
            restored_configuration({**startup, "model": "different"}, {"configuration": wanted}, {"host_sandbox": True})


if __name__ == "__main__":
    unittest.main(verbosity=2)
