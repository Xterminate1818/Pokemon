import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class BattleFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.stats = ttk.Label(self, text="stats")
        self.stats.grid(column=0, row=0)

        self.moves_frame = ttk.Frame(self)

        self.moves = list(ttk.Button(self.moves_frame, text=m) for m in range(4))
        for m in range(len(self.moves)):
            self.moves[m].grid(row=1, column=m, ipady=25)

        self.moves_frame.grid(column=0, row=1)

        self.log = ScrolledText(self)
        self.log.grid(column=2, row=0, rowspan=2)


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(True, True)
    b = BattleFrame(root)
    b.pack()
    root.mainloop()

