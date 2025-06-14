// input_simple.s - Simple keyboard input for Space Invaders
// Uses polling approach without IOKit for initial testing

.section __TEXT,__text
.p2align 2

#include "constants.inc"
#include "macros.inc"

// Input state structure
.section __DATA,__data
.p2align 3
input_state:
    .byte 0     // left_pressed
    .byte 0     // right_pressed  
    .byte 0     // fire_pressed
    .byte 0     // fire_prev (for edge detection)
    .space 4    // padding

// Public functions
.global _input_init
.global _input_poll
.global _input_is_left_pressed
.global _input_is_right_pressed
.global _input_is_fire_pressed
.global _input_cleanup

// Initialize input system (simplified - no IOKit)
_input_init:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    
    // Clear input state
    adrp x0, input_state@PAGE
    add x0, x0, input_state@PAGEOFF
    str xzr, [x0]
    
    // Return success
    mov w0, #0
    
    ldp x29, x30, [sp], #16
    ret

// Poll for input (stub for now)
_input_poll:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    
    // For now, just clear all inputs
    // In a real implementation, this would check keyboard state
    adrp x0, input_state@PAGE
    add x0, x0, input_state@PAGEOFF
    
    // Clear all inputs for now
    strb wzr, [x0]        // left = 0
    strb wzr, [x0, #1]    // right = 0
    
    // Update fire edge detection
    ldrb w1, [x0, #2]     // current fire
    strb w1, [x0, #3]     // save as previous
    strb wzr, [x0, #2]    // clear current fire
    
    ldp x29, x30, [sp], #16
    ret

// Check if left arrow is pressed
_input_is_left_pressed:
    adrp x0, input_state@PAGE
    add x0, x0, input_state@PAGEOFF
    ldrb w0, [x0]
    ret

// Check if right arrow is pressed
_input_is_right_pressed:
    adrp x0, input_state@PAGE
    add x0, x0, input_state@PAGEOFF
    ldrb w0, [x0, #1]
    ret

// Check if fire is pressed (edge triggered)
_input_is_fire_pressed:
    adrp x0, input_state@PAGE
    add x0, x0, input_state@PAGEOFF
    ldrb w1, [x0, #2]     // current
    ldrb w2, [x0, #3]     // previous
    
    // Return 1 if pressed now but not before
    cmp w1, #1
    ccmp w2, #0, #0, eq   // if current=1, check prev=0
    cset w0, eq           // set result
    ret

// Clean up input system
_input_cleanup:
    // Nothing to clean up in simple version
    ret