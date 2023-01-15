import tkinter as tk


class ObjectStorage:
    def __init__(self):
        self.name_widgets = dict()
        self.storage = dict()


class Menu:
    def __init__(self, root):
        self.choose_state = "not stated"
        self.menubar = tk.Menu(root)
        self.text_bar = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Add", menu=self.text_bar)
        root.config(menu=self.menubar)
