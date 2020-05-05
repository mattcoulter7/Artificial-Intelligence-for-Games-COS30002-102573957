from projectile import Projectile
from point2d import Point2D
from graphics import egi

class Weapon(object):
    """description of class"""

    def __init__(self,agent = None,world = None):
        self.projectiles = []
        self.agent = agent
        self.world = world

        self.color = 'WHITE'
        self.shape = [
            Point2D(0.0,  0.0),
            Point2D( 0.5,  0.0),
            Point2D( 0.5, -0.25),
            Point2D( 0.25, -0.25),
            Point2D( 0.25, -0.5),
            Point2D( 0.0, -0.5),
            Point2D( 0.0, 0.0)
        ]

    def update(self,delta):
        for proj in self.projectiles:
            proj.update(delta)

    def render(self):
        x = self.agent.pos.x
        y = self.agent.pos.y

        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.shape, self.agent.pos, self.agent.heading, self.agent.side, self.agent.scale)
        egi.closed_shape(pts)

    def shoot(self):
        self.projectiles.append(Projectile(self.agent.pos.copy(),self.agent.heading.copy()))


