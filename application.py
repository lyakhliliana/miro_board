import os
import tkinter as tk
from tkinter import filedialog as fd
import board
import object_storage
import text
import logging


class AppSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(AppSingleton, cls).__call__(*args,
                                                                    **kwargs)
        return cls._instances[cls]


class Application(metaclass=AppSingleton):
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(True, True)
        self.root.geometry("1000x700")
        self.canvas = board.Canvas(self.root, bg='lightgrey')
        self.storage = object_storage.ObjectStorage()
        self.menu = object_storage.Menu(self.root)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w+",
                            format="%(asctime)s %(levelname)s %(message)s")

    def set_bind(self):
        self.canvas.bind_canvas()

    @staticmethod
    def add_modules():
        text.AddModuleText()

    def on_closing(self):
        file = 'previous_session.txt'
        with open(file, 'w+', encoding='utf8') as f:
            for obj in self.storage.storage.values():
                f.write(f'{obj.__repr__()}\n')
        self.root.destroy()

    def open_file(self):
        # file = fd.askopenfilename(filetypes=[("txt file", ".txt")],
        #                           defaultextension=".txt")
        file = 'previous_session.txt'
        if not os.path.isfile(file):
            return
        with open(file, 'r', encoding='utf8') as f:
            for line in f:
                args = line.split('#')
                event = type('event', (object,), {'x': int(args[1]),
                                                  'y': int(args[2])})()
                self.storage.name_widgets[args[0]](event, txt=args[3].rstrip())
