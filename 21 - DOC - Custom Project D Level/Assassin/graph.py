from graphics import egi
from point2d import Point2D
from vector2d import Vector2D
from math import floor
from random import randrange,choice
import pyglet

class Graph(object):
    """description of class"""
    def __init__(self,world,height,width):
        self.world = world
        # Grid
        self.grid_size = 80
        self.height = height
        self.width = width
        self.grid = [[0 for x in range(self.height)] for y in range(self.width)]
        self.image = pyglet.image.load('resources/grey_tile.png')
        self.sprites = self.init_sprites()
        self.move_compensate = Vector2D(0,0) # Keeps track of how much the screen has moved for position calculations.

    def render(self):
        ''' Draws the grid to the screen'''
        for sprite in self.sprites:
            sprite.draw()

    def init_sprites(self):
        '''Generates a list of all of the ground sprites'''
        sprites = []
        grid=self.grid_size
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 0:
                    x = i*grid
                    y = j*grid
                    sprite = pyglet.sprite.Sprite(self.image,x,y)
                    sprite.update(scale=grid/self.image.width)
                    sprites.append(sprite)
        return sprites

    def get_node(self,pt):
        ''' Returns the node of a given coordinate '''
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if floor(pt.x/self.grid_size) == i - self.move_compensate.x and floor(pt.y/self.grid_size) == j - self.move_compensate.y:
                    return Vector2D(i,j)

    def fit_pos(self,pt,type):
        ''' Takes a coord and fits it to a given place in a square '''
        x = floor(pt.x/self.grid_size)
        y = floor(pt.y/self.grid_size)
        if type == 'center':
            return Vector2D(x*self.grid_size + self.grid_size/2,y*self.grid_size + self.grid_size/2)
        elif type == 'corner':
            return Vector2D(x*self.grid_size,y*self.grid_size)

    def get_pos(self,pt,type = None):
        ''' Returns the position of a node, fitted to the square '''
        if type is not None:
            return self.fit_pos(Vector2D((pt.x - self.move_compensate.x) * self.grid_size,(pt.y - self.move_compensate.y) * self.grid_size),type)
        else:
            return Vector2D((pt.x - self.move_compensate.x) * self.grid_size + self.grid_size/2,(pt.y - self.move_compensate.y) * self.grid_size + self.grid_size/2)

    def node_available(self,node):
        ''' returns true if node is 0 '''
        return self.grid[node.x][node.y] == 0

    def node_exists(self,pt):
        ''' returns true if a node is valid '''
        return pt.x in range(0,self.height) and pt.y in range(0,self.width)

    def rand_node(self,other_node = None):
        ''' returns an random node that is still available, other node is 
        another node to avoid such as the same position as the object 
        requesting a rand_node. Range is a limited distance from other_pos '''
        node = Vector2D(randrange(0,self.height),randrange(0,self.width))
        not_self = True
        if other_node is not None:
            if node == other_node:
                not_self = False
        if self.node_available(node) and not_self:
            return node
        return self.rand_node(other_node)

    def rand_node_from_pos(self,pos,dist):
        ''' returns an random node that is still available, other node is 
        another node to avoid such as the same position as the object 
        requesting a rand_node. dist is a limited distance from other_pos '''
        x_rand = choice([i for i in range(-dist,dist) if i != 0])
        y_rand = choice([i for i in range(-dist,dist) if i != 0])
        rand_node = Vector2D(pos.x+x_rand,pos.y+y_rand)
        if self.node_exists(rand_node):
            if self.node_available(rand_node):
                return rand_node
        return self.rand_node_from_pos(pos,dist)

    def node_visible(self,node):
        ''' Returns true if the current node is visible '''
        return 0 <= node.x <= self.world.cx and 0 <= node.y <= self.world.cy


