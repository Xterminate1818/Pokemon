import tkinter as tk
from tkinter import ttk
import database


class SearchBox(tk.Frame):
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


import database


class PokedexSearchBox(SearchBox):
    def __init__(self, root, command=None):
        super().__init__(root, lambda v, k="name": database.search_pokedex(k, v), command=command)

    def update_search(self, *args):
        results = list(i["name"] for i in self.search(self.search_var.get()))
        self.list_box.grid(row=1, column=0)
        if self.search_var.get().strip() == "" or len(results) == 0:
            self.results_var.set("")
            self.list_box.config(height=0)
            self.list_box.grid_forget()
            return
        self.results_var.set(results)
        self.list_box.config(height=min(len(results), 6))


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(True, True)
    b = PokedexSearchBox(root)
    b.pack()
    root.mainloop()
