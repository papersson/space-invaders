// collision.s - NEON-optimized collision detection for Space Invaders
// Provides fast collision detection between game objects using SIMD

.include "constants.inc"

.section __TEXT,__text
.global _collision_player_bullet_aliens
.global _collision_alien_bullets_player
.global _collision_bullets_shields
.global _collision_aliens_shields
.global _collision_point_in_rect
.global _collision_check_alien_bullets
.global _collision_bbox_overlap

.p2align 4

// Collision data structures
.section __DATA,__data
.p2align 4

// Shield positions (4 shields evenly spaced)
shield_positions:
    .hword 32, 180              // Shield 0: x, y
    .hword 78, 180              // Shield 1: x, y
    .hword 124, 180             // Shield 2: x, y
    .hword 170, 180             // Shield 3: x, y

// Shield damage masks (22x16 pixels each)
shield_damage_masks:
    .space SHIELD_WIDTH * SHIELD_HEIGHT * 4  // 4 shields

// Alien bullet tracking (up to MAX_ALIEN_BULLETS)
alien_bullets:
    .space MAX_ALIEN_BULLETS * 8  // x, y, active, type (2+2+1+1+2 padding)

.section __TEXT,__text

// Check player bullet against all aliens
// Parameters: x0 = bullet_x, x1 = bullet_y
// Returns: x0 = alien index hit (0-54) or -1 if no hit
_collision_player_bullet_aliens:
    stp x29, x30, [sp, #-64]!
    stp x19, x20, [sp, #16]
    stp x21, x22, [sp, #32]
    stp x23, x24, [sp, #48]
    mov x29, sp
    
    // Save bullet position
    mov w19, w0                 // bullet_x
    mov w20, w1                 // bullet_y
    
    // Get aliens array
    bl _aliens_get_array
    mov x21, x0                 // aliens array pointer
    
    // Prepare for NEON processing - check 4 aliens at once
    dup v16.4s, w19             // Broadcast bullet_x
    dup v17.4s, w20             // Broadcast bullet_y
    
    // Prepare alien width/height for bounds checking
    mov w23, #ALIEN_WIDTH
    mov w24, #ALIEN_HEIGHT
    dup v18.4s, w23             // Broadcast ALIEN_WIDTH
    dup v19.4s, w24             // Broadcast ALIEN_HEIGHT
    
    // Process aliens in groups of 4
    mov w22, #0                 // alien index
    mov w0, #-1                 // default return (no hit)
    
alien_check_loop_neon:
    // Check if we have at least 4 aliens left
    mov w23, #ALIEN_COUNT
    sub w23, w23, w22
    cmp w23, #4
    blt alien_check_single      // Less than 4, check individually
    
    // Load 4 aliens' alive status
    ldrb w2, [x21, #4]          // alien[0].alive
    ldrb w3, [x21, #12]         // alien[1].alive
    ldrb w4, [x21, #20]         // alien[2].alive
    ldrb w5, [x21, #28]         // alien[3].alive
    
    // Combine alive status
    orr w2, w2, w3, lsl #8
    orr w2, w2, w4, lsl #16
    orr w2, w2, w5, lsl #24
    cbz w2, skip_group          // All 4 are dead
    
    // Load 4 aliens' positions
    ldrh w3, [x21, #0]          // alien[0].x
    ldrh w4, [x21, #8]          // alien[1].x
    ldrh w5, [x21, #16]         // alien[2].x
    ldrh w6, [x21, #24]         // alien[3].x
    
    // Create vector of alien X positions
    mov v0.s[0], w3
    mov v0.s[1], w4
    mov v0.s[2], w5
    mov v0.s[3], w6
    
    // Load Y positions
    ldrh w3, [x21, #2]          // alien[0].y
    ldrh w4, [x21, #10]         // alien[1].y
    ldrh w5, [x21, #18]         // alien[2].y
    ldrh w6, [x21, #26]         // alien[3].y
    
    // Create vector of alien Y positions
    mov v1.s[0], w3
    mov v1.s[1], w4
    mov v1.s[2], w5
    mov v1.s[3], w6
    
    // Check X bounds: bullet_x >= alien_x && bullet_x < alien_x + width
    cmhs v2.4s, v16.4s, v0.4s   // bullet_x >= alien_x
    add v3.4s, v0.4s, v18.4s    // alien_x + width
    cmhi v4.4s, v3.4s, v16.4s   // alien_x + width > bullet_x
    and v2.16b, v2.16b, v4.16b  // combine X checks
    
    // Check Y bounds: bullet_y >= alien_y && bullet_y < alien_y + height
    cmhs v3.4s, v17.4s, v1.4s   // bullet_y >= alien_y
    add v4.4s, v1.4s, v19.4s    // alien_y + height
    cmhi v5.4s, v4.4s, v17.4s   // alien_y + height > bullet_y
    and v3.16b, v3.16b, v5.16b  // combine Y checks
    
    // Combine X and Y checks
    and v2.16b, v2.16b, v3.16b
    
    // Extract results and check each alien
    umov w3, v2.s[0]
    cbz w3, check_alien_1
    ldrb w3, [x21, #4]          // Check if alive
    cbnz w3, found_alien_0
    
check_alien_1:
    umov w3, v2.s[1]
    cbz w3, check_alien_2
    ldrb w3, [x21, #12]         // Check if alive
    cbnz w3, found_alien_1
    
check_alien_2:
    umov w3, v2.s[2]
    cbz w3, check_alien_3
    ldrb w3, [x21, #20]         // Check if alive
    cbnz w3, found_alien_2
    
check_alien_3:
    umov w3, v2.s[3]
    cbz w3, skip_group
    ldrb w3, [x21, #28]         // Check if alive
    cbnz w3, found_alien_3
    
skip_group:
    add x21, x21, #32           // Move to next group (4 aliens * 8 bytes)
    add w22, w22, #4
    cmp w22, #ALIEN_COUNT
    blt alien_check_loop_neon
    b collision_not_found
    
found_alien_0:
    mov w0, w22
    b collision_found
found_alien_1:
    add w0, w22, #1
    b collision_found
found_alien_2:
    add w0, w22, #2
    b collision_found
found_alien_3:
    add w0, w22, #3
    b collision_found
    
alien_check_single:
    // Check remaining aliens individually
    cmp w22, #ALIEN_COUNT
    bge collision_not_found
    
    // Check if alien is alive
    ldrb w2, [x21, #4]          // ALIEN_ALIVE offset
    cbz w2, next_alien_single
    
    // Load alien position
    ldrh w3, [x21, #0]          // alien_x
    ldrh w4, [x21, #2]          // alien_y
    
    // Check X bounds
    sub w5, w19, w3             // delta_x = bullet_x - alien_x
    cmp w5, #0
    blt next_alien_single       // bullet is left of alien
    cmp w5, #ALIEN_WIDTH
    bge next_alien_single       // bullet is right of alien
    
    // Check Y bounds
    sub w6, w20, w4             // delta_y = bullet_y - alien_y
    cmp w6, #0
    blt next_alien_single       // bullet is above alien
    cmp w6, #ALIEN_HEIGHT
    bge next_alien_single       // bullet is below alien
    
    // Hit detected!
    mov w0, w22                 // return alien index
    b collision_found

next_alien_single:
    add x21, x21, #8            // Move to next alien (ALIEN_SIZE)
    add w22, w22, #1
    b alien_check_single
    
collision_not_found:
    mov w0, #-1                 // No collision
    
collision_found:
    ldp x23, x24, [sp, #48]
    ldp x21, x22, [sp, #32]
    ldp x19, x20, [sp, #16]
    ldp x29, x30, [sp], #64
    ret

// Check all alien bullets against player
// Parameters: x0 = player_x, x1 = player_y
// Returns: x0 = 1 if hit, 0 if not
_collision_alien_bullets_player:
    stp x29, x30, [sp, #-48]!
    stp x19, x20, [sp, #16]
    stp x21, x22, [sp, #32]
    mov x29, sp
    
    // Save player position
    mov w19, w0                 // player_x
    mov w20, w1                 // player_y
    
    // Get alien bullets array
    adrp x0, alien_bullets@PAGE
    add x0, x0, alien_bullets@PAGEOFF
    
    // Check each alien bullet
    mov w21, #0                 // bullet index
    mov w0, #0                  // default: no hit
    
bullet_player_loop:
    // Check if bullet is active
    ldrb w2, [x0, #4]           // active flag
    cbz w2, next_bullet_player
    
    // Load bullet position
    ldrh w3, [x0, #0]           // bullet_x
    ldrh w4, [x0, #2]           // bullet_y
    
    // Check collision with player bounding box
    // Check if bullet_x is within player bounds
    sub w5, w3, w19             // delta = bullet_x - player_x
    cmp w5, #0
    blt next_bullet_player
    cmp w5, #PLAYER_WIDTH
    bge next_bullet_player
    
    // Check if bullet_y is within player bounds
    sub w5, w4, w20             // delta = bullet_y - player_y
    cmp w5, #0
    blt next_bullet_player
    cmp w5, #PLAYER_HEIGHT
    bge next_bullet_player
    
    // Hit detected!
    mov w0, #1
    b player_hit_found
    
next_bullet_player:
    add x0, x0, #8              // Next bullet
    add w21, w21, #1
    cmp w21, #MAX_ALIEN_BULLETS
    blt bullet_player_loop
    
player_hit_found:
    ldp x21, x22, [sp, #32]
    ldp x19, x20, [sp, #16]
    ldp x29, x30, [sp], #48
    ret

// Check all bullets against shields (pixel-perfect)
// Parameters: x0 = bullet_x, x1 = bullet_y, x2 = bullet_type (0=player, 1=alien)
// Returns: x0 = shield_index hit (0-3) or -1, x1 = pixel_x, x2 = pixel_y
_collision_bullets_shields:
    stp x29, x30, [sp, #-80]!
    stp x19, x20, [sp, #16]
    stp x21, x22, [sp, #32]
    stp x23, x24, [sp, #48]
    stp x25, x26, [sp, #64]
    mov x29, sp
    
    mov w19, w0                 // bullet_x
    mov w20, w1                 // bullet_y
    mov w21, w2                 // bullet_type
    
    // Get shield positions
    adrp x25, shield_positions@PAGE
    add x25, x25, shield_positions@PAGEOFF
    
    // Get shield damage masks
    adrp x26, shield_damage_masks@PAGE
    add x26, x26, shield_damage_masks@PAGEOFF
    
    mov w22, #0                 // shield index
    
shield_check_loop:
    // Load shield position
    ldrh w23, [x25], #2         // shield_x
    ldrh w24, [x25], #2         // shield_y
    
    // Check if bullet overlaps shield bounding box
    sub w0, w19, w23            // delta_x = bullet_x - shield_x
    cmp w0, #0
    blt next_shield
    cmp w0, #SHIELD_WIDTH
    bge next_shield
    
    sub w1, w20, w24            // delta_y = bullet_y - shield_y
    cmp w1, #0
    blt next_shield
    cmp w1, #SHIELD_HEIGHT
    bge next_shield
    
    // Bounding box hit - check pixel-perfect collision
    // Calculate relative position within shield
    sub w3, w19, w23            // rel_x
    sub w4, w20, w24            // rel_y
    
    // Check center of bullet (more accurate for small bullets)
    add w3, w3, #(BULLET_WIDTH/2)
    add w4, w4, #(BULLET_HEIGHT/2)
    
    // Ensure we're within shield bounds after centering
    cmp w3, #SHIELD_WIDTH
    bge next_shield
    cmp w4, #SHIELD_HEIGHT
    bge next_shield
    
    // Calculate damage mask offset for this shield
    mov w5, #(SHIELD_WIDTH * SHIELD_HEIGHT)
    mul w5, w5, w22             // shield_index * pixels_per_shield
    add x5, x26, x5             // damage mask for this shield
    
    // Calculate pixel offset within shield
    mov w6, #SHIELD_WIDTH
    mul w6, w4, w6              // y * width
    add w6, w6, w3              // + x
    
    // Check if pixel is already destroyed
    ldrb w7, [x5, x6]           // Load damage value
    cbnz w7, next_shield        // Already destroyed, no collision
    
    // Solid pixel hit!
    mov w0, w22                 // shield index
    sub w1, w19, w23            // pixel_x within shield
    sub w2, w20, w24            // pixel_y within shield
    
    // Mark pixel as destroyed
    mov w7, #1
    strb w7, [x5, x6]
    
    // Optionally create explosion pattern based on bullet type
    cmp w21, #0                 // Player bullet?
    beq small_damage
    
    // Alien bullet - larger damage pattern
    bl create_large_damage_pattern
    b shield_collision_found
    
small_damage:
    // Player bullet - smaller damage pattern
    bl create_small_damage_pattern
    
shield_collision_found:
    ldp x25, x26, [sp, #64]
    ldp x23, x24, [sp, #48]
    ldp x21, x22, [sp, #32]
    ldp x19, x20, [sp, #16]
    ldp x29, x30, [sp], #80
    ret
    
next_shield:
    add w22, w22, #1
    cmp w22, #SHIELD_COUNT
    blt shield_check_loop
    
    // No collision
    mov w0, #-1
    mov w1, #0
    mov w2, #0
    
    ldp x25, x26, [sp, #64]
    ldp x23, x24, [sp, #48]
    ldp x21, x22, [sp, #32]
    ldp x19, x20, [sp, #16]
    ldp x29, x30, [sp], #80
    ret

// Create small damage pattern (3x3)
// Parameters: x5 = damage mask base, w3 = center_x, w4 = center_y
create_small_damage_pattern:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    
    // Damage a 3x3 area around impact point
    sub w0, w3, #1              // start_x = center_x - 1
    sub w1, w4, #1              // start_y = center_y - 1
    
    mov w2, #3                  // rows to damage
damage_row_small:
    mov w7, w0                  // x = start_x
    mov w8, #3                  // cols to damage
    
damage_col_small:
    // Bounds check
    cmp w7, #0
    blt skip_pixel_small
    cmp w7, #SHIELD_WIDTH
    bge skip_pixel_small
    cmp w1, #0
    blt skip_pixel_small
    cmp w1, #SHIELD_HEIGHT
    bge skip_pixel_small
    
    // Calculate offset and mark as destroyed
    mov w9, #SHIELD_WIDTH
    mul w9, w1, w9              // y * width
    add w9, w9, w7              // + x
    mov w10, #1
    strb w10, [x5, x9]          // Mark as destroyed
    
skip_pixel_small:
    add w7, w7, #1              // next column
    subs w8, w8, #1
    bne damage_col_small
    
    add w1, w1, #1              // next row
    subs w2, w2, #1
    bne damage_row_small
    
    ldp x29, x30, [sp], #16
    ret

// Create large damage pattern (5x5)
// Parameters: x5 = damage mask base, w3 = center_x, w4 = center_y
create_large_damage_pattern:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    
    // Damage a 5x5 area around impact point
    sub w0, w3, #2              // start_x = center_x - 2
    sub w1, w4, #2              // start_y = center_y - 2
    
    mov w2, #5                  // rows to damage
damage_row_large:
    mov w7, w0                  // x = start_x
    mov w8, #5                  // cols to damage
    
damage_col_large:
    // Bounds check
    cmp w7, #0
    blt skip_pixel_large
    cmp w7, #SHIELD_WIDTH
    bge skip_pixel_large
    cmp w1, #0
    blt skip_pixel_large
    cmp w1, #SHIELD_HEIGHT
    bge skip_pixel_large
    
    // Calculate offset and mark as destroyed
    mov w9, #SHIELD_WIDTH
    mul w9, w1, w9              // y * width
    add w9, w9, w7              // + x
    mov w10, #1
    strb w10, [x5, x9]          // Mark as destroyed
    
skip_pixel_large:
    add w7, w7, #1              // next column
    subs w8, w8, #1
    bne damage_col_large
    
    add w1, w1, #1              // next row
    subs w2, w2, #1
    bne damage_row_large
    
    ldp x29, x30, [sp], #16
    ret

// Check if aliens are touching shields
// Returns: x0 = 1 if touching, 0 if not
_collision_aliens_shields:
    stp x29, x30, [sp, #-48]!
    stp x19, x20, [sp, #16]
    stp x21, x22, [sp, #32]
    mov x29, sp
    
    // Get aliens array
    bl _aliens_get_array
    mov x19, x0
    
    // Shield Y position
    mov w20, #180               // shields y position
    
    // Check each alien
    mov w21, #0                 // alien index
    
alien_shield_loop:
    // Check if alien is alive
    ldrb w0, [x19, #4]          // ALIEN_ALIVE offset
    cbz w0, next_alien_shield
    
    // Get alien bottom position
    ldrh w0, [x19, #2]          // alien_y
    add w0, w0, #ALIEN_HEIGHT   // alien bottom
    
    // Check if alien bottom touches shield top
    cmp w0, w20
    bge aliens_touching_shields
    
next_alien_shield:
    add x19, x19, #8            // Move to next alien
    add w21, w21, #1
    cmp w21, #ALIEN_COUNT
    blt alien_shield_loop
    
    // No collision
    mov w0, #0
    b aliens_shields_done
    
aliens_touching_shields:
    mov w0, #1
    
aliens_shields_done:
    ldp x21, x22, [sp, #32]
    ldp x19, x20, [sp, #16]
    ldp x29, x30, [sp], #48
    ret

// Basic point-in-rectangle test
// Parameters: x0 = point_x, x1 = point_y, x2 = rect_x, x3 = rect_y,
//            x4 = rect_width, x5 = rect_height
// Returns: x0 = 1 if inside, 0 if outside
_collision_point_in_rect:
    // Check X bounds
    sub w6, w0, w2              // delta_x = point_x - rect_x
    cmp w6, #0
    blt point_outside
    cmp w6, w4                  // compare with rect_width
    bge point_outside
    
    // Check Y bounds
    sub w6, w1, w3              // delta_y = point_y - rect_y
    cmp w6, #0
    blt point_outside
    cmp w6, w5                  // compare with rect_height
    bge point_outside
    
    // Point is inside
    mov w0, #1
    ret
    
point_outside:
    mov w0, #0
    ret

// NEON-optimized helper: Check multiple rectangles at once
// Parameters: x0 = point_x, x1 = point_y, x2 = rects array pointer,
//            x3 = rect count
// Returns: x0 = index of hit rect or -1
.global _collision_point_in_rects_neon
_collision_point_in_rects_neon:
    stp x29, x30, [sp, #-32]!
    stp x19, x20, [sp, #16]
    mov x29, sp
    
    // Broadcast point coordinates
    dup v0.4s, w0               // point_x in all lanes
    dup v1.4s, w1               // point_y in all lanes
    
    mov w19, #0                 // rect index
    mov w0, #-1                 // default return
    
rect_check_loop:
    // Process 4 rectangles at once
    mov w20, w3
    cmp w20, #4
    blt check_remaining_rects
    
    // Load 4 rect X positions
    ldp w4, w5, [x2]
    ldp w6, w7, [x2, #16]
    mov v2.s[0], w4
    mov v2.s[1], w5
    mov v2.s[2], w6
    mov v2.s[3], w7
    
    // Load 4 rect Y positions
    ldp w4, w5, [x2, #8]
    ldp w6, w7, [x2, #24]
    mov v3.s[0], w4
    mov v3.s[1], w5
    mov v3.s[2], w6
    mov v3.s[3], w7
    
    // Load 4 rect widths
    ldp w4, w5, [x2, #32]
    ldp w6, w7, [x2, #48]
    mov v4.s[0], w4
    mov v4.s[1], w5
    mov v4.s[2], w6
    mov v4.s[3], w7
    
    // Load 4 rect heights
    ldp w4, w5, [x2, #40]
    ldp w6, w7, [x2, #56]
    mov v5.s[0], w4
    mov v5.s[1], w5
    mov v5.s[2], w6
    mov v5.s[3], w7
    
    // Check X bounds: point_x >= rect_x && point_x < rect_x + width
    cmhs v6.4s, v0.4s, v2.4s    // point_x >= rect_x
    add v7.4s, v2.4s, v4.4s     // rect_x + width
    cmhi v8.4s, v7.4s, v0.4s    // rect_x + width > point_x
    and v6.16b, v6.16b, v8.16b  // combine X checks
    
    // Check Y bounds: point_y >= rect_y && point_y < rect_y + height
    cmhs v7.4s, v1.4s, v3.4s    // point_y >= rect_y
    add v8.4s, v3.4s, v5.4s     // rect_y + height
    cmhi v9.4s, v8.4s, v1.4s    // rect_y + height > point_y
    and v7.16b, v7.16b, v9.16b  // combine Y checks
    
    // Combine X and Y checks
    and v6.16b, v6.16b, v7.16b
    
    // Extract results
    umov w4, v6.s[0]
    cbnz w4, found_rect_0
    umov w4, v6.s[1]
    cbnz w4, found_rect_1
    umov w4, v6.s[2]
    cbnz w4, found_rect_2
    umov w4, v6.s[3]
    cbnz w4, found_rect_3
    
    add x2, x2, #64             // Move to next 4 rects
    add w19, w19, #4
    sub w3, w3, #4
    b rect_check_loop
    
found_rect_0:
    mov w0, w19
    b rect_hit_done
found_rect_1:
    add w0, w19, #1
    b rect_hit_done
found_rect_2:
    add w0, w19, #2
    b rect_hit_done
found_rect_3:
    add w0, w19, #3
    b rect_hit_done
    
check_remaining_rects:
    // Handle remaining rects one by one
    cbz w3, no_rect_hit
    
single_rect_loop:
    ldp w4, w5, [x2], #8        // rect_x, rect_y
    ldp w6, w7, [x2], #8        // rect_width, rect_height
    
    // Check bounds
    sub w8, w0, w4              // delta_x
    cmp w8, #0
    blt next_single_rect
    cmp w8, w6
    bge next_single_rect
    
    sub w8, w1, w5              // delta_y
    cmp w8, #0
    blt next_single_rect
    cmp w8, w7
    bge next_single_rect
    
    // Hit found
    mov w0, w19
    b rect_hit_done
    
next_single_rect:
    add w19, w19, #1
    subs w3, w3, #1
    bne single_rect_loop
    
no_rect_hit:
    mov w0, #-1
    
rect_hit_done:
    ldp x19, x20, [sp, #16]
    ldp x29, x30, [sp], #32
    ret

// Get alien bullets array for rendering
// Returns: x0 = pointer to alien bullets array
.global _collision_get_alien_bullets
_collision_get_alien_bullets:
    adrp x0, alien_bullets@PAGE
    add x0, x0, alien_bullets@PAGEOFF
    ret

// Deactivate specific alien bullet
// Parameters: x0 = bullet index
.global _collision_deactivate_alien_bullet
_collision_deactivate_alien_bullet:
    cmp w0, #MAX_ALIEN_BULLETS
    bhs invalid_bullet
    
    adrp x1, alien_bullets@PAGE
    add x1, x1, alien_bullets@PAGEOFF
    
    mov w2, #8
    mul w2, w0, w2
    add x1, x1, x2
    
    strb wzr, [x1, #4]          // active = 0
    
invalid_bullet:
    ret

// Bounding box overlap check (NEON-optimized)
// Parameters: x0 = box1_x, x1 = box1_y, x2 = box1_width, x3 = box1_height,
//            x4 = box2_x, x5 = box2_y, x6 = box2_width, x7 = box2_height
// Returns: x0 = 1 if overlap, 0 if not
_collision_bbox_overlap:
    // Check if box1 is completely to the left of box2
    add w8, w0, w2              // box1_right = box1_x + box1_width
    cmp w8, w4                  // box1_right <= box2_x?
    ble no_overlap
    
    // Check if box1 is completely to the right of box2
    add w8, w4, w6              // box2_right = box2_x + box2_width
    cmp w0, w8                  // box1_x >= box2_right?
    bge no_overlap
    
    // Check if box1 is completely above box2
    add w8, w1, w3              // box1_bottom = box1_y + box1_height
    cmp w8, w5                  // box1_bottom <= box2_y?
    ble no_overlap
    
    // Check if box1 is completely below box2
    add w8, w5, w7              // box2_bottom = box2_y + box2_height
    cmp w1, w8                  // box1_y >= box2_bottom?
    bge no_overlap
    
    // Boxes overlap
    mov w0, #1
    ret
    
no_overlap:
    mov w0, #0
    ret

// Initialize collision system
// Called once at game start to set up collision data
.global _collision_init
_collision_init:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    
    // Clear shield damage masks
    adrp x0, shield_damage_masks@PAGE
    add x0, x0, shield_damage_masks@PAGEOFF
    mov x1, #(SHIELD_WIDTH * SHIELD_HEIGHT * SHIELD_COUNT)
    
clear_shield_loop:
    strb wzr, [x0], #1
    subs x1, x1, #1
    bne clear_shield_loop
    
    // Clear alien bullets
    adrp x0, alien_bullets@PAGE
    add x0, x0, alien_bullets@PAGEOFF
    mov x1, #(MAX_ALIEN_BULLETS * 8)
    
clear_bullets_loop:
    strb wzr, [x0], #1
    subs x1, x1, #1
    bne clear_bullets_loop
    
    ldp x29, x30, [sp], #16
    ret

// Add alien bullet to tracking array
// Parameters: x0 = bullet_x, x1 = bullet_y
// Returns: x0 = 1 if added, 0 if array full
.global _collision_add_alien_bullet
_collision_add_alien_bullet:
    stp x29, x30, [sp, #-32]!
    stp x19, x20, [sp, #16]
    mov x29, sp
    
    mov w19, w0                 // bullet_x
    mov w20, w1                 // bullet_y
    
    // Find empty slot
    adrp x0, alien_bullets@PAGE
    add x0, x0, alien_bullets@PAGEOFF
    mov w2, #0                  // index
    
find_empty_slot:
    ldrb w3, [x0, #4]           // active flag
    cbz w3, found_slot          // Found empty slot
    
    add x0, x0, #8              // Next bullet
    add w2, w2, #1
    cmp w2, #MAX_ALIEN_BULLETS
    blt find_empty_slot
    
    // Array full
    mov w0, #0
    ldp x19, x20, [sp, #16]
    ldp x29, x30, [sp], #32
    ret
    
found_slot:
    // Store bullet data
    strh w19, [x0, #0]          // x position
    strh w20, [x0, #2]          // y position
    mov w3, #1
    strb w3, [x0, #4]           // active = 1
    
    mov w0, #1                  // Success
    ldp x19, x20, [sp, #16]
    ldp x29, x30, [sp], #32
    ret

// Update alien bullet positions
// Called each frame to move bullets down
.global _collision_update_alien_bullets
_collision_update_alien_bullets:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    
    adrp x0, alien_bullets@PAGE
    add x0, x0, alien_bullets@PAGEOFF
    mov w1, #0                  // index
    
update_bullet_loop:
    ldrb w2, [x0, #4]           // active flag
    cbz w2, next_update_bullet
    
    // Update Y position
    ldrh w3, [x0, #2]           // current y
    add w3, w3, #BULLET_SPEED   // Move down
    
    // Check if off screen
    cmp w3, #SCREEN_HEIGHT
    blt store_new_y
    
    // Deactivate bullet
    strb wzr, [x0, #4]
    b next_update_bullet
    
store_new_y:
    strh w3, [x0, #2]
    
next_update_bullet:
    add x0, x0, #8
    add w1, w1, #1
    cmp w1, #MAX_ALIEN_BULLETS
    blt update_bullet_loop
    
    ldp x29, x30, [sp], #16
    ret

// Get shield damage mask for rendering
// Parameters: x0 = shield_index
// Returns: x0 = pointer to damage mask
.global _collision_get_shield_mask
_collision_get_shield_mask:
    cmp w0, #SHIELD_COUNT
    bhs invalid_shield
    
    adrp x1, shield_damage_masks@PAGE
    add x1, x1, shield_damage_masks@PAGEOFF
    
    mov w2, #(SHIELD_WIDTH * SHIELD_HEIGHT)
    mul w2, w0, w2
    add x0, x1, x2
    ret
    
invalid_shield:
    mov x0, #0
    ret

// External function declarations
.extern _aliens_get_array