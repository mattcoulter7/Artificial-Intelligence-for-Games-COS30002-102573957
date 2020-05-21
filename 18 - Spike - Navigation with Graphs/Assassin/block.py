from graphics import egi
from point2d import Point2D
from random import randrange

class Block(object):
    def __init__(self, world):
        self.world = world
        self.size = world.graph.grid_size
        node = self.world.graph.rand_node()
        self.pos = self.world.graph.get_pos(node,'corner')
        self.world.graph.update_grid(node)
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
