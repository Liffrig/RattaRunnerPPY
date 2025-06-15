from tkinter import PhotoImage, Canvas, Tk
from typing import Tuple, Dict, Optional, TYPE_CHECKING
from model.labyrinth import Labyrinth

from model.direction import Direction
from model.square import Square
from utils.misc_utils import BASE_SETTINGS
from utils.random_engine import roll_dice

if TYPE_CHECKING:
	from view.mouse_gui import MouseGUI
	from model.labyrinth import Labyrinth


class LabyrinthGUI(Labyrinth):
	def __init__(self, max_rows: int, max_columns: int) -> None:
		super().__init__(max_rows, max_columns)
		self.root = Tk()
		self.root.title(f"Labyrinth {self._max_rows} x {self._max_columns}")
		self.finish_image = PhotoImage(file="asset/chizu.png")
		self.cell_size: int = BASE_SETTINGS["cell_size"]
		self.wall_width: int = BASE_SETTINGS["wall_width"]
		self.animation_steps: int = BASE_SETTINGS["animation_steps"]
		self.is_moving = False

		canvas_width: float = self.max_columns * self.cell_size + BASE_SETTINGS["canvas_padding"]
		canvas_height: float = self.max_rows * self.cell_size + BASE_SETTINGS["canvas_padding"]
		self.canvas = Canvas(self.root, width=canvas_width, height=canvas_height, bg='aliceblue')
		self.canvas.pack(padx=10, pady=10) # żeby działało

		self.hero: Optional[MouseGUI] = None
		self.root.bind('<KeyPress>', self.on_key_press)
		self.root.focus_set()  # Make sure window can receive key events
		self.draw()


	def draw(self, include_mouse: bool = True) -> None:
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


		self.draw_static_elem(self.finish)

		if include_mouse:
			self.draw_hero()


	def draw_hero(self):
		if self.hero is None:
			return

		x,y = self._calculate_mid_sq_position(self.hero.square_on)

		self.canvas.create_image(x,y, image = self.hero.mouse_image)


	def draw_static_elem(self, sq: Square) -> None:

		x,y = self._calculate_mid_sq_position(sq)

		print(x, y)

		image_size:int = int(BASE_SETTINGS['cell_size'] * BASE_SETTINGS["image_size"])
		self.cheese_image = self.finish_image.subsample(
			max(1, self.finish_image.width() // image_size),
			max(1, self.finish_image.height() // image_size)
		)

		self.canvas.create_image(x, y, image=self.cheese_image)


		# image_size:int = int(BASE_SETTINGS['cell_size'] * BASE_SETTINGS["image_size"])
		# self.mouse_image = self.mouse_image.subsample(
		# 	max(1, self.mouse_image.width() // image_size),
		# 	max(1, self.mouse_image.height() // image_size)
		# )

	def _calculate_mid_sq_position(self, sq: Square) -> Tuple[int, int]:

		x = (self.cell_size // 2) + (sq.col * self.cell_size) + BASE_SETTINGS["square_padding"]
		y = (self.cell_size // 2) + (sq.row * self.cell_size) + BASE_SETTINGS["square_padding"]
		return x, y

	def on_key_press(self, event):
		key = event.keysym.lower()
		direction = None

		if key == 'up' or key == 'w':
			direction = Direction.UP
		elif key == 'down' or key == 's':
			direction = Direction.DOWN
		elif key == 'left' or key == 'a':
			direction = Direction.LEFT
		elif key == 'right' or key == 'd':
			direction = Direction.RIGHT

		if direction:
			self.hero.move_to(direction)

		self.draw()