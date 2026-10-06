#!/usr/bin/env python3
"""Render the adaptation distance as a case dendrogram, with an explicit global-model root.
No model calls, no fitted theory. Computed joins need separate substantive adjudication.
    python3 tools/adaptation_tree.py --out out
"""
import argparse, csv, hashlib, html, json, math
from pathlib import Path
import distance
from adaptation_ledger import shared_lines, ledger_provenance

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None

def read_matrix(path):
    with path.open() as f: rows=list(csv.reader(f,delimiter='\t'))
    if not rows: raise ValueError('Missing distance header')
    names=rows[0][1:]
    if len(set(names))!=len(names) or len(rows)!=len(names)+1: raise ValueError('Invalid distance dimensions')
    data=[]
    for name,row in zip(names,rows[1:]):
        if not row or row[0]!=name or len(row)!=len(names)+1: raise ValueError('Mismatched distance labels')
        data.append([float(v) for v in row[1:]])
    for i,row in enumerate(data):
        for j,v in enumerate(row):
            if not math.isfinite(v) or not 0<=v<=1 or abs(v-data[j][i])>1e-8 or (i==j and abs(v)>1e-8):
                raise ValueError('Distance must be finite, symmetric, bounded and zero on its diagonal')
    return names,data

def condition_collisions(lines):
    groups={}
    for r in lines:
        key=(r['op'],r['element'],distance.node_at(r,'3'))
        groups.setdefault(key,[]).append(r)
    return [{'key':list(k),'line_ids':[r['id'] for r in rows], 'texts':sorted({r.get('condition') or r.get('statement') or '' for r in rows})} for k,rows in groups.items() if len({r.get('condition') or r.get('statement') or '' for r in rows})>1]

def generate(out):
    out=Path(out); views=out/'_views'; names,D=read_matrix(views/'distance.tsv'); n=len(names)
    retained=shared_lines(out)
    keys={s:set() for s in names}
    for r in retained:
        if r['sub'] in keys and distance.node_at(r,'3') is not None:
            keys[r['sub']].add(':'.join(str(x) for x in (r['op'],r['element'],distance.node_at(r,'3'))))
    from vlib import local_return_states
    local_states=local_return_states(str(out))
    branches=distance.jl(out/'branches.jsonl'); crosslinks=distance.jl(out/'crosslinks.jsonl')
    nodes={i:{'id':i,'case':s,'members':[s],'shared_keys':sorted(keys[s]),'height':0} for i,s in enumerate(names)}
    # Exact-key Jaccard is a declared sensitivity view. It does not replace the carried metric.
    J=[[0.0]*n for _ in names]
    masked=[]
    for i in range(n):
        for j in range(i):
            a,b=keys[names[i]],keys[names[j]]; union=a|b
            J[i][j]=J[j][i]=1-len(a&b)/len(union) if union else 0
            if D[i][j]==0 and a!=b: masked.append([names[i],names[j]])
    merges=distance.upgma(names,D) if n>1 else []
    strict=distance.upgma(names,J) if n>1 else []
    placements={(r['sub'],r['theme_id']):r.get('third_order') or [] for r in distance.jl(out/'assignments_final.jsonl')}
    code_theme={(r['sub'],r['code_id']):r.get('theme_id') for r in distance.jl(out.parent/'package/store/codes.jsonl')}
    all_keys={s:set(keys[s]) for s in names};multiple=[]
    for r in retained:
        sub=r['sub'];source=r.get('source') or (r.get('lift') or [None])[0]
        if sub not in all_keys or not source:continue
        source=source.split(':')[-1];source=code_theme.get((sub,source),source)
        placed=placements.get((sub,source),[]);placed=[placed] if isinstance(placed,str) else placed
        if len(placed)>1:multiple.append(r['id'])
        for node in placed:
            if node is not None:all_keys[sub].add(':'.join((r['op'],r['element'],node)))
    M=[[0.0]*n for _ in names]
    for i in range(n):
        for j in range(i):
            a,b=all_keys[names[i]],all_keys[names[j]];u=a|b
            M[i][j]=M[j][i]=1-len(a&b)/len(u) if u else 0
    multi=distance.upgma(names,M) if n>1 else []
    for k,(a,b,h,size) in enumerate(merges):
        members=nodes[a]['members']+nodes[b]['members']
        shared=sorted(set(nodes[a]['shared_keys']) & set(nodes[b]['shared_keys']))
        matched=[r['id'] for r in branches if set(r.get('members',[]))==set(members)]
        nodes[n+k]={'id':n+k,'children':[a,b],'height':h,'members':members,'shared_keys':shared,'declared_branches':matched,
                    'status':'declared branch, inspect warrant' if matched else 'computed join, not an adjudicated form'}
    root=n+len(merges)-1 if n else None
    leaves=[]
    def walk(i):
        if 'case' in nodes[i]: leaves.append(i)
        else:
            for c in nodes[i]['children']:walk(c)
    if root is not None: walk(root)
    yp={i:50+24*k for k,i in enumerate(leaves)}
    maxh=max([m[2] for m in merges] or [0]); scale=maxh or 1
    xp={i:850-550*nodes[i]['height']/scale for i in nodes}
    for k,(a,b,h,size) in enumerate(merges):yp[n+k]=(yp[a]+yp[b])/2
    esc=lambda x:html.escape(str(x),quote=True)
    paths=[]; labels=['<text x="10" y="18">Join heights show dissimilarity. The dashed trunk is the global model reference, not a measured ancestor.</text>']
    for i,node in nodes.items():
        if 'children' in node:
            a,b=node['children']; paths.append(f'<path d="M{xp[a]},{yp[a]} H{xp[i]} V{yp[b]} H{xp[b]}"/>')
            title='; '.join(node['declared_branches'] or [node['status']])+f"; {len(node['members'])} cases; dissimilarity {node['height']:.4f}; shared keys: "+', '.join(node['shared_keys'])
            labels.append(f'<circle cx="{xp[i]}" cy="{yp[i]}" r="4"><title>{esc(title)}</title></circle>')
        else:
            sub=node['case']; p=out/'rooms'/sub/'model-D-recheck.md'
            if not p.exists():p=out/'rooms'/sub/'model-D.md'
            state=local_states.get(sub,{})
            status=state.get('local_status','unresolved')
            node['local_status']=status
            node['local_version_status']=state.get('version_status','stale-or-unknown')
            node['local_model_version']=state.get('current_model_version')
            node['branch_memberships']=[r['id'] for r in branches if sub in r.get('members',[])]
            title=f"{sub}: local status {status}; branches {', '.join(node['branch_memberships']) or 'none declared'}; {len(keys[sub])} accepted shared keys. Local particulars remain in the case account."
            labels.append(f'<text x="860" y="{yp[i]+4}"><title>{esc(title)}</title>{esc(sub)}</text>')
    if root is not None:
        paths.append(f'<path class="anchor" d="M170,{yp[root]} H{xp[root]}"/>')
        labels.append(f'<text x="10" y="{yp[root]-10}">Global model</text>')
    height=max(160,24*n+85)
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1250" height="{height}" role="img" aria-label="Adaptation similarity dendrogram"><rect width="100%" height="100%" fill="white"/><style>path{{fill:none;stroke:#596d64;stroke-width:1.3}}.anchor{{stroke-dasharray:5 4}}text{{font:13px sans-serif;fill:#21392f}}circle{{fill:#647cba}}</style>'+''.join(paths+labels)+'</svg>'
    provenance={str(p.relative_to(out)):digest(p) for p in [views/'distance.tsv',out/'adaptations.jsonl',out/'adjudications.jsonl',out/'branches.jsonl',out/'crosslinks.jsonl',out/'prior.md',out/'model/elements.jsonl',out/'model/arrows.jsonl']}
    report={'format':'adaptation-tree-v1','root':'global-model','cluster_root':root,'rooms':names,'nodes':list(nodes.values()),'crosslinks':crosslinks,
            'root_meaning':'Global model is the conceptual reference, not an estimated ancestor or a distance observation.',
            'missing_returns':'Not equivalent to empty adaptation sets; excluded by distance.py and reported in D4 accounting.',
            'local_particulars':'Kept in leaf case accounts; not discarded because they lack portable keys.',
            'sensitivity':{'method':'exact third-tier key Jaccard, average linkage','zero_distance_different_key_pairs':masked,'multiply_placed_lines':multiple,'all_placement_cuts':{str(k):distance.cut(names,multi,k) for k in (2,3,5,8,12) if k<=n},
              'cuts':{str(k):{'carried':distance.cut(names,merges,k),'exact_keys':distance.cut(names,strict,k)} for k in (2,3,5,8,12) if k<=n}},'input_sha256':dict(provenance, **ledger_provenance(out)), 'semantic_limits': ['Exact keys do not align condition meaning or direction.', 'Primary lift omits additional placements; inspect multiply placed sources separately.'], 'incomplete_lift_lines':[r['id'] for r in retained if distance.node_at(r,'3') is None], 'condition_collisions':condition_collisions(retained)}
    (views/'adaptation-tree.json').write_text(json.dumps(report,indent=2)+'\n')
    (views/'adaptation-tree.svg').write_text(svg)
    title='Adaptations from cases to the global model'
    text='Leaves are cases. Join heights measure adaptation dissimilarity, not time, causation or amount of global change. The dashed trunk labels the global model as a reference. Hover over joins and cases. A computed join becomes a form only after its shared mechanism is justified in branches.jsonl. Cross-links and local particulars remain in the record. Empty shared-key profiles do not establish local adequacy.'
    body=f'<!doctype html><meta charset="utf-8"><title>{title}</title><style>body{{font:16px system-ui;margin:30px;color:#21392f}}.tree{{overflow:auto;border:1px solid #ccc;max-height:75vh}}p{{max-width:1000px}}</style><h1>{title}</h1><p>{text}</p><p><a href="adaptation-tree.svg">Export SVG</a> | <a href="adaptation-tree.json">Lineage, cross-links and sensitivity cuts</a></p><div class="tree">{svg}</div><h2>Cross-links</h2><pre>{esc(json.dumps(crosslinks,indent=2))}</pre>'
    (views/'adaptation-tree.html').write_text(body)
    return report

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='out');a=p.parse_args()
    r=generate(a.out);print(json.dumps({'cases':len(r['rooms']),'outputs':'_views/adaptation-tree.{json,svg,html}'}))

if __name__=='__main__':main()
