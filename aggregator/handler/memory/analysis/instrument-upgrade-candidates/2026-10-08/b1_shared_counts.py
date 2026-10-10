"""Count members shared between one room's dump and each partner dump.

Usage: python3 out/_analysis/b1_shared_counts.py <dir> <room> <partner> [<partner> ...]
Reads <dir>/d_<room>.txt files written by b1_dump_rooms.py and prints, per partner,
the number of shared writers and their names with the codes on each side.
"""
import os
import sys


def writers(path):
    out = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            parts = line.split()
            if len(parts) < 6:
                continue
            code, author = parts[0], parts[5] if parts[3] == "h" else parts[4]
            if parts[3] == "h":
                author = parts[5]
            else:
                author = parts[4]
            if author in ("[deleted]", "[removed]"):
                continue
            out.setdefault(author, []).append(code)
    return out


def main():
    d, room = sys.argv[1], sys.argv[2]
    base = writers(os.path.join(d, "d_%s.txt" % room))
    for p in sys.argv[3:]:
        path = os.path.join(d, "d_%s.txt" % p)
        if not os.path.exists(path):
            print("%s: no dump" % p)
            continue
        other = writers(path)
        shared = sorted(set(base) & set(other))
        print("%s: %d shared" % (p, len(shared)))
        for a in shared:
            print("  %s | %s: %s | %s: %s" % (a, room, ",".join(base[a][:6]), p, ",".join(other[a][:6])))


if __name__ == "__main__":
    main()
