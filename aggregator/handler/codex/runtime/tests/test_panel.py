"""Keep the phone's stage choices aligned with the shared instrument."""
import csv
import json
import re
import unittest

from runtime.common import CODEX, REPO


class PanelCatalogTests(unittest.TestCase):
    def test_stage_menu_matches_current_instrument(self):
        panel = (CODEX / 'runtime/panel.html').read_text()
        match = re.search(r'<script id="stage-catalog" type="application/json">(.*?)</script>', panel, re.S)
        self.assertIsNotNone(match)
        with (REPO / 'aggregator/instrument/tools/steps.tsv').open() as handle:
            rows = list(csv.DictReader(handle, delimiter='\t'))
        fields = ('stage', 'stage_name', 'step', 'step_name', 'repeat')
        self.assertEqual(json.loads(match.group(1)), [{key: row[key] for key in fields} for row in rows])
