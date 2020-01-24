from tkinter import Tk, LabelFrame, mainloop, Button
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
        """
        filenamelabel = Label(root, text=filename)
        filenamelabel.grid(column=0, row=0, sticky='ew')
        """
        party_button = Button(root, text="Party Edit",
                              command=lambda: CharacterWindow.CharacterEdit(filename,
                                                                            PARTY,
                                                                            PARTY_ADDRESSES,
                                                                            party_name_length,
                                                                            1))
        party_button.grid(column=0, row=1, sticky='ew')
        party_button.config(width=12)

        enemy_button = Button(root, text="Enemy Edit",
                              command=lambda: CharacterWindow.CharacterEdit(filename,
                                                                            ENEMIES,
                                                                            ENEMY_ADDRESSES,
                                                                            enemy_name_length,
                                                                            0))
        enemy_button.grid(column=0, row=2)
        enemy_button.config(width=12)

        """accessory_button = Button(root, text="Accessory Edit",
                                  command=lambda: AccessoryWindow.AccessoryEdit(filename))
        accessory_button.grid(column=0, row=3)
        accessory_button.config(width=12)"""

        armor_button = Button(root, text="Armor Edit",
                              command=lambda: ArmorShieldWindow.ArmorShieldEdit(filename,
                                                                                ARMOR_NAMES,
                                                                                ARMOR_ADDRESSES,
                                                                                1))
        armor_button.grid(column=0, row=4)
        armor_button.config(width=12)

        """item_button = Button(root, text='Item Edit',
                             command=lambda: ItemWindow.ItemEdit(filename))
        item_button.grid(column=0, row=5)
        item_button.config(width=12)"""

        shield_button = Button(root, text="Shield Edit",
                               command=lambda: ArmorShieldWindow.ArmorShieldEdit(filename,
                                                                                 SHIELD_NAMES,
                                                                                 SHIELD_ADDRESSES,
                                                                                 0))
        shield_button.grid(column=0, row=6)
        shield_button.config(width=12)

        spell_button = Button(root, text="Spell Edit",
                              command=lambda: SpellWindow.SpellEdit(filename))
        spell_button.grid(column=0, row=7)
        spell_button.config(width=12)

        weapon_button = Button(root, text="Weapon Edit",
                               command=lambda: WeaponWindow.WeaponEdit(filename))
        weapon_button.grid(column=0, row=8)
        weapon_button.config(width=12)


root = Tk()
root.resizable(False, False)
root.title("Aidyn Editor")

browse_frame = LabelFrame(root, text="Aidyn Chronicles ROM")
browse_frame.pack()
browse_button = Button(browse_frame, text='Browse', command=file_dialog)
browse_button.pack()

mainloop()
