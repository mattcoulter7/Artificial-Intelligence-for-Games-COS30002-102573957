from vector2d import Point2D, Vector2D
from graphics import egi
from random import randrange

class Enemy(object):
    """description of class"""
    def __init__(self,world = None):
        self.world = world
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.health = 100
        self.shape = {
            Point2D(-1.0,0.0),
            Point2D(0.0,0.0),
            Point2D(1.0,0.0),
        }

    def render(self):
        for pt in self.shape:
            egi.white_pen()
            egi.circle(pt,20)

    def update(self):
        # Removes health if agent is in proximity
        for agent in self.world.agents:
            to_agent = agent.pos - self.pos
            dist = to_agent.length()
            if dist < 50:
                self.health -= 1

