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
        self.all_available_nodes = None
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
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 0:
                    x = i*grid
                    y = j*grid
                    sprite = pyglet.sprite.Sprite(self.image,x,y)
                    sprite.update(scale=grid/self.image.width)
                    sprites.append(sprite)
        return sprites

    #---------------------------------------------------------------------

    def restrict_point_to_grid(self,pt):
        ''' if a pt is outside of the grid, it will bring it back into the grid '''
        if pt.x < 0:
            pt.x = 0
        elif pt.x > self.width:
            pt.x = self.width
        if pt.y < 0:
            pt.y = 0
        elif pt.y > self.height:
            pt.y = self.height
        return pt

    def relative_to_global(self,node):
        ''' a position on the screen will be converted to position on grid 
        I.E. a position of (1,2) on screen to be accurate would assume that position (0,0) is in the bottom left of the screen
        Because this isn't always the case, it will use move_compensate to compensate for this'''
        node.x += self.move_compensate.x
        node.y += self.move_compensate.y
        return node

    def global_to_relative(self,node):
        ''' Achieves the opposite of relative_to_global '''
        node.x -= self.move_compensate.x
        node.y -= self.move_compensate.y
        return node

    def pos_to_node(self,pos,relative = False):
        ''' Returns the restricted node of a given coordinate, return global node by default'''
        pos.x = floor(pos.x/self.grid_size)
        pos.y = floor(pos.y/self.grid_size)
        if not relative:
            pos = self.relative_to_global(pos)
        return self.restrict_point_to_grid(pos)

    def node_to_pos(self,node,type = None):
        ''' Returns the position of a node, fitted to the square '''
        node.x *= self.grid_size
        node.y *= self.grid_size
        if type == 'center':
            node.x += self.grid_size/2
            node.y += self.grid_size/2
        return node

    def fit_pos_to(self,pos,type = None,relative = False):
        ''' Takes a coord and fits it to a given place in a square '''
        pos = self.pos_to_node(pos,relative)
        pos = self.node_to_pos(pos,type)
        return pos

    def node_available(self,node):
        ''' returns true if node is 0 '''
        if self.node_exists(node):
            return self.grid[node.x][node.y] == 0
        return False

    def node_exists(self,pt):
        ''' returns true if a node is valid '''
        return pt.x in range(0,self.width) and pt.y in range(0,self.height)

    def node_visible(self,node):
        ''' Returns true if the current node is visible '''
        return 0 <= node.x <= self.world.cx and 0 <= node.y <= self.world.cy

    def rand_node(self,avoid = None):
        ''' returns an random node that is still available, other node is 
        another node to avoid such as the same position as the object 
        requesting a rand_node. Range is a limited distance from other_pos '''
        node = Vector2D(randrange(0,self.width),randrange(0,self.height))
        not_self = True
        if avoid is not None:
            if node == avoid:
                not_self = False
        if self.node_available(node) and not_self:
            return node
        return self.rand_node(avoid)

    def rand_node_from_pos(self,pos,dist):
        ''' returns an random node that is still available, other node is 
        another node to avoid such as the same position as the object 
        requesting a rand_node. dist is a limited distance from other_pos '''
        x_rand = choice([i for i in range(-dist,dist) if i not in range(-1,1)])
        y_rand = choice([i for i in range(-dist,dist) if i not in range(-1,1)])
        rand_node = Vector2D(pos.x+x_rand,pos.y+y_rand)
        rand_node = self.restrict_point_to_grid(rand_node)
        if self.node_available(rand_node):
            return rand_node
        return self.rand_node_from_pos(pos,dist)

    def rand_node_from_list(self,list):
        ''' Generates a random node from a provided list '''
        choice = randrange(len(list))
        return list[choice]

    def fix_grid(self):
        ''' automatically replaces any points that can't be travelled to with 1 '''
        adjacent = [(1,0),(0,1),(-1,0),(0,-1)]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                update = True # Assume update
                node = Vector2D(i,j)
                print(node)
                for pt in adjacent:
                    new_node = Vector2D(node.x+pt[0],node.y+pt[1])
                    if self.node_available(new_node):
                        update = False # Update not required
                if update:
                    self.grid[i][j] = -1
    def generate_all_available(self):
        ''' generates a list of all nodes that are available '''
        available = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                node = Vector2D(i,j)
                if self.node_available(node):
                    available.append(node)
        return available
