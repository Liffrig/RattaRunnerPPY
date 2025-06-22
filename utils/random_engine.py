from typing import Set, Generator, Optional, List, Tuple
from random import choice, randint, sample
from functools import wraps
from model.direction import Direction


def prime(func):
	"""Decorator to automatically prime a two-way generator."""
	@wraps(func)
	def wrapper(*args, **kwargs):
		gen = func(*args, **kwargs)
		next(gen)  # Prime the generator
		return gen

	return wrapper

@prime
def labyrinth_architect(full_list: Set[int]) -> Generator[int, None, None]:
	exclude_list: Optional[Set[int]] = None
	while full_list:
		if exclude_list is not None:
			full_list -= exclude_list
			if not full_list:
				return
			exclude_list = yield choice(list(full_list))
		else:
			exclude_list = yield choice(list(full_list))

	return

def random_direction_generator() -> Generator[Direction, None, None]:
	while True:
		yield Direction(randint(0, 3))


def roll_dice(range:int, lower:int = 0) -> int:
	return randint(lower, range)


def choose_stats(pool: List[float]) -> List[float]:
	ret_pool: List[float] = []
	size = len(pool)
	third = size // 3
	ret_pool.append(choice(pool[:third]))
	ret_pool.append(choice(pool[third:third*2]))
	ret_pool.append(choice(pool[third*2:]))
	return ret_pool


def get_k_uniques(up_range: int, k:int ) -> List[int]:
	return sample(range(up_range), k)