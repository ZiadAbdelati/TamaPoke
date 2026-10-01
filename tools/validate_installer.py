#!/usr/bin/env python3
"""Validate installer offsets, save-region preservation, and complete sprite bundle."""
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parent.parent


def validate():
    manifest = json.loads((ROOT / 'web/manifest.json').read_text())
    parts = manifest['builds'][0]['parts']
    assert manifest['builds'][0]['chipFamily'] == 'ESP32-S3'
    assert [p['offset'] for p in parts] == [0, 0x8000, 0xe000, 0x10000]
    intervals = [(p['offset'], p['offset'] + (ROOT / 'web' / p['path']).stat().st_size)
                 for p in parts]
    partitions = (ROOT / 'web/firmware/partitions.bin').read_bytes()
    save_regions = []
    for pos in range(0, len(partitions) - 31, 32):
        magic, kind, subtype, offset, size, _, _ = struct.unpack_from('<HBBII16sI', partitions, pos)
        if magic == 0x50aa and kind == 1 and subtype == 2:
            save_regions.append((offset, offset + size))
    assert save_regions, 'NVS partition missing'
    for start, end in intervals:
        assert all(end <= low or start >= high for low, high in save_regions), 'firmware overlaps saved pet'
    for name in ('bootloader.bin', 'tamapoke.bin'):
        assert (ROOT / 'web/firmware' / name).read_bytes()[0] == 0xe9, 'invalid ESP image'

    blob = (ROOT / 'web/sprites.pak').read_bytes()
    assert blob[:4] == b'TPAK'
    count, = struct.unpack_from('<H', blob, 4)
    pos, entries = 6, []
    for _ in range(count):
        length = blob[pos]
        pos += 1
        name = blob[pos:pos+length].decode()
        pos += length
        size, = struct.unpack_from('<I', blob, pos)
        pos += 4
        entries.append((name, size))
    expected = {f'mons/p{n:03}.bin' for n in range(1, 152)}
    expected |= {f'mons/ps{n:03}.bin' for n in range(1, 152)}
    expected |= {'mons/thumbs.bin'}
    expected |= {f'mons/c_{s}.bin' for s in ('chiikawa', 'usagi', 'hachiware')}
    assert {name for name, _ in entries} == expected and count == len(expected), 'incomplete roster'
    for name, size in entries:
        assert blob[pos:pos+size] == (ROOT / 'tools/sdcard' / name).read_bytes(), name
        pos += size
    assert pos == len(blob), 'truncated or trailing bundle data'
    print(f'Installer verified: {count} files, all 151 + shiny Pokemon, three companions; NVS untouched')


if __name__ == '__main__':
    validate()
