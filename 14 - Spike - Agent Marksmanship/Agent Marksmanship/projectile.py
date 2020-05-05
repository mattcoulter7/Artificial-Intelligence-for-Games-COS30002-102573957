from graphics import egi
from vector2d import Vector2D

class Projectile(object):
    """description of class"""
    def __init__(self,pos,heading):
        self.pos = pos
        self.heading = heading
        self.vel = Vector2D()
        self.max_speed = 400.0

    def update(self,delta):
        # new velocity
        self.vel += self.heading
        # check for limits of new velocity
        self.vel.truncate(self.max_speed)
        # update position
        self.pos += self.vel * delta

    def render(self):
        egi.circle(self.pos,5)