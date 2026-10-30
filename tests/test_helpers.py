"""Offline workflow checks. Never contacts a TV or installs apps."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import stat
import subprocess
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


backup = load('lampa_backup', 'tv-toolkit/tv-lampa-torrserve/scripts/lampa_backup.py')
server = load('torrserver_config', 'tv-toolkit/tv-lampa-torrserve/scripts/torrserver_config.py')
inventory = load('snapshot', 'tv-toolkit/tv-privacy-optimize/scripts/snapshot.py')


class LampaTests(unittest.TestCase):
    def test_final_config_roundtrip_and_private_files(self):
        config = json.loads((ROOT / 'tv-toolkit/tv-lampa-torrserve/assets/lampa-config.json').read_text())
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'export'
            backup.export(config, destination)
            settings = ET.parse(destination / 'settings.backup').getroot()
            values = {e.attrib['name']: e for e in settings}
            self.assertEqual(values['sync_account'].tag, 'boolean')
            self.assertEqual(values['sync_account'].attrib['value'], 'false')
            storage = ET.parse(destination / 'storage.backup').getroot()
            values = {e.attrib['name']: e for e in storage}
            self.assertEqual(values['internal_torrclient'].tag, 'string')
            self.assertEqual(values['internal_torrclient'].text, 'false')
            self.assertEqual(values['torrserver_preload'].text, 'false')
            self.assertEqual(stat.S_IMODE((destination / 'storage.backup').stat().st_mode), 0o600)
            with self.assertRaises(FileExistsError):
                backup.export(config, destination)

    def test_xml_escaping_and_bad_storage_rejected_before_write(self):
        encoded = backup.encode_preferences({'url': 'https://example.org/?a=1&b=<test>'})
        self.assertEqual(ET.fromstring(encoded)[0].text, 'https://example.org/?a=1&b=<test>')
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'export'
            with self.assertRaises(ValueError):
                backup.export({'settings': {'lang': 'ru'}, 'storage': {'x': False}}, destination)
            self.assertFalse(destination.exists())


class FakeHandler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def respond(self, value, raw=False):
        data = value.encode() if raw else json.dumps(value).encode()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self.server.calls.append(('GET', self.path, None))
        if self.path == '/echo':
            self.respond(self.server.version, raw=True)
        elif self.path == '/waf':
            self.respond(self.server.waf)
        else:
            self.send_error(404)

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.server.calls.append(('POST', self.path, body))
        if self.path == '/settings':
            if body['action'] == 'get':
                self.respond(self.server.settings)
            else:
                if not self.server.ignore_writes:
                    self.server.settings = body['sets']
                self.respond(None)
        elif self.path == '/waf':
            self.server.waf = dict(body, ip_enabled=True)
            self.respond(self.server.waf)
        else:
            self.send_error(404)


class TorrServerTests(unittest.TestCase):
    def setUp(self):
        self.httpd = HTTPServer(('127.0.0.1', 0), FakeHandler)
        self.httpd.version = 'MatriX.147.1'
        self.httpd.settings = dict(server.PROFILE, CacheSize=33554432, custom_preserved='yes')
        self.httpd.waf = {'whitelist': '', 'blacklist': '', 'referers': '', 'ip_enabled': False}
        self.httpd.calls = []
        self.httpd.ignore_writes = False
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.client = server.Client(self.httpd.server_port)
        self.temp = tempfile.TemporaryDirectory()
        self.destination = Path(self.temp.name) / 'private' / 'before.json'
        self.redirect = contextlib.redirect_stdout(io.StringIO())
        self.redirect.__enter__()

    def tearDown(self):
        self.redirect.__exit__(None, None, None)
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=2)
        self.temp.cleanup()

    def mutations(self):
        return [(method, path, body) for method, path, body in self.httpd.calls
                if method == 'POST' and (path == '/waf' or body.get('action') == 'set')]

    def test_default_reads_only(self):
        server.configure(self.client)
        self.assertFalse(self.mutations())
        self.assertFalse(self.destination.exists())

    def test_apply_preserves_unknown_fields_and_records_exact_original(self):
        server.configure(self.client, apply=True, backup=self.destination)
        original = json.loads(self.destination.read_text())
        self.assertEqual(original['settings']['CacheSize'], 33554432)
        self.assertFalse(original['waf']['ip_enabled'])
        self.assertEqual(self.httpd.settings['custom_preserved'], 'yes')
        self.assertEqual(self.httpd.settings['CacheSize'], 67108864)
        self.assertEqual(self.httpd.waf['whitelist'], '127.0.0.1\n::1')
        self.assertEqual(stat.S_IMODE(self.destination.stat().st_mode), 0o600)
        prior_mutations = list(self.mutations())
        with self.assertRaises(FileExistsError):
            server.configure(self.client, apply=True, backup=self.destination)
        self.assertEqual(self.mutations(), prior_mutations)

    def test_version_mismatch_never_mutates(self):
        self.httpd.version = 'unknown'
        with self.assertRaises(ValueError):
            server.configure(self.client, apply=True, backup=self.destination)
        self.assertFalse(self.mutations())
        self.assertFalse(self.destination.exists())

    def test_readback_failure_stops_before_waf_and_keeps_recovery(self):
        self.httpd.ignore_writes = True
        with self.assertRaises(RuntimeError):
            server.configure(self.client, apply=True, backup=self.destination)
        self.assertTrue(self.destination.exists())
        self.assertFalse(any(path == '/waf' for _, path, _ in self.mutations()))

    def test_no_backup_never_mutates(self):
        with self.assertRaises(ValueError):
            server.configure(self.client, apply=True)
        self.assertFalse(self.mutations())


class SnapshotTests(unittest.TestCase):
    def test_unauthorized_target_never_enters_shell(self):
        result = subprocess.CompletedProcess([], 1, '', 'unauthorized')
        with tempfile.TemporaryDirectory() as directory, patch.object(inventory.subprocess, 'run', return_value=result) as run:
            with self.assertRaises(RuntimeError):
                inventory.snapshot('adb', 'fixture-target:5555', directory)
            self.assertEqual(run.call_count, 1)
            self.assertEqual(run.call_args.args[0], ['adb', '-s', 'fixture-target:5555', 'get-state'])
            self.assertFalse((Path(directory) / 'snapshot.json').exists())

    def test_commands_select_target_and_failures_remain_unknown(self):
        calls = []

        def fake_run(command, **kwargs):
            calls.append(command)
            if command[-1] == 'get-state':
                return subprocess.CompletedProcess(command, 0, 'device\n', '')
            if command[-1] == 'dumpsys cpuinfo':
                raise subprocess.TimeoutExpired(command, 25)
            value = '0\n' if command[-1] == 'am get-current-user' else 'fixture\n'
            return subprocess.CompletedProcess(command, 0, value, '')

        with tempfile.TemporaryDirectory() as directory, patch.object(inventory.subprocess, 'run', side_effect=fake_run):
            with contextlib.redirect_stdout(io.StringIO()):
                inventory.snapshot('adb', 'fixture-target:5555', directory)
            result = json.loads((Path(directory) / 'snapshot.json').read_text())
            self.assertTrue(result['read_only'])
            self.assertIn('unknown', result['observations']['cpu']['error'])
            self.assertTrue(all(command[:3] == ['adb', '-s', 'fixture-target:5555'] for command in calls))


if __name__ == '__main__':
    unittest.main()
