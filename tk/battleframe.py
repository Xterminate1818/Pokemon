import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

class BattleFrame:
    def __init__(self, root):
        super().__init__(root)

        self.log = ScrolledText(self)
