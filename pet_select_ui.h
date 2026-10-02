#pragma once
#include <stdint.h>

// Use the same rectangles for painting and taps. Margins are symmetric so
// finger-sized taps near an edge work without changing global calibration.
struct PetSelectRect {
  int16_t x, y, w, h;
  constexpr bool contains(int16_t px, int16_t py, int16_t margin = 0) const {
    return px >= x - margin && px < x + w + margin &&
           py >= y - margin && py < y + h + margin;
  }
};
constexpr PetSelectRect petSelectRow(int i) { return {70, (int16_t)(110 + i * 78), 326, 70}; }
constexpr PetSelectRect PET_SELECT_ROSTER = {93, 348, 280, 64};
constexpr int16_t PET_SELECT_ROW_MARGIN = 4;
constexpr int16_t PET_SELECT_ROSTER_MARGIN = 8;
