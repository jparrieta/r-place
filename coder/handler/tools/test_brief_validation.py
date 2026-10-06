#!/usr/bin/env python3
"""Regression fixtures for corrected v30 brief validation; no model or account required."""

import gzip
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from verify_room import (BRIEF_HARD_CEILING_TOKENS, BRIEF_HEADINGS,
                         BRIEF_READER_VERSION, BRIEF_REFERENCE_TOKENS, BRIEF_REVISION,
                         PREWEEK_OPEN, Report, _item_body, _thread_of, check_brief)


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class BriefFixture:
    def __init__(self, root, items, read_mode="full", citation=True, citation_id=None,
                 removed_statement=False):
        self.room = Path(root) / "room"
        self.brief = self.room / "brief"
        self.out = self.brief / "out"
        self.out.mkdir(parents=True)
        self.items = items

        rec = self.brief / "brief_corpus.jsonl"
        rows = [{"_n_items": len(items), "_segment": "pre"}] + items
        rec.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
        for name in ("read_brief.py", "cite.py", "CONTRACT.md", "brief_corpus.txt"):
            (self.brief / name).write_text("fixture " + name + "\n", encoding="utf-8")

        text = self._brief_text(citation, citation_id, removed_statement)
        (self.out / "brief.md").write_text(text, encoding="utf-8")
        (self.out / "_transcript.jsonl").write_text(
            '{"type":"assistant","message":{"model":"fixture"}}\n', encoding="utf-8")

        reads = [{"seq": 1, "kind": "header", "tool": BRIEF_READER_VERSION, "chars": 13,
                  "item_ids": [], "item_spans": []}]
        if read_mode in ("full", "first"):
            selected = items if read_mode == "full" else items[:1]
            spans = [{"item_id": r["id"], "start": 0, "end": len(_item_body(r))}
                     for r in selected]
            reads.append({"seq": 2, "kind": "sample", "tool": BRIEF_READER_VERSION, "chars": 17,
                          "item_ids": [r["id"] for r in selected], "item_spans": spans})
        (self.out / "_read.jsonl").write_text(
            "".join(json.dumps(r) + "\n" for r in reads), encoding="utf-8")
        self.coverage = self._coverage(reads)
        self.write_evidence()

        hashed = ["read_brief.py", "cite.py", "CONTRACT.md", "brief_corpus.txt",
                  "brief_corpus.jsonl"]
        manifest = {
            "instrument": "v30", "brief_revision": BRIEF_REVISION,
            "sub": "fixture", "model": "fixture", "preweek_items": len(items),
            "sha256": {name: _sha(self.brief / name) for name in hashed},
        }
        (self.brief / "_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    def _brief_text(self, citation, citation_id, removed_statement):
        lines = ["# Brief: fixture", "", "## Evidence base"]
        if removed_statement:
            lines += ["All item bodies were deleted or removed in the supplied record (state)."]
        else:
            lines += ["The logged sample served every item on every active day (state)."]
        for heading in BRIEF_HEADINGS:
            lines += ["", "## " + heading, "A concise evidence-proportionate observation."]
            if heading == "Vernacular" and citation:
                first = self.items[0]
                quote = " ".join(_item_body(first).split())
                lines += ["> %s (`%s`)" % (quote, citation_id or first["id"])]
        return "\n".join(lines) + "\n"

    def _coverage(self, reads):
        spans = {}
        chars = sum(r["chars"] for r in reads)
        for entry in reads:
            for span in entry.get("item_spans", []):
                spans.setdefault(span["item_id"], []).append((span["start"], span["end"]))
        seen = set(spans)
        complete = {iid for iid, ivals in spans.items()
                    if min(a for a, _ in ivals) == 0 and
                    max(b for _, b in ivals) == len(_item_body(next(r for r in self.items
                                                                   if r["id"] == iid)))}
        served_threads = {_thread_of(r) for r in self.items if r["id"] in seen}
        by_day = []
        for n in range(7):
            day = "d%d" % n
            ids = {r["id"] for r in self.items
                   if (r["created_utc"] - PREWEEK_OPEN) // 86400 == n}
            by_day.append({
                "day": day, "items": len(ids), "items_seen": len(ids & seen),
                "items_complete": len(ids & complete),
                "threads": len({_thread_of(r) for r in self.items if r["id"] in ids}),
            })
        active = [r["day"] for r in by_day if r["items"]]
        unseen = [r["day"] for r in by_day if r["items"] and not r["items_seen"]]
        return {
            "tool": BRIEF_READER_VERSION, "corpus": str(self.brief / "brief_corpus.txt"),
            "items_in_corpus": len(self.items), "items_seen": len(seen),
            "items_complete": len(complete),
            "threads_in_corpus": len({_thread_of(r) for r in self.items}),
            "threads_served": len(served_threads), "threads_seen": len(served_threads),
            "threads_total": len({_thread_of(r) for r in self.items}),
            "chars_served": chars, "tokens_read": (chars + 3) // 4,
            "reference_tokens": BRIEF_REFERENCE_TOKENS,
            "hard_ceiling_tokens": BRIEF_HARD_CEILING_TOKENS,
            "days_total": 7, "days_with_items": active,
            "days_touched": len(active) - len(unseen), "days_unseen": unseen,
            "by_day": by_day,
            "coverage_unit": ("unique items with explicitly logged body spans; "
                              "complete items distinguished"),
            "advice": (("Read active days %s before going deeper." % ", ".join(unseen))
                       if unseen else
                       "All active days touched; judge whether the nine headings have enough evidence."),
        }

    def write_evidence(self):
        (self.out / "evidence.json").write_text(
            json.dumps({"version": 1, "coverage": self.coverage}, indent=2) + "\n",
            encoding="utf-8")

    def report(self):
        report = Report()
        check_brief(str(self.room), report)
        return report


def item(iid, body, day=0, thread="thread1"):
    return {"id": iid, "kind": "comment", "body": body,
            "link_id": "t3_" + thread, "created_utc": PREWEEK_OPEN + day * 86400 + 60}


class CorrectedBriefValidationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def test_header_only_read_fails(self):
        fixture = BriefFixture(self.tmp.name, [item("item01", "A useful exact quote.")],
                               read_mode="header")
        report = fixture.report()
        self.assertTrue(any(f.startswith("F3") and "only metadata/header" in f
                            for f in report.fails), report.fails)

    def test_sparse_brief_under_300_words_passes(self):
        fixture = BriefFixture(self.tmp.name, [
            item("item01", "A useful\nexact quote.", day=0),
            item("item02", "A second small observation.", day=6, thread="thread2"),
        ])
        self.assertLess(len((fixture.out / "brief.md").read_text().split()), 300)
        self.assertEqual(fixture.report().fails, [])

    def test_quote_cannot_fall_back_to_a_different_item(self):
        fixture = BriefFixture(self.tmp.name, [
            item("item01", "The quote belongs only to item one."),
            item("item02", "Different words in item two."),
        ], citation_id="item02")
        report = fixture.report()
        self.assertTrue(any(f.startswith("F4") and "not in item item02" in f
                            for f in report.fails), report.fails)

    def test_quote_must_have_been_inside_a_served_span(self):
        fixture = BriefFixture(self.tmp.name, [item("item01", "Prefix then the quoted words.")])
        reads = [
            {"seq": 1, "kind": "header", "tool": BRIEF_READER_VERSION, "chars": 13,
             "item_ids": [], "item_spans": []},
            {"seq": 2, "kind": "item", "tool": BRIEF_READER_VERSION, "chars": 17,
             "item_ids": ["item01"],
             "item_spans": [{"item_id": "item01", "start": 0, "end": 6}]},
        ]
        (fixture.out / "_read.jsonl").write_text(
            "".join(json.dumps(r) + "\n" for r in reads), encoding="utf-8")
        fixture.coverage = fixture._coverage(reads)
        fixture.write_evidence()
        report = fixture.report()
        self.assertTrue(any(f.startswith("F4") and "quote span was not served" in f
                            for f in report.fails), report.fails)

    def test_unexplained_active_day_omission_fails(self):
        fixture = BriefFixture(self.tmp.name, [
            item("item01", "Evidence from the first day.", day=0),
            item("item02", "Unread evidence from the last day.", day=6, thread="thread2"),
        ], read_mode="first")
        report = fixture.report()
        self.assertTrue(any(f.startswith("F3") and "active days were left unread" in f
                            for f in report.fails), report.fails)

    def test_named_hard_ceiling_exception_can_leave_an_active_day_unread(self):
        fixture = BriefFixture(self.tmp.name, [
            item("item01", "Evidence from the first day.", day=0),
            item("item02", "Unread evidence from the last day.", day=6, thread="thread2"),
        ], read_mode="first")
        reads = [json.loads(line) for line in
                 (fixture.out / "_read.jsonl").read_text(encoding="utf-8").splitlines()]
        reads[0]["chars"] = 299483       # with sample: 299500 chars = 74875 tokens
        (fixture.out / "_read.jsonl").write_text(
            "".join(json.dumps(r) + "\n" for r in reads), encoding="utf-8")
        fixture.coverage = fixture._coverage(reads)
        fixture.write_evidence()
        brief = fixture.out / "brief.md"
        brief.write_text(brief.read_text(encoding="utf-8").replace(
            "The logged sample served every item on every active day (state).",
            "The hard ceiling was reached with d6 still unread (state)."), encoding="utf-8")
        self.assertEqual(fixture.report().fails, [])

    def test_lower_receipt_ceiling_cannot_bypass_active_day_coverage(self):
        fixture = BriefFixture(self.tmp.name, [
            item("item01", "Evidence from the first day.", day=0),
            item("item02", "Unread evidence from the last day.", day=6, thread="thread2"),
        ], read_mode="first")
        brief = fixture.out / "brief.md"
        brief.write_text(brief.read_text(encoding="utf-8").replace(
            "The logged sample served every item on every active day (state).",
            "The ceiling was reached with d6 still unread (state)."), encoding="utf-8")
        fixture.coverage["hard_ceiling_tokens"] = fixture.coverage["tokens_read"]
        fixture.write_evidence()
        report = fixture.report()
        self.assertTrue(any(f.startswith("F3") and "hard_ceiling_tokens" in f
                            for f in report.fails), report.fails)

    def test_malformed_blockquote_with_item_id_fails(self):
        fixture = BriefFixture(self.tmp.name, [item("item01", "Exact source words.")])
        brief = fixture.out / "brief.md"
        brief.write_text(brief.read_text(encoding="utf-8").replace(
            "> Exact source words. (`item01`)",
            "> Exact source words. `item01`"), encoding="utf-8")
        report = fixture.report()
        self.assertTrue(any(f.startswith("F4") and "must end exactly" in f
                            for f in report.fails), report.fails)

    def test_zero_quotes_fail_for_a_surviving_body(self):
        fixture = BriefFixture(self.tmp.name, [item("item01", "Surviving body text.")],
                               citation=False)
        report = fixture.report()
        self.assertTrue(any(f.startswith("F4") and "no supported citation" in f
                            for f in report.fails), report.fails)

    def test_all_removed_record_allows_explicit_zero_quote_exception(self):
        fixture = BriefFixture(self.tmp.name, [item("item01", "[removed]")],
                               citation=False, removed_statement=True)
        self.assertEqual(fixture.report().fails, [])

    def test_altered_evidence_receipt_fails(self):
        fixture = BriefFixture(self.tmp.name, [item("item01", "Receipt truth matters.")])
        fixture.coverage["items_seen"] = 0
        fixture.write_evidence()
        report = fixture.report()
        self.assertTrue(any(f.startswith("F3") and "coverage.items_seen" in f
                            for f in report.fails), report.fails)

    def test_harness_cannot_forge_an_empty_preweek(self):
        room = Path(self.tmp.name) / "room"
        out = room / "brief" / "out"
        record = room / "record"
        out.mkdir(parents=True)
        record.mkdir(parents=True)
        brief_md = out / "brief.md"
        brief_md.write_text("# Empty fixture\n\nThe harness found no items.\n", encoding="utf-8")
        (out / "_transcript.jsonl").write_text('{"type":"assistant"}\n', encoding="utf-8")
        with gzip.open(str(record / "preweek.jsonl.gz"), "wt", encoding="utf-8") as fh:
            fh.write(json.dumps(item("item01", "This proves the week was not empty.")) + "\n")
        manifest = {
            "instrument": "v30", "brief_revision": BRIEF_REVISION, "model": "harness",
            "kind": "harness", "preweek_items": 0,
            "brief": "harness-written; no pre-week exists",
            "sha256": {"out/brief.md": _sha(brief_md)},
        }
        (room / "brief" / "_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        report = Report()
        check_brief(str(room), report)
        self.assertTrue(any(f.startswith("F1") and "raw pre-week" in f for f in report.fails),
                        report.fails)

    def test_verified_raw_zero_harness_needs_no_fake_transcript(self):
        room = Path(self.tmp.name) / "room"
        out = room / "brief" / "out"
        record = room / "record"
        out.mkdir(parents=True)
        record.mkdir(parents=True)
        brief_md = out / "brief.md"
        brief_md.write_text("# Empty fixture\n\nThe harness verified a silent week.\n",
                            encoding="utf-8")
        with gzip.open(str(record / "preweek.jsonl.gz"), "wt", encoding="utf-8") as fh:
            fh.write("")
        manifest = {
            "instrument": "v30", "brief_revision": BRIEF_REVISION, "model": "harness",
            "kind": "harness", "preweek_items": 0,
            "brief": "harness-written; no pre-week exists",
            "sha256": {"out/brief.md": _sha(brief_md)},
        }
        (room / "brief" / "_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        report = Report()
        check_brief(str(room), report)
        self.assertEqual(report.fails, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
