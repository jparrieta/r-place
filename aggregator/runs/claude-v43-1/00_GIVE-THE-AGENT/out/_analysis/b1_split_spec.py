# usage: python3 out/_analysis/b1_split_spec.py <spec.json> <outdir>
# writes one spec file per entry, <outdir>/spec_01.json, spec_02.json ..., in the spec's order,
# so that b1_episode_join.py can apply entries for the same episode one after another
import json, os, sys

spec, outdir = sys.argv[1], sys.argv[2]
entries = json.load(open(spec))
os.makedirs(outdir, exist_ok=True)
for i, e in enumerate(entries, 1):
    p = os.path.join(outdir, "spec_%02d.json" % i)
    json.dump([e], open(p, "w"), ensure_ascii=False)
    print(p, e["episode"], e["room"])
