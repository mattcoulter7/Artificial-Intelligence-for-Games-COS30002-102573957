from graphics import egi
from vector2d import Vector2D
from playsound import playsound

class Projectile(object):
    """description of class"""
    def __init__(self,world,weapon):
        self.world = world
        self.weapon = weapon
        self.pos = Vector2D()
        self.vel = Vector2D()
        self.max_speed = None

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
            self.world.assassins.remove(assassin_hit)
            self.recycle()

        if self.intersect_block():
            self.recycle()

    def render(self):
        egi.circle(self.pos,5)

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
        to_assassin = assassin.pos - self.pos
        dist = to_assassin.length()
        if dist < 50:
            return assassin
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
        self.pos = self.weapon.assassin.pos.copy()
        self.vel = self.weapon.assassin.vel.copy()
        