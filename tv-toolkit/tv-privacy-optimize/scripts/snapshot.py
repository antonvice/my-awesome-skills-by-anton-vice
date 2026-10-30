#!/usr/bin/env python3
"""Read-only Android TV inventory. Output may be private; this is not full rollback."""
import argparse
import json
import os
from pathlib import Path
import subprocess

COMMANDS = {
    'manufacturer': 'getprop ro.product.manufacturer',
    'model': 'getprop ro.product.model',
    'device': 'getprop ro.product.device',
    'build': 'getprop ro.build.fingerprint',
    'sdk': 'getprop ro.build.version.sdk',
    'abis': 'getprop ro.product.cpu.abilist',
    'current_user': 'am get-current-user',
    'uptime': 'cat /proc/uptime',
    'packages': 'pm list packages -f --user 0',
    'disabled_packages': 'pm list packages -d --user 0',
    'home': 'cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.HOME',
    'accessibility_services': 'settings get secure enabled_accessibility_services',
    'accessibility_enabled': 'settings get secure accessibility_enabled',
    'assistant': 'settings get secure assistant',
    'voice_interaction': 'settings get secure voice_interaction_service',
    'voice_recognition': 'settings get secure voice_recognition_service',
    'window_animation_scale': 'settings get global window_animation_scale',
    'transition_animation_scale': 'settings get global transition_animation_scale',
    'animator_duration_scale': 'settings get global animator_duration_scale',
    'tcl_diagnostics': 'settings get global tcl_diagnostic_status',
    'tcl_uxp': 'settings get global tcl_uxp_status',
    'cpu': 'dumpsys cpuinfo',
    'memory': 'cat /proc/meminfo',
    'storage': 'df -h /data',
    'media_projection': 'dumpsys media_projection',
}


def snapshot(adb, serial, destination):
    state = subprocess.run([adb, '-s', serial, 'get-state'], text=True, capture_output=True, timeout=15)
    if state.returncode or state.stdout.strip() != 'device':
        raise RuntimeError('Selected TV is not authorized/connected; no shell inventory attempted')
    results = {}
    for name, command in COMMANDS.items():
        try:
            result = subprocess.run([adb, '-s', serial, 'shell', command],
                                    text=True, capture_output=True, timeout=25)
            results[name] = {'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
        except subprocess.TimeoutExpired:
            results[name] = {'error': 'timeout; unknown, not zero'}
    # A non-owner active user requires a correctly scoped inventory before changes.
    result = results.get('current_user', {})
    if result.get('stdout', '').strip() != '0' or result.get('returncode') != 0:
        results['user_scope_warning'] = 'Package queries cover user 0 only; inventory the actual profile before changes.'
    destination = Path(destination)
    destination.mkdir(parents=True, mode=0o700, exist_ok=True)
    fd = os.open(destination / 'snapshot.json', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as handle:
        json.dump({'serial': serial, 'read_only': True, 'observations': results}, handle, indent=2)
    print('Private baseline saved; inspect failures and capture exact prior states before each change.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serial', required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--adb', default='adb')
    args = parser.parse_args()
    snapshot(args.adb, args.serial, args.out)


if __name__ == '__main__':
    main()
