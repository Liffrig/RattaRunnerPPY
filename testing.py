import unittest

from model.direction import Direction
from model.labyrinth import Labyrinth
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

    def test_surroundings_calculation(self):

        expected_results = [
            [1,3,0],
            [0,2,4,1],
            [1,5,2],
            [4,0,6,3],
            [3,5,1,7,4],
            [4,2,8,5],
            [7,3,6],
            [6,8,4,7],
            [7,5,8]
        ]

        test_lab = Labyrinth(3,3)
        for i,square in enumerate(test_lab):
            self.assertEqual(expected_results[i], test_lab.get_surrounding_indexes(square))


    def test_ini_walls_in_labyrinth(self):
        expected_results = [
            [1, 0, 0, 1],
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 1, 1, 0]
        ]

        for i,square in enumerate(Labyrinth(2,2)):
            self.assertEqual(expected_results[i], square._walls)

if __name__ == '__main__':
    unittest.main()
