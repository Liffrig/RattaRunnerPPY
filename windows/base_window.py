
import tkinter as tk
from abc import ABC, abstractmethod
from typing import List, Type, Optional, ClassVar





class BaseWindow(ABC):
	window_flow: ClassVar[List[Type['BaseWindow']]] = []
	current_window: ClassVar[Optional['BaseWindow']] = None
	current_index: ClassVar[int] = 0
	_root: ClassVar[Optional[tk.Tk]] = None

	def __init__(self, root: tk.Tk) -> None:
		self.root: tk.Tk = root
		# Set the root as class variable if not already set
		if BaseWindow._root is None:
			BaseWindow._root = root

		if type(self) not in BaseWindow.window_flow:
			BaseWindow.window_flow.append(type(self))
		self.setup_window()
		self.create_widgets()

	@abstractmethod
	def setup_window(self) -> None:
		pass

	@abstractmethod
	def create_widgets(self) -> None:
		pass

	def destroy(self) -> None:
		for widget in self.root.winfo_children():
			widget.destroy()

	@staticmethod
	def switch_to_next_window() -> None:
		"""Static method to switch to the next window in the extent"""
		# Destroy the current window
		if BaseWindow.current_window:
			BaseWindow.current_window.destroy()

		# Move to the next window in the extent
		BaseWindow.current_index = (BaseWindow.current_index + 1) % len(BaseWindow.window_flow)

		# Create a new window instance
		window_class: Type[BaseWindow] = BaseWindow.window_flow[BaseWindow.current_index]
		BaseWindow.current_window = window_class(BaseWindow._root)
