from tkinter import PhotoImage

from model.mouse import Mouse
from typing import Dict, List, Optional, TYPE_CHECKING
from utils.misc_utils import BASE_SETTINGS
from model.square import Square
from view.labyrinth_gui import LabyrinthGUI
from utils.random_engine import roll_dice, choose_stats
from utils.misc_utils import BASE_SETTINGS

if TYPE_CHECKING:
	from view.labyrinth_gui import LabyrinthGUI



class MouseGUI(Mouse):

	def __init__(self, appearance_id: int , abilities_pref: Dict[str,int], labyrinth: "LabyrinthGUI") -> None:
		super().__init__(appearance_id , abilities_pref)
		self.mouse_image = PhotoImage(file=self.model_path)

		image_size: int = BASE_SETTINGS["image_size"]


		image_size:int = int(BASE_SETTINGS['cell_size'] * BASE_SETTINGS["image_size"])
		self.mouse_image = self.mouse_image.subsample(
			max(1, self.mouse_image.width() // image_size),
			max(1, self.mouse_image.height() // image_size)
		)

		self.link(labyrinth)
