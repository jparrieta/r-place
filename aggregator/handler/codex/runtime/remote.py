"""Optional private HTTPS gateway. Never owns or starts research actors."""
import hmac
import http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import re
import secrets
import tempfile
from urllib.parse import urlsplit

from .common import CODEX, DATA, Error, lock, now, read

MAX_REQUEST = 2 * 1024**2
MAX_RESPONSE = 32 * 1024**2


def origin_parts(origin):
    """An exact Tailscale HTTPS origin, with no URL credentials or path."""
    pattern = r'https://(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.){2,}ts\.net(?::8444)?'
    if not isinstance(origin, str) or not re.fullmatch(pattern, origin):
        raise Error('Use https://machine.tailnet.ts.net, optionally with :8444')
    return urlsplit(origin)


def config_path():
    return DATA / 'remote' / 'access.json'


def private_write(path, value):
    """The temporary file is private from creation, including under umask 000."""
    fd, temp = tempfile.mkstemp(prefix='.access-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as handle:
            json.dump(value, handle)
            handle.write('\n')
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def access():
    value = read(config_path())
    if not isinstance(value, dict) or not value:
        raise Error('Remote access is not configured. Start remote-serve first.')
    origin_parts(value.get('origin'))
    if not isinstance(value.get('token'), str) or not re.fullmatch(r'[A-Za-z0-9_-]{64}', value['token']):
        raise Error('Invalid remote access record')
    return value


def configure(origin, port):
    origin_parts(origin)
    if not 1024 <= port <= 65535:
        raise Error('Gateway port must be between 1024 and 65535')
    directory = config_path().parent
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    directory.chmod(0o700)
    with lock(directory / 'access.lock', wait=True):
        previous = read(config_path(), {})
        if not isinstance(previous, dict):
            raise Error('Invalid remote access record; preserve it for inspection')
        # A changed origin invalidates links from the former origin.
        token = previous.get('token') if previous.get('origin') == origin else None
        if not isinstance(token, str) or not re.fullmatch(r'[A-Za-z0-9_-]{64}', token):
            token = secrets.token_urlsafe(48)
        value = {'origin': origin, 'port': port, 'token': token, 'updated_utc': now()}
        private_write(config_path(), value)
    return value


def link():
    value = access()
    return value['origin'] + '/#token=' + value['token']


def revoke():
    with lock(config_path().parent / 'access.lock', wait=True):
        value = access()
        value.update(token=secrets.token_urlsafe(48), updated_utc=now())
        private_write(config_path(), value)
    return 'Remote links revoked. Use remote-link for a new link. Agents are unchanged.'


def controller_endpoint():
    """Read the current credentials, never accept an arbitrary proxy target."""
    value = read(DATA / 'controller.json', {})
    if not isinstance(value, dict):
        raise Error('Invalid local controller record')
    url = value.get('url', '')
    if not isinstance(url, str) or not re.fullmatch(r'http://127\.0\.0\.1:[0-9]{1,5}', url):
        raise Error('Start the local Codex controller first')
    parsed = urlsplit(url)
    if not parsed.port or not isinstance(value.get('token'), str) or not value['token']:
        raise Error('Invalid local controller record')
    return parsed.port, value['token']


def forward(body, gateway_port):
    port, token = controller_endpoint()
    if port == gateway_port:
        raise Error('Gateway and local controller must use different ports')
    connection = http.client.HTTPConnection('127.0.0.1', port, timeout=30)
    try:
        connection.request('POST', '/api', body=body, headers={
            'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token,
            'Origin': f'http://127.0.0.1:{port}'})
        response = connection.getresponse()
        payload = response.read(MAX_RESPONSE + 1)
        if len(payload) > MAX_RESPONSE or response.status not in (200, 400, 401, 403, 404, 409, 500, 503):
            raise Error('Unexpected local controller response')
        value = json.loads(payload)
        if not isinstance(value, dict):
            raise Error('Unexpected local controller response')
        return response.status, value
    finally:
        connection.close()


def make_server(origin, port):
    authority = origin_parts(origin).netloc

    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(15)

        def log_message(self, *_):
            pass  # No request headers, credentials or messages in access logs.

        def reply(self, status, value, kind='application/json'):
            body = value.encode() if isinstance(value, str) else json.dumps(value).encode()
            self.send_response(status)
            for key, val in {
                'Content-Type': kind + '; charset=utf-8', 'Content-Length': str(len(body)),
                'Cache-Control': 'no-store', 'Referrer-Policy': 'no-referrer',
                'X-Content-Type-Options': 'nosniff', 'X-Frame-Options': 'DENY',
                'Content-Security-Policy': "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'",
            }.items():
                self.send_header(key, val)
            self.end_headers()
            self.wfile.write(body)

        def valid_host(self):
            return self.headers.get_all('Host', []) == [authority]

        def do_GET(self):
            if not self.valid_host():
                return self.reply(403, {'error': 'Host rejected'})
            if self.path != '/':
                return self.reply(404, {'error': 'Not found'})
            panel = (CODEX / 'runtime/panel.html').read_text()
            self.reply(200, panel, 'text/html')

        def do_POST(self):
            if self.path != '/api' or not self.valid_host():
                return self.reply(403, {'error': 'Endpoint rejected'})
            if self.headers.get_all('Origin', []) != [origin]:
                return self.reply(403, {'error': 'Origin rejected'})
            try:
                current = access()
            except (Error, OSError, ValueError):
                return self.reply(503, {'error': 'Remote access unavailable'})
            authorization = self.headers.get_all('Authorization', [])
            if current['origin'] != origin or len(authorization) != 1 or not hmac.compare_digest(
                authorization[0].encode(), ('Bearer ' + current['token']).encode()
            ):
                return self.reply(401, {'error': 'Remote link expired or missing. Open a current remote-link.'})
            lengths = self.headers.get_all('Content-Length', [])
            if self.headers.get_all('Transfer-Encoding') or len(lengths) != 1 or not re.fullmatch(r'[0-9]{1,9}', lengths[0]):
                return self.reply(400, {'error': 'A single Content-Length is required'})
            if self.headers.get_all('Content-Type', []) != ['application/json']:
                return self.reply(415, {'error': 'Content-Type must be application/json'})
            size = int(lengths[0])
            if not 0 < size <= MAX_REQUEST:
                return self.reply(413, {'error': 'Request exceeds the controller limit'})
            try:
                body = self.rfile.read(size)
                if len(body) != size or not isinstance(json.loads(body), dict):
                    raise ValueError()
            except (OSError, ValueError):
                return self.reply(400, {'error': 'Expected a complete JSON object'})
            try:
                status, value = forward(body, self.server.server_port)
            except (Error, OSError, ValueError, http.client.HTTPException):
                # A POST may already have taken effect. Never retry it automatically.
                return self.reply(502, {'error': 'Controller response unavailable. Check Operations before repeating a command.'})
            self.reply(status, value)

    return ThreadingHTTPServer(('127.0.0.1', port), Handler)


def serve(origin, port=8768):
    origin_parts(origin)
    if not 1024 <= port <= 65535:
        raise Error('Gateway port must be between 1024 and 65535')
    upstream_port, _ = controller_endpoint()
    if port == upstream_port:
        raise Error('Gateway and local controller must use different ports')
    with lock(DATA / 'remote-gateway.lock'):
        # Bind before storing configuration, so a failed start cannot revoke links.
        with make_server(origin, port) as server:
            configure(origin, port)
            from .native import process_identity
            record = config_path().parent / 'gateway.json'
            private_write(record, {'pid': os.getpid(), 'identity': process_identity(os.getpid()),
                                   'origin': origin, 'port': port})
            print(f'Remote gateway listening on 127.0.0.1:{port}.', flush=True)
            print('Configure private Tailscale Serve, then use remote-link. Ctrl+C stops only this gateway.', flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                if read(record, {}).get('pid') == os.getpid():
                    record.unlink(missing_ok=True)
    return 0
