from typing import Set, Generator, Optional
from random import choice, randint
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