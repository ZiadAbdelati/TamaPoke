#!/usr/bin/env python3
"""Pack local PNG action strips into TPK2 companion sprites.

python3 tools/pack_companions.py assets/companions/chiikawa/manifest.json
The manifest names a companion slug and actions (see docs/CHIIKAWA.md).
No Pokemon data or downloadable SpriteCollab assets are changed.
"""
import argparse
import json
from pathlib import Path
import struct
from PIL import Image

ACTIONS = dict(Idle=0, WalkL=1, WalkR=2, Sleep=3, Eat=4, Hurt=5,
               Attack=6, Pose=7, Hop=8, Nod=9, DeepBreath=10, Sit=11)
SLUGS = {'chiikawa', 'usagi', 'hachiware'}


def pack(manifest, out_dir):
    manifest = Path(manifest)
    spec = json.loads(manifest.read_text())
    slug = spec['slug']
    if slug not in SLUGS:
        raise ValueError('unknown companion slug')
    actions = spec['actions']
    if 'Idle' not in actions:
        raise ValueError('Idle animation is required')
    palette, colors, packed = [], {}, []
    for name, action in actions.items():
        if name not in ACTIONS:
            raise ValueError(f'unknown action: {name}')
        w, h = action['width'], action['height']
        if not isinstance(w, int) or not isinstance(h, int) or not (1 <= w <= 255 and 1 <= h <= 255):
            raise ValueError('frame dimensions must be integers from 1 to 255')
        im = Image.open(manifest.parent / action['file']).convert('RGBA')
        if im.height != h or im.width % w:
            raise ValueError('each action must be one horizontal strip of whole frames')
        nf = im.width // w
        if not 1 <= nf <= 24:
            raise ValueError('each action needs 1 to 24 frames')
        ms = action.get('ms', 150)
        timings = [ms] * nf if isinstance(ms, int) else ms
        if not isinstance(timings, list):
            raise ValueError('durations must be an integer or a list of integers')
        if len(timings) != nf or any(not isinstance(t, int) or not 1 <= t <= 65535 for t in timings):
            raise ValueError('provide one positive 16-bit duration per frame')
        data = bytearray()
        for frame in range(nf):
            pixels = im.crop((frame*w, 0, (frame+1)*w, h))
            for r, g, b, a in pixels.getdata():
                if a < 128:
                    data.append(255)
                    continue
                color = (r >> 3) << 11 | (g >> 2) << 5 | (b >> 3)
                if color not in colors:
                    if len(palette) >= 255:
                        raise ValueError('use at most 255 RGB565 colors across all actions')
                    colors[color] = len(palette)
                    palette.append(color)
                data.append(colors[color])
        packed.append(struct.pack('<4B', ACTIONS[name], w, h, nf) +
                      struct.pack(f'<{nf}H', *timings) + data)
    blob = (b'TPK2' + struct.pack('<BH', len(packed), len(palette)) +
            struct.pack(f'<{len(palette)}H', *palette) + b''.join(packed))
    if len(blob) > 3 * 1024 * 1024:
        raise ValueError('sprite exceeds the firmware 3 MiB limit')
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f'c_{slug}.bin'
    target.write_bytes(blob)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--out', type=Path, default=Path(__file__).parent / 'sdcard' / 'mons')
    args = parser.parse_args()
    print(pack(args.manifest, args.out))


if __name__ == '__main__':
    main()
