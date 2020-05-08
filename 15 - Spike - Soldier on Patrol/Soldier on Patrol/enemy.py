from vector2d import Point2D, Vector2D
from graphics import egi
from random import randrange

class Enemy(object):
    """description of class"""
    def __init__(self,world = None):
        self.world = world
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.health = 100

    def render(self):
        egi.red_pen()
        egi.circle(self.pos,20)
        egi.white_pen()
        egi.circle(self.pos,15)
        egi.red_pen()
        egi.circle(self.pos,10)

    def update(self):
        # Removes health if agent is in proximity
        for agent in self.world.agents:
            to_agent = agent.pos - self.pos
            dist = to_agent.length()
            if dist < 50:
                self.health -= 1

        if self.health == 0:
            self.world.enemies.remove(self)

