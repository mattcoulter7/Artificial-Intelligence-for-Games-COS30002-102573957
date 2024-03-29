import pyglet
from vector2d import Vector2D
from matrix33 import Matrix33
from graphics import egi
from assassin import Assassin
from guard import Guard
from point2d import Point2D
from math import floor
from graph import Graph
from block import Block
from random import randrange
import os

class World(object):

    def __init__(self, cx, cy,map):
        # sizing
        self.cx = cx
        self.cy = cy
        self.main_batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)
        # Game objects
        self.assassin = None
        self.num_guards = None
        self.guards = []
        self.blocks = []
        self.target = None
        # Game info
        self.paused = False
        self.show_info = True
        # Read map from file
        self.map = open(map, "r")
        self.map_name = self.map.readline().rstrip()
        # Generate graph
        self.graph = Graph(self,int(self.map.readline()),int(self.map.readline()))
        # Read map data
        self.read_file()
        # Tolerance for automatic screen shifting
        self.shifting_tolerance = 5
        # Score graphics
        target = pyglet.image.load('resources/target.png')
        self.target_spr = pyglet.sprite.Sprite(img=target,x=15,y=self.cy - 80,batch=self.main_batch,group = self.foreground)
        self.label = pyglet.text.Label('{}/{}'.format(self.num_guards-len(self.guards),self.num_guards),
            font_name='Arial Black',
            font_size=36,
            x=100,y=self.cy - 65,
            batch=self.main_batch,
            group = self.foreground)

    def update(self, delta):
        ''' Updates all of the world objects'''
        if not self.paused:
            # Check for win or loss
            if self.assassin.alive and self.remaining_guards() == 0:
                self.next_level()
            elif not self.assassin.alive and self.remaining_guards():
                self.restart_level()
            # Update
            for guard in self.guards:
                guard.update(delta)
            self.assassin.update(delta)

    def render(self):
        ''' Renders all of the world objects'''
        # Update the sprites
        for block in self.blocks:
            block.update_sprite()
        self.target_spr.update(y=self.cy - 80)
        self.label.y = self.cy - 65
        self.label.text = '{}/{}'.format(self.num_guards-len(self.guards),self.num_guards)
        # Draw most sprites at once
        self.main_batch.draw()
        # Target
        if self.target:
            egi.red_pen()
            egi.cross(self.target,self.graph.grid_size/4)
        # Guards
        for guard in self.guards:
            guard.render()
        # Assassin
        self.assassin.render()
    
    def move_screen(self,direction):
        ''' Move all of the objects in a particular direction '''
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
        ''' Returns true when the screen sees the edge of the map '''
        bottom_left = self.graph.pos_to_node(Vector2D(0,0))
        top_right = self.graph.pos_to_node(Vector2D(self.cx,self.cy))
        if edge == 'left':
            return bottom_left.x == 0
        elif edge == 'right':
            return top_right.x == self.graph.width
        elif edge == 'up':
            return top_right.y == self.graph.height
        elif edge == 'down':
            return bottom_left.y == 0

    def click_on(self,pt,object):
        ''' returns an object that was clicked on '''
        for obj in getattr(self,object):
            to_obj = obj.pos - pt
            dist = to_obj.length()
            if dist < self.graph.grid_size * 2:
                return obj

    def read_file(self):
        # Loop until end of file
        with self.map as openfileobject:
            for line in openfileobject:
                # Get coordinate and type from line
                point = line.split(',')
                key = point[0]
                if key == 'assassin':
                    self.assassin = Assassin(self,int(point[1]),int(point[2]))
                elif key == 'guard':
                    self.guards.append(Guard(self,int(point[1]),int(point[2])))
                elif key == 'num_guards':
                    self.num_guards = int(point[1])
                elif key in ['tile','block']:
                    x = int(point[1])
                    y = int(point[2])
                    type = int(point[3])
                    self.graph.grid[x][y] = type
                    self.blocks.append(Block(self,type,Vector2D(x,y)))
                elif key == 'map_done':
                    # Fix errors of unreachable points in the map
                    self.graph.fix_grid()
                    # Generate list of all available nodes for history checking
                    self.graph.all_available_nodes = self.graph.generate_all_available()
        self.map.close()

    def remaining_guards(self):
        return len(self.guards)

    def restart_level(self):
        self.__init__(self.cx,self.cy,'maps/{}.csv'.format(self.map_name))

    def next_level(self):
        map_count = len([name for name in os.listdir('maps')])
        self.__init__(self.cx,self.cy,'maps/map{}.csv'.format(randrange(0,map_count - 1)))