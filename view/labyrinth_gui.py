import tkinter as tk
from typing import Tuple, Dict, Optional, TYPE_CHECKING
from model.labyrinth import Labyrinth

from model.direction import Direction
from utils.misc_utils import BASE_SETTINGS
from utils.random_engine import roll_dice

if TYPE_CHECKING:
	from view.mouse_gui import MouseGUI
	from model.labyrinth import Labyrinth




class LabyrinthGUI(Labyrinth):
	def __init__(self, max_rows: int, max_columns: int) -> None:
		super().__init__(max_rows, max_columns)
		self.root = tk.Tk()
		self.root.title(f"Labyrinth {self._max_rows} x {self._max_columns}")

		self.cell_size: int = BASE_SETTINGS["cell_size"]
		self.wall_width: int = BASE_SETTINGS["wall_width"]
		self.animation_steps: int = BASE_SETTINGS["animation_steps"]


		canvas_width: float = self.max_columns * self.cell_size + BASE_SETTINGS["canvas_padding"]
		canvas_height: float = self.max_rows * self.cell_size + BASE_SETTINGS["canvas_padding"]
		self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg='aliceblue')
		self.canvas.pack(padx=10, pady=10) # żeby działało

		self.hero: Optional[MouseGUI] = None
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
					self.canvas.create_line(*coords, fill='black', width=self.wall_width, smooth=True)


		self.draw_hero()

	def draw_hero(self):
		if self.hero is None:
			return

		row = self.hero.square_on.row + 1
		col = self.hero.square_on.col + 1

		x = (col * self.cell_size) // 2
		y = (row * self.cell_size) // 2

		self.canvas.create_image(x,y, image = self.hero.mouse_image)
