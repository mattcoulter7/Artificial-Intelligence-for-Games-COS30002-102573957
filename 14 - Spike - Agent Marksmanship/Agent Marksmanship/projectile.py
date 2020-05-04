class Projectile(object):
    """description of class"""
    def __init__(self,pos,world = None):
        self.world = world
        self.pos = pos

    def update(self):
        return