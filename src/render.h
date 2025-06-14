#ifndef RENDER_H
#define RENDER_H

// Screen dimensions
#define SCREEN_WIDTH 224
#define SCREEN_HEIGHT 256
#define SCALE_FACTOR 3
#define WINDOW_WIDTH (SCREEN_WIDTH * SCALE_FACTOR)
#define WINDOW_HEIGHT (SCREEN_HEIGHT * SCALE_FACTOR)

// Assembly functions
extern int render_init(void);
extern void render_frame(void);
extern void render_cleanup(void);
extern void clear_screen(void);
extern void render_sprite(const unsigned char* sprite_data, int x, int y, int width, int height);
extern void render_sprite_masked(const unsigned char* sprite_data, int x, int y, int width, int height, const unsigned char* mask_data);
extern void render_text(const char* text, int x, int y);
extern void render_digit(int digit, int x, int y);

// C bridge functions (from render_window.m)
extern void* create_window(int width, int height);
extern void* get_framebuffer(void);
extern void present_frame(void* context);
extern void cleanup_window(void* context);
extern int get_window_event(void);

#endif // RENDER_H