from vector2d import Vector2D
from matrix33 import Matrix33
from graphics import egi
from assassin import Assassin
from point2d import Point2D
from math import floor

class World(object):

    def __init__(self, cx, cy):
        # sizing
        self.cx = cx
        self.cy = cy
        # Game objects
        self.assassin = Assassin(self)
        self.enemies = []
        self.blocks = []
        self.target = None
        # Game info
        self.paused = True
        self.show_info = True
        # Grid
        rows = 10
        columns = 10
        self.grid = [[0 for x in range(columns)] for y in range(rows)]
        self.grid_size = 50

    def update(self, delta):
        self.assassin.update(delta)

    def render(self):
        self.assassin.render()

        if self.target:
            egi.red_pen()
            egi.cross(self.target,self.grid_size/4)

        grid = self.grid_size
        egi.aqua_pen()
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                x = i*grid
                y = j*grid
                pt1 = Point2D(i*grid,j*grid)
                pt2 = Point2D(pt1.x + grid,pt1.y)
                pt3 = Point2D(pt1.x,pt1.y + grid)
                egi.line_by_pos(pt1,pt2)
                egi.line_by_pos(pt1,pt3)
    
    def get_grid(self,x,y):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if floor(x/self.grid_size) == i and floor(y/self.grid_size) == j:
                    return Vector2D(i*self.grid_size + self.grid_size/2,j*self.grid_size + self.grid_size/2)

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
