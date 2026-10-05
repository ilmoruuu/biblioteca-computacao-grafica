from graphics.canva import Canvas
from sdl.create_window import SDL


WIDTH = 800
HEIGHT = 600


canvas = Canvas(
    WIDTH,
    HEIGHT
)


canvas.line(
    50, 50,
    300, 150,
    255, 0, 0
)

canvas.triangle(
    100, 200,
    200, 100,
    300, 200,
    0, 255, 0
)

canvas.rectangle(
    400, 100,
    200, 150,
    0, 0, 255
)


sdl = SDL(
    WIDTH,
    HEIGHT,
    "BCG - Biblioteca de Computação Gráfica"
)

sdl.create_window()

sdl.update(
    canvas.framebuffer
)

running = True

while running:

    running = sdl.process_events()

sdl.destroy()