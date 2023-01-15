import tkinter as tk
from tkinter import Tk
import random


# fontSize = 10

class Layout(tk.Frame):

    def __init__(self, root):
        tk.Frame.__init__(self, root)  # [![enter image description here][1]][1]
        self.canvas = tk.Canvas(self, width=200, height=750, background="white")
        self.xsb = tk.Scrollbar(self, orient="horizontal",
                                command=self.canvas.xview)
        self.ysb = tk.Scrollbar(self, orient="vertical",
                                command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set,
                              xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0, 0, 1000, 1000))

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas.fontSize = 10
        # self.canvas.create_text(50,10, text="Click and drag to move the canvas\nScroll to zoom.")

        # This is what enables using the mouse:
        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)
        # linux scroll
        self.canvas.bind("<Button-4>", self.zoomerP)
        self.canvas.bind("<Button-5>", self.zoomerM)
        # windows scroll
        self.canvas.bind("<MouseWheel>", self.zoomer)

    # move
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    # windows zoom
    def zoomer(self, event):
        if (event.delta > 0):
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
            self.canvas.fontSize = self.canvas.fontSize * 1.1
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
            self.canvas.fontSize = self.canvas.fontSize * 0.9
        for child_widget in self.canvas.find_withtag("text"):
            self.canvas.itemconfigure(child_widget, font=(
                "Helvetica", int(self.canvas.fontSize)))
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # linux zoom
    def zoomerP(self, event):
        self.canvas.fontSize = self.canvas.fontSize * 1.1
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        for child_widget in self.canvas.find_withtag("text"):
            self.canvas.itemconfigure(child_widget, font=(
                "Helvetica", int(self.canvas.fontSize)))
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoomerM(self, event):
        self.canvas.fontSize = self.canvas.fontSize * 0.9
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        for child_widget in self.canvas.find_withtag("text"):
            self.canvas.itemconfigure(child_widget, font=(
                "Helvetica", int(self.canvas.fontSize)))
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


root = Tk()
root.title("Seoul Cell")
root.geometry("1300x1000")
root.resizable(True, True)

if __name__ == "__main__":
    global monitor1
    monitor1 = Layout(root)
    monitor1.pack(fill="both", expand=True)

for i in range(10):
    x1 = random.randrange(0, 1000)
    x2 = random.randrange(0, 1000)
    y1 = random.randrange(0, 1000)
    y2 = random.randrange(0, 1000)
    monitor1.canvas.create_rectangle(x1, x2, y1, y2, fill="black",
                                     stipple="gray50")
    monitor1.canvas.create_text(x1, y1, text="random word!",
                                font=("Helvetica", 10), tags="text")
root.mainloop()
