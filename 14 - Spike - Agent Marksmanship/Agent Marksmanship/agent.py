from vector2d import Vector2D,Point2D,Vector2DToPoint
from graphics import egi, KEY
from math import sin, cos, radians, pi
from random import random, randrange, uniform
from weapon import Weapon

class Agent(object):
    def __init__(self, world=None, mode = None, scale=30.0, mass=1.0):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        self.weapon = Weapon(self,world)

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

        # NEW WANDER INFO
        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 1.0 * scale
        self.wander_radius = 1.0 * scale
        self.wander_jitter = 10.0 * scale
        self.bRadius = scale

        # Force and speed limiting code
        self.max_speed = 20.0 * scale
        self.max_force = 500.0


        # debug draw info?
        self.show_info = False

    def calculate(self,delta):
        # reset the steering force
        mode = self.mode
        force = None
        if mode == 'attacking':
            target = None
            if self.world.agents_of_type('target'):
                force = self.chase(self.closest(self.world.agents_of_type('target')))
            else:
                force = self.wander(delta)
        elif mode == 'target':
            force = self.wander(delta)
        else:
            force = Vector2D()
        return force

    def should_shoot(self):
        '''uses distance, proj velocity and target agent velocity to predict which direction to shoot'''
        if self.world.agents_of_type('target'):
            for agent in self.world.agents_of_type('target'):
                # Predicts where the 
                predicted_pos = agent.vel.copy()
                predicted_pos.normalise()
                predicted_pos *= self.get_look_ahead(agent)
                to_predicted = agent.pos + predicted_pos - self.pos
                angle = self.vel.angle_with(to_predicted) * 180 / pi
                if angle < self.weapon.accuracy and angle > -self.weapon.accuracy:
                    return True
        return False

    def update(self, delta):
        ''' update vehicle position and orientation '''
        # Attacking agents shoot according to weapon accuracy
        if self.mode == 'attacking' and self.should_shoot():
            self.weapon.shoot()

        # calculate and set self.force to be applied
        ## force = self.calculate()
        self.force = self.calculate(delta)
        ## limit force
        self.force.truncate(self.max_force)
        # determine the new acceleration
        self.accel = self.force / self.mass
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
        middle = Vector2D(self.world.cx/2,self.world.cy/2)
        # draw the ship
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)

        # draw the path if it exists and the mode is follow
        if self.mode == 'follow_path':
            self.path.render()

        # add some handy debug drawing info lines - force and velocity
        if self.show_info:
            if self.mode == 'attacking':
                # Blue line for bullet path
                egi.blue_pen()
                shoot_path = self.vel.copy()
                shoot_path.normalise()
                shoot_path *= self.weapon.proj_speed
                egi.line_with_arrow(self.pos,self.pos + shoot_path,5)
                # egi.line_with_arrow(middle, middle + shoot_path,5)
                
                # Red line for predicted location of closest target
                if self.world.agents_of_type('target'):
                    # Necessary render from attacking agent because of look_ahead
                    closest_target = self.closest(self.world.agents_of_type('target'))
                    egi.red_pen()
                    predicted_pos = closest_target.vel.copy()
                    predicted_pos.normalise()
                    predicted_pos *= self.get_look_ahead(closest_target)
                    egi.line_with_arrow(closest_target.pos,closest_target.pos + predicted_pos,5)
                    
                    # Green line for line from attaking to predicted target location 
                    egi.green_pen()
                    to_predicted = closest_target.pos + predicted_pos - self.pos
                    egi.line_with_arrow(self.pos,closest_target.pos + predicted_pos,5)
                    # egi.line_with_arrow(middle, middle + to_predicted,5)

                    angle = self.vel.angle_with(to_predicted) * 180 / pi
                    print(angle)
                    

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

    def get_look_ahead(self,agent):
        to_target = agent.pos - self.pos
        dist = to_target.length()
        look_ahead = dist * agent.speed() / self.weapon.proj_speed
        return look_ahead

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def chase(self,target):
        '''seeks the prdicted position of an agent'''
        predicted_pos = target.vel.copy()
        predicted_pos.normalise()
        predicted_pos *= self.get_look_ahead(target)
        target_pos = predicted_pos + target.pos
        return self.seek(target_pos)

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