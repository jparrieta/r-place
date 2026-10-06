#!/usr/bin/env python3
"""Model-free fixtures for coder_preflight.py."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HELPER = Path(__file__).resolve().with_name("coder_preflight.py")
SECTIONS = ["## Chronology", "## Relations", "## Posts against comments",
            "## Counter-reading", "## Saturation", "## Selection", "## Absence"]


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def fixture(root):
    out = root / "out"
    out.mkdir()
    (root / "_manifest.json").write_text(json.dumps({"role": "fleet coder", "batch": "01"}))
    records = [{"_slice": {"batch": "01", "n_threads": 2},
                "_thread_index": [{"thread_id": "aaaaa"}, {"thread_id": "bbbbb"}]}]
    records.append({"id": "aaaaa", "kind": "post", "title": "alpha", "selftext": ""})
    records.append({"id": "bbbbb", "kind": "post", "title": "exclude this", "selftext": ""})
    for number in range(9):
        records.append({"id": "c%04d" % number, "kind": "comment",
                        "link_id": "t3_bbbbb", "body": "reply %d" % number})
    write_jsonl(root / "coder_corpus.jsonl", records)
    journal = [
        {"kind": "thread", "rec": {"thread_id": "aaaaa", "read": "full", "verdict": "coded"}},
        {"kind": "code", "rec": {"code_id": "c0001", "thread_id": "aaaaa"}},
        {"kind": "thread", "rec": {"thread_id": "bbbbb", "read": "triaged",
         "verdict": "out_of_scope",
         "excluded_quote": {"item_id": "bbbbb", "start": 0, "end": 12, "text": "exclude this"}}},
    ]
    write_jsonl(out / "_journal.jsonl", journal)
    write_jsonl(out / "_read.jsonl", [
        {"kind": "thread", "thread_id": "aaaaa"},
        {"kind": "windows", "served": [["bbbbb", "triaged"]]},
    ])
    body = "\n\n".join(section + "\n" + ("substantive account [closed] " * 8)
                         for section in SECTIONS)
    (out / "case.md").write_text(body, encoding="utf-8")
    (out / "notes.md").write_text("notes " * 50, encoding="utf-8")
    return out / "_journal.jsonl"


class PreflightTest(unittest.TestCase):
    def run_helper(self, root):
        return subprocess.run([sys.executable, str(HELPER)], cwd=root,
                              capture_output=True, text=True)

    def test_complete_preconsolidation_fixture_passes_without_mutation(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            journal = fixture(root)
            before = journal.read_bytes(), sorted(str(p.relative_to(root)) for p in root.rglob("*"))
            result = self.run_helper(root)
            after = journal.read_bytes(), sorted(str(p.relative_to(root)) for p in root.rglob("*"))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("PREFLIGHT PASSED", result.stdout)
            self.assertEqual(before, after)

    def test_missing_live_code_fails(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            journal = fixture(root)
            rows = [json.loads(line) for line in journal.read_text().splitlines()]
            write_jsonl(journal, [row for row in rows if row.get("kind") != "code"])
            result = self.run_helper(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no LIVE code", result.stdout)

    def test_ten_item_exclusion_without_citation_fails(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            journal = fixture(root)
            rows = [json.loads(line) for line in journal.read_text().splitlines()]
            for row in rows:
                if row.get("kind") == "thread" and row["rec"]["thread_id"] == "bbbbb":
                    row["rec"].pop("excluded_quote")
            write_jsonl(journal, rows)
            result = self.run_helper(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("C5 exclusion citation", result.stdout)


if __name__ == "__main__":
    unittest.main()
