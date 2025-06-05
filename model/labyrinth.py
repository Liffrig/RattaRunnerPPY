from __future__ import annotations
from collections.abc import Iterable
from typing import Iterator, Optional, List, TYPE_CHECKING, Set
from model.direction import Direction
from utils.misc_utils import check_labyrinth_solution
from utils.random_engine import labyrinth_architect, random_direction_generator
from model.square import Square
from model.mouse import Mouse

if TYPE_CHECKING:
    from model.square import Square
    from model.mouse import Mouse


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

        self.hero: Optional[Mouse] = None


    def __iter__(self) -> Iterator[Optional['Square']]:
        return iter(self.__fields)

    def __getitem__(self, index: int) -> Optional['Square']:
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

    def get_surrounding_indexes(self, element: 'Square' | int) -> Set[int]:
        surroundings = set()
        square = self.get_square_by_sequence(element) if type(element) == int else element

        for direction in Direction:
            if not square.check_wall(direction):
                surroundings.add(square.move_to(direction).get_sequence())

        surroundings.add(square.get_sequence())
        return surroundings


    def get_square_by_sequence(self, sequence:int) -> 'Square':
        try:
            square = self.__fields[sequence]
        except IndexError:
            raise IndexError("sequence out of range")

        return square

    def _construct_random_walls(self) -> None:
        sq_gen = labyrinth_architect(set([x for x in range(self.size)]))
        rdg = random_direction_generator()
        seq_i = next(sq_gen)

        for i in range(self._max_columns * 4):
            drawn_sq = self.get_square_by_sequence(seq_i)
            nbrs = self.get_surrounding_indexes(drawn_sq)
            drawn_dir = next(rdg)
            disjoint_sq = drawn_sq.move_to(drawn_dir)
            drawn_sq.build_wall(drawn_dir)
            if check_labyrinth_solution(drawn_sq):
                try:
                    seq_i = sq_gen.send(nbrs)
                except StopIteration:
                    break
            else:
                # rollback
                drawn_sq.link_to_square(drawn_dir, disjoint_sq)
                break

    @property
    def max_columns(self):
        return self._max_columns

    @property
    def max_rows(self):
        return self._max_rows

    def link(self, mouse: 'Mouse') -> None:
        if self.hero is None:
            self.hero = mouse
            mouse.link(self)