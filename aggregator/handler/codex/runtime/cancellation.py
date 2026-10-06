"""Durable stop requests and bounded dispatch admission, with no inference retries."""
import concurrent.futures, threading
from .common import *

_guard=threading.RLock()
_gates={}

class Gate:
    def __init__(self,root):
        self.root=inside(root); self.cancelled=threading.Event(); self.admission=threading.RLock()
    def check(self):
        if self.cancelled.is_set() or (self.root/'CANCELLED.json').exists():
            raise Error('Dispatch stopped; explicit recovery is required')
        inp=read(self.root/'input.json',{})
        if inp.get('run') and (DATA/'runs'/inp['run']/'STOP.json').exists():
            raise Error('Study stopped; explicit recovery is required')
    def call(self,fn,*args,**kwargs):
        # Admission is serialized. A call already admitted is in flight and is
        # interrupted by the controller; no pending call is admitted after stop.
        with self.admission:
            self.check(); return fn(*args,**kwargs)
    def cancel(self,reason):
        self.cancelled.set()
        write(self.root/'CANCELLED.json',{'reason':reason,'utc':now()})


def gate(root):
    root=inside(root)
    with _guard:
        return _gates.setdefault(str(root),Gate(root))


def reset(root):
    """Only explicit recovery calls this after verifying dispatch ownership."""
    root=inside(root)
    with _guard:
        (root/'CANCELLED.json').unlink(missing_ok=True)
        _gates[str(root)]=Gate(root)
    return _gates[str(root)]


def run_stopped(run):
    if (DATA/'runs'/identity(run)/'STOP.json').exists():
        raise Error('Study is stopped. Use recover-plan, recover, or continue-run explicitly.')


def bounded(items,fn,parallel,token):
    """At most parallel outstanding jobs; never prequeue the entire cohort."""
    iterator=iter(items); results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as pool:
        pending=set()
        def admit():
            token.check()
            try: item=next(iterator)
            except StopIteration:return False
            def work():
                token.check(); return fn(item)
            pending.add(pool.submit(work)); return True
        try:
            for _ in range(parallel):
                if not admit():break
            while pending:
                done,pending=concurrent.futures.wait(pending,return_when=concurrent.futures.FIRST_COMPLETED)
                for future in done:
                    results.append(future.result())
                for _ in done:
                    if not admit():break
        finally:
            for future in pending:future.cancel()
    return results
