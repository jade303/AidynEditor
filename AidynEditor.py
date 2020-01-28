from tkinter import Tk, LabelFrame, mainloop, Button, PhotoImage, Label, Frame, Canvas
from tkinter import filedialog

import AccessoryWindow
import ItemWindow
from variables import PARTY, PARTY_ADDRESSES, ENEMIES, ENEMY_ADDRESSES, ARMOR_NAMES, ARMOR_ADDRESSES, SHIELD_NAMES, \
    SHIELD_ADDRESSES
import CharacterWindow
import SpellWindow
import WeaponWindow
import ArmorShieldWindow


def file_dialog():
    # Searching function for the Browse button
    party_name_length = 9
    enemy_name_length = 17

    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("z64", "*.z64"), ("all files", "*.*")))
    if filename != '':
        browse_frame.destroy()
        root.configure(background='black')
        # root.geometry("500x500")
        canvas = Canvas(root, width=295, height=225)
        canvas.grid()
        canvas.create_image(150, 115, image=image)
        """
        filenamelabel = Label(root, text=filename)
        filenamelabel.grid(column=0, row=0, sticky='ew')
        """
        party_button = Button(root, text="Party Edit", width=12,
                              command=lambda: CharacterWindow.CharacterEdit(filename,
                                                                            PARTY,
                                                                            PARTY_ADDRESSES,
                                                                            party_name_length,
                                                                            1))
        # party_button.grid(column=0, row=1, sticky='ew')
        # party_button.config(width=12)

        enemy_button = Button(canvas, text="Enemy Edit", width=12,
                              command=lambda: CharacterWindow.CharacterEdit(filename,
                                                                            ENEMIES,
                                                                            ENEMY_ADDRESSES,
                                                                            enemy_name_length,
                                                                            0))
        # enemy_button.grid(column=0, row=2)
        # enemy_button.config(width=12)""".

        accessory_button = Button(canvas, text="Accessory Edit", width=12,
                                  command=lambda: AccessoryWindow.AccessoryEdit(filename))
        # accessory_button.grid(column=0, row=3)
        # accessory_button.config(width=12)

        armor_button = Button(canvas, text="Armor Edit", width=12,
                              command=lambda: ArmorShieldWindow.ArmorShieldEdit(filename,
                                                                                ARMOR_NAMES,
                                                                                ARMOR_ADDRESSES,
                                                                                1))
        # armor_button.grid(column=0, row=4)
        # armor_button.config(width=12)"""

        item_button = Button(root, text='Item Edit', width=12,
                             command=lambda: ItemWindow.ItemEdit(filename))
        # item_button.grid(column=0, row=5)
        # item_button.config(width=12)

        shield_button = Button(canvas, text="Shield Edit", width=12,
                               command=lambda: ArmorShieldWindow.ArmorShieldEdit(filename,
                                                                                 SHIELD_NAMES,
                                                                                 SHIELD_ADDRESSES,
                                                                                 0))
        # shield_button.grid(column=0, row=6)
        # shield_button.config(width=12)

        spell_button = Button(canvas, text="Spell Edit", width=12,
                              command=lambda: SpellWindow.SpellEdit(filename))
        # spell_button.grid(column=0, row=7)
        # spell_button.config(width=12)

        weapon_button = Button(canvas, text="Weapon Edit", width=12,
                               command=lambda: WeaponWindow.WeaponEdit(filename))
        # weapon_button.grid(column=0, row=8)
        # weapon_button.config(width=12)

        party_button_window = canvas.create_window(290, 7, anchor='ne', window=party_button)
        enemy_button_window = canvas.create_window(290, 34, anchor='ne', window=enemy_button)
        accessory_button_window = canvas.create_window(290, 61, anchor='ne', window=accessory_button)
        armor_button_window = canvas.create_window(290, 88, anchor='ne', window=armor_button)
        item_button_window = canvas.create_window(290, 115, anchor='ne', window=item_button)
        shield_button_window = canvas.create_window(290, 142, anchor='ne', window=shield_button)
        spell_button_window = canvas.create_window(290, 169, anchor='ne', window=spell_button)
        weapon_button_window = canvas.create_window(290, 196, anchor='ne', window=weapon_button)


root = Tk()
root.resizable(False, False)
root.title("Aidyn Editor")
root.iconbitmap('images\icon.ico')
image = PhotoImage(file="images\main_background.gif")

browse_frame = LabelFrame(root, text="Aidyn Chronicles ROM")
browse_frame.pack()
browse_button = Button(browse_frame, text='Browse', command=file_dialog)
browse_button.pack()

mainloop()
