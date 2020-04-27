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
        self.color = 'GREEN'
        self.pos = self.randomise_location()

    def render(self):

        egi.set_pen_color(name=self.color)
        egi.circle(self.pos,self.size)

    def get_hiding_point(self,hunter_pos):
        # Uses angle to calculate best spot behind the hiding object
        position = Vector2D(hunter_pos.x - self.pos.x,hunter_pos.y - self.pos.y)
        position.normalise()
        return self.pos + -self.size * self.scale * position

    def randomise_location(self):
        margin = 80
        pos_x = randrange(margin, self.world.cx - margin)
        pos_y = randrange(margin, self.world.cy - margin)
        if (self.check_location_valid(Vector2D(pos_x, pos_y))):
            return Vector2D(pos_x, pos_y)
        return self.randomise_location()

    def check_location_valid(self,pos):
        # Checks if a hiding spot already exists near a new hiding spot
        valid = True
        for obj in self.world.hiding_objects:
            to_existing = obj.pos - pos
            dist = to_existing.length()
            if (dist < 2 * self.size):
                return False
        return True

        
