from __future__ import annotations
from collections.abc import Iterable
from typing import Iterator, Optional, List, TYPE_CHECKING, Set
from model.direction import Direction
from model.square import Square

# if TYPE_CHECKING:
#     from model.square import Square


class Labyrinth(Iterable):
    def __init__(self, max_rows: int, max_columns: int):
        self._max_rows: int = max_rows
        self._max_columns: int = max_columns
        self.__fields: List['Square'] = []
        self.size: int = self._max_rows * self._max_columns


        for i in range(self.size):
            self.__fields.append(Square(i,self))

        # hook everything up
        for i, sq in enumerate(self.__fields):
            border_check: bool = (i+1) % self._max_columns == 0
            last_row_check: bool = i >= self._max_columns * (self._max_rows - 1)

            if sq.is_last:
                break

            if not (border_check or last_row_check):
                sq.link_to_square(Direction.RIGHT, self.__fields[i+1])
                sq.link_to_square(Direction.DOWN, self.__fields[i+self._max_columns])
                continue
            elif last_row_check:
                sq.link_to_square(Direction.RIGHT, self.__fields[i+1])
                continue
            elif border_check:
                sq.link_to_square(Direction.DOWN, self.__fields[i+self._max_columns])
                continue

        self.start: Square = self.get_square_by_sequence(0)


    def __iter__(self) -> Iterator[Optional[Square]]:
        return iter(self.__fields)

    def __getitem__(self, index: int) -> Optional[Square]:
        return self.__fields[index]

    def __repr__(self) -> str:
        result: str = ""
        i: int = 0
        for row in range(self._max_rows):
            for column in range(self._max_columns):
                result += (str(self.__fields[i]) + " ")
                i += 1
            result += "\n"

        return result

    def get_surrounding_indexes(self, element: Square | int) -> Set[int]:
        surroundings = set()
        square: Square = self.get_square_by_sequence(element) if type(element) == int else element

        for direction in Direction:
            if not square.check_wall(direction):
                surroundings.add(square.move_to(direction).get_sequence())

        surroundings.add(square.get_sequence())
        return surroundings


    def get_square_by_sequence(self, sequence:int) -> Square:
        try:
            square = self.__fields[sequence]
        except IndexError:
            raise IndexError("sequence out of range")

        return square