from math import sqrt, atan2, sin, cos, pi
from collections.abc import Sequence

class Point(Sequence):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __getitem__(self, u):
        return [self.x, self.y][u]

    def __len__(self):
        return 2

    def __repr__(self):
        return '{self.__class__.__name__}: '.format(self=self) + '{' + \
                'x: {self.x}, y: {self.y}'.format(self=self) + '}'

    @property
    def r(self):
        return sqrt(self.x**2 + self.y**2)

    @property
    def angle(self):
        return atan2(self.y, self.x)

    def round(self):
        return Point(int(self.x), int(self.y))

class Line:
    def __init__(self, p = Point(0,0), q = Point(0,0)):
        assert(isinstance(p, Point))
        assert(isinstance(q, Point))
        self.p = p
        self.q = q

    def __repr__(self):
        return '{self.__class__.__name__}: '.format(self=self) + '{' + \
                '{self.a}*x + {self.b}*y + {self.c}'.format(self=self) + '}'

    @property
    def length(self):
        return sqrt((self.q.x-self.p.x)**2 + (self.q.y-self.p.y)**2)

    @property
    def angle(self):
        return atan2(self.q.y - self.p.y, self.q.x - self.p.x) % pi

    @property
    def a(self):
        return sin(self.angle)

    @property
    def b(self):
        return -cos(self.angle)

    @property
    def c(self):
        return -(self.b*self.p.y + self.a*self.p.x)

    def intersection(self, other):
        den_x = other.a * self.b - other.b * self.a
        den_y = self.a * other.b - other.a * self.b

        assert(den_x and den_y)
        return Point(
            x=(other.b * self.c - self.b * other.c) / den_x,
            y=(other.a * self.c - self.a * other.c) / den_y
        )

    def offsetLine(self, p):
        assert(isinstance(p,Point))
        self.p = self.p + p
        self.q = self.q + p
