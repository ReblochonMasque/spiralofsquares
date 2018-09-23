"""
a Rectangle
"""

from anchor import Anchor


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        center = self.width//2, self.height//2
        self.bbox = [Anchor(*center) + (-self.width//2, -self.height//2),
                     Anchor(*center) + (self.width//2, self.height//2)]
        self.norm_bbox = None
        self.normalize_bbox()

    def calc_bbox(self, anchor):
        x, y = anchor
        self.bbox = [Anchor(anchor.x, anchor.y), (x + self.width, y + self.height)]
        self.normalize_bbox()

    def normalize_bbox(self):
        """
        set the anchor point to the top left corner of the bbox
        :return:
        """
        p0, p1 = self.bbox
        x0, y0 = p0
        x1, y1 = p1
        self.norm_bbox = [Anchor(min(x0, x1), min(y0, y1)), Anchor(max(x0, x1), max(y0, y1))]
        # self.bbox = [Anchor(min(x0, x1), min(y0, y1)), Anchor(max(x0, x1), max(y0, y1))]

    def get_corners(self):
        tl, br = self.bbox
        tr = br[0], tl[1]
        bl = tl[0], br[1]
        return tl, tr, br, bl

    def get_center(self):
        tl, br = self.bbox
        return tl.get_mid(br)


if __name__ == '__main__':
    pass
