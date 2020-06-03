from graphics import egi
from point2d import Point2D
from random import randrange
import pyglet

class Block(object):
    def __init__(self,world,type,node):
        self.type = type - 1
        self.world = world
        self.size = world.graph.grid_size
        self.pos = self.world.graph.node_to_pos(node)

        images = ['brown_block.png','grey_block.png','purple_block.png']
        self.image = pyglet.image.load('resources/' + images[self.type])
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.pos.x, y=self.pos.y)

    def render(self):
        # Render if visible
        if self.world.graph.pos_visible(pos = self.pos):
            ''' Render Sprite (more intensive)'''
            #self.sprite.update(x=self.pos.x,y=self.pos.y,scale=self.size/self.image.width)
            #self.sprite.draw()
        
            ''' Render White Square (less intensive)''' 
            egi.white_pen()
            egi.rect(self.pos.x,self.pos.y,self.pos.x + self.world.graph.grid_size,self.pos.y + self.world.graph.grid_size,filled = True)
