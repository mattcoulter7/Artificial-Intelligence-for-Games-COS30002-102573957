from graphics import egi
from point2d import Point2D

class Block(object):

    def __init__(self, size,x,y):
        self.size = size
        self.pos = Point2D(x,y)
        self.shape = [
            Point2D(x,y),
            Point2D(x+size,y),
            Point2D(x+size,y+size),
            Point2D(x,y+size)
        ]

    def render(self):
        egi.white_pen()
        egi.closed_shape(self.shape,filled=True)
