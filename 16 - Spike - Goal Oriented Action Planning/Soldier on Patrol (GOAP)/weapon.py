from projectile import Projectile
from vector2d import Vector2D
from point2d import Point2D
from graphics import egi, KEY
from queue import Queue
from math import sin,cos,radians
from random import random,randrange

class Weapon(object):
    """description of class"""
    def __init__(self, world = None, agent = None,scale = 30.0):
        self.max_ammo = 10
        self.projectiles = []
        self.projectiles_queue = Queue(maxsize = self.max_ammo)
        self.agent = agent
        self.world = world
        self.color = 'WHITE'
        self.pos = Vector2D(randrange(0,world.cx),randrange(0,world.cy))
        dir = radians(random()*360)
        self.heading =  self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.shape = [
            Point2D(0.0,  0.0),
            Point2D( 1.0,  0.0),
            Point2D( 1.0, -0.25),
            Point2D( 0.25, -0.25),
            Point2D( 0.25, -0.5),
            Point2D( 0.0, -0.5),
            Point2D( 0.0, 0.0)
        ]
        self.proj_speed = 2000.0
        self.accuracy = 2.0
        self.fire_rate = 20
        self.fire_rate_tmr = self.fire_rate
        self.cooling_down = False # time for reloading and rate of fire
        self.remaining_ammo = self.max_ammo
        self.reloading = False
        self.reloading_time = 300
        self.reloading_tmr = self.reloading_time
        self.initialise_queue(self.projectiles_queue)

    def update(self,delta):
        if self.agent:
            self.pos = self.agent.pos
            self.heading = self.agent.heading
            self.side = self.agent.side

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

    def render(self):
        '''Renders gun to screen'''
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.shape, self.pos, self.heading, self.side, self.scale)
        egi.closed_shape(pts)

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

    def initialise_queue(self,queue):
        '''Fills up a queue to its max size'''
        for i in range(queue.maxsize):
            queue.put(Projectile(self.world,self))