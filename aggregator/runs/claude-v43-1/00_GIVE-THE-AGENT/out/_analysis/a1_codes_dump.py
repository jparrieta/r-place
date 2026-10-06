"""Stage A1 section 5: every room's first-order concepts, read through mem.py (each call logged), into one file.

python3 out/_analysis/a1_codes_dump.py <outfile>
Reads out/order-A1.txt for the analysed set; for each room calls `mem.py codes --sub S --json` with a limit
large enough for the room, keeps the fields section 5 needs, and writes one JSON line per concept.
Prints each room's concept count, then the total, so a short read shows at once.
"""
import json, subprocess, sys

out = sys.argv[1]
subs = [l.rstrip("\n").split("\t")[1] for l in open("out/order-A1.txt", encoding="utf-8") if "\t" in l]
keep = ("sub", "code_id", "theme_id", "first_order", "text", "note", "hour", "item_id", "item_kind", "author")
total = 0
with open(out, "w", encoding="utf-8") as f:
    for s in subs:
        r = subprocess.run([sys.executable, "-W", "ignore", "tools/mem.py", "codes", "--sub", s, "--stage", "A1",
                            "--json", "--limit", "20000"], capture_output=True, text=True)
        n = 0
        for line in r.stdout.splitlines():
            if not line.startswith("{"):
                continue
            c = json.loads(line)
            f.write(json.dumps({k: c.get(k) for k in keep}, ensure_ascii=False) + "\n")
            n += 1
        total += n
        print(f"{s}\t{n}")
print(f"TOTAL\t{len(subs)} rooms\t{total} concepts")
