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
    states:
    'right' --> add to the right side, going down
    'down'  --> add to the bottom side, going left
    'left'  --> add to the left side, going up
    'up'    --> add to tthe top side, going right

    """

    def __init__(self, anchor=CENTER, xoffset: int=5, yoffset: int=5):
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
        self.anchor_points = [self.anchor.clone()]

    def add_rectangle(self, rect):
        self.rectangles.append(rect)
        if len(self.rectangles) == 1:
            self.place_first(rect)
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
        rect.calc_bbox(self.anchor.clone())
        self.anchor = self.anchor + (rect.width + self.xoffset, 0)
        self.add_to = 'right'
        self.boundaries['right'] += rect.width + self.xoffset
        self.boundaries['down'] += rect.height + self.yoffset
        self.anchor_points.append(self.anchor.clone())

    def place(self, rect):
        """
        places a rectangle at the current anchor, taking offsets and side into account
        """
        w, h = rect.width, rect.height
        anchor = self.anchor.clone()

        if self.add_to == 'right':
            rect.calc_bbox(anchor)

        if self.add_to == 'down':
            anchor = anchor + (-w, 0)
            rect.calc_bbox(anchor)
            self.anchor = self.anchor + (-w, 0)

        if self.add_to == 'left':
            anchor = anchor + (-w, -h)
            rect.calc_bbox(anchor)
            self.anchor = self.anchor + (-w, -h)

        if self.add_to == 'up':
            anchor = anchor + (0, -h)
            rect.calc_bbox(anchor)
            self.anchor = self.anchor + (w, -h)

    def calc_next_add_to_side(self):
        """
        calculates the next anchor placement and the side we are on.
        updates the inner_boundary each full turn cycle
        updates the boundary each new rectangle (used to update inner at next turn cycle)

        """

        w, h = self.rectangles[-1].width, self.rectangles[-1].height
        current_x, current_y = self.anchor

        if self.add_to == 'right':
            if current_y + h < self.inner_boundaries['down']:  # ne depasse pas la border
                current_x = self.inner_boundaries['right'] + self.xoffset
                current_y += h + self.yoffset
            else:
                self.add_to = 'down'
                current_x += self.xoffset
                self.turn += 1
                current_x = self.inner_boundaries['right']
                current_y = self.inner_boundaries['down'] + self.yoffset
            self.boundaries['right'] = max(self.boundaries['right'], self.inner_boundaries['right'] + w)
            self.boundaries['down'] = max(self.boundaries['down'], self.inner_boundaries['down'] + h)
            self.inner_boundaries['left'] = self.boundaries['left']

        elif self.add_to == 'down':
            if current_x > self.inner_boundaries['left']:  # ne depasse pas la border
                current_x -= self.xoffset
            else:
                self.turn += 1
                self.add_to = 'left'
                current_x = self.inner_boundaries['left'] - self.xoffset
                current_y = self.inner_boundaries['down']
            self.boundaries['down'] = max(self.boundaries['down'], self.inner_boundaries['down'] + h)
            self.boundaries['left'] = min(self.boundaries['left'], self.inner_boundaries['left'] - w)
            self.inner_boundaries['up'] = self.boundaries['up']

        elif self.add_to == 'left':
            if current_y > self.inner_boundaries['up']:  # ne depasse pas la border
                current_x = self.inner_boundaries['left'] - self.xoffset
                current_y -= self.yoffset
            else:
                self.turn += 1
                self.add_to = 'up'
                current_x = self.inner_boundaries['left']
                current_y = self.inner_boundaries['up'] - self.yoffset
            self.boundaries['left'] = min(self.boundaries['left'], self.inner_boundaries['left'] - w)
            self.boundaries['up'] = min(self.boundaries['up'], self.inner_boundaries['up'])
            self.inner_boundaries['right'] = self.boundaries['right']

        elif self.add_to == 'up':
            if current_x < self.inner_boundaries['right']:  # ne depasse pas la border
                current_x = current_x + self.xoffset
                current_y = self.inner_boundaries['up'] - self.yoffset
            else:
                self.turn += 1
                self.add_to = 'right'
                print('one turn completed, reset to first anchor')
                current_x = self.inner_boundaries['right'] + self.xoffset
                current_y = self.inner_boundaries['up']
            self.boundaries['up'] = min(self.boundaries['up'], self.inner_boundaries['up'] - h)
            self.boundaries['right'] = max(self.boundaries['right'], self.inner_boundaries['right'] + w)
            self.inner_boundaries['down'] = self.boundaries['down']

        self.anchor = Anchor(current_x, current_y)
        self.anchor_points.append(self.anchor.clone())

    def get_current_boundaries(self):
        return self.inner_boundaries

    def get_boundaries(self):
        return self.boundaries

    def get_anchor_points(self):
        return self.anchor_points


if __name__ == '__main__':

    cr = 1
    if cr:
        num_rect = 18
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
        for idx, (rect, color) in enumerate(zip(spiral.rectangles, ['blue', 'red', 'green', 'black', 'cyan', 'grey', 'purple',\
                'lightgreen', 'lightblue', 'gold', 'black', 'blue', 'red', 'green', 'black', 'cyan', 'grey', 'purple'])):
            tl, br = rect.norm_bbox
            canvas.create_rectangle(*tl, *br, fill='', outline=color, width=2)
            x, y = tl
            canvas.create_oval(x + 2, y + 2, x - 2, y - 1)
            print(*rect.get_center())
            canvas.create_text(*rect.get_center(), text=str(idx))
    else:
        for idx, rect in enumerate(spiral.rectangles):
            tl, br = rect.norm_bbox
            canvas.create_rectangle(*tl, *br, fill='', outline='black', width=2)
            x, y = tl
            canvas.create_oval(x + 2, y + 2, x - 2, y - 1)
            print(*rect.get_center())
            canvas.create_text(*rect.get_center(), text=str(idx))

    root.mainloop()
