from tkinter import PhotoImage, Canvas, Tk, Frame, Button, LEFT, RIGHT
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
		self.canvas = Canvas(self.root, width=canvas_width, height=canvas_height, bg='floralwhite')
		self.canvas.pack(padx=10, pady=10) # żeby działało

		self.hero: Optional[MouseGUI] = None

		# Buttons
		btn_frame = Frame(self.root)
		btn_frame.pack(pady=10)
		Button(btn_frame, text="Zapierdalaj", command=self.run_little_buddy).pack(side=LEFT, padx=5)
		Button(btn_frame, text="Test", command=None).pack(side=LEFT, padx=5)


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
				fill="floralwhite",
				outline="gainsboro")

			wall_lines: Dict[Direction, Tuple[int, int, int, int]] = {
				Direction.UP: (x, y, x1, y),
				Direction.RIGHT: (x1, y, x1, y1),
				Direction.DOWN: (x, y1, x1, y1),
				Direction.LEFT: (x, y, x, y1)
			}

			for direction, coords in wall_lines.items():
				if sq.check_wall(direction):
					self.canvas.create_line(*coords, fill='gray1', width=self.wall_width, smooth=True)


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


	def animate_movement(self, from_pos: Square, to_pos: Square, callback=None) -> None:
		self.is_moving = True

		start_x, start_y = self._calculate_mid_sq_position(from_pos)
		end_x, end_y =  self._calculate_mid_sq_position(to_pos)

		# Animation parameters
		move_time = 0.5  # Random time between 0.5s and 2s
		step_delay = int(move_time * 1000 / self.animation_steps)  # Delay per step in ms

		# Calculate step increments
		dx = (end_x - start_x) / self.animation_steps
		dy = (end_y - start_y) / self.animation_steps

		def animate_step(step):
			if step >= self.animation_steps:
				# Animation complete
				self.hero.square_on = to_pos
				self.is_moving = False
				self.draw()  # Final redraw to ensure correct position

				if callback:
					callback()
				return

			# Redraw everything except the player
			self.draw(False)

			# Calculate current position
			current_x = start_x + dx * step
			current_y = start_y + dy * step

			self.canvas.create_image(current_x, current_y, image=self.hero.mouse_image)

			# Schedule next step
			self.root.after(step_delay, lambda: animate_step(step + 1))

		animate_step(0)

	def run_little_buddy(self):
		"""Animate the mouse following its chosen path"""
		if not self.hero or not self.hero.path_chosen:
			return

		def animate_next_step(step_index):
			# Check if we've reached the end of the path
			if step_index >= len(self.hero.path_chosen) - 1:
				return

			from_square = self.hero.path_chosen[step_index]
			to_square = self.hero.path_chosen[step_index + 1]

			# Animate movement to next square, with callback to continue the chain
			self.animate_movement(
				from_square,
				to_square,
				callback=lambda: animate_next_step(step_index + 1)
			)

		# Start the animation sequence
		animate_next_step(0)