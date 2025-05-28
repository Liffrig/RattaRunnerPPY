from __future__ import annotations
from enum import Enum

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @classmethod
    def get_opposite(cls, direction: Direction) -> Literal[
	                                                   Direction.RIGHT, Direction.LEFT, Direction.DOWN, Direction.UP] | None:
        match direction:
            case Direction.UP:
                return Direction.DOWN
            case Direction.RIGHT:
                return Direction.LEFT
            case Direction.DOWN:
                return Direction.UP
            case Direction.LEFT:
                return Direction.RIGHT
        return None
