#!/usr/bin/env python3
"""Deterministic composition diagnostic. Fractional pseudo-count smoothing is a heuristic.
No ledger, branch, outcome or canvas inputs. Reproduction is the acceptance gate.
"""
import argparse, hashlib, json, math
from pathlib import Path
import numpy as np
import scipy
from scipy.cluster.hierarchy import linkage, cut_tree
from scipy.spatial.distance import pdist, squareform

VERSION='chunk-comparison-v1.1'
def jl(p):
    p=Path(p);return [json.loads(s) for s in p.read_text().splitlines() if s.strip()] if p.exists() else []
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest() if Path(p).exists() else None

def inputs(out,store):
    out,store=Path(out),Path(store)
    paths={'store/'+n:store/n for n in ['rooms.jsonl','themes.jsonl','codes.jsonl']}
    paths.update({n:out/n for n in ['assignments_final.jsonl','fourth/fourth.jsonl','dimensions.jsonl','dropped.jsonl','prior.md']})
    return {k:sha(p) for k,p in paths.items()}

def features(out,store):
    out,store=Path(out),Path(store)
    dropped={r.get('sub') for r in jl(out/'dropped.jsonl')}
    rooms=sorted(r['sub'] for r in jl(store/'rooms.jsonl') if r['sub'] not in dropped)
    themes={(r['sub'],r['theme_id']):r for r in jl(store/'themes.jsonl')}
    codes={}
    seen=set()
    for r in jl(store/'codes.jsonl'):
        identity=(r['sub'],r['code_id'])
        if identity in seen:raise ValueError('Duplicate concept id: '+str(identity))
        seen.add(identity);key=(r['sub'],r.get('theme_id'))
        if key not in themes:raise ValueError('Concept lacks resolvable theme: '+str(identity))
        codes.setdefault(key,[]).append(r['code_id'])
    placed={}
    for r in jl(out/'assignments_final.jsonl'):
        key=(r['sub'],r['theme_id']);v=r.get('third_order') or []
        placed[key]=[v] if isinstance(v,str) else list(dict.fromkeys(v))
    t4={m:r['id'] for r in jl(out/'fourth/fourth.jsonl') for m in r.get('members',[])}
    dims={m:r['id'] for r in jl(out/'dimensions.jsonl') for m in r.get('members',[])}
    columns=sorted(set(t4.values()));ci={c:i for i,c in enumerate(columns)}
    groups=[];meta=[];failures=[]
    thirdcols=sorted(t4);third_index={c:i for i,c in enumerate(thirdcols)};X3=np.zeros((len(rooms),len(thirdcols)))
    for room_index,s in enumerate(rooms):
        items=[];total=0;unplaced=0;splits=0;resid_themes=0;resid_concepts=0
        for key,row in sorted(themes.items()):
            if key[0]!=s:continue
            ids=codes.get(key,[]);n=len(ids);total+=n
            declared=row.get('concept_ids',row.get('code_ids',row.get('codes')))
            if isinstance(declared,list) and declared and all(isinstance(x,str) for x in declared):
                if {x.split(':')[-1] for x in declared} != set(ids):failures.append(list(key))
            paths=placed.get(key,[])
            # v1.1 (QD4-002, J 2026-10-25): third-order residue that no fourth-order theme gathers is counted apart,
            # as the stage says of unplaced concepts; a theme also placed on a gathered node keeps only that node.
            residue=[v for v in paths if v not in t4]
            if residue:
                resid_themes+=1
                if len(residue)==len(paths):resid_concepts+=n
            paths=[v for v in paths if v in t4]
            cats=sorted({t4[v] for v in paths})
            if not cats:unplaced+=n;continue
            for node in paths:
                X3[room_index,third_index[node]]+=n/len(paths)
            if len(cats)>1:splits+=1
            if n:items.append((n,[ci[x] for x in cats]))
        groups.append(items)
        meta.append({'sub':s,'concepts':total,'placed_concepts':sum(x[0] for x in items),'placed_themes':len(items),'unplaced_concepts':unplaced,'residue_themes':resid_themes,'residue_concepts':resid_concepts,'split_themes':splits,'low_information':len(items)<5})
    if failures:raise ValueError('Theme-to-concept identity mismatch: '+str(failures[:5]))
    X=matrix(groups,len(columns));nonzero=X.sum(axis=0)>0
    removed=[c for c,keep in zip(columns,nonzero) if not keep]
    return rooms,columns,X,groups,meta,{'zero_columns':removed,'theme_link_failures':0,'dimension_of':dims,'third_tier':'All recorded placements split equally as fractional weights; descriptive sensitivity only.'},thirdcols,X3

def matrix(groups,p):
    X=np.zeros((len(groups),p))
    for i,items in enumerate(groups):
        for weight,cats in items:
            for j in cats:X[i,j]+=weight/len(cats)
    return X

def clr(X,a,m):
    P=(X+a*m)/(X.sum(axis=1)[:,None]+a)
    z=np.log(P);return z-z.mean(axis=1)[:,None]

def ari(a,b):
    a=np.asarray(a);b=np.asarray(b);n=len(a)
    if n<2:return 1.0
    _,a=np.unique(a,return_inverse=True);_,b=np.unique(b,return_inverse=True)
    tab=np.zeros((a.max()+1,b.max()+1),dtype=int);np.add.at(tab,(a,b),1)
    pairs=lambda x:float(np.sum(x*(x-1)/2))
    total=n*(n-1)/2;x=pairs(tab);ra=pairs(tab.sum(axis=1));cb=pairs(tab.sum(axis=0));exp=ra*cb/total;den=(ra+cb)/2-exp
    return float((x-exp)/den) if den else 1.0

def partitions(z,ks,method='ward',metric='euclidean'):
    if not ks:return {}
    Z=linkage(z,method=method,metric=metric)
    cuts=cut_tree(Z,n_clusters=ks)
    return {k:cuts[:,j] for j,k in enumerate(ks)}

def silhouette(z,labels):
    D=squareform(pdist(z));vals=[]
    for i,g in enumerate(labels):
        same=np.flatnonzero(labels==g)
        if len(same)==1:vals.append(0.0);continue
        a=D[i,same].sum()/(len(same)-1)
        b=min(D[i,np.flatnonzero(labels==h)].mean() for h in set(labels) if h!=g)
        vals.append(float((b-a)/max(a,b)) if max(a,b)>0 else 0.)
    return float(np.mean(vals))

def summary(v):
    return {'mean':float(np.mean(v)),'median':float(np.median(v)), 'mc_se_mean':float(np.std(v,ddof=1)/math.sqrt(len(v))) if len(v)>1 else None,'n':len(v)}

def permutation(groups,rng,p):
    # Shuffle complete allocation patterns among themes, retaining each room's theme weights.
    patterns=[c for row in groups for _,c in row];rng.shuffle(patterns);it=iter(patterns)
    return matrix([[(w,next(it)) for w,_ in row] for row in groups],p)

def analyse(X,groups,params):
    keep=X.sum(axis=1)>0;idx=np.flatnonzero(keep);X=X[keep];groups=[groups[i] for i in idx]
    cols=X.sum(axis=0)>0;X=X[:,cols]
    # Reindex allocation patterns to retained columns.
    remap={old:new for new,old in enumerate(np.flatnonzero(cols))}
    groups=[[(w,[remap[j] for j in c]) for w,c in row] for row in groups]
    n,p=X.shape;a=params['concentration']
    if n<4 or p<2:return {'status':'no-supported-partition','reason':'Fewer than four eligible cases or two nonzero columns','eligible_indices':idx.tolist(),'ks':[],'tables':[],'carried_k':None,'labels':None}
    m=X.sum(axis=0)/X.sum();z=clr(X,a,m);ks=list(range(2,min(12,n//2)+1))
    if np.allclose(z,z[0]):return {'status':'no-supported-partition','reason':'All smoothed profiles identical','eligible_indices':idx.tolist(),'ks':[],'tables':[],'carried_k':None,'labels':None}
    full=partitions(z,ks);tables=[]
    for seed in params['seeds']:
        rng=np.random.default_rng(seed);real={k:[] for k in ks};null={k:[] for k in ks}
        while min(map(len,real.values()),default=params['resamples']) < params['resamples']:
            # Counts implement a bootstrap weighted fit; comparison scores unique sampled cases once.
            sampled=rng.integers(0,n,n);unique,first=np.unique(sampled,return_index=True)
            cuts=partitions(z[sampled],ks)
            for k in ks:
                if len(unique)>k and len(real[k])<params['resamples']:real[k].append(ari(full[k][unique],cuts[k][first]))
        while min(map(len,null.values()),default=params['permutations']) < params['permutations']:
            NX=permutation(groups,rng,p);nz=clr(NX,a,m);nf=partitions(nz,ks)
            sampled=rng.integers(0,n,n);unique,first=np.unique(sampled,return_index=True);nc=partitions(nz[sampled],ks)
            for k in ks:
                if len(unique)>k and len(null[k])<params['permutations']:null[k].append(ari(nf[k][unique],nc[k][first]))
        for k in ks:
            r,q=summary(real[k]),summary(null[k]);tables.append({'seed':seed,'k':k,'real':r,'null':q,'mean_margin':r['mean']-q['mean'],'median_margin':r['median']-q['median'],'silhouette':silhouette(z,full[k]),'null_95':float(np.quantile(null[k],.95))})
    clears=[k for k in ks if all(r['mean_margin']>0 and r['median_margin']>0 for r in tables if r['k']==k)]
    carried=max(clears,key=lambda k:(min(min(r['mean_margin'],r['median_margin']) for r in tables if r['k']==k),-k)) if clears else None
    sens={}
    for k in ks:
        jac=partitions(X>0,[k],method='average',metric='jaccard')[k]
        hell=partitions(np.sqrt(X/X.sum(axis=1)[:,None]),[k],method='average')[k]
        sens[str(k)]={'jaccard_ari':ari(full[k],jac),'hellinger_ari':ari(full[k],hell),'concentration_0.1x_ari':ari(full[k],partitions(clr(X,a/10,m),[k])[k]),'concentration_10x_ari':ari(full[k],partitions(clr(X,a*10,m),[k])[k])}
    return {'status':'supported-diagnostic-cut' if carried else 'no-supported-partition','eligible_indices':idx.tolist(),'ks':ks,'tables':tables,'carried_k':carried,'labels':full[carried].tolist() if carried else None,'sensitivities':sens,'mean_profile':m.tolist(),'own_weight_median':float(np.median(X.sum(axis=1)/(X.sum(axis=1)+a)))}

def compute(out,store,params):
    a=params.get('concentration');seeds=params.get('seeds')
    if not isinstance(a,(float,int)) or not math.isfinite(a) or a<=0:raise ValueError('Concentration must be finite and positive')
    if not isinstance(seeds,list) or len(seeds)!=2 or len(set(seeds))!=2 or not all(isinstance(x,int) for x in seeds):raise ValueError('Exactly two distinct integer seeds required')
    if params.get('resamples',0)<200 or params.get('permutations',0)<100:raise ValueError('At least 200 resamples and 100 null copies required')
    prior=(Path(out)/'prior.md').read_text() if (Path(out)/'prior.md').exists() else ''
    import re
    match=re.search(r'chunk_concentration\s*=\s*([0-9.eE+-]+)',prior)
    declared=float(match.group(1)) if match else 1.0
    if a!=declared:raise ValueError('Concentration differs from prior chunk_concentration (default 1.0)')
    rooms,cols,X,groups,meta,accounting,thirdcols,X3=features(out,store)
    full=analyse(X,groups,params)
    high=[i for i,m in enumerate(meta) if not m['low_information']]
    restricted=analyse(X[high], [groups[i] for i in high],params)
    restricted['source_room_indices']=high
    dims=sorted({accounting['dimension_of'][c] for j,c in enumerate(cols) if X[:,j].sum() and c in accounting['dimension_of']});dimX=np.zeros((len(rooms),len(dims)))
    for j,c in enumerate(cols):
        if c not in accounting['dimension_of']:
            if accounting['dimension_of'] and X[:,j].sum():raise ValueError('Nonzero fourth-tier column lacks dimension: '+c)
        else:dimX[:,dims.index(accounting['dimension_of'][c])]+=X[:,j]
    tier={}
    valid=X.sum(axis=1)>0
    if full['ks'] and len(dims)>1:
        dx=dimX[valid];dz=clr(dx,params['concentration'],dx.sum(axis=0)/dx.sum());fx=X[valid];fx=fx[:,fx.sum(axis=0)>0];fz=clr(fx,params['concentration'],fx.sum(axis=0)/fx.sum())
        for k in full['ks']:tier[str(k)]=ari(partitions(fz,[k])[k],partitions(dz,[k])[k])
    third={"columns":len(thirdcols),"mean_nonzero_per_case":float(np.mean((X3>0).sum(axis=1))) if len(rooms) else 0.,"ari":{},"interpretation":"Sparse tier agreement is descriptive; no form claim or independence inference."}
    if full['ks']:
        tx=X3[valid];tx=tx[:,tx.sum(axis=0)>0]
        if tx.shape[1]>1:
            tz=clr(tx,params['concentration'],tx.sum(axis=0)/tx.sum());fx=X[valid];fx=fx[:,fx.sum(axis=0)>0];fz=clr(fx,params['concentration'],fx.sum(axis=0)/fx.sum())
            for k in full['ks']:third['ari'][str(k)]=ari(partitions(fz,[k])[k],partitions(tz,[k])[k])
    clusters=[]
    if full['labels'] is not None:
        eligible=full['eligible_indices'];lab=full['labels'];used=set()
        for g in sorted(set(lab)):
            inds=[eligible[i] for i,x in enumerate(lab) if x==g];members=[rooms[i] for i in inds]
            h=int(hashlib.sha256('\n'.join(members).encode()).hexdigest(),16)%676
            while h in used:h=(h+1)%676
            used.add(h);code=chr(65+h//26)+chr(65+h%26)
            profile=X[inds].sum(axis=0);profile=profile/profile.sum()
            clusters.append({'code':code,'members':members,'n':len(inds),'n_low_information':sum(meta[i]['low_information'] for i in inds),'profile':{c:float(v) for c,v in zip(cols,profile)},'nearest':None,'merge_height':None,'over':[],'under':[]})
    report={'format':VERSION,'dependencies':{'numpy':np.__version__,'scipy':scipy.__version__},'engine_sha256':sha(__file__),'input_sha256':inputs(out,store),'parameters':params,'heuristic_defaults':{'low_information_themes':5,'maximum_k':12,'maximum_k_fraction':0.5},'interpretation':'Conditional exploratory stability, not independent validation, causal form evidence or a population confidence level. Fractional pseudo-count smoothing is a heuristic, not exact DM maximum likelihood.', 'null':'Theme allocation patterns permuted globally; room concept weights and theme counts retained; theme allocation frequencies retained; concept category totals need not be retained. Frozen mean and concentration throughout.','bootstrap':'Fit weighted duplicate draws; compare unique observed case identities once; retain a draw for k only with more than k distinct cases. Eligible k <= min(12, floor(n/2)).' ,'rooms':rooms,'features_sha256':hashlib.sha256(X.tobytes()).hexdigest(),'columns':cols,'accounting':accounting,'case_information':meta,'all_cases':full,'without_low_information':restricted,'dimension_ari':tier,'dimension_status':'available' if len(dims)>1 else 'unavailable: absent or single dimension','third_tier':third,'clusters':clusters}
    return report

def generate(out,store,concentration=1.0,seeds=(0,1),resamples=200,permutations=100):
    out=Path(out);params={'concentration':concentration,'seeds':list(seeds),'resamples':resamples,'permutations':permutations}
    r=compute(out,store,params)
    (out/'chunk-share-D4.result.json').write_text(json.dumps(r,indent=2,allow_nan=False)+'\n')
    (out/'chunk-share-D4.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in r['clusters']))
    (out/'chunk-share-D4.py').write_text('from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parent.parent / "tools"))\nfrom chunk_compare import main\nmain()\n')
    lines=['# Composition comparison',r['interpretation'],r['null'],'','Status: '+r['all_cases']['status'], 'Seeds: '+str(params['seeds']), 'Concentration: '+str(concentration),'','Numerical silhouette, adjusted Rand stability and null percentile tables are in chunk-share-D4.result.json. No cut is carried if both stability margins do not clear under both seeds.','', 'Excluded without a composition: '+', '.join(m['sub'] for m in r['case_information'] if not m['placed_concepts'])]
    (out/'chunk-share-D4.md').write_text('\n'.join(lines)+'\n')
    return r

def verify_report(out,store):
    out=Path(out);p=out/'chunk-share-D4.result.json'
    if not p.exists():return ['Missing numerical result; a script stub is insufficient']
    r=json.loads(p.read_text())
    if r.get('format')!=VERSION:return ['Unknown result format']
    expected=compute(out,store,r['parameters'])
    errors=[]
    if canonical(r)!=canonical(expected):errors.append('Numerical result or provenance differs from deterministic replay')
    if canonical(jl(out/'chunk-share-D4.jsonl'))!=canonical(expected['clusters']):errors.append('Cluster membership/profile differs from deterministic replay')
    return errors

def main():
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');p.add_argument('--out',default='out');p.add_argument('--store',default='package/store');p.add_argument('--concentration',type=float,default=1.);p.add_argument('--seeds',nargs=2,type=int,default=[0,1]);p.add_argument('--resamples',type=int,default=200);p.add_argument('--permutations',type=int,default=100);a=p.parse_args()
    if a.verify:
        problems=verify_report(a.out,a.store)
        if problems:raise ValueError('; '.join(problems))
        print('Verified deterministic numerical replay');return
    r=generate(a.out,a.store,a.concentration,a.seeds,a.resamples,a.permutations);print(r['all_cases']['status'])
if __name__=='__main__':main()
