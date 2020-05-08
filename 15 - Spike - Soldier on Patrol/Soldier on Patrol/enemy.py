from vector2d import Point2D, Vector2D
from graphics import egi
from random import randrange

class Enemy(object):
    """description of class"""
    def __init__(self,world = None,scale = 30.0):
        self.world = world
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.scale = scale
        self.alive = True
        self.max_health = 100
        self.health = self.max_health

    def render(self):
        # Get color
        egi.set_pen_color(color = (1.0, self.health/self.max_health, 0.0, 1))

        # Draw Body
        egi.circle(self.pos,self.scale)

        # Draw Arms
        leftarm = Vector2D(self.pos.x - self.scale,self.pos.y)
        rightarm = Vector2D(self.pos.x + self.scale,self.pos.y)
        egi.circle(leftarm,self.scale / 3)
        egi.circle(rightarm,self.scale / 3)

        # Draw cross to indicate death
        if not self.alive:
            egi.cross(self.pos,self.scale/2)

    def update(self):
        # Removes health if agent is in proximity
        if self.alive:
            for agent in self.world.agents:
                to_agent = agent.pos - self.pos
                dist = to_agent.length()
                if dist < self.scale * 2 :
                    self.health -= 1

        if self.health == 0:
            self.alive = False
