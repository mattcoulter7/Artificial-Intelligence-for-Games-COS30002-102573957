from graphics import egi
from vector2d import Vector2D

class Projectile(object):
    """description of class"""
    def __init__(self,world,weapon):
        self.world = world
        self.weapon = weapon
        self.pos = Vector2D()
        self.vel = Vector2D()
        self.max_speed = 1000.0

    def update(self,delta):
        # check for limits of new velocity
        self.vel.normalise()
        self.vel *= self.max_speed
        # update position
        self.pos += self.vel * delta
        # Recycle self back into queue if outside of map
        if self.intersect_edge():
            self.recycle()
        
        agent_hit = self.intersect_agent()
        if agent_hit:
            self.world.agents.remove(agent_hit)
            self.recycle()

    def render(self):
        egi.circle(self.pos,5)

    #--------------------------------------------------------------------------

    def intersect_edge(self):
        if self.pos.x < 0:
            return True
        elif self.pos.x > self.world.cx:
            return True
        elif self.pos.y < 0:
            return True
        elif self.pos.y > self.world.cy:
            return True
        return False

    def intersect_agent(self):
        for agent in self.world.agents:
            if agent is not self.weapon.agent:
                to_agent = agent.pos - self.pos
                dist = to_agent.length()
                if dist < 20:
                    return agent
        return False

    def recycle(self):
        self.weapon.projectiles.remove(self)
        self.weapon.projectiles_queue.put(self)

    def prepare(self):
        self.pos = self.weapon.agent.pos.copy()
        self.vel = self.weapon.agent.vel.copy()