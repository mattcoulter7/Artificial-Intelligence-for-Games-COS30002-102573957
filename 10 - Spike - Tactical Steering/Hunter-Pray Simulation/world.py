'''A 2d world that supports agents with steering behaviour

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

'''

from vector2d import Vector2D
from matrix33 import Matrix33
from graphics import egi


class World(object):

    def __init__(self, cx, cy,bot):
        self.cx = cx
        self.cy = cy
        self.agents = []
        self.hiding_objects = []
        self.paused = True
        self.show_info = False

        self.name = bot.replace('.py', '')  # accept both "Dumbo" or "Dumbo.py"
        # Create a controller object based on the name
        # - Look for a ./bots/BotName.py module (file) we need
        mod = __import__('bots.' + bot)  # ... the top level bots mod (dir)
        mod = getattr(mod, bot)       # ... then the bot mod (file)
        cls = getattr(mod, bot)      # ... the class (eg DumBo.py contains DumBo class)
        self.controller = cls()

    def update(self, delta):
        # Game stops when paused or no prey left
        if not self.paused and self.preys():
            # Updates the AI calculations
            self.controller.update(self)
            # Updates all agents
            for agent in self.agents:
                agent.update(delta)
            # Updates all all hiding positions, (checking for agents hiding at it)
            for obj in self.hiding_objects:
                obj.update()

    def render(self):
        for agent in self.agents:
            agent.render()

        for obj in self.hiding_objects:
            obj.render()

    def wrap_around(self, pos):
        ''' Treat world as a toroidal space. Updates parameter object pos '''
        max_x, max_y = self.cx, self.cy
        if pos.x > max_x:
            pos.x = pos.x - max_x
        elif pos.x < 0:
            pos.x = max_x - pos.x
        if pos.y > max_y:
            pos.y = pos.y - max_y
        elif pos.y < 0:
            pos.y = max_y - pos.y

    def transform_points(self, points, pos, forward, side, scale):
        ''' Transform the given list of points, using the provided position,
            direction and scale, to object world space. '''
        # make a copy of original points (so we don't trash them)
        wld_pts = [pt.copy() for pt in points]
        # create a transformation matrix to perform the operations
        mat = Matrix33()
        # scale,
        mat.scale_update(scale.x, scale.y)
        # rotate
        mat.rotate_by_vectors_update(forward, side)
        # and translate
        mat.translate_update(pos.x, pos.y)
        # now transform all the points (vertices)
        mat.transform_vector2d_list(wld_pts)
        # done
        return wld_pts

    def transform_point(self, point, pos, forward, side):
        ''' Transform the given single point, using the provided position,
        and direction (forward and side unit vectors), to object world space. '''
        # make a copy of the original point (so we don't trash it)
        wld_pt = point.copy()
        # create a transformation matrix to perform the operations
        mat = Matrix33()
        # rotate
        mat.rotate_by_vectors_update(forward, side)
        # and translate
        mat.translate_update(pos.x, pos.y)
        # now transform the point (in place)
        mat.transform_vector2d(wld_pt)
        # done
        return wld_pt

    def hunters(self):
        ''' Returns all of the hunters in agents '''
        hunters = []
        for agent in self.agents:
            if (agent.mode == 'hunter'):
                hunters.append(agent)
        return hunters

    def preys(self):
        ''' Returns all of the prey in agents '''
        preys = []
        for agent in self.agents:
            if (agent.mode == 'prey'):
                preys.append(agent)
        return preys