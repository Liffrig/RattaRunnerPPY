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
        self.size: int = self._max_rows * self._max_columns

        for i in range(self.size):
            self.__fields.append(Square(i,self))

        # hookup everything
        for i, sq in enumerate(self.__fields):

            border_check: bool = (i+1) % self._max_columns == 0
            last_row_check: bool = i >=  self._max_rows * (self._max_columns - 1)

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



        #
        # for i in range(self._max_rows):
        #     for j in range(self._max_columns):
        #         self.__fields.append(Square(i, j, self))
        #
        # for s in self.__fields:
        #     if s.column == 0:
        #         s.build_wall(Direction.LEFT)
        #     if s.column == self._max_columns - 1:
        #         s.build_wall(Direction.RIGHT)
        #     if s.row == 0:
        #         s.build_wall(Direction.UP)
        #     if s.row == self._max_rows - 1:
        #         s.build_wall(Direction.DOWN)




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

    # def get_surrounding_indexes(self,square: Square) -> List[int]:
    #     surroundings: List[int] = []
    #
    #     try:
    #         center: int = self.__fields.index(square)
    #     except ValueError:
    #         return surroundings
    #
    #     # check if a border on the side
    #     border_check_lr: int = center % self._max_columns
    #
    #     match border_check_lr:
    #         # the center is on the left border
    #         case 0:
    #             surroundings.append(center + 1) # field on the right
    #         # the center is on the right border
    #         case r if r == self._max_columns - 1 :
    #             surroundings.append(center - 1)
    #         # default case for non-border squares
    #         case _:
    #             surroundings.append(center - 1)  # left neighbor
    #             surroundings.append(center + 1)  # right neighbor
    #
    #     # check if border on the top or bottom
    #     border_check_ud: int = center // self._max_columns
    #
    #     match border_check_ud:
    #         # top border
    #         case 0:
    #             surroundings.append(center + self._max_columns)
    #         # bottom border
    #         case d if d == self._max_rows - 1:
    #             surroundings.append(center - self._max_columns)
    #         # default case for non-border squares
    #         case _:
    #             surroundings.append(center - self._max_columns)
    #             surroundings.append(center + self._max_columns)
    #
    #     # append also the center square
    #     surroundings.append(center)
    #     return surroundings
    #
    # def get_next_square(self,direction: Direction, square: Square) -> Optional[Square]:
    #     surroundings: List[int] = self.get_surrounding_indexes(square)
    #     try:
    #         return self.__fields[surroundings[direction.value]]
    #     except IndexError:
    #         return None
    #
    # def _get_square_on(self, row:int, column:int) -> Optional[Square]:
    #
    #     for square in self.__fields:
    #         if square.row == row and square.column == column:
    #             return square
    #
    #     return None