"""A scripted stand-in for a fleet coder: reads its slice through read.py, disposes every
thread, codes three passages it can cite, records one pointer, appends to the facts files."""
import sys, os, json, subprocess, re
rundir = sys.argv[1]; batch = sys.argv[2]
sys.path.insert(0, rundir)
from emit import Emit
from cite import Corpus
out = os.path.join(rundir, "out"); rec = os.path.join(rundir, "coder_corpus.jsonl"); corpus = os.path.join(rundir, "corpus.txt")
emit = Emit(out, corpus_path=rec); C = Corpus(rec); cite, find = C.cite, C.find
emit.stage("step1_brief"); emit.stage("step2_read")
def rd(*args):
    return subprocess.run(["python3", os.path.join(rundir, "read.py"), corpus] + list(args), capture_output=True, text=True).stdout
hdr = rd("header")
served = []
while True:
    st = json.loads(rd("state"))
    if st["threads_remaining"] == 0: break
    w = rd("windows", "25")
    served += re.findall(r"^=+\s*THREAD (\S+)", w, re.M) or []
st = json.loads(rd("state"))
# the items of the slice, for choosing passages
items = [json.loads(l) for l in open(rec) if '"id"' in l]
items = [i for i in items if "id" in i and not i.get("_context")]
threads = sorted({(i["id"] if i.get("kind")=="post" else i["link_id"][3:]) for i in items})
# read three threads whole and code a passage in each
coded = []
for t in threads[:3]:
    rd("thread", t)
    cands = [i for i in items if (i["id"] if i.get("kind")=="post" else i["link_id"][3:]) == t and len(i.get("body") or i.get("selftext") or "") > 40 and (i.get("body") or "") not in ("[deleted]","[removed]")]
    if not cands: continue
    c = None
    for it in cands[:5]:
        body = it.get("body") or it.get("selftext")
        for n in (30, 60, 120, len(body)):
            try:
                c = cite(it["id"], body[:n]); break
            except Exception:
                c = None
        if c: break
    if not c: continue
    q = body[:30]
    emit.stage("step3_codes")
    cid = emit.code(c, "saying %s (batch %s)" % (q[:15].strip().lower(), batch), thread_id=t, note="scripted")
    coded.append((t, cid, it["id"]))
    emit.stage("step2_read")
rows = []
for t in threads:
    rows.append({"thread_id": t, "read": "full" if any(x[0]==t for x in coded) else "triaged", "verdict": "coded" if any(x[0]==t for x in coded) else "out_of_scope", "reason": "scripted", "excluded_quote": None})
# a ten-item out-of-scope thread needs a cited line
sizes = {}
for i in items:
    sizes[(i["id"] if i.get("kind")=="post" else i["link_id"][3:])] = sizes.get((i["id"] if i.get("kind")=="post" else i["link_id"][3:]),0)+1
for r in rows:
    if r["verdict"]=="out_of_scope" and sizes.get(r["thread_id"],0) >= 10:
        cands = [i for i in items if (i["id"] if i.get("kind")=="post" else i["link_id"][3:]) == r["thread_id"] and len(i.get("body") or i.get("selftext") or "") > 20 and (i.get("body") or "") not in ("[deleted]","[removed]")]
        if cands:
            it = cands[0]; body = it.get("body") or it.get("selftext"); r["excluded_quote"] = cite(it["id"], body[:20])
emit.threads_bulk(rows)
# a pointer on a coded thread
if coded:
    t, cid, iid = coded[0]
    body = next(i for i in items if i["id"]==iid).get("body") or next(i for i in items if i["id"]==iid).get("selftext")
    c = None
    for n in (12, 30, 60, len(body)):
        try:
            c = cite(iid, body[:n]); break
        except Exception:
            c = None
    if c:
        emit.stage("step3_codes")
        emit.pointer(c, raw="r/place", kind="subreddit", thread_id=t, relation="mentioned-only", code_ids=[cid])
emit.stage("step7_write")
pad = ("This slice case was written by simcoder.py, the scripted stand-in the self-test uses in "
       "place of a model. It carries the sections CONTRACT.md names, one tag, and enough text to "
       "pass the scheduler's size floor, so that the yard's own checks and its self-test agree "
       "about what a passable batch looks like. Nothing in it is a reading of the material. ")
open(os.path.join(out, "case.md"), "w", encoding="utf-8").write("# r/%s, batch %s (scripted)\n\n%s\n\n## Chronology\n\nscripted [closed]\n\n## Relations — what set off what\n\nnone\n\n## Posts against comments\n\nnone\n\n## Counter-reading\n\nscripted\n\n## Saturation\n\nscripted\n\n## Selection\n\nscripted\n\n## Absence\n\nscripted\n" % (os.path.basename(os.path.dirname(rundir)) or "room", batch, pad * 2))
open(os.path.join(out, "notes.md"), "w", encoding="utf-8").write("scripted notes, batch %s. " % batch + pad)
ref = coded[0][2] if coded else (items[0]["id"] if items else "none")
open(os.path.join(rundir, "timeline.md"), "a").write("- h+%s sticky (scripted) item %s\n" % (batch, ref))
open(os.path.join(rundir, "lexicon.md"), "a").write("- term%s  %s\n" % (batch, ref))
print("batch", batch, "threads", len(threads), "coded", len(coded), "state", st["threads_served"], st["cursor"])
