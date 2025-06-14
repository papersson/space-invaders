.global _render_init
.global _render_frame
.global _render_cleanup
.global _render_sprite
.global _render_sprite_masked
.global _clear_screen
.global _render_text
.global _render_digit

.p2align 4

// Constants
.equ SCREEN_WIDTH, 224
.equ SCREEN_HEIGHT, 256
.equ SCALE_FACTOR, 3
.equ WINDOW_WIDTH, 672    // 224 * 3
.equ WINDOW_HEIGHT, 768   // 256 * 3
.equ BYTES_PER_PIXEL, 4   // BGRA format

// External functions (from render_bridge.c)
.extern _create_window
.extern _present_frame
.extern _cleanup_window
.extern _get_framebuffer

.section __DATA,__data
.p2align 4
framebuffer_ptr: .quad 0
window_ptr: .quad 0
current_buffer: .word 0

// Font data for digits 0-9 (5x7 pixels each)
font_data:
    // '0'
    .byte 0x3E, 0x51, 0x49, 0x45, 0x3E
    // '1'
    .byte 0x00, 0x42, 0x7F, 0x40, 0x00
    // '2'
    .byte 0x42, 0x61, 0x51, 0x49, 0x46
    // '3'
    .byte 0x21, 0x41, 0x45, 0x4B, 0x31
    // '4'
    .byte 0x18, 0x14, 0x12, 0x7F, 0x10
    // '5'
    .byte 0x27, 0x45, 0x45, 0x45, 0x39
    // '6'
    .byte 0x3C, 0x4A, 0x49, 0x49, 0x30
    // '7'
    .byte 0x01, 0x71, 0x09, 0x05, 0x03
    // '8'
    .byte 0x36, 0x49, 0x49, 0x49, 0x36
    // '9'
    .byte 0x06, 0x49, 0x49, 0x29, 0x1E

.section __TEXT,__text
.p2align 4

// render_init: Initialize rendering system
// Returns: 0 on success, -1 on failure
_render_init:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    
    // Create window with scaled dimensions
    mov w0, #WINDOW_WIDTH
    mov w1, #WINDOW_HEIGHT
    bl _create_window
    
    // Check if window creation succeeded
    cbz x0, init_failed
    
    // Store window pointer
    adrp x1, window_ptr@PAGE
    str x0, [x1, window_ptr@PAGEOFF]
    
    // Get framebuffer pointer
    bl _get_framebuffer
    cbz x0, init_failed
    
    // Store framebuffer pointer
    adrp x1, framebuffer_ptr@PAGE
    str x0, [x1, framebuffer_ptr@PAGEOFF]
    
    // Clear screen initially
    bl _clear_screen
    
    mov w0, #0  // Success
    ldp x29, x30, [sp], #16
    ret
    
init_failed:
    mov w0, #-1  // Failure
    ldp x29, x30, [sp], #16
    ret

// render_frame: Present the current frame
_render_frame:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    
    // Get window pointer
    adrp x0, window_ptr@PAGE
    ldr x0, [x0, window_ptr@PAGEOFF]
    
    // Present frame
    bl _present_frame
    
    ldp x29, x30, [sp], #16
    ret

// render_cleanup: Clean up rendering resources
_render_cleanup:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    
    // Get window pointer
    adrp x0, window_ptr@PAGE
    ldr x0, [x0, window_ptr@PAGEOFF]
    
    // Clean up
    bl _cleanup_window
    
    ldp x29, x30, [sp], #16
    ret

// clear_screen: Clear screen to black
_clear_screen:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    
    // Get framebuffer pointer
    adrp x0, framebuffer_ptr@PAGE
    ldr x0, [x0, framebuffer_ptr@PAGEOFF]
    
    // Calculate total size (width * height * bytes_per_pixel)
    mov w1, #WINDOW_WIDTH
    mov w2, #WINDOW_HEIGHT
    mul w1, w1, w2
    mov w2, #BYTES_PER_PIXEL
    mul w1, w1, w2
    
    // Use NEON to clear 16 bytes at a time
    movi v0.16b, #0  // All zeros (black)
    
clear_loop:
    cmp w1, #16
    b.lt clear_remainder
    
    st1 {v0.16b}, [x0], #16
    sub w1, w1, #16
    b clear_loop
    
clear_remainder:
    cbz w1, clear_done
    strb wzr, [x0], #1
    sub w1, w1, #1
    b clear_remainder
    
clear_done:
    ldp x29, x30, [sp], #16
    ret

// render_sprite: Render a sprite at given position
// x0 = sprite data pointer
// w1 = x position (game coordinates)
// w2 = y position (game coordinates)
// w3 = width in pixels
// w4 = height in pixels
_render_sprite:
    stp x29, x30, [sp, #-48]!
    stp x19, x20, [sp, #16]
    stp x21, x22, [sp, #32]
    mov x29, sp
    
    mov x19, x0  // Save sprite data pointer
    mov w20, w1  // Save x position
    mov w21, w2  // Save y position
    mov w22, w3  // Save width
    mov w23, w4  // Save height
    
    // Scale coordinates
    mov w0, #SCALE_FACTOR
    mul w20, w20, w0  // Scaled x
    mul w21, w21, w0  // Scaled y
    
    // Get framebuffer pointer
    adrp x5, framebuffer_ptr@PAGE
    ldr x5, [x5, framebuffer_ptr@PAGEOFF]
    
    // Calculate starting position in framebuffer
    mov w0, #WINDOW_WIDTH
    mul w0, w21, w0      // y * width
    add w0, w0, w20      // + x
    mov w1, #BYTES_PER_PIXEL
    mul w0, w0, w1       // * bytes per pixel
    add x5, x5, x0       // Add to framebuffer base
    
    // Prepare white color in NEON register (BGRA format)
    mov w0, #0xFFFFFFFF
    dup v1.4s, w0
    
    mov w24, #0  // Current row
    
sprite_row_loop:
    cmp w24, w23
    b.ge sprite_done
    
    mov w25, #0  // Current column
    mov x6, x5   // Current framebuffer position
    
sprite_col_loop:
    cmp w25, w22
    b.ge sprite_next_row
    
    // Check if pixel is set in sprite data
    mov w0, w25
    lsr w0, w0, #3       // Byte offset (x / 8)
    ldrb w1, [x19, x0]   // Load sprite byte
    
    and w2, w25, #7      // Bit position (x % 8)
    mov w3, #7
    sub w2, w3, w2       // Reverse bit order
    lsr w1, w1, w2       // Shift to get bit
    and w1, w1, #1       // Isolate bit
    
    cbz w1, sprite_skip_pixel
    
    // Draw scaled pixel (3x3 block)
    mov w26, #0  // Scale y
scale_y_loop:
    cmp w26, #SCALE_FACTOR
    b.ge sprite_next_pixel
    
    mov x7, x6
    mov w0, #WINDOW_WIDTH
    mov w1, #BYTES_PER_PIXEL
    mul w0, w0, w1
    mul w1, w26, w0
    add x7, x7, x1
    
    // Draw 3 pixels horizontally using NEON
    st1 {v1.s}[0], [x7], #4
    st1 {v1.s}[0], [x7], #4
    st1 {v1.s}[0], [x7], #4
    
    add w26, w26, #1
    b scale_y_loop
    
sprite_skip_pixel:
sprite_next_pixel:
    add w25, w25, #1
    add x6, x6, #(SCALE_FACTOR * BYTES_PER_PIXEL)
    b sprite_col_loop
    
sprite_next_row:
    add w24, w24, #1
    add x19, x19, x22, lsr #3  // Move to next row in sprite data
    
    // Move framebuffer pointer to next row
    mov w0, #WINDOW_WIDTH
    mov w1, #BYTES_PER_PIXEL
    mul w0, w0, w1
    mov w1, #SCALE_FACTOR
    mul w0, w0, w1
    add x5, x5, x0
    
    b sprite_row_loop
    
sprite_done:
    ldp x19, x20, [sp, #16]
    ldp x21, x22, [sp, #32]
    ldp x29, x30, [sp], #48
    ret

// render_sprite_masked: Render sprite with transparency
// Same parameters as render_sprite
// x5 = mask data pointer
_render_sprite_masked:
    stp x29, x30, [sp, #-64]!
    stp x19, x20, [sp, #16]
    stp x21, x22, [sp, #32]
    stp x23, x24, [sp, #48]
    mov x29, sp
    
    mov x19, x0  // Save sprite data pointer
    mov x20, x5  // Save mask data pointer
    mov w21, w1  // Save x position
    mov w22, w2  // Save y position
    mov w23, w3  // Save width
    mov w24, w4  // Save height
    
    // Scale coordinates
    mov w0, #SCALE_FACTOR
    mul w21, w21, w0  // Scaled x
    mul w22, w22, w0  // Scaled y
    
    // Get framebuffer pointer
    adrp x5, framebuffer_ptr@PAGE
    ldr x5, [x5, framebuffer_ptr@PAGEOFF]
    
    // Calculate starting position
    mov w0, #WINDOW_WIDTH
    mul w0, w22, w0
    add w0, w0, w21
    mov w1, #BYTES_PER_PIXEL
    mul w0, w0, w1
    add x5, x5, x0
    
    // Prepare colors
    mov w0, #0xFFFFFFFF
    dup v1.4s, w0        // White
    movi v2.4s, #0       // Black (transparent)
    
    mov w25, #0  // Current row
    
masked_row_loop:
    cmp w25, w24
    b.ge masked_done
    
    mov w26, #0  // Current column
    mov x6, x5   // Current framebuffer position
    
masked_col_loop:
    cmp w26, w23
    b.ge masked_next_row
    
    // Get bit offset and position
    mov w0, w26
    lsr w0, w0, #3       // Byte offset
    and w2, w26, #7      // Bit position
    mov w3, #7
    sub w2, w3, w2       // Reverse bit order
    
    // Check mask bit
    ldrb w1, [x20, x0]
    lsr w1, w1, w2
    and w1, w1, #1
    cbz w1, masked_skip_pixel  // Skip if mask bit is 0
    
    // Check sprite bit
    ldrb w1, [x19, x0]
    lsr w1, w1, w2
    and w1, w1, #1
    
    // Select color based on sprite bit
    cmp w1, #1
    csel w27, w0, wzr, eq  // Choose white or black
    
    // Draw scaled pixel
    mov w28, #0  // Scale y
masked_scale_y_loop:
    cmp w28, #SCALE_FACTOR
    b.ge masked_next_pixel
    
    mov x7, x6
    mov w0, #WINDOW_WIDTH
    mov w1, #BYTES_PER_PIXEL
    mul w0, w0, w1
    mul w1, w28, w0
    add x7, x7, x1
    
    // Draw 3 pixels horizontally
    cmp w27, #0
    b.eq masked_draw_black
    
    st1 {v1.s}[0], [x7], #4
    st1 {v1.s}[0], [x7], #4
    st1 {v1.s}[0], [x7], #4
    b masked_scale_y_continue
    
masked_draw_black:
    st1 {v2.s}[0], [x7], #4
    st1 {v2.s}[0], [x7], #4
    st1 {v2.s}[0], [x7], #4
    
masked_scale_y_continue:
    add w28, w28, #1
    b masked_scale_y_loop
    
masked_skip_pixel:
masked_next_pixel:
    add w26, w26, #1
    add x6, x6, #(SCALE_FACTOR * BYTES_PER_PIXEL)
    b masked_col_loop
    
masked_next_row:
    add w25, w25, #1
    mov w0, w23
    lsr w0, w0, #3
    add x19, x19, x0  // Move to next row in sprite data
    add x20, x20, x0  // Move to next row in mask data
    
    // Move framebuffer pointer
    mov w0, #WINDOW_WIDTH
    mov w1, #BYTES_PER_PIXEL
    mul w0, w0, w1
    mov w1, #SCALE_FACTOR
    mul w0, w0, w1
    add x5, x5, x0
    
    b masked_row_loop
    
masked_done:
    ldp x23, x24, [sp, #48]
    ldp x21, x22, [sp, #32]
    ldp x19, x20, [sp, #16]
    ldp x29, x30, [sp], #64
    ret

// render_text: Render text string at position
// x0 = string pointer (null-terminated)
// w1 = x position
// w2 = y position
_render_text:
    stp x29, x30, [sp, #-32]!
    stp x19, x20, [sp, #16]
    mov x29, sp
    
    mov x19, x0  // Save string pointer
    mov w20, w1  // Save x position
    mov w21, w2  // Save y position
    
text_loop:
    ldrb w0, [x19], #1
    cbz w0, text_done
    
    // Check if it's a digit (0-9)
    cmp w0, #'0'
    b.lt text_loop
    cmp w0, #'9'
    b.gt text_loop
    
    // Render digit
    sub w0, w0, #'0'  // Convert to digit index
    mov w1, w20
    mov w2, w21
    bl _render_digit
    
    // Move x position for next character
    add w20, w20, #6  // 5 pixels + 1 space
    
    b text_loop
    
text_done:
    ldp x19, x20, [sp, #16]
    ldp x29, x30, [sp], #32
    ret

// render_digit: Render a single digit
// w0 = digit (0-9)
// w1 = x position
// w2 = y position
_render_digit:
    stp x29, x30, [sp, #-32]!
    stp x19, x20, [sp, #16]
    mov x29, sp
    
    mov w19, w1  // Save x position
    mov w20, w2  // Save y position
    
    // Get font data address for digit
    adrp x3, font_data@PAGE
    add x3, x3, font_data@PAGEOFF
    mov w4, #5   // 5 bytes per digit
    mul w0, w0, w4
    add x3, x3, x0
    
    // Scale coordinates
    mov w0, #SCALE_FACTOR
    mul w19, w19, w0
    mul w20, w20, w0
    
    // Get framebuffer
    adrp x5, framebuffer_ptr@PAGE
    ldr x5, [x5, framebuffer_ptr@PAGEOFF]
    
    // Calculate starting position
    mov w0, #WINDOW_WIDTH
    mul w0, w20, w0
    add w0, w0, w19
    mov w1, #BYTES_PER_PIXEL
    mul w0, w0, w1
    add x5, x5, x0
    
    // Prepare white color
    mov w0, #0xFFFFFFFF
    dup v1.4s, w0
    
    // Render 5x7 character
    mov w21, #0  // Column counter
    
digit_col_loop:
    cmp w21, #5
    b.ge digit_done
    
    ldrb w0, [x3], #1  // Load column data
    mov w22, #0        // Row counter
    mov x6, x5         // Current position
    
digit_row_loop:
    cmp w22, #7
    b.ge digit_next_col
    
    // Check if bit is set
    and w1, w0, #1
    cbz w1, digit_skip_pixel
    
    // Draw scaled pixel (3x3)
    mov w23, #0  // Scale y
digit_scale_y_loop:
    cmp w23, #SCALE_FACTOR
    b.ge digit_next_pixel
    
    mov x7, x6
    mov w1, #WINDOW_WIDTH
    mov w2, #BYTES_PER_PIXEL
    mul w1, w1, w2
    mul w2, w23, w1
    add x7, x7, x2
    
    // Draw 3 pixels
    st1 {v1.s}[0], [x7], #4
    st1 {v1.s}[0], [x7], #4
    st1 {v1.s}[0], [x7], #4
    
    add w23, w23, #1
    b digit_scale_y_loop
    
digit_skip_pixel:
digit_next_pixel:
    lsr w0, w0, #1  // Next bit
    add w22, w22, #1
    
    // Move down one scaled row
    mov w1, #WINDOW_WIDTH
    mov w2, #BYTES_PER_PIXEL
    mul w1, w1, w2
    mov w2, #SCALE_FACTOR
    mul w1, w1, w2
    add x6, x6, x1
    
    b digit_row_loop
    
digit_next_col:
    add w21, w21, #1
    add x5, x5, #(SCALE_FACTOR * BYTES_PER_PIXEL)
    b digit_col_loop
    
digit_done:
    ldp x19, x20, [sp, #16]
    ldp x29, x30, [sp], #32
    ret