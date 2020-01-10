from tkinter import *
from tkinter import filedialog
from variables import PARTY, PARTY_ADDRESSES, ENEMIES, ENEMY_ADDRESSES
import CharacterWindow
import SpellWindow
import WeaponWindow


def file_dialog():
    # Searching function for the Browse button
    party_name_length = 9
    enemy_name_length = 17

    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("z64", "*.z64"), ("all files", "*.*")))
    if filename != '':
        browse_frame.destroy()
        filenamelabel = Label(root, text=filename)
        filenamelabel.grid(column=0, row=0, columnspan=3, sticky='ew')
        party_button = Button(root, text="Party Edit (NG only)",
                              command=lambda: CharacterWindow.CharacterEdit(filename,
                                                                            PARTY,
                                                                            PARTY_ADDRESSES,
                                                                            party_name_length))
        party_button.grid(column=0, row=1)
        enemy_button = Button(root, text="Enemy Edit",
                              command=lambda: CharacterWindow.CharacterEdit(filename,
                                                                            ENEMIES,
                                                                            ENEMY_ADDRESSES,
                                                                            enemy_name_length))
        enemy_button.grid(column=1, row=1)
        spell_button = Button(root, text="Spell Edit",
                              command=lambda: SpellWindow.SpellEdit(filename))
        spell_button.grid(column=2, row=1)
        weapon_button = Button(root, text="Weapon Edit",
                               command=lambda: WeaponWindow.WeaponEdit(filename))
        weapon_button.grid(column=3, row=1)


root = Tk()
root.title("Aidyn Editor")

browse_frame = LabelFrame(root, text="Aidyn Chronicles ROM")
browse_frame.pack()
browse_button = Button(browse_frame, text='Browse', command=file_dialog)
browse_button.pack()

mainloop()
