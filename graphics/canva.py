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
                
    def triangle(self, x1, y1, x2, y2, x3, y3, red, green, blue):

        self.line(x1, y1, x2, y2, red, green, blue)
        self.line(x2, y2, x3, y3, red, green, blue)
        self.line(x3, y3, x1, y1, red, green, blue)
        
    def triangle_filled(self, x1, y1, x2, y2, x3, y3,red, green, blue):
        min_y = min(y1, y2, y3)
        max_y = max(y1, y2, y3)

        edges = [
            (x1, y1, x2, y2),
            (x2, y2, x3, y3),
            (x3, y3, x1, y1)
        ]

        for y in range(min_y, max_y + 1):

            intersections = []

            for xa, ya, xb, yb in edges:

                if ya == yb:
                    continue

                if min(ya, yb) <= y < max(ya, yb):

                    x = xa + (y - ya) * (xb - xa) / (yb - ya)

                    intersections.append(int(x))

            if len(intersections) >= 2:

                intersections.sort()

                x_start = intersections[0]
                x_end = intersections[-1]

                for x in range(x_start, x_end + 1):
                    self.pixel(x, y, red, green, blue)
                    
    def rectangle(self, x, y, width, height, red, green, blue):

        self.line(x, y, x + width, y, red, green, blue)

        self.line(x + width, y, x + width, y + height, red, green, blue)

        self.line(x + width, y + height, x, y + height,red, green, blue)

        self.line(x, y + height, x, y, red, green, blue)
        
