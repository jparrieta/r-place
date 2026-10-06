"""Private phone admission checks. No VPN changes, gateway or model launches."""
import copy
import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

from runtime import common, phone
from runtime.common import Error

ORIGIN = 'https://research.tail123.ts.net:8444'
STATUS = {'BackendState': 'Running', 'Self': {'DNSName': 'research.tail123.ts.net.'}}
SERVE = {'TCP': {'8444': {'HTTPS': True}}, 'Web': {
    'research.tail123.ts.net:8444': {'Handlers': {'/': {'Proxy': phone.TARGET}}}}}


class PhoneTests(unittest.TestCase):
    def setUp(self):
        common.TMP.mkdir(parents=True, exist_ok=True)
        directory = tempfile.TemporaryDirectory(dir=common.TMP)
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.patches = []
        for name, value in [('DATA', self.root), ('executable', Mock(return_value='/fixture/tailscale')),
                            ('ensure_gateway', Mock()), ('check_gateway', Mock())]:
            p = patch.object(phone, name, value); p.start(); self.addCleanup(p.stop)
        p = patch.object(phone.remote, 'controller_endpoint', return_value=(8765, 'local-test-token'))
        p.start(); self.addCleanup(p.stop)
        p = patch.object(phone.remote, 'link', return_value=ORIGIN + '/#token=private-fixture')
        p.start(); self.addCleanup(p.stop)

    def test_origin_requires_running_login_and_valid_private_hostname(self):
        self.assertEqual(phone.origin_from(STATUS), ORIGIN)
        for value in ({'BackendState': 'NeedsLogin'}, {'BackendState': 'Stopped'},
                      {'BackendState': 'Running', 'Self': None},
                      {'BackendState': 'Running', 'Self': {'DNSName': 'outside.example'}}):
            with self.subTest(value=value), self.assertRaises(Error): phone.origin_from(value)

    def test_existing_exact_route_is_reusable_without_changing_other_ports(self):
        config = copy.deepcopy(SERVE)
        config['TCP']['443'] = {'HTTPS': True}
        config['Web']['other.tail123.ts.net:443'] = {'Handlers': {'/': {'Proxy': 'http://127.0.0.1:9000'}}}
        before = copy.deepcopy(config)
        self.assertTrue(phone.serving(config, ORIGIN)); self.assertEqual(config, before)
        self.assertFalse(phone.serving({}, ORIGIN))

    def test_foreign_or_public_port_is_refused(self):
        variants = []
        for field, value in [('TCP', {'8444': {'TCPForward': '127.0.0.1:9000'}}),
                             ('AllowFunnel', {'research.tail123.ts.net:8444': True}),
                             ('Foreground', {'existing': {}}), ('Web', ['unreadable']),
                             ('Web', {'research.tail123.ts.net:8444': {'Handlers': {'/': {'Proxy': 'http://127.0.0.1:9000'}}}})]:
            config = copy.deepcopy(SERVE); config[field] = value; variants.append(config)
        for config in variants:
            with self.subTest(config=config), self.assertRaises(Error): phone.serving(config, ORIGIN)

    def test_setup_does_not_start_anything_until_signed_in(self):
        with patch.object(phone, 'config', return_value={'BackendState': 'NeedsLogin'}), patch.object(phone, 'command') as command:
            with self.assertRaises(Error): phone.setup()
        phone.ensure_gateway.assert_not_called(); command.assert_not_called()

    def test_setup_refuses_foreign_service_before_starting_gateway(self):
        with patch.object(phone, 'config', side_effect=[STATUS, {'TCP': {'8444': {'HTTP': True}}}]), patch.object(phone, 'command') as command:
            with self.assertRaises(Error): phone.setup()
        phone.ensure_gateway.assert_not_called(); command.assert_not_called()

    def test_setup_admits_only_our_port_and_checks_confirmation(self):
        with patch.object(phone, 'config', side_effect=[STATUS, {}, SERVE]), patch.object(phone, 'command') as command:
            result = phone.setup()
        command.assert_called_once_with('/fixture/tailscale', 'serve', '--bg', '--https=8444', '--yes', phone.TARGET)
        phone.ensure_gateway.assert_called_once_with(ORIGIN); phone.check_gateway.assert_called_once_with(ORIGIN)
        self.assertTrue(result['ready']); self.assertFalse(result['physical_phone_tested'])

    def test_repeat_reuses_route_without_serve_mutation(self):
        with patch.object(phone, 'config', side_effect=[STATUS, SERVE, SERVE]), patch.object(phone, 'command') as command:
            self.assertTrue(phone.setup()['ready'])
        command.assert_not_called()

    def test_check_does_not_start_gateway_or_publish_access_token(self):
        with patch.object(phone, 'config', side_effect=[STATUS, SERVE]), patch.object(phone, 'command') as command:
            result = phone.setup(check=True)
        phone.ensure_gateway.assert_not_called(); command.assert_not_called()
        self.assertTrue(result['ready']); self.assertNotIn('token', json.dumps(result))

    def test_unconfirmed_serve_is_not_reported_ready(self):
        with patch.object(phone, 'config', side_effect=[STATUS, {}, {}]), patch.object(phone, 'command'):
            with self.assertRaisesRegex(Error, 'not confirmed'): phone.setup()

    def test_gateway_identity_rejects_missing_or_reused_pid(self):
        with patch.object(phone, 'read', return_value={'pid': 0}), patch.object(phone, 'process_identity', return_value=None):
            self.assertIsNone(phone.gateway_record())
        with patch.object(phone, 'read', return_value={'pid': 123, 'identity': 'old'}), patch.object(phone, 'process_identity', return_value='new'):
            self.assertIsNone(phone.gateway_record())

    def test_failure_does_not_echo_tailscale_account_or_auth_output(self):
        result = subprocess.CompletedProcess([], 1, 'private-account-url', 'private-account-email')
        with patch.object(phone.subprocess, 'run', return_value=result):
            with self.assertRaises(Error) as caught: phone.command('/fixture/tailscale', 'status', '--json')
        self.assertNotIn('private-account', str(caught.exception))
        with patch.object(phone.subprocess, 'run', side_effect=subprocess.TimeoutExpired('tailscale', 25, output='private-account-url')):
            with self.assertRaisesRegex(Error, 'admin console DNS') as caught:
                phone.command('/fixture/tailscale', 'serve')
        self.assertNotIn('private-account', str(caught.exception))

    def test_cli_phone_check_never_calls_actor_api(self):
        from runtime.cli import main
        with patch.object(phone, 'setup', return_value={'ready': False}) as setup, \
             patch('runtime.cli.request') as request, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(['phone', '--check']), 0)
        setup.assert_called_once_with(check=True); request.assert_not_called()

    def test_occupied_gateway_port_is_not_replaced(self):
        # Exercise the real startup function saved before its setup patch.
        with patch.object(phone, 'gateway_record', return_value=None), patch.object(phone, 'read', return_value={}), \
             patch.object(phone.socket, 'socket') as socket, patch.object(phone.subprocess, 'Popen') as launch:
            socket.return_value.__enter__.return_value.bind.side_effect = OSError('busy')
            with self.assertRaisesRegex(Error, 'occupied'): REAL_ENSURE(ORIGIN)
        launch.assert_not_called()


REAL_ENSURE = phone.ensure_gateway
