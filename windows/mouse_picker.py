import random
import tkinter as tk

from utils.random_engine import roll_dice, get_k_uniques
from windows.base_window import BaseWindow
from utils.misc_utils import BUTTON_DESIGN, BASE_SETTINGS, LABEL_DESIGN
from model.mouse_blueprint import MouseBlueprint
from typing import ClassVar, Optional, Dict, Any, List


class MousePicker(BaseWindow):
	_bg_image: ClassVar[Optional[tk.PhotoImage]] = None

	def __init__(self, root: tk.Tk) -> None:
		self.bg_label: tk.Label
		self.images: list[tk.PhotoImage] = []
		self.selected_mice: list[str] = []
		self.radio_vars: list[tk.StringVar] = []
		self.user_selection: Dict[str, Any] = {}

		self.blueprints: List[MouseBlueprint] = MouseBlueprint.get_blueprints()
		self.image_paths = [
			f"asset/mouse{x.model_id}.png" for x in self.blueprints
		]


		super().__init__(root)

	def setup_window(self) -> None:
		self.root.title("RattaRunnerPPY")
		self.root.geometry("1200x800")

	def create_widgets(self) -> None:
		# Background
		if MousePicker._bg_image is None:
			MousePicker._bg_image = tk.PhotoImage(file="asset/bg_all.gif")
		self.bg_label = tk.Label(self.root, image=self._bg_image)
		self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

		# Create main frame for content
		main_frame = tk.Frame(self.root, bg='white', relief='sunken')
		main_frame.place(relx=0.5, rely=0.4, anchor='center', width=800, height=400)


		blueprints: List[MouseBlueprint] = MouseBlueprint.get_blueprints()
		# Load images (replace with your actual image paths)



		# Calculate target image size
		image_size: int = int(BASE_SETTINGS['cell_size'] * BASE_SETTINGS["image_size"])

		for path in self.image_paths:
			img = tk.PhotoImage(file=path)
			# Resize the loaded image
			img = img.subsample(
				max(1, img.width() // image_size),
				max(1, img.height() // image_size)
			)
			self.images.append(img)


		mouse_stats = [bp.abilities_pref for bp in self.blueprints]

		self.selected_mice = []
		self.radio_vars = []

		# Create image columns
		for col in range(3):
			mouse_name = f"Mouse {col + 1}"

			# Create radio button variable for this mouse
			radio_var = tk.StringVar(value="")
			self.radio_vars.append(radio_var)

			# Radio button above image
			radio_button = tk.Radiobutton(
				main_frame,
				text=mouse_name,
				variable=radio_var,
				value=mouse_name,
				**LABEL_DESIGN,
				command=lambda idx=col: self.handle_selection(idx)
			)
			radio_button.place(x=50 + col * 280, y=10, width=150, height=30)

			# Image
			img_label = tk.Label(main_frame, image=self.images[col], bg='white')
			img_label.place(x=50 + col * 280, y=50, width=image_size, height=image_size)

			# Stats labels under each image
			stats_y_start = 210
			for i, (stat_name, stat_value) in enumerate(mouse_stats[col].items()):
				stat_label = tk.Label(
					main_frame,
					text=f"{stat_name}: {stat_value}",
					**LABEL_DESIGN,
					anchor='center'
				)
				stat_label.place(x=50 + col * 280, y=stats_y_start + i * 25, width=150, height=20)

		# Instructions
		instruction_label = tk.Label(
			main_frame,
			text="Select exactly 2 mice using the radio buttons above",
			**LABEL_DESIGN,
			fg='navy'
		)
		instruction_label.place(relx=0.5, y=320, anchor='center')

		# Exit button (modified to save selection)
		exit_button: tk.Button = tk.Button(
			self.root,
			text="Exit",
			command=self.save_and_exit,
			**BUTTON_DESIGN,
			width=10,
			height=2
		)
		exit_button.place(relx=1.0, rely=0.9, x=-20, anchor='e')

	def handle_selection(self, mouse_index: int) -> None:
		"""Handle mouse selection with limit of 2 selections"""
		mouse_name = f"Mouse {mouse_index + 1}"

		if mouse_name in self.selected_mice:
			# Already selected, remove it
			self.selected_mice.remove(mouse_name)
			self.radio_vars[mouse_index].set("")
		else:
			# Not selected, try to add it
			if len(self.selected_mice) < 2:
				self.selected_mice.append(mouse_name)
				self.radio_vars[mouse_index].set(mouse_name)
			else:
				# Already have 2 selections, need to replace oldest
				# Remove the first selected mouse
				oldest_mouse = self.selected_mice.pop(0)
				oldest_index = int(oldest_mouse.split()[1]) - 1
				self.radio_vars[oldest_index].set("")

				# Add the new selection
				self.selected_mice.append(mouse_name)
				self.radio_vars[mouse_index].set(mouse_name)

		# Exit button (modified to save selection)
		exit_button: tk.Button = tk.Button(
			self.root,
			text="Exit",
			command=self.save_and_exit,
			**BUTTON_DESIGN,
			width=10,
			height=2
		)
		exit_button.place(relx=1.0, rely=0.9, x=-20, anchor='e')

	def save_and_exit(self) -> None:
		"""Save user selection to dictionary and exit"""
		self.user_selection = {
			'selected_mice': self.selected_mice.copy(),
			'total_selected': len(self.selected_mice),
			'timestamp': 'current_time'  # You can import datetime if needed
		}

		# Print selection for debugging (remove in production)
		print("User Selection:", self.user_selection)

		# You can add additional logic here before exiting
		# For example, save to file, send to database, etc.

		self.root.quit()