from random import randrange
from vector2d import Vector2D
from point2d import Point2D
from graphics import egi, KEY

class HideObject(object):
    def __init__(self,world = None):
        self.world = world
        self.pos = Point2D(randrange(world.cx), randrange(world.cy))
        self.color = 'GREEN'

    def render(self):
        egi.set_pen_color(name=self.color)
        egi.circle(self.pos,20,True)