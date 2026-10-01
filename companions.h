#pragma once
#include <stdint.h>

// Companion IDs belong to their own roster, never to the Pokemon dex.
enum CompanionId : uint8_t {
  COMPANION_NONE = 0, COMPANION_CHIIKAWA, COMPANION_USAGI,
  COMPANION_HACHIWARE, COMPANION_COUNT = 3
};

struct PetTraits {
  uint16_t accent;
  uint8_t biome, bAtk, bDef, bSpe, evolvesTo, evolveLevel;
};
struct CompanionEntry {
  const char *name;
  const char *spritePath;
  PetTraits traits;
  uint8_t favoriteBerry;
};
static const CompanionEntry COMPANIONS[] = {
  { "?", nullptr, { 0x2946, 0, 50, 50, 50, 0, 0 }, 0 },
  { "Chiikawa", "/mons/c_chiikawa.bin", { 0xFBB7, 0, 45, 60, 45, 0, 0 }, 0 },
  { "Usagi", "/mons/c_usagi.bin", { 0xFEA0, 0, 65, 45, 70, 0, 0 }, 2 },
  { "Hachiware", "/mons/c_hachiware.bin", { 0x6D5F, 0, 50, 50, 60, 0, 0 }, 1 }
};
static inline bool validCompanion(uint8_t id) {
  return id >= COMPANION_CHIIKAWA && id <= COMPANION_COUNT;
}
