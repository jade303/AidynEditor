from tkinter import Toplevel, Label


class WandScrollEdit:
    def __init__(self, filename):
        wandwin = Toplevel()
        wandwin.resizable(False, False)
        wandwin.title("Item Edit")
        wandwin.iconbitmap('images\\aidyn.ico')
        filename = filename
        data_seek = 0
        data_read = 0
        name_length = 0

        label = Label(wandwin, text='Nothing yet!')
        label.grid()
