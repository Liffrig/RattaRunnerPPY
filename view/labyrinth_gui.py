import tkinter as tk
from typing import Tuple, Dict

from model.labyrinth import Labyrinth
from model.direction import Direction
from utils.misc_utils import BASE_SETTINGS
from utils.random_engine import choose_in_range


class LabyrinthGUI(Labyrinth):
	def __init__(self, max_rows: int, max_columns: int) -> None:
		super().__init__(max_rows, max_columns)
		self.root = tk.Tk()
		self.root.title(f"Labyrinth {self._max_rows} x {self._max_columns}")

		self.cell_size: int = BASE_SETTINGS["cell_size"]
		self.wall_width: int = BASE_SETTINGS["wall_width"]
		self.animation_steps: int = BASE_SETTINGS["animation_steps"]

		self.mouse_model: tk.PhotoImage = tk.PhotoImage(file=f"./asset/mouse{choose_in_range(10)}.png")
		image_size:int = int(self.cell_size * BASE_SETTINGS["image_size"])
		self.mouse_model = self.mouse_model.subsample(
			max(1, self.mouse_model.width() // image_size),
			max(1, self.mouse_model.height() // image_size)
		)

		canvas_width: float = self.max_columns * self.cell_size + BASE_SETTINGS["canvas_padding"]
		canvas_height: float = self.max_rows * self.cell_size + BASE_SETTINGS["canvas_padding"]
		self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg='aliceblue')
		self.canvas.pack(padx=10, pady=10) # żeby działało

		self.draw()

	def draw(self):
		self.canvas.delete("all")

		for sq in self:
			x = sq.col * self.cell_size + BASE_SETTINGS["square_padding"]
			y = sq.row * self.cell_size + BASE_SETTINGS["square_padding"]

			x1 = x + self.cell_size
			y1 = y + self.cell_size

			self.canvas.create_rectangle(
				# lewy górny róg
				x,
				y,
				# prawy dolny róg
				x+self.cell_size,
				y+self.cell_size,
				fill="ivory3",
				outline="white")

			wall_lines: Dict[Direction, Tuple[int, int, int, int]] = {
				Direction.UP: (x, y, x1, y),
				Direction.RIGHT: (x1, y, x1, y1),
				Direction.DOWN: (x, y1, x1, y1),
				Direction.LEFT: (x, y, x, y1)
			}

			for direction, coords in wall_lines.items():
				if sq.check_wall(direction):
					self.canvas.create_line(*coords, fill='black', width=self.wall_width)
