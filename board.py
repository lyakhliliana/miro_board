import tkinter as tk
import application


class Canvas(tk.Canvas):
    def __init__(self, root, *args, **kwargs):
        super(Canvas, self).__init__(root, *args, **kwargs)
        self.root = root
        self.fontSize = 10
        self.pack(fill='both', expand=True)
        self.selected_box = None
        self.x_select_start = 0
        self.y_select_start = 0
        self.highlight_object = 0
        self.selected_pointers = []

    def bind_canvas(self):
        canvas_methods = CanvasMethods()
        self.bind('<Button-1>', canvas_methods.one_click)
        self.bind("<MouseWheel>", canvas_methods.zoomer)

        self.bind("<Button-3>", canvas_methods.move_start)
        self.bind("<Button-3>", canvas_methods.unbound, add="+")
        self.bind("<B3-Motion>", canvas_methods.move_move)

        self.bind("<ButtonPress-1>", canvas_methods.select_start, add='+')
        self.bind("<B1-Motion>", canvas_methods.select_motion)
        self.bind("<B1-Motion>", canvas_methods.select_move, add='+')
        self.bind("<ButtonRelease-1>", canvas_methods.select_release)


class CanvasMethods:
    def __init__(self):
        self.app = application.Application()

    def one_click(self, event):
        if self.app.menu.choose_state == "not stated":
            self.app.canvas.x_select_start = self.app.canvas.canvasx(event.x)
            self.app.canvas.y_select_start = self.app.canvas.canvasy(event.y)
            return
        else:
            self.app.storage.name_widgets[self.app.menu.choose_state](event)
            self.app.menu.choose_state = "not stated"

    def move_start(self, event):
        self.app.canvas.focus("")
        self.app.canvas.delete("highlight")
        self.app.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.app.canvas.scan_dragto(event.x, event.y, gain=1)

    def zoomer(self, event):
        x = self.app.canvas.canvasx(event.x)
        y = self.app.canvas.canvasy(event.y)
        if event.delta > 0:
            self.app.canvas.scale("all", x, y, 1.1, 1.1)
            self.app.canvas.fontSize = self.app.canvas.fontSize * 1.1
        elif event.delta < 0:
            self.app.canvas.scale("all", x, y, 0.9, 0.9)
            self.app.canvas.fontSize = self.app.canvas.fontSize * 0.9
        for child_widget in self.app.canvas.find_withtag("text"):
            self.app.canvas.itemconfigure(child_widget,
                                          font=("Helvetica",
                                                int(self.app.canvas.fontSize)))

    def select_start(self, event):
        origin_x = self.app.canvas.canvasx(event.x)
        origin_y = self.app.canvas.canvasy(event.y)
        focused = self.app.canvas.find_overlapping(origin_x, origin_y, origin_x, origin_y)
        # print(focused)
        if self.app.canvas.selected_pointers:
            return
        if focused:
            return
        self.app.canvas.selected_box = self.app.canvas.create_rectangle(origin_x, origin_y, origin_x, origin_y)
        self.app.canvas.x_select_start = origin_x
        self.app.canvas.y_select_start = origin_y

    # binding for drag select
    def select_motion(self, event):
        if not self.app.canvas.selected_box:
            return
        x_new = self.app.canvas.canvasx(event.x)
        y_new = self.app.canvas.canvasy(event.y)
        x = self.app.canvas.x_select_start
        y = self.app.canvas.y_select_start
        if x_new < x and y_new < y:
            self.app.canvas.coords(self.app.canvas.selected_box, x_new, y_new, x, y)
        elif x_new < x:
            self.app.canvas.coords(self.app.canvas.selected_box, x_new, y, x, y_new)
        elif y_new < y:
            self.app.canvas.coords(self.app.canvas.selected_box, x, y_new, x_new, y)
        else:
            self.app.canvas.coords(self.app.canvas.selected_box, x, y, x_new, y_new)

    # binding for drag select
    def select_release(self, _):
        if self.app.canvas.selected_pointers:
            self.app.canvas.selected_pointers = []
            return

        if not self.app.canvas.selected_box:
            return
        x1, y1, x2, y2 = self.app.canvas.coords(self.app.canvas.selected_box)
        self.app.canvas.delete(self.app.canvas.selected_box)
        # find all objects within select box
        self.app.canvas.selected_pointers = []
        self.app.canvas.delete("highlight")
        self.app.canvas.focus("")
        for i in self.app.canvas.find_enclosed(x1, y1, x2, y2):
            # self.app.canvas.focus(i)
            if i in self.app.storage.storage:
                self.app.canvas.selected_pointers.append(i)
                self.app.storage.storage[i].set_focus_box()
        self.app.canvas.selected_box = None

    def unbound(self, _):
        self.app.canvas.selected_pointers = []

    def select_move(self, event):
        if not self.app.canvas.selected_pointers:
            return
        delta = [0] * 2
        delta[0] = (self.app.canvas.canvasx(event.x) - self.app.canvas.x_select_start)
        delta[1] = (self.app.canvas.canvasy(event.y) - self.app.canvas.y_select_start)
        for id_ in self.app.canvas.selected_pointers:
            self.app.storage.storage[id_].do_move_delta(event, delta)
        self.app.canvas.x_select_start = self.app.canvas.canvasx(event.x)
        self.app.canvas.y_select_start = self.app.canvas.canvasy(event.y)
