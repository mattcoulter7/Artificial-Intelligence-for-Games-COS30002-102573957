from graphics import egi
from point2d import Point2D
from random import randrange
import pyglet

class Block(object):
    def __init__(self,world,type,node):
        self.type = type
        self.world = world
        self.size = world.graph.grid_size
        self.pos = self.world.graph.node_to_pos(node)

        images = ['grey_tile.png','brown_block.png','grey_block.png','purple_block.png']
        self.image = pyglet.image.load('resources/' + images[self.type])
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.pos.x, y=self.pos.y,batch=self.world.main_batch,group=self.world.background)

    def update_sprite(self):
        # Resize the sprite
        if self.world.graph.pos_visible(pos = self.pos):
            if self.sprite.batch != self.world.main_batch:
                self.sprite.batch = self.world.main_batch
            self.sprite.update(x=self.pos.x,y=self.pos.y,scale=self.size/self.image.width)
        else: # Don't render if not visible
            self.sprite.batch = None
