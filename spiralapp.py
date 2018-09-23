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
        self.commands_frame.pack()

        self.canvas2 = tk.Canvas(self.master, width=100, height=HEIGHT, bg='grey80')
        self.canvas2.pack(side='left', expand=True, fill='both')

        self.canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT)
        self.canvas.pack(side='left', expand=True, fill='both')

        self.spiral = Spiral()

        self.make_rectangle_collection()

        self.canvas2.bind('<ButtonRelease-1>', self.select_rectangle)

    def make_rectangle_collection(self):
        whs = [(20, 80), (20, 60), (20, 40),
               (80, 20), (60, 20), (40, 20),
               (80, 80), (60, 60), (40, 40), (20, 20),
               (80, 60), (80, 40), (60, 80), (60, 40)]
        pos = [(10, 10), (40, 10), (70, 10),
               (10, 100), (10, 130), (10, 160),
               (10, 190), (10, 280), (10, 350), (60, 350),
               (10, 400), (10, 470), (10, 520), (10, 610)]
        rectangle_models = []
        for wh, pos in zip(whs, pos):
            w, h = wh
            rect = Rectangle(w, h)
            rect.calc_bbox(Anchor(*pos))
            rectangle_models.append(rect)

        self.rectangle_models_ids2 = {}
        for rect in rectangle_models:
            tl, br = rect.norm_bbox
            self.rectangle_models_ids2[self.canvas2.create_rectangle(*tl, *br, activefill='red', outline='black', width=2)] = rect

    def select_rectangle(self, event):
        x0, y0 = event.x, event.y
        x1, y1 = x0 + 1, y0 + 1
        key = self.canvas2.find_overlapping(x0, y0, x1, y1)[0]
        print(key, self.rectangle_models_ids2[key])

    def add_rect_from_selection(self, rect):
        print(rect)

    def add_random_rect(self):
        width, height = random.randrange(10, 80), random.randrange(10, 80)
        rect = Rectangle(width, height)
        self.spiral.add_rectangle(rect)

    def draw_rectangles(self):
        for rect, color in zip(self.spiral.rectangles, SpiralApp.colors):
            tl, br = rect.norm_bbox
            self.canvas.create_rectangle(*tl, *br, fill='', outline=color, width=2)


if __name__ == '__main__':

    root = tk.Tk()
    app = SpiralApp(root)
    app.pack()
    root.mainloop()
