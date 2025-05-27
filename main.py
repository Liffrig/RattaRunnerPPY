from __future__ import annotations

import itertools

from model.labyrinth import Labyrinth
from utils.random_engine import labyrinth_architect


def main() -> None:
    print("start")
    test_lab = Labyrinth(2,3)
    g = labyrinth_architect(set([x for x in range(test_lab.size)]))


    for i in g:
        print(f"***{i}***")
        w = test_lab.get_surrounding_indexes(test_lab[i])
        print(f"{w=}  ")
        first_sq = g.send(w)
        print(f"{first_sq=}  ")



if __name__ == "__main__":
    main()
    