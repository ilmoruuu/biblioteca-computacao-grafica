class Canvas:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.framebuffer = bytearray(width * height * 4)

    def pixel(self, x, y, red, green, blue):

        self.pixel_index = (y * self.width) + x
        self.byte_index = self.pixel_index * 4

        self.framebuffer[self.byte_index] = red
        self.framebuffer[self.byte_index + 1] = green
        self.framebuffer[self.byte_index + 2] = blue
        self.framebuffer[self.byte_index + 3] = 255

    def line(self, x1, y1, x2, y2, red, green, blue):

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

        error = dx - dy

        while True:

            self.pixel(x1, y1, red, green, blue)

            if x1 == x2 and y1 == y2:
                break

            error2 = 2 * error

            if error2 > -dy:
                error -= dy
                x1 += sx

            if error2 < dx:
                error += dx
                y1 += sy