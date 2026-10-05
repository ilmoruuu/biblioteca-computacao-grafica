import sdl2
import sdl2.ext
import ctypes


class SDL:

    def __init__(self, width, height, title):

        self.width = width
        self.height = height
        self.title = title

        self.window = None
        self.renderer = None
        self.texture = None

    def create_window(self):

        sdl2.ext.init()

        self.window = sdl2.ext.Window(
            self.title,
            size=(self.width, self.height)
        )

        self.window.show()

        self.renderer = sdl2.SDL_CreateRenderer(
            self.window.window,
            -1,
            sdl2.SDL_RENDERER_ACCELERATED
        )

        self.texture = sdl2.SDL_CreateTexture(
            self.renderer,
            sdl2.SDL_PIXELFORMAT_RGBA8888,
            sdl2.SDL_TEXTUREACCESS_STREAMING,
            self.width,
            self.height
        )

    def update(self, framebuffer):

        buffer = (
            ctypes.c_ubyte * len(framebuffer)
        ).from_buffer(framebuffer)

        sdl2.SDL_UpdateTexture(
            self.texture,
            None,
            buffer,
            self.width * 4
        )

        sdl2.SDL_RenderClear(
            self.renderer
        )

        sdl2.SDL_RenderCopy(
            self.renderer,
            self.texture,
            None,
            None
        )

        sdl2.SDL_RenderPresent(
            self.renderer
        )

    def process_events(self):

        event = sdl2.SDL_Event()

        while sdl2.SDL_PollEvent(event):

            if event.type == sdl2.SDL_QUIT:
                return False

        return True

    def destroy(self):

        if self.texture:
            sdl2.SDL_DestroyTexture(
                self.texture
            )

        if self.renderer:
            sdl2.SDL_DestroyRenderer(
                self.renderer
            )

        if self.window:
            self.window.close()

        sdl2.ext.quit()