import tkinter as tk
from tkinter import ttk
import database


class SearchBox(ttk.Frame):
	def __init__(self, root, search, command=None):
		super().__init__(root, takefocus=tk.NO)
		self.command = command

		self.search = search
		self.bind('<Return>', self._on_enter)
		self.results_var = tk.StringVar()
		self.list_box = tk.Listbox(self, listvariable=self.results_var)
		self.list_box.bind('<Return>', self._on_enter)
		self.list_box.bind('<Button-1>', self._on_enter)
		self.list_box.bind('<Tab>', self._on_tab)

		self.search_var: tk.StringVar = tk.StringVar(self)
		self.search_var.trace("w", self.update_search)
		self.entry: ttk.Entry = ttk.Entry(self, textvariable=self.search_var, takefocus=tk.NO)
		self.entry.grid(row=0, column=0)
		self.entry.bind("<Tab>", self._on_tab)

		self.entry.tkraise()
		self.list_box.tkraise()

		self.reset()

	def get(self):
		return self.search_var.get()

	def reset(self):
		self.search_var.set("")
		self.entry.delete(0, tk.END)
		self.update_search()

	def update_search(self, *args):
		results = self.search(self.search_var.get())
		self.list_box.grid(row=1, column=0)
		if self.search_var.get().strip() == "" or len(results) == 0:
			self.results_var.set("")
			self.list_box.config(height=0)
			self.list_box.grid_forget()
			return
		self.results_var.set(results)
		self.list_box.config(height=min(len(results), 6))

	def _on_enter(self, event):
		selection = self.list_box.curselection()
		if len(selection) > 0:
			completion = self.list_box.get(selection)
			self.search_var.set(completion)
			self.update_search()
			if self.command:
				self.command()

	def _on_tab(self, event):
		self.list_box.focus_set()
		selection = self.list_box.curselection()
		if len(selection) == 0 and self.list_box.size() != 0:
			self.list_box.selection_set(0)
		elif self.list_box.size() > 0:
			self.list_box.selection_clear(0, self.list_box.size())
			self.list_box.selection_set((selection[0] + 1) % self.list_box.size())

	def _on_exit(self, event):
		self.list_box.grid_forget()


import database


class PokedexSearchBox(SearchBox):
	def __init__(self, root, command=None):
		super().__init__(root, lambda v, k="name": database.search_pokedex(k, v, get="name"), command=command)

	def update_search(self, *args):
		results = self.search(self.search_var.get())
		self.list_box.grid(row=1, column=0)
		if self.search_var.get().strip() == "" or len(results) == 0:
			self.results_var.set("")
			self.list_box.config(height=0)
			self.list_box.grid_forget()
			return
		self.results_var.set(results)
		self.list_box.config(height=min(len(results), 6))


class TeamTree(ttk.Treeview):
	def __init__(self, root, name=None):
		super().__init__(root)
		# Root node 0
		self.insert("", tk.END, text="Unnamed Team", iid=0, open=False)
		# Pokemon nodes 1-6
		for i in range(6):
			self.insert(0, tk.END, text="", iid=i + 1, open=False)
		# Move nodes 7-30
		for i in range(6):
			for j in range(4):
				self.insert(i + 1, tk.END, text="", iid=(i * 6) + 7 + j, open=False)
		if name is not None:
			self.from_db(name)

	def set_team_name(self, name):
		self.item(0, text=name)

	def get_team_name(self):
		return self.item(0)["text"]

	def set_pokemon_name(self, pkm_id, name):
		if not 0 <= pkm_id <= 5:
			raise IndexError("Pokemon ID must be between 0 and 5")
		self.item(pkm_id + 1, text=name)

	def get_pokemon_name(self, pkm_id):
		if not 0 <= pkm_id <= 5:
			raise IndexError("Pokemon ID must be between 0 and 5")
		return self.item(pkm_id + 1)["text"]

	def set_move_name(self, pkm_id, mv_id, name):
		if not 0 <= pkm_id <= 5:
			raise IndexError("Pokemon ID must be between 0 and 5")
		if not 0 <= mv_id <= 3:
			raise IndexError("Move ID must be between 0 and 3")
		self.item(pkm_id * 6 + 7 + mv_id, text=name)

	def get_move_name(self, pkm_id, mv_id):
		if not 0 <= pkm_id <= 5:
			raise IndexError("Pokemon ID must be between 0 and 5")
		if not 0 <= mv_id <= 3:
			raise IndexError("Move ID must be between 0 and 3")
		return self.item(pkm_id * 6 + 7 + mv_id)["text"]

	def from_db(self, name):
		t = database.TEAMS[name]
		self.set_team_name(name)
		for pkm_index in range(len(t)):
			pkm = t[pkm_index]
			name = pkm["name"]
			self.set_pokemon_name(pkm_index, name)
			moves = pkm["moves"]
			for mv_index in range(len(moves)):
				self.set_move_name(pkm_index, mv_index, moves[mv_index])

	def to_db(self):
		name = self.item(0)["text"]
		info = [
			{
				"name": self.get_pokemon_name(p),
				"moves": [self.get_move_name(p, m) for m in range(4)]
			} for p in range(6)
		]
		database.add_team(name, info)


if __name__ == "__main__":
	root = tk.Tk()
	root.resizable(True, True)
	b = TeamTree(root, name="Starter Team")
	b.to_db()
	b.pack()
	root.mainloop()
