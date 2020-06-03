from vector2d import Vector2D
from matrix33 import Matrix33
from graphics import egi
from assassin import Assassin
from point2d import Point2D
from math import floor
from graph import Graph
from block import Block

class World(object):

    def __init__(self, cx, cy,map):
        # sizing
        self.cx = cx
        self.cy = cy
        # Game objects
        self.assassin = None
        self.guards = []
        self.blocks = []
        self.target = None
        # Game info
        self.paused = False
        self.show_info = True
        # Read map from file
        self.map = open(map, "r")
        self.map_name = self.map.readline()
        # Generate graph
        self.graph = Graph(self,int(self.map.readline()),int(self.map.readline()))
        # Read map data
        self.read_file()
        # Fix errors of unreachable points in the map
        self.graph.fix_grid()
        # Generate list of all available nodes for history checking
        self.graph.all_available_nodes = self.graph.generate_all_available()
        # Tolerance for automatic screen shifting
        self.shifting_tolerance = 5

    def update(self, delta):
        ''' Updates all of the world objects'''
        if not self.paused:
            for guard in self.guards:
                guard.update(delta)
        self.assassin.update(delta)

    def render(self):
        ''' Renders all of the world objects'''
        #self.graph.render()

        if self.target:
            egi.red_pen()
            egi.cross(self.target,self.graph.grid_size/4)

        for guard in self.guards:
            guard.render()

        for block in self.blocks:
            block.render()

        self.assassin.render()

    def read_file(self):
        # Loop until end of file
        with self.map as openfileobject:
            for line in openfileobject:
                # Get coordinate and type from line
                point = line.split(',')
                x = int(point[0])
                y = int(point[1])
                type = int(point[2])
                # Update the grid
                self.graph.grid[x][y] = type
                # Add blocks on non zero points
                if type != 0:
                    self.blocks.append(Block(self,type,Vector2D(x,y)))
        self.map.close()
    
    def move_screen(self,direction):
        amount = None
        if direction == 'left':
            amount = Vector2D(self.graph.grid_size,0)
            self.graph.move_compensate.x -= 1
        elif direction == 'right':
            amount = Vector2D(-self.graph.grid_size,0)
            self.graph.move_compensate.x += 1
        elif direction == 'up':
            amount = Vector2D(0,-self.graph.grid_size)
            self.graph.move_compensate.y += 1
        elif direction == 'down':
            amount = Vector2D(0,self.graph.grid_size)
            self.graph.move_compensate.y -= 1

        if self.target:
            self.target += amount

        self.assassin.pos += amount 
        if self.assassin.path._pts:
            for pt in self.assassin.path._pts:
                pt += amount

        for guard in self.guards:
            guard.pos += amount
            if guard.path._pts:
                for pt in guard.path._pts:
                    pt += amount

        for block in self.blocks:
            block.pos += amount

    def shift(self,pos):
        ''' use move_screen() based off of an object position and self.shift_tolerance
        This can only be used for the position of ONE existing object as it does not zoom in and out'''
        node = self.graph.pos_to_node(pos.copy(),relative = True)
        max = self.graph.pos_to_node(Vector2D(self.cx,self.cy),relative = True) - Vector2D(1,1) #First component is edge to the right outside of screen
        min = Vector2D(0,0)

        horizontal_tolerance = floor(max.y / self.shifting_tolerance)
        vertical_tolerance = floor(max.x / self.shifting_tolerance)

        if node.x <= min.x + horizontal_tolerance and not self.at_edge('left'):
            self.move_screen('left')
        elif node.x >= max.x - vertical_tolerance and not self.at_edge('right'):
            self.move_screen('right')
        elif node.y >= max.y - vertical_tolerance and not self.at_edge('up'):
            self.move_screen('up')
        elif node.y <= min.y + horizontal_tolerance and not self.at_edge('down'):
            self.move_screen('down')

    def at_edge(self,edge):
        bottom_left = self.graph.pos_to_node(Vector2D(0,0))
        top_right = self.graph.pos_to_node(Vector2D(self.cx,self.cy))
        if edge == 'left':
            return bottom_left.x == 0
        elif edge == 'right':
            return top_right.x == self.graph.width - 1
        elif edge == 'up':
            return top_right.y == self.graph.height - 1
        elif edge == 'down':
            return bottom_left.y == 0

    def click_on(self,pt,object):
        ''' returns an object that was clicked on '''
        for obj in getattr(self,object):
            to_obj = obj.pos - pt
            dist = to_obj.length()
            if dist < self.graph.grid_size * 2:
                return obj