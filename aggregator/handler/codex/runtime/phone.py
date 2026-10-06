"""Set up private phone access without owning or starting research actors."""
import http.client
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time

from . import remote
from .common import CODEX, DATA, Error, lock, read
from .native import process_identity

PORT = 8768
HTTPS_PORT = 8444
TARGET = 'http://127.0.0.1:8768'


def executable():
    candidates = [shutil.which('tailscale'), '/Applications/Tailscale.app/Contents/MacOS/Tailscale']
    for candidate in candidates:
        if candidate and os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    raise Error('Install Tailscale on the Mac, open it, approve its network extension and sign in. Then run phone again.')


def command(exe, *args):
    try:
        result = subprocess.run([exe, *args], capture_output=True, text=True, timeout=25)
    except subprocess.TimeoutExpired:
        raise Error('Tailscale timed out. Finish Mac sign-in; for Serve, enable MagicDNS and HTTPS Certificates on the Tailscale admin console DNS page, then run phone again. No research action was sent.') from None
    except OSError:
        raise Error('Tailscale did not respond. Open its Mac app and finish network-extension approval and sign-in. No research action was sent.') from None
    if result.returncode:
        raise Error('Tailscale needs attention. Finish Mac sign-in; for Serve, enable MagicDNS and HTTPS Certificates on the Tailscale admin console DNS page, then run phone again. No service was reset.')
    return result.stdout


def config(exe, *args):
    try:
        value = json.loads(command(exe, *args))
    except ValueError:
        raise Error('Tailscale returned an unreadable status; no configuration was changed.') from None
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise Error('Unexpected Tailscale status; inspect it before continuing.')
    return value


def origin_from(status):
    if status.get('BackendState') != 'Running':
        raise Error('Open Tailscale on the Mac, approve its network extension and sign in to the same account as the phone. Then run phone again.')
    own = status.get('Self')
    if not isinstance(own, dict) or not isinstance(own.get('DNSName'), str):
        raise Error('Tailscale has not supplied this Mac\'s private hostname yet. Finish sign-in first.')
    name = own['DNSName'].rstrip('.')
    origin = 'https://' + name + ':8444'
    remote.origin_parts(origin)
    return origin


def serving(configuration, origin):
    """Only reuse our exact private mount; leave all other ports alone."""
    authority = remote.origin_parts(origin).netloc
    if any(not isinstance(configuration.get(key) or {}, dict) for key in ('TCP', 'Web', 'AllowFunnel')):
        raise Error('Unexpected Tailscale service configuration. Nothing was changed.')
    if configuration.get('Foreground'):
        raise Error('A foreground Tailscale service exists. Inspect it before setting up phone access.')
    funnel = configuration.get('AllowFunnel') or {}
    if any(enabled and name.endswith(':8444') for name, enabled in funnel.items()):
        raise Error('Port 8444 is public through Funnel. Disable that exposure before private phone setup.')
    tcp = (configuration.get('TCP') or {}).get('8444')
    web = configuration.get('Web') or {}
    mounts = {name: value for name, value in web.items() if name.endswith(':8444')}
    expected = {authority: {'Handlers': {'/': {'Proxy': TARGET}}}}
    if tcp is None and not mounts:
        return False
    if tcp != {'HTTPS': True} or mounts != expected:
        raise Error('Port 8444 belongs to a different Tailscale service. Nothing was replaced.')
    return True


def gateway_record():
    record = read(DATA / 'remote/gateway.json', {})
    if not isinstance(record, dict) or not isinstance(record.get('pid'), int) or record['pid'] <= 0 or not record.get('identity'):
        return None
    return record if process_identity(record['pid']) == record['identity'] else None


def check_gateway(origin):
    record = gateway_record()
    if not record or record.get('origin') != origin or record.get('port') != PORT:
        raise Error('The private gateway is not attached to this phone address.')
    access = remote.access()
    if access['origin'] != origin or access['port'] != PORT:
        raise Error('The gateway access record differs; inspect it before reconnecting.')
    conn = http.client.HTTPConnection('127.0.0.1', PORT, timeout=5)
    try:
        conn.request('POST', '/api', json.dumps({'action': 'status'}), headers={
            'Host': remote.origin_parts(origin).netloc, 'Origin': origin,
            'Authorization': 'Bearer ' + access['token'], 'Content-Type': 'application/json'})
        response = conn.getresponse()
        value = json.loads(response.read(remote.MAX_RESPONSE + 1))
        result = value.get('result') if isinstance(value, dict) else None
        if response.status != 200 or not isinstance(result, dict) or not isinstance(result.get('actors'), list):
            raise Error('The gateway cannot read the controller status. No research command was sent.')
    except (OSError, ValueError, http.client.HTTPException):
        raise Error('The private gateway did not answer. Inspect its log before repeating setup.') from None
    finally:
        conn.close()


def ensure_gateway(origin):
    record = gateway_record()
    if record:
        check_gateway(origin)
        return
    previous = read(remote.config_path(), {})
    if previous and (previous.get('origin') != origin or previous.get('port') != PORT):
        raise Error('Existing remote access belongs to another address. Inspect it before replacing credentials.')
    with socket.socket() as probe:
        try:
            probe.bind(('127.0.0.1', PORT))
        except OSError:
            raise Error('Local port 8768 is occupied by an unrecognised process. Nothing was stopped.') from None
    directory = DATA / 'remote'
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    directory.chmod(0o700)
    fd = os.open(directory / 'gateway.log', os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    os.fchmod(fd, 0o600)
    with os.fdopen(fd, 'ab') as log:
        process = subprocess.Popen([sys.executable, '-B', str(CODEX / 'run.py'), 'remote-serve',
                                    '--origin', origin, '--port', str(PORT)],
                                   cwd=CODEX, stdin=subprocess.DEVNULL, stdout=log,
                                   stderr=log, start_new_session=True)
    for _ in range(40):
        if process.poll() is not None:
            raise Error('The gateway stopped during startup. Its private log is preserved.')
        if gateway_record():
            check_gateway(origin)
            return
        time.sleep(0.1)
    raise Error('Gateway startup is not confirmed. Inspect its private log; do not start another copy.')


def setup(check=False):
    exe = executable()
    origin = origin_from(config(exe, 'status', '--json'))
    remote.controller_endpoint()
    with lock(DATA / 'phone-setup.lock'):
        existing = serving(config(exe, 'serve', 'status', '--json'), origin)
        if check:
            check_gateway(origin)
            return {'ready': existing, 'origin': origin, 'physical_phone_tested': False}
        ensure_gateway(origin)
        if not existing:
            command(exe, 'serve', '--bg', '--https=8444', '--yes', TARGET)
        if not serving(config(exe, 'serve', 'status', '--json'), origin):
            raise Error('Tailscale has not confirmed the private HTTPS route. No research action was sent.')
        check_gateway(origin)
        return {'ready': True, 'phone_link': remote.link(), 'physical_phone_tested': False,
                'next': 'Open this private link in the phone browser with Tailscale connected. Keep it out of Git and shared messages.'}
