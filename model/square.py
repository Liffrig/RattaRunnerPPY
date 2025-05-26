from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from utils.custom_exceptions import *
from model.direction import Direction

if TYPE_CHECKING:
    from model.labyrinth import Labyrinth




class Square:
    def __init__(self, row: int, column: int, what_labyrinth: Optional["Labyrinth"]=None) -> None:
        self.row = row
        self.column = column
        self.what_labyrinth = what_labyrinth
        
        self._walls = [0 for _ in range(4)]



    def __repr__(self) -> str:
        return f"[{self.row}, {self.column}]"
        
    def check_wall(self, direction: Direction) -> bool:
        return bool(self._walls[direction.value])


    def build_wall(self, direction: Direction) -> None:
        if sum(self._walls) == 3:
            raise SquareWillBeClosedError()
    
        self._walls[direction.value] = 1
   
        
     