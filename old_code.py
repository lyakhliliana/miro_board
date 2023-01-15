import tkinter as tk
from enum import Enum
from abc import ABC


class State(Enum):
    NotStated = 1
    Text = 2


class Menu:
    def __init__(self, root, board):
        self.menubar = tk.Menu(root)
        self.text_bar = tk.Menu(self.menubar, tearoff=0)
        self.text_bar.add_command(label="Text", command=board.text_set)
        self.menubar.add_cascade(label="Add", menu=self.text_bar)
        root.config(menu=self.menubar)


class Board:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, bg='lightgrey')
        self.canvas.pack(fill='both', expand=True)
        self.state = State.NotStated
        self.objects = []
        # self.text = tk.Text(root, width=5, height=5)
        self.canvas.bind('<Button-1>',
                         lambda event: self.create_widget(event))
        self.canvas.tag_bind("text", "<Double-Button-1>",
                             lambda event: Text.set_focus(event, self))
        self.canvas.tag_bind("text", "<Key>",
                             lambda event: Text.do_key(event, self))
        self.canvas.tag_bind("text", "<Home>",
                             lambda event: Text.do_home(event, self))
        self.canvas.tag_bind("text", "<End>",
                             lambda event: Text.do_end(event, self))
        self.canvas.tag_bind("text", "<Left>",
                             lambda event: Text.do_left(event, self))
        self.canvas.tag_bind("text", "<Right>",
                             lambda event: Text.do_right(event, self))
        self.canvas.tag_bind("text", "<BackSpace>",
                             lambda event: Text.do_backspace(event, self))
        self.canvas.tag_bind("text", "<Return>",
                             lambda event: Text.do_return(event, self))
        self.canvas.tag_bind("text", "<Shift-Return>",
                             lambda event: Text.do_new_line(self))
        self.canvas.tag_bind("text", "<B1-Motion>",
                             lambda event: Text.do_move(event, self))
        self.canvas.tag_bind("text", "<Button-1>",
                             lambda event: Text.set_cursor(event, self))
        self.canvas.pack()

    def create_widget(self, event):
        if self.state == State.NotStated:
            pass
        elif self.state == State.Text:
            self.state = State.NotStated
            self.objects.append(Text(self, event))

    def text_set(self):
        self.state = State.Text


class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.board = Board(self.root)
        self.menu = Menu(self.root, self.board)
        self.root.mainloop()


class Widget(ABC):
    def __init__(self):
        super().__init__()

    # @abstractmethod
    # def mouse_one_click_select(self):
    #     pass
    #
    # @abstractmethod
    # def mouse_double_click_edit(self):
    #     pass
    #
    # @abstractmethod
    # def mouse_one_click_motion(self):
    #     pass


class Text(Widget):
    # def mouse_one_click_select(self):
    #     pass
    #
    # def mouse_double_click_edit(self):
    #     pass
    #
    # def mouse_one_click_motion(self):
    #     pass

    def __init__(self, board, event):
        super().__init__()
        self.text_id = board.canvas.create_text(event.x, event.y,
                                                tags=("text",),
                                                text='default')
        self.x, self.y = event.x, event.y

    @staticmethod
    def do_return(_, board):
        # Handle the return key by turning off editing

        board.canvas.focus("")
        board.canvas.delete("highlight")
        board.canvas.select_clear()

    @staticmethod
    def do_left(_, board):
        # Move text cursor one character to the left

        item = board.canvas.focus()
        if item:
            new_index = board.canvas.index(item, "insert") - 1
            board.canvas.icursor(item, new_index)
            board.canvas.select_clear()

    @staticmethod
    def do_right(_, board):
        # Move text cursor one character to the right

        item = board.canvas.focus()
        if item:
            new_index = board.canvas.index(item, "insert") + 1
            board.canvas.icursor(item, new_index)
            board.canvas.select_clear()

    @staticmethod
    def do_new_line(board):
        # Move text cursor one character to the new line

        item = board.canvas.focus()
        if item:
            board.canvas.icursor(item, "end")
            board.canvas.insert(item, "end", '\n')
            board.canvas.delete("highlight")
            Text.highlight("current", board)
            board.canvas.select_clear()

    @staticmethod
    def do_backspace(_, board):
        # Handle the backspace key

        item = board.canvas.focus()
        if item:
            selection = board.canvas.select_item()
            if selection:
                board.canvas.dchars(item, "sel.first", "sel.last")
                board.canvas.select_clear()
            else:
                insert = board.canvas.index(item, "insert")
                if insert > 0:
                    board.canvas.dchars(item, insert - 1, insert)
            Text.highlight(item, board)

    @staticmethod
    def do_home(_, board):
        """Move text cursor to the start of the text item"""

        item = board.canvas.focus()
        if item:
            board.canvas.icursor(item, 0)
            board.canvas.select_clear()

    @staticmethod
    def do_end(_, board):
        """Move text cursor to the end of the text item"""

        item = board.canvas.focus()
        if item:
            board.canvas.icursor(item, "end")
            board.canvas.select_clear()

    @staticmethod
    def do_key(event, board):
        """Handle the insertion of characters"""

        item = board.canvas.focus()
        if item and event.char >= " ":
            _ = board.canvas.index(item, "insert")
            selection = board.canvas.select_item()
            if selection:
                board.canvas.dchars(item, "sel.first", "sel.last")
                board.canvas.select_clear()
            board.canvas.insert(item, "insert", event.char)
            Text.highlight(item, board)

    @staticmethod
    def highlight(item, board):
        """Highlight the given text item to show that it's editable"""

        items = board.canvas.find_withtag("highlight")
        if len(items) == 0:
            # no highlight box; create it
            ids = board.canvas.create_rectangle((0, 0, 0, 0), fill="white",
                                                outline="blue",
                                                dash=".", tag="highlight")
            board.canvas.lower(ids, item)
        else:
            ids = items[0]
            board.canvas.lower(ids, item)

        # resize the highlight
        bbox = board.canvas.bbox(item)
        rect_bbox = (bbox[0] - 4, bbox[1] - 4, bbox[2] + 4, bbox[3] + 4)
        board.canvas.coords(ids, rect_bbox)

    @staticmethod
    def set_focus(_, board):
        # Give focus to the text element under the cursor double-click
        if board.canvas.type("current") == "text":
            board.canvas.focus_set()
            board.canvas.focus("current")
            board.canvas.select_from("current", 0)
            board.canvas.select_to("current", "end")
            Text.highlight("current", board)

    @staticmethod
    def set_cursor(event, board):
        """Move the insertion point"""
        board.canvas.focus("")
        item = board.canvas.focus()
        if item:
            x = board.canvas.canvasx(event.x)
            y = board.canvas.canvasy(event.y)

            board.canvas.icursor(item, "@%d,%d" % (x, y))
            board.canvas.select_clear()
        widget = event.widget
        widget.startX = event.x
        widget.startY = event.y
        Text.highlight("current", board)

    @staticmethod
    def do_move(event, board):
        widget = event.widget
        x = widget.winfo_x() - widget.startX + event.x
        y = widget.winfo_y() - widget.startY + event.y
        # item = board.canvas.focus()
        if board.canvas.type("current") == "text":
            # board.canvas.focus_set()
            board.canvas.focus("current")
            board.canvas.move("current", x, y)
            board.canvas.move("highlight", x, y)
            widget.startX = event.x
            widget.startY = event.y
            board.canvas.update()


Application()
