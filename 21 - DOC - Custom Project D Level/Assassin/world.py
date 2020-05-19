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
        self.scale = 100
        # Game objects
        self.assassin = Assassin(self)
        self.guards = []
        self.blocks = []
        self.target = None
        # Game info
        self.paused = True
        self.show_info = True
        # Grid
        self.grid_size = cx/cy * self.scale
        self.grid_count = round(cx / self.grid_size)
        self.grid = [[0 for x in range(self.grid_count)] for y in range(self.grid_count)]
        

    def update(self, delta):
        self.assassin.update(delta)
        
        for guard in self.guards:
            guard.update(delta)

    def render(self):
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

        for block in self.blocks:
            block.render()

        if self.target:
            egi.red_pen()
            egi.cross(self.target,self.grid_size/4)

        self.assassin.render()

        for guard in self.guards:
            guard.render()
    
    def get_node(self,pt):
        ''' Returns the node of a given coordinate '''
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if floor(pt.x/self.grid_size) == i and floor(pt.y/self.grid_size) == j:
                    return Vector2D(i,j)

    def fit_pos(self,pt,type):
        ''' Takes a coord and fits it to a given place in a square '''
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if floor(pt.x/self.grid_size) == i and floor(pt.y/self.grid_size) == j:
                    if type == 'center':
                        return Vector2D(i*self.grid_size + self.grid_size/2,j*self.grid_size + self.grid_size/2)
                    elif type == 'corner':
                        return Vector2D(i*self.grid_size,j*self.grid_size)

    def get_pos(self,pt,type):
        ''' Returns the position of a node, fitted to the square '''
        return self.fit_pos(pt*self.grid_size,type)

    def node_available(self,node):
        ''' returns true if node is 0 '''
        return not self.grid[node.x][node.y]

    def update_grid(self,node):
        ''' O becomes 1, 1 becomes 0'''
        self.grid[node.x][node.y] = (self.grid[node.x][node.y] - 1) % 2

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
