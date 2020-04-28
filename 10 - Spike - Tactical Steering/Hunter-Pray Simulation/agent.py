'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

'''

from vector2d import Vector2D
from point2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform

class Agent(object):

    DECELERATION_SPEEDS = {
        'slower' : 0.5,
        'slow': 0.9,
        'normal': 1.4,
        'fast': 1.9
    }
    def __init__(self, mode, world=None,name = None, scale=30.0, mass=1.0):
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
        if (self.mode == 'hunter'): self.color = 'RED'
        elif (self.mode == 'prey'): self.color = 'BLUE'
        
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]

        # Visibility for other agents
        self.visibility = 200

        # NEW WANDER INFO
        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 1.0 * scale
        self.wander_radius = 1.0 * scale
        self.wander_jitter = 10.0 * scale
        self.bRadius = scale

        # Force and speed limiting code
        self.max_speed = 20.0 * scale
        self.max_force = 1000.0  
        
        # HIDING VARIABLES
        self.hiding_object = None

        # debug draw info?
        self.show_info = False

    def calculate(self,delta):
        # calculate the current steering force
        mode = self.mode
        if mode == 'hunter':
            closest_pray = self.closest(self.world.preys())
            dist = (closest_pray.pos - self.pos).length()
            if dist <= self.visibility:
                force = self.seek(closest_pray.pos)
            else:
                force = self.wander(delta)
        elif mode == 'prey':
            closest_hunter = self.closest(self.world.hunters())
            force = self.flee(closest_hunter.pos)
        else:
            force = Vector2D()
        self.force = force
        return force

    def update(self, delta):
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
        if (self.mode == 'prey' and self.intersect_hunter()):
            self.world.agents.remove(self)

    def render(self, color=None):
        ''' Draw the triangle agent with color'''
        # draw the ship
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)
        # add some handy debug drawing info lines - force and velocity
        if self.world.show_info:
            # Visibility Radius
            if (self.mode == 'hunter'):
                egi.red_pen()
                egi.circle(self.pos,self.visibility)
                
                # Draws all hiding spots from all hunters
                for obj in self.world.hiding_objects:
                    hiding_pos = obj.get_hiding_pos(self.pos)
                    egi.line_by_pos(self.pos,hiding_pos)
                    egi.cross(hiding_pos,10)
            if (self.mode == 'prey'):
                egi.blue_pen()
                # Draws all hiding spots from all preys
                closest_hunter = self.closest(self.world.hunters()).pos
                hiding_pos = self.hiding_object.get_hiding_pos(closest_hunter)
                egi.line_by_pos(self.pos,hiding_pos)
            
    def speed(self):
        return self.vel.length()

    def closest(self,objects):
        # Returns the closest object to self from a given list of objects
        dist_to_closest = None
        closest = None
        # Gets the closest object to hide behind
        for obj in objects:
            to_obj = obj.pos - self.pos
            dist = to_obj.length()
            if (closest is None or dist < dist_to_closest):
                closest = obj
                dist_to_closest = dist
        return closest

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def wander(self, delta):
        ''' random wandering using a projected jitter circle '''
        wt = self.wander_target
        # this behaviour is dependent on the update rate, so this line must
        # be included when using time independent framerate.
        jitter_tts = self.wander_jitter * delta # this time slice
        # first, add a small random vector to the target's position
        wt += Vector2D(uniform(-1,1) * jitter_tts, uniform(-1,1) * jitter_tts)
        # re-project this new vector back on to a unit circle
        wt.normalise()
        # increase the length of the vector to the same as the radius
        # of the wander circle
        wt *= self.wander_radius
        # move the target into a position WanderDist in front of the agent
        target = wt + Vector2D(self.wander_dist, 0)
        # project the target into world space
        wld_target = self.world.transform_point(target, self.pos, self.heading, self.side)
        # and steer towards it
        return self.seek(wld_target)

    def flee(self, hunter_pos):
        ''' move away from hunter position '''
        ## add panic distance (second)
        panic_distance = self.visibility
        ## add flee calculations (first)
        dist_to_hunter = hunter_pos.distance(self.pos)
        # fly as fast as possible to escape hunter
        if dist_to_hunter <= panic_distance:
            # Goes quickly to get out of panic distance
            desired_vel = (hunter_pos + self.pos).normalise() * self.max_speed
            return (desired_vel + self.vel)
        # Approaches hiding spot for the closest hiding spot calculated in HideObject class
        return self.arrive(self.hiding_object.get_hiding_pos(hunter_pos),'slow')

    def arrive(self, target_pos, speed):
        ''' this behaviour is similar to seek() but it attempts to arrive at
            the target position with a zero velocity'''
        decel_rate = self.DECELERATION_SPEEDS[speed]
        to_target = target_pos - self.pos
        dist = to_target.length()
        if dist > 0:
            # calculate the speed required to reach the target given the
            # desired deceleration rate
            speed = dist / decel_rate
            # make sure the velocity does not exceed the max
            speed = min(speed, self.max_speed)
            # from here proceed just like Seek except we don't need to
            # normalize the to_target vector because we have already gone to the
            # trouble of calculating its length for dist.
            desired_vel = to_target * (speed / dist)
            return (desired_vel - self.vel)
        return Vector2D(0, 0) - self.vel

    def intersect_hunter(self):
        # Detects collision between hunter and self
        for hunter in self.world.hunters():
            to_hunter = self.pos - hunter.pos
            dist = to_hunter.length()
            if (dist < 30):
                return True
        return False

    


    

    