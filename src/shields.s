// shields.s - Destructible shield barriers for Space Invaders
// ARM64 Assembly for Apple Silicon
// Implements pixel-perfect destruction with efficient bitmap storage

.include "constants.inc"
.include "macros.inc"

.section __TEXT,__text
.p2align 4

// Shield constants
.equ SHIELD_SPACING,        ((SCREEN_WIDTH - (SHIELD_COUNT * SHIELD_WIDTH)) / (SHIELD_COUNT + 1))
.equ SHIELD_Y_POS,          (SCREEN_HEIGHT - 80)   // Position from top
.equ SHIELD_BITMAP_SIZE,    (SHIELD_WIDTH * SHIELD_HEIGHT / 8 + 1)  // Bits to bytes, rounded up
.equ SHIELD_DAMAGE_SMALL,   3    // Small damage radius (bullets)
.equ SHIELD_DAMAGE_LARGE,   5    // Large damage radius (alien contact)

// Shield structure offsets
.equ SHIELD_X_POS,          0    // X position (word)
.equ SHIELD_Y_POS_OFF,      4    // Y position (word)
.equ SHIELD_ACTIVE,         8    // Active flag (word)
.equ SHIELD_DAMAGE_BITMAP,  16   // Start of damage bitmap (aligned to 16)
.equ SHIELD_STRUCT_SIZE,    (16 + SHIELD_BITMAP_SIZE + 15) & ~15  // Align to 16 bytes

// Shield data section
.section __DATA,__data
.p2align 4  // Align to 16 bytes for NEON

// Shield array - 4 shields with position and damage data
shield_array:
    .rept SHIELD_COUNT
    .word 0                     // x_position
    .word SHIELD_Y_POS         // y_position
    .word 1                     // active (1 = active, 0 = destroyed)
    .word 0                     // padding for alignment
    .space SHIELD_BITMAP_SIZE   // damage bitmap
    .balign 16                  // Ensure each shield is 16-byte aligned
    .endr

// Original shield pattern (22x16 pixels)
// This represents the intact shield shape
shield_pattern:
    // Top section - thick protective layer
    .byte 0b00111111, 0b11111111, 0b11110000  // Row 0
    .byte 0b01111111, 0b11111111, 0b11111000  // Row 1
    .byte 0b11111111, 0b11111111, 0b11111100  // Row 2
    .byte 0b11111111, 0b11111111, 0b11111100  // Row 3
    .byte 0b11111111, 0b11111111, 0b11111100  // Row 4
    .byte 0b11111111, 0b11111111, 0b11111100  // Row 5
    // Middle section with gap
    .byte 0b11111111, 0b11111111, 0b11111100  // Row 6
    .byte 0b11111111, 0b11111111, 0b11111100  // Row 7
    .byte 0b11111111, 0b11111111, 0b11111100  // Row 8
    .byte 0b11111111, 0b11111111, 0b11111100  // Row 9
    // Bottom section with entrance
    .byte 0b11111111, 0b00000001, 0b11111100  // Row 10
    .byte 0b11111110, 0b00000000, 0b11111100  // Row 11
    .byte 0b11111100, 0b00000000, 0b01111100  // Row 12
    .byte 0b11111100, 0b00000000, 0b01111100  // Row 13
    .byte 0b11111100, 0b00000000, 0b01111100  // Row 14
    .byte 0b11111100, 0b00000000, 0b01111100  // Row 15

// Erosion patterns for different damage types
erosion_pattern_small:
    .byte 0b00100000  // 3x3 pattern
    .byte 0b01110000
    .byte 0b00100000

erosion_pattern_large:
    .byte 0b00100000  // 5x5 pattern
    .byte 0b01110000
    .byte 0b11111000
    .byte 0b01110000
    .byte 0b00100000

.section __TEXT,__text

// Initialize shields at starting positions
// No parameters
// Returns: nothing
GLOBAL_FUNC shields_init
    FUNC_PROLOGUE_SAVE 4
    
    // x19 = shield array pointer
    // x20 = current shield index
    // x21 = x position accumulator
    // x22 = shield structure pointer
    
    LOAD_ADDR x19, shield_array
    mov x20, #0                         // Shield index
    mov x21, #SHIELD_SPACING           // Initial X position
    
init_shield_loop:
    // Calculate shield structure offset
    mov x0, #SHIELD_STRUCT_SIZE
    mul x0, x0, x20
    add x22, x19, x0
    
    // Set X position
    str w21, [x22, #SHIELD_X_POS]
    
    // Set Y position
    mov w0, #SHIELD_Y_POS
    str w0, [x22, #SHIELD_Y_POS_OFF]
    
    // Set active flag
    mov w0, #1
    str w0, [x22, #SHIELD_ACTIVE]
    
    // Initialize damage bitmap to all zeros (no damage)
    add x0, x22, #SHIELD_DAMAGE_BITMAP
    mov x1, #0
    mov x2, #SHIELD_BITMAP_SIZE
    bl memset_aligned
    
    // Update X position for next shield
    add w21, w21, #SHIELD_WIDTH
    add w21, w21, #SHIELD_SPACING
    
    // Next shield
    add x20, x20, #1
    cmp x20, #SHIELD_COUNT
    blt init_shield_loop
    
    FUNC_EPILOGUE_RESTORE 4

// Reset all shields to undamaged state
// No parameters
// Returns: nothing
GLOBAL_FUNC shields_reset
    FUNC_PROLOGUE_SAVE 2
    
    LOAD_ADDR x19, shield_array
    mov x20, #0
    
reset_shield_loop:
    // Calculate shield structure offset
    mov x0, #SHIELD_STRUCT_SIZE
    mul x0, x0, x20
    add x0, x19, x0
    
    // Set active flag
    mov w1, #1
    str w1, [x0, #SHIELD_ACTIVE]
    
    // Clear damage bitmap
    add x0, x0, #SHIELD_DAMAGE_BITMAP
    mov x1, #0
    mov x2, #SHIELD_BITMAP_SIZE
    bl memset_aligned
    
    // Next shield
    add x20, x20, #1
    cmp x20, #SHIELD_COUNT
    blt reset_shield_loop
    
    FUNC_EPILOGUE_RESTORE 2

// Apply damage at specific pixel
// x0 = world X coordinate
// x1 = world Y coordinate
// x2 = damage type (0 = small, 1 = large)
// Returns: x0 = 1 if hit shield, 0 if not
GLOBAL_FUNC shields_damage_at
    FUNC_PROLOGUE_SAVE 6
    
    // x19 = X coordinate
    // x20 = Y coordinate
    // x21 = damage type
    // x22 = shield array pointer
    // x23 = current shield index
    // x24 = shield structure pointer
    
    mov x19, x0
    mov x20, x1
    mov x21, x2
    LOAD_ADDR x22, shield_array
    mov x23, #0
    
check_shield_loop:
    // Calculate shield structure offset
    mov x0, #SHIELD_STRUCT_SIZE
    mul x0, x0, x23
    add x24, x22, x0
    
    // Check if shield is active
    ldr w0, [x24, #SHIELD_ACTIVE]
    cbz w0, next_shield
    
    // Check if coordinates are within shield bounds
    ldr w0, [x24, #SHIELD_X_POS]
    sub w1, w19, w0                    // Relative X
    cmp w1, #0
    blt next_shield
    cmp w1, #SHIELD_WIDTH
    bge next_shield
    
    ldr w0, [x24, #SHIELD_Y_POS_OFF]
    sub w2, w20, w0                    // Relative Y
    cmp w2, #0
    blt next_shield
    cmp w2, #SHIELD_HEIGHT
    bge next_shield
    
    // Hit detected - apply damage
    mov x0, x24                        // Shield pointer
    mov x3, x21                        // Damage type
    bl apply_damage_to_shield
    
    mov x0, #1                         // Return hit
    FUNC_EPILOGUE_RESTORE 6
    
next_shield:
    add x23, x23, #1
    cmp x23, #SHIELD_COUNT
    blt check_shield_loop
    
    mov x0, #0                         // Return no hit
    FUNC_EPILOGUE_RESTORE 6

// Apply damage to a specific shield
// x0 = shield structure pointer
// x1 = relative X coordinate
// x2 = relative Y coordinate
// x3 = damage type (0 = small, 1 = large)
// Returns: nothing
LOCAL_FUNC apply_damage_to_shield
    FUNC_PROLOGUE_SAVE 6
    
    // x19 = shield pointer
    // x20 = relative X
    // x21 = relative Y
    // x22 = damage radius
    
    mov x19, x0
    mov x20, x1
    mov x21, x2
    
    // Determine damage radius
    cbz x3, small_damage
    mov x22, #SHIELD_DAMAGE_LARGE
    b apply_erosion
small_damage:
    mov x22, #SHIELD_DAMAGE_SMALL
    
apply_erosion:
    // Apply circular erosion pattern
    mov x23, x22
    neg x23, x23                       // Start at -radius
    
erosion_y_loop:
    mov x24, x22
    neg x24, x24                       // Start at -radius
    
erosion_x_loop:
    // Calculate actual coordinates
    add w0, w20, w24                   // X + dx
    add w1, w21, w23                   // Y + dy
    
    // Check bounds
    cmp w0, #0
    blt skip_pixel
    cmp w0, #SHIELD_WIDTH
    bge skip_pixel
    cmp w1, #0
    blt skip_pixel
    cmp w1, #SHIELD_HEIGHT
    bge skip_pixel
    
    // Check if within circular radius
    mul w2, w24, w24                   // dx²
    mul w3, w23, w23                   // dy²
    add w2, w2, w3                     // dx² + dy²
    mul w3, w22, w22                   // radius²
    cmp w2, w3
    bgt skip_pixel
    
    // Set damage bit
    mov x2, x19
    bl set_damage_bit
    
skip_pixel:
    add x24, x24, #1
    cmp x24, x22
    ble erosion_x_loop
    
    add x23, x23, #1
    cmp x23, x22
    ble erosion_y_loop
    
    FUNC_EPILOGUE_RESTORE 6

// Set damage bit for a pixel
// x0 = X coordinate (0-21)
// x1 = Y coordinate (0-15)
// x2 = shield structure pointer
// Returns: nothing
LOCAL_FUNC set_damage_bit
    FUNC_PROLOGUE
    
    // Calculate bit position: bit = y * SHIELD_WIDTH + x
    mov w3, #SHIELD_WIDTH
    mul w3, w1, w3
    add w3, w3, w0
    
    // Calculate byte offset and bit mask
    lsr w4, w3, #3                     // Byte offset = bit / 8
    and w5, w3, #7                     // Bit position = bit % 8
    mov w6, #1
    lsl w6, w6, w5                     // Bit mask
    
    // Set the bit in damage bitmap
    add x2, x2, #SHIELD_DAMAGE_BITMAP
    ldrb w7, [x2, x4]
    orr w7, w7, w6
    strb w7, [x2, x4]
    
    FUNC_EPILOGUE

// Check if pixel is solid (not damaged)
// x0 = world X coordinate
// x1 = world Y coordinate
// Returns: x0 = 1 if solid, 0 if damaged or not on shield
GLOBAL_FUNC shields_check_pixel
    FUNC_PROLOGUE_SAVE 6
    
    // x19 = X coordinate
    // x20 = Y coordinate
    // x21 = shield array pointer
    // x22 = current shield index
    // x23 = shield structure pointer
    
    mov x19, x0
    mov x20, x1
    LOAD_ADDR x21, shield_array
    mov x22, #0
    
check_pixel_shield_loop:
    // Calculate shield structure offset
    mov x0, #SHIELD_STRUCT_SIZE
    mul x0, x0, x22
    add x23, x21, x0
    
    // Check if shield is active
    ldr w0, [x23, #SHIELD_ACTIVE]
    cbz w0, next_shield_pixel
    
    // Check if coordinates are within shield bounds
    ldr w0, [x23, #SHIELD_X_POS]
    sub w24, w19, w0                   // Relative X
    cmp w24, #0
    blt next_shield_pixel
    cmp w24, #SHIELD_WIDTH
    bge next_shield_pixel
    
    ldr w0, [x23, #SHIELD_Y_POS_OFF]
    sub w25, w20, w0                   // Relative Y
    cmp w25, #0
    blt next_shield_pixel
    cmp w25, #SHIELD_HEIGHT
    bge next_shield_pixel
    
    // Check if pixel exists in original pattern
    LOAD_ADDR x0, shield_pattern
    mov w1, #SHIELD_WIDTH
    add w1, w1, #7
    lsr w1, w1, #3                     // Bytes per row
    mul w1, w25, w1                    // Row offset
    add x0, x0, x1
    lsr w1, w24, #3                    // Byte within row
    ldrb w0, [x0, x1]
    and w1, w24, #7                    // Bit within byte
    lsr w0, w0, w1
    and w0, w0, #1
    cbz w0, pixel_not_solid            // Not in original pattern
    
    // Check if pixel is damaged
    add x0, x23, #SHIELD_DAMAGE_BITMAP
    mov w1, #SHIELD_WIDTH
    mul w1, w25, w1
    add w1, w1, w24                    // Bit position
    lsr w2, w1, #3                     // Byte offset
    and w3, w1, #7                     // Bit position
    ldrb w0, [x0, x2]
    lsr w0, w0, w3
    and w0, w0, #1
    eor w0, w0, #1                     // Invert: 1 if not damaged
    
    FUNC_EPILOGUE_RESTORE 6
    
next_shield_pixel:
    add x22, x22, #1
    cmp x22, #SHIELD_COUNT
    blt check_pixel_shield_loop
    
pixel_not_solid:
    mov x0, #0
    FUNC_EPILOGUE_RESTORE 6

// Get shield pixel data for rendering
// x0 = shield index (0-3)
// x1 = destination buffer pointer
// Returns: x0 = 1 if shield active, 0 if destroyed
GLOBAL_FUNC shields_render
    FUNC_PROLOGUE_SAVE 6
    
    // x19 = shield structure pointer
    // x20 = destination buffer
    // x21 = pattern pointer
    // x22 = damage bitmap pointer
    // x23 = current row
    // x24 = current column
    
    // Calculate shield structure offset
    mov x2, #SHIELD_STRUCT_SIZE
    mul x2, x0, x2
    LOAD_ADDR x19, shield_array
    add x19, x19, x2
    
    // Check if shield is active
    ldr w0, [x19, #SHIELD_ACTIVE]
    cbz w0, shield_inactive
    
    mov x20, x1
    LOAD_ADDR x21, shield_pattern
    add x22, x19, #SHIELD_DAMAGE_BITMAP
    mov x23, #0                        // Row counter
    
render_row_loop:
    mov x24, #0                        // Column counter
    
render_col_loop:
    // Calculate bit position
    mov w0, #SHIELD_WIDTH
    mul w0, w23, w0
    add w0, w0, w24
    
    // Check original pattern
    lsr w1, w0, #3                     // Byte offset
    and w2, w0, #7                     // Bit position
    ldrb w3, [x21, x1]
    lsr w3, w3, w2
    and w3, w3, #1
    cbz w3, pixel_empty
    
    // Check damage bitmap
    ldrb w3, [x22, x1]
    lsr w3, w3, w2
    and w3, w3, #1
    cbnz w3, pixel_empty
    
    // Pixel is solid - write to buffer
    mov w3, #1
    b write_pixel
    
pixel_empty:
    mov w3, #0
    
write_pixel:
    strb w3, [x20], #1
    
    add x24, x24, #1
    cmp x24, #SHIELD_WIDTH
    blt render_col_loop
    
    add x23, x23, #1
    cmp x23, #SHIELD_HEIGHT
    blt render_row_loop
    
    mov x0, #1                         // Shield is active
    FUNC_EPILOGUE_RESTORE 6
    
shield_inactive:
    mov x0, #0
    FUNC_EPILOGUE_RESTORE 6

// Get shield X,Y position
// x0 = shield index (0-3)
// Returns: x0 = X position, x1 = Y position
GLOBAL_FUNC shields_get_position
    FUNC_PROLOGUE
    
    // Calculate shield structure offset
    mov x1, #SHIELD_STRUCT_SIZE
    mul x1, x0, x1
    LOAD_ADDR x2, shield_array
    add x2, x2, x1
    
    // Load positions
    ldr w0, [x2, #SHIELD_X_POS]
    ldr w1, [x2, #SHIELD_Y_POS_OFF]
    
    FUNC_EPILOGUE

// Erode larger area (for explosions)
// x0 = world X coordinate (center)
// x1 = world Y coordinate (center)
// x2 = radius
// Returns: nothing
GLOBAL_FUNC shields_erode_area
    FUNC_PROLOGUE_SAVE 6
    
    // x19 = center X
    // x20 = center Y
    // x21 = radius
    // x22 = shield array pointer
    // x23 = current shield index
    
    mov x19, x0
    mov x20, x1
    mov x21, x2
    LOAD_ADDR x22, shield_array
    mov x23, #0
    
erode_shield_loop:
    // Calculate shield structure offset
    mov x0, #SHIELD_STRUCT_SIZE
    mul x0, x0, x23
    add x24, x22, x0
    
    // Check if shield is active
    ldr w0, [x24, #SHIELD_ACTIVE]
    cbz w0, next_shield_erode
    
    // Check if explosion overlaps shield
    ldr w0, [x24, #SHIELD_X_POS]
    ldr w1, [x24, #SHIELD_Y_POS_OFF]
    
    // Calculate distance to shield corners
    sub w2, w19, w0
    cmp w2, w21, lsl #1               // Check if too far left
    blt might_overlap
    sub w2, w0, w19
    add w2, w2, #SHIELD_WIDTH
    cmp w2, w21, lsl #1               // Check if too far right
    bge next_shield_erode
    
might_overlap:
    sub w2, w20, w1
    cmp w2, w21, lsl #1               // Check if too far up
    blt apply_area_damage
    sub w2, w1, w20
    add w2, w2, #SHIELD_HEIGHT
    cmp w2, w21, lsl #1               // Check if too far down
    bge next_shield_erode
    
apply_area_damage:
    // Apply damage to all pixels within radius
    mov x0, x24
    mov x1, x19
    mov x2, x20
    mov x3, x21
    bl apply_explosion_damage
    
next_shield_erode:
    add x23, x23, #1
    cmp x23, #SHIELD_COUNT
    blt erode_shield_loop
    
    FUNC_EPILOGUE_RESTORE 6

// Apply explosion damage to shield
// x0 = shield structure pointer
// x1 = explosion center X (world)
// x2 = explosion center Y (world)
// x3 = explosion radius
// Returns: nothing
LOCAL_FUNC apply_explosion_damage
    FUNC_PROLOGUE_SAVE 6
    
    // x19 = shield pointer
    // x20 = shield X position
    // x21 = shield Y position
    // x22 = explosion radius
    // x23 = current Y offset
    // x24 = current X offset
    
    mov x19, x0
    ldr w20, [x0, #SHIELD_X_POS]
    ldr w21, [x0, #SHIELD_Y_POS_OFF]
    mov x22, x3
    
    // Convert explosion center to shield-relative coordinates
    sub w1, w1, w20
    sub w2, w2, w21
    
    // Iterate through affected area
    mov x23, x22
    neg x23, x23
    
explosion_y_loop:
    mov x24, x22
    neg x24, x24
    
explosion_x_loop:
    // Calculate actual coordinates
    add w0, w1, w24                    // X + dx
    add w3, w2, w23                    // Y + dy
    
    // Check bounds
    cmp w0, #0
    blt skip_explosion_pixel
    cmp w0, #SHIELD_WIDTH
    bge skip_explosion_pixel
    cmp w3, #0
    blt skip_explosion_pixel
    cmp w3, #SHIELD_HEIGHT
    bge skip_explosion_pixel
    
    // Check if within circular radius
    mul w4, w24, w24                   // dx²
    mul w5, w23, w23                   // dy²
    add w4, w4, w5                     // dx² + dy²
    mul w5, w22, w22                   // radius²
    cmp w4, w5
    bgt skip_explosion_pixel
    
    // Set damage bit
    mov x1, x3
    mov x2, x19
    bl set_damage_bit
    
skip_explosion_pixel:
    add x24, x24, #1
    cmp x24, x22
    ble explosion_x_loop
    
    add x23, x23, #1
    cmp x23, x22
    ble explosion_y_loop
    
    FUNC_EPILOGUE_RESTORE 6

// Aligned memset for damage bitmaps
// x0 = destination
// x1 = value (byte)
// x2 = count
// Returns: nothing
LOCAL_FUNC memset_aligned
    FUNC_PROLOGUE
    
    // Use NEON for efficient clearing
    dup v0.16b, w1                     // Duplicate byte to all lanes
    
    // Process 16 bytes at a time
memset_loop:
    cmp x2, #16
    blt memset_remainder
    
    str q0, [x0], #16
    sub x2, x2, #16
    b memset_loop
    
memset_remainder:
    // Handle remaining bytes
    cbz x2, memset_done
memset_byte_loop:
    strb w1, [x0], #1
    subs x2, x2, #1
    bne memset_byte_loop
    
memset_done:
    FUNC_EPILOGUE

// Get shield damage percentage
// x0 = shield index (0-3)
// Returns: x0 = damage percentage (0-100)
GLOBAL_FUNC shields_get_damage_percent
    FUNC_PROLOGUE_SAVE 4
    
    // Calculate shield structure offset
    mov x1, #SHIELD_STRUCT_SIZE
    mul x1, x0, x1
    LOAD_ADDR x19, shield_array
    add x19, x19, x1
    
    // Check if shield is active
    ldr w0, [x19, #SHIELD_ACTIVE]
    cbz w0, shield_destroyed
    
    // Count damaged pixels
    add x20, x19, #SHIELD_DAMAGE_BITMAP
    mov x21, #0                        // Damage count
    mov x22, #0                        // Byte counter
    
count_damage_loop:
    cmp x22, #SHIELD_BITMAP_SIZE
    bge calculate_percentage
    
    ldrb w0, [x20, x22]
    
    // Count set bits using bit manipulation
    mov w1, w0
    lsr w2, w1, #1
    mov w3, #0x55
    and w2, w2, w3
    sub w1, w1, w2
    
    mov w3, #0x33
    and w2, w1, w3
    lsr w1, w1, #2
    and w1, w1, w3
    add w1, w1, w2
    
    add w1, w1, w1, lsr #4
    and w1, w1, #0x0F
    
    add x21, x21, x1
    add x22, x22, #1
    b count_damage_loop
    
calculate_percentage:
    // Calculate percentage: (damaged * 100) / total_pixels
    mov w0, #100
    mul x21, x21, x0
    mov w0, #SHIELD_WIDTH
    mov w1, #SHIELD_HEIGHT
    mul w0, w0, w1
    udiv x0, x21, x0
    
    FUNC_EPILOGUE_RESTORE 4
    
shield_destroyed:
    mov x0, #100
    FUNC_EPILOGUE_RESTORE 4

// Check if shield should be destroyed (too damaged)
// x0 = shield index (0-3)
// Returns: nothing
GLOBAL_FUNC shields_check_destruction
    FUNC_PROLOGUE_SAVE 2
    
    mov x19, x0
    bl shields_get_damage_percent
    
    // Destroy shield if more than 80% damaged
    cmp x0, #80
    ble not_destroyed
    
    // Mark shield as destroyed
    mov x0, #SHIELD_STRUCT_SIZE
    mul x0, x19, x0
    LOAD_ADDR x1, shield_array
    add x1, x1, x0
    str wzr, [x1, #SHIELD_ACTIVE]
    
not_destroyed:
    FUNC_EPILOGUE_RESTORE 2