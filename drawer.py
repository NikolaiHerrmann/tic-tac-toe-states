
import drawsvg as draw


class Drawer:

    def __init__(self, box_dim=60):
        self.box_dim = box_dim
        self.border = box_dim
        
        # Hacky dimensions (66 x 83 = 5478)
        width = ((box_dim * 3.505) * 66)
        height = ((box_dim * 3.505) * 83)

        self.d = draw.Drawing(width, height)
        self.d.append(draw.Rectangle(0, 0, width, height, fill="white")) # background

        self.init_cross()
        self.init_circle()
        self.init_grid()

    def init_cross(self):
        cross_length = self.box_dim / 2
        self.cross_length_half = cross_length / 2
        self.cross_shape = draw.Group(stroke_linecap="round")
        self.cross_shape.append(draw.Line(cross_length, cross_length, 0, 0))
        self.cross_shape.append(draw.Line(0, cross_length, cross_length, 0))

    def init_circle(self):
        circle_radius = self.box_dim / 3.5
        self.circle_shape = draw.Circle(0, 0, circle_radius)

    def init_grid(self):
        length = self.box_dim * 3

        self.grid = draw.Group()

        box = draw.Rectangle(0, 0, length, length)
        length_third = length / 3
        length_two_third = length * (2 / 3)

        line_1 = draw.Line(length_third, 0, length_third, length)
        line_2 = draw.Line(length_two_third, 0, length_two_third, length)
        line_3 = draw.Line(0, length_third, length, length_third)
        line_4 = draw.Line(0, length_two_third, length, length_two_third)

        shapes = [box, line_1, line_2, line_3, line_4]
        for shape in shapes:
            self.grid.append(shape)

    def get_game(self, x, y, xs, os):
        game = draw.Group(transform=f"translate({x}, {y})")
        game.append(draw.Use(self.grid, 0, 0))

        x = self.box_dim / 2
        y = self.box_dim / 2
        x_count = 0
        idx = 1

        while idx < 0b1000000000:
            if xs & idx:
                cross = draw.Use(self.cross_shape, x - self.cross_length_half, y - self.cross_length_half)
                game.append(cross)
            elif os & idx:
                circle = draw.Use(self.circle_shape, x, y)
                game.append(circle)

            if x_count == 2:
                x = self.box_dim / 2
                y += self.box_dim
                x_count = 0
            else:
                x += self.box_dim
                x_count += 1

            idx <<= 1

        return game
    
    def draw(self, states, output_name):
        poster = draw.Group(stroke="black", stroke_width=3, fill="none")

        x = self.box_dim / 2
        y = self.box_dim / 2
        x_count = 0
        game_size = (self.box_dim * 3) + (self.border / 2)

        for xs, os, _ in states:
            game = self.get_game(x, y, xs, os)
            poster.append(game)
            
            if x_count == 66 - 1:
                x = self.box_dim / 2
                y += game_size
                x_count = 0
            else:
                x += game_size
                x_count += 1

        self.d.append(poster)
        self.d.save_svg(f"{output_name}.svg")
        return self.d
