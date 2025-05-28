from __future__ import annotations

import itertools

from model.labyrinth import Labyrinth
from utils.random_engine import labyrinth_architect


def main() -> None:
    print("start")
    test_lab = Labyrinth(2,3)
    architect2 = labyrinth_architect(set([x for x in range(test_lab.size)]))


    for i in range(4):
        a = next(architect2)
        exclude_next = test_lab.get_surrounding_indexes(test_lab[choice_made])



    print("Generator finished naturally")







if __name__ == "__main__":
    main()
    