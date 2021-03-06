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
              'lightgreen', 'lightblue', 'gold', 'black']

    def __init__(self, master):
        self.master = master
        super().__init__(self.master)

        self.colors_used = []

        self.commands_frame = tk.Frame(self.master)
        self.add_random_rectangle_btn = tk.Button(self.commands_frame, text='Add\nRandom', command=self.add_random_rect)
        self.add_random_rectangle_btn.pack(side='left', padx=5)
        self.draw_rectangle_btn = tk.Button(self.commands_frame, text='Draw\nRect', command=self.draw_rectangles)
        self.draw_rectangle_btn.pack(side='left', padx=5)

        self.show_current_boundaries_btn = tk.Button(self.commands_frame, text='inner\nbounds', command=self.show_current_boundaries)
        self.show_current_boundaries_btn.pack(side='left', padx=5)
        self.right_boundary_line = None
        self.left_boundary_line = None
        self.top_boundary_line = None
        self.bottom_boundary_line = None
        self.show_curr_bounds = False

        self.show_boundaries_btn = tk.Button(self.commands_frame, text='outer\nbounds', command=self.show_boundaries)
        self.show_boundaries_btn.pack(side='left', padx=5)
        self.right_b_line = None
        self.left_b_line = None
        self.top_b_line = None
        self.bottom_b_line = None
        self.show_bounds = False

        self.show_anchor_points_btn = tk.Button(self.commands_frame, text='anchor\npoints', command=self.show_anchor_points)
        self.show_anchor_points_btn.pack(side='left', padx=5)
        self.show_anchor_points_flag = False
        self.anchor_points_items = []

        self.connect_center_points_btn = tk.Button(self.commands_frame, text='connect\ncenters', command=self.connect_center_points)
        self.connect_center_points_btn.pack(side='left', padx=5)
        self.connect_center_points_flag = False
        self.center_points_items = []

        self.add_50_rectangles_btn = tk.Button(self.commands_frame, text='add 50\nrectangles', command=self.add_50_rectangles)
        self.add_50_rectangles_btn.pack(side='left', padx=5)

        self.clear_btn = tk.Button(self.commands_frame, text='clear\nall', command=self.clear)
        self.clear_btn.pack(side='left', padx=5)

        self.commands_frame.pack()

        self.canvas2 = RectangleChoice(self)
        self.canvas2.pack(side='left', expand=True, fill='both')

        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg='beige')
        self.canvas.pack(side='left', expand=True, fill='both')

        self.spiral = Spiral()

        self.canvas2.bind('<ButtonRelease-1>', self.add_rect_from_selection)

    def clear(self):
        self.canvas.delete('all')

        self.right_boundary_line = None
        self.left_boundary_line = None
        self.top_boundary_line = None
        self.bottom_boundary_line = None
        self.show_curr_bounds = False

        self.right_b_line = None
        self.left_b_line = None
        self.top_b_line = None
        self.bottom_b_line = None
        self.show_bounds = False

        self.show_anchor_points_flag = False
        self.anchor_points_items = []

        self.connect_center_points_flag = False
        self.center_points_items = []

        self.spiral = Spiral()

    def add_rect_from_selection(self, event):
        rect = self.canvas2.select_rectangle(event)
        if rect is None:
            return
        w, h = rect.width, rect.height
        self.spiral.add_rectangle(Rectangle(w, h))
        self.colors_used.append(random.choice(SpiralApp.colors))
        self.draw_rectangles()

    def add_random_rect(self):
        width, height = random.randrange(5, 20), random.randrange(5, 20)
        rect = Rectangle(width, height)
        self.colors_used.append(random.choice(SpiralApp.colors))
        self.spiral.add_rectangle(rect)

    def draw_rectangles(self):
        self.canvas.delete('all')
        for rect, color in zip(self.spiral.rectangles, self.colors_used):
            tl, br = rect.norm_bbox
            self.canvas.create_rectangle(*tl, *br, fill='white', outline=color, width=2)
        self.draw_current_boundaries()
        self.draw_boundaries()
        self.draw_anchor_points()
        self.draw_center_points()

    def show_current_boundaries(self):
        self.show_curr_bounds = not self.show_curr_bounds
        self.draw_current_boundaries()

    def draw_current_boundaries(self):
        self.hide_current_boundaries()
        if self.show_curr_bounds:
            boundary = self.spiral.get_current_boundaries()
            x_ = boundary['right']
            self.right_boundary_line = self.canvas.create_line(x_, 0, x_, HEIGHT, fill='green', dash=(2, 4))
            x_ = boundary['left']
            self.left_boundary_line = self.canvas.create_line(x_, 0, x_, HEIGHT, fill='green', dash=(2, 4))
            y_ = boundary['up']
            self.top_boundary_line = self.canvas.create_line(0, y_, WIDTH, y_, fill='green', dash=(2, 4))
            y_ = boundary['down']
            self.bottom_boundary_line = self.canvas.create_line(0, y_, WIDTH, y_, fill='green', dash=(2, 4))

    def hide_current_boundaries(self):
        self.canvas.delete(self.right_boundary_line)
        self.canvas.delete(self.left_boundary_line)
        self.canvas.delete(self.top_boundary_line)
        self.canvas.delete(self.bottom_boundary_line)

    def show_boundaries(self):
        self.show_bounds = not self.show_bounds
        self.draw_boundaries()

    def draw_boundaries(self):
        self.hide_boundaries()
        if self.show_bounds:
            boundary = self.spiral.get_boundaries()
            x_ = boundary['right']
            self.right_b_line = self.canvas.create_line(x_, 0, x_, HEIGHT, fill='blue', dash=(1, 4))
            x_ = boundary['left']
            self.left_b_line = self.canvas.create_line(x_, 0, x_, HEIGHT, fill='blue', dash=(1, 4))
            y_ = boundary['up']
            self.top_b_line = self.canvas.create_line(0, y_, WIDTH, y_, fill='blue', dash=(1, 4))
            y_ = boundary['down']
            self.bottom_b_line = self.canvas.create_line(0, y_, WIDTH, y_, fill='blue', dash=(1, 4))

    def hide_boundaries(self):
        self.canvas.delete(self.right_b_line)
        self.canvas.delete(self.left_b_line)
        self.canvas.delete(self.top_b_line)
        self.canvas.delete(self.bottom_b_line)

    def show_anchor_points(self):
        self.show_anchor_points_flag = not self.show_anchor_points_flag
        self.draw_anchor_points()

    def draw_anchor_points(self):
        self.hide_anchor_points()
        if self.show_anchor_points_flag:
            anchor_points = self.spiral.get_anchor_points()
            for point in anchor_points:
                x, y = point
                x0, y0, x1, y1 = x - 2, y - 2, x + 2, y + 2
                self.anchor_points_items.append(self.canvas.create_oval(x0, y0, x1, y1))

    def hide_anchor_points(self):
        for a_point in self.anchor_points_items:
            self.canvas.delete(a_point)
        self.anchor_points_items = []

    def connect_center_points(self):
        self.connect_center_points_flag = not self.connect_center_points_flag
        self.draw_center_points()

    def draw_center_points(self):
        self.hide_center_points()
        if self.connect_center_points_flag:
            points = self.spiral.get_center_points()
            for p0, p1 in zip(points[:-1], points[1:]):
                self.center_points_items.append(self.canvas.create_line(*p0, *p1))

    def hide_center_points(self):
        for item in self.center_points_items:
            self.canvas.delete(item)
        self.center_points_items = []

    def add_50_rectangles(self, idx=50):
        if idx >= 0:
            self.add_random_rect()
            self.draw_rectangles()
            self.after(10, self.add_50_rectangles, idx-1)


if __name__ == '__main__':

    root = tk.Tk()
    app = SpiralApp(root)
    app.pack()
    root.mainloop()
