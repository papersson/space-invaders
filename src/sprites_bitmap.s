// sprites_bitmap.s - Bitmap format sprites for Space Invaders
// 1 bit per pixel format for render_sprite function

.section __DATA,__data
.p2align 2

// Player sprite (16x8 pixels) - Tank/cannon shape
.global _player_bitmap
_player_bitmap:
    .byte 0b00000001, 0b10000000  // Row 0: _______##_______
    .byte 0b00000011, 0b11000000  // Row 1: ______####______
    .byte 0b00000011, 0b11000000  // Row 2: ______####______
    .byte 0b01111111, 0b11111110  // Row 3: _###############
    .byte 0b11111111, 0b11111111  // Row 4: ################
    .byte 0b11111111, 0b11111111  // Row 5: ################
    .byte 0b11111111, 0b11111111  // Row 6: ################
    .byte 0b11111111, 0b11111111  // Row 7: ################

// Alien 1 sprite (11x8 pixels) - Classic invader
.global _alien1_bitmap
_alien1_bitmap:
    .byte 0b00100000, 0b10000000  // Row 0: __#___#____
    .byte 0b00010001, 0b00000000  // Row 1: ___#_#_____
    .byte 0b00111111, 0b10000000  // Row 2: __#######__
    .byte 0b01101110, 0b11000000  // Row 3: _##_###_##_
    .byte 0b11111111, 0b11100000  // Row 4: ###########
    .byte 0b10111111, 0b10100000  // Row 5: #_#######_#
    .byte 0b10100000, 0b10100000  // Row 6: #_#___#_#__
    .byte 0b00011011, 0b00000000  // Row 7: ___##_##___

// Player bullet sprite (3x5 pixels)
.global _bullet_bitmap
_bullet_bitmap:
    .byte 0b01000000   // Row 0: _#_
    .byte 0b11100000   // Row 1: ###
    .byte 0b11100000   // Row 2: ###
    .byte 0b11100000   // Row 3: ###
    .byte 0b01000000   // Row 4: _#_

// Shield sprite (22x16 pixels) - Protective bunker
.global _shield_bitmap
_shield_bitmap:
    .byte 0b00000111, 0b11111111, 0b11100000  // Row 0
    .byte 0b00001111, 0b11111111, 0b11110000  // Row 1
    .byte 0b00011111, 0b11111111, 0b11111000  // Row 2
    .byte 0b00111111, 0b11111111, 0b11111100  // Row 3
    .byte 0b01111111, 0b11111111, 0b11111110  // Row 4
    .byte 0b11111111, 0b11111111, 0b11111111  // Row 5
    .byte 0b11111111, 0b11111111, 0b11111111  // Row 6
    .byte 0b11111111, 0b11111111, 0b11111111  // Row 7
    .byte 0b11111111, 0b11111111, 0b11111111  // Row 8
    .byte 0b11111111, 0b11111111, 0b11111111  // Row 9
    .byte 0b11111111, 0b11111111, 0b11111111  // Row 10
    .byte 0b11111111, 0b00000011, 0b11111111  // Row 11
    .byte 0b11111110, 0b00000000, 0b11111111  // Row 12
    .byte 0b11111100, 0b00000000, 0b01111111  // Row 13
    .byte 0b11111000, 0b00000000, 0b00111111  // Row 14
    .byte 0b11110000, 0b00000000, 0b00011111  // Row 15