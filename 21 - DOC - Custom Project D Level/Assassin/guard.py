from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians, pi
from random import random, randrange, uniform
from path import Path
from search_functions import astar,smooth

class Guard(object):

    def __init__(self, world=None, scale=30.0, mode='Wander'):
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
        self.color = 'RED'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]

        # speed limiting code
        self.max_speed = 5.0 * scale

        # nodes
        self.path = Path()
        self.generate_random_path()

        # debug draw info?
        self.show_info = True

    def calculate(self):
        # calculate the current steering force
        mode = self.mode
        vel = Vector2D(0,0)
        if self.mode == 'wander':
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

    def update_mode(self):
        ''' Updates state according to different variables '''
        self.mode = 'wander'

    def render(self, color=None):
        ''' Draw the triangle Assassin with color'''
        # draw the ship
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)

        if self.path._pts:
            self.path.render()

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return desired_vel

    def intersect_pos(self,pos):
        ''' Returns true if assassin intersects a particular position'''
        return self.world.graph.get_node(pos) == self.world.graph.get_node(self.pos)

    def follow_path(self):
        # Goes to the current waypoint and increments on arrival
        if self.intersect_pos(self.path.current_pt()):
            self.path.inc_current_pt()
        elif self.path.is_finished():
            self.generate_random_path()
        return self.seek(self.path.current_pt())

    def generate_random_path(self):
        rand_node = self.world.graph.rand_node()
        pts = astar(self.world.graph.grid,self.world.graph.get_node(self.pos),rand_node)
        pts = smooth(pts)
        for pt in pts:
            pt.x = pt.x * self.world.graph.grid_size + self.world.graph.grid_size/2
            pt.y = pt.y * self.world.graph.grid_size + self.world.graph.grid_size/2
        self.path.set_pts(pts)

    def valid(self,pt):
        return (self.world.graph.node_exists(pt) and self.world.graph.node_available(pt))