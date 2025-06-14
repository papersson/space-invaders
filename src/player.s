// player.s - Player cannon implementation for Space Invaders
// Manages player movement, firing, and collision detection

.include "constants.inc"

.section __TEXT,__text
.global _player_init
.global _player_update
.global _player_move_left
.global _player_move_right
.global _player_fire
.global _player_update_bullet
.global _player_hit
.global _player_get_x
.global _player_get_bullet_pos
.global _player_is_bullet_active

.p2align 4

// External functions
.extern _input_is_left_pressed
.extern _input_is_right_pressed
.extern _input_is_fire_pressed

// Player constants
.equ PLAYER_START_X, (SCREEN_WIDTH / 2 - PLAYER_WIDTH / 2)
.equ PLAYER_START_Y, (SCREEN_HEIGHT - 32)
.equ FIRE_COOLDOWN, 30          // Frames between shots
.equ BULLET_START_Y_OFFSET, -8  // Bullet starts above player

// Player data structure
.section __DATA,__data
.p2align 3
player_data:
    .hword PLAYER_START_X       // x_position (16-bit)
    .byte 0                     // fire_cooldown (8-bit)
    .byte LIVES_COUNT           // lives_remaining (8-bit)
    .byte 0                     // bullet_active (8-bit)
    .byte 0                     // padding for alignment
    .hword 0                    // bullet_x (16-bit)
    .hword 0                    // bullet_y (16-bit)
    .hword 0                    // padding for 8-byte alignment

// Initialize player at starting position
// Returns: void
_player_init:
    stp x29, x30, [sp, #-16]!
    mov x29, sp

    // Get player data address
    adrp x0, player_data@PAGE
    add x0, x0, player_data@PAGEOFF

    // Reset position
    mov w1, #PLAYER_START_X
    strh w1, [x0, #0]           // x_position = PLAYER_START_X

    // Reset fire cooldown
    strb wzr, [x0, #2]          // fire_cooldown = 0

    // Reset lives
    mov w1, #LIVES_COUNT
    strb w1, [x0, #3]           // lives_remaining = LIVES_COUNT

    // Reset bullet
    strb wzr, [x0, #4]          // bullet_active = 0
    strh wzr, [x0, #6]          // bullet_x = 0
    strh wzr, [x0, #8]          // bullet_y = 0

    ldp x29, x30, [sp], #16
    ret

// Update player based on input
// Returns: void
_player_update:
    stp x29, x30, [sp, #-32]!
    stp x19, x20, [sp, #16]
    mov x29, sp

    // Get player data address
    adrp x19, player_data@PAGE
    add x19, x19, player_data@PAGEOFF

    // Update fire cooldown
    ldrb w0, [x19, #2]          // Load fire_cooldown
    cbz w0, check_input         // Skip if already 0
    sub w0, w0, #1              // Decrement cooldown
    strb w0, [x19, #2]          // Store updated cooldown

check_input:
    // Check left input
    bl _input_is_left_pressed
    cbz w0, check_right
    bl _player_move_left

check_right:
    // Check right input
    bl _input_is_right_pressed
    cbz w0, check_fire
    bl _player_move_right

check_fire:
    // Check fire input
    bl _input_is_fire_pressed
    cbz w0, update_bullet
    bl _player_fire

update_bullet:
    // Update bullet if active
    ldrb w0, [x19, #4]          // Load bullet_active
    cbz w0, player_update_done  // Skip if not active
    bl _player_update_bullet

player_update_done:
    ldp x19, x20, [sp, #16]
    ldp x29, x30, [sp], #32
    ret

// Move player left with boundary check
// Returns: void
_player_move_left:
    stp x29, x30, [sp, #-16]!
    mov x29, sp

    // Get player data address
    adrp x0, player_data@PAGE
    add x0, x0, player_data@PAGEOFF

    // Load current x position
    ldrh w1, [x0, #0]           // Load x_position

    // Check left boundary
    cmp w1, #(PLAYER_MIN_X + PLAYER_SPEED)
    blt move_left_done          // Don't move if too close to edge

    // Move left
    sub w1, w1, #PLAYER_SPEED
    strh w1, [x0, #0]           // Store new x_position

move_left_done:
    ldp x29, x30, [sp], #16
    ret

// Move player right with boundary check
// Returns: void
_player_move_right:
    stp x29, x30, [sp, #-16]!
    mov x29, sp

    // Get player data address
    adrp x0, player_data@PAGE
    add x0, x0, player_data@PAGEOFF

    // Load current x position
    ldrh w1, [x0, #0]           // Load x_position

    // Check right boundary
    cmp w1, #(PLAYER_MAX_X - PLAYER_SPEED)
    bgt move_right_done         // Don't move if too close to edge

    // Move right
    add w1, w1, #PLAYER_SPEED
    strh w1, [x0, #0]           // Store new x_position

move_right_done:
    ldp x29, x30, [sp], #16
    ret

// Fire bullet if cooldown allows
// Returns: 1 if fired, 0 if not
_player_fire:
    stp x29, x30, [sp, #-16]!
    mov x29, sp

    // Get player data address
    adrp x0, player_data@PAGE
    add x0, x0, player_data@PAGEOFF

    // Check if can fire
    ldrb w1, [x0, #2]           // Load fire_cooldown
    cbnz w1, cant_fire          // Can't fire if cooldown active

    ldrb w1, [x0, #4]           // Load bullet_active
    cbnz w1, cant_fire          // Can't fire if bullet already active

    // Create bullet
    mov w1, #1
    strb w1, [x0, #4]           // bullet_active = 1

    // Set bullet position
    ldrh w1, [x0, #0]           // Load player x_position
    add w1, w1, #(PLAYER_WIDTH / 2)  // Center bullet
    strh w1, [x0, #6]           // bullet_x = player_x + width/2

    mov w1, #(PLAYER_START_Y + BULLET_START_Y_OFFSET)
    strh w1, [x0, #8]           // bullet_y = player_y - offset

    // Set fire cooldown
    mov w1, #FIRE_COOLDOWN
    strb w1, [x0, #2]           // fire_cooldown = FIRE_COOLDOWN

    mov w0, #1                  // Return success
    ldp x29, x30, [sp], #16
    ret

cant_fire:
    mov w0, #0                  // Return failure
    ldp x29, x30, [sp], #16
    ret

// Move bullet upward
// Returns: void
_player_update_bullet:
    stp x29, x30, [sp, #-16]!
    mov x29, sp

    // Get player data address
    adrp x0, player_data@PAGE
    add x0, x0, player_data@PAGEOFF

    // Load bullet y position
    ldrh w1, [x0, #8]           // Load bullet_y

    // Move bullet up
    sub w1, w1, #BULLET_SPEED

    // Check if bullet went off screen
    cmp w1, #0
    bgt bullet_still_active

    // Deactivate bullet
    strb wzr, [x0, #4]          // bullet_active = 0
    b update_bullet_done

bullet_still_active:
    // Update bullet position
    strh w1, [x0, #8]           // Store new bullet_y

update_bullet_done:
    ldp x29, x30, [sp], #16
    ret

// Handle player being hit
// Returns: 1 if game over, 0 if player still has lives
_player_hit:
    stp x29, x30, [sp, #-16]!
    mov x29, sp

    // Get player data address
    adrp x0, player_data@PAGE
    add x0, x0, player_data@PAGEOFF

    // Decrement lives
    ldrb w1, [x0, #3]           // Load lives_remaining
    cbz w1, game_over           // Already 0 lives?
    
    sub w1, w1, #1              // Decrement lives
    strb w1, [x0, #3]           // Store updated lives

    // Reset player position
    mov w2, #PLAYER_START_X
    strh w2, [x0, #0]           // x_position = PLAYER_START_X

    // Clear any active bullet
    strb wzr, [x0, #4]          // bullet_active = 0

    // Reset fire cooldown
    strb wzr, [x0, #2]          // fire_cooldown = 0

    // Check if game over
    cbz w1, game_over

    mov w0, #0                  // Not game over
    ldp x29, x30, [sp], #16
    ret

game_over:
    mov w0, #1                  // Game over
    ldp x29, x30, [sp], #16
    ret

// Get current X position
// Returns: x0 = x position (16-bit value)
_player_get_x:
    adrp x0, player_data@PAGE
    add x0, x0, player_data@PAGEOFF
    ldrh w0, [x0, #0]           // Load x_position
    ret

// Get bullet X,Y position
// Parameters: x0 = pointer to store x, x1 = pointer to store y
// Returns: void
_player_get_bullet_pos:
    stp x29, x30, [sp, #-16]!
    mov x29, sp

    // Save parameter pointers
    mov x2, x0                  // Save x pointer
    mov x3, x1                  // Save y pointer

    // Get player data address
    adrp x0, player_data@PAGE
    add x0, x0, player_data@PAGEOFF

    // Load and store bullet positions
    ldrh w1, [x0, #6]           // Load bullet_x
    strh w1, [x2]               // Store to x pointer

    ldrh w1, [x0, #8]           // Load bullet_y
    strh w1, [x3]               // Store to y pointer

    ldp x29, x30, [sp], #16
    ret

// Check if bullet is active
// Returns: x0 = 1 if active, 0 if not
_player_is_bullet_active:
    adrp x0, player_data@PAGE
    add x0, x0, player_data@PAGEOFF
    ldrb w0, [x0, #4]           // Load bullet_active
    ret