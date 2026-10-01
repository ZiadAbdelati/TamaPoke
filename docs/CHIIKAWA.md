# Chiikawa companions

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

The fork bundles AI-generated pixel-art sheets for all three characters, with
idle/blinking, left/right walking, sleep, eating, sad/hurt, attack, pose, hop,
nod, deep-breathing and sitting animations. The 4x3 base sheets and 4x3 gesture
sheets are in `web/`. `python3 tools/build_companion_assets.py` converts them
into TPK2 sprites and GIF previews. They are original generated fan artwork,
not official Chiikawa assets. Character rights belong to Nagano.

Use the browser installer's **Load sprites** step to load all 151 Pokemon,
their shinies, gallery thumbnails and the three companions onto the microSD.
The game uses these animations on its main screen, profile and minigame.
Simple code-drawn portraits remain as a fallback without SD animation files,
and for the small companion-selection rows. See COMPANION_ART.md for provenance.

## Browser installer

The Browser installer workflow builds this branch, runs the host tests and
checks that the bundle contains all 306 files. GitHub Pages serves the output.
The manifest flashes bootloader, partitions, boot selector and app separately;
it does not write through the NVS saved-pet region. When updating, leave
**Erase device** unchecked to retain your save. Erasing intentionally resets it.
The stock SD sprites are retained and the three companion files are added.
This page is for the Waveshare ESP32-S3 Touch AMOLED 1.75 with 16 MB flash
and OPI PSRAM. Physical-device verification is still pending.

## How collection works

One active pet is raised at a time. Hatching registers a Pokemon, and evolving
registers each new form. Those records and shiny records stay in the gallery
when the pet leaves. The next Pokemon egg uses the original rarity rules and
prefers evolution lines that you have not finished. Good care and farewell
improve the original egg odds; legendaries unlock after 25 registered species.

You can keep your pet indefinitely. You confirm evolution and farewell;
farewell is offered at final form after three days. Long-press release lets
you move on earlier. Leaving a pet retains its collection record, not a
restorable individual with its nickname and stats. There is no pet storage box.
After an ending, **Choose next pet** lets you choose either roster for the egg.
Companions are selectable directly and have a separate three-character record.
Switching never replaces a live pet and never resets the Pokemon gallery.
All Pokemon species data, evolution and shiny rules, care mechanics, training,
minigames, localized stock text and completion denominator remain in place.
Player care streaks remain shared, as in the prototype. New selector text is English.

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

The upstream installer does not contain the companions. Use this fork's
browser installer, or build this branch yourself. The installer is produced
from source by the Browser installer workflow, rather than a GitHub Release.

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

The ESP32 firmware build passes CI. Physical-device touch/display testing is
still required before treating this as a verified hardware release. New selector strings are English;
existing localized Pokemon UI is retained. Companion combat base stats are
prototype balance values, not canonical franchise statistics.
