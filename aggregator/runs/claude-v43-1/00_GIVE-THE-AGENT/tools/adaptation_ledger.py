"""Effective adaptation records. Originals remain immutable; returned copies carry provenance."""
import copy, hashlib, json
from pathlib import Path
KINDS = {'specification', 'elaboration', 'correction'}
OBSERVED_ABSENCE = {'observed-absent', 'not-needed'}

def read_jsonl(path):
    p = Path(path)
    return [json.loads(s) for s in p.read_text().splitlines() if s.strip()] if p.exists() else []

def effective_rooms(outdir):
    out = Path(outdir); records = {}
    for name, phase in [('adaptations.jsonl','initial'),('adaptations-recheck.jsonl','recheck')]:
        for row in read_jsonl(out/name):
            sub = row['sub']
            if sub not in records or (phase == 'recheck' and records[sub]['phase'] != phase):
                records[sub] = {'sub':sub,'phase':phase,'status':'accepted','ids':[], 'model_version':row.get('model_version'), 'legacy':True}
            if records[sub]['phase'] == phase:
                records[sub]['ids'].append(row['id'])
    manifest = read_jsonl(out/'adaptation-returns.jsonl')
    for phase in ('initial','recheck'):
        for row in manifest:
            if row.get('phase') == phase and row.get('status') == 'accepted':
                if phase == 'initial' and records.get(row['sub'],{}).get('phase') == 'recheck':
                    continue
                records[row['sub']] = copy.deepcopy(row)
    available={phase:{r['id']:r['sub'] for r in read_jsonl(out/name)} for name,phase in [('adaptations.jsonl','initial'),('adaptations-recheck.jsonl','recheck')]}
    for sub,ret in records.items():
        ids=ret.get('ids')
        if not isinstance(ids,list) or any(not isinstance(x,str) for x in ids) or len(ids)!=len(set(ids)):
            raise ValueError('Invalid return manifest ids for '+sub)
        if set(ids)-set(available[ret['phase']]):raise ValueError('Return manifest names missing ledger records for '+sub)
        if any(available[ret['phase']][ident]!=sub for ident in ids):raise ValueError('Return manifest names another room record for '+sub)
    return records

def effective_lines(outdir, include_particular=False, include_pending=False, include_rejected=False):
    out = Path(outdir); rooms = effective_rooms(out)
    adjudications = {r['adaptation']:r for r in read_jsonl(out/'adjudications.jsonl')}
    allowed = {'accept','modify'}
    if include_particular: allowed.add('particular')
    if include_pending: allowed.add('pending')
    if include_rejected: allowed.add('reject')
    result=[]
    for name,phase in [('adaptations.jsonl','initial'),('adaptations-recheck.jsonl','recheck')]:
        for original in read_jsonl(out/name):
            ret=rooms.get(original['sub'],{})
            if ret.get('phase') != phase or original['id'] not in ret.get('ids',[]): continue
            row=copy.deepcopy(original); adj=adjudications.get(row['id'],{})
            row['decision']=adj.get('decision') or row.get('decision') or 'pending'
            if row['decision'] not in allowed and row.get('op') != 'none': continue
            row['original_kind']=original.get('kind'); row['original_condition']=original.get('condition');row['original_statement']=original.get('statement')
            row['kind']=adj.get('kind') or row.get('kind')
            revised=adj.get('revised')
            if isinstance(revised,dict):
                for key in ('condition','statement','how','kind'):
                    if key in revised and revised[key] is not None: row[key]=revised[key]
            elif isinstance(revised,str) and revised:
                row['condition' if row.get('condition') else 'statement']=revised
            row['source_ledger']=name
            row['current_model_version']=ret.get('model_version') or row.get('model_version')
            row['adjudication']=copy.deepcopy(adj)
            if row.get('op')=='absent': row['observation']=row.get('observation') or 'unobserved'
            result.append(row)
    return result

def shared_lines(outdir):
    return [r for r in effective_lines(outdir) if r.get('decision') in ('accept','modify') and r.get('kind') in KINDS and r.get('element') and (r.get('op')!='absent' or r.get('observation') in OBSERVED_ABSENCE)]

def ledger_provenance(outdir):
    out=Path(outdir)
    names=['adaptations.jsonl','adaptations-recheck.jsonl','adjudications.jsonl','adaptation-returns.jsonl','model/elements.jsonl','model/arrows.jsonl','assignments_final.jsonl','fourth/fourth.jsonl','dimensions.jsonl','recheck-scope.json','_closes/model-D3.sha256']
    return {name:hashlib.sha256((out/name).read_bytes()).hexdigest() if (out/name).exists() else None for name in names}
