from collections import deque
from typing import Dict, Tuple
from model.square import Square
from model.direction import Direction


BASE_SETTINGS: Dict[str, int|float] = {
	'cell_size': 150,
	'wall_width': 10,
	'animation_steps': 50,
	'image_size': 0.75,
	'canvas_padding': 25,
	'square_padding': 10,
	'abilities_base_mult': 30
}

BUTTON_DESIGN: Dict[str,str|Tuple[str,int]] = {
	'font' : ('Fira Code', 15),
	'bg' : 'red',
	'fg' : 'yellow',
	'activebackground' : 'yellow',
	'activeforeground' : 'red',
}


LABEL_DESIGN: Dict[str,str|Tuple[str,int]] = {
	'bg' : 'white',
	'font' : ('Fira Code', 12)
}


def check_labyrinth_solution(start_square: Square) -> bool:
	if start_square.is_last:
		return True

	visited = {start_square}
	queue = deque([start_square])

	while queue:
		current = queue.popleft()

		# Check all 4 directions
		for direction in Direction:
			next_square = current.move_to(direction)
			if next_square and (next_square not in visited):
				if next_square.is_last:
					return True
				visited.add(next_square)
				queue.append(next_square)

	return False



