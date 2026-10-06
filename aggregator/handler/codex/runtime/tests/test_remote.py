"""Real loopback HTTP exchanges against a fake controller. No model calls."""
import contextlib
import http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import os
from pathlib import Path
import stat
import tempfile
import threading
import unittest
from unittest.mock import patch

from runtime import common, remote
from runtime.cli import main


class RemoteTests(unittest.TestCase):
    def setUp(self):
        common.TMP.mkdir(parents=True, exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(prefix='remote-test-', dir=common.TMP)
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.patch = patch.object(remote, 'DATA', self.root)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.origin = 'https://research.tail123.ts.net'
        self.authority = 'research.tail123.ts.net'
        self.calls = []
        self.result = {'result': {'job': 'fake-job'}}
        self.upstream_status = 200
        owner = self

        class Upstream(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def do_POST(self):
                body = self.rfile.read(int(self.headers['Content-Length']))
                owner.calls.append((self.path, dict(self.headers), json.loads(body)))
                payload = json.dumps(owner.result).encode()
                self.send_response(owner.upstream_status)
                self.send_header('Content-Length', str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

        self.upstream = self.start_server(ThreadingHTTPServer(('127.0.0.1', 0), Upstream))
        self.local_token = 'local-controller-test-secret'
        self.endpoint(self.upstream.server_port, self.local_token)
        self.gateway = self.start_server(remote.make_server(self.origin, 0))
        self.config = remote.configure(self.origin, self.gateway.server_port)

    def start_server(self, server):
        thread = threading.Thread(target=lambda: server.serve_forever(poll_interval=0.01), daemon=True)
        thread.start()

        def finish():
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)
        self.addCleanup(finish)
        return server

    def endpoint(self, port, token):
        (self.root / 'controller.json').write_text(json.dumps({
            'url': f'http://127.0.0.1:{port}', 'token': token}))

    def request(self, data=None, headers=None, method='POST', path='/api', raw=None, extra=()):
        body = raw if raw is not None else json.dumps(data or {'action': 'status'}).encode()
        standard = {'Host': self.authority, 'Origin': self.origin,
                    'Authorization': 'Bearer ' + self.config['token'],
                    'Content-Type': 'application/json', 'Content-Length': str(len(body))}
        standard.update(headers or {})
        connection = http.client.HTTPConnection('127.0.0.1', self.gateway.server_port, timeout=3)
        try:
            connection.putrequest(method, path, skip_host=True, skip_accept_encoding=True)
            for key, value in [*standard.items(), *extra]:
                if value is not None:
                    connection.putheader(key, value)
            connection.endheaders(body)
            response = connection.getresponse()
            return response.status, response.read().decode(), dict(response.getheaders())
        finally:
            connection.close()

    def test_remote_actions_reach_same_controller_with_local_credentials(self):
        for action in ('status', 'message', 'events', 'pause', 'stop', 'save', 'restore', 'card'):
            with self.subTest(action=action):
                data = {'action': action, 'actor': 'existing-actor', 'text': 'phone message'}
                status, body, _ = self.request(data)
                self.assertEqual(status, 200)
                self.assertEqual(json.loads(body), self.result)
                path, headers, actual = self.calls[-1]
                self.assertEqual((path, actual), ('/api', data))
                self.assertEqual(headers['Authorization'], 'Bearer ' + self.local_token)
                self.assertEqual(headers['Origin'], f'http://127.0.0.1:{self.upstream.server_port}')
                self.assertNotIn(self.local_token, body)

    def test_host_cannot_be_spoofed_or_duplicated(self):
        for host in ('127.0.0.1', 'evil.example', self.authority + '.evil.example', None):
            self.assertEqual(self.request(headers={'Host': host})[0], 403)
        self.assertEqual(self.request(extra=[('Host', self.authority)])[0], 403)
        self.assertFalse(self.calls)

    def test_origin_must_match_exactly(self):
        for origin in (None, 'null', 'http://' + self.authority, self.origin + '.evil.example'):
            self.assertEqual(self.request(headers={'Origin': origin})[0], 403)
        self.assertEqual(self.request(extra=[('Origin', self.origin)])[0], 403)
        self.assertFalse(self.calls)

    def test_missing_wrong_and_duplicate_tokens_rejected(self):
        for token in (None, 'Bearer wrong', 'Bearer ' + self.local_token):
            self.assertEqual(self.request(headers={'Authorization': token})[0], 401)
        self.assertEqual(self.request(extra=[('Authorization', 'Bearer ' + self.config['token'])])[0], 401)
        self.assertFalse(self.calls)

    def test_revoke_invalidates_old_link_without_controller_call(self):
        old = remote.link()
        remote.revoke()
        self.assertNotEqual(old, remote.link())
        self.assertFalse(self.calls)
        self.assertEqual(self.request()[0], 401)
        self.config = remote.access()
        self.assertEqual(self.request()[0], 200)

    def test_restart_keeps_token_but_new_origin_invalidates_it(self):
        same = remote.configure(self.origin, self.gateway.server_port)
        self.assertEqual(same['token'], self.config['token'])
        different = remote.configure('https://another.tail123.ts.net', self.gateway.server_port)
        self.assertNotEqual(different['token'], same['token'])
        self.assertEqual(self.request()[0], 401)

    def test_controller_token_is_refreshed_on_next_request(self):
        self.request()
        self.endpoint(self.upstream.server_port, 'replacement-test-secret')
        self.assertEqual(self.request()[0], 200)
        self.assertEqual(self.calls[-1][1]['Authorization'], 'Bearer replacement-test-secret')

    def test_only_loopback_controller_target_allowed(self):
        for url in ('http://evil.example:80', 'https://127.0.0.1:8765',
                    'http://127.0.0.1:8765/other', 'http://user@127.0.0.1:8765',
                    'http://127.0.0.1:99999'):
            (self.root / 'controller.json').write_text(json.dumps({'url': url, 'token': self.local_token}))
            status, body, _ = self.request()
            self.assertEqual(status, 502)
            self.assertNotIn(self.local_token, body)
        self.assertFalse(self.calls)

    def test_gateway_cannot_proxy_to_itself(self):
        self.endpoint(self.gateway.server_port, 'loop-test-secret')
        self.assertEqual(self.request()[0], 502)
        self.assertFalse(self.calls)

    def test_no_redirect_following_or_post_retries(self):
        self.upstream_status = 302
        status, body, _ = self.request({'action': 'message'})
        self.assertEqual(status, 502)
        self.assertIn('before repeating', body)
        self.assertEqual(len(self.calls), 1)

    def test_local_errors_propagate_once(self):
        self.upstream_status = 409
        self.result = {'error': 'Actor is busy'}
        status, body, _ = self.request()
        self.assertEqual(status, 409)
        self.assertEqual(json.loads(body), self.result)
        self.assertEqual(len(self.calls), 1)

    def test_panel_contains_mobile_controls_but_no_credentials(self):
        status, body, headers = self.request(method='GET', path='/')
        self.assertEqual(status, 200)
        for fragment in ('max-width:700px', 'name="viewport"', 'id="send"', 'id="pause"', 'id="stop"', 'Resume as interview'):
            self.assertIn(fragment, body)
        self.assertNotIn(self.local_token, body)
        self.assertNotIn(self.config['token'], body)
        self.assertEqual(headers['Cache-Control'], 'no-store')
        self.assertIn("frame-ancestors 'none'", headers['Content-Security-Policy'])
        self.assertNotIn('Access-Control-Allow-Origin', headers)
        self.assertFalse(self.calls)
        self.assertEqual(self.gateway.server_address[0], '127.0.0.1')

    def test_unknown_paths_do_not_read_files_or_forward(self):
        for path in ('/../controller.json', '/api?token=x', '/index.html', '/remote/access.json'):
            self.assertEqual(self.request(method='GET', path=path)[0], 404)
            self.assertEqual(self.request(path=path)[0], 403)
        self.assertFalse(self.calls)

    def test_malformed_json_and_request_framing_rejected(self):
        for raw in (b'{', b'[]', b'null', b'"string"', b'\xff'):
            self.assertEqual(self.request(raw=raw)[0], 400)
        for length in ('-1', 'many', None):
            self.assertEqual(self.request(headers={'Content-Length': length})[0], 400)
        self.assertEqual(self.request(extra=[('Content-Length', '20')])[0], 400)
        self.assertEqual(self.request(headers={'Transfer-Encoding': 'chunked'})[0], 400)
        self.assertEqual(self.request(headers={'Content-Type': 'text/plain'})[0], 415)
        for length in ('0', str(remote.MAX_REQUEST + 1)):
            self.assertEqual(self.request(headers={'Content-Length': length})[0], 413)
        self.assertFalse(self.calls)

    def test_private_permissions_even_with_permissive_umask(self):
        previous = os.umask(0)
        try:
            remote.configure(self.origin, self.gateway.server_port)
            remote.revoke()
        finally:
            os.umask(previous)
        self.assertEqual(stat.S_IMODE(remote.config_path().stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(remote.config_path().parent.stat().st_mode), 0o700)
        self.assertFalse(list(remote.config_path().parent.glob('.access-*')))

    def test_only_private_https_origins_allowed(self):
        for origin in ('http://research.tail123.ts.net', 'https://example.com',
                       self.origin + '/', self.origin + '?x=1', self.origin + '#token=x',
                       self.origin + ':443', self.origin + ':8766',
                       'https://user@research.tail123.ts.net', 'https://research.ts.net'):
            with self.subTest(origin=origin), self.assertRaises(common.Error):
                remote.origin_parts(origin)
        self.assertEqual(remote.origin_parts(self.origin + ':8444').port, 8444)

    def test_documented_https_port_works_with_exact_browser_headers(self):
        self.origin += ':8444'
        self.authority += ':8444'
        self.gateway = self.start_server(remote.make_server(self.origin, 0))
        self.config = remote.configure(self.origin, self.gateway.server_port)
        self.assertEqual(self.request()[0], 200)
        self.assertEqual(self.request(headers={'Host': self.authority.split(':')[0]})[0], 403)

    def test_missing_or_malformed_configuration_fails_closed(self):
        for bad in ([], {'origin': self.origin, 'token': None}, {}):
            remote.config_path().write_text(json.dumps(bad))
            self.assertEqual(self.request()[0], 503)
        self.assertFalse(self.calls)

    def test_failed_bind_keeps_current_remote_links(self):
        before = remote.config_path().read_bytes()
        with self.assertRaises(OSError):
            remote.serve('https://another.tail123.ts.net', port=self.gateway.server_port)
        self.assertEqual(remote.config_path().read_bytes(), before)
        self.assertFalse(self.calls)

    def test_cli_remote_commands_do_not_call_local_api(self):
        with patch('runtime.cli.request', side_effect=AssertionError('No live API call')), \
                patch.object(remote, 'serve', return_value=0) as serve, \
                contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(main(['remote-serve', '--origin', self.origin]), 0)
            serve.assert_called_once_with(origin=self.origin, port=8768)
            self.assertEqual(main(['remote-link']), 0)
            self.assertIn(self.config['token'], output.getvalue())
            self.assertEqual(main(['remote-revoke']), 0)
            self.assertNotIn(remote.access()['token'], output.getvalue())
        self.assertFalse(self.calls)

    def test_gateway_exit_does_not_stop_controller_or_actors(self):
        fake = unittest.mock.MagicMock()
        fake.__enter__.return_value = fake
        fake.serve_forever.side_effect = KeyboardInterrupt()
        with patch.object(remote, 'make_server', return_value=fake), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(remote.serve(self.origin), 0)
        self.assertFalse(self.calls)
        self.assertEqual(remote.controller_endpoint()[0], self.upstream.server_port)

    def test_single_gateway_lock_and_port_guard(self):
        with common.lock(self.root / 'remote-gateway.lock'):
            with self.assertRaises(common.Error):
                remote.serve(self.origin)
        for port in (0, 80, 65536, self.upstream.server_port):
            with self.subTest(port=port), self.assertRaises(common.Error):
                remote.serve(self.origin, port=port)
        self.assertFalse(self.calls)
