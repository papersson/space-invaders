// bullets.s - Alien bullet management system
// Handles alien projectiles with different movement patterns

.section __TEXT,__const
.p2align 4

// Bullet system constants
.equ MAX_ALIEN_BULLETS, 4
.equ ALIEN_BULLET_SPEED, 3
.equ BULLET_WIDTH, 3
.equ BULLET_HEIGHT, 5
.equ SCREEN_HEIGHT, 256
.equ SCREEN_WIDTH, 224

// Bullet structure offsets
.equ BULLET_X, 0            // 2 bytes - X position
.equ BULLET_Y, 2            // 2 bytes - Y position  
.equ BULLET_ACTIVE, 4       // 1 byte - Active flag (0=inactive, 1=active)
.equ BULLET_TYPE, 5         // 1 byte - Bullet type (0=straight, 1=zigzag)
.equ BULLET_FRAME, 6        // 1 byte - Animation frame counter
.equ BULLET_RESERVED, 7     // 1 byte - Reserved for alignment
.equ BULLET_SIZE, 8         // Total size of bullet structure

// Bullet types
.equ BULLET_TYPE_STRAIGHT, 0
.equ BULLET_TYPE_ZIGZAG, 1

// Zigzag pattern constants
.equ ZIGZAG_AMPLITUDE, 2    // Pixels to move left/right
.equ ZIGZAG_PERIOD, 8       // Frames per zigzag cycle

.section __DATA,__data
.p2align 4

// Alien bullets array
alien_bullets:
    .space MAX_ALIEN_BULLETS * BULLET_SIZE

// Bullet system state
active_bullet_count:    .word 0
next_bullet_index:      .word 0     // Ring buffer index

.section __TEXT,__text
.p2align 2

// Initialize bullet system
// No parameters
// Returns: nothing
.global _bullets_init
_bullets_init:
    stp     x29, x30, [sp, #-16]!
    mov     x29, sp
    
    // Clear all bullets
    adrp    x0, alien_bullets@PAGE
    add     x0, x0, alien_bullets@PAGEOFF
    mov     w1, #MAX_ALIEN_BULLETS
    mov     w2, #0
    
1:  // Clear loop
    strb    wzr, [x0, #BULLET_ACTIVE]
    strh    wzr, [x0, #BULLET_X]
    strh    wzr, [x0, #BULLET_Y]
    strb    wzr, [x0, #BULLET_TYPE]
    strb    wzr, [x0, #BULLET_FRAME]
    add     x0, x0, #BULLET_SIZE
    subs    w1, w1, #1
    bne     1b
    
    // Reset counters
    adrp    x0, active_bullet_count@PAGE
    add     x0, x0, active_bullet_count@PAGEOFF
    str     wzr, [x0]
    
    adrp    x0, next_bullet_index@PAGE
    
    add     x0, x0, next_bullet_index@PAGEOFF
    str     wzr, [x0]
    
    ldp     x29, x30, [sp], #16
    ret

// Fire alien bullet
// x0 = X position
// x1 = Y position  
// x2 = bullet type (0=straight, 1=zigzag)
// Returns: w0 = 1 if bullet created, 0 if failed
.global _bullets_fire_alien
_bullets_fire_alien:
    stp     x29, x30, [sp, #-32]!
    mov     x29, sp
    stp     x19, x20, [sp, #16]
    
    // Check if we can create a new bullet
    adrp    x3, active_bullet_count@PAGE
    add     x3, x3, active_bullet_count@PAGEOFF
    ldr     w4, [x3]
    cmp     w4, #MAX_ALIEN_BULLETS
    bge     2f                      // Failed - too many bullets
    
    // Find an inactive bullet slot
    adrp    x3, alien_bullets@PAGE
    add     x3, x3, alien_bullets@PAGEOFF
    mov     w4, #0                  // Index counter
    
1:  // Search loop
    ldrb    w5, [x3, #BULLET_ACTIVE]
    cbz     w5, 3f                  // Found inactive slot
    add     x3, x3, #BULLET_SIZE
    add     w4, w4, #1
    cmp     w4, #MAX_ALIEN_BULLETS
    blt     1b
    
2:  // Failed to create bullet
    mov     w0, #0
    ldp     x19, x20, [sp, #16]
    ldp     x29, x30, [sp], #32
    ret
    
3:  // Create bullet in slot x3
    // Store position
    strh    w0, [x3, #BULLET_X]
    strh    w1, [x3, #BULLET_Y]
    
    // Set active and type
    mov     w5, #1
    strb    w5, [x3, #BULLET_ACTIVE]
    strb    w2, [x3, #BULLET_TYPE]
    
    // Clear frame counter
    strb    wzr, [x3, #BULLET_FRAME]
    
    // Increment active count
    adrp    x4, active_bullet_count@PAGE
    add     x4, x4, active_bullet_count@PAGEOFF
    ldr     w5, [x4]
    add     w5, w5, #1
    str     w5, [x4]
    
    // Success
    mov     w0, #1
    ldp     x19, x20, [sp, #16]
    ldp     x29, x30, [sp], #32
    ret

// Update all alien bullets
// No parameters
// Returns: nothing
.global _bullets_update_alien
_bullets_update_alien:
    stp     x29, x30, [sp, #-32]!
    mov     x29, sp
    stp     x19, x20, [sp, #16]
    
    // Process each bullet
    adrp    x19, alien_bullets@PAGE
    add     x19, x19, alien_bullets@PAGEOFF
    mov     w20, #0                 // Index
    
1:  // Update loop
    ldrb    w0, [x19, #BULLET_ACTIVE]
    cbz     w0, 4f                  // Skip inactive bullets
    
    // Get current position
    ldrh    w0, [x19, #BULLET_X]
    ldrh    w1, [x19, #BULLET_Y]
    
    // Update Y position (move down)
    add     w1, w1, #ALIEN_BULLET_SPEED
    
    // Check if bullet type is zigzag
    ldrb    w2, [x19, #BULLET_TYPE]
    cmp     w2, #BULLET_TYPE_ZIGZAG
    bne     2f
    
    // Apply zigzag pattern
    ldrb    w3, [x19, #BULLET_FRAME]
    and     w4, w3, #ZIGZAG_PERIOD - 1
    
    // Calculate X offset based on frame
    cmp     w4, #(ZIGZAG_PERIOD / 2)
    blt     3f
    
    // Move left
    sub     w0, w0, #ZIGZAG_AMPLITUDE
    b       2f
    
3:  // Move right
    add     w0, w0, #ZIGZAG_AMPLITUDE
    
2:  // Store updated position
    strh    w0, [x19, #BULLET_X]
    strh    w1, [x19, #BULLET_Y]
    
    // Increment frame counter
    ldrb    w3, [x19, #BULLET_FRAME]
    add     w3, w3, #1
    strb    w3, [x19, #BULLET_FRAME]
    
    // Check if bullet went off screen
    cmp     w1, #SCREEN_HEIGHT
    blt     4f
    
    // Deactivate bullet
    strb    wzr, [x19, #BULLET_ACTIVE]
    
    // Decrement active count
    adrp    x0, active_bullet_count@PAGE
    add     x0, x0, active_bullet_count@PAGEOFF
    ldr     w1, [x0]
    sub     w1, w1, #1
    str     w1, [x0]
    
4:  // Next bullet
    add     x19, x19, #BULLET_SIZE
    add     w20, w20, #1
    cmp     w20, #MAX_ALIEN_BULLETS
    blt     1b
    
    ldp     x19, x20, [sp, #16]
    ldp     x29, x30, [sp], #32
    ret

// Deactivate specific alien bullet
// x0 = bullet index (0-3)
// Returns: nothing
.global _bullets_deactivate_alien
_bullets_deactivate_alien:
    stp     x29, x30, [sp, #-16]!
    mov     x29, sp
    
    // Validate index
    cmp     x0, #MAX_ALIEN_BULLETS
    bge     2f
    
    // Calculate bullet address
    adrp    x1, alien_bullets@PAGE
    add     x1, x1, alien_bullets@PAGEOFF
    mov     x2, #BULLET_SIZE
    mul     x2, x0, x2
    add     x1, x1, x2
    
    // Check if already inactive
    ldrb    w2, [x1, #BULLET_ACTIVE]
    cbz     w2, 2f
    
    // Deactivate bullet
    strb    wzr, [x1, #BULLET_ACTIVE]
    
    // Decrement active count
    adrp    x0, active_bullet_count@PAGE
    add     x0, x0, active_bullet_count@PAGEOFF
    ldr     w1, [x0]
    sub     w1, w1, #1
    str     w1, [x0]
    
2:  
    ldp     x29, x30, [sp], #16
    ret

// Get active alien bullet count
// No parameters
// Returns: w0 = number of active bullets
.global _bullets_get_alien_count
_bullets_get_alien_count:
    adrp    x0, active_bullet_count@PAGE
    add     x0, x0, active_bullet_count@PAGEOFF
    ldr     w0, [x0]
    ret

// Get alien bullet data at index
// x0 = bullet index (0-3)
// Returns: x0 = X position (or -1 if invalid/inactive)
//         x1 = Y position
//         x2 = bullet type
.global _bullets_get_alien_at
_bullets_get_alien_at:
    // Validate index
    cmp     x0, #MAX_ALIEN_BULLETS
    bge     1f
    
    // Calculate bullet address
    adrp    x1, alien_bullets@PAGE
    add     x1, x1, alien_bullets@PAGEOFF
    mov     x2, #BULLET_SIZE
    mul     x2, x0, x2
    add     x1, x1, x2
    
    // Check if active
    ldrb    w2, [x1, #BULLET_ACTIVE]
    cbz     w2, 1f
    
    // Return bullet data
    ldrh    w0, [x1, #BULLET_X]
    ldrh    w1, [x1, #BULLET_Y]
    ldrb    w2, [x1, #BULLET_TYPE]
    ret
    
1:  // Invalid or inactive
    mov     x0, #-1
    mov     x1, #0
    mov     x2, #0
    ret

// Clear all bullets
// No parameters
// Returns: nothing
.global _bullets_clear_all
_bullets_clear_all:
    stp     x29, x30, [sp, #-16]!
    mov     x29, sp
    
    // Deactivate all bullets
    adrp    x0, alien_bullets@PAGE
    add     x0, x0, alien_bullets@PAGEOFF
    mov     w1, #MAX_ALIEN_BULLETS
    
1:  
    strb    wzr, [x0, #BULLET_ACTIVE]
    add     x0, x0, #BULLET_SIZE
    subs    w1, w1, #1
    bne     1b
    
    // Reset active count
    adrp    x0, active_bullet_count@PAGE
    add     x0, x0, active_bullet_count@PAGEOFF
    str     wzr, [x0]
    
    ldp     x29, x30, [sp], #16
    ret

// Check collision between bullet and rectangle
// x0 = bullet index
// x1 = rect X
// x2 = rect Y
// x3 = rect width
// x4 = rect height
// Returns: w0 = 1 if collision, 0 if not
.global _bullets_check_collision_at
_bullets_check_collision_at:
    stp     x29, x30, [sp, #-32]!
    mov     x29, sp
    stp     x19, x20, [sp, #16]
    
    // Validate index
    cmp     x0, #MAX_ALIEN_BULLETS
    bge     2f
    
    // Calculate bullet address
    adrp    x5, alien_bullets@PAGE
    add     x5, x5, alien_bullets@PAGEOFF
    mov     x6, #BULLET_SIZE
    mul     x6, x0, x6
    add     x5, x5, x6
    
    // Check if active
    ldrb    w6, [x5, #BULLET_ACTIVE]
    cbz     w6, 2f
    
    // Get bullet position
    ldrh    w6, [x5, #BULLET_X]
    ldrh    w7, [x5, #BULLET_Y]
    
    // Check X collision
    cmp     w6, w1
    blt     2f                  // bullet.x < rect.x
    add     w8, w1, w3
    cmp     w6, w8
    bge     2f                  // bullet.x >= rect.x + rect.width
    
    // Check Y collision
    cmp     w7, w2
    blt     2f                  // bullet.y < rect.y
    add     w8, w2, w4
    cmp     w7, w8
    bge     2f                  // bullet.y >= rect.y + rect.height
    
    // Collision detected
    mov     w0, #1
    ldp     x19, x20, [sp, #16]
    ldp     x29, x30, [sp], #32
    ret
    
2:  // No collision
    mov     w0, #0
    ldp     x19, x20, [sp, #16]
    ldp     x29, x30, [sp], #32
    ret