from tkinter import Toplevel


class ItemEdit:
    def __init__(self, filename):
        itemwin = Toplevel()
        itemwin.resizable(False, False)
        itemwin.title("Item Edit")
        filename = filename
