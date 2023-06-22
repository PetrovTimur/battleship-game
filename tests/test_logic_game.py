from battleship.logic.game import Ship
import unittest


class ShipPlaceTestCase(unittest.TestCase):

    def test_place_1(self):
        self.ship = Ship(3)
        self.ship.place([(1, 1), (1, 2), (1, 3)])
        self.assertEqual(self.ship.status[(1, 1)], False)
        self.assertEqual(self.ship.status[(1, 2)], False)
        self.assertEqual(self.ship.status[(1, 3)], False)
        self.assertEqual(self.ship.placed, True)

    def test_place_2(self):
        self.ship = Ship(3)
        self.ship.place([(5, 5), (6, 5), (7, 5)])
        self.assertEqual(self.ship.status[(5, 5)], False)
        self.assertEqual(self.ship.status[(6, 5)], False)
        self.assertEqual(self.ship.status[(7, 5)], False)
        self.assertEqual(self.ship.placed, True)

    def test_place_3(self):
        self.ship = Ship(2)
        self.ship.place([(5, 5), (4, 5)])
        self.assertEqual(self.ship.status[(5, 5)], False)
        self.assertEqual(self.ship.status[(4, 5)], False)
        self.assertEqual(self.ship.placed, True)


class ShipHitTestCase(unittest.TestCase):

    def test_place_1(self):
        self.ship = Ship(3)
        self.ship.place([(1, 1), (1, 2), (1, 3)])
        self.ship.hit((1, 2))
        self.assertEqual(self.ship.status[(1, 2)], True)
        self.assertEqual(self.ship.afloat, True)

    def test_place_2(self):
        self.ship = Ship(3)
        self.ship.place([(5, 5), (6, 5), (7, 5)])
        self.ship.hit((7, 5))
        self.assertEqual(self.ship.status[(7, 5)], True)
        self.assertEqual(self.ship.afloat, True)

    def test_place_3(self):
        self.ship = Ship(2)
        self.ship.place([(5, 5), (4, 5)])
        self.ship.hit((5, 5))
        self.ship.hit((4, 5))
        self.assertEqual(self.ship.status[(5, 5)], True)
        self.assertEqual(self.ship.status[(4, 5)], True)
        self.assertEqual(self.ship.afloat, False)


if __name__ == "__main__":
    unittest.main()
