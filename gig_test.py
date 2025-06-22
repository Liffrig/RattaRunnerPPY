# # import tkinter as tk
# # from tkinter import PhotoImage
# # from typing import List, Optional, Iterable, Iterator, Set
# # from enum import Enum
# # import random
# # import os
# #
# #
# # class Direction(Enum):
# # 	UP = "UP"
# # 	DOWN = "DOWN"
# # 	LEFT = "LEFT"
# # 	RIGHT = "RIGHT"
# #
# #
# #
# #
# #
# # class Labyrinth(Iterable):
# # 	def __init__(self, max_rows: int, max_columns: int):
# # 		self._max_rows: int = max_rows
# # 		self._max_columns: int = max_columns
# # 		self.__fields: List['Square'] = []
# # 		self.size: int = self._max_rows * self._max_columns
# #
# # 		for i in range(self.size):
# # 			self.__fields.append(Square(i, self))
# #
# # 		# hook everything up
# # 		for i, sq in enumerate(self.__fields):
# # 			border_check: bool = (i + 1) % self._max_columns == 0
# # 			last_row_check: bool = i >= self._max_columns * (self._max_rows - 1)
# #
# # 			if sq.is_last:
# # 				break
# #
# # 			if not (border_check or last_row_check):
# # 				sq.link_to_square(Direction.RIGHT, self.__fields[i + 1])
# # 				sq.link_to_square(Direction.DOWN, self.__fields[i + self._max_columns])
# # 				continue
# # 			elif last_row_check and not border_check:
# # 				sq.link_to_square(Direction.RIGHT, self.__fields[i + 1])
# # 				continue
# # 			elif border_check and not last_row_check:
# # 				sq.link_to_square(Direction.DOWN, self.__fields[i + self._max_columns])
# # 				continue
# #
# # 		self.start: Square = self.get_square_by_sequence(0)
# #
# # 	def __iter__(self) -> Iterator[Optional[Square]]:
# # 		return iter(self.__fields)
# #
# # 	def __getitem__(self, index: int) -> Optional[Square]:
# # 		return self.__fields[index]
# #
# # 	def get_square_by_sequence(self, sequence: int) -> Square:
# # 		return self.__fields[sequence]
# #
# # 	def construct_random_walls(self) -> None:
# # 		# Simple random wall construction
# # 		for square in self.__fields:
# # 			for direction in [Direction.RIGHT, Direction.DOWN]:
# # 				if random.random() < 0.3:  # 30% chance to build wall
# # 					square.build_wall(direction)
# #
# #
# # class LabyrinthGUI:
# # 	def __init__(self, rows=6, cols=6):
# # 		self.labyrinth = Labyrinth(rows, cols)
# # 		self.root = tk.Tk()
# # 		self.root.title("Labyrinth")
# # 		self.cell_size = 120
# # 		self.wall_width = 8
# # 		self.player_pos = 0  # Start at square 0
# # 		self.is_moving = False  # Flag to prevent movement during animation
# # 		self.animation_steps = 50  # Number of steps for smooth movement
# #
# # 		# Load mouse image
# # 		try:
# # 			self.mouse_image = PhotoImage(file="../asset/m1.png")
# # 			# Resize image to fit in cell
# # 			image_size = self.cell_size - 10  # Leave some padding
# # 			self.mouse_image = self.mouse_image.subsample(
# # 				max(1, self.mouse_image.width() // image_size),
# # 				max(1, self.mouse_image.height() // image_size)
# # 			)
# # 		except (tk.TclError, FileNotFoundError):
# # 			print("Warning: Could not load asset/mouse.png, using red circle instead")
# # 			self.mouse_image = None
# #
# # 		# Buttons
# # 		btn_frame = tk.Frame(self.root)
# # 		btn_frame.pack(pady=10)
# #
# # 		tk.Button(btn_frame, text="Add Random Walls", command=self.add_walls).pack(side=tk.LEFT, padx=5)
# # 		tk.Button(btn_frame, text="Clear Walls", command=self.clear_walls).pack(side=tk.LEFT, padx=5)
# # 		tk.Button(btn_frame, text="Auto Move", command=self.start_auto_move).pack(side=tk.LEFT, padx=5)
# # 		tk.Button(btn_frame, text="Stop Auto", command=self.stop_auto_move).pack(side=tk.LEFT, padx=5)
# #
# # 		# Canvas
# # 		canvas_width = cols * self.cell_size + 20
# # 		canvas_height = rows * self.cell_size + 20
# # 		self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg='white')
# # 		self.canvas.pack(padx=10, pady=10)
# #
# # 		# Auto movement
# # 		self.auto_move_active = False
# # 		self.auto_move_job = None
# #
# # 		# Keyboard bindings
# # 		self.root.bind('<KeyPress>', self.on_key_press)
# # 		self.root.focus_set()  # Make sure window can receive key events
# #
# # 		self.draw()
# #
# # 	def draw(self):
# # 		self.canvas.delete("all")
# # 		rows = self.labyrinth._max_rows
# # 		cols = self.labyrinth._max_columns
# #
# # 		for row in range(rows):
# # 			for col in range(cols):
# # 				sequence = row * cols + col
# # 				square = self.labyrinth.get_square_by_sequence(sequence)
# #
# # 				x = col * self.cell_size + 10
# # 				y = row * self.cell_size + 10
# #
# # 				# Draw cell
# # 				self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size,
# # 				                             fill='lightblue', outline='gray')
# #
# #
# # 				# Draw walls
# # 				if square.check_wall(Direction.UP):
# # 					self.canvas.create_line(x, y, x + self.cell_size, y,
# # 					                        fill='black', width=self.wall_width)
# #
# # 				if square.check_wall(Direction.DOWN):
# # 					self.canvas.create_line(x, y + self.cell_size, x + self.cell_size, y + self.cell_size,
# # 					                        fill='black', width=self.wall_width)
# #
# # 				if square.check_wall(Direction.LEFT):
# # 					self.canvas.create_line(x, y, x, y + self.cell_size,
# # 					                        fill='black', width=self.wall_width)
# #
# # 				if square.check_wall(Direction.RIGHT):
# # 					self.canvas.create_line(x + self.cell_size, y, x + self.cell_size, y + self.cell_size,
# # 					                        fill='black', width=self.wall_width)
# #
# # 		# Draw player (red circle)
# # 		self.draw_player()
# #
# # 	def draw_player(self):
# # 		rows = self.labyrinth._max_rows
# # 		cols = self.labyrinth._max_columns
# #
# # 		# Convert player position to row, col
# # 		row = self.player_pos // cols
# # 		col = self.player_pos % cols
# #
# # 		# Calculate position (center of the cell)
# # 		x = col * self.cell_size + 10 + self.cell_size // 2
# # 		y = row * self.cell_size + 10 + self.cell_size // 2
# #
# # 		if self.mouse_image:
# # 			# Draw mouse image
# # 			self.canvas.create_image(x, y, image=self.mouse_image)
# # 		else:
# # 			# Fallback to red circle if image not available
# # 			radius = self.cell_size // 4
# # 			self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
# # 			                        fill='red', outline='darkred', width=2)
# #
# # 	def on_key_press(self, event):
# # 		if self.is_moving:  # Don't allow manual movement during animation
# # 			return
# #
# # 		key = event.keysym.lower()
# # 		direction = None
# #
# # 		if key == 'up' or key == 'w':
# # 			direction = Direction.UP
# # 		elif key == 'down' or key == 's':
# # 			direction = Direction.DOWN
# # 		elif key == 'left' or key == 'a':
# # 			direction = Direction.LEFT
# # 		elif key == 'right' or key == 'd':
# # 			direction = Direction.RIGHT
# #
# # 		if direction:
# # 			self.move_player(direction)
# #
# # 	def move_player(self, direction):
# # 		if self.is_moving:  # Prevent multiple simultaneous movements
# # 			return
# #
# # 		current_square = self.labyrinth.get_square_by_sequence(self.player_pos)
# #
# # 		# Check if there's a wall in that direction
# # 		if not current_square.check_wall(direction):
# # 			# No wall, can move
# # 			next_square = current_square.move_to(direction)
# # 			if next_square:
# # 				self.animate_movement(self.player_pos, next_square.get_sequence())
# #
# # 	def animate_movement(self, from_pos, to_pos):
# # 		self.is_moving = True
# # 		rows = self.labyrinth._max_rows
# # 		cols = self.labyrinth._max_columns
# #
# # 		# Calculate start and end positions
# # 		from_row, from_col = from_pos // cols, from_pos % cols
# # 		to_row, to_col = to_pos // cols, to_pos % cols
# #
# # 		start_x = from_col * self.cell_size + 10 + self.cell_size // 2
# # 		start_y = from_row * self.cell_size + 10 + self.cell_size // 2
# # 		end_x = to_col * self.cell_size + 10 + self.cell_size // 2
# # 		end_y = to_row * self.cell_size + 10 + self.cell_size // 2
# #
# # 		# Animation parameters
# # 		move_time = random.uniform(0.5, 2.0)  # Random time between 0.5s and 2s
# # 		step_delay = int(move_time * 1000 / self.animation_steps)  # Delay per step in ms
# #
# # 		# Calculate step increments
# # 		dx = (end_x - start_x) / self.animation_steps
# # 		dy = (end_y - start_y) / self.animation_steps
# #
# # 		def animate_step(step):
# # 			if step >= self.animation_steps:
# # 				# Animation complete
# # 				self.player_pos = to_pos
# # 				self.is_moving = False
# # 				self.draw()  # Final redraw to ensure correct position
# # 				return
# #
# # 			# Redraw everything except the player
# # 			self.draw_labyrinth_only()
# #
# # 			# Calculate current position
# # 			current_x = start_x + dx * step
# # 			current_y = start_y + dy * step
# #
# # 			# Draw player at current position
# # 			if self.mouse_image:
# # 				self.canvas.create_image(current_x, current_y, image=self.mouse_image)
# # 			else:
# # 				radius = self.cell_size // 4
# # 				self.canvas.create_oval(current_x - radius, current_y - radius,
# # 				                        current_x + radius, current_y + radius,
# # 				                        fill='red', outline='darkred', width=2)
# #
# # 			# Schedule next step
# # 			self.root.after(step_delay, lambda: animate_step(step + 1))
# #
# # 		animate_step(0)
# #
# # 	def draw_labyrinth_only(self):
# # 		"""Draw only the labyrinth without the player"""
# # 		self.canvas.delete("all")
# # 		rows = self.labyrinth._max_rows
# # 		cols = self.labyrinth._max_columns
# #
# # 		for row in range(rows):
# # 			for col in range(cols):
# # 				sequence = row * cols + col
# # 				square = self.labyrinth.get_square_by_sequence(sequence)
# #
# # 				x = col * self.cell_size + 10
# # 				y = row * self.cell_size + 10
# #
# # 				# Draw cell
# # 				self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size,
# # 				                             fill='lightblue', outline='gray')
# #
# #
# # 				# Draw walls
# # 				if square.check_wall(Direction.UP):
# # 					self.canvas.create_line(x, y, x + self.cell_size, y,
# # 					                        fill='black', width=self.wall_width)
# #
# # 				if square.check_wall(Direction.DOWN):
# # 					self.canvas.create_line(x, y + self.cell_size, x + self.cell_size, y + self.cell_size,
# # 					                        fill='black', width=self.wall_width)
# #
# # 				if square.check_wall(Direction.LEFT):
# # 					self.canvas.create_line(x, y, x, y + self.cell_size,
# # 					                        fill='black', width=self.wall_width)
# #
# # 				if square.check_wall(Direction.RIGHT):
# # 					self.canvas.create_line(x + self.cell_size, y, x + self.cell_size, y + self.cell_size,
# # 					                        fill='black', width=self.wall_width)
# #
# # 	def start_auto_move(self):
# # 		if not self.auto_move_active:
# # 			self.auto_move_active = True
# # 			self.auto_move()
# #
# # 	def stop_auto_move(self):
# # 		self.auto_move_active = False
# # 		if self.auto_move_job:
# # 			self.root.after_cancel(self.auto_move_job)
# # 			self.auto_move_job = None
# #
# # 	def auto_move(self):
# # 		if not self.auto_move_active or self.is_moving:
# # 			if self.auto_move_active:  # Reschedule if still active but currently moving
# # 				self.auto_move_job = self.root.after(100, self.auto_move)
# # 			return
# #
# # 		# Get current square and find possible moves
# # 		current_square = self.labyrinth.get_square_by_sequence(self.player_pos)
# # 		possible_directions = []
# #
# # 		for direction in Direction:
# # 			if not current_square.check_wall(direction) and current_square.move_to(direction):
# # 				possible_directions.append(direction)
# #
# # 		if possible_directions:
# # 			# Choose random direction and move
# # 			direction = random.choice(possible_directions)
# # 			self.move_player(direction)
# #
# # 		# Schedule next auto move (after current movement finishes)
# # 		if self.auto_move_active:
# # 			delay = random.randint(100, 700)  # Random delay between moves
# # 			self.auto_move_job = self.root.after(delay, self.auto_move)
# #
# # 	def add_walls(self):
# # 		self.labyrinth.construct_random_walls()
# # 		self.draw()
# #
# # 	def clear_walls(self):
# # 		self.stop_auto_move()  # Stop auto movement when clearing
# # 		rows = self.labyrinth._max_rows
# # 		cols = self.labyrinth._max_columns
# # 		self.labyrinth = Labyrinth(rows, cols)
# # 		self.player_pos = 0  # Reset player position
# # 		self.is_moving = False  # Reset movement flag
# # 		self.draw()
# #
# # 	def run(self):
# # 		self.root.mainloop()
# #
# #
# # # Run the application
# # if __name__ == "__main__":
# # 	app = LabyrinthGUI(rows=8, cols=8)
# # 	app.run()
#
# import tkinter as tk
# from tkinter import ttk
#
#
# class MainMenuApp:
# 	def __init__(self, background_image_path=None):
# 		self.root = tk.Tk()
# 		self.root.title("Main Menu")
# 		self.root.resizable(True, True)
#
#
#
# 		# Store background image path
# 		self.background_image_path = background_image_path
# 		self.background_photo = None
#
# 		# Center the window on screen
# 		self.center_window(self.root, 1200, 800)
#
# 		# Load background image if provided
# 		if self.background_image_path:
# 			self.load_background_image()
#
# 		self.create_main_menu()
#
# 	def center_window(self, window, width, height):
# 		"""Center the window on the screen"""
# 		screen_width = window.winfo_screenwidth()
# 		screen_height = window.winfo_screenheight()
# 		x = (screen_width - width) // 2
# 		y = (screen_height - height) // 2
# 		window.geometry(f"{width}x{height}+{x}+{y}")
#
# 	def load_background_image(self):
# 		"""Load background image using tkinter PhotoImage"""
# 		try:
# 			self.background_photo = tk.PhotoImage(file=self.background_image_path)
# 		except Exception as e:
# 			print(f"Error loading background image: {e}")
# 			self.background_photo = None
#
# 	def create_background_label(self, parent):
# 		"""Create background label with image"""
# 		if self.background_photo:
# 			bg_label = tk.Label(parent, image=self.background_photo)
# 			bg_label.place(x=0, y=0, relwidth=1, relheight=1)
# 			return bg_label
# 		return None
# 		"""Center the window on the screen"""
# 		screen_width = window.winfo_screenwidth()
# 		screen_height = window.winfo_screenheight()
# 		x = (screen_width - width) // 2
# 		y = (screen_height - height) // 2
# 		window.geometry(f"{width}x{height}+{x}+{y}")
#
# 	def create_main_menu(self):
# 		"""Create the main menu window with 3 buttons"""
# 		# Clear the window
# 		for widget in self.root.winfo_children():
# 			widget.destroy()
#
# 		# Add background image
# 		bg_label = self.create_background_label(self.root)
#
# 		# Title label with transparent background
# 		title_label = tk.Label(self.root, text="Main Menu",
# 		                       font=("Arial", 18, "bold"))
# 		title_label.pack(pady=30)
#
#
# 		# Frame to hold buttons with transparent background
# 		button_frame = tk.Frame(self.root,
# 		                        bg=self.root.cget('bg') if not self.background_photo else 'white')
# 		button_frame.pack(expand=True)
#
# 		# Button 1 - Opens name input window
# 		btn1 = tk.Button(button_frame, text="Enter Name",
# 		                 command=self.open_name_window,
# 		                 width=15, height=2, font=("Arial", 12),
# 		                 bg='lightblue', activebackground='lightcyan')
# 		btn1.pack(pady=10)
#
# 		# Button 2 - Placeholder functionality
# 		btn2 = tk.Button(button_frame, text="Option 2",
# 		                 command=self.button2_action,
# 		                 width=15, height=2, font=("Arial", 12),
# 		                 bg='lightgreen', activebackground='lightgray')
# 		btn2.pack(pady=10)
#
# 		# Button 3 - Placeholder functionality
# 		btn3 = tk.Button(button_frame, text="Option 3",
# 		                 command=self.button3_action,
# 		                 width=15, height=2, font=("Arial", 12),
# 		                 bg='lightyellow', activebackground='lightgray')
# 		btn3.pack(pady=10)
#
# 		# Exit button
# 		exit_btn = tk.Button(self.root, text="Exit",
# 		                     command=self.root.quit,
# 		                     font=("Arial", 10),
# 		                     bg='lightcoral', activebackground='lightgray')
# 		exit_btn.pack(side=tk.BOTTOM, pady=20)
#
# 	def open_name_window(self):
# 		"""Open the name input window"""
# 		# Clear the main window
# 		for widget in self.root.winfo_children():
# 			widget.destroy()
#
# 		# Add background image
# 		bg_label = self.create_background_label(self.root)
#
# 		# Title for name input window
# 		title_label = tk.Label(self.root, text="Enter Your Name",
# 		                       font=("Arial", 16, "bold"),
# 		                       bg=self.root.cget('bg') if not self.background_photo else 'white',
# 		                       fg='black')
# 		title_label.pack(pady=30)
#
# 		# Frame for input elements
# 		input_frame = tk.Frame(self.root,
# 		                       bg=self.root.cget('bg') if not self.background_photo else 'white')
# 		input_frame.pack(expand=True)
#
# 		# Name label
# 		name_label = tk.Label(input_frame, text="Name:",
# 		                      font=("Arial", 12),
# 		                      bg=self.root.cget('bg') if not self.background_photo else 'white',
# 		                      fg='black')
# 		name_label.pack(pady=10)
#
# 		# Text entry box
# 		self.name_entry = tk.Entry(input_frame, font=("Arial", 12),
# 		                           width=25)
# 		self.name_entry.pack(pady=10)
# 		self.name_entry.focus()  # Set focus to the text box
#
# 		# Submit button
# 		submit_btn = tk.Button(input_frame, text="Submit",
# 		                       command=self.submit_name,
# 		                       font=("Arial", 12),
# 		                       bg='lightblue', activebackground='lightcyan')
# 		submit_btn.pack(pady=20)
#
# 		# Back to main menu button
# 		back_btn = tk.Button(self.root, text="Back to Main Menu",
# 		                     command=self.create_main_menu,
# 		                     font=("Arial", 10),
# 		                     bg='lightgray', activebackground='gray')
# 		back_btn.pack(side=tk.BOTTOM, pady=20)
#
# 		# Bind Enter key to submit
# 		self.name_entry.bind('<Return>', lambda event: self.submit_name())
#
# 	def submit_name(self):
# 		"""Handle name submission"""
# 		name = self.name_entry.get().strip()
# 		if name:
# 			# Display confirmation message
# 			for widget in self.root.winfo_children():
# 				widget.destroy()
#
# 			# Confirmation message
# 			confirm_label = tk.Label(self.root,
# 			                         text=f"Hello, {name}!\nName submitted successfully.",
# 			                         font=("Arial", 14), justify=tk.CENTER)
# 			confirm_label.pack(expand=True)
#
# 			# Back to main menu button
# 			back_btn = tk.Button(self.root, text="Back to Main Menu",
# 			                     command=self.create_main_menu,
# 			                     font=("Arial", 12))
# 			back_btn.pack(pady=20)
# 		else:
# 			# Show error if name is empty
# 			error_label = tk.Label(self.root, text="Please enter a name!",
# 			                       fg="red", font=("Arial", 10))
# 			error_label.pack()
# 			# Remove error message after 3 seconds
# 			self.root.after(3000, error_label.destroy)
#
# 	def button2_action(self):
# 		"""Placeholder for button 2 functionality"""
# 		print("Button 2 clicked!")
#
# 	# You can add your own functionality here
#
# 	def button3_action(self):
# 		"""Placeholder for button 3 functionality"""
# 		print("Button 3 clicked!")
#
# 	# You can add your own functionality here
#
# 	def run(self):
# 		"""Start the application"""
# 		self.root.mainloop()
#
#
# # Run the application
# if __name__ == "__main__":
# 	# Option 1: No background image
# 	# app = MainMenuApp()
#
# 	# Option 2: With background image (replace with your PNG file path)
# 	app = MainMenuApp("asset/bg_rat.gif")  # Replace "background.png" with your file path
#
# 	app.run()

import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from typing import List, Type, Optional, Union, ClassVar


class BaseWindow(ABC):
	"""Abstract base class for all windows"""
	# Class variables to store extent and current state
	_extent: ClassVar[List[Type['BaseWindow']]] = []
	_current_window: ClassVar[Optional['BaseWindow']] = None
	_current_index: ClassVar[int] = 0
	_root: ClassVar[Optional[tk.Tk]] = None
	_initialized: ClassVar[bool] = False

	def __init__(self, root: tk.Tk) -> None:
		self.root: tk.Tk = root
		# Set the root as class variable if not already set
		if BaseWindow._root is None:
			BaseWindow._root = root
		# Initialize extent with all window classes on first instantiation
		if not BaseWindow._initialized:
			BaseWindow._extent = [MainWindow, SettingsWindow, DataWindow, AboutWindow]
			BaseWindow._initialized = True
		self.setup_window()
		self.create_widgets()

	@abstractmethod
	def setup_window(self) -> None:
		"""Abstract method to set window properties - must be implemented by subclasses"""
		pass

	@abstractmethod
	def create_widgets(self) -> None:
		"""Abstract method to create window widgets - must be implemented by subclasses"""
		pass

	def destroy(self) -> None:
		"""Clean up the window"""
		for widget in self.root.winfo_children():
			widget.destroy()

	@staticmethod
	def switch_to_next_window() -> None:
		"""Static method to switch to the next window in the extent"""
		# Destroy current window
		if BaseWindow._current_window:
			BaseWindow._current_window.destroy()

		# Move to next window in the extent
		BaseWindow._current_index = (BaseWindow._current_index + 1) % len(BaseWindow._extent)

		# Create new window instance
		window_class: Type[BaseWindow] = BaseWindow._extent[BaseWindow._current_index]
		BaseWindow._current_window = window_class(BaseWindow._root)


class MainWindow(BaseWindow):
	# Class variable to keep image reference alive
	_bg_image: ClassVar[Optional[tk.PhotoImage]] = None

	def __init__(self, root: tk.Tk) -> None:
		self.bg_label: tk.Label
		super().__init__(root)

	def setup_window(self) -> None:
		self.root.title("Main Window")
		self.root.geometry("400x300")
		self.root.configure(bg='lightblue')

	def create_widgets(self) -> None:
		# Load and set background image using class variable to prevent garbage collection
		try:
			if MainWindow._bg_image is None:
				MainWindow._bg_image = tk.PhotoImage(file="background.gif")
			self.bg_label = tk.Label(self.root, image=MainWindow._bg_image)
			self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
		except tk.TclError:
			# If image file not found, create a colored background
			self.bg_label = tk.Label(self.root, bg='lightblue')
			self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
			print("Warning: background.gif not found, using solid color background")

		title: tk.Label = tk.Label(self.root, text="Main Window",
		                           font=('Arial', 18, 'bold'),
		                           bg='white', fg='darkblue')
		title.pack(pady=20)

		info: tk.Label = tk.Label(self.root,
		                          text="This is the main application window.\nClick 'Next Window' to switch.",
		                          bg='white', font=('Arial', 12))
		info.pack(pady=10)

		# First button - Next Window (centered vertically, 20px from right)
		switch_btn: tk.Button = tk.Button(self.root, text="Next Window",
		                                  command=BaseWindow.switch_to_next_window,
		                                  font=('Arial', 12),
		                                  bg='white', fg='darkblue',
		                                  activebackground='lightblue',
		                                  activeforeground='darkblue',
		                                  width=15, height=2)
		switch_btn.place(relx=1.0, rely=0.5, x=-20, y=-25, anchor='e')

		# Second button - Exit (positioned under the first one)
		exit_btn: tk.Button = tk.Button(self.root, text="Exit",
		                                command=self.root.quit,
		                                font=('Arial', 12),
		                                bg='white', fg='darkred',
		                                activebackground='lightcoral',
		                                activeforeground='darkred',
		                                width=15, height=2)
		exit_btn.place(relx=1.0, rely=0.5, x=-20, y=25, anchor='e')


class SettingsWindow(BaseWindow):
	def __init__(self, root: tk.Tk) -> None:
		self.option1: tk.BooleanVar
		self.option2: tk.BooleanVar
		super().__init__(root)

	def setup_window(self) -> None:
		self.root.title("Settings Window")
		self.root.geometry("400x300")
		self.root.configure(bg='lightgreen')

	def create_widgets(self) -> None:
		title: tk.Label = tk.Label(self.root, text="Settings Window",
		                           font=('Arial', 18, 'bold'),
		                           bg='lightgreen', fg='darkgreen')
		title.pack(pady=20)

		# Sample settings
		settings_label: tk.Label = tk.Label(self.root, text="Application Settings:",
		                                    bg='lightgreen', font=('Arial', 12, 'bold'))
		settings_label.pack(pady=10)

		# Checkboxes
		self.option1 = tk.BooleanVar()
		self.option2 = tk.BooleanVar()

		checkbox1: tk.Checkbutton = tk.Checkbutton(self.root, text="Enable notifications",
		                                           variable=self.option1, bg='lightgreen',
		                                           font=('Arial', 10))
		checkbox1.pack(pady=5)

		checkbox2: tk.Checkbutton = tk.Checkbutton(self.root, text="Auto-save",
		                                           variable=self.option2, bg='lightgreen',
		                                           font=('Arial', 10))
		checkbox2.pack(pady=5)

		switch_btn: tk.Button = tk.Button(self.root, text="Next Window",
		                                  command=BaseWindow.switch_to_next_window,
		                                  font=('Arial', 12),
		                                  bg='white', fg='darkgreen',
		                                  width=15, height=2)
		switch_btn.pack(pady=30)


class DataWindow(BaseWindow):
	def setup_window(self) -> None:
		self.root.title("Data Window")
		self.root.geometry("400x300")
		self.root.configure(bg='lightyellow')

	def create_widgets(self) -> None:
		title: tk.Label = tk.Label(self.root, text="Data Window",
		                           font=('Arial', 18, 'bold'),
		                           bg='lightyellow', fg='darkorange')
		title.pack(pady=20)

		# Sample data display
		data_label: tk.Label = tk.Label(self.root, text="Sample Data:",
		                                bg='lightyellow', font=('Arial', 12, 'bold'))
		data_label.pack(pady=10)

		# Listbox with sample data
		listbox: tk.Listbox = tk.Listbox(self.root, height=6, width=30)
		listbox.pack(pady=10)

		sample_data: List[str] = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
		for item in sample_data:
			listbox.insert(tk.END, item)

		switch_btn: tk.Button = tk.Button(self.root, text="Next Window",
		                                  command=BaseWindow.switch_to_next_window,
		                                  font=('Arial', 12),
		                                  bg='white', fg='darkorange',
		                                  width=15, height=2)
		switch_btn.pack(pady=20)


class AboutWindow(BaseWindow):
	def setup_window(self) -> None:
		self.root.title("About Window")
		self.root.geometry("400x300")
		self.root.configure(bg='lightcoral')

	def create_widgets(self) -> None:
		title: tk.Label = tk.Label(self.root, text="About Window",
		                           font=('Arial', 18, 'bold'),
		                           bg='lightcoral', fg='darkred')
		title.pack(pady=20)

		info_text: str = """Window Switcher Application
Version 1.0

This application demonstrates switching
between multiple tkinter windows using
a global list and navigation function.

Created with Python & Tkinter"""

		info: tk.Label = tk.Label(self.root, text=info_text,
		                          bg='lightcoral', font=('Arial', 10),
		                          justify='center')
		info.pack(pady=20)

		switch_btn: tk.Button = tk.Button(self.root, text="Back to Main",
		                                  command=BaseWindow.switch_to_next_window,
		                                  font=('Arial', 12),
		                                  bg='white', fg='darkred',
		                                  width=15, height=2)
		switch_btn.pack(pady=20)


def main() -> None:
	# Create main tkinter root
	root: tk.Tk = tk.Tk()
	root.resizable(True, True)

	# Start with the first window (this will populate the extent and set class variables)
	BaseWindow._current_window = MainWindow(root)

	# Handle window close event
	def on_closing() -> None:
		root.quit()
		root.destroy()

	root.protocol("WM_DELETE_WINDOW", on_closing)

	# Start the main loop
	root.mainloop()


if __name__ == "__main__":
	main()