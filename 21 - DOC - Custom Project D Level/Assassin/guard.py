import pyglet
from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians, pi
from random import random, randrange, uniform
from path import Path
from search_functions import astar,smooth
from weapon import Weapon

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

        # Weapon
        self.weapon = Weapon(self,self.world)

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
        self.vision_range = 5
        self.vision = []

        # AI Wandering
        self.wander_dist = 10
        self.wander()

    def calculate(self):
        # calculate the current steering force
        vel = Vector2D(0,0)
        if self.path._pts:
            if self.mode == 'suspicious':
                self.investigate()
            elif self.mode == 'attack':
                self.investigate()
            vel = self.follow_path()
        return vel

    def update(self, delta):
        ''' update vehicle position and orientation '''
        
        # Refresh what can be seen by guard
        self.update_vision()
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

        self.weapon.update(delta)

    def update_mode(self):
        ''' Updates state according to different variables '''
        if self.see_assassin():
            self.mode = 'attack'
        elif self.hear_assassin():
            self.mode = 'suspicious'
        else:
            self.mode = 'wander'

    def update_vision(self):
        # Adjacent edges of node
        adjacent = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        # Nodes that the guard will be able to see
        visible_nodes = []
        # Distance to middle point of vision square that will be made
        ahead_range = int((self.vision_range - 1) / 2)
        # Node of self
        self_node = self.world.graph.pos_to_node(self.pos.copy())
        # Middle point of vision square that will be made
        ahead_node = self.world.graph.pos_to_node(self.pos + self.heading * self.world.graph.grid_size * ahead_range)
        # Add that centre point to begin with
        visible_nodes.append(ahead_node)
        # Expand from centre outwards adding nodes to cover full square
        check_from = 0 # Used to avoid retesting adjacent nodes that we have already checked for
        for i in range(ahead_range):
            for j in range(check_from,len(visible_nodes)):
                for pt2 in adjacent:
                    pt1 = visible_nodes[j]
                    new_node = Vector2D(pt1.x + pt2[0],pt1.y + pt2[1])
                    if self.world.graph.node_available(new_node) and new_node not in visible_nodes:
                        visible_nodes.append(new_node)
                        check_from += 1
        for i in range(len(visible_nodes)):
            visible_nodes[i] = self.world.graph.global_to_relative(visible_nodes[i])
        self.vision = visible_nodes

    def render(self, color=None):
        ''' Draw the Guard'''
        # Update variables
        angle = self.heading.angle('deg') + 90
        x_val = self.pos.x - (self.char.width/2 * cos(angle * pi/180))
        y_val = self.pos.y + (self.char.height/2 * sin(angle * pi/180))
        if self.mode is not None: # Moving
            self.walking.update(x=x_val,y=y_val,rotation=angle)
            self.walking.draw()
            self.path.render()
        else: # Still
            self.still.update(x=x_val,y=y_val,rotation=angle)
            self.still.draw()
        # Visibility
        for pt in self.vision:
            egi.red_pen()
            egi.circle(self.world.graph.node_to_pos(pt.copy(),'center'),self.world.graph.grid_size/2)
        # Weapon and Bullets
        self.weapon.render()

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
        assassin_node = self.world.graph.pos_to_node(self.world.assassin.pos.copy())
        return assassin_node in self.vision

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
        if self.path.is_finished():
            if self.mode == 'suspicious':
                self.investigate()
            else:
                self.wander()
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

    def wander(self):
        ''' Chooses a random available location on the map and path finds towards it '''
        rand_node = self.world.graph.rand_node_from_pos(self.world.graph.pos_to_node(self.pos.copy()),self.wander_dist)
        self.approach(rand_node)

    def investigate(self):
        node = self.world.graph.pos_to_node(self.world.assassin.pos.copy())
        self.approach(node)