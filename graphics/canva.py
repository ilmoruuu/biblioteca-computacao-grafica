import math

class Canvas:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.framebuffer = bytearray(width * height * 4)
        
    def translate(self, points, tx, ty):

        translated = []

        for x, y in points:

            new_x = x + tx
            new_y = y + ty

            translated.append((new_x, new_y))

        return translated
    
    def scale(self, points, sx, sy):

        scaled = []

        for x, y in points:

            new_x = x * sx
            new_y = y * sy

            scaled.append((new_x, new_y))

        return scaled
    
    def rotate(self, points, angle, pivot_x=0, pivot_y=0):

        rotated = []

        radians = math.radians(angle)

        cos_angle = math.cos(radians)
        sin_angle = math.sin(radians)

        for x, y in points:

            x -= pivot_x
            y -= pivot_y

            new_x = (x * cos_angle- y * sin_angle)

            new_y = (x * sin_angle + y * cos_angle)

            new_x += pivot_x
            new_y += pivot_y

            rotated.append(
                (int(new_x), int(new_y))
            )

        return rotated
    
    def multiply_matrices(self, a, b):

        result = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        for i in range(3):
            for j in range(3):

                for k in range(3):

                    result[i][j] += a[i][k] * b[k][j]

        return result
    
    def translation_matrix(self, tx, ty):

        return [
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ]
        
    def scale_matrix(self, sx, sy):

        return [
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ]
        
    def rotation_matrix(self, angle):

        radians = math.radians(angle)

        cos_angle = math.cos(radians)
        sin_angle = math.sin(radians)

        return [
            [cos_angle, -sin_angle, 0],
            [sin_angle, cos_angle, 0],
            [0, 0, 1]
        ]
        
    
    def multiply_matrices(self, a, b):

        result = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        for i in range(3):
            for j in range(3):

                for k in range(3):

                    result[i][j] += a[i][k] * b[k][j]

        return result
    
    def translation_matrix(self, tx, ty):

        return [
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ]
        
    def scale_matrix(self, sx, sy):

        return [
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ]
        
    def rotation_matrix(self, angle):

        radians = math.radians(angle)

        cos_angle = math.cos(radians)
        sin_angle = math.sin(radians)

        return [
            [cos_angle, -sin_angle, 0],
            [sin_angle, cos_angle, 0],
            [0, 0, 1]
        ]
    
    def transform_point(self, point, matrix):

        x, y = point

        new_x = (
            matrix[0][0] * x +
            matrix[0][1] * y +
            matrix[0][2]
        )

        new_y = (
            matrix[1][0] * x +
            matrix[1][1] * y +
            matrix[1][2]
        )

        return int(new_x), int(new_y)
    
    def transform_points(self, points, matrix):

        transformed = []

        for point in points:

            transformed.append(
                self.transform_point(point, matrix)
            )

        return transformed
    

    def pixel(self, x, y, red, green, blue):

        self.pixel_index = (y * self.width) + x
        self.byte_index = self.pixel_index * 4

        self.framebuffer[self.byte_index] = red
        self.framebuffer[self.byte_index + 1] = green
        self.framebuffer[self.byte_index + 2] = blue
        self.framebuffer[self.byte_index + 3] = 255

    def clip_line(self, x1, y1, x2, y2):

        code1 = self.compute_out_code(x1, y1)
        code2 = self.compute_out_code(x2, y2)

        while True:

            if code1 == 0 and code2 == 0:

                return x1, y1, x2, y2

            elif code1 & code2:

                return None

            else:

                if code1 != 0:
                    code_out = code1
                else:
                    code_out = code2

                if code_out & 8:

                    x = x1 + (
                        (x2 - x1)
                        * (0 - y1)
                        / (y2 - y1)
                    )

                    y = 0

                elif code_out & 4:

                    x = x1 + (
                        (x2 - x1)
                        * (self.height - 1 - y1)
                        / (y2 - y1)
                    )

                    y = self.height - 1

                elif code_out & 2:

                    y = y1 + (
                        (y2 - y1)
                        * (self.width - 1 - x1)
                        / (x2 - x1)
                    )

                    x = self.width - 1

                else:

                    y = y1 + (
                        (y2 - y1)
                        * (0 - x1)
                        / (x2 - x1)
                    )

                    x = 0

                x = int(x)
                y = int(y)

                if code_out == code1:

                    x1 = x
                    y1 = y

                    code1 = self.compute_out_code(
                        x1, y1
                    )

                else:

                    x2 = x
                    y2 = y

                    code2 = self.compute_out_code(
                        x2, y2
                    )

    def line(self, x1, y1, x2, y2, red, green, blue):
        
        
        clipped = self.clip_line(
            x1, y1,
            x2, y2
        )

        if clipped is None:
            return

        x1, y1, x2, y2 = clipped

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
        
    def rectangle_filled(self, x, y, width, height, red, green, blue):

        for current_y in range(y, y + height + 1):

            for current_x in range(x, x + width + 1):
                self.pixel(current_x,current_y, red, green, blue)
                
    def polygon(self, points, red, green, blue):

        if len(points) < 3:
            return

        for i in range(len(points)):

            x1, y1 = points[i]

            x2, y2 = points[(i + 1) % len(points)]

            self.line(x1, y1, x2, y2, red, green, blue)
            
    def polygon_filled(self, points, red, green, blue):

        if len(points) < 3:
            return

        min_y = min(y for x, y in points)
        max_y = max(y for x, y in points)

        edges = []

        for i in range(len(points)):

            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]

            edges.append((x1, y1, x2, y2))

        for y in range(min_y, max_y + 1):

            intersections = []

            for x1, y1, x2, y2 in edges:

                if y1 == y2:
                    continue

                if min(y1, y2) <= y < max(y1, y2):

                    x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)

                    intersections.append(int(x))

            intersections.sort()


            for i in range(0, len(intersections) - 1, 2):

                x_start = intersections[i]
                x_end = intersections[i + 1]

                for x in range(x_start, x_end + 1):

                    self.pixel(
                        x, y,
                        red, green, blue
                    )
                    
    def world_to_screen(self, x, y, scale=1):

        screen_x = int(
            self.width / 2 + x * scale
        )

        screen_y = int(
            self.height / 2 - y * scale
        )

        return screen_x, screen_y
    
    def screen_to_world(self, x, y, scale=1):

        world_x = (x - self.width / 2) / scale

        world_y = (self.height / 2 - y) / scale

        return world_x, world_y
    
    def line_antialiased(self, x1, y1, x2, y2, red, green, blue):

        dx = x2 - x1
        dy = y2 - y1

        steps = max(abs(dx), abs(dy))

        if steps == 0:
            self.pixel(x1, y1, red, green, blue)
            return

        x_increment = dx / steps
        y_increment = dy / steps

        x = x1
        y = y1

        for _ in range(steps + 1):

            x_floor = int(x)
            y_floor = int(y)

            fraction_x = x - x_floor
            fraction_y = y - y_floor

            intensity = 1 - min(
                fraction_x,
                fraction_y
            )

            r = int(red * intensity)
            g = int(green * intensity)
            b = int(blue * intensity)

            self.pixel(
                x_floor,
                y_floor,
                r, g, b
            )

            x += x_increment
            y += y_increment