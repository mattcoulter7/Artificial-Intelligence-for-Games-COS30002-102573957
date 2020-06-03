from graphics import egi
from vector2d import Vector2D

class Health(object):
    """player health and renders health bar"""
    def __init__(self,parent):
        # References
        self.parent = parent
        # Statistics
        self.max_health = 100
        self.health = self.max_health
        # Sizing
        self.height = 20
        self.width = 150
        self.distance_from_parent = 100

    def render(self):
        pos = self.parent.pos + Vector2D(-self.width/2,self.distance_from_parent)
        border = 3
        midpoint = self.percent() * (self.width - 2 * border)
        # Outer black rectangle
        egi.white_pen()
        egi.rect(pos.x,pos.y,pos.x + self.width,pos.y - self.height,filled = True)
        
        # Inner Red rectangle
        egi.red_pen()
        egi.rect(pos.x + border,pos.y - border,pos.x + self.width - border,pos.y - self.height + border,filled = True)

        # Inner Green rectangle
        egi.green_pen()
        egi.rect(pos.x + border,pos.y - border,pos.x + midpoint + border,pos.y - self.height + border,filled = True)

    def take_damage(self,amount):
        if amount > self.remaining():
            self.health = amount
        self.health -= amount

    def remaining(self):
        return self.health

    def reset(self):
        self.health = self.max_health

    def still_alive(self):
        return self.health > 0

    def percent(self):
        return self.health/self.max_health



