# TamaPoke + Chiikawa browser installer

The Browser installer GitHub Actions workflow builds chiikawa-companions and
publishes the web/ output through GitHub Pages. The build includes firmware,
all 151 Pokemon and their shinies, thumbnails, and three animated companions.

## Install

1. Open the published HTTPS page in desktop Chrome or Edge and connect the
   Waveshare ESP32-S3 Touch AMOLED 1.75 over a data-capable USB cable.
2. Click Install TamaPoke + Chiikawa and choose the board's serial port.
   Leave Erase device unchecked to retain an existing save. Erase resets it.
3. Insert a microSD card. Close the firmware serial session, then click
   Connect board and Load sprites. Wait for completion and restart.
4. Choose the Pokemon or Chiikawa roster on the starter screen. After a pet
   leaves, Choose next pet on the egg lets you change rosters.

Physical-device touch/display and flashing checks have not yet been performed.
Firmware compilation, host tests and bundle validation run before deployment.

## Rebuild

Install ESP32 core 3.3.10 and the libraries listed in ../README.md, plus Pillow.
Run bash tools/build_web.sh from the repository root. The four firmware parts
are installed at 0x0, 0x8000, 0xe000 and 0x10000. Unlike a padded merged image,
they do not write through the NVS save partition. validate_installer.py verifies
that property using the actual generated partition table and part lengths.

The build regenerates three companion TPK2 files from six committed PNG sheets
and combines them with the 303 stock sprite/thumbnail files into sprites.pak.
It verifies all 306 bundled files byte-for-byte against their inputs.
Do not deploy the repository's old prebuilt firmware or sprite bundle directly;
deploy the freshly built output of the workflow.

For local preview: cd web, then python3 -m http.server 8000. Open localhost:8000.
For hosting, enable GitHub Pages with source GitHub Actions; installer.yml
publishes the built artifact. The github-pages environment must allow deployment
from chiikawa-companions.

Pokemon sprites: PMD SpriteCollab (CC BY-NC), original credits unchanged.
Chiikawa companion art: AI-generated fan interpretations; characters by Nagano.
See ../docs/COMPANION_ART.md. Non-commercial fan project.
