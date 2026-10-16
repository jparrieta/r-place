#!/usr/bin/env python3
"""Quote several concepts in one call: each room:code goes through tools/cite.py, whose output
is printed whole (no clipping), one block per concept.

  python3 out/_analysis/d3_cite_many.py COSI:c0002 GreenCorner:c0043
"""
import subprocess
import sys


def main():
    items = sys.argv[1:]
    if not items:
        sys.exit("give room:code items")
    for item in items:
        room, code = item.split(":")
        out = subprocess.run([sys.executable, "tools/cite.py", "--room", room, "--code", code],
                             capture_output=True, text=True)
        lines = [ln for ln in out.stdout.splitlines() if ln.startswith('"')]
        print(f"[{room}/{code}]")
        print("\n".join(lines) if lines else out.stdout.strip() or out.stderr.strip())


if __name__ == "__main__":
    main()
