"""Durable phase plans published with leg closure and each delivered workspace."""
from .common import *


def new(stage,leg,round=None):
    if stage=='B2':
        phases=[{'kind':'fleet','stage':stage,'round':r} for r in ([round] if round else ['gold','stab-1','stab-2'])]
    elif stage in ('D1','D3'):
        phases=[{'kind':'labelers','stage':'D3' if stage=='D3' else 'D2','recheck':stage=='D3'},
                {'kind':'fleet','stage':'D3' if stage=='D3' else 'D2'}]
    else:phases=[{'kind':'fleet','stage':stage}]
    return {'leg':leg,'status':'pending','created_utc':now(),'phases':[{**p,'status':'pending','dispatch':None} for p in phases]}


def pending(state):
    return bool(state.get('dispatch_plan') and state['dispatch_plan']['status']!='completed')


def claim(state,kind,stage,dispatch,phase=None,round=None):
    plan=state.get('dispatch_plan')
    if not pending(state):
        if phase is not None:raise Error('Dispatch plan is no longer pending')
        return
    if phase is None:raise Error('A dispatch plan owns this study; use recover-plan')
    leg,index=phase
    if plan['leg']!=leg or not 0<=index<len(plan['phases']):raise Error('Wrong dispatch phase')
    row=plan['phases'][index]
    if any(p['status']!='completed' for p in plan['phases'][:index]) or row['status']!='pending':raise Error('Dispatch phase is not ready')
    if (row['kind'],row['stage'],row.get('round'))!=(kind,stage,round):raise Error('Dispatch phase parameters differ')
    row.update(dispatch=dispatch,status='working');plan['status']='working'


def complete(state,dispatch):
    plan=state.get('dispatch_plan')
    if not plan:return
    for row in plan['phases']:
        if row.get('dispatch')==dispatch:row.update(status='completed',completed_utc=now())
    if all(row['status']=='completed' for row in plan['phases']):plan.update(status='completed',completed_utc=now())


def resume(run,register,explicit=False):
    from . import study,fleet,labelers,cancellation
    base=study.run_dir(run)
    with lock(DATA/'locks'/('plan-'+identity(run)+'.lock')):
        if explicit:(base/'STOP.json').unlink(missing_ok=True)
        cancellation.run_stopped(run)
        state=study.run_state(run);plan=state.get('dispatch_plan')
        if not plan:raise Error('Study has no dispatch plan')
        for index in range(len(plan['phases'])):
            cancellation.run_stopped(run)
            state=study.run_state(run);plan=state['dispatch_plan'];row=plan['phases'][index]
            if row['status']=='completed':continue
            if row.get('dispatch'):
                if not explicit:raise Error('Interrupted phase needs explicit recovery')
                fleet.recover(row['dispatch'],register,reset_stop=True)
            elif row['kind']=='labelers':
                labelers.dispatch(run,register,recheck=row.get('recheck',False),phase=(plan['leg'],index))
            else:
                fleet.dispatch(run,row['stage'],register,round=row.get('round'),phase=(plan['leg'],index))
        return {'run':run,'plan':study.run_state(run)['dispatch_plan']}


def recover(dispatch,register):
    from . import study,fleet
    inp=read(DATA/'dispatches'/identity(dispatch)/'input.json',{})
    if not inp:raise Error('Unknown dispatch')
    run=inp['run'];state=study.run_state(run)
    if any(p.get('dispatch')==dispatch for p in state.get('dispatch_plan',{}).get('phases',[])):
        return resume(run,register,explicit=True)
    return fleet.recover(dispatch,register,reset_stop=True)
