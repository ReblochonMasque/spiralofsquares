"""
# Spiral Of Squares:

https://stackoverflow.com/questions/52433658/arrange-rectangles-in-a-spiral
"""

import random
import tkinter as tk

from anchor import Anchor
from rectangle import Rectangle

WIDTH, HEIGHT = 800, 800
CENTER = WIDTH // 2, HEIGHT // 2


class Spiral:
    """
    'right' --> add to the right side, going down
    'down'  --> add to the bottom side, going left
    'left'  --> add to the left side, going up
    'up'    --> add to tthe top side, going right

    """

    def __init__(self, anchor=CENTER, xoffset=5, yoffset=5):
        self.anchor = Anchor(*anchor)
        lr, td = self.anchor.x, self.anchor.y
        self.boundaries = {'right': lr, 'down': td, 'left': lr, 'up': td}
        self.current_x, self.current_y = self.anchor
        self.inner_boundaries = None
        self.add_to = None
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.rectangles = []
        self.turn = 0

    def add_rectangle(self, rect):
        self.rectangles.append(rect)
        num_rect = len(self.rectangles)
        if num_rect == 1:
            self.place_first(rect)
        # elif num_rect == 2:
        #     self.place_second(rect)
        else:
            self.place(rect)
            self.calc_next_add_to_side()

    def place_first(self, rect):
        """
        places the first rectangle at current anchor
        updates the anchor
        """
        self.inner_boundaries = {'right': self.anchor.x + rect.width, 'down': self.anchor.y + rect.height,
                                 'left': self.anchor.x, 'up': self.anchor.y}
        self.boundaries = {k: v for k, v in self.inner_boundaries.items()}
        self.place(rect)
        self.anchor = self.anchor + (rect.width + self.xoffset, 0)
        self.add_to = 'right'
        self.boundaries[self.add_to] += rect.width + self.xoffset

    # def place_second(self, rect):
    #     """
    #     places the first rectangle at current anchor
    #     updates the anchor
    #     """
    #     rect.calc_bbox(self.anchor.clone())
    #     self.add_to = 'right'
    #     self.turn += 1

    def place(self, rect):
        """
        places a rectangle at the current anchor, taking offsets and side into account
        """
        rect.calc_bbox(self.anchor.clone())

    def calc_next_add_to_side(self):
        """
        calculates the next anchor placement and the side we are on without worrying about offsets
        """

        w, h = self.rectangles[-1].width, self.rectangles[-1].height

        if self.turn % 4 == 0 and self.turn != 0:
            self.inner_boundaries = {k: v for k, v in self.boundaries.items()}

        if self.add_to == 'right':
            if self.current_x + w > self.inner_boundaries['right']:  # ne depasse pas la border
                self.current_x = self.inner_boundaries['right'] + w + self.xoffset
                self.current_y = self.inner_boundaries['up']
            else:
                self.turn += 1
                self.add_to = 'down'
                self.current_x = self.inner_boundaries['right'] - self.xoffset
                self.current_y = self.inner_boundaries['down'] + self.yoffset
            self.boundaries['right'] = max(self.boundaries['right'], self.inner_boundaries['right'] + w)
            self.boundaries['down'] = max(self.boundaries['down'], self.inner_boundaries['down'] + h)

        elif self.add_to == 'down':
            if self.current_y + h > self.inner_boundaries['down']:  # ne depasse pas la border
                self.current_x = self.inner_boundaries['right']
                self.current_y = self.inner_boundaries['up'] + h + self.yoffset
            else:
                self.turn += 1
                self.add_to = 'left'
                self.current_y = self.inner_boundaries['down'] + self.yoffset
                self.current_x = self.inner_boundaries['right'] - self.xoffset
            self.boundaries['left'] = min(self.boundaries['left'], self.inner_boundaries['left'] - w)
            self.boundaries['down'] = max(self.boundaries['down'], self.inner_boundaries['down'] + h)

        elif self.add_to == 'left':
            if self.current_x - w < self.inner_boundaries['left']:  # ne depasse pas la border
                self.current_x -= w + self.xoffset
                self.current_y = self.inner_boundaries['down']
            else:
                self.turn += 1
                self.add_to = 'up'
                self.current_y = self.inner_boundaries['down'] - self.yoffset
                self.current_x = self.inner_boundaries['left'] - self.xoffset
            self.boundaries['left'] = min(self.boundaries['left'], self.inner_boundaries['left'] - w)
            self.boundaries['up'] = min(self.boundaries['up'], self.inner_boundaries['up'] - h)

        elif self.add_to == 'up':
            if self.current_y - h < self.inner_boundaries['up']:  # ne depasse pas la border
                self.current_x = self.inner_boundaries['left']
                self.current_y += h - self.yoffset
            else:
                self.turn += 1
                self.add_to = 'right'
                self.current_y = self.inner_boundaries['up'] - self.yoffset
                self.current_x = self.inner_boundaries['left'] + self.xoffset
            self.boundaries['right'] = max(self.boundaries['right'], self.inner_boundaries['right'] + w)
            self.boundaries['up'] = min(self.boundaries['up'], self.inner_boundaries['up'] - h)

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