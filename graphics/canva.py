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