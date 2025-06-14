.section __TEXT,__const
.p2align 4

// Alien formation constants
.equ ALIEN_ROWS, 5
.equ ALIEN_COLS, 11
.equ ALIEN_COUNT, 55
.equ ALIEN_WIDTH, 24
.equ ALIEN_HEIGHT, 16
.equ ALIEN_H_SPACING, 32
.equ ALIEN_V_SPACING, 24
.equ ALIEN_MOVE_STEP, 8
.equ ALIEN_DROP_STEP, 16

// Alien structure offsets
.equ ALIEN_X, 0
.equ ALIEN_Y, 2
.equ ALIEN_ALIVE, 4
.equ ALIEN_TYPE, 5
.equ ALIEN_SIZE, 8

// Formation boundaries
.equ FORMATION_LEFT_EDGE, 32
.equ FORMATION_RIGHT_EDGE, 608
.equ FORMATION_BOTTOM, 400

// Movement timing
.equ INITIAL_MOVE_DELAY, 60
.equ MIN_MOVE_DELAY, 2
.equ SPEED_INCREASE_STEP, 10

// Alien types (points value)
.equ ALIEN_TYPE_TOP, 30      // Top row
.equ ALIEN_TYPE_MIDDLE, 20   // Middle 2 rows
.equ ALIEN_TYPE_BOTTOM, 10   // Bottom 2 rows

.section __DATA,__data
.p2align 4

// Alien formation array (55 aliens * 8 bytes each)
aliens_array:
    .space ALIEN_COUNT * ALIEN_SIZE

// Formation state
formation_x:        .hword 100      // Formation left position
formation_y:        .hword 80       // Formation top position
formation_dir:      .byte 1         // Movement direction (1=right, -1=left)
                   .p2align 2
alive_count:        .word ALIEN_COUNT
move_delay:         .word INITIAL_MOVE_DELAY
move_counter:       .word 0
drop_pending:       .byte 0
                   .p2align 2

// Random number for firing
fire_counter:       .word 0

.section __TEXT,__text
.p2align 2

// Initialize alien formation
// No parameters
.global _aliens_init
_aliens_init:
    stp     x29, x30, [sp, #-16]!
    mov     x29, sp
    
    // Reset formation state
    adrp    x0, formation_x@PAGE
    add     x0, x0, formation_x@PAGEOFF
    mov     w1, #100
    strh    w1, [x0]
    
    adrp    x0, formation_y@PAGE
    
    add     x0, x0, formation_y@PAGEOFF
    mov     w1, #80
    strh    w1, [x0]
    
    adrp    x0, formation_dir@PAGE
    
    add     x0, x0, formation_dir@PAGEOFF
    mov     w1, #1
    strb    w1, [x0]
    
    adrp    x0, alive_count@PAGE
    
    add     x0, x0, alive_count@PAGEOFF
    mov     w1, #ALIEN_COUNT
    str     w1, [x0]
    
    adrp    x0, move_delay@PAGE
    
    add     x0, x0, move_delay@PAGEOFF
    mov     w1, #INITIAL_MOVE_DELAY
    str     w1, [x0]
    
    adrp    x0, move_counter@PAGE
    
    add     x0, x0, move_counter@PAGEOFF
    str     wzr, [x0]
    
    adrp    x0, drop_pending@PAGE
    
    add     x0, x0, drop_pending@PAGEOFF
    strb    wzr, [x0]
    
    // Initialize each alien
    adrp    x0, aliens_array@PAGE
    add     x0, x0, aliens_array@PAGEOFF
    mov     w1, #0              // Row counter
    
1:  // Row loop
    mov     w2, #0              // Column counter
    
2:  // Column loop
    // Calculate X position
    mov     w3, w2
    mov     w4, #ALIEN_H_SPACING
    mul     w3, w3, w4
    add     w3, w3, #FORMATION_LEFT_EDGE
    strh    w3, [x0, #ALIEN_X]
    
    // Calculate Y position
    mov     w3, w1
    mov     w4, #ALIEN_V_SPACING
    mul     w3, w3, w4
    add     w3, w3, #80
    strh    w3, [x0, #ALIEN_Y]
    
    // Set alive
    mov     w3, #1
    strb    w3, [x0, #ALIEN_ALIVE]
    
    // Set type based on row
    cmp     w1, #0
    b.eq    3f                  // Top row
    cmp     w1, #2
    b.le    4f                  // Middle rows
    b       5f                  // Bottom rows
    
3:  // Top row alien
    mov     w3, #ALIEN_TYPE_TOP
    b       6f
    
4:  // Middle rows alien
    mov     w3, #ALIEN_TYPE_MIDDLE
    b       6f
    
5:  // Bottom rows alien
    mov     w3, #ALIEN_TYPE_BOTTOM
    
6:  strb    w3, [x0, #ALIEN_TYPE]
    
    // Next alien
    add     x0, x0, #ALIEN_SIZE
    add     w2, w2, #1
    cmp     w2, #ALIEN_COLS
    b.lt    2b
    
    // Next row
    add     w1, w1, #1
    cmp     w1, #ALIEN_ROWS
    b.lt    1b
    
    ldp     x29, x30, [sp], #16
    ret

// Update alien positions
// No parameters
.global _aliens_update
_aliens_update:
    stp     x29, x30, [sp, #-32]!
    mov     x29, sp
    stp     x19, x20, [sp, #16]
    
    // Check if it's time to move
    adrp    x0, move_counter@PAGE
    add     x0, x0, move_counter@PAGEOFF
    ldr     w1, [x0]
    add     w1, w1, #1
    str     w1, [x0]
    
    adrp    x0, move_delay@PAGE
    
    add     x0, x0, move_delay@PAGEOFF
    ldr     w2, [x0]
    cmp     w1, w2
    b.lt    9f                  // Not time to move yet
    
    // Reset counter
    adrp    x0, move_counter@PAGE
    add     x0, x0, move_counter@PAGEOFF
    str     wzr, [x0]
    
    // Check if we need to drop
    adrp    x0, drop_pending@PAGE
    add     x0, x0, drop_pending@PAGEOFF
    ldrb    w1, [x0]
    cbnz    w1, 1f
    
    // Check edges
    bl      _aliens_check_edges
    cbnz    w0, 2f              // Hit edge
    
    // Normal horizontal movement
    bl      _aliens_move
    b       9f
    
1:  // Drop down
    bl      _aliens_drop_row
    adrp    x0, drop_pending@PAGE
    add     x0, x0, drop_pending@PAGEOFF
    strb    wzr, [x0]
    b       9f
    
2:  // Hit edge - prepare to drop
    adrp    x0, drop_pending@PAGE
    add     x0, x0, drop_pending@PAGEOFF
    mov     w1, #1
    strb    w1, [x0]
    
    // Reverse direction
    adrp    x0, formation_dir@PAGE
    add     x0, x0, formation_dir@PAGEOFF
    ldrsb   w1, [x0]
    neg     w1, w1
    strb    w1, [x0]
    
9:  ldp     x19, x20, [sp, #16]
    ldp     x29, x30, [sp], #32
    ret

// Move formation horizontally
// No parameters
.global _aliens_move
_aliens_move:
    stp     x29, x30, [sp, #-16]!
    mov     x29, sp
    
    // Get movement direction
    adrp    x0, formation_dir@PAGE
    add     x0, x0, formation_dir@PAGEOFF
    ldrsb   w1, [x0]
    mov     w2, #ALIEN_MOVE_STEP
    mul     w1, w1, w2          // Movement delta
    
    // Update formation position
    adrp    x0, formation_x@PAGE
    add     x0, x0, formation_x@PAGEOFF
    ldrsh   w2, [x0]
    add     w2, w2, w1
    strh    w2, [x0]
    
    // Use NEON to update all alien positions
    adrp    x0, aliens_array@PAGE
    add     x0, x0, aliens_array@PAGEOFF
    mov     w2, #ALIEN_COUNT
    dup     v0.8h, w1           // Broadcast movement delta
    
1:  // Update loop
    ldrb    w3, [x0, #ALIEN_ALIVE]
    cbz     w3, 2f              // Skip dead aliens
    
    // Load position
    ldr     h1, [x0, #ALIEN_X]
    
    // Add movement delta
    add     v1.8h, v1.8h, v0.8h
    
    // Store back
    str     h1, [x0, #ALIEN_X]
    
2:  add     x0, x0, #ALIEN_SIZE
    subs    w2, w2, #1
    b.ne    1b
    
    ldp     x29, x30, [sp], #16
    ret

// Check if formation hit screen edge
// Returns: w0 = 1 if hit edge, 0 otherwise
.global _aliens_check_edges
_aliens_check_edges:
    stp     x29, x30, [sp, #-16]!
    mov     x29, sp
    
    adrp    x0, aliens_array@PAGE
    
    add     x0, x0, aliens_array@PAGEOFF
    adrp    x1, formation_dir@PAGE
    add     x1, x1, formation_dir@PAGEOFF
    ldrsb   w2, [x1]            // Get direction
    
    mov     w3, #ALIEN_COUNT
    mov     w4, #9999           // Min X (for right movement)
    mov     w5, #0              // Max X (for left movement)
    
1:  // Find extremes
    ldrb    w6, [x0, #ALIEN_ALIVE]
    cbz     w6, 2f              // Skip dead aliens
    
    ldrsh   w6, [x0, #ALIEN_X]
    
    // Update min/max
    cmp     w6, w4
    csel    w4, w6, w4, lt      // Update min
    cmp     w6, w5
    csel    w5, w6, w5, gt      // Update max
    
2:  add     x0, x0, #ALIEN_SIZE
    subs    w3, w3, #1
    b.ne    1b
    
    // Check boundaries based on direction
    mov     w0, #0              // Default: no collision
    cmp     w2, #0
    b.lt    3f                  // Moving left
    
    // Moving right - check right edge
    add     w5, w5, #ALIEN_WIDTH
    cmp     w5, #FORMATION_RIGHT_EDGE
    cset    w0, ge
    b       4f
    
3:  // Moving left - check left edge
    cmp     w4, #FORMATION_LEFT_EDGE
    cset    w0, le
    
4:  ldp     x29, x30, [sp], #16
    ret

// Drop formation down one row
// No parameters
.global _aliens_drop_row
_aliens_drop_row:
    stp     x29, x30, [sp, #-16]!
    mov     x29, sp
    
    // Update formation Y position
    adrp    x0, formation_y@PAGE
    add     x0, x0, formation_y@PAGEOFF
    ldrsh   w1, [x0]
    add     w1, w1, #ALIEN_DROP_STEP
    strh    w1, [x0]
    
    // Use NEON to update all alien Y positions
    adrp    x0, aliens_array@PAGE
    add     x0, x0, aliens_array@PAGEOFF
    mov     w2, #ALIEN_COUNT
    mov     w3, #ALIEN_DROP_STEP
    dup     v0.8h, w3           // Broadcast drop distance
    
1:  // Update loop
    ldrb    w3, [x0, #ALIEN_ALIVE]
    cbz     w3, 2f              // Skip dead aliens
    
    // Load Y position
    ldr     h1, [x0, #ALIEN_Y]
    
    // Add drop distance
    add     v1.8h, v1.8h, v0.8h
    
    // Store back
    str     h1, [x0, #ALIEN_Y]
    
2:  add     x0, x0, #ALIEN_SIZE
    subs    w2, w2, #1
    b.ne    1b
    
    // Increase speed after drop
    bl      _aliens_increase_speed
    
    ldp     x29, x30, [sp], #16
    ret

// Increase movement speed
// No parameters
.global _aliens_increase_speed
_aliens_increase_speed:
    stp     x29, x30, [sp, #-16]!
    mov     x29, sp
    
    // Get current delay
    adrp    x0, move_delay@PAGE
    add     x0, x0, move_delay@PAGEOFF
    ldr     w1, [x0]
    
    // Calculate new delay based on alive count
    adrp    x2, alive_count@PAGE
    add     x2, x2, alive_count@PAGEOFF
    ldr     w2, [x2]
    
    // Speed formula: delay = initial * (alive_count / total_count)
    mov     w3, #INITIAL_MOVE_DELAY
    mul     w3, w3, w2
    mov     w4, #ALIEN_COUNT
    udiv    w3, w3, w4
    
    // Ensure minimum delay
    cmp     w3, #MIN_MOVE_DELAY
    csel    w3, w3, w4, gt
    mov     w4, #MIN_MOVE_DELAY
    csel    w3, w3, w4, gt
    
    // Store new delay
    str     w3, [x0]
    
    ldp     x29, x30, [sp], #16
    ret

// Get number of alive aliens
// Returns: w0 = alive count
.global _aliens_get_count
_aliens_get_count:
    adrp    x0, alive_count@PAGE
    add     x0, x0, alive_count@PAGEOFF
    ldr     w0, [x0]
    ret

// Get alien at specific row/column
// Parameters: w0 = row, w1 = column
// Returns: x0 = alien pointer, or NULL if invalid
.global _aliens_get_at
_aliens_get_at:
    // Validate indices
    cmp     w0, #ALIEN_ROWS
    b.hs    1f
    cmp     w1, #ALIEN_COLS
    b.hs    1f
    
    // Calculate index
    mov     w2, #ALIEN_COLS
    mul     w2, w0, w2
    add     w2, w2, w1
    
    // Calculate address
    adrp    x0, aliens_array@PAGE
    add     x0, x0, aliens_array@PAGEOFF
    mov     w3, #ALIEN_SIZE
    mul     w3, w2, w3
    add     x0, x0, x3
    ret
    
1:  mov     x0, #0              // Invalid index
    ret

// Kill alien at row/column
// Parameters: w0 = row, w1 = column
.global _aliens_kill
_aliens_kill:
    stp     x29, x30, [sp, #-16]!
    mov     x29, sp
    
    // Get alien pointer
    bl      _aliens_get_at
    cbz     x0, 1f              // Invalid position
    
    // Check if already dead
    ldrb    w1, [x0, #ALIEN_ALIVE]
    cbz     w1, 1f
    
    // Mark as dead
    strb    wzr, [x0, #ALIEN_ALIVE]
    
    // Decrease alive count
    adrp    x1, alive_count@PAGE
    add     x1, x1, alive_count@PAGEOFF
    ldr     w2, [x1]
    sub     w2, w2, #1
    str     w2, [x1]
    
    // Update speed
    bl      _aliens_increase_speed
    
1:  ldp     x29, x30, [sp], #16
    ret

// Select random alien to fire
// Returns: x0 = alien pointer, or NULL if none available
.global _aliens_fire
_aliens_fire:
    stp     x29, x30, [sp, #-32]!
    mov     x29, sp
    stp     x19, x20, [sp, #16]
    
    // Simple counter-based "randomness"
    adrp    x0, fire_counter@PAGE
    add     x0, x0, fire_counter@PAGEOFF
    ldr     w1, [x0]
    add     w1, w1, #1
    str     w1, [x0]
    
    // Get alive count
    adrp    x2, alive_count@PAGE
    add     x2, x2, alive_count@PAGEOFF
    ldr     w2, [x2]
    cbz     w2, 4f              // No aliens alive
    
    // Select which alive alien (modulo alive count)
    udiv    w3, w1, w2
    msub    w1, w3, w2, w1      // w1 = w1 % w2
    
    // Find the nth alive alien
    adrp    x0, aliens_array@PAGE
    add     x0, x0, aliens_array@PAGEOFF
    mov     w3, #ALIEN_COUNT
    mov     w4, #0              // Alive counter
    
1:  ldrb    w5, [x0, #ALIEN_ALIVE]
    cbz     w5, 2f              // Skip dead aliens
    
    cmp     w4, w1
    b.eq    3f                  // Found our alien
    add     w4, w4, #1
    
2:  add     x0, x0, #ALIEN_SIZE
    subs    w3, w3, #1
    b.ne    1b
    
    // Shouldn't reach here, but return first alive alien
    adrp    x0, aliens_array@PAGE
    add     x0, x0, aliens_array@PAGEOFF
    mov     w3, #ALIEN_COUNT
    
5:  ldrb    w5, [x0, #ALIEN_ALIVE]
    cbnz    w5, 3f
    add     x0, x0, #ALIEN_SIZE
    subs    w3, w3, #1
    b.ne    5b
    b       4f
    
3:  // Found alien - check if it's in bottom row of formation
    // (Only bottom-most alive aliens in each column can fire)
    mov     x19, x0             // Save alien pointer
    
    // Get this alien's position
    ldrsh   w1, [x19, #ALIEN_X]
    ldrsh   w2, [x19, #ALIEN_Y]
    
    // Check if there's an alive alien below this one
    adrp    x0, aliens_array@PAGE
    add     x0, x0, aliens_array@PAGEOFF
    mov     w3, #ALIEN_COUNT
    mov     w20, #0             // Found lower alien flag
    
6:  ldrb    w4, [x0, #ALIEN_ALIVE]
    cbz     w4, 7f              // Skip dead aliens
    
    ldrsh   w4, [x0, #ALIEN_X]
    ldrsh   w5, [x0, #ALIEN_Y]
    
    // Check if same column and lower
    sub     w6, w4, w1
    cmp     w6, #8              // Within same column (some tolerance)
    b.gt    7f
    cmn     w6, #8
    b.lt    7f
    
    cmp     w5, w2              // Is it lower?
    b.le    7f
    
    mov     w20, #1             // Found a lower alien
    b       8f
    
7:  add     x0, x0, #ALIEN_SIZE
    subs    w3, w3, #1
    b.ne    6b
    
8:  cbnz    w20, 1b             // This alien can't fire, try another
    
    mov     x0, x19             // Return the alien pointer
    b       9f
    
4:  mov     x0, #0              // No aliens available
    
9:  ldp     x19, x20, [sp, #16]
    ldp     x29, x30, [sp], #32
    ret

// Check if aliens reached bottom (invasion)
// Returns: w0 = 1 if invaded, 0 otherwise
.global _aliens_check_invasion
_aliens_check_invasion:
    adrp    x0, aliens_array@PAGE
    add     x0, x0, aliens_array@PAGEOFF
    mov     w1, #ALIEN_COUNT
    mov     w2, #0              // Max Y position
    
1:  ldrb    w3, [x0, #ALIEN_ALIVE]
    cbz     w3, 2f              // Skip dead aliens
    
    ldrsh   w3, [x0, #ALIEN_Y]
    add     w3, w3, #ALIEN_HEIGHT
    cmp     w3, w2
    csel    w2, w3, w2, gt      // Update max Y
    
2:  add     x0, x0, #ALIEN_SIZE
    subs    w1, w1, #1
    b.ne    1b
    
    // Check if max Y reached bottom
    cmp     w2, #FORMATION_BOTTOM
    cset    w0, ge
    ret

// Get alien array base address (for rendering)
// Returns: x0 = array address
.global _aliens_get_array
_aliens_get_array:
    adrp    x0, aliens_array@PAGE
    add     x0, x0, aliens_array@PAGEOFF
    ret

// Get formation position (for collision detection)
// Returns: w0 = X position, w1 = Y position
.global _aliens_get_formation_pos
_aliens_get_formation_pos:
    adrp    x2, formation_x@PAGE
    add     x2, x2, formation_x@PAGEOFF
    ldrsh   w0, [x2]
    adrp    x2, formation_y@PAGE
    add     x2, x2, formation_y@PAGEOFF
    ldrsh   w1, [x2]
    ret