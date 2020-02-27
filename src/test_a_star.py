import unittest
from BaseObjects import Map, a_star

class MyTestCase(unittest.TestCase):

    def test_direct_route(self):
        test_map = Map()
        self.assertListEqual(a_star((1, 1), (9, 9), test_map),
                             [(2, 2), (3 ,3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])


if __name__ == '__main__':
    unittest.main()
