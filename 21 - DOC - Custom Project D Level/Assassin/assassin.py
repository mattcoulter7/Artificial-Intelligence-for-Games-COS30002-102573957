import pyglet
from vector2d import Vector2D,TupleToPoint2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians, pi
from random import random, randrange, uniform
from path import Path
from node import Node
from search_functions import astar,smooth

class Assassin(object):

    def __init__(self, world=None, scale=30.0, mode=None):
        # keep a reference to the world object
        self.world = world
        self.mode = mode

        # where am i and where am i going? random start pos
        dir = radians(random()*360)
        self.pos = world.graph.node_to_pos(Vector2D(5,5))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of Assassin size

        # speed limiting code
        self.max_speed = 10.0 * scale

        # Path
        self.path = Path()

        # debug draw info?
        self.show_info = True

        # Sprites
        self.char = pyglet.image.load('resources/assassin.png')
        self.still = pyglet.sprite.Sprite(self.char, x=self.pos.x, y=self.pos.y)
        self.ani = pyglet.resource.animation('resources/assassin_walk.gif')
        self.walking = pyglet.sprite.Sprite(img=self.ani)

        # Chasing
        self.guard = None

    def calculate(self):
        # calculate the current steering force
        vel = Vector2D(0,0)
        if self.path._pts:
            if self.mode == 'chase':
                self.chase(self.guard)
                self.update_path()
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
                self.path.clear()

        if self.mode == 'chase':
            self.kill_guard()

    def update_mode(self):
        ''' Updates state according to different variables '''
        if self.guard:
            self.mode = 'chase'
        else:
            self.mode = None

    def render(self):
        ''' Draw the Assassin'''
        if self.path._pts:
            # Walking animation
            self.walking.update(x=self.pos.x+self.char.width/2,y=self.pos.y+self.char.height/2,rotation=self.heading.angle('deg') + 90,scale=self.world.graph.grid_size/self.char.height)
            self.walking.draw()
            # Path
            self.path.render()
        else:
            # Still
            self.still.update(x=self.pos.x+self.char.width/2,y=self.pos.y+self.char.height/2,rotation=self.heading.angle('deg') + 90,scale=self.world.graph.grid_size/self.char.height)
            self.still.draw()

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

    def chase(self,guard):
        self.world.target = guard.path.current_pt()

    def intersect_pos(self,pos):
        ''' Returns true if assassin intersects a particular position'''
        return self.world.graph.pos_to_node(self.pos) == self.world.graph.pos_to_node(pos)

    def update_path(self):
        ''' Reassigns the points of path to head towards new destination'''
        maze = self.world.graph.grid
        start = self.world.graph.pos_to_node(self.pos)
        end = self.world.graph.pos_to_node(self.world.target)

        # Can't travel into blocks
        if self.world.graph.node_available(end):
            # Calculate points
            pts = astar(maze,1.0,start,end)
            pts = smooth(pts)
            # Convert points into coordinates
            for i in range(0,len(pts)):
                pts[i] = self.world.graph.node_to_pos(pts[i].copy())
            self.path.set_pts(pts)

    def kill_guard(self):
        if self.intersect_pos(self.guard.pos):
            self.world.guards.remove(self.guard)
            self.guard = None




