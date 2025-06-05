from typing import Dict, List, Optional, TYPE_CHECKING



from utils.random_engine import roll_dice, choose_stats
from utils.misc_utils import BASE_SETTINGS

if TYPE_CHECKING:
    from model.square import Square
    from model.labyrinth import Labyrinth



class Mouse:
	def __init__(self, appearance_id: int , abilities_pref: Dict[str,int]) -> None:

		self.model_path: str =  f"asset/mouse{appearance_id}.png"

		stat_pool = self._roll_stat_pool()

		self._smartness = stat_pool[abilities_pref['smartness']]
		self._speed = stat_pool[abilities_pref['speed']]
		self._stamina = stat_pool[abilities_pref['stamina']]

		self.square_on: Optional[Square] = None


	def _roll_stat_pool(self) -> List[float]:
		roll_results: List[float] = []

		for mult in range(3):
			lower = (BASE_SETTINGS['abilities_base_mult'] * mult) + 1
			upper = min(BASE_SETTINGS['abilities_base_mult'] * (mult+1), 80)

			roll_results.extend([roll_dice(upper,lower)/100 for x in range(10)])

		roll_results = roll_results[9:12] + roll_results[15:18] + roll_results[20:23]
		return choose_stats(sorted(roll_results))


	def link(self, labyrinth: "Labyrinth") -> None:
		if self.square_on is None:
			self.square_on = labyrinth.start
			labyrinth.link(self)


	@property
	def smartness(self) -> float:
		return self._smartness
	@property
	def speed(self) -> float:
		return self._speed
	@property
	def stamina(self) -> float:
		return self._stamina
