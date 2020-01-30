from tkinter import Toplevel, Label


class ItemEdit:
    def __init__(self, filename):
        itemwin = Toplevel()
        itemwin.resizable(False, False)
        itemwin.title("Item Edit")
        itemwin.iconbitmap('images\icon.ico')
        filename = filename

        label = Label(itemwin, text='Nothing yet!')
        label.grid()
