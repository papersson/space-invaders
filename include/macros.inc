// macros.inc - Common ARM64 macros for Space Invaders
// Compatible with Apple's ARM64 toolchain

#ifndef MACROS_INC
#define MACROS_INC

// Function prologue - saves frame pointer and link register
.macro FUNC_PROLOGUE
    stp     x29, x30, [sp, #-16]!   // Save FP and LR
    mov     x29, sp                  // Set up frame pointer
.endm

// Function epilogue - restores frame pointer and link register
.macro FUNC_EPILOGUE
    ldp     x29, x30, [sp], #16     // Restore FP and LR
    ret
.endm

// Extended prologue for functions that use callee-saved registers
.macro FUNC_PROLOGUE_SAVE reg_count=2
    .if \reg_count == 2
        stp     x29, x30, [sp, #-32]!
        stp     x19, x20, [sp, #16]
    .elseif \reg_count == 4
        stp     x29, x30, [sp, #-48]!
        stp     x19, x20, [sp, #16]
        stp     x21, x22, [sp, #32]
    .elseif \reg_count == 6
        stp     x29, x30, [sp, #-64]!
        stp     x19, x20, [sp, #16]
        stp     x21, x22, [sp, #32]
        stp     x23, x24, [sp, #48]
    .else
        .error "Unsupported register count for FUNC_PROLOGUE_SAVE"
    .endif
    mov     x29, sp
.endm

// Extended epilogue for functions that use callee-saved registers
.macro FUNC_EPILOGUE_RESTORE reg_count=2
    .if \reg_count == 2
        ldp     x19, x20, [sp, #16]
        ldp     x29, x30, [sp], #32
    .elseif \reg_count == 4
        ldp     x21, x22, [sp, #32]
        ldp     x19, x20, [sp, #16]
        ldp     x29, x30, [sp], #48
    .elseif \reg_count == 6
        ldp     x23, x24, [sp, #48]
        ldp     x21, x22, [sp, #32]
        ldp     x19, x20, [sp, #16]
        ldp     x29, x30, [sp], #64
    .else
        .error "Unsupported register count for FUNC_EPILOGUE_RESTORE"
    .endif
    ret
.endm

// Stack allocation with 16-byte alignment
.macro STACK_ALLOC size
    .if (\size & 15) != 0
        sub     sp, sp, #(((\size + 15) / 16) * 16)
    .else
        sub     sp, sp, #\size
    .endif
.endm

// Stack deallocation with 16-byte alignment
.macro STACK_FREE size
    .if (\size & 15) != 0
        add     sp, sp, #(((\size + 15) / 16) * 16)
    .else
        add     sp, sp, #\size
    .endif
.endm

// Save NEON registers to stack
.macro SAVE_NEON_REGS start_reg=0, count=4
    sub     sp, sp, #(16 * \count)
    .set    offset, 0
    .rept   \count
        str     q\start_reg, [sp, #offset]
        .set    offset, offset + 16
        .set    start_reg, start_reg + 1
    .endr
.endm

// Restore NEON registers from stack
.macro RESTORE_NEON_REGS start_reg=0, count=4
    .set    offset, 0
    .rept   \count
        ldr     q\start_reg, [sp, #offset]
        .set    offset, offset + 16
        .set    start_reg, start_reg + 1
    .endr
    add     sp, sp, #(16 * \count)
.endm

// Load 16-byte aligned vector
.macro LOAD_VECTOR_ALIGNED dest, base, offset=0
    .if \offset == 0
        ldr     q\dest, [\base]
    .else
        ldr     q\dest, [\base, #\offset]
    .endif
.endm

// Store 16-byte aligned vector
.macro STORE_VECTOR_ALIGNED src, base, offset=0
    .if \offset == 0
        str     q\src, [\base]
    .else
        str     q\src, [\base, #\offset]
    .endif
.endm

// Zero a NEON register
.macro ZERO_VECTOR reg
    movi    v\reg\().16b, #0
.endm

// Set all bytes in a NEON register to a value
.macro SET_VECTOR_BYTE reg, value
    movi    v\reg\().16b, #\value
.endm

// Memory barrier for synchronization
.macro MEMORY_BARRIER
    dmb     sy
.endm

// Data cache operations
.macro CACHE_CLEAN_LINE addr
    dc      cvac, \addr
.endm

.macro CACHE_INVALIDATE_LINE addr
    dc      ivac, \addr
.endm

// Debug assert macro - checks condition and breaks if false
.macro DEBUG_ASSERT condition, code
#ifdef DEBUG
    \condition
    b.eq    1f
    brk     #\code
1:
#endif
.endm

// Debug print macro - prints register value (requires debug print function)
.macro DEBUG_PRINT_REG reg
#ifdef DEBUG
    stp     x0, x1, [sp, #-16]!
    stp     x2, x3, [sp, #-16]!
    mov     x0, \reg
    bl      _debug_print_hex
    ldp     x2, x3, [sp], #16
    ldp     x0, x1, [sp], #16
#endif
.endm

// Align code to cache line boundary
.macro ALIGN_CODE
    .align  7   // 2^7 = 128 bytes for Apple Silicon
.endm

// Align data to specified power of 2
.macro ALIGN_DATA power=4
    .align  \power
.endm

// Create a global function entry point
.macro GLOBAL_FUNC name
    .global _\name
    .align  2
_\name:
.endm

// Create a local function entry point
.macro LOCAL_FUNC name
    .align  2
\name:
.endm

// Load immediate value (handles large immediates)
.macro LOAD_IMM reg, value
    .if ((\value >= -65536) && (\value <= 65535))
        mov     \reg, #\value
    .else
        movz    \reg, #(\value & 0xFFFF)
        .if (\value >> 16) != 0
            movk    \reg, #((\value >> 16) & 0xFFFF), lsl #16
        .endif
        .if (\value >> 32) != 0
            movk    \reg, #((\value >> 32) & 0xFFFF), lsl #32
        .endif
        .if (\value >> 48) != 0
            movk    \reg, #((\value >> 48) & 0xFFFF), lsl #48
        .endif
    .endif
.endm

// Load address of a symbol
.macro LOAD_ADDR reg, symbol
    adrp    \reg, \symbol@PAGE
    add     \reg, \reg, \symbol@PAGEOFF
.endm

// Conditional move based on flag
.macro CMOV dest, src, cond
    csel    \dest, \src, \dest, \cond
.endm

// Min/Max operations
.macro MIN dest, a, b
    cmp     \a, \b
    csel    \dest, \a, \b, lt
.endm

.macro MAX dest, a, b
    cmp     \a, \b
    csel    \dest, \a, \b, gt
.endm

// Clamp value between min and max
.macro CLAMP value, min, max, temp
    cmp     \value, \min
    csel    \temp, \min, \value, lt
    cmp     \temp, \max
    csel    \value, \max, \temp, gt
.endm

// NEON helper for parallel byte comparison
.macro COMPARE_BYTES_16 dest, src1, src2
    cmeq    v\dest\().16b, v\src1\().16b, v\src2\().16b
.endm

// NEON helper for finding minimum bytes
.macro MIN_BYTES_16 dest, src1, src2
    umin    v\dest\().16b, v\src1\().16b, v\src2\().16b
.endm

// NEON helper for finding maximum bytes
.macro MAX_BYTES_16 dest, src1, src2
    umax    v\dest\().16b, v\src1\().16b, v\src2\().16b
.endm

#endif // MACROS_INC