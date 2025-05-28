from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Dict, List

from model.obstacle import Obstacle
from utils.custom_exceptions import *
from model.direction import Direction

if TYPE_CHECKING:
    from model.labyrinth import Labyrinth
    from model.obstacle import Obstacle




class Square:
    def __init__(self, sequence:int, what_labyrinth: Optional["Labyrinth"]=None) -> None:
        self.connected_squares: Dict[Direction, Optional[Square]] = {
            Direction.UP: None,
            Direction.RIGHT: None,
            Direction.DOWN: None,
            Direction.LEFT: None}

        self.obstacles: List[Obstacle] = []
        self.what_labyrinth = what_labyrinth
        self.__sequence = sequence


        self.is_first = True if sequence == 0 else False
        self.is_last = True if sequence == self.what_labyrinth.size - 1 else False


    def __repr__(self) -> str:
        return f"[{self.__sequence}]"
        
    def check_wall(self, direction: Direction) -> bool:
        return self.connected_squares[direction] is None

    def build_wall(self, direction: Direction) -> None:
       self.connected_squares[direction] = None
   
        
    def link_to_square(self, direction: Direction, link_with: Square) -> None:

        if self.check_wall(direction):
            self.connected_squares[direction] = link_with
            link_with.link_to_square(Direction.get_opposite(direction), self)
        else:
            return