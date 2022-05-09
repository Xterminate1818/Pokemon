import tkinter as tk
from tkinter import ttk


class MainMenu(ttk.Frame):
	def __init__(self, root):
		super().__init__(root)
		self.battle_button = ttk.Button(self, text="Battle", command=root.switch_battle, takefocus=tk.NO)
		self.battle_button.grid(row=0, column=0, padx=5, pady=5, ipadx=50, ipady=10)

		self.team_button = ttk.Button(self, text="Teams", takefocus=tk.NO)
		self.team_button.grid(row=1, column=0, padx=5, pady=5, ipadx=50, ipady=10)

		self.pokedex_button = ttk.Button(self, text="Pokedex", command=root.switch_pokedex, takefocus=tk.NO)
		self.pokedex_button.grid(row=2, column=0, padx=5, pady=5, ipadx=50, ipady=10)

		self.exit_button = ttk.Button(self, text="Exit", command=root.destroy, takefocus=tk.NO)
		self.exit_button.grid(row=3, column=0, padx=5, pady=5, ipadx=50, ipady=10)


if __name__ == "__main__":
	root = tk.Tk()
	root.resizable(True, True)
	mm = MainMenu(root)
	mm.pack()
	root.mainloop()
