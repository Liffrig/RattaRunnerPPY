from __future__ import annotations

from typing import List, Type, Optional

import tkinter as tk

from model.mouse_blueprint import MouseBlueprint
from view.labyrinth_gui import LabyrinthGUI
from view.mouse_gui import MouseGUI
from windows.base_window import BaseWindow
from windows.main_menu import MainMenu
from windows.mouse_picker import MousePicker





def main() -> None:


    # lg = LabyrinthGUI(6,12)
    # ab = {'smartness':0, "speed":1, "stamina":2}
    # m = MouseGUI(3,ab,lg)
    # lg.draw()
    # lg.root.mainloop()

    root = tk.Tk()
    root.resizable(False, False)
    BaseWindow.window_flow = [MainMenu, MousePicker]
    BaseWindow.current_window = MainMenu(root)
    root.mainloop()








if __name__ == "__main__":
    main()



# minimum minimorum
'''
wybór szczura
generowanie do skutku labiryntu 
algorytm błądzenia - smartness
szybkość - speed
utrzymanie szybkości stamina
mierznie czasu

opis co było użyte
'''


