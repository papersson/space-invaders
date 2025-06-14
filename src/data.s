.section __DATA,__data
.p2align 4

# Sprite dimensions constants
.equ PLAYER_WIDTH, 16
.equ PLAYER_HEIGHT, 8
.equ ALIEN_WIDTH, 11
.equ ALIEN_HEIGHT, 8
.equ UFO_WIDTH, 16
.equ UFO_HEIGHT, 7
.equ SHIELD_WIDTH, 22
.equ SHIELD_HEIGHT, 16
.equ BULLET_WIDTH, 3
.equ BULLET_HEIGHT, 5
.equ EXPLOSION_WIDTH, 13
.equ EXPLOSION_HEIGHT, 8

# Color constants (RGBA format)
.equ COLOR_WHITE, 0xFFFFFFFF
.equ COLOR_GREEN, 0x00FF00FF
.equ COLOR_RED, 0xFF0000FF
.equ COLOR_YELLOW, 0xFFFF00FF
.equ COLOR_CYAN, 0x00FFFFFF
.equ COLOR_MAGENTA, 0xFF00FFFF
.equ COLOR_TRANSPARENT, 0x00000000

# Player cannon sprite (16x8 pixels)
# Shape: ___##___
#        ___##___
#        ___##___
#        _########
#        ##########
#        ##########
#        ##########
#        ####__####
.p2align 4
.globl _player_sprite
_player_sprite:
    # Row 0
    .long 0, 0, 0, COLOR_GREEN, COLOR_GREEN, 0, 0, 0
    .long 0, 0, 0, COLOR_GREEN, COLOR_GREEN, 0, 0, 0
    # Row 1
    .long 0, 0, 0, COLOR_GREEN, COLOR_GREEN, 0, 0, 0
    .long 0, 0, 0, COLOR_GREEN, COLOR_GREEN, 0, 0, 0
    # Row 2
    .long 0, 0, 0, COLOR_GREEN, COLOR_GREEN, 0, 0, 0
    .long 0, 0, 0, COLOR_GREEN, COLOR_GREEN, 0, 0, 0
    # Row 3
    .long 0, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN
    .long COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, 0
    # Row 4
    .long COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN
    .long COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN
    # Row 5
    .long COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN
    .long COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN
    # Row 6
    .long COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN
    .long COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN
    # Row 7
    .long COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, 0, 0, COLOR_GREEN, COLOR_GREEN
    .long COLOR_GREEN, COLOR_GREEN, 0, 0, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN

# Alien Type 1 sprite (11x8 pixels) - Classic invader
# Shape: __#___#__
#        ___###___
#        __#####__
#        ###_#_###
#        #########
#        #_#####_#
#        #_#___#_#
#        ___#_#___
.p2align 4
.globl _alien1_sprite
_alien1_sprite:
    # Row 0
    .long 0, 0, COLOR_WHITE, 0, 0, 0, COLOR_WHITE, 0, 0, 0, 0
    # Row 1
    .long 0, 0, 0, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, 0, 0, 0, 0, 0
    # Row 2
    .long 0, 0, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, 0, 0, 0, 0
    # Row 3
    .long COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, 0, COLOR_WHITE, 0, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, 0, 0
    # Row 4
    .long COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, 0, 0
    # Row 5
    .long COLOR_WHITE, 0, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, 0, COLOR_WHITE, 0, 0
    # Row 6
    .long COLOR_WHITE, 0, COLOR_WHITE, 0, 0, 0, COLOR_WHITE, 0, COLOR_WHITE, 0, 0
    # Row 7
    .long 0, 0, 0, COLOR_WHITE, 0, COLOR_WHITE, 0, 0, 0, 0, 0

# Alien Type 2 sprite (11x8 pixels) - Medium invader
# Shape: _#_____#_
#        _#_###_#_
#        _#######_
#        ###_#_###
#        #########
#        __#___#__
#        _#_#_#_#_
#        #_#___#_#
.p2align 4
.globl _alien2_sprite
_alien2_sprite:
    # Row 0
    .long 0, COLOR_CYAN, 0, 0, 0, 0, 0, COLOR_CYAN, 0, 0, 0
    # Row 1
    .long 0, COLOR_CYAN, 0, COLOR_CYAN, COLOR_CYAN, COLOR_CYAN, 0, COLOR_CYAN, 0, 0, 0
    # Row 2
    .long 0, COLOR_CYAN, COLOR_CYAN, COLOR_CYAN, COLOR_CYAN, COLOR_CYAN, COLOR_CYAN, COLOR_CYAN, 0, 0, 0
    # Row 3
    .long COLOR_CYAN, COLOR_CYAN, COLOR_CYAN, 0, COLOR_CYAN, 0, COLOR_CYAN, COLOR_CYAN, COLOR_CYAN, 0, 0
    # Row 4
    .long COLOR_CYAN, COLOR_CYAN, COLOR_CYAN, COLOR_CYAN, COLOR_CYAN, COLOR_CYAN, COLOR_CYAN, COLOR_CYAN, COLOR_CYAN, 0, 0
    # Row 5
    .long 0, 0, COLOR_CYAN, 0, 0, 0, COLOR_CYAN, 0, 0, 0, 0
    # Row 6
    .long 0, COLOR_CYAN, 0, COLOR_CYAN, 0, COLOR_CYAN, 0, COLOR_CYAN, 0, 0, 0
    # Row 7
    .long COLOR_CYAN, 0, COLOR_CYAN, 0, 0, 0, COLOR_CYAN, 0, COLOR_CYAN, 0, 0

# Alien Type 3 sprite (11x8 pixels) - Small invader
# Shape: ___###___
#        __#####__
#        _#######_
#        ##_###_##
#        #########
#        _#_#_#_#_
#        #___#___#
#        _#_____#_
.p2align 4
.globl _alien3_sprite
_alien3_sprite:
    # Row 0
    .long 0, 0, 0, COLOR_MAGENTA, COLOR_MAGENTA, COLOR_MAGENTA, 0, 0, 0, 0, 0
    # Row 1
    .long 0, 0, COLOR_MAGENTA, COLOR_MAGENTA, COLOR_MAGENTA, COLOR_MAGENTA, COLOR_MAGENTA, 0, 0, 0, 0
    # Row 2
    .long 0, COLOR_MAGENTA, COLOR_MAGENTA, COLOR_MAGENTA, COLOR_MAGENTA, COLOR_MAGENTA, COLOR_MAGENTA, COLOR_MAGENTA, 0, 0, 0
    # Row 3
    .long COLOR_MAGENTA, COLOR_MAGENTA, 0, COLOR_MAGENTA, COLOR_MAGENTA, COLOR_MAGENTA, 0, COLOR_MAGENTA, COLOR_MAGENTA, 0, 0
    # Row 4
    .long COLOR_MAGENTA, COLOR_MAGENTA, COLOR_MAGENTA, COLOR_MAGENTA, COLOR_MAGENTA, COLOR_MAGENTA, COLOR_MAGENTA, COLOR_MAGENTA, COLOR_MAGENTA, 0, 0
    # Row 5
    .long 0, COLOR_MAGENTA, 0, COLOR_MAGENTA, 0, COLOR_MAGENTA, 0, COLOR_MAGENTA, 0, 0, 0
    # Row 6
    .long COLOR_MAGENTA, 0, 0, 0, COLOR_MAGENTA, 0, 0, 0, COLOR_MAGENTA, 0, 0
    # Row 7
    .long 0, COLOR_MAGENTA, 0, 0, 0, 0, 0, COLOR_MAGENTA, 0, 0, 0

# Mystery UFO sprite (16x7 pixels)
# Shape: ____######____
#        __##########__
#        ################
#        ##_##_##_##_##
#        ################
#        __###____###__
#        ___##____##___
.p2align 4
.globl _ufo_sprite
_ufo_sprite:
    # Row 0
    .long 0, 0, 0, 0, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED
    .long COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, 0, 0, 0, 0
    # Row 1
    .long 0, 0, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED
    .long COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, 0, 0
    # Row 2
    .long COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED
    .long COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED
    # Row 3
    .long COLOR_RED, COLOR_RED, 0, COLOR_RED, COLOR_RED, 0, COLOR_RED, COLOR_RED
    .long 0, COLOR_RED, COLOR_RED, 0, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED
    # Row 4
    .long COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED
    .long COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED
    # Row 5
    .long 0, 0, COLOR_RED, COLOR_RED, COLOR_RED, 0, 0, 0
    .long 0, 0, COLOR_RED, COLOR_RED, COLOR_RED, 0, 0, 0
    # Row 6
    .long 0, 0, 0, COLOR_RED, COLOR_RED, 0, 0, 0
    .long 0, 0, COLOR_RED, COLOR_RED, 0, 0, 0, 0

# Shield sprite template (22x16 pixels)
# Shape: solid bunker with damage states
.p2align 4
.globl _shield_sprite
_shield_sprite:
    # Top section (rows 0-3)
    .rept 4
    .long 0, 0, 0, 0, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN
    .long COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN
    .long COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, 0, 0, 0, 0
    .endr
    # Middle section (rows 4-11)
    .rept 8
    .long 0, 0, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN
    .long COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN
    .long COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, 0, 0
    .endr
    # Bottom section with gap (rows 12-15)
    .rept 4
    .long 0, 0, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN
    .long 0, 0, 0, 0, 0, 0
    .long COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN, 0, 0
    .endr

# Player bullet sprite (3x5 pixels)
.p2align 4
.globl _player_bullet_sprite
_player_bullet_sprite:
    # Row 0
    .long 0, COLOR_WHITE, 0
    # Row 1
    .long 0, COLOR_WHITE, 0
    # Row 2
    .long 0, COLOR_WHITE, 0
    # Row 3
    .long 0, COLOR_WHITE, 0
    # Row 4
    .long 0, COLOR_WHITE, 0

# Alien bullet sprite (3x5 pixels) - zigzag pattern
.p2align 4
.globl _alien_bullet_sprite
_alien_bullet_sprite:
    # Row 0
    .long COLOR_YELLOW, 0, 0
    # Row 1
    .long 0, COLOR_YELLOW, 0
    # Row 2
    .long COLOR_YELLOW, 0, 0
    # Row 3
    .long 0, COLOR_YELLOW, 0
    # Row 4
    .long COLOR_YELLOW, 0, 0

# Explosion animation frame 1 (13x8 pixels)
.p2align 4
.globl _explosion_frame1
_explosion_frame1:
    # Row 0
    .long 0, 0, 0, 0, 0, COLOR_WHITE, 0, COLOR_WHITE, 0, 0, 0, 0, 0
    # Row 1
    .long 0, 0, COLOR_WHITE, 0, 0, 0, COLOR_WHITE, 0, 0, 0, COLOR_WHITE, 0, 0
    # Row 2
    .long 0, 0, 0, COLOR_WHITE, 0, 0, 0, 0, 0, COLOR_WHITE, 0, 0, 0
    # Row 3
    .long COLOR_WHITE, 0, 0, 0, 0, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, 0, 0, 0, 0, COLOR_WHITE
    # Row 4
    .long 0, COLOR_WHITE, 0, 0, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, 0, 0, COLOR_WHITE, 0
    # Row 5
    .long 0, 0, COLOR_WHITE, 0, 0, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, 0, 0, COLOR_WHITE, 0, 0
    # Row 6
    .long 0, COLOR_WHITE, 0, 0, 0, 0, COLOR_WHITE, 0, 0, 0, 0, COLOR_WHITE, 0
    # Row 7
    .long COLOR_WHITE, 0, 0, 0, COLOR_WHITE, 0, 0, 0, COLOR_WHITE, 0, 0, 0, COLOR_WHITE

# Explosion animation frame 2 (13x8 pixels)
.p2align 4
.globl _explosion_frame2
_explosion_frame2:
    # Row 0
    .long COLOR_WHITE, 0, 0, COLOR_WHITE, 0, 0, 0, 0, 0, COLOR_WHITE, 0, 0, COLOR_WHITE
    # Row 1
    .long 0, COLOR_WHITE, 0, 0, COLOR_WHITE, 0, 0, 0, COLOR_WHITE, 0, 0, COLOR_WHITE, 0
    # Row 2
    .long 0, 0, COLOR_WHITE, 0, 0, COLOR_WHITE, 0, COLOR_WHITE, 0, 0, COLOR_WHITE, 0, 0
    # Row 3
    .long COLOR_WHITE, 0, 0, COLOR_WHITE, 0, 0, 0, 0, 0, COLOR_WHITE, 0, 0, COLOR_WHITE
    # Row 4
    .long 0, COLOR_WHITE, 0, 0, COLOR_WHITE, 0, 0, 0, COLOR_WHITE, 0, 0, COLOR_WHITE, 0
    # Row 5
    .long 0, 0, COLOR_WHITE, 0, 0, COLOR_WHITE, 0, COLOR_WHITE, 0, 0, COLOR_WHITE, 0, 0
    # Row 6
    .long COLOR_WHITE, 0, 0, COLOR_WHITE, 0, 0, COLOR_WHITE, 0, 0, COLOR_WHITE, 0, 0, COLOR_WHITE
    # Row 7
    .long 0, COLOR_WHITE, 0, 0, COLOR_WHITE, 0, 0, 0, COLOR_WHITE, 0, 0, COLOR_WHITE, 0

# Sprite lookup table
.p2align 4
.globl _sprite_table
_sprite_table:
    .quad _player_sprite
    .quad _alien1_sprite
    .quad _alien2_sprite
    .quad _alien3_sprite
    .quad _ufo_sprite
    .quad _shield_sprite
    .quad _player_bullet_sprite
    .quad _alien_bullet_sprite
    .quad _explosion_frame1
    .quad _explosion_frame2

# Sprite dimension table (width, height pairs)
.p2align 4
.globl _sprite_dimensions
_sprite_dimensions:
    .long PLAYER_WIDTH, PLAYER_HEIGHT
    .long ALIEN_WIDTH, ALIEN_HEIGHT
    .long ALIEN_WIDTH, ALIEN_HEIGHT
    .long ALIEN_WIDTH, ALIEN_HEIGHT
    .long UFO_WIDTH, UFO_HEIGHT
    .long SHIELD_WIDTH, SHIELD_HEIGHT
    .long BULLET_WIDTH, BULLET_HEIGHT
    .long BULLET_WIDTH, BULLET_HEIGHT
    .long EXPLOSION_WIDTH, EXPLOSION_HEIGHT
    .long EXPLOSION_WIDTH, EXPLOSION_HEIGHT

# Sprite IDs for easy reference
.equ SPRITE_PLAYER, 0
.equ SPRITE_ALIEN1, 1
.equ SPRITE_ALIEN2, 2
.equ SPRITE_ALIEN3, 3
.equ SPRITE_UFO, 4
.equ SPRITE_SHIELD, 5
.equ SPRITE_PLAYER_BULLET, 6
.equ SPRITE_ALIEN_BULLET, 7
.equ SPRITE_EXPLOSION1, 8
.equ SPRITE_EXPLOSION2, 9