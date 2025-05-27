from __future__ import annotations
from collections.abc import Iterable
from typing import Iterator, Optional, List, TYPE_CHECKING

from model.direction import Direction
from model.square import Square

if TYPE_CHECKING:
    from model.square import Square


class Labyrinth(Iterable):
    def __init__(self, max_rows: int, max_columns: int):
        self._max_rows: int = max_rows
        self._max_columns: int = max_columns
        self.__fields: List['Square'] = []

        for i in range(self._max_rows):
            for j in range(self._max_columns):
                self.__fields.append(Square(i, j, self))

        for s in self.__fields:
            if s.column == 0:
                s.build_wall(Direction.LEFT)
            if s.column == self._max_columns - 1:
                s.build_wall(Direction.RIGHT)
            if s.row == 0:
                s.build_wall(Direction.UP)
            if s.row == self._max_rows - 1:
                s.build_wall(Direction.DOWN)


        self.size: int = self._max_rows * self._max_columns

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

    def get_surrounding_indexes(self,square: Square) -> List[int]:
        surroundings: List[int] = []

        try:
            center: int = self.__fields.index(square)
        except ValueError:
            return surroundings

        # check if a border on the side
        border_check_lr: int = center % self._max_columns

        match border_check_lr:
            # the center is on the left border
            case 0:
                surroundings.append(center + 1) # field on the right
            # the center is on the right border
            case r if r == self._max_columns - 1 :
                surroundings.append(center - 1)
            # default case for non-border squares
            case _:
                surroundings.append(center - 1)  # left neighbor
                surroundings.append(center + 1)  # right neighbor

        # check if border on the top or bottom
        border_check_ud: int = center // self._max_columns

        match border_check_ud:
            # top border
            case 0:
                surroundings.append(center + self._max_columns)
            # bottom border
            case d if d == self._max_rows - 1:
                surroundings.append(center - self._max_columns)
            # default case for non-border squares
            case _:
                surroundings.append(center - self._max_columns)
                surroundings.append(center + self._max_columns)

        # append also the center square
        surroundings.append(center)
        return surroundings
