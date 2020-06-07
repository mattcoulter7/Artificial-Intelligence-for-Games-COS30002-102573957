from projectile import Projectile
from vector2d import Vector2D
from point2d import Point2D
from graphics import egi, KEY
from queue import Queue
from math import sin,cos,radians
from random import random,randrange
import pyglet

class Weapon(object):
    """description of class"""
    def __init__(self, world = None, guard = None,scale = 30.0):
        # References
        self.guard = guard
        self.world = world

        # Statistics
        self.max_ammo = 16
        self.proj_speed = 2000.0
        self.accuracy = 2.0
        self.damage = 25

        # Queue and List
        self.projectiles = []
        self.projectiles_queue = Queue(maxsize = self.max_ammo)

        # Fire Rate
        self.fire_rate = 4
        self.fire_rate_tmr = self.fire_rate
        self.cooling_down = False # time for reloading and rate of fire

        # Magazine/reloading
        self.remaining_ammo = self.max_ammo
        self.reloading = False
        self.reloading_time = 50
        self.reloading_tmr = self.reloading_time
        self.initialise_queue(self.projectiles_queue)

        # Graphics
        gunflare = pyglet.image.load('resources/gunflare.png')
        self.gunflare_spr = pyglet.sprite.Sprite(img = gunflare)

    def update(self,delta):
        # Update position of all projectiles
        for proj in self.projectiles:
            proj.update(delta)

        # Reload when no ammo left
        if self.remaining_ammo == 0:
            self.reloading = True

        # Reload timer
        if self.reloading:
            self.reloading_tmr -= 1
        if self.reloading_tmr == 0:
            self.reloading = False
            self.reloading_tmr = self.reloading_time
            self.remaining_ammo = self.max_ammo

        # Cool down timer between shots
        if self.cooling_down:
            self.fire_rate_tmr -= 1
        if self.fire_rate_tmr == 0:
            self.cooling_down = False
            self.fire_rate_tmr = self.fire_rate

    def render(self,gunflare = False):
        # Gunflare
        if gunflare:
            angle = self.guard.heading.angle('deg') + 90
            gunflare_pos = self.guard.pos + (self.guard.heading * 100) + (self.guard.side * 10) # Adjustment for gunflare to be positioned at weapon
            self.gunflare_spr.update(x = gunflare_pos.x,y = gunflare_pos.y,rotation = angle)
            self.gunflare_spr.draw()
        else:
            # Bullets
            for proj in self.projectiles:
                proj.render()

    def shoot(self):
        '''Moves obj from queue into list'''
        # Shoot if queue still has obj to move
        if not self.projectiles_queue.empty() and not self.cooling_down and not self.reloading:
            # Get obj at front of queue
            proj = self.projectiles_queue.get()
            # Prepare for shooting
            proj.calculate()
            # Put obj in list so it is updated
            self.projectiles.append(proj)
            self.cooling_down = True
            self.remaining_ammo -= 1
            # Render the gunflare
            self.render(gunflare = True)


    def initialise_queue(self,queue):
        '''Fills up a queue to its max size'''
        for i in range(queue.maxsize):
            queue.put(Projectile(self.world,self))