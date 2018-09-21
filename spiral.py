"""
# Spiral Of Squares:

https://stackoverflow.com/questions/52433658/arrange-rectangles-in-a-spiral
"""

import random
import tkinter as tk

WIDTH, HEIGHT = 800, 800
CENTER = WIDTH // 2, HEIGHT // 2


class Anchor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Anchor(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        return Anchor(self.x - other[0], self.y - other[1])

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, idx):
        a = (self.x, self.y)
        return a[idx]


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bbox = [Anchor(*CENTER), Anchor(*CENTER) + (self.width, self.height)]
        self.norm_bbox = None
        self.normalize_bbox()

    def calc_bbox(self, anchor):
        x, y = anchor
        self.bbox = [Anchor(anchor.x, anchor.y), (x + self.width, y + self.height)]
        self.normalize_bbox()

    def normalize_bbox(self):
        p0, p1 = self.bbox
        x0, y0 = p0
        x1, y1 = p1
        self.norm_bbox = [Anchor(min(x0, x1), min(y0, y1)), Anchor(max(x0, x1), max(y0, y1))]

    #         self.bbox = [Anchor(min(x0, x1), min(y0, y1)), Anchor(max(x0, x1), max(y0, y1))]
    def get_corners(self):
        tl, br = self.bbox
        tr = br[0], tl[1]
        bl = tl[0], br[1]
        return tl, tr, br, bl


class Spiral:
    def __init__(self, anchor=CENTER, direction='right', xoff=5, yoff=5):
        self.anchor = Anchor(*anchor)
        self.next_anchors = {'right': self.anchor, 'down': self.anchor, 'left': self.anchor, 'up': self.anchor}
        lr, td = self.anchor.x, self.anchor.y
        self.boundaries = {'right': lr, 'down': td, 'left': lr, 'up': td}
        self.current_x, self.current_y = self.anchor
        self.turn_boundaries = None
        self.direction = direction
        self.xoff = xoff
        self.yoff = yoff
        self.rectangles = []
        self.turn = 0

    def add_rectangle(self, rect):
        self.rectangles.append(rect)
        rect.calc_bbox(self.anchor)  # place at correct anchor
        self.calc_next_direction()

    def calc_next_direction(self):
        w, h = self.rectangles[-1].width, self.rectangles[-1].height

        if self.turn == 0:
            self.turn_boundaries = {'right': self.anchor.x + w, 'down': self.anchor.y + h,
                                    'left': self.anchor.x, 'up': self.anchor.y}

        if self.turn % 4 == 0:
            self.turn_boundaries = {k: v for k, v in self.boundaries.items()}

        if self.direction == 'right':
            if self.current_x + w > self.turn_boundaries['right']:  # ne depasse pas la border
                self.current_x = self.turn_boundaries['right'] + w + self.xoff
                self.current_y = self.turn_boundaries['up']
            else:
                self.turn += 1
                self.direction = 'down'
                self.current_x = self.turn_boundaries['right'] - self.xoff
                self.current_y = self.turn_boundaries['up'] + self.yoff
            self.boundaries['right'] = max(self.boundaries['right'], self.turn_boundaries['right'] + w)
            self.boundaries['down'] = max(self.boundaries['down'], self.turn_boundaries['down'] + h)

        elif self.direction == 'down':
            if self.current_y + h > self.turn_boundaries['down']:  # ne depasse pas la border
                self.current_x = self.turn_boundaries['right']
                self.current_y = self.turn_boundaries['up'] + h + self.yoff
            else:
                self.turn += 1
                self.direction = 'left'
                self.current_y = self.turn_boundaries['down'] + self.yoff
                self.current_x = self.turn_boundaries['right'] - self.xoff
            self.boundaries['left'] = min(self.boundaries['left'], self.turn_boundaries['left'] - w)
            self.boundaries['down'] = max(self.boundaries['down'], self.turn_boundaries['down'] + h)

        elif self.direction == 'left':
            if self.current_x - w < self.turn_boundaries['left']:  # ne depasse pas la border
                self.current_x -= w + self.xoff
                self.current_y = self.turn_boundaries['down']
            else:
                self.turn += 1
                self.direction = 'up'
                self.current_y = self.turn_boundaries['down'] - self.yoff
                self.current_x = self.turn_boundaries['left'] - self.xoff
            self.boundaries['left'] = min(self.boundaries['left'], self.turn_boundaries['left'] - w)
            self.boundaries['up'] = min(self.boundaries['up'], self.turn_boundaries['up'] - h)

        elif self.direction == 'up':
            if self.current_y - h < self.turn_boundaries['up']:  # ne depasse pas la border
                self.current_x = self.turn_boundaries['left']
                self.current_y += h - self.yoff
            else:
                self.turn += 1
                self.direction = 'right'
                self.current_y = self.turn_boundaries['up'] - self.yoff
                self.current_x = self.turn_boundaries['left'] + self.xoff
            self.boundaries['right'] = max(self.boundaries['right'], self.turn_boundaries['right'] + w)
            self.boundaries['up'] = min(self.boundaries['up'], self.turn_boundaries['up'] - h)

        self.anchor = Anchor(self.current_x, self.current_y)


if __name__ == '__main__':

    cr = 1
    num_rect = 0
    if cr:
        num_rect = 4
    else:
        num_rect = 14
    rectangles = [Rectangle(random.randrange(20, 100), random.randrange(20, 100)) for _ in range(num_rect)]

    spiral = Spiral()
    for rect in rectangles:
        spiral.add_rectangle(rect)

    root = tk.Tk()
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack(expand=True, fill='both')

    if cr:
        for rect, color in zip(spiral.rectangles, ['blue', 'red', 'green', 'black']):
            tl, br = rect.norm_bbox
            canvas.create_rectangle(*tl, *br, fill='', outline=color, width=2)
            x, y = tl
            canvas.create_oval(x + 2, y + 2, x - 2, y - 1)
    else:
        for rect in spiral.rectangles:
            tl, br = rect.norm_bbox
            canvas.create_rectangle(*tl, *br, fill='', outline='black', width=2)
            x, y = tl
            canvas.create_oval(x + 2, y + 2, x - 2, y - 1)

    root.mainloop()