'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform
from path import Path

class Agent(object):

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='patrol'):
        # keep a reference to the world object
        self.world = world
        self.mode = mode

        # where am i and where am i going? random start pos
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.force = Vector2D()  # current steering force
        self.accel = Vector2D() # current acceleration due to force
        self.mass = mass

        # data for drawing this agent
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]

        # Path to follow
        self.path = Path(looped = True)
        self.randomise_path()
        self.waypoint_threshold = 100.0

        # Force and speed limiting code
        self.max_speed = 20.0 * scale
        self.max_force = 500.0
        # debug draw info?
        self.show_info = True

    def calculate(self,delta):
        # calculate the current steering force
        mode = self.mode
        if mode == 'patrol':
            force = self.follow_path()
        elif mode == 'attack':
            force = self.attack()
        else:
            force = Vector2D()
        self.force = force
        return force

    def update(self, delta):
        ''' update state '''
        if self.world.enemies:
            self.mode = 'attack'
        else:
            self.mode = 'patrol'
        
        ''' update vehicle position and orientation '''
        # calculate and set self.force to be applied
        ## force = self.calculate()
        force = self.calculate(delta)
        ## limit force? <-- for wander
        force.truncate(self.max_force)
        # determine the new acceleration
        self.accel = force / self.mass  # not needed if mass = 1.0
        # new velocity
        self.vel += self.accel * delta
        # check for limits of new velocity
        self.vel.truncate(self.max_speed)
        # update position
        self.pos += self.vel * delta
        # update heading is non-zero velocity (moving)
        if self.vel.length_sq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
        # treat world as continuous space - wrap new position if needed
        self.world.wrap_around(self.pos)

    def render(self, color=None):
        ''' Draw the triangle agent with color'''
        # draw the ship
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)

        # draw the path if it exists and the mode is follow
        if self.show_info:
            if self.mode in ['patrol','attack']:
                self.path.render()

    def speed(self):
        return self.vel.length()

    #--------------------------------------------------------------------------

    def arrive(self, target_pos):
        ''' this behaviour is similar to seek() but it attempts to arrive at
            the target position with a zero velocity'''
        decel_rate = 1
        to_target = target_pos - self.pos
        dist = to_target.length()
        # calculate the speed required to reach the target given the
        # desired deceleration rate
        speed = dist / decel_rate
        # make sure the velocity does not exceed the max
        speed = min(speed, self.max_speed)
        # from here proceed just like Seek except we don't need to
        # normalize the to_target vector because we have already gone to the
        to_target.normalise()
        # trouble of calculating its length for dist.
        desired_vel = to_target * speed
        return (desired_vel - self.vel)

    def follow_path(self):
        if (self.path.is_finished()):
            # Arrives at the final waypoint
            return self.arrive(self.path._pts[-1])
        else:
            # Goes to the current waypoint and increments on arrival
            to_target = self.path.current_pt() - self.pos
            dist = to_target.length()
            if (dist < self.waypoint_threshold):
                self.path.inc_current_pt()
            return self.arrive(self.path.current_pt())

    def randomise_path(self):
        cx = self.world.cx
        cy = self.world.cy
        margin = min(cx,cy) * 1/6
        self.path.create_random_path(10, margin, margin, cx - margin, cy - margin,looped = True)

    def attack(self):
        closest = min(self.world.enemies, key = lambda e: (e.pos - self.pos).length())
        return self.arrive(closest.pos)
