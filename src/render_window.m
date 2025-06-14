#import <Cocoa/Cocoa.h>
#import <QuartzCore/QuartzCore.h>
#include <pthread.h>

#define WINDOW_WIDTH 672
#define WINDOW_HEIGHT 768
#define BYTES_PER_PIXEL 4

@interface SpaceInvadersView : NSView
{
    CGContextRef bitmapContext;
    void* framebuffer;
    pthread_mutex_t* mutex;
}
- (id)initWithFrame:(NSRect)frame framebuffer:(void*)fb mutex:(pthread_mutex_t*)m;
- (void)updateDisplay;
@end

@implementation SpaceInvadersView

- (id)initWithFrame:(NSRect)frame framebuffer:(void*)fb mutex:(pthread_mutex_t*)m {
    self = [super initWithFrame:frame];
    if (self) {
        framebuffer = fb;
        mutex = m;
        
        // Create bitmap context
        CGColorSpaceRef colorSpace = CGColorSpaceCreateDeviceRGB();
        bitmapContext = CGBitmapContextCreate(
            framebuffer,
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            8,
            WINDOW_WIDTH * BYTES_PER_PIXEL,
            colorSpace,
            kCGImageAlphaPremultipliedFirst | kCGBitmapByteOrder32Little
        );
        CGColorSpaceRelease(colorSpace);
        
        // Set up layer for better performance
        [self setWantsLayer:YES];
        self.layer.magnificationFilter = kCAFilterNearest;
    }
    return self;
}

- (void)dealloc {
    if (bitmapContext) {
        CGContextRelease(bitmapContext);
    }
    // ARC handles [super dealloc] automatically
}

- (void)drawRect:(NSRect)dirtyRect {
    pthread_mutex_lock(mutex);
    
    CGContextRef currentContext = [[NSGraphicsContext currentContext] CGContext];
    
    // Create image from bitmap context
    CGImageRef image = CGBitmapContextCreateImage(bitmapContext);
    if (image) {
        // Draw image scaled to window size
        CGContextDrawImage(currentContext, 
                          CGRectMake(0, 0, self.bounds.size.width, self.bounds.size.height), 
                          image);
        CGImageRelease(image);
    }
    
    pthread_mutex_unlock(mutex);
}

- (void)updateDisplay {
    [self setNeedsDisplay:YES];
}

- (BOOL)acceptsFirstResponder {
    return YES;
}

// Store last key event
static int lastKeyEvent = 0;

- (void)keyDown:(NSEvent *)event {
    NSLog(@"Key down: %d", [event keyCode]);
    switch ([event keyCode]) {
        case 123: lastKeyEvent = 1; break;  // Left arrow
        case 124: lastKeyEvent = 2; break;  // Right arrow
        case 49:  lastKeyEvent = 3; break;  // Space
        case 53:  lastKeyEvent = 4; break;  // Escape
    }
}

- (void)keyUp:(NSEvent *)event {
    switch ([event keyCode]) {
        case 123: if (lastKeyEvent == 1) lastKeyEvent = 0; break;  // Left arrow
        case 124: if (lastKeyEvent == 2) lastKeyEvent = 0; break;  // Right arrow
        case 49:  if (lastKeyEvent == 3) lastKeyEvent = 0; break;  // Space
    }
}

@end

// C interface structures
typedef struct {
    NSWindow* window;
    SpaceInvadersView* view;
    NSApplication* app;
    void* framebuffer;
    pthread_mutex_t mutex;
    BOOL running;
} WindowContext;

static WindowContext* g_windowContext = NULL;

// C interface functions

void* create_window(int width, int height) {
    @autoreleasepool {
        // Initialize application if needed
        NSApplication* app = [NSApplication sharedApplication];
        [app setActivationPolicy:NSApplicationActivationPolicyRegular];
        
        // Allocate window context
        g_windowContext = (WindowContext*)malloc(sizeof(WindowContext));
        if (!g_windowContext) return NULL;
        
        memset((void*)g_windowContext, 0, sizeof(WindowContext));
        pthread_mutex_init(&g_windowContext->mutex, NULL);
        
        // Allocate framebuffer
        g_windowContext->framebuffer = malloc(width * height * BYTES_PER_PIXEL);
        if (!g_windowContext->framebuffer) {
            free(g_windowContext);
            return NULL;
        }
        memset(g_windowContext->framebuffer, 0, width * height * BYTES_PER_PIXEL);
        
        // Create window
        NSRect frame = NSMakeRect(100, 100, width, height);
        NSUInteger styleMask = NSWindowStyleMaskTitled | 
                               NSWindowStyleMaskClosable | 
                               NSWindowStyleMaskMiniaturizable;
        
        g_windowContext->window = [[NSWindow alloc] initWithContentRect:frame
                                                              styleMask:styleMask
                                                                backing:NSBackingStoreBuffered
                                                                  defer:NO];
        
        [g_windowContext->window setTitle:@"Space Invaders"];
        [g_windowContext->window setAcceptsMouseMovedEvents:YES];
        
        // Create custom view
        g_windowContext->view = [[SpaceInvadersView alloc] initWithFrame:frame 
                                                             framebuffer:g_windowContext->framebuffer
                                                                   mutex:&g_windowContext->mutex];
        
        [g_windowContext->window setContentView:g_windowContext->view];
        [g_windowContext->window makeKeyAndOrderFront:nil];
        [g_windowContext->window makeFirstResponder:g_windowContext->view];
        [g_windowContext->window setAcceptsMouseMovedEvents:YES];
        
        // Make sure the window can receive key events
        [NSApp activateIgnoringOtherApps:YES];
        
        // Run the event loop briefly to ensure window is set up
        [[NSRunLoop currentRunLoop] runUntilDate:[NSDate dateWithTimeIntervalSinceNow:0.1]];
        
        // Make window key again
        [g_windowContext->window makeKeyAndOrderFront:nil];
        [g_windowContext->window makeFirstResponder:g_windowContext->view];
        
        g_windowContext->running = YES;
        
        return g_windowContext;
    }
}

void* get_framebuffer(void) {
    if (!g_windowContext) return NULL;
    return g_windowContext->framebuffer;
}

void present_frame(void* context) {
    if (!g_windowContext || !g_windowContext->view) return;
    
    @autoreleasepool {
        // Update display on main thread
        dispatch_async(dispatch_get_main_queue(), ^{
            [g_windowContext->view updateDisplay];
        });
        
        // Process events
        NSEvent* event;
        while ((event = [NSApp nextEventMatchingMask:NSEventMaskAny
                                           untilDate:[NSDate distantPast]
                                              inMode:NSDefaultRunLoopMode
                                             dequeue:YES])) {
            [NSApp sendEvent:event];
        }
    }
}

void cleanup_window(void* context) {
    if (!g_windowContext) return;
    
    @autoreleasepool {
        if (g_windowContext->window) {
            [g_windowContext->window close];
            // ARC handles release automatically
        }
        
        if (g_windowContext->view) {
            // ARC handles release automatically
        }
        
        if (g_windowContext->framebuffer) {
            free(g_windowContext->framebuffer);
        }
        
        pthread_mutex_destroy(&g_windowContext->mutex);
        free(g_windowContext);
        g_windowContext = NULL;
    }
}

// Get window events (for input handling)
extern int lastKeyEvent;  // Defined in SpaceInvadersView

int get_window_event(void) {
    if (!g_windowContext) return -1;
    
    @autoreleasepool {
        // Process pending events to update lastKeyEvent
        NSEvent* event;
        while ((event = [NSApp nextEventMatchingMask:NSEventMaskKeyDown | NSEventMaskKeyUp | NSEventMaskFlagsChanged
                                            untilDate:[NSDate distantPast]
                                               inMode:NSDefaultRunLoopMode
                                              dequeue:YES])) {
            [NSApp sendEvent:event];
        }
        
        // Return the current key state
        return lastKeyEvent;
    }
}