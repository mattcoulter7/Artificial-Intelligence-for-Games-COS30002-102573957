from vector2d import Vector2D
from matrix33 import Matrix33
from graphics import egi
from assassin import Assassin
from point2d import Point2D
from math import floor
from graph import Graph

class World(object):

    def __init__(self, cx, cy):
        # sizing
        self.cx = cx
        self.cy = cy
        # Game objects
        self.assassins = []
        self.blocks = []
        self.target = None
        # Game info
        self.paused = True
        self.show_info = True
        self.graph = Graph(self)
        

    def update(self, delta):
        for assassin in self.assassins:
            assassin.update(delta)

    def render(self):
        self.graph.render()

        for block in self.blocks:
            block.render()

        if self.target:
            egi.red_pen()
            egi.cross(self.target,self.graph.grid_size/4)

        for assassin in self.assassins:
            assassin.render()

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
