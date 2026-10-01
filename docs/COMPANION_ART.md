# Companion animation artwork

Created with the built-in image-generation tool for this fork. Character designs
are Chiikawa, Usagi and Hachiware from Nagano's Chiikawa; these are generated fan
interpretations, not official sprites. This does not change the Pokemon artwork,
its source, attribution or CC BY-NC terms. Non-commercial fan project.

## Prompt set

Each base-sheet prompt requested crisp limited-palette pixel art, warm dark
outlines, a genuinely transparent background, consistent character identity,
no text or gridlines, and exactly four columns by three rows:

1. Idle neutral, idle blink, walk left step 1, walk left step 2.
2. Walk right step 1, walk right step 2, curled sleep, sleep breathing.
3. Eat with small food, eat cheeks puffed, happy arms raised, happy hop.

Character descriptions: Chiikawa is a small white round bear-like character
with round ears and pink cheeks. Usagi is a pale-yellow rabbit with long upright
ears, dark expressive eyes and tiny limbs. Hachiware is a white cat-like character
with pointed ears, blue head fur divided by a white central forehead marking,
dark eyes, pink cheeks and tiny limbs.

For each character, its base sheet was used as the visual reference for a second
4x3 transparent gesture sheet with the same style and identity:

1. Sad/hurt tearful, sad/hurt blink, playful attack preparation, arm thrust.
2. Nod neutral, nod lowered head, relaxed deep breath, expanded deep breath.
3. Awake sitting, sitting blink, grounded happy hop, airborne happy hop.

## Production processing

Frames were isolated from their cells, transparent-edge speckles removed, and
normalized to a shared character scale on 64x72 canvases. Nearest-neighbor
sampling preserves pixel edges. The base and gesture sheets share a limited
palette; alpha is binary for the firmware format. Source frames are committed
as six PNG sheets in web/. The deterministic build script chooses action pairs,
sets timings, packs all twelve TPK2 action slots and generates preview GIFs.
Idle holds for 1200 ms and blinks for 120 ms; walking alternates at 180 ms.

The installer builds these animations and bundles them alongside all stock
Pokemon assets. No downloaded franchise artwork was added for the companions.
Visual appearance and touch behavior still need a physical-board check.
