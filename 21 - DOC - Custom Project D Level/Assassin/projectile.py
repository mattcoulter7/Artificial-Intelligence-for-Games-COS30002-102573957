from graphics import egi
from vector2d import Vector2D
import pyglet

class Projectile(object):
    """description of class"""
    def __init__(self,world,weapon):
        self.world = world
        self.weapon = weapon
        self.pos = Vector2D()
        self.vel = Vector2D()
        self.max_speed = None
        self.angle = None
        # Sprites
        bullet = pyglet.image.load('resources/bullet.png')
        self.bullet_spr = pyglet.sprite.Sprite(bullet, x=self.pos.x, y=self.pos.y)

    def update(self,delta):
        # check for limits of new velocity
        self.vel.normalise()
        self.vel *= self.max_speed
        # update position
        self.pos += self.vel * delta
        # Recycle self back into queue if outside of map
        if self.intersect_edge():
            self.recycle()
        
        assassin_hit = self.intersect_assassin()
        if assassin_hit:
            self.recycle()

        if self.intersect_block():
            self.recycle()

    def render(self):
        self.bullet_spr.update(x=self.pos.x,y=self.pos.y,rotation = self.angle)
        self.bullet_spr.draw()

    #--------------------------------------------------------------------------

    def intersect_edge(self):
        '''check if projectile goes out of the map'''
        if self.pos.x < 0:
            return True
        elif self.pos.x > self.world.cx:
            return True
        elif self.pos.y < 0:
            return True
        elif self.pos.y > self.world.cy:
            return True
        return False

    def intersect_assassin(self):
        '''check if projectile hits another assassin'''
        to_assassin = self.world.assassin.pos - self.pos
        dist = to_assassin.length()
        if dist < 50:
            return self.world.assassin
        return False

    def intersect_block(self):
        '''check if projectile hits another assassin'''
        intersect = False
        for block in self.world.blocks:
            block_node = self.world.graph.pos_to_node(block.pos.copy())
            self_node = self.world.graph.pos_to_node(self.pos.copy())
            intersect = self_node == block_node
        return intersect

    def recycle(self):
        '''remove projectile from list and put it at the end of the queue for reuse'''
        self.weapon.projectiles.remove(self)
        self.weapon.projectiles_queue.put(self)

    def calculate(self):
        '''prepare to be put back onto the screen'''
        self.max_speed = self.weapon.proj_speed
        self.pos = self.weapon.guard.pos + (self.weapon.guard.heading * 70) - (self.weapon.guard.side * 10) # Adjustment for bullet to come out of weapon
        self.vel = self.weapon.guard.heading.copy()
        self.angle = self.vel.angle('deg') + 90
        