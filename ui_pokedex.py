import tkinter as tk
from tkinter import ttk
import database


class PokedexFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.selected_id = 1

        self.info_frame = ttk.Frame(self)
        self.info_legends = [
            ttk.Label(self.info_frame, text="ID", width=12),
            ttk.Label(self.info_frame, text="Name", width=12),
            ttk.Label(self.info_frame, text="Stat Total", width=12),
            ttk.Label(self.info_frame, text="HP", width=12),
            ttk.Label(self.info_frame, text="Attack", width=12),
            ttk.Label(self.info_frame, text="Defense", width=12),
            ttk.Label(self.info_frame, text="Special Attack", width=12),
            ttk.Label(self.info_frame, text="Special Defense", width=12),
            ttk.Label(self.info_frame, text="Speed", width=12)
        ]
        self.info_variables = list(tk.StringVar() for _ in range(9))
        self.info_labels = []
        for i in range(9):
            self.info_labels.append(ttk.Label(self.info_frame, textvariable=self.info_variables[i], width=10, anchor=tk.E))

        for i in range(9):
            self.info_legends[i].grid(row=i, column=0)
            self.info_labels[i].grid(row=i, column=1)
        self.info_frame.grid(row=0, column=0, columnspan=2)

        self.back_button = ttk.Button(self, text="Back", command=self._on_back)
        self.back_button.grid(row=1, column=0)

        self.next_button = ttk.Button(self, text="Next", command=self._on_next)
        self.next_button.grid(row=1, column=1)

        self.search_box = ttk.Entry(self)
        self.search_box.grid(row=2, column=0)

        self.search_button = ttk.Button(self, text="Search", command=self._on_search)
        self.search_button.grid(row=2, column=1)

        self.select_pokemon()

    def select_pokemon(self):
        name = database.get_pokedex_id(self.selected_id)
        dex = database.POKEDEX[name]
        iv = self.info_variables
        iv[0].set(dex["id"])
        iv[1].set(name)
        iv[2].set(dex["total"])
        iv[3].set(dex["hp"])
        iv[4].set(dex["attack"])
        iv[5].set(dex["defense"])
        iv[6].set(dex["sp-attack"])
        iv[7].set(dex["sp-defense"])
        iv[8].set(dex["speed"])

    def _on_next(self):
        self.selected_id = min(151, self.selected_id + 1)
        self.select_pokemon()

    def _on_back(self):
        self.selected_id = max(1, self.selected_id - 1)
        self.select_pokemon()

    def _on_search(self):
        str = self.search_box.get()
        results = database.search_pokedex_name(str.lower())
        if len(results) > 0:
            self.selected_id = database.POKEDEX[results[0]]["id"]
            self.select_pokemon()


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(True, True)
    b = PokedexFrame(root)
    b.pack()
    root.mainloop()
