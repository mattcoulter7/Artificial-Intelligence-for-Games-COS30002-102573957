from projectile import Projectile
from point2d import Point2D
from graphics import egi, KEY
from queue import Queue
from random import randrange
from playsound import playsound

PROJECTILE_SPEED = {
    KEY.F: 2500.0, # fast
    KEY.S: 500.0 # slow
}

PROJECTILE_ACCURACY = {
    KEY.A: 0.5, # small margin of error for perfect shot
    KEY.I: 180.0 # big margin of error for perfect shot
}

class Weapon(object):
    """description of class"""
    def __init__(self,agent = None,world = None):
        self.projectiles = []
        self.projectiles_queue = Queue(maxsize = 5)
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
        self.proj_speed = 1000.0
        self.accuracy = 0.5
        self.initialise_queue(self.projectiles_queue)

    def update(self,delta):
        # Update position of all projectiles
        for proj in self.projectiles:
            proj.update(delta)

    def render(self):
        '''Renders gun to screen'''
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.shape, self.agent.pos, self.agent.heading, self.agent.side, self.agent.scale)
        egi.closed_shape(pts)

    def shoot(self):
        '''Moves obj from queue into list'''
        # Shoot if queue still has obj to move
        if not self.projectiles_queue.empty():
            # Get obj at front of queue
            proj = self.projectiles_queue.get()
            # Prepare for shooting
            proj.calculate()
            # Put obj in list so it is updated
            self.projectiles.append(proj)
        sound = randrange(0,7)
        playsound('b%s.wav' % sound,block = False)

    def initialise_queue(self,queue):
        '''Fills up a queue to its max size'''
        for i in range(queue.maxsize):
            queue.put(Projectile(self.world,self))


