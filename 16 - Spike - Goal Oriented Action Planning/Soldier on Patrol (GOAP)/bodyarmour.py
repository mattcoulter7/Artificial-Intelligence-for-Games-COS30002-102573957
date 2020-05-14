from vector2d import Vector2D
from point2d import Point2D
from graphics import egi, KEY
from math import sin,cos,radians
from random import random,randrange

class BodyArmour(object):
    """Spawns randomly on the map and adds health to agent if picked up"""
    def __init__(self,world = None,agent = None,scale = 30.0):
        self.protection = 100
        self.world = world
        self.agent = agent
        self.color = 'WHITE'
        self.pos = Vector2D(randrange(0,world.cx),randrange(0,world.cy))
        dir = radians(random()*360)
        self.heading =  self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size

        self.shape = [
            Point2D(-1.2,  0.8),
            Point2D( 0.5,  0.25),
            Point2D( 0.5,  -0.25),
            Point2D(-1.2, -0.8)
        ]

    def update(self,delta):
        if self.agent:
            self.pos = self.agent.pos
            self.heading = self.agent.heading
            self.side = self.agent.side

    def render(self):
        '''Renders gun to screen'''
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.shape, self.pos, self.heading, self.side, self.scale)
        egi.closed_shape(pts)


