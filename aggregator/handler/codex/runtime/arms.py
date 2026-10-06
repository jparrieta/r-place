"""Study-level reader arms. Selection is frozen before any scientific leg."""
import copy
from .common import *

CATALOG = REPO/'aggregator/handler/claude/fleet-arms.json'

def catalog():
    return read(CATALOG)

def resolve(name='codex'):
    profiles=catalog()
    if name not in profiles: raise Error('Unknown fleet arm: '+str(name))
    profile=copy.deepcopy(profiles[name])
    arm=read(REPO/'aggregator/handler/claude/arm.codex.json')
    for stage in profile['stages']:
        if 'readers' not in arm[stage]: raise Error('Arm names a stage without readers: '+stage)
        arm[stage]['readers'].update(profile['reader'])
    for stage,config in arm.items():
        if isinstance(config,dict) and config.get('readers'): validate(config['readers'])
    return arm,{'name':name,'profile':profile,'catalog_sha256':sha(CATALOG)}

def validate(config):
    if config.get('route','codex') not in ('codex','openrouter'): raise Error('Unsupported reader route')
    if not isinstance(config.get('model'),str) or not config['model'].strip(): raise Error('Reader model is required')
    if not isinstance(config.get('n'),int) or not 1<=config['n']<=12: raise Error('Reader replication must be 1..12')
    if config.get('effort') not in ('none','minimal','low','medium','high','xhigh'): raise Error('Invalid reader effort')
    if config.get('route')=='openrouter':
        allowed={'route','model','effort','n','shared','max_tokens','timeout','temperature','offset'}
        if set(config)-allowed: raise Error('Unknown OpenRouter reader settings: '+str(sorted(set(config)-allowed)))
        if not 1<=config.get('max_tokens',16000)<=200000: raise Error('Invalid reader token ceiling')
        if not 1<=config.get('timeout',900)<=1800: raise Error('Invalid reader timeout')

def frozen(run_dir):
    selection=read(run_dir/'fleet-arm.json')
    if selection and sha(run_dir/'arm.json')!=selection['arm_sha256']:
        raise Error('Study arm changed after build. Build a separate study for the other arm.')
    return selection
