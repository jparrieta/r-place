import json,sys,re
sys.path.insert(0,'00_GIVE-THE-AGENT/tools'); import mem
st=mem.Store('00_GIVE-THE-AGENT','00_GIVE-THE-AGENT/out')
acc=0; rows=[]
for l in open(sys.argv[1]):
    try: r=json.loads(l)
    except: continue
    n=r.get("native",{})
    if n.get("method")!="item/completed": continue
    it=n["params"]["item"]
    if it["type"] not in ("commandExecution","dynamicToolCall"): continue
    c=it.get("command",""); o=it.get("aggregatedOutput") or ""
    m=re.search(r'room boundary:? (?:\w+ )?([A-Za-z0-9_]+)',c)
    if m and "mem.py log" in c:
        s=m.group(1)
        if s=="room": continue
        try: f,cb,tb=mem.room_bytes(st,s); size=cb+tb
        except Exception: size=0
        rows.append((s,acc,size)); acc=0
    else: acc+=len(o)
tot_s=sum(a for _,a,_ in rows); tot_r=sum(z for *_,z in rows)
for s,a,z in rows: print("%-22s shown %6d room %6d %3d%%"%(s,a,z,100*a//max(1,z)))
print("TOTAL shown",tot_s,"room",tot_r, "%d%%"%(100*tot_s//max(1,tot_r)))
