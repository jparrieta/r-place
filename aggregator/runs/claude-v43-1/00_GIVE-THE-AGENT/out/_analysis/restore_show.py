"""Read-only helper for the restore legs (A1b-49 onward): for each room named, print the diff
between the note and the handler's prototype, flag gendered pronouns in restored lines, and,
where the prototype left cuts to me, print the handler's review file. Writes nothing."""
import sys, subprocess, csv, re
base = "out/_handling/pretrim-A1/"
proto = {r["sub"]: r for r in csv.DictReader(open(base + "restored/PROTOTYPES.tsv"), delimiter="\t")}
pron = re.compile(r"\b(he|she|his|her|him|hers|himself|herself)\b", re.I)
for sub in sys.argv[1:]:
    p = proto.get(sub, {})
    print("=" * 8, sub, "put_back", p.get("groups_put_back"), "left", p.get("groups_left_to_you"),
          "now", p.get("words_now"), "proto", p.get("words_prototype"))
    d = subprocess.run(["diff", "out/rooms/%s.md" % sub, base + "restored/%s.md" % sub],
                       capture_output=True, text=True).stdout
    for line in d.splitlines():
        m = pron.findall(line) if line.startswith(">") else []
        print(line + ("   [PRONOUN: %s]" % ",".join(m) if m else ""))
    if p.get("groups_left_to_you", "0") != "0":
        txt = open(base + "review/%s.md" % sub).read()
        body = txt.split("\n## ", 1)[1] if "\n## " in txt else txt
        print("--- review ---")
        print("## " + body)
