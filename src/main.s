// main_fixed.s - Fixed main with proper rendering
.section __TEXT,__text
.global _start
.p2align 2

#include "constants.inc"

// External functions
.extern _render_init
.extern _render_frame
.extern _render_cleanup
.extern _clear_screen
.extern _clear_screen_color
.extern _render_sprite
.extern _render_sprite_colored
.extern _get_window_event
.extern _puts
.extern _exit
.extern _usleep

// Sprite data 
.extern _player_bitmap
.extern _alien1_bitmap
.extern _bullet_bitmap

// Simple bullet sprite (3x5 bitmap)
.section __DATA,__data
.p2align 2
bullet_sprite:
    .byte 0b01000000   // Row 0: X
    .byte 0b11100000   // Row 1: XXX
    .byte 0b11100000   // Row 2: XXX
    .byte 0b11100000   // Row 3: XXX
    .byte 0b01000000   // Row 4: X

.p2align 3
game_state:
    .word 112   // player_x
    .word 220   // player_y  
    .word 20    // alien_x
    .word 40    // alien_y
    .word 1     // alien_dir
    .word 0     // bullet_active
    .word 0     // bullet_x
    .word 0     // bullet_y
    .word 1     // running

title_msg: .asciz "Space Invaders ARM64 - Arrow keys to move, Space to shoot, ESC to quit"

.section __TEXT,__text

_start:
    // Set up stack
    sub sp, sp, #32
    stp x29, x30, [sp, #16]
    add x29, sp, #16
    
    // Print title
    adrp x0, title_msg@PAGE
    add x0, x0, title_msg@PAGEOFF
    bl _puts
    
    // Initialize render system
    bl _render_init
    cmp w0, #0
    b.ne exit_game
    
game_loop:
    // Load game state base
    adrp x19, game_state@PAGE
    add x19, x19, game_state@PAGEOFF
    
    // Check if still running
    ldr w0, [x19, #32]
    cbz w0, exit_game
    
    // Handle input
    bl _get_window_event
    cmp w0, #1              // Left arrow
    b.eq move_left
    cmp w0, #2              // Right arrow
    b.eq move_right
    cmp w0, #3              // Space
    b.eq fire_bullet
    cmp w0, #4              // Escape
    b.eq quit_game
    b update_game
    
move_left:
    ldr w0, [x19]           // player_x
    cmp w0, #8
    b.le update_game
    sub w0, w0, #3
    str w0, [x19]
    b update_game
    
move_right:
    ldr w0, [x19]           // player_x
    cmp w0, #200            // SCREEN_WIDTH - 24
    b.ge update_game
    add w0, w0, #3
    str w0, [x19]
    b update_game

fire_bullet:
    // Check if bullet already active
    ldr w0, [x19, #20]      // bullet_active
    cbnz w0, update_game
    
    // Activate bullet at player position
    mov w0, #1
    str w0, [x19, #20]      // bullet_active = 1
    ldr w0, [x19]           // player_x
    add w0, w0, #8          // center of player
    str w0, [x19, #24]      // bullet_x
    ldr w0, [x19, #4]       // player_y
    sub w0, w0, #5
    str w0, [x19, #28]      // bullet_y
    b update_game
    
update_game:
    // Move alien
    ldr w0, [x19, #8]       // alien_x
    ldr w1, [x19, #16]      // alien_dir
    add w0, w0, w1
    str w0, [x19, #8]
    
    // Check alien boundaries
    cmp w0, #8
    b.le reverse_alien
    cmp w0, #205            // SCREEN_WIDTH - 19
    b.lt update_bullet
    
reverse_alien:
    ldr w1, [x19, #16]      // alien_dir
    neg w1, w1
    str w1, [x19, #16]
    ldr w0, [x19, #12]      // alien_y
    add w0, w0, #8
    str w0, [x19, #12]
    
    // Reset if too low
    cmp w0, #180
    b.lt update_bullet
    mov w0, #40
    str w0, [x19, #12]

update_bullet:
    // Update bullet if active
    ldr w0, [x19, #20]      // bullet_active
    cbz w0, render_frame
    
    // Move bullet up
    ldr w0, [x19, #28]      // bullet_y
    sub w0, w0, #4
    str w0, [x19, #28]
    
    // Deactivate if off screen
    cmp w0, #0
    b.gt check_collision
    str wzr, [x19, #20]     // bullet_active = 0
    b render_frame

check_collision:
    // Simple collision check
    ldr w0, [x19, #24]      // bullet_x
    ldr w1, [x19, #8]       // alien_x
    sub w2, w0, w1
    cmp w2, #-3
    b.lt render_frame
    cmp w2, #14             // alien width + bullet width
    b.gt render_frame
    
    ldr w0, [x19, #28]      // bullet_y
    ldr w1, [x19, #12]      // alien_y
    sub w2, w0, w1
    cmp w2, #-3
    b.lt render_frame
    cmp w2, #11             // alien height + bullet height
    b.gt render_frame
    
    // Hit! Reset alien and deactivate bullet
    mov w0, #20
    str w0, [x19, #8]       // alien_x = 20
    mov w0, #40
    str w0, [x19, #12]      // alien_y = 40
    str wzr, [x19, #20]     // bullet_active = 0
    
render_frame:
    // Clear screen to very dark gray (almost black)
    movz w0, #0x10FF        // Lower 16 bits - Blue=16, Alpha=255
    movk w0, #0x1010, lsl #16  // Upper 16 bits - Red=16, Green=16
    bl _clear_screen_color
    
    // Draw player sprite (green)
    adrp x0, _player_bitmap@PAGE
    add x0, x0, _player_bitmap@PAGEOFF
    ldr w1, [x19]           // x
    ldr w2, [x19, #4]       // y
    mov w3, #16             // width
    mov w4, #8              // height
    movz w5, #0x00FF        // Lower 16 bits
    movk w5, #0x00FF, lsl #16  // Upper 16 bits - Green color (RGBA)
    bl _render_sprite_colored
    
    // Draw alien sprite (white)
    adrp x0, _alien1_bitmap@PAGE
    add x0, x0, _alien1_bitmap@PAGEOFF
    ldr w1, [x19, #8]       // x
    ldr w2, [x19, #12]      // y
    mov w3, #11             // width
    mov w4, #8              // height
    mov w5, #-1             // White color (0xFFFFFFFF)
    bl _render_sprite_colored
    
    // Draw bullet if active
    ldr w0, [x19, #20]      // bullet_active
    cbz w0, present
    
    // Draw simple bullet (3x5 white rectangle)
    ldr w1, [x19, #24]      // bullet_x
    ldr w2, [x19, #28]      // bullet_y
    mov w3, #3              // width
    mov w4, #5              // height
    
    // Use bullet sprite (yellow)
    adrp x0, _bullet_bitmap@PAGE
    add x0, x0, _bullet_bitmap@PAGEOFF
    movz w5, #0x00FF        // Lower 16 bits  
    movk w5, #0xFFFF, lsl #16  // Upper 16 bits - Yellow color (RGBA)
    bl _render_sprite_colored
    
present:
    // Present frame
    bl _render_frame
    
    // Sleep for ~16ms (60 FPS)
    mov w0, #16666
    bl _usleep
    
    b game_loop
    
quit_game:
    str wzr, [x19, #32]     // running = 0
    
exit_game:
    // Clean up
    bl _render_cleanup
    
    mov x0, #0
    bl _exit