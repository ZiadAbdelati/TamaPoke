# Chiikawa companion prototype

This fork adds Chiikawa, Usagi, and Hachiware as a separate companion roster.
The Pokemon dex is still exactly 151 entries. Companion IDs 1, 2, and 3 are
not Pokemon numbers; they never enter the Pokemon species table.

## Try it

Build and flash the firmware using the upstream instructions in README.md.
On the first starter screen, tap **Chiikawa companions**, then select a character.
Tap the egg three times to hatch. Existing players can reach the same selector
using **Choose next pet** on an egg, after the current pet's release/farewell.
Selection never replaces a live pet. Both roster pages remain available. After
registering your first Pokemon, the Pokemon page offers a normal mystery egg
rather than a repeat starter selection, preserving rarity and shiny rules.

Companions use the normal food, sleep, bath, affection, minigame, training,
level, bond, nickname, and life-cycle features. Their next egg defaults to the
same companion; choose another roster/character on that egg to change it.
They can say farewell after three days. The normal 151-entry Pokemon gallery
continues to show only Pokemon; companion roster rows display **Met before**.

## Isolation and saves

- Pokemon dex numbers, collection/shiny bitmaps, completion denominator,
  evolution lines, rarity gates and egg candidate pool are unchanged.
- `companionId` is separate from `speciesId`. A live companion uses the unused
  dex value 0; -1 still means an egg. Active-pet display and stat calculations
  use neutral `PetTraits` and `speciesName()` accessors.
- Companion registration and lifetime medal counts have separate NVS keys.
  Companions have the seven generic care medals, excluding the Pokemon final-form
  medal. Pokemon retain their eight medals and original lifetime medal counter.
- Companions do not evolve or receive shinies. Their endings do not overwrite
  the Pokemon farewell/runaway blessing state. Care streaks remain player-wide.
- Older saves default to Pokemon when the companion key is absent. No factory
  reset is required. Returning to upstream firmware while a companion is active
  is unsupported: first choose/hatch a Pokemon in this fork and save it.

## Artwork status

The firmware includes simple code-drawn prototype portraits with idle bobbing,
eating and sleeping expressions, including profile/minigame portraits. They
work without an SD card. These are temporary approximations, not finished pixel
sprite sheets. Custom SD animations take precedence over those portraits.

No new downloaded or official Chiikawa artwork is bundled. Use artwork you have
permission to use and credit its author when adding sprite assets. The upstream
MIT license covers code; it does not grant rights to franchise artwork.

## Add polished animation strips

Install Pillow: `python3 -m pip install pillow`.
For each character, make horizontal PNG strips, one action per strip. A strip
must contain 1–24 equal-size frames, with each frame at most 255x255 pixels.
Transparent pixels use alpha below 128. The combined palette may contain at most
255 distinct RGB565 colors. Typical small pixel-art frames are preferable.

Example `assets/companions/chiikawa/manifest.json` (paths relative to the manifest):

```json
{
  "slug": "chiikawa",
  "actions": {
    "Idle": {"file": "idle.png", "width": 40, "height": 48, "ms": [180, 180]},
    "WalkL": {"file": "walk-left.png", "width": 40, "height": 48, "ms": 140},
    "WalkR": {"file": "walk-right.png", "width": 40, "height": 48, "ms": 140},
    "Sleep": {"file": "sleep.png", "width": 40, "height": 48, "ms": 300},
    "Eat": {"file": "eat.png", "width": 40, "height": 48, "ms": 180}
  }
}
```

`Idle` is required. Missing other actions fall back to idle. Optional actions:
`Hurt`, `Attack`, `Pose`, `Hop`, `Nod`, `DeepBreath`, `Sit`.
Set `slug` to `chiikawa`, `usagi`, or `hachiware`.

```bash
python3 tools/pack_companions.py assets/companions/chiikawa/manifest.json
python3 tools/pack_companions.py assets/companions/usagi/manifest.json
python3 tools/pack_companions.py assets/companions/hachiware/manifest.json
python3 tools/send_sd.py
```

Output paths are `/mons/c_chiikawa.bin`, `/mons/c_usagi.bin`, and
`/mons/c_hachiware.bin`. They use the existing TPK2 action/palette format and
USB uploader. `tools/pack_bundle.py` automatically includes them when rebuilding
the web sprite bundle. Pokemon thumbnail generation remains independent.

The upstream prebuilt web firmware does not contain these changes. Build this
fork's firmware before flashing; do not use the upstream installer expecting
companion support. No new prebuilt firmware release is bundled yet.

## Validation

```bash
./test/run_tests.sh --asan
python3 tools/test_i18n_formats.py
```

Companion regression tests cover all three identities, shared care, restart
persistence, registration isolation, selection boundaries, separate medal totals,
Pokemon egg constraints and switching back to Pokemon. The PNG packer has tests
for frame layout, palette, transparency, filenames and rejected invalid inputs.

Current local check: 107 game-logic tests (normal and ASan/UBSan), 18 existing
tooling tests and 8 companion packer tests pass. LeakSanitizer had to be disabled
locally because this environment prevents its process inspection; ASan/UBSan
remained enabled. The language format check also passes.

A real ESP32 firmware build and physical-device touch/display test are still
required before treating this as a release. New selector strings are English;
existing localized Pokemon UI is retained. Companion combat base stats are
prototype balance values, not canonical franchise statistics.
