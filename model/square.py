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
        self.__sequence:int = sequence

        self.is_first = True if sequence == 0 else False
        self.is_last = True if sequence == self.what_labyrinth.size - 1 else False


    def build_wall(self, direction: Direction) -> None:
        if self.check_wall(direction):
            return

        sq_to_disconnect = self.connected_squares[direction]
        self.connected_squares[direction] = None
        sq_to_disconnect.build_wall(Direction.get_opposite(direction))

    def check_wall(self, direction: Direction) -> bool:
        return self.connected_squares[direction] is None

    def link_to_square(self, direction: Direction, link_with: Square) -> None:

        if self.check_wall(direction):
            self.connected_squares[direction] = link_with
            link_with.link_to_square(Direction.get_opposite(direction), self)
        else:
            return

    def get_sequence(self) -> int:
        return self.__sequence

    def move_to(self, direction: Direction) -> Optional[Square]:
        return self.connected_squares[direction]

    def __repr__(self):
        if self.is_first:
            return '🯅'
        elif self.is_last:
            return '🮱'
        return ' '