from graphics import egi
from point2d import Point2D
from random import randrange
import pyglet

class Block(object):
    def __init__(self, world,type):
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
        images = ['brown_block.png','grey_block.png','purple_block.png']
        self.image = pyglet.image.load('resources/' + images[type])
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.pos.x, y=self.pos.y)

    def render(self):
        self.sprite.update(x=self.pos.x,y=self.pos.y,scale=self.size/self.image.width)
        self.sprite.draw()
