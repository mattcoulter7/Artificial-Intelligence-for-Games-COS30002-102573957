from vector2d import Vector2D
from point2d import Point2D
from random import random, randrange, uniform
from agent import Agent

class MyNewBot(object):
    def update(self,world):
        for prey in world.preys():
            # Create ratio between distance and size
            closest_hunter_pos = prey.closest(world.hunters()).pos
            hiding_object = min(world.hiding_objects,key = lambda h: (h.pos - prey.pos).length()/h.size)
            prey.hiding_object = hiding_object