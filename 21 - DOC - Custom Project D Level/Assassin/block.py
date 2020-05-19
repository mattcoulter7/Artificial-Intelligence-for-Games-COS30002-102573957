from graphics import egi
from point2d import Point2D
from random import randrange

class Block(object):
    def __init__(self, world):
        self.world = world
        self.size = world.grid_size
        pt = Point2D(randrange(0,world.cx),randrange(0,world.cy))
        node = self.world.get_node(pt)
        self.pos = self.world.fit_pos(pt,'corner')
        self.world.grid[node.x][node.y] = 1
        self.shape = [
            Point2D(self.pos.x,self.pos.y),
            Point2D(self.pos.x + self.size,self.pos.y),
            Point2D(self.pos.x + self.size,self.pos.y + self.size),
            Point2D(self.pos.x,self.pos.y + self.size)
        ]

    def render(self):
        egi.white_pen()
        # draw it!
        egi.closed_shape(self.shape,filled=True)
