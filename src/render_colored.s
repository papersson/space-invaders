// render_colored.s - Colored sprite rendering functions
.section __TEXT,__text
.p2align 2

#include "constants.inc"

// External function
.extern _get_framebuffer

// render_sprite_colored: Render a sprite with specified color
// Parameters:
//   x0 = sprite data pointer (bitmap format)
//   w1 = x position
//   w2 = y position  
//   w3 = width
//   w4 = height
//   w5 = color (RGBA format)
.global _render_sprite_colored
_render_sprite_colored:
    stp x29, x30, [sp, #-64]!
    stp x19, x20, [sp, #16]
    stp x21, x22, [sp, #32]
    stp x23, x24, [sp, #48]
    mov x29, sp
    
    mov x19, x0  // Save sprite data pointer
    mov w20, w1  // Save x position
    mov w21, w2  // Save y position
    mov w22, w3  // Save width
    mov w23, w4  // Save height
    
    // Scale coordinates
    mov w0, #3              // SCALE_FACTOR = 3
    mul w20, w20, w0  // Scaled x
    mul w21, w21, w0  // Scaled y
    
    // Get framebuffer pointer from render system
    stp x19, x20, [sp, #-16]!
    stp x21, x22, [sp, #-16]!
    stp x23, x24, [sp, #-16]!
    stp x25, x26, [sp, #-16]!
    
    // Save parameters
    mov x19, x0
    mov w20, w1
    mov w21, w2
    mov w22, w3
    mov w23, w4
    mov w24, w5
    
    // Get framebuffer
    bl _get_framebuffer
    mov x6, x0
    
    // Restore parameters
    mov x0, x19
    mov w1, w20
    mov w2, w21
    mov w3, w22
    mov w4, w23
    mov w5, w24
    
    ldp x25, x26, [sp], #16
    ldp x23, x24, [sp], #16
    ldp x21, x22, [sp], #16
    ldp x19, x20, [sp], #16
    
    // Calculate starting position in framebuffer
    mov w0, #672            // WINDOW_WIDTH = 224 * 3
    mul w0, w21, w0      // y * width
    add w0, w0, w20      // + x
    mov w1, #4              // BYTES_PER_PIXEL
    mul w0, w0, w1       // * bytes per pixel
    add x6, x6, x0       // Add to framebuffer base
    
    // Prepare color in NEON register
    dup v1.4s, w5        // Duplicate color to all lanes
    
    mov w24, #0  // Current row
    
sprite_row_loop_colored:
    cmp w24, w23
    b.ge sprite_done_colored
    
    mov w25, #0  // Current column
    mov x7, x6   // Current framebuffer position
    
sprite_col_loop_colored:
    cmp w25, w22
    b.ge sprite_next_row_colored
    
    // Check if pixel is set in sprite data
    mov w0, w25
    lsr w0, w0, #3       // Byte offset (x / 8)
    ldrb w1, [x19, x0]   // Load sprite byte
    
    and w2, w25, #7      // Bit position (x % 8)
    mov w3, #7
    sub w2, w3, w2       // Reverse bit order
    lsr w1, w1, w2       // Shift to get bit
    and w1, w1, #1       // Isolate bit
    
    cbz w1, sprite_skip_pixel_colored
    
    // Draw scaled pixel (3x3 block)
    mov w26, #0  // Scale y
scale_y_loop_colored:
    cmp w26, #3             // SCALE_FACTOR
    b.ge sprite_next_pixel_colored
    
    mov x8, x7
    mov w0, #672            // WINDOW_WIDTH
    mov w1, #4              // BYTES_PER_PIXEL
    mul w0, w0, w1
    mul w1, w26, w0
    add x8, x8, x1
    
    // Draw 3 pixels horizontally
    st1 {v1.s}[0], [x8], #4
    st1 {v1.s}[0], [x8], #4
    st1 {v1.s}[0], [x8], #4
    
    add w26, w26, #1
    b scale_y_loop_colored
    
sprite_skip_pixel_colored:
sprite_next_pixel_colored:
    add w25, w25, #1
    add x7, x7, #12         // SCALE_FACTOR * BYTES_PER_PIXEL = 3 * 4
    b sprite_col_loop_colored
    
sprite_next_row_colored:
    add w24, w24, #1
    
    // Move sprite pointer to next row
    mov w0, w22
    add w0, w0, #7
    lsr w0, w0, #3       // Bytes per row
    add x19, x19, x0
    
    // Move framebuffer to next row
    mov w0, #672            // WINDOW_WIDTH
    mov w1, #3              // SCALE_FACTOR
    mul w0, w0, w1
    mov w1, #4              // BYTES_PER_PIXEL
    mul w0, w0, w1
    add x6, x6, x0
    
    b sprite_row_loop_colored
    
sprite_done_colored:
    ldp x23, x24, [sp, #48]
    ldp x21, x22, [sp, #32]
    ldp x19, x20, [sp, #16]
    ldp x29, x30, [sp], #64
    ret

// clear_screen_color: Clear screen to specified color
// Parameters:
//   w0 = color (RGBA format)
.global _clear_screen_color
_clear_screen_color:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    
    // Get framebuffer pointer
    stp x19, x20, [sp, #-16]!
    mov w19, w0            // Save color
    
    bl _get_framebuffer
    mov x1, x0             // framebuffer in x1
    mov w0, w19            // Restore color
    
    ldp x19, x20, [sp], #16
    
    // Calculate total size (width * height * bytes_per_pixel)
    mov w2, #672            // WINDOW_WIDTH = 224 * 3
    mov w3, #768            // WINDOW_HEIGHT = 256 * 3
    mul w2, w2, w3
    mov w3, #4              // BYTES_PER_PIXEL
    mul w2, w2, w3
    
    // Prepare color in NEON register
    dup v0.4s, w0        // Duplicate color to all lanes
    
clear_color_loop:
    cmp w2, #16
    b.lt clear_color_remainder
    
    st1 {v0.16b}, [x1], #16
    sub w2, w2, #16
    b clear_color_loop
    
clear_color_remainder:
    cbz w2, clear_color_done
    str w0, [x1], #4
    sub w2, w2, #4
    b clear_color_remainder
    
clear_color_done:
    ldp x29, x30, [sp], #16
    ret

