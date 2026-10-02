#!/usr/bin/env bash
# Build browser-installable firmware parts without writing across the NVS save region.
set -euo pipefail
cd "$(dirname "$0")/.."
FQBN="esp32:esp32:esp32s3:CDCOnBoot=cdc,FlashSize=16M,PSRAM=opi,PartitionScheme=app3M_fat9M_16MB"
python3 tools/build_companion_assets.py
arduino-cli compile --warnings=all --fqbn "$FQBN" --build-path build/web .
mkdir -p web/firmware
cp build/web/TamaPoke.ino.bootloader.bin web/firmware/bootloader.bin
cp build/web/TamaPoke.ino.partitions.bin web/firmware/partitions.bin
cp build/web/boot_app0.bin web/firmware/boot_app0.bin
cp build/web/TamaPoke.ino.bin web/firmware/tamapoke.bin
python3 tools/pack_bundle.py
python3 tools/validate_installer.py
