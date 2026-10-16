#!/usr/bin/env python3
"""Order test for the keepers pattern (D3a-04, P05's re-examination).

Each argument is room:code:role, role one of plan, erase, tell, switch:
  plan    the change is proposed, agreed or begun;
  erase   keepers repair the change away as damage (or builders give it up after);
  tell    someone tells the keepers the change is intended;
  switch  a keeper stops, apologises or helps the change.
Every quote is read through tools/cite.py and printed whole. Per room the test asks two
questions of the hours: does an erase come before the first tell, and does every switch come
after the first tell (or, with no tell coded, after the first erase)?

  python3 out/_analysis/d3_order_keepers.py --items mordhau:c0018:plan mordhau:c0021:erase ...
"""
import argparse
import re
import subprocess
import sys
from collections import defaultdict

ROLES = ("plan", "erase", "tell", "switch")


def cite(room, code):
    out = subprocess.run([sys.executable, "tools/cite.py", "--room", room, "--code", code],
                         capture_output=True, text=True)
    text = out.stdout
    m = re.search(r"h\+(\d+(?:\.\d+)?)", text)
    return text, (float(m.group(1)) if m else None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", nargs="+", required=True)
    a = ap.parse_args()
    rows = defaultdict(list)
    for item in a.items:
        room, code, role = item.split(":")
        if role not in ROLES:
            sys.exit(f"bad role {role!r} in {item}")
        text, hour = cite(room, code)
        if hour is None:
            sys.exit(f"no hour for {room}/{code}")
        rows[room].append((hour, role, code, text))
    held = 0
    for room in sorted(rows):
        events = sorted(rows[room])
        print(f"== {room}")
        for hour, role, code, text in events:
            quote = [ln for ln in text.splitlines() if ln.startswith('"')]
            print(f"  h+{hour:6.2f}  {role:6}  {code}  {quote[0] if quote else text.strip()}")
        tells = [h for h, r, _, _ in events if r == "tell"]
        erases = [h for h, r, _, _ in events if r == "erase"]
        switches = [h for h, r, _, _ in events if r == "switch"]
        first_tell = min(tells) if tells else None
        anchor = first_tell if first_tell is not None else (min(erases) if erases else None)
        erase_first = bool(erases) and (first_tell is None or min(erases) <= first_tell)
        switch_after = all(anchor is not None and s >= anchor for s in switches)
        ok = erase_first and switch_after
        held += ok
        print(f"  erase before the first tell: {erase_first}; every switch after it: {switch_after}"
              f"  -> {'holds' if ok else 'fails'}")
    print(f"\nrooms: {len(rows)}; order holds in {held}")


if __name__ == "__main__":
    main()
