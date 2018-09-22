"""
The coordinates at which a rectangle is anchored on canvas

"""


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

    def clone(self):
        return Anchor(self.x, self.y)


if __name__ == '__main__':
    pass
