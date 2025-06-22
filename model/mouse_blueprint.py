from __future__ import annotations
from utils.random_engine import get_k_uniques
from typing import Dict, List


class MouseBlueprint:
	def __init__(self, sm, sp, st, m_id) -> None:
		self.abilities_pref: Dict[str,int] ={
			'smartness' : sm,
			'speed': sp,
			'stamina' : st
		}
		self.model_id: int =m_id

	@classmethod
	def get_blueprints(cls) -> List[MouseBlueprint]:

		result_list: List[MouseBlueprint] = []
		model_id_lst: List[int] = get_k_uniques(10,3)

		for i in model_id_lst:
			result_list.append(
				MouseBlueprint(*get_k_uniques(3,3), i)
			)
		return result_list



