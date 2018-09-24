"""
a tkinter app showing rectangles arranged in a spiral

"""

import random
import tkinter as tk

from anchor import Anchor
from rectangle import Rectangle
from spiral import Spiral


WIDTH, HEIGHT = 800, 800
CENTER = WIDTH // 2, HEIGHT // 2


class RectangleChoice(tk.Canvas):
    whs = [(20, 80), (20, 60), (20, 40),
           (80, 20), (60, 20), (40, 20),
           (80, 80), (60, 60), (40, 40), (20, 20),
           (80, 60), (80, 40), (60, 80), (60, 40)]
    pos = [(10, 10), (40, 10), (70, 10),
           (10, 100), (10, 130), (10, 160),
           (10, 190), (10, 280), (10, 350), (60, 350),
           (10, 400), (10, 470), (10, 520), (10, 610)]

    def __init__(self, master):
        self.master = master
        super().__init__(self.master, width=100, height=HEIGHT, bg='grey80')
        self.rectangle_models_ids2 = {}
        self.make_rectangle_collection()

    def make_rectangle_collection(self):

        rectangle_models = []
        for wh, pos in zip(RectangleChoice.whs, RectangleChoice.pos):
            w, h = wh
            rect = Rectangle(w, h)
            rect.calc_bbox(Anchor(*pos))
            rectangle_models.append(rect)

        for rect in rectangle_models:
            tl, br = rect.norm_bbox
            self.rectangle_models_ids2[self.create_rectangle(*tl, *br, activefill='red', outline='black', width=2)] = rect

    def select_rectangle(self, event):
        x0, y0 = event.x, event.y
        x1, y1 = x0 + 1, y0 + 1
        rect = None
        try:
            key = self.find_overlapping(x0, y0, x1, y1)[0]
            rect = self.rectangle_models_ids2[key]
        except IndexError:   # case of click in an empty space of the canvas
            pass
        return rect


class SpiralApp(tk.Frame):

    colors = ['blue', 'red', 'green', 'black', 'cyan', 'grey', 'purple',
              'lightgreen', 'lightblue', 'gold', 'black', 'blue', 'red',
              'green', 'black', 'cyan', 'grey', 'purple']

    def __init__(self, master):
        self.master = master
        super().__init__(self.master)

        self.commands_frame = tk.Frame(self.master)
        self.add_random_rectangle_btn = tk.Button(self.commands_frame, text='Add\nRandom', command=self.add_random_rect)
        self.add_random_rectangle_btn.pack(side='left', padx=5)
        self.draw_rectangle_btn = tk.Button(self.commands_frame, text='Draw\nRect', command=self.draw_rectangles)
        self.draw_rectangle_btn.pack(side='left', padx=5)

        self.show_current_boundaries = tk.Button(self.commands_frame, text='inner\nbounds', command=self.show_current_boundaries)
        self.show_current_boundaries.pack(side='left', padx=5)
        self.right_boundary_line = None
        self.left_boundary_line = None
        self.top_boundary_line = None
        self.bottom_boundary_line = None
        self.show_curr_bounds = False

        self.commands_frame.pack()

        self.canvas2 = RectangleChoice(self)
        self.canvas2.pack(side='left', expand=True, fill='both')

        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(side='left', expand=True, fill='both')

        self.spiral = Spiral()

        self.canvas2.bind('<ButtonRelease-1>', self.add_rect_from_selection)

    def add_rect_from_selection(self, event):
        rect = self.canvas2.select_rectangle(event)
        if rect is None:
            return
        print(rect)
        w, h = rect.width, rect.height
        self.spiral.add_rectangle(Rectangle(w, h))
        self.draw_rectangles()
        self.draw_current_boundaries()

    def add_random_rect(self):
        width, height = random.randrange(10, 80), random.randrange(10, 80)
        rect = Rectangle(width, height)
        self.spiral.add_rectangle(rect)

    def draw_rectangles(self):
        self.canvas.delete('all')
        for rect, color in zip(self.spiral.rectangles, SpiralApp.colors):
            tl, br = rect.norm_bbox
            self.canvas.create_rectangle(*tl, *br, fill='', outline=color, width=2)

    def show_current_boundaries(self):
        self.show_curr_bounds = not self.show_curr_bounds
        self.draw_current_boundaries()

    def draw_current_boundaries(self):
        self.hide_current_boundaries()
        if self.show_curr_bounds:
            boundary = self.spiral.get_current_boundaries()
            x_ = boundary['right']
            self.right_boundary_line = self.canvas.create_line(x_, 0, x_, HEIGHT, fill='lightgreen')
            x_ = boundary['left']
            self.left_boundary_line = self.canvas.create_line(x_, 0, x_, HEIGHT, fill='lightgreen')
            y_ = boundary['up']
            self.top_boundary_line = self.canvas.create_line(0, y_, WIDTH, y_, fill='lightgreen')
            y_ = boundary['down']
            self.bottom_boundary_line = self.canvas.create_line(0, y_, WIDTH, y_, fill='lightgreen')

    def hide_current_boundaries(self):
        self.canvas.delete(self.right_boundary_line)
        self.canvas.delete(self.left_boundary_line)
        self.canvas.delete(self.top_boundary_line)
        self.canvas.delete(self.bottom_boundary_line)


if __name__ == '__main__':

    root = tk.Tk()
    app = SpiralApp(root)
    app.pack()
    root.mainloop()
