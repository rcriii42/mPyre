import unittest
from BaseObjects import Map, a_star

class MyTestCase(unittest.TestCase):

    def test_direct_route(self):
        """
         01234567890
        0EEEEEEEEEEE
        1EsPPPPPPPPE
        2EPrPPPPPPPE
        3EPPrPPPPPPE
        4EPPPrPPPPPE
        5EPPPPrPPPPE
        6EPPPPPrPPPE
        7EPPPPPPrPPE
        8EPPPPPPPrPE
        9EPPPPPPPPgE
        0EEEEEEEEEEE
        """
        test_map = Map()
        self.assertListEqual(a_star((1, 1), (9, 9), test_map),
                             [(1, 1), (2, 2), (3 ,3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])

    def test_indirect_route(self):
        """
         01234567890
        0EEEEEEEEEEE
        1EsPPPPPPPPE
        2EP.PPPPPPPE
        3EPP.PPPPPPE
        4EPPP...PPPE
        5EWWWWWW.WWE
        6EPPPPP.PPPE
        7EPPPPPP.PPE
        8EPPPPPPP.PE
        9EPPPPPPPPgE
        0EEEEEEEEEEE
        """
        test_map = Map()
        for x in range(1, 7):
            test_map[(x, 5)] = 'water'
        for x in range(8, 10):
            test_map[(x, 5)] = 'water'
        route = a_star((1, 1), (9, 9), test_map)
        self.assertIn((1, 1), route)
        self.assertIn((7, 5), route)
        self.assertIn((9, 9), route)
        self.assertEqual(11, len(route))

    def test_multiple_routes(self):
        """
         01234567890
        0EEEEEEEEEEE
        1Es....PPPPE
        2EP.PPP.PPPE
        3EPP.PPP.PPE
        4EPPP.PPP.PE
        5EPPPP....gE
        6EPPPPPPPPPE
        7EPPPPPPPPPE
        8EPPPPPPPPPE
        9EPPPPPPPPPE
        0EEEEEEEEEEE
        """
        test_map = Map()
        route = a_star((1, 1), (9, 5), test_map)
        self.assertIn((1, 1), route)
        self.assertIn((9, 5), route)
        self.assertEqual(9, len(route))

    def test_indirect_route2(self):
        """
         01234567890
        0EEEEEEEEEEE
        1EsPPPPPPPPE
        2EP.PPPPPWPE
        3EPP.PPPPWPE
        4EPP.PPPPWPE
        5EP.WWWWWWPE
        6EPP.PPPPPPE
        7EPPP.PPPPPE
        8EPPPP.PPPPE
        9EPPPPP...gE
        0EEEEEEEEEEE
        """
        test_map = Map()
        for x in range(3, 10):
            test_map[(x, 5)] = 'water'
        route = a_star((1, 1), (9, 9), test_map)
        self.assertIn((1, 1), route)
        self.assertTrue((1, 5) in route or (2, 5) in route)
        self.assertIn((9, 9), route)

    def test_no_route(self):
        """
         01234567890
        0EEEEEEEEEEE
        1EsPPPPPPPPE
        2EP.PPPPPPPE
        3EPP.PPPPPPE
        4EPPP...PPPE
        5EWWWWWWWWWE
        6EPPPPPPPPPE
        7EPPPPPPPPPE
        8EPPPPPPPPPE
        9EPPPPPPPPgE
        0EEEEEEEEEEE
        """
        test_map = Map()
        for x in range(1, 10):
            test_map[(x, 5)] = 'water'
        self.assertFalse(a_star((1, 1), (9, 9), test_map))

if __name__ == '__main__':
    unittest.main()
