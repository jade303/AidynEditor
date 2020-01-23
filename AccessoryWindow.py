from tkinter import Toplevel


class AccessoryEdit:
    def __init__(self, filename):
        accesswin = Toplevel()
        accesswin.resizable(False, False)
        accesswin.title("Accessory Edit")
        filename = filename
