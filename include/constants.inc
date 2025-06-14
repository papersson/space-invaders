// constants.inc - Common constants for Space Invaders
// Screen dimensions
.equ SCREEN_WIDTH, 224
.equ SCREEN_HEIGHT, 256

// Player constants
.equ PLAYER_WIDTH, 16
.equ PLAYER_HEIGHT, 8
.equ PLAYER_MIN_X, 8
.equ PLAYER_MAX_X, (SCREEN_WIDTH - PLAYER_WIDTH - 8)
.equ PLAYER_SPEED, 2
.equ LIVES_COUNT, 3

// Alien constants
.equ ALIEN_WIDTH, 11
.equ ALIEN_HEIGHT, 8
.equ ALIEN_ROWS, 5
.equ ALIEN_COLS, 11
.equ ALIEN_COUNT, 55

// Shield constants
.equ SHIELD_WIDTH, 22
.equ SHIELD_HEIGHT, 16
.equ SHIELD_COUNT, 4

// Bullet constants
.equ BULLET_WIDTH, 3
.equ BULLET_HEIGHT, 5
.equ BULLET_SPEED, 4
.equ MAX_ALIEN_BULLETS, 3

// UFO constants
.equ UFO_WIDTH, 16
.equ UFO_HEIGHT, 7

// Other game constants
.equ EXPLOSION_WIDTH, 13
.equ EXPLOSION_HEIGHT, 8

// Game timing (60 FPS)
.equ FPS, 60
.equ FRAME_TIME_NS, 16666667    // 1,000,000,000 / 60
.equ FRAME_TIME_MS, 16          // milliseconds per frame

// Entity counts and limits
.equ LIVES_DEFAULT, 3
.equ MAX_PLAYER_BULLETS, 1
.equ UFO_SPAWN_MIN, 1500        // 25 seconds at 60 FPS
.equ UFO_SPAWN_MAX, 2400        // 40 seconds at 60 FPS

// Memory offsets and sizes
.equ GAME_STATE_SIZE, 64        // Total game state structure
.equ ALIEN_STRUCT_SIZE, 8       // Per alien: x(2) + y(2) + alive(1) + type(1) + pad(2)
.equ SHIELD_MASK_SIZE, 352      // 22 * 16 pixels = 352 bits = 44 bytes (rounded to 48)
.equ BULLET_STRUCT_SIZE, 8      // x(2) + y(2) + active(1) + type(1) + frame(1) + pad(1)

// Movement speeds (pixels per frame)
.equ ALIEN_SPEED_X, 2
.equ ALIEN_SPEED_Y, 8           // When dropping down
.equ ALIEN_BULLET_SPEED, 3
.equ UFO_SPEED, 2

// Movement boundaries
.equ ALIEN_MIN_X, 8
.equ ALIEN_MAX_X, (SCREEN_WIDTH - ALIEN_WIDTH - 8)
.equ ALIEN_INVASION_Y, 200      // Y position where aliens win
.equ UFO_Y, 32                  // UFO flies at top of screen

// Delays and timers (in frames)
.equ ALIEN_BASE_DELAY, 30       // Starting movement delay
.equ ALIEN_MIN_DELAY, 2         // Fastest movement delay
.equ BULLET_COOLDOWN, 30        // Player fire rate limit
.equ ALIEN_FIRE_DELAY, 60       // Frames between alien shots
.equ GAME_OVER_DELAY, 180       // 3 seconds at 60 FPS

// Score values
.equ SCORE_ALIEN_BOTTOM, 10     // Bottom 2 rows
.equ SCORE_ALIEN_MIDDLE, 20     // Middle 2 rows
.equ SCORE_ALIEN_TOP, 30        // Top row
.equ SCORE_UFO_1, 50
.equ SCORE_UFO_2, 100
.equ SCORE_UFO_3, 150
.equ SCORE_UFO_4, 300
.equ SCORE_LEVEL_BONUS, 100     // Multiplied by level number

// Audio frequencies (Hz)
.equ FREQ_PLAYER_FIRE, 880
.equ FREQ_ALIEN_HIT, 1320
.equ FREQ_PLAYER_HIT, 110
.equ FREQ_UFO_LOW, 440
.equ FREQ_UFO_HIGH, 660

// Audio durations (ms)
.equ DUR_LASER, 60
.equ DUR_HIT, 60
.equ DUR_PLAYER_HIT, 220

// Game states
.equ STATE_MENU, 0
.equ STATE_PLAYING, 1
.equ STATE_PAUSED, 2
.equ STATE_GAME_OVER, 3
.equ STATE_HIGH_SCORE, 4

// Input bit masks
.equ INPUT_LEFT, 0x01
.equ INPUT_RIGHT, 0x02
.equ INPUT_FIRE, 0x04
.equ INPUT_PAUSE, 0x08
.equ INPUT_QUIT, 0x10

// Colors (RGBA format)
.equ COLOR_BLACK, 0x000000FF
.equ COLOR_WHITE, 0xFFFFFFFF
.equ COLOR_GREEN, 0x00FF00FF
.equ COLOR_RED, 0xFF0000FF
.equ COLOR_CYAN, 0x00FFFFFF
.equ COLOR_YELLOW, 0xFFFF00FF
.equ COLOR_MAGENTA, 0xFF00FFFF

// System constants
.equ PAGE_SIZE, 16384           // 16KB pages on Apple Silicon
.equ CACHE_LINE_SIZE, 128       // M1/M2/M3 cache line size