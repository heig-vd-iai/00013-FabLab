import unittest
from geometry import Point

class test_Point(unittest.TestCase):
    def test_add(self):
        self.assertEqual(Point(10, 5) + Point(2, 3), Point(12, 8))
        self.assertEqual(Point(-1,-1) + Point(1, 1), Point(0 ,0))
        self.assertEqual(Point(-1, -1) + Point(-1, -1), Point(-2, -2))

    def test_sub(self):
        self.assertEqual(Point(10, 5) - Point(2, 3), Point(8, 2))
        self.assertEqual(Point(-1,-1) - Point(1, 1), Point(-2, -2))
        self.assertEqual(Point(-1, -1) - Point(-1, -1), Point(-0, 0))

if __name__ == '__main__':
    unittest.main()
