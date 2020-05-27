from graphics import egi
from point2d import Point2D
from random import randrange
import pyglet

class Block(object):
    def __init__(self,world,type,node):
        self.type = type - 1
        self.world = world
        self.size = world.graph.grid_size
        self.pos = self.world.graph.get_pos(node,'corner')

        images = ['brown_block.png','grey_block.png','purple_block.png']
        self.image = pyglet.image.load('resources/' + images[self.type])
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.pos.x, y=self.pos.y)

    def render(self):
        self.sprite.update(x=self.pos.x,y=self.pos.y,scale=self.size/self.image.width)
        self.sprite.draw()
