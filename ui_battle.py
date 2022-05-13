import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class TeamFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root, takefocus=tk.NO)
        self.image = ttk.Label(self, text="image")
        self.name = ttk.Label(self, text="Pokemon")
        self.health = ttk.Progressbar(self)
        self.switch_frame = ttk.Frame(self)
        self.switch_buttons = [ttk.Button(self.switch_frame) for i in range(6)]
        self.moves_frame = ttk.Frame(self)
        self.move_buttons = [ttk.Button(self.moves_frame) for i in range(4)]

        self.image.grid(row=0, column=1)
        self.name.grid(row=1, column=1)
        self.health.grid(row=2, column=1)
        self.switch_frame.grid(row=0, column=0, rowspan=5)
        for i in range(6):
            self.switch_buttons[i].grid(row=i, column=0)
        self.moves_frame.grid(row=3, column=1, rowspan=2)
        self.move_buttons[0].grid(row=0, column=0)
        self.move_buttons[1].grid(row=0, column=1)
        self.move_buttons[2].grid(row=1, column=0)
        self.move_buttons[3].grid(row=1, column=1)


class BattleFrame(ttk.Frame):
    # States enum (not really)
    WAIT_TEAM1 = 0
    WAIT_TEAM2 = 1
    DISPLAY_MSG = 2
    WIN_STATE = 3
    PICK_TEAMS = 4

    def __init__(self, root):
        super().__init__(root, takefocus=tk.NO)
        self.team1 = TeamFrame(self)
        self.team1.grid(column=0, row=0)
        self.team2 = TeamFrame(self)
        self.team2.grid(column=2, row=0)
        self.state = self.WAIT_TEAM1

    def

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(True, True)
    b = BattleFrame(root)
    b.pack()
    root.mainloop()
