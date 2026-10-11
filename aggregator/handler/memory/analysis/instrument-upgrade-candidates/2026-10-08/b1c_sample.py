"""B1c: draw the saturation test's sample of the rooms read, by the rule in notes-B1.md (Leg B1c).

usage: python3 out/_analysis/b1c_sample.py [--min-rooms 30] [--min-themes 300] [--show 40]

The order: the rooms `saturation.py order --stage B1` marks read, sorted by name and shuffled with
saturation.py's own `shuffled`, seed from out/seed.txt, tag "B1c". Rooms are taken from the head
until both minimums hold. Prints each drawn room with its second-order themes, codes and words
(saturation.py's count), the running totals, and the words in average rooms.
"""
import collections
import subprocess
import sys

sys.path.insert(0, "tools")
import saturation as S  # noqa: E402


def opt(name, default):
    if name in sys.argv:
        return int(sys.argv[sys.argv.index(name) + 1])
    return default


min_rooms = opt("--min-rooms", 30)
min_themes = opt("--min-themes", 300)
show = opt("--show", 0)

root, out = ".", "out"
st = S.store(root)
w = S.words(st)
an = S.analysed(root, out, st)
avg = sum(w[s] for s in an) / len(an)

listing = subprocess.run(["python3", "tools/saturation.py", "order", "--stage", "B1"],
                         capture_output=True, text=True).stdout
read = [ln.split("\t")[1] for ln in listing.splitlines() if ln.rstrip().endswith("\tread")]

nthemes = collections.Counter(t.get("sub") for t in st["themes"])
ncodes = collections.Counter(c.get("sub") for c in st["codes"])
sd = S.seed(root)
order = S.shuffled(read, sd, "B1c")

print("seed %s, tag B1c; %d read rooms; average room %.1f words" % (sd, len(read), avg))
print("rule: at least %d rooms and at least %d second-order themes" % (min_rooms, min_themes))
print("n\tsub\tthemes\tcodes\twords\tcum_themes\tcum_codes\tcum_avg_rooms")
ct = cc = cw = 0
taken = 0
for i, sub in enumerate(order, 1):
    ct += nthemes[sub]
    cc += ncodes[sub]
    cw += w[sub]
    print("%d\t%s\t%d\t%d\t%d\t%d\t%d\t%.1f" % (i, sub, nthemes[sub], ncodes[sub], w[sub], ct, cc, cw / avg))
    if not taken and i >= min_rooms and ct >= min_themes:
        taken = i
        print("-- sample ends here: %d rooms, %d second-order themes, %d codes, %.1f average rooms" % (i, ct, cc, cw / avg))
    if taken and i >= max(taken, show):
        break
