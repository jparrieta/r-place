"""Restore helper (legs A1b-50 onward). Usage: restore_put.py <sub> <leg> <field> [<field> ...]
For each field named (doing, week, named, goal, unsettled, ended, made, ...), take the pre-cut
line marked "+" in that leg's section of out/_handling/pretrim-A1/review/<sub>.md and put it
in place of the note's current line for that field in out/rooms/<sub>.md. Only my own earlier
words are copied; nothing else in the note changes. Prints the note's word count before and after.
Fails without writing if a field's "+" line or the note's line is missing."""
import sys, re
args = [a for a in sys.argv[1:] if a != "--force"]
force = "--force" in sys.argv
sub, leg, fields = args[0], args[1], args[2:]
tok = lambda s: set(re.findall(r"[\w']+", s.lower()))
review = open("out/_handling/pretrim-A1/review/%s.md" % sub).read()
m = re.search(r"^## %s:.*?(?=^## |\Z)" % re.escape(leg), review, re.S | re.M)
if not m:
    sys.exit("no section %s in review/%s.md" % (leg, sub))
plus = [l[1:] for l in m.group(0).splitlines() if l.startswith("+") and not l.startswith("+++")]
path = "out/rooms/%s.md" % sub
note = open(path).read().split("\n")
before = len(" ".join(note).split())
for f in fields:
    key = f + ":"
    new = [l for l in plus if l.startswith(key)]
    if len(new) != 1:
        sys.exit("field %s: %d '+' lines in %s" % (f, len(new), leg))
    idx = [i for i, l in enumerate(note) if l.startswith(key)]
    if len(idx) != 1:
        sys.exit("field %s: %d lines in the note" % (f, len(idx)))
    lost = sorted(tok(note[idx[0]]) - tok(new[0]))
    if lost and not force:
        sys.exit("field %s: the current line has words the pre-cut line lacks, nothing written: %s" % (f, " ".join(lost)))
    note[idx[0]] = new[0]
open(path, "w").write("\n".join(note))
print(sub, leg, ",".join(fields), "words", before, "->", len(" ".join(note).split()))
