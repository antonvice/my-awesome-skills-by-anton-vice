#!/usr/bin/env python3
"""Inspect or apply the reference TorrServer profile through a local ADB forward."""
import argparse
import json
import os
from pathlib import Path
from urllib.request import ProxyHandler, Request, build_opener

PROFILE = {
    'CacheSize': 67108864, 'PreloadCache': 12, 'ConnectionsLimit': 20,
    'UseDisk': False, 'EnableRutorSearch': False, 'EnableTorznabSearch': False,
    'EnableDLNA': False, 'EnableBonjour': False, 'EnableLPD': False,
    'DisableUPNP': True, 'DisableUpload': True, 'EnableDebug': False,
    'TorrentDisconnectTimeout': 30,
}
WAF = {'whitelist': '127.0.0.1\n::1', 'blacklist': '', 'referers': ''}


class Client:
    def __init__(self, port):
        if not 1 <= port <= 65535:
            raise ValueError('Invalid local port')
        self.base = f'http://127.0.0.1:{port}'
        # Local setup traffic must not be sent through an environment-configured proxy.
        self.opener = build_opener(ProxyHandler({}))

    def request(self, path, body=None):
        data = None if body is None else json.dumps(body).encode()
        req = Request(self.base + path, data=data, headers={'Content-Type': 'application/json'})
        with self.opener.open(req, timeout=10) as reply:
            data = reply.read().decode()
        if not data:
            return None
        return data if path == '/echo' else json.loads(data)


def configure(client, expected_version='MatriX.147.1', apply=False, backup=None):
    version = client.request('/echo').strip()
    if version != expected_version:
        raise ValueError(f'Expected {expected_version}; got {version}. Review the server API first.')
    before = client.request('/settings', {'action': 'get'})
    before_waf = client.request('/waf')
    if not isinstance(before, dict) or not isinstance(before_waf, dict):
        raise ValueError('Unexpected settings/WAF response')
    missing = PROFILE.keys() - before.keys()
    if missing:
        raise ValueError('Server lacks required settings: ' + ', '.join(sorted(missing)))
    changes = {key: {'before': before[key], 'after': value}
               for key, value in PROFILE.items() if before[key] != value}
    print(json.dumps({'version': version, 'apply': apply, 'settings_diff': changes,
                      'target_waf': WAF}, indent=2))
    if not apply:
        return
    if backup is None:
        raise ValueError('--apply requires --backup in a private directory')
    backup = Path(backup)
    backup.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    # Never replace an original rollback record on a second invocation.
    fd = os.open(backup, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as handle:
        json.dump({'version': version, 'settings': before, 'waf': before_waf}, handle, indent=2)
    merged = dict(before)
    merged.update(PROFILE)
    client.request('/settings', {'action': 'set', 'sets': merged})
    after = client.request('/settings', {'action': 'get'})
    if not isinstance(after, dict) or any(after.get(k) != v for k, v in PROFILE.items()):
        raise RuntimeError('Settings readback failed; original state is in the backup. Stop and inspect.')
    client.request('/waf', WAF)
    waf = client.request('/waf')
    if not isinstance(waf, dict) or not waf.get('ip_enabled') or waf.get('whitelist') != WAF['whitelist']:
        raise RuntimeError('WAF readback failed; restore/review access control before continuing.')
    print('Readback passed. Verify LAN HTTP 403 and restart persistence separately.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=18090)
    parser.add_argument('--expected-version', default='MatriX.147.1')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--backup', type=Path)
    args = parser.parse_args()
    configure(Client(args.port), args.expected_version, args.apply, args.backup)


if __name__ == '__main__':
    main()
