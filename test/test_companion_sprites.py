#!/usr/bin/env python3
"""Exercise companion packing with synthetic PNGs, not character artwork."""
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from pack_companions import pack


class CompanionPacking(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        # Two 2x2 frames; a transparent pixel must retain its reserved index.
        im = Image.new('RGBA', (4, 2), (255, 0, 0, 255))
        im.putpixel((0, 0), (0, 0, 0, 0))
        im.putpixel((2, 0), (0, 255, 0, 255))
        im.save(self.root / 'idle.png')
        self.spec = {'slug': 'chiikawa', 'actions': {
            'Idle': {'file': 'idle.png', 'width': 2, 'height': 2, 'ms': [100, 200]}}}

    def build(self):
        manifest = self.root / 'manifest.json'
        manifest.write_text(json.dumps(self.spec))
        return pack(manifest, self.root / 'output')

    def test_frame_order_palette_and_transparency(self):
        target = self.build()
        self.assertEqual(target.name, 'c_chiikawa.bin')
        blob = target.read_bytes()
        self.assertEqual(blob[:4], b'TPK2')
        self.assertEqual(struct.unpack_from('<BH', blob, 4), (1, 2))
        self.assertEqual(struct.unpack_from('<2H', blob, 7), (0xF800, 0x07E0))
        self.assertEqual(struct.unpack_from('<4B', blob, 11), (0, 2, 2, 2))
        self.assertEqual(struct.unpack_from('<2H', blob, 15), (100, 200))
        self.assertEqual(blob[19:], bytes([255, 0, 0, 0, 1, 0, 0, 0]))

    def test_all_companion_filenames(self):
        for slug in ('chiikawa', 'usagi', 'hachiware'):
            self.spec['slug'] = slug
            self.assertEqual(self.build().name, f'c_{slug}.bin')

    def test_missing_idle(self):
        self.spec['actions'] = {}
        with self.assertRaisesRegex(ValueError, 'Idle'):
            self.build()

    def test_bad_slug(self):
        self.spec['slug'] = 'pikachu'
        with self.assertRaisesRegex(ValueError, 'slug'):
            self.build()

    def test_invalid_durations(self):
        for ms in (0, 65536, [150], [-1, 150]):
            self.spec['actions']['Idle']['ms'] = ms
            with self.assertRaisesRegex(ValueError, 'duration'):
                self.build()

    def test_invalid_dimensions(self):
        for w in (0, 256, 3, 2.5):
            self.spec['actions']['Idle']['width'] = w
            with self.assertRaises(ValueError):
                self.build()

    def test_too_many_frames(self):
        Image.new('RGBA', (50, 2)).save(self.root / 'idle.png')
        with self.assertRaisesRegex(ValueError, '24'):
            self.build()

    def test_unknown_action(self):
        self.spec['actions']['Dance'] = self.spec['actions']['Idle']
        with self.assertRaisesRegex(ValueError, 'unknown action'):
            self.build()


if __name__ == '__main__':
    unittest.main(verbosity=2)
