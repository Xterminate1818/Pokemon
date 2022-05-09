import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import database
from ui_searchbox import PokedexSearchBox


class PokedexFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.selected_id = 1

        self.current_image_reference = None
        self.image_label = tk.Label(self, takefocus=tk.NO)
        self.image_label.grid(row=0, column=0)

        self.primary_info_variable = tk.StringVar(self)
        self.primary_info = ttk.Label(self, textvariable=self.primary_info_variable, takefocus=tk.NO)
        self.primary_info.grid(row=1, column=0)

        self.stats_frame = ttk.Frame(self, takefocus=tk.NO)

        self.info_legends = [
            ttk.Label(self.stats_frame, text="HP", width=14, takefocus=tk.NO),
            ttk.Label(self.stats_frame, text="Attack", width=14, takefocus=tk.NO),
            ttk.Label(self.stats_frame, text="Defense", width=14, takefocus=tk.NO),
            ttk.Label(self.stats_frame, text="Special Attack", width=14, takefocus=tk.NO),
            ttk.Label(self.stats_frame, text="Special Defense", width=14, takefocus=tk.NO),
            ttk.Label(self.stats_frame, text="Speed", width=14, takefocus=tk.NO),
            ttk.Label(self.stats_frame, text="Stat Total", width=14, takefocus=tk.NO)
        ]
        self.info_variables = list(tk.StringVar() for _ in range(len(self.info_legends)))
        self.info_labels = []
        for i in range(len(self.info_legends)):
            self.info_labels.append(ttk.Label(self.stats_frame, textvariable=self.info_variables[i], width=12, anchor=tk.E, takefocus=tk.NO))

        for i in range(len(self.info_legends)):
            self.info_legends[i].grid(row=i, column=0)
            self.info_labels[i].grid(row=i, column=1)
        self.stats_frame.grid(row=0, column=1)

        self.back_button = ttk.Button(self, text="Back", command=self._on_back, takefocus=tk.NO)
        self.back_button.grid(row=2, column=0, sticky=tk.N)

        self.next_button = ttk.Button(self, text="Next", command=self._on_next, takefocus=tk.NO)
        self.next_button.grid(row=2, column=1, sticky=tk.N)

        self.search_label = ttk.Label(self, text="Search:", takefocus=tk.NO)
        self.search_label.grid(row=2, column=2, sticky=tk.N)

        self.search_box = PokedexSearchBox(self, command=self._on_search)
        self.search_box.grid(row=2, column=3, sticky=tk.N)

        self.return_button = ttk.Button(self, text="Return to Menu", command=self.back_out, takefocus=tk.NO)
        self.return_button.grid(row=0, column=3, sticky=tk.N)
        self.return_func = root.switch_mainmenu

        self.select_pokemon()

    def back_out(self):
        self.selected_id = 1
        self.select_pokemon()
        self.search_box.reset()
        self.return_func()

    def select_pokemon(self):
        self.change_image()
        dex = database.search_pokedex("id", self.selected_id)[0]
        iv = self.info_variables
        self.primary_info_variable.set("#" + str(dex["id"]).rjust(3, '0') + " - " + dex["name"])
        iv[0].set(dex["hp"])
        iv[1].set(dex["attack"])
        iv[2].set(dex["defense"])
        iv[3].set(dex["sp-attack"])
        iv[4].set(dex["sp-defense"])
        iv[5].set(dex["speed"])
        iv[6].set(dex["total"])

    def change_image(self):
        image = Image.open("./images/" + str(self.selected_id) + ".png")
        resize_image = image.resize((150, 150))
        img = ImageTk.PhotoImage(resize_image)
        self.current_image_reference = img
        self.image_label.config(image=img)

    def _on_next(self):
        self.selected_id = min(151, self.selected_id + 1)
        self.select_pokemon()

    def _on_back(self):
        self.selected_id = max(1, self.selected_id - 1)
        self.select_pokemon()

    def _on_search(self, *args):
        results = database.search_pokedex("name", self.search_box.get())
        if len(results) > 0:
            self.selected_id = results[0]["id"]
            self.select_pokemon()


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(True, True)
    b = PokedexFrame(root)
    b.pack()
    root.mainloop()
