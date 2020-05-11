from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians, pi
from random import random, randrange, uniform
from path import Path
from weapon import Weapon

class Agent(object):

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='patrol'):
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
        self.color = 'WHITE'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]

        # Path to follow
        self.path = world.path
        self.waypoint_threshold = 100.0

        # Force and speed limiting code
        self.max_speed = 20.0 * scale
        self.max_force = 500.0

        # Shooting variables
        self.shooting_distance = 250.0

        # Cohesion, separation and alignment steering behaviours
        self.separation = 200.0

        # debug draw info?
        self.show_info = True

    def calculate(self,delta):
        # calculate the current steering force
        mode = self.mode
        force = Vector2D(0,0)
        if mode == 'patrol':
            force = self.follow_path()
        elif mode == 'attack':
            force = self.attack()
        elif mode == 'hide':
            force = self.hide()
        else:
            force = Vector2D()
        force += self.separate()
        self.force = force
        return force

    def update(self, delta):
        ''' Check if state needs to be updated '''
        self.check_state()
        self.weapon.update(delta)
        # Shoot
        if self.mode == 'attack' and self.should_shoot():
            self.weapon.shoot()

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
        

    def check_state(self):
        ''' check if state should be updated '''
        alive_enemies = list(filter(lambda e: e.alive == True, self.world.enemies))
        if alive_enemies:
            if self.weapon.reloading:
                self.mode = 'hide'
            else:
                self.mode = 'attack'
        else:
            self.mode = 'patrol'

    def render(self, color=None):
        ''' Draw the triangle agent with color'''
        # draw the ship
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)

        if self.mode == 'attack': self.weapon.render()

        # draw the path if it exists and the mode is follow
        if self.show_info:
            self.path.render()

    def speed(self):
        return self.vel.length()

    def should_shoot(self):
        '''uses distance, proj velocity and target agent velocity to predict which direction to shoot'''
        for enemy in list(filter(lambda e: e.alive == True, self.world.enemies)):
            to_enemy = enemy.pos - self.pos
            angle = self.vel.angle_with(to_enemy) * 180 / pi
            if -self.weapon.accuracy < angle < self.weapon.accuracy:
                return True
        return False

    #--------------------------------------------------------------------------
    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

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

    def attack(self):
        alive = list(filter(lambda e: e.alive, self.world.enemies))
        closest = min(alive, key = lambda e: (e.pos - self.pos).length() * e.health)
        to_closest = closest.pos - self.pos
        to_closest -= self.heading.copy() * self.shooting_distance

        dead = list(filter(lambda e: not e.alive, self.world.enemies))
        if dead:
            closest_dead = min(dead, key = lambda e: (e.pos - self.pos).length())
            to_closest_dead = closest_dead.pos - self.pos
            dist = to_closest_dead.length()
            angle = self.vel.angle_with(to_closest_dead)
            ratio = dist/angle
            if 0 < ratio < closest_dead.scale/2:
                to_closest += self.vel.perp().get_reverse().normalise()
            else:
                to_closest += self.vel.perp().normalise()

        return self.arrive(self.pos + to_closest)

    def hide(self):
        '''Goes to nearest dead body and hides behind it'''
        alive = list(filter(lambda e: e.alive, self.world.enemies))
        enemy = min(alive, key = lambda e: (e.pos - self.pos).length() * e.health)
        dead = list(filter(lambda e: e.alive == False, self.world.enemies))
        if dead:
            closest = min(dead, key = lambda e: (e.pos - self.pos).length())
            # Uses angle to calculate best spot behind the hiding object
            position = enemy.pos - closest.pos
            position.normalise()
            hiding_point = closest.pos - closest.scale * 2 * position
            return self.arrive(hiding_point)
        return Vector2D()

    def separate(self):
        # Moves away from nearby agent
        closeby = list(filter(lambda a: a is not self and (a.pos - self.pos).length() < self.separation,self.world.agents))
        if (closeby):
            closest_agent_pos = min(closeby,key = lambda a: (a.pos - self.pos).length()).pos
            target = (2 * self.pos - closest_agent_pos)
            to_target = target - self.pos
            length = to_target.copy().length()
            to_target.normalise()
            to_target *= self.separation - length
            return to_target
        return Vector2D()