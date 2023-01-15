import application
import logging


def AddModuleText():
    def text_set():
        app.menu.choose_state = "text"

    app = application.Application()
    app.storage.name_widgets["text"] = Text
    app.menu.text_bar.add_command(label="Text", command=text_set)


class Text:
    def __init__(self, event, **kwargs):
        if 'txt' not in kwargs:
            kwargs['txt'] = 'default'
        self.app = application.Application()
        x = self.app.canvas.canvasx(event.x)
        y = self.app.canvas.canvasy(event.y)
        self.text_id = self.app.canvas.create_text(
            x, y,
            tags=("text", "all"),
            text=kwargs['txt'], font=(
                "Helvetica", int(self.app.canvas.fontSize)))
        self.x, self.y = x, y
        self.app.storage.storage[self.text_id] = self
        logging.info(f"text created {self.text_id}, on {self.x}, {self.y}")
        self.app.canvas.tag_bind(self.text_id, "<Button-1>", self.set_focus)
        self.app.canvas.tag_bind(self.text_id, "<B1-Motion>", self.do_move)
        self.app.canvas.tag_bind(self.text_id, "<Double-Button-1>",
                                 self.set_cursor)
        # to edit text
        self.app.canvas.tag_bind(self.text_id, "<Key>", self.do_key)
        self.app.canvas.tag_bind(self.text_id, "<Left>", self.do_left)
        self.app.canvas.tag_bind(self.text_id, "<Right>", self.do_right)
        self.app.canvas.tag_bind(self.text_id, "<BackSpace>", self.do_backspace)
        self.app.canvas.tag_bind(self.text_id, "<Return>", self.do_return)

    def highlight(self):
        # Highlight the given text item
        self.app.canvas.highlight_object = self.text_id
        items = self.app.canvas.find_withtag(f"highlight{self.text_id}")
        if len(items) == 0:
            ids = self.app.canvas.create_rectangle((0, 0, 0, 0), fill="white",
                                                   outline="blue",
                                                   dash=".", tag=(f"highlight{self.text_id}", "highlight"))
            self.app.canvas.lower(ids, self.text_id)
        else:
            ids = items[0]
            self.app.canvas.lower(ids, self.text_id)

        # resize the highlight
        bbox = self.app.canvas.bbox(self.text_id)
        rect_bbox = (bbox[0] - 4, bbox[1] - 4, bbox[2] + 4, bbox[3] + 4)
        self.app.canvas.coords(ids, rect_bbox)

    def set_focus(self, event):
        self.app.canvas.focus("")
        item = self.app.canvas.focus()
        if item:
            x = self.app.canvas.canvasx(event.x)
            y = self.app.canvas.canvasy(event.y)

            self.app.canvas.icursor(self.text_id, "@%d,%d" % (x, y))
            self.app.canvas.select_clear()
        self.app.canvas.delete("highlight")
        self.highlight()

    def set_focus_box(self):
        self.app.canvas.focus("")
        self.highlight()

    def set_cursor(self, _):
        # Give focus to the text element under the cursor double-click
        self.app.canvas.focus("")
        self.app.canvas.focus_set()
        self.app.canvas.focus(self.text_id)
        self.highlight()

    def do_key(self, event):
        # Handle the insertion of characters
        item = self.app.canvas.focus()
        if item and event.char >= " ":
            _ = self.app.canvas.index(self.text_id, "insert")
            selection = self.app.canvas.select_item()
            if selection:
                self.app.canvas.dchars(self.text_id, "sel.first", "sel.last")
            self.app.canvas.insert(self.text_id, "insert", event.char)
            self.highlight()

    def do_left(self, _):
        # Move text cursor one character to the left

        item = self.app.canvas.focus()
        if item:
            new_index = self.app.canvas.index(self.text_id, "insert") - 1
            self.app.canvas.icursor(self.text_id, new_index)
            self.app.canvas.select_clear()

    def do_right(self, _):
        # Move text cursor one character to the right

        item = self.app.canvas.focus()
        if item:
            new_index = self.app.canvas.index(self.text_id, "insert") + 1
            self.app.canvas.icursor(self.text_id, new_index)
            self.app.canvas.select_clear()

    def do_return(self, _):
        # Move text cursor one character to the new line
        # item = self.app.canvas.focus()
        # if item:
        self.app.canvas.icursor(self.text_id, "insert")
        self.app.canvas.insert(self.text_id, "insert", '\n')
        # self.app.canvas.delete(f"highlight{self.text_id}")
        self.highlight()

    def do_backspace(self, _):
        # Handle the backspace key
        item = self.app.canvas.focus()
        if item:
            selection = self.app.canvas.select_item()
            if selection:
                self.app.canvas.dchars(self.text_id, "sel.first", "sel.last")
                self.app.canvas.select_clear()
            else:
                insert = self.app.canvas.index(self.text_id, "insert")
                if insert > 0:
                    self.app.canvas.dchars(self.text_id, insert - 1, insert)
            self.highlight()

    def do_move(self, event):
        self.app.canvas.focus("")
        self.app.canvas.selected_pointers = []
        # if self.app.canvas.highlight_object != self.text_id:
        #     self.highlight()
        x_event = self.app.canvas.canvasx(event.x)
        y_event = self.app.canvas.canvasy(event.y)
        bbox = self.app.canvas.bbox(self.text_id)
        x = self.app.canvas.winfo_x() - (bbox[0] + bbox[2]) // 2 + x_event
        y = self.app.canvas.winfo_y() - (bbox[1] + bbox[3]) // 2 + y_event
        # self.app.canvas.focus(self.text_id)
        self.app.canvas.move(self.text_id, x, y)
        self.app.canvas.move(f"highlight{self.text_id}", x, y)
        self.app.canvas.update()
        self.x = x_event
        self.y = y_event

    def do_move_delta(self, _, delta):
        self.app.canvas.focus("")
        x = self.app.canvas.winfo_x() + delta[0]
        y = self.app.canvas.winfo_y() + delta[1]
        self.app.canvas.move(self.text_id, x, y)
        self.app.canvas.move(f"highlight{self.text_id}", x, y)
        self.app.canvas.update()
        bbox = self.app.canvas.bbox(self.text_id)
        self.x = (bbox[0] + bbox[2]) // 2
        self.y = (bbox[1] + bbox[3]) // 2

    def __repr__(self):
        return f"text#{int(self.x)}#{int(self.y)}#{self.app.canvas.itemcget(self.text_id, 'text')}"
