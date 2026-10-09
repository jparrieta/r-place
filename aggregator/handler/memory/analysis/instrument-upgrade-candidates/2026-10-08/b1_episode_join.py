"""Add a joining room to existing episode lines, as the B1 walk records it: the room appended to
"rooms", "Added at <leg>: <evidence>" put at the start of the evidence, "Added at <leg>: <why>"
put at the end of the why. Reads a JSON list of {"episode", "room", "evidence", "why"} from a spec
file; every other line of episodes-B1.jsonl is written back byte for byte. Dry run unless --write.

usage: python3 out/_analysis/b1_episode_join.py <spec.json> --leg B1b-21 [--write]
"""
import json
import sys

spec_path = sys.argv[1]
leg = sys.argv[sys.argv.index("--leg") + 1]
write = "--write" in sys.argv
specs = {s["episode"]: s for s in json.load(open(spec_path, encoding="utf-8"))}
path = "out/episodes-B1.jsonl"
lines = open(path, encoding="utf-8").read().splitlines(keepends=True)
done = set()
out = []
for line in lines:
    if not line.strip():
        out.append(line)
        continue
    d = json.loads(line)
    s = specs.get(d["episode"])
    if not s:
        out.append(line)
        continue
    if s["room"] in d["rooms"]:
        sys.exit("PROBLEM: %s already lists %s" % (d["episode"], s["room"]))
    d["rooms"].append(s["room"])
    d["evidence"] = "Added at %s: %s %s" % (leg, s["evidence"].rstrip(), d["evidence"])
    d["why"] = "%s; Added at %s: %s" % (d["why"].rstrip(), leg, s["why"].rstrip())
    out.append(json.dumps(d, ensure_ascii=False) + "\n")
    done.add(d["episode"])
    print("%s: rooms now %s" % (d["episode"], ", ".join(d["rooms"])))
missing = set(specs) - done
if missing:
    sys.exit("PROBLEM: no line for %s" % ", ".join(sorted(missing)))
if write:
    open(path, "w", encoding="utf-8").write("".join(out))
    print("written: %d lines changed" % len(done))
else:
    print("dry run: %d lines would change" % len(done))
