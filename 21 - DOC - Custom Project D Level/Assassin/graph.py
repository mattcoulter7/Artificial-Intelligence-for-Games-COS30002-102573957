from graphics import egi
from point2d import Point2D
from vector2d import Vector2D
from math import floor
from random import randrange

class Graph(object):
    """description of class"""
    def __init__(self,world):
        self.world = world
        # Grid
        self.scale = 60
        self.grid_size = world.cx/world.cy * self.scale
        self.height = round(world.cx / self.grid_size)
        self.width = round(world.cy / self.grid_size)
        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]

    def render(self):
        ''' Draws the grid to the screen'''
        grid = self.grid_size
        egi.white_pen()
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                x = i*grid
                y = j*grid
                pt1 = Point2D(i*grid,j*grid)
                pt2 = Point2D(pt1.x + grid,pt1.y)
                pt3 = Point2D(pt1.x,pt1.y + grid)
                egi.line_by_pos(pt1,pt2)
                egi.line_by_pos(pt1,pt3)

    def get_node(self,pt):
        ''' Returns the node of a given coordinate '''
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if floor(pt.x/self.grid_size) == i and floor(pt.y/self.grid_size) == j:
                    return Vector2D(i,j)

    def fit_pos(self,pt,type):
        ''' Takes a coord and fits it to a given place in a square '''
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if floor(pt.x/self.grid_size) == i and floor(pt.y/self.grid_size) == j:
                    if type == 'center':
                        return Vector2D(i*self.grid_size + self.grid_size/2,j*self.grid_size + self.grid_size/2)
                    elif type == 'corner':
                        return Vector2D(i*self.grid_size,j*self.grid_size)

    def get_pos(self,pt,type):
        ''' Returns the position of a node, fitted to the square '''
        return self.fit_pos(Point2D(pt.x * self.grid_size,pt.y * self.grid_size),type)

    def node_available(self,node):
        ''' returns true if node is 0 '''
        return not self.grid[node.x][node.y]

    def node_exists(self,pt):
        ''' returns true if a node is valid '''
        return pt.x in range(0,self.height) and pt.y in range(0,self.width)

    def update_grid(self,node):
        ''' 0 becomes 1 '''
        self.grid[node.x][node.y] = 1

    def rand_node(self):
        ''' returns an random node that is still available '''
        return Point2D(randrange(0,self.height),randrange(0,self.width))


