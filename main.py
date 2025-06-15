from __future__ import annotations

import itertools
from time import sleep

from model.direction import Direction
from model.labyrinth import Labyrinth
from model.mouse import Mouse
from utils.random_engine import labyrinth_architect, random_direction_generator
from view.labyrinth_gui import LabyrinthGUI
from view.mouse_gui import MouseGUI

def main() -> None:


    lg = LabyrinthGUI(8,8)
    lg._construct_random_walls()

    ab = {'smartness':0, "speed":1, "stamina":2}
    m = MouseGUI(3,ab,lg)
    lg.draw()
    lg.root.mainloop()








if __name__ == "__main__":
    main()












# TODO
# zrobić refaktor labirynt_view
# Zrobić klasę playera i zapodać mu parametry gry
# wylosować możliwe ścieżki na podstawie skilla
# mierzyć czas myszy
# porównać 2
# update skill myszki
# zapisz w json????
#profit
