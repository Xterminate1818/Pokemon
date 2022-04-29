import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.resizable(True, True)

# place a label on the root window
message = tk.Label(root, text="Hello, World!")
message.pack()

# keep the window displaying
root.mainloop()
