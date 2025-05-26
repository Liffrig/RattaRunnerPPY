import unittest

from model.direction import Direction
from model.square import Square
from utils.custom_exceptions import SquareWillBeClosedError


class ModelTests(unittest.TestCase):

    def test_square_ini(self):
        square = Square(1,2)
        self.assertEqual(square.row, 1)
        self.assertEqual(square.column, 2)
        self.assertEqual([0,0,0,0], square._walls)
    
    def test_walls(self):
        square = Square(1,1)
        self.assertEqual(square.check_wall(Direction.UP), False)
        square.build_wall(Direction.UP)
        self.assertEqual(square.check_wall(Direction.UP), True)

    def test_walls_exception(self):
        square = Square(0,0)
        with self.assertRaises(SquareWillBeClosedError):
            for direction in Direction:
                square.build_wall(direction)




if __name__ == '__main__':
    unittest.main()
