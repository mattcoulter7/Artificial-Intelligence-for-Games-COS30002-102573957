'''2D Vector with related methods

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

Updated by Steve Dower
'''

from math import sqrt
from point2d import Point2D  # Not used here, but easy way to expose it

MIN_FLOAT = 1e-300


def is_equal(a, b):
    return abs(a-b) < 1e-12

# Not needed, but fyi ...
#def PointToVector2D(pt):
#    return Vector2D(pt.x, pt.y)
#
#def Vector2DToPoint(v):
#    return Point2D(v.x, v.y)


class Vector2D(object):
    __slots__ = ('x', 'y')

    def __init__(self, x=0., y=0.):
        self.x = x
        self.y = y

    def zero(self):
        ''' set x and y to zero '''
        self.x = 0.
        self.y = 0.

    def is_zero(self):
        ''' return true if both x and y are zero '''
        return (self.x**2 + self.y**2) < MIN_FLOAT

    def length(self):
        ''' return the length of the vector '''
        x = self.x
        y = self.y
        return sqrt(x*x + y*y)

    def length_sq(self):
        ''' return the squared length (avoid sqrt()) '''
        x = self.x
        y = self.y
        return x*x + y*y

    def normalise(self):
        ''' normalise self to a unit vector of length = 1.0 '''
        x = self.x
        y = self.y
        l = sqrt(x*x + y*y)
        try:
            self.x = x/l
            self.y = y/l
        except ZeroDivisionError:
            self.x = 0.
            self.y = 0.
        return self

    def get_normalised(self):
        ''' return a normalised copy of self '''
        result = self.copy()
        result.normalise()
        return result

    def dot(self, v2):
        ''' The dot (inner) product of self and v2 vector '''
        return self.x*v2.x + self.y*v2.y

    def sign(self, v2):
        ''' return +1 if v2 is clockwise of self.
            return -1 if v2 is anti-clockwise of self
            Assumes Y axis points down and X points right '''
        if self.y*v2.x > self.x*v2.y:
            return -1
        else:
            return 1

    def perp(self):
        ''' return a vector perpendicular to self. '''
        return Vector2D(-self.y, self.x)

    def truncate(self, maxlength):
        ''' limit the length (scale x and y) to maxlength '''
        if self.length() > maxlength:
            self.normalise()  # unit vector length = 1.0
            self *= maxlength  # so length is 1.0 * maxlength

    def distance(self, v2):
        ''' the distance between self and v2 vector '''
        dx = v2.x - self.x
        dy = v2.y - self.y
        return sqrt(dx*dx + dy*dy)

    def distance_sq(self, v2):
        ''' the squared distance between self and v2 vector '''
        dx = v2.x - self.x
        dy = v2.y - self.y
        return dx*dx + dy*dy

    def reflect(self, norm):
        ''' Reflect self around the norm vector provided. '''
        # eg the path of a ball reflected off a wall
        self += 2.0 * self.dot(norm) * norm.get_reverse()

    def get_reverse(self):
        ''' return a new vector that is the reverse of self. '''
        return Vector2D(-self.x, -self.y)

 # -
        ''' get_reverse(), but using - operator based instead. '''
        return Vector2D(-self.x, -self.y)

    def copy(self):
        ''' Simple copy Vector2D with self values '''
        return Vector2D(self.x, self.y)

 # +=
        self.x += rhs.x
        self.y += rhs.y
        return self

 # -=
        self.x -= rhs.x
        self.y -= rhs.y
        return self

 # *=
        self.x *= rhs
        self.y *= rhs
        return self

 # /=
        self.x /= rhs
        self.y /= rhs
        return self

 # ==
        return is_equal(self.x, rhs.x) and is_equal(self.y, rhs.y)

 # !=
        return (self.x != rhs.x) or (self.y != rhs.y)

 # self + rhs
        return Vector2D(self.x+rhs.x, self.y+rhs.y)

 # self - rhs
        return Vector2D(self.x-rhs.x, self.y-rhs.y)

 # self * rhs (scalar)
        return Vector2D(self.x*rhs, self.y*rhs)
 # lhs (scalar) * self
        return Vector2D(self.x*lhs, self.y*lhs)

 # self / rhs (scalar)
        return Vector2D(self.x/rhs, self.y/rhs)
 # lhs (scalar) / self
        return Vector2D(lhs/self.x, lhs/self.y)

    def __str__(self):
        return '[%7.2f, %7.2f]' % (self.x, self.y)
