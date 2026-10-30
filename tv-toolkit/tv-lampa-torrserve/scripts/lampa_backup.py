#!/usr/bin/env python3
"""Generate Lampa's supported backup XML files; never connects to a TV."""
import argparse
import json
import os
from pathlib import Path
import xml.etree.ElementTree as ET


def encode_preferences(values, strings_only=False):
    if not isinstance(values, dict):
        raise ValueError('Preferences must be an object')
    root = ET.Element('map')
    for key, value in values.items():
        if not isinstance(key, str) or not key:
            raise ValueError('Preference names must be nonempty strings')
        if strings_only and not isinstance(value, str):
            raise ValueError('Lampa frontend storage values must remain strings')
        if isinstance(value, bool):
            ET.SubElement(root, 'boolean', name=key, value=str(value).lower())
        elif isinstance(value, str):
            ET.SubElement(root, 'string', name=key).text = value
        else:
            raise ValueError(f'Unsupported preference type for {key}')
    return ET.tostring(root, encoding='utf-8', xml_declaration=True)


def export(config, destination):
    # Validate both before creating anything; do not overwrite a user's existing export.
    payloads = {
        'settings.backup': encode_preferences(config['settings']),
        'storage.backup': encode_preferences(config['storage'], strings_only=True),
    }
    destination = Path(destination)
    if any((destination / name).exists() for name in payloads):
        raise FileExistsError('Choose a fresh export directory; backup files already exist')
    destination.mkdir(parents=True, exist_ok=True, mode=0o700)
    for name, content in payloads.items():
        fd = os.open(destination / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'wb') as handle:
            handle.write(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    export(json.loads(args.config.read_text()), args.out)
    print('Created settings.backup and storage.backup; import through Lampa Backup/Restore.')


if __name__ == '__main__':
    main()
