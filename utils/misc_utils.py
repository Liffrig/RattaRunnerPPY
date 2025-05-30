from collections import deque

from model.square import Square
from model.direction import Direction

def has_path_to_bottom_right(start_square: Square) -> bool:
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