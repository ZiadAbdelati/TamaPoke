#!/usr/bin/env python3
"""Build TPK2 actions and browser previews from the committed 4x3 sheets."""
import json
from pathlib import Path
import tempfile
from PIL import Image
from pack_companions import pack

ROOT = Path(__file__).resolve().parent.parent
SLUGS = ('chiikawa', 'usagi', 'hachiware')
SEQUENCES = {
    'Idle': ([0, 1], [1200, 120]),
    'WalkL': ([2, 3], 180), 'WalkR': ([4, 5], 180),
    'Sleep': ([6, 7], 600), 'Eat': ([8, 9], 250),
    'Hurt': ([12, 13], 350), 'Attack': ([14, 15], 180),
    'Pose': ([10, 11], 300), 'Hop': ([22, 23], 180),
    'Nod': ([16, 17], 250), 'DeepBreath': ([18, 19], 650),
    'Sit': ([20, 21], 450),
}


def build_previews():
    """Embed the actual idle pair for the chooser, including boards without SD."""
    lines = ['// Generated from web/*-sheet.png by tools/build_companion_assets.py.',
             '#pragma once', '#include <stdint.h>',
             'struct CompanionPreview { const uint16_t *palette; const uint8_t *pixels; };']
    for slug in SLUGS:
        sheet = Image.open(ROOT / 'web' / f'{slug}-sheet.png').convert('RGBA')
        palette, indices = [], []
        for frame in range(2):
            for r, g, b, a in sheet.crop((frame*64, 0, (frame+1)*64, 72)).getdata():
                if a < 128:
                    indices.append(255)
                    continue
                color = (r >> 3) << 11 | (g >> 2) << 5 | (b >> 3)
                if color not in palette:
                    palette.append(color)
                if len(palette) > 255:
                    raise ValueError('chooser preview exceeds 255 colors')
                indices.append(palette.index(color))
        lines.append(f'static const uint16_t PREVIEW_{slug}_PAL[] = {{' +
                     ','.join(str(c) for c in palette) + '};')
        lines.append(f'static const uint8_t PREVIEW_{slug}_PIX[] = {{')
        lines += [','.join(str(c) for c in indices[i:i+64]) + ','
                  for i in range(0, len(indices), 64)]
        lines.append('};')
    lines.append('static const CompanionPreview COMPANION_PREVIEWS[] = {')
    lines += [f'  {{PREVIEW_{slug}_PAL, PREVIEW_{slug}_PIX}},' for slug in SLUGS]
    lines.append('};')
    (ROOT / 'companion_previews.h').write_text('\n'.join(lines) + '\n')


def build(slug):
    sheet = Image.open(ROOT / 'web' / f'{slug}-sheet.png').convert('RGBA')
    if sheet.size != (256, 216):
        raise ValueError('expected a 4x3 sheet of 64x72 frames')
    frames = [sheet.crop(((i % 4)*64, (i // 4)*72,
                          (i % 4 + 1)*64, (i // 4 + 1)*72)) for i in range(12)]
    gestures = Image.open(ROOT / 'web' / f'{slug}-gestures.png').convert('RGBA')
    if gestures.size != (256, 216):
        raise ValueError('expected 4x3 gesture sheet')
    frames += [gestures.crop(((i % 4)*64, (i // 4)*72,
                              (i % 4 + 1)*64, (i // 4 + 1)*72)) for i in range(12)]
    preview, durations = [], []
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        manifest = {'slug': slug, 'actions': {}}
        for name, (indices, ms) in SEQUENCES.items():
            strip = Image.new('RGBA', (64*len(indices), 72))
            for j, index in enumerate(indices):
                frame = frames[index]
                strip.paste(frame, (j*64, 0))
                canvas = Image.new('RGBA', (128, 144), '#faf3e6')
                canvas.alpha_composite(frame.resize((128, 144), Image.Resampling.NEAREST))
                preview.append(canvas.convert('RGB'))
                durations.append(ms[j] if isinstance(ms, list) else ms)
            strip.save(folder / f'{name}.png')
            manifest['actions'][name] = dict(file=f'{name}.png', width=64, height=72, ms=ms)
        path = folder / 'manifest.json'
        path.write_text(json.dumps(manifest))
        target = pack(path, ROOT / 'tools' / 'sdcard' / 'mons')
    preview[0].save(ROOT / 'web' / f'{slug}-preview.gif', save_all=True,
                    append_images=preview[1:], duration=durations, loop=0)
    print(f'{target}: {target.stat().st_size} bytes, 12 actions')


if __name__ == '__main__':
    build_previews()
    for companion in SLUGS:
        build(companion)
