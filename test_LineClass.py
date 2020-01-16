import unittest
from math import sqrt, pi
from GeometricClass import Line, Point

class test_Line(unittest.TestCase):
    def setUp(self):
        self.l1 = Line(Point(), Point(10, 0))
        self.l2 = Line(Point(), Point(10, 10))
        self.l3 = Line(Point(), Point(0, 10))
        self.l4 = Line(Point(), Point(-10, 10))
        self.l5 = Line(Point(), Point(-10, 0))
        self.l6 = Line(Point(), Point(-10, -10))
        self.l7 = Line(Point(), Point(0, -10))
        self.l8 = Line(Point(), Point(10, -10))

    def test_length(self):
        self.assertAlmostEqual(self.l1.length, 10)
        self.assertAlmostEqual(self.l2.length, 10*sqrt(2))
        self.assertAlmostEqual(self.l3.length, 10)
        self.assertAlmostEqual(self.l4.length, 10*sqrt(2))
        self.assertAlmostEqual(self.l5.length, 10)
        self.assertAlmostEqual(self.l6.length, 10*sqrt(2))
        self.assertAlmostEqual(self.l7.length, 10)
        self.assertAlmostEqual(self.l8.length, 10*sqrt(2))

    def test_angle(self):
        self.assertAlmostEqual(self.l1.angle,       0 % pi)
        self.assertAlmostEqual(self.l2.angle,    pi/4 % pi)
        self.assertAlmostEqual(self.l3.angle,    pi/2 % pi)
        self.assertAlmostEqual(self.l4.angle,  3*pi/4 % pi)
        self.assertAlmostEqual(self.l5.angle,      pi % pi)
        self.assertAlmostEqual(self.l6.angle, -3*pi/4 % pi)
        self.assertAlmostEqual(self.l7.angle,   -pi/2 % pi)
        self.assertAlmostEqual(self.l8.angle,   -pi/4 % pi)


if __name__ == '__main__':
    unittest.main()
