from vector2d import Vector2D
from matrix33 import Matrix33
from graphics import egi
from path import Path


class World(object):

    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.agents = []
        self.enemies = []
        self.weapon = []
        self.bodyarmour = []
        self.paused = True
        self.show_info = True

        # Path for all agents
        self.path = Path(looped = True)
        self.randomise_path()


    def update(self, delta):
        if not self.paused:
            for agent in self.agents:
                agent.update(delta)

            for enemy in self.enemies:
                enemy.update(delta)

            for weapon in self.weapon:
                weapon.update(delta)

            for bodyarmour in self.bodyarmour:
                bodyarmour.update(delta)

    def render(self):
        for agent in self.agents:
            agent.render()

        for enemy in self.enemies:
            enemy.render()

        for weapon in self.weapon:
            weapon.render()

        for bodyarmour in self.bodyarmour:
            bodyarmour.render()

        if self.show_info:
            infotext = ', '.join(set(agent.mode for agent in self.agents))
            egi.white_pen()
            egi.text_at_pos(0, 0, infotext)

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

    def randomise_path(self):
        cx = self.cx
        cy = self.cy
        margin = min(cx,cy) * 1/6
        self.path.create_random_path(10, margin, margin, cx - margin, cy - margin,looped = True)