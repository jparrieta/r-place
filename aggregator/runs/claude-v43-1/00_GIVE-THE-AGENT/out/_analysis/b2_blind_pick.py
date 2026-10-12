#!/usr/bin/env python3
"""B2d: the ten hard items re-placed blind (stage B2 section 3, after the last round), drawn by seed "b2d:blind" from
author_items.jsonl's 50; prints the item names only, never a placement. Reads only."""
import json, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
items = sorted(json.loads(x)["item"] for x in open(os.path.join(ROOT, "out", "author_items.jsonl"), encoding="utf-8") if x.strip())
print(" ".join(random.Random("b2d:blind").sample(items, 10)))
