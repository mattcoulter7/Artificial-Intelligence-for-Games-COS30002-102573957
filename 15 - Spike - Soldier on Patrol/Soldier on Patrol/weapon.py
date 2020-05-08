from projectile import Projectile
from point2d import Point2D
from graphics import egi, KEY
from queue import Queue
from random import randrange

class Weapon(object):
    """description of class"""
    def __init__(self,agent = None,world = None):
        self.projectiles = []
        self.projectiles_queue = Queue(maxsize = 8)
        self.agent = agent
        self.world = world
        self.color = 'WHITE'
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
        self.accuracy = 5.0
        self.fire_rate = 10
        self.wait_time = self.fire_rate
        self.cooling_down = False
        self.reloading = False
        self.initialise_queue(self.projectiles_queue)

    def update(self,delta):
        # Update position of all projectiles
        for proj in self.projectiles:
            proj.update(delta)
        if not self.projectiles:
            self.reload()
        if self.cooling_down:
            self.wait_time -= 1
        if self.wait_time == 0:
            self.cooling_down = False
            self.wait_time = self.fire_rate

    def render(self):
        '''Renders gun to screen'''
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.shape, self.agent.pos, self.agent.heading, self.agent.side, self.agent.scale)
        egi.closed_shape(pts)

        for proj in self.projectiles:
            proj.render()

    def shoot(self):
        '''Moves obj from queue into list'''
        # Shoot if queue still has obj to move
        if not self.projectiles_queue.empty() and not self.cooling_down:
            # Get obj at front of queue
            proj = self.projectiles_queue.get()
            # Prepare for shooting
            proj.calculate()
            # Put obj in list so it is updated
            self.projectiles.append(proj)
            self.cooling_down = True

    def initialise_queue(self,queue):
        '''Fills up a queue to its max size'''
        for i in range(queue.maxsize):
            queue.put(Projectile(self.world,self))

    def reload(self):
        return

