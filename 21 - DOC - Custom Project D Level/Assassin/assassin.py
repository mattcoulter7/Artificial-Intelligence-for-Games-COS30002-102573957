from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians, pi
from random import random, randrange, uniform
from path import Path
from node import Node

class Assassin(object):

    def __init__(self, world=None, scale=30.0, mode=None):
        # keep a reference to the world object
        self.world = world
        self.mode = mode

        # where am i and where am i going? random start pos
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of Assassin size

        # data for drawing this Assassin
        self.color = 'WHITE'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]

        # speed limiting code
        self.max_speed = 20.0 * scale

        # Path
        self.path = Path()

        # debug draw info?
        self.show_info = True

    def calculate(self):
        # calculate the current steering force
        mode = self.mode
        vel = Vector2D(0,0)
        if self.mode == 'follow_path':
            vel = self.follow_path()
        return vel

    def update(self, delta):
        ''' update vehicle position and orientation '''
        # update mode if necessary
        self.update_mode()

        # new velocity
        self.vel = self.calculate()
        # limit velocity
        self.vel.truncate(self.max_speed)
        # update position
        self.pos += self.vel * delta

        # update heading is non-zero velocity (moving)
        if self.vel.length_sq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()

        if self.world.target:
            if self.intersect_pos(self.world.target):
                self.world.target = None
                self.path.clear()

    def update_mode(self):
        ''' Updates state according to different variables '''
        if self.path._pts:
            self.mode = 'follow_path'
        else:
            self.mode = None

    def render(self, color=None):
        ''' Draw the triangle Assassin with color'''
        # draw the ship
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)

        #if self.path._pts:
            #self.path.render()

    def speed(self):
        return self.vel.length()

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return desired_vel

    def follow_path(self):
        if (self.path.is_finished()):
            # Arrives at the final waypoint 
            return self.seek(self.path._pts[-1])
        else:
            # Goes to the current waypoint and increments on arrival
            if self.intersect_pos(self.path.current_pt()):
                self.path.inc_current_pt()
            return self.seek(self.path.current_pt())

    def intersect_pos(self,pos):
        ''' Returns true if assassin intersects a particular position'''
        return self.world.get_node(pos) == self.world.get_node(self.pos)

    def astar(self, maze, start, end):
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

                # Get node position
                node_position = Vector2D(current_node.position.x + new_position[0], current_node.position.y + new_position[1])

                # Make sure within range
                if node_position.x > (len(maze) - 1) or node_position.x < 0 or node_position.y > (len(maze[len(maze)-1]) -1) or node_position.y < 0:
                    continue

                # Make sure walkable terrain
                if maze[node_position.x][node_position.y] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position.x - end_node.position.x) ** 2) + ((child.position.y - end_node.position.y) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)

    def update_path(self):
        maze = self.world.grid
        start = self.world.get_node(self.pos)
        end = self.world.get_node(self.world.target)

        if self.world.node_available(end):
            pts = self.astar(maze,start,end)
            for pt in pts:
                pt.x = pt.x * self.world.grid_size + self.world.grid_size/2
                pt.y = pt.y * self.world.grid_size + self.world.grid_size/2
            self.path.set_pts(pts)




