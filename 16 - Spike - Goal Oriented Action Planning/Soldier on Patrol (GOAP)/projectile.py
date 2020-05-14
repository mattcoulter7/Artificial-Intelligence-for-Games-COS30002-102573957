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
        self.damage = 30

    def update(self,delta):
        if self.intersect_edge():
            self.recycle()
        
        enemy_hit = self.intersect_enemy()
        if enemy_hit:
            enemy_hit.take_damage(self.damage)
            self.recycle()
        # check for limits of new velocity
        self.vel.normalise()
        self.vel *= self.max_speed
        # update position
        self.pos += self.vel * delta
        # Recycle self back into queue if outside of map
        

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

    def intersect_enemy(self):
        '''check if projectile hits another agent'''
        for enemy in self.world.enemies:
            to_enemy = enemy.pos - self.pos
            dist = to_enemy.length()
            if dist < enemy.scale:
                return enemy
        return False

    def recycle(self):
        '''remove projectile from list and put it at the end of the queue for reuse'''
        if self in self.weapon.projectiles:
            self.weapon.projectiles.remove(self)
            self.weapon.projectiles_queue.put(self)

    def calculate(self):
        '''prepare to be put back onto the screen'''
        self.max_speed = self.weapon.proj_speed
        self.pos = self.weapon.agent.pos.copy()
        self.vel = self.weapon.agent.vel.copy()
        