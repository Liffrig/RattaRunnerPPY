from typing import List, Generator
from random import choice

def labyrinth_architect(free_properties: List[int] | int) -> Generator[int, None, None]:
	where_to_build = None
	possible_positions = None
	while True:
		if type(free_properties) == int:
			possible_positions = [x for x in range(free_properties)]
			where_to_build = yield choice(possible_positions)
		else:
			possible_positions  -= free_properties
			where_to_build = yield choice(possible_positions)

		print(possible_positions)