from __future__ import annotations
from collections.abc import Iterable
from typing import Iterator, Optional, List, TYPE_CHECKING
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
