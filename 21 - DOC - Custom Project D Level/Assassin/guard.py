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
        self.pos = world.graph.node_to_pos(world.graph.rand_node())
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of Assassin size

        # speed limiting code
        self.max_speed = 5.0 * scale

        # nodes
        self.path = Path()
        self.wander()

        # debug draw info?
        self.show_info = True

        # Sprites
        self.char = pyglet.image.load('resources/guard.png')
        self.still = pyglet.sprite.Sprite(self.char, x=self.pos.x, y=self.pos.y)
        self.ani = pyglet.resource.animation('resources/guard_walk.gif')
        self.walking = pyglet.sprite.Sprite(img=self.ani)

        # AI variables
        self.hearing_range = 5.0
        self.vision_range = 10.0

    def update(self, delta):
        ''' update vehicle position and orientation '''
        # update mode if necessary
        self.update_mode()

        # new velocity
        self.vel = self.follow_path()
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
        if self.hear_assassin():
            self.mode = 'suspicious'
            self.approach(self.world.assassin.pos.copy())
        elif self.see_assassin():
            self.mode = 'kill'
            self.approach(self.world.assassin.pos)
        else:
            self.mode = 'wander'

    def render(self, color=None):
        ''' Draw the Guard'''
        if self.mode is not None:
            self.walking.update(x=self.pos.x+self.char.width/2,y=self.pos.y+self.char.height/2,rotation=self.heading.angle('deg') + 90,scale=self.world.graph.grid_size/self.char.height)
            self.walking.draw()
        else:
            self.still.update(x=self.pos.x+self.char.width/2,y=self.pos.y+self.char.height/2,rotation=self.heading.angle('deg') + 90,scale=self.world.graph.grid_size/self.char.height)
            self.still.draw()
        # Path
        if self.path._pts:
            self.path.render()

    #--------------------------------------------------------------------------

    def point_in_range(self,pt,ran):
        ''' Returns true if pt is within a circular radius of self '''
        ran *= self.world.graph.grid_size
        return pt.x in range(self.world.graph.pos_to_node(self.pos.x-ran),self.pos.x+ran) and pt.y in range(self.pos.y-ran,self.pos.y+ran)

    def point_in_front_range(self,pt,ran):
        ''' Returns true if pt is in front of self '''
        ran *= self.world.graph.grid_size
        return pt.x in range(self.pos.x,self.pos.x + (self.heading.x * ran)) and pt.y in range(self.pos.y,self.pos.y + (self.heading.y * ran))

    def hear_assassin(self):
        ''' Returns true if assassin walking is in hearing range '''
        return self.point_in_range(self.world.assassin.pos,self.hearing_range)

    def see_assassin(self):
        ''' returns true if assassin is in guard visibility range '''
        return self.point_in_front_range(self.world.assassin.pos,self.hearing_range)

    def intersect_pos(self,pos):
        ''' Returns true if assassin intersects a particular position'''
        return self.world.graph.pos_to_node(pos) == self.world.graph.pos_to_node(self.pos)

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return desired_vel

    def follow_path(self):
        ''' Goes to the current waypoint and increments on arrival '''
        if self.path.is_finished():
            self.wander()
        elif self.intersect_pos(self.path.current_pt()):
            self.path.inc_current_pt()
        return self.seek(self.path.current_pt())

    def approach(self,pt):
        ''' Resets the path to the new specified pts '''
        pts = astar(self.world.graph.grid,1.0,self.world.graph.pos_to_node(self.pos),pt)
        pts = smooth(pts)
        for i in range(0,len(pts)):
            pts[i] = self.world.graph.node_to_pos(pts[i].copy(),'center')
        self.path.set_pts(pts)

    def wander(self):
        ''' Chooses a random available location on the map and path finds towards it '''
        rand_node = self.world.graph.rand_node_from_pos(self.world.graph.pos_to_node(self.pos),10)
        self.approach(rand_node)