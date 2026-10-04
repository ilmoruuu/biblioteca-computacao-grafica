import sdl2
import sdl2.ext
import ctypes

from graphics.canva import Canvas


WIDTH = 800
HEIGHT = 600


canvas = Canvas(WIDTH, HEIGHT)

canvas.pixel(400, 300, 255, 0, 0)


sdl2.ext.init()

window = sdl2.ext.Window(
    "BCG - Biblioteca de Computação Gráfica",
    size=(WIDTH, HEIGHT)
)

window.show()


renderer = sdl2.SDL_CreateRenderer(
    window.window,
    -1,
    sdl2.SDL_RENDERER_ACCELERATED
)


texture = sdl2.SDL_CreateTexture(
    renderer,
    sdl2.SDL_PIXELFORMAT_RGBA8888,
    sdl2.SDL_TEXTUREACCESS_STREAMING,
    WIDTH,
    HEIGHT
)


sdl2.SDL_UpdateTexture(
    texture,
    None,
    (ctypes.c_ubyte * len(canvas.framebuffer)).from_buffer(canvas.framebuffer),
    WIDTH * 4
)


sdl2.SDL_RenderClear(renderer)

sdl2.SDL_RenderCopy(
    renderer,
    texture,
    None,
    None
)

sdl2.SDL_RenderPresent(renderer)


running = True

while running:

    event = sdl2.SDL_Event()

    while sdl2.SDL_PollEvent(event):

        if event.type == sdl2.SDL_QUIT:
            running = False


sdl2.SDL_DestroyTexture(texture)
sdl2.SDL_DestroyRenderer(renderer)

window.close()

sdl2.ext.quit()