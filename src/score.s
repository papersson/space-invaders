// score.s - Score tracking and display for Space Invaders
// Implements score management, high score persistence, and formatting

.global __score_init
.global __score_add
.global __score_add_alien
.global __score_add_ufo
.global __score_get_current
.global __score_get_high
.global __score_save_high
.global __score_load_high
.global __score_format
.global __score_check_new_high
.global __score_add_level_bonus

.include "constants.inc"

// Score data structure
.equ SCORE_CURRENT,         0       // 32-bit current score
.equ SCORE_HIGH,            4       // 32-bit high score
.equ SCORE_MULTIPLIER,      8       // 32-bit combo multiplier
.equ SCORE_UFO_COUNTER,     12      // UFO hit counter for pattern
.equ SCORE_STRUCT_SIZE,     16

// UFO scoring pattern (50, 100, 150, 300, repeat)
.equ UFO_PATTERN_SIZE,      4
.equ UFO_SCORE_1,           50
.equ UFO_SCORE_2,           100
.equ UFO_SCORE_3,           150
.equ UFO_SCORE_4,           300

// File paths and constants
.equ O_RDONLY,              0x0000
.equ O_WRONLY,              0x0001
.equ O_CREAT,               0x0200
.equ O_TRUNC,               0x0400
.equ S_IRUSR,               0x0100
.equ S_IWUSR,               0x0080

.section __DATA,__data
.p2align 3
_score_data:
    .word   0                   // Current score
    .word   0                   // High score
    .word   1                   // Multiplier
    .word   0                   // UFO counter

ufo_scores:
    .word   UFO_SCORE_1
    .word   UFO_SCORE_2
    .word   UFO_SCORE_3
    .word   UFO_SCORE_4

// High score file path components
app_support_dir:
    .asciz  "/Library/Application Support"
game_dir:
    .asciz  "SpaceInvaders"
high_score_file:
    .asciz  "highscore.dat"

// Format buffer for score display
_score_format_buffer:
    .space  8                   // 6 digits + null + padding

.section __TEXT,__text
.p2align 2

// Initialize scoring system
// Input: none
// Output: none
// Clobbers: x0-x3, x16-x17
_score_init:
    stp     x29, x30, [sp, #-16]!
    mov     x29, sp
    
    // Clear score data
    adrp    x0, _score_data@PAGE
    add     x0, x0, _score_data@PAGEOFF
    
    str     wzr, [x0, #SCORE_CURRENT]
    str     wzr, [x0, #SCORE_HIGH]
    mov     w1, #1
    str     w1, [x0, #SCORE_MULTIPLIER]
    str     wzr, [x0, #SCORE_UFO_COUNTER]
    
    // Load high score from file
    bl      _score_load_high
    
    ldp     x29, x30, [sp], #16
    ret

// Add points to current score
// Input: w0 = points to add
// Output: none
// Clobbers: x0-x3
_score_add:
    adrp    x1, _score_data@PAGE
    add     x1, x1, _score_data@PAGEOFF
    
    // Load current score and multiplier
    ldr     w2, [x1, #SCORE_CURRENT]
    ldr     w3, [x1, #SCORE_MULTIPLIER]
    
    // Apply multiplier and add
    mul     w0, w0, w3
    add     w2, w2, w0
    
    // Store updated score
    str     w2, [x1, #SCORE_CURRENT]
    
    // Check if new high score
    ldr     w3, [x1, #SCORE_HIGH]
    cmp     w2, w3
    b.le    1f
    str     w2, [x1, #SCORE_HIGH]
1:
    ret

// Add points based on alien type
// Input: w0 = alien row (0-4, 0=top)
// Output: none
// Clobbers: x0-x3
_score_add_alien:
    stp     x29, x30, [sp, #-16]!
    mov     x29, sp
    
    // Determine points based on row
    cmp     w0, #2
    b.gt    2f              // Rows 3-4 = bottom aliens
    cmp     w0, #0
    b.eq    1f              // Row 0 = top aliens
    
    // Middle aliens (rows 1-2)
    mov     w0, #SCORE_ALIEN_MIDDLE
    b       3f
    
1:  // Top aliens
    mov     w0, #SCORE_ALIEN_TOP
    b       3f
    
2:  // Bottom aliens
    mov     w0, #SCORE_ALIEN_BOTTOM
    
3:  bl      _score_add
    
    ldp     x29, x30, [sp], #16
    ret

// Add UFO points based on pattern
// Input: none
// Output: none
// Clobbers: x0-x4
_score_add_ufo:
    stp     x29, x30, [sp, #-16]!
    mov     x29, sp
    
    adrp    x1, _score_data@PAGE
    add     x1, x1, _score_data@PAGEOFF
    
    // Get UFO counter
    ldr     w2, [x1, #SCORE_UFO_COUNTER]
    
    // Get score from pattern
    adrp    x3, ufo_scores@PAGE
    add     x3, x3, ufo_scores@PAGEOFF
    ldr     w0, [x3, x2, lsl #2]
    
    // Update counter (0-3 pattern)
    add     w2, w2, #1
    and     w2, w2, #3
    str     w2, [x1, #SCORE_UFO_COUNTER]
    
    // Add the score
    bl      _score_add
    
    ldp     x29, x30, [sp], #16
    ret

// Get current score
// Input: none
// Output: w0 = current score
// Clobbers: x1
_score_get_current:
    adrp    x1, _score_data@PAGE
    add     x1, x1, _score_data@PAGEOFF
    ldr     w0, [x1, #SCORE_CURRENT]
    ret

// Get high score
// Input: none
// Output: w0 = high score
// Clobbers: x1
_score_get_high:
    adrp    x1, _score_data@PAGE
    add     x1, x1, _score_data@PAGEOFF
    ldr     w0, [x1, #SCORE_HIGH]
    ret

// Save high score to file
// Input: none
// Output: none
// Clobbers: x0-x5, x16-x17
_score_save_high:
    stp     x29, x30, [sp, #-32]!
    mov     x29, sp
    
    // Get home directory
    mov     x16, #0x2C          // getpwuid syscall
    mov     x0, #0              // uid = 0 for current user
    svc     #0x80
    cbz     x0, 9f              // Failed to get home dir
    
    // Build full path: $HOME/Library/Application Support/SpaceInvaders/
    sub     sp, sp, #256        // Path buffer
    mov     x19, sp
    mov     x20, x0             // Save pwent pointer
    
    // Copy home directory
    ldr     x1, [x20, #0x28]    // pw_dir field
    mov     x0, x19
    bl      strcpy
    
    // Append /Library/Application Support
    adrp    x1, app_support_dir@PAGE
    add     x1, x1, app_support_dir@PAGEOFF
    bl      strcat
    
    // Create directory if needed
    mov     x0, x19
    mov     x1, #0x1FF          // Mode 0777
    mov     x16, #0x88          // mkdir syscall
    svc     #0x80
    
    // Append /SpaceInvaders
    mov     x0, x19
    mov     x1, #'/'
    bl      append_char
    adrp    x1, game_dir@PAGE
    add     x1, x1, game_dir@PAGEOFF
    bl      strcat
    
    // Create game directory if needed
    mov     x0, x19
    mov     x1, #0x1FF          // Mode 0777
    mov     x16, #0x88          // mkdir syscall
    svc     #0x80
    
    // Append /highscore.dat
    mov     x0, x19
    mov     x1, #'/'
    bl      append_char
    adrp    x1, high_score_file@PAGE
    add     x1, x1, high_score_file@PAGEOFF
    bl      strcat
    
    // Open file for writing
    mov     x0, x19             // Path
    mov     x1, #(O_WRONLY | O_CREAT | O_TRUNC)
    mov     x2, #(S_IRUSR | S_IWUSR)
    mov     x16, #0x5           // open syscall
    svc     #0x80
    
    cmp     x0, #0
    b.lt    8f                  // Failed to open
    mov     x19, x0             // Save fd
    
    // Write high score
    adrp    x1, _score_data@PAGE
    add     x1, x1, _score_data@PAGEOFF
    add     x1, x1, #SCORE_HIGH
    mov     x2, #4              // Write 4 bytes
    mov     x16, #0x4           // write syscall
    svc     #0x80
    
    // Close file
    mov     x0, x19
    mov     x16, #0x6           // close syscall
    svc     #0x80
    
8:  add     sp, sp, #256        // Clean up path buffer
9:  ldp     x29, x30, [sp], #32
    ret

// Load high score from file
// Input: none
// Output: none
// Clobbers: x0-x5, x16-x17
_score_load_high:
    stp     x29, x30, [sp, #-32]!
    mov     x29, sp
    
    // Get home directory
    mov     x16, #0x2C          // getpwuid syscall
    mov     x0, #0              // uid = 0 for current user
    svc     #0x80
    cbz     x0, 9f              // Failed to get home dir
    
    // Build full path
    sub     sp, sp, #256        // Path buffer
    mov     x19, sp
    mov     x20, x0             // Save pwent pointer
    
    // Copy home directory
    ldr     x1, [x20, #0x28]    // pw_dir field
    mov     x0, x19
    bl      strcpy
    
    // Append paths
    adrp    x1, app_support_dir@PAGE
    add     x1, x1, app_support_dir@PAGEOFF
    bl      strcat
    mov     x0, x19
    mov     x1, #'/'
    bl      append_char
    adrp    x1, game_dir@PAGE
    add     x1, x1, game_dir@PAGEOFF
    bl      strcat
    mov     x0, x19
    mov     x1, #'/'
    bl      append_char
    adrp    x1, high_score_file@PAGE
    add     x1, x1, high_score_file@PAGEOFF
    bl      strcat
    
    // Open file for reading
    mov     x0, x19             // Path
    mov     x1, #O_RDONLY
    mov     x2, #0
    mov     x16, #0x5           // open syscall
    svc     #0x80
    
    cmp     x0, #0
    b.lt    8f                  // File doesn't exist
    mov     x19, x0             // Save fd
    
    // Read high score
    adrp    x1, _score_data@PAGE
    add     x1, x1, _score_data@PAGEOFF
    add     x1, x1, #SCORE_HIGH
    mov     x2, #4              // Read 4 bytes
    mov     x16, #0x3           // read syscall
    svc     #0x80
    
    // Close file
    mov     x0, x19
    mov     x16, #0x6           // close syscall
    svc     #0x80
    
8:  add     sp, sp, #256        // Clean up path buffer
9:  ldp     x29, x30, [sp], #32
    ret

// Format score as string for display
// Input: w0 = score value
//        x1 = output buffer (min 8 bytes)
// Output: x0 = pointer to formatted string
// Clobbers: x0-x4
_score_format:
    mov     x2, x1              // Save output buffer
    mov     w3, w0              // Save score
    
    // Start from the end of 6-digit field
    add     x1, x1, #5          // Point to last digit position
    mov     w4, #6              // Digit counter
    
1:  // Extract digit
    mov     w0, #10
    udiv    w5, w3, w0
    msub    w0, w5, w0, w3      // w0 = w3 % 10
    add     w0, w0, #'0'        // Convert to ASCII
    strb    w0, [x1], #-1       // Store and move back
    mov     w3, w5              // w3 = w3 / 10
    
    subs    w4, w4, #1
    b.ne    1b
    
    // Null terminate
    mov     w0, #0
    strb    w0, [x2, #6]
    
    mov     x0, x2              // Return buffer pointer
    ret

// Check if current score is new high score
// Input: none
// Output: w0 = 1 if new high score, 0 otherwise
// Clobbers: x1-x2
_score_check_new_high:
    adrp    x1, _score_data@PAGE
    add     x1, x1, _score_data@PAGEOFF
    
    ldr     w0, [x1, #SCORE_CURRENT]
    ldr     w2, [x1, #SCORE_HIGH]
    
    cmp     w0, w2
    cset    w0, gt
    ret

// Add level completion bonus
// Input: w0 = level number
// Output: none
// Clobbers: x0-x3
_score_add_level_bonus:
    stp     x29, x30, [sp, #-16]!
    mov     x29, sp
    
    // Level bonus = 100 × level
    mov     w1, #100
    mul     w0, w0, w1
    
    bl      _score_add
    
    ldp     x29, x30, [sp], #16
    ret

// Helper: String copy
// Input: x0 = dest, x1 = src
// Output: x0 = dest
// Clobbers: x2-x3
strcpy:
    mov     x2, x0              // Save dest
1:  ldrb    w3, [x1], #1
    strb    w3, [x0], #1
    cbnz    w3, 1b
    mov     x0, x2
    ret

// Helper: String concatenate
// Input: x0 = dest, x1 = src
// Output: x0 = dest
// Clobbers: x2-x3
strcat:
    mov     x2, x0              // Save dest
    // Find end of dest
1:  ldrb    w3, [x0]
    cbz     w3, 2f
    add     x0, x0, #1
    b       1b
    // Copy src
2:  ldrb    w3, [x1], #1
    strb    w3, [x0], #1
    cbnz    w3, 2b
    mov     x0, x2
    ret

// Helper: Append single character
// Input: x0 = string, x1 = char
// Output: x0 = string
// Clobbers: x2
append_char:
    mov     x2, x0
    // Find end
1:  ldrb    w3, [x0]
    cbz     w3, 2f
    add     x0, x0, #1
    b       1b
2:  strb    w1, [x0]
    strb    wzr, [x0, #1]
    mov     x0, x2
    ret