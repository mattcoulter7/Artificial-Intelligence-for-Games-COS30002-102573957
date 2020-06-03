import pyglet
from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians, pi
from random import random, randrange, uniform
from path import Path
from search_functions import astar,smooth
from weapon import Weapon
from history import History
from vision import Vision

class Guard(object):

    def __init__(self, world=None, scale=30.0, mode='scout'):
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

        # Weapon
        self.weapon = Weapon(self.world,self)

        # speed limiting code
        self.max_speed = 5.0 * scale

        # nodes
        self.path = Path()

        # debug draw info?
        self.show_info = True

        # Sprites
        self.char = pyglet.image.load('resources/guard.png')
        self.still = pyglet.sprite.Sprite(self.char, x=self.pos.x, y=self.pos.y)
        self.ani = pyglet.resource.animation('resources/guard_walk.gif')
        self.walking = pyglet.sprite.Sprite(img=self.ani)

        # AI Hearing
        self.hearing_range = 5.0

        # AI Vision
        self.vision = Vision(self,3,self.world)
        self.assassin_seen = 0

        # Memory
        self.history = History(self,self.world)

        # Generate first path
        self.scout()

    def calculate(self):
        # Update the path based off mode
        vel = Vector2D(0,0)
        if self.mode == 'attack':
            self.attack()
        elif self.mode == 'investigate':
            vel = self.follow_path()
        elif self.mode == 'scout':
            vel = self.follow_path()
        return vel

    def update(self, delta):
        ''' update vehicle position and orientation '''
        # Refresh what can be seen by guard
        self.vision.update()
        # update mode if necessary
        self.update_mode()
        # new velocity
        self.vel = self.calculate()
        # update position
        self.pos += self.vel * delta

        # update heading is non-zero velocity (moving)
        if self.vel.length_sq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()

        self.weapon.update(delta)

        # Memory of seeing assassin
        if self.see_assassin():
            self.assassin_seen = 500
        if self.assassin_seen > 0:
            self.assassin_seen -= 1


    def update_mode(self):
        ''' Updates state according to different variables '''
        if self.see_assassin():
            self.mode = 'attack'
            return True
        elif self.assassin_seen > 0 or self.hear_assassin():
            self.mode = 'investigate'
            return True
        else:
            self.mode = 'scout'
            return True
        return False

    def render(self, color=None):
        ''' Draw the Guard'''
        # Weapon and Bullets
        self.weapon.render()
        # Update variables
        angle = self.heading.angle('deg') + 90
        x_val = self.pos.x - (self.char.width/2 * cos(angle * pi/180))
        y_val = self.pos.y + (self.char.height/2 * sin(angle * pi/180))
        if self.mode in ['scout','investigate']: # Moving
            self.walking.update(x=x_val,y=y_val,rotation=angle)
            self.walking.draw()
        else: # Still
            self.still.update(x=x_val,y=y_val,rotation=angle)
            self.still.draw()

    #--------------------------------------------------------------------------
    
    def line_distance_to(self,pt):
        ''' returns the straight line length divided by gridsize from self to pt '''
        to_pt = pt - self.pos
        return to_pt.length() / self.world.graph.grid_size

    def hear_assassin(self):
        ''' Returns true if assassin walking is in hearing range '''
        if self.world.assassin.volume > 0:
            return self.line_distance_to(self.world.assassin.pos.copy()) <= (self.hearing_range + self.world.assassin.volume)

    def see_assassin(self):
        ''' Returns true if the assassin is within the vision blocks '''
        assassin_node = self.world.graph.pos_to_node(self.world.assassin.pos.copy(),relative = True)
        return assassin_node in self.vision.vision

    def intersect_pos(self,pos):
        ''' Returns true if assassin intersects a particular position'''
        return self.world.graph.pos_to_node(pos.copy()) == self.world.graph.pos_to_node(self.pos.copy())

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return desired_vel

    def follow_path(self):
        ''' Goes to the current waypoint and increments on arrival '''
        if self.path.is_finished() or len(self.path._pts) == 0:
            if self.mode == 'investigate':
                self.investigate()
            elif self.mode == 'scout':
                self.scout()
        elif self.intersect_pos(self.path.current_pt()):
            self.path.inc_current_pt()
        return self.seek(self.path.current_pt())

    def approach(self,pt):
        ''' Resets the path to the new specified pts '''
        pts = astar(self.world.graph.grid,1.0,self.world.graph.pos_to_node(self.pos.copy()),pt)
        if pts: #ASTAR success
            pts = smooth(pts)
            for i in range(len(pts)):
                pts[i] = self.world.graph.global_to_relative(pts[i])
                pts[i] = self.world.graph.node_to_pos(pts[i].copy(),'center')
            self.path.set_pts(pts)

    def scout(self):
        ''' Chooses a random available location on the map that hasn't been seen yet and path finds towards it '''
        self.history.update()
        rand_node = self.world.graph.rand_node_from_list(self.history.yet_to_visit)
        self.approach(rand_node)

    def investigate(self):
        ''' Updates the path to target towards last heard sound of assassin '''
        node = self.world.graph.pos_to_node(self.world.assassin.pos.copy())
        rand_node = self.world.graph.rand_node_from_pos(node,5)
        self.approach(rand_node)

    def attack(self):
        ''' Prompts guard to shoot assassin '''
        if self.path._pts:
            self.path.clear()
        self.heading = (self.world.assassin.pos - self.pos).normalise()
        self.weapon.shoot()

