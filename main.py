from __future__ import annotations

import itertools

from model.labyrinth import Labyrinth
from utils.random_engine import labyrinth_architect


def main() -> None:
    print("start")
    g = labyrinth_architect(7)
    g.send(None)
    print(g.send([5,6]))
    print(g.send([1, 2]))


if __name__ == "__main__":
    main()
    