#!/usr/bin/env python

from PIL import Image, ImageDraw

WHITE = 'White'
BLACK = 'Black'
RED = 'Red'
BLUE = 'Blue'
GREEN = 'Green'


class GridImageMaker:

    def __init__(self, num_x_cells, num_y_cells, cell_size_in_px=25):
        """
        Create an Image Grid Maker object
        :param num_x_cells: Number of X cells on the grid
        :param num_y_cells: Number of Y cells on the grid
        :param cell_size_in_px: Determines size of grid cell in the resulting image
        """

        self.cell_size_in_px = cell_size_in_px
        self.width = num_x_cells * cell_size_in_px
        self.height = num_y_cells * cell_size_in_px

        # Set up Image
        self.image = Image.new(mode='RGBA', size=(self.height, self.width), color=WHITE)
        self.draw = ImageDraw.Draw(self.image)

        for x in range(0, self.image.width, cell_size_in_px):
            line = ((x, 0), (x, self.image.height))
            self.draw.line(line, fill=BLACK)

        x_start = 0
        x_end = self.image.width

        for y in range(0, self.image.height, cell_size_in_px):
            line = ((x_start, y), (x_end, y))
            self.draw.line(line, fill=BLACK)

    def fill_square(self, x1, y1):
        x2 = x1 + 1
        y2 = y1 + 1
        OFFSET = 2
        x1, y1, x2, y2 = [i * self.cell_size_in_px for i in [x1, y1, x2, y2]]

        self.draw.rectangle(((x1 + OFFSET, y1 + OFFSET), (x2 - OFFSET, y2 - OFFSET)), fill=GREEN)

    def show_image(self):
        self.image.show()

    def outline_area(self, x1, y1, x2, y2):
        x1, y1, x2, y2 = [i * self.cell_size_in_px for i in [x1, y1, x2, y2]]

        line_width = int(self.cell_size_in_px / 5)
        fill = RED

        self.draw.line(((x1, y1), (x1, y2)), fill=fill, width=line_width)
        self.draw.line(((x1, y1), (x2, y1)), fill=fill, width=line_width)
        self.draw.line(((x1, y2), (x2, y2)), fill=fill, width=line_width)
        self.draw.line(((x2, y1), (x2, y2)), fill=fill, width=line_width)

    def draw_path(self, x1, y1, x2, y2):
        x1, y1, x2, y2 = [i * self.cell_size_in_px for i in [x1, y1, x2, y2]]
        fill = BLUE
        line_width = int(self.cell_size_in_px / 2)
        x1, y1, x2, y2 = [i + line_width for i in [x1, y1, x2, y2]]
        self.draw.line(((x1, y1), (x2, y2)), fill=fill, width=line_width)
