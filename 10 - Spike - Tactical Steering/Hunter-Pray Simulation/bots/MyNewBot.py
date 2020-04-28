from vector2d import Vector2D
from point2d import Point2D
from random import random, randrange, uniform
from agent import Agent

class MyNewBot(object):
    def __init__(self,world = None,agent = None):
        self.world = world
        self.agent = agent

    def calculate_hide(self):
        # Create ratio between distance and size
        closest_hunter_pos = self.agent.closest(self.world.hunters()).pos
        hiding_object = min(self.world.hiding_objects,key = lambda h: ((h.pos - self.agent.pos).length())/h.size)
        self.agent.hiding_object = hiding_object