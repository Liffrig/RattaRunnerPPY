from __future__ import annotations

import itertools

from model.direction import Direction
from model.labyrinth import Labyrinth
from utils.random_engine import labyrinth_architect, random_direction_generator
from utils.misc_utils import has_path_to_bottom_right

def main() -> None:
# TODO move to a function
  test_lab = Labyrinth(4,4)
  fn = labyrinth_architect(set([x for x in range(test_lab.size)]))
  rdg = random_direction_generator()
  seq_i = next(fn)

  for i in range(test_lab._max_columns+2):
      drawn_sq = test_lab.get_square_by_sequence(seq_i)
      nbrs = test_lab.get_surrounding_indexes(drawn_sq)
      drawn_dir = next(rdg)
      disjoint_sq = drawn_sq.move_to(drawn_dir)
      drawn_sq.build_wall(drawn_dir)
      if has_path_to_bottom_right(test_lab.start):
          try:
            seq_i = fn.send(nbrs)
          except StopIteration:
            break
      else:
          # rollback
          drawn_sq.link_to_square(drawn_dir, disjoint_sq)
          break

  print(test_lab)









if __name__ == "__main__":
    main()
    