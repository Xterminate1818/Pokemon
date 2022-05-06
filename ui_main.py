import tkinter as tk
import ui_mainmenu
import ui_battle
import ui_pokedex


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pokemon Battle Simulator")
        self.resizable(True, True)

        # Frames
        self.main_menu = ui_mainmenu.MainMenu(self)
        self.main_menu.grid(row=0, column=0, sticky=tk.NSEW)
        self.battle_menu = ui_battle.BattleFrame(self)
        self.battle_menu.grid(row=0, column=0, sticky=tk.NSEW)
        self.pokedex_menu = ui_pokedex.PokedexFrame(self)
        self.pokedex_menu.grid(row=0, column=0, sticky=tk.NSEW)

        self.switch_mainmenu()

    def switch_mainmenu(self):
        self.main_menu.tkraise()

    def switch_battle(self):
        self.battle_menu.tkraise()

    def switch_pokedex(self):
        self.pokedex_menu.tkraise()


if __name__ == "__main__":
    a = App()
    a.mainloop()
