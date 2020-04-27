from random import randrange
from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, atan, radians

class HideObject(object):
    def __init__(self,world = None):
        self.world = world
        self.scale = 1.5
        self.size = 40
        
        margin = 80
        self.pos = Vector2D(randrange(margin, world.cx-margin), randrange(margin,world.cy - margin))
        self.color = 'GREEN'

    def render(self):

        egi.set_pen_color(name=self.color)
        egi.circle(self.pos,self.size)

    def get_hiding_point(self,hunter_pos):
        # Uses angle to calculate best spot behind the hiding object
        position = Vector2D(hunter_pos.x - self.pos.x,hunter_pos.y - self.pos.y)
        position.normalise()
        return self.pos + -self.size * self.scale * position

        
