import pyglet
from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians, pi
from random import random, randrange, uniform
from path import Path
from search_functions import astar,smooth

class Guard(object):

    def __init__(self, world=None, scale=30.0, mode='wander'):
        # keep a reference to the world object
        self.world = world
        self.mode = mode

        # where am i and where am i going? random start pos
        dir = radians(random()*360)
        self.pos = world.graph.get_pos(world.graph.rand_node(),'corner')
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of Assassin size

        # speed limiting code
        self.max_speed = 5.0 * scale

        # nodes
        self.path = Path()
        self.generate_random_path()

        # debug draw info?
        self.show_info = True

        # Sprites
        self.char = pyglet.image.load('resources/guard.png')
        self.still = pyglet.sprite.Sprite(self.char, x=self.pos.x, y=self.pos.y)
        self.ani = pyglet.resource.animation('resources/guard_walk.gif')
        self.walking = pyglet.sprite.Sprite(img=self.ani)

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
        if self.path._pts:
            self.mode = 'wander'
        else:
            self.mode = None

    def render(self, color=None):
        ''' Draw the Guard'''
        if self.mode == 'wander':
            self.walking.update(x=self.pos.x+self.char.width/2,y=self.pos.y+self.char.height/2,rotation=self.heading.angle('deg') + 90,scale=self.world.graph.grid_size/self.char.height)
            self.walking.draw()
        elif self.mode == None:
            self.still.update(x=self.pos.x+self.char.width/2,y=self.pos.y+self.char.height/2,rotation=self.heading.angle('deg') + 90,scale=self.world.graph.grid_size/self.char.height)
            self.still.draw()
        # Path
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
        if self.path.is_finished():
            self.generate_random_path()
        elif self.intersect_pos(self.path.current_pt()):
            self.path.inc_current_pt()
        return self.seek(self.path.current_pt())

    def generate_random_path(self):
        rand_node = self.world.graph.rand_node_from_pos(self.world.graph.get_node(self.pos),5)
        pts = astar(self.world.graph.grid,self.world.graph.get_node(self.pos),rand_node)
        pts = smooth(pts)
        for i in range(0,len(pts)):
            pts[i] = self.world.graph.get_pos(pts[i].copy(),'center')
        self.path.set_pts(pts)