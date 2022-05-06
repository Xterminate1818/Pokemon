import tkinter as tk
from tkinter import ttk
import database


class TeamsFrame(ttk.Frame):
	def __init__(self, root):
		super().__init__(root)
		self.selected_member: int = 0
		self.members: list[str] = ["NONE"] * 6
		# Team member selection
		self.team_frame: ttk.Frame = ttk.Frame(self)
		self.pkm_buttons: list[ttk.Button] = []
		for i in range(6):
			self.pkm_buttons.append(ttk.Button(
				self.team_frame,
				text="NONE",
				width=12,
				command=(lambda j=i: self.select_member(j)
				         )))
			self.pkm_buttons[i].grid(column=i, row=0)
		self.team_frame.grid(row=0, column=0, columnspan=2)
		self.name_var: tk.StringVar = tk.StringVar(self)
		self.name: ttk.Label = ttk.Label(self, textvariable=self.name_var)
		self.name.grid(row=1, column=0)
		self.moves = list[ttk.Combobox] = []

		self.selection: ttk.Entry = ttk.Entry(self)
		self.selection.grid(row=2, column=0, columnspan=2)
		self.selection_button: ttk.Button = ttk.Button(self, text="Select Pokemon", command=self.select_pokemon)
		self.selection_button.grid(row=2, column=1)

	def select_member(self, num: int):
		print(num)

	def select_pokemon(self):
		str = self.selection.get()
		results = database.search_pokedex_name(str.lower())
		if len(results) > 0:
			self.name_var.set(results[0])


if __name__ == "__main__":
	root = tk.Tk()
	root.resizable(True, True)
	b = TeamsFrame(root)
	b.pack()
	root.mainloop()
