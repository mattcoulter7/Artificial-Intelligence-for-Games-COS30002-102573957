class Weapon(object):
    """description of class"""

    def __init__(self,agent = None,world = None):
        projectiles = []
        self.agent = agent
        self.world = world

    def update(self):
        for proj in self.projectiles:
            proj.update()


