from typing import Set, Generator, Optional
from random import choice

def labyrinth_architect(full_list: Set[int]) -> Generator[int, None, None]:
	exclude_list: Optional[Set[int]] = None
	while full_list:
		if exclude_list is not None:
			full_list -= set(exclude_list)
			exclude_list = yield choice(list(full_list))
		else:
			exclude_list = yield choice(list(full_list))
