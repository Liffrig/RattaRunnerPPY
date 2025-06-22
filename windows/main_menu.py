import tkinter as tk
from windows.base_window import BaseWindow
from utils.misc_utils import BUTTON_DESIGN
from typing import ClassVar, Optional, TYPE_CHECKING


class MainMenu(BaseWindow):

	_bg_image: ClassVar[Optional[tk.PhotoImage]] = None

	def __init__(self, root: tk.Tk) -> None:
		self.bg_label: tk.Label
		super().__init__(root)





	def setup_window(self) -> None:
		self.root.title("RattaRunnerPPY")
		self.root.geometry("1200x800")







	def create_widgets(self) -> None:
		if MainMenu._bg_image is None:
			MainMenu._bg_image = tk.PhotoImage(file="asset/bg_rat.gif")
		self.bg_label = tk.Label(self.root, image=self._bg_image)
		self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)



		ngame_button: tk.Button = tk.Button(self.root, text="New Game",
		                                    **BUTTON_DESIGN,
		                                  command=BaseWindow.switch_to_next_window,

		                                  width=10, height=2)
		ngame_button.place(relx=1.0, rely=0.5, x=-20, y=-35, anchor='e')

		exit_button: tk.Button = tk.Button(self.root, text="Exit",
		                                   command=self.root.quit,
		                                   **BUTTON_DESIGN,
		                                   width=10, height=2)
		exit_button.place(relx=1.0, rely=0.5, x=-20, y=35, anchor='e')

