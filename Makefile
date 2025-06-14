# Space Invaders ARM64 Assembly Makefile
# Platform: macOS ARM64

# Project name
PROJECT = space_invaders

# Directories
SRC_DIR = src
INC_DIR = include
BUILD_DIR = build
ASSETS_DIR = assets

# Compiler and tools
AS = xcrun clang
CC = xcrun clang
LD = xcrun clang
RM = rm -rf
MKDIR = mkdir -p

# Architecture flags
ARCH = -arch arm64

# Assembly flags
ASFLAGS = $(ARCH) -I$(INC_DIR) -g
CFLAGS = $(ARCH) -I$(INC_DIR) -I$(SRC_DIR) -g -fobjc-arc
LDFLAGS = $(ARCH) -lSystem -framework Cocoa -framework CoreGraphics -framework IOKit -framework QuartzCore

# Debug flags
DEBUG_FLAGS = -DDEBUG -O0
RELEASE_FLAGS = -O2

# Find all source files
ASM_SOURCES = $(wildcard $(SRC_DIR)/*.s)
C_SOURCES = $(wildcard $(SRC_DIR)/*.c)
OBJC_SOURCES = $(wildcard $(SRC_DIR)/*.m)

# Generate object file names
ASM_OBJECTS = $(ASM_SOURCES:$(SRC_DIR)/%.s=$(BUILD_DIR)/%.o)
C_OBJECTS = $(C_SOURCES:$(SRC_DIR)/%.c=$(BUILD_DIR)/%.o)
OBJC_OBJECTS = $(OBJC_SOURCES:$(SRC_DIR)/%.m=$(BUILD_DIR)/%.o)
OBJECTS = $(ASM_OBJECTS) $(C_OBJECTS) $(OBJC_OBJECTS)

# Default target
.PHONY: all
all: debug

# Debug build
.PHONY: debug
debug: ASFLAGS += $(DEBUG_FLAGS)
debug: $(BUILD_DIR) $(PROJECT)
	@echo "Debug build complete: $(PROJECT)"

# Release build
.PHONY: release
release: ASFLAGS += $(RELEASE_FLAGS)
release: clean $(BUILD_DIR) $(PROJECT)
	@echo "Release build complete: $(PROJECT)"

# Create build directory
$(BUILD_DIR):
	@$(MKDIR) $(BUILD_DIR)

# Link object files to create executable
$(PROJECT): $(OBJECTS)
	@echo "Linking $@..."
	@$(LD) $(LDFLAGS) -o $@ $^

# Compile assembly files to object files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.s
	@echo "Assembling $<..."
	@$(AS) $(ASFLAGS) -c $< -o $@

# Compile C files to object files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	@echo "Compiling $<..."
	@$(CC) $(CFLAGS) -c $< -o $@

# Compile Objective-C files to object files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.m
	@echo "Compiling $<..."
	@$(CC) $(CFLAGS) -c $< -o $@

# Clean build artifacts
.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	@$(RM) $(BUILD_DIR)
	@$(RM) $(PROJECT)

# Run the program
.PHONY: run
run: debug
	@echo "Running $(PROJECT)..."
	@./$(PROJECT)

# Run with LLDB debugger
.PHONY: debug-run
debug-run: debug
	@echo "Starting LLDB debugger..."
	@lldb ./$(PROJECT)

# Show project info
.PHONY: info
info:
	@echo "Project: $(PROJECT)"
	@echo "Sources: $(SOURCES)"
	@echo "Objects: $(OBJECTS)"
	@echo "Compiler flags: $(ASFLAGS)"
	@echo "Linker flags: $(LDFLAGS)"

# Help target
.PHONY: help
help:
	@echo "Space Invaders ARM64 Assembly Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  all       - Build debug version (default)"
	@echo "  debug     - Build with debug symbols and no optimization"
	@echo "  release   - Build with optimization"
	@echo "  clean     - Remove all build artifacts"
	@echo "  run       - Build and run the debug version"
	@echo "  debug-run - Build debug version and start LLDB"
	@echo "  info      - Show project configuration"
	@echo "  help      - Show this help message"
	@echo ""
	@echo "Build examples:"
	@echo "  make              # Build debug version"
	@echo "  make release      # Build optimized version"
	@echo "  make clean all    # Clean and rebuild"

# Ensure all targets are remade if Makefile changes
$(OBJECTS): Makefile