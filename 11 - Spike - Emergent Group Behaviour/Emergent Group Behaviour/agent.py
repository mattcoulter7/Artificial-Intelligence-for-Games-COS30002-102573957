'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform

class Agent(object):
    def __init__(self, world=None, scale=30.0, mass=1.0, mode='seek'):
        # keep a reference to the world object
        self.world = world
        self.mode = mode

        # Physics for self
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.force = Vector2D()
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.force = Vector2D()  # current steering force
        self.accel = Vector2D() # current acceleration due to force
        self.mass = mass

        # Appearance variables
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]

        # Force and speed limiting variables
        self.max_speed = 10.0 * scale
        self.max_force = 600.0

        # Cohesion, separation and alignment steering behaviours
        self.cohesion = 400.0
        self.separation = 100.0
        self.alignment = 200.0
        self.neighbours = []
        self.closeby = []

        # Wander Variables
        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 3.0 * scale
        self.wander_radius = 1.0 * scale
        self.wander_jitter = 0.5 * scale
        self.bRadius = scale

        # debug draw info?
        self.show_info = False

    def calculate(self,delta):
        '''calculate the current steering force'''
        # Wander by default
        force = self.wander(delta)
        # Update steering force to neighbours average force if they exist
        if (self.neighbours):
            self.force += self.emerge()
        if (self.closeby):
            self.force += self.seperate()
        if (self.neighbours and not self.closeby):
            self.force += self.approach_centre()
        return force

    def update(self, delta):
        ''' update vehicle position and orientation '''
        # calculate and set self.force to be applied
        ## force = self.calculate()
        self.force += self.calculate(delta)
        ## limit force? <-- for wander
        self.force.truncate(self.max_force)
        # determine the new acceleration
        self.accel = self.force / self.mass  # not needed if mass = 1.0
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

        # update emerge seperate lists
        self.neighbours = self.get_agents_in_radius(self.cohesion)
        self.closeby = self.get_agents_in_radius(self.separation)

    def render(self, color=None):
        ''' Draw the triangle agent with color'''
        # draw the ship
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)
        # add some handy debug drawing info lines - force and velocity
        if self.show_info:
            s = 0.5 # <-- scaling factor
            ### PHYSICS
            # force
            egi.red_pen()
            egi.line_with_arrow(self.pos, self.pos + self.force * s, 5)
            # net (desired) change
            egi.grey_pen()
            egi.line_with_arrow(self.pos, self.pos+ (self.force+self.vel) * s, 5)

            ### EMERGE
            # cohesion circle
            egi.pink_pen()
            egi.circle(self.pos,self.cohesion)
            # separation circle
            egi.grey_pen()
            egi.circle(self.pos,self.separation)
            if (self.neighbours):
                # Average Heading Line
                egi.green_pen()
                ave_heading = self.neighbour_average('heading')
                egi.line_with_arrow(self.pos, self.pos + self.alignment * ave_heading * s,5)
                # Average Position Line
                egi.blue_pen()
                ave_position = self.neighbour_average('pos')
                egi.line_with_arrow(self.pos, ave_position,5)
            if (self.closeby):
                egi.aqua_pen()
                closest_agent_pos = self.closest(self.closeby).pos
                target = 2 * self.pos - closest_agent_pos
                egi.line_with_arrow(self.pos, target,5)
            # Become pink if in neighbourhood of agents[0]
            for agent in self.world.agents:
                if agent in self.neighbours:
                    agent.color = 'PINK'
                else:
                    agent.color = 'ORANGE'

            ### WANDER
            # calculate the center of the wander circle in front of the agent
            wnd_pos = Vector2D(self.wander_dist, 0)
            wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
            # draw the wander circle
            egi.green_pen()
            egi.circle(wld_pos, self.wander_radius)
            # draw the wander target (little circle on the big circle)
            egi.red_pen()
            wnd_pos = (self.wander_target + Vector2D(self.wander_dist, 0))
            wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
            egi.circle(wld_pos, 3)

    def speed(self):
        return self.vel.length()

    def get_agents_in_radius(self,radius):
        # Returns a list of all the agents within a given radius of self
        neighbours = []
        for agent in self.world.agents:
            if (agent != self):
                agent_to_self = self.pos - agent.pos
                dist = agent_to_self.length()
                if (dist < radius):
                    neighbours.append(agent)
        return neighbours
    
    def neighbour_average(self,attr):
        # Gets the average of a given attribute from all of the neighbour
        average = Vector2D(0,0)
        for agent in self.neighbours:
            average += getattr(agent,attr)
        average /= len(self.neighbours)
        return average

    def closest(self,list):
        # Returns the closest object to self from a given list of objects
        dist_to_closest = None
        closest = None
        # Gets the closest object to hide behind
        for obj in list:
            to_obj = obj.pos - self.pos
            dist = to_obj.length()
            if (closest is None or dist < dist_to_closest):
                closest = obj
                dist_to_closest = dist
        return closest

    #--------------------------------------------------------------------------

    def emerge(self):
        # Approaches the average heading
        ave_heading = self.neighbour_average('heading')
        ave_heading.normalise()
        target = self.pos + self.alignment * ave_heading
        to_target = target - self.pos
        return to_target

    def approach_centre(self):
        # Approaches the centre
        ave_position = self.neighbour_average('pos')
        to_ave = ave_position - self.pos
        return to_ave

    def seperate(self):
        # Moves away from nearby agent
        closest_agent_pos = self.closest(self.closeby).pos
        target = (2 * self.pos - closest_agent_pos)
        to_target = target - self.pos
        return to_target

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

