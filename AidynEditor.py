from tkinter import Tk, LabelFrame, mainloop, Button, PhotoImage, Label
from tkinter import filedialog
import os

from lib import accessories, armorshields, characters, spells, wandsscrolls, weapons
from lib.variables import PARTY, PARTY_ADDRESSES, ENEMIES, ENEMY_ADDRESSES, ARMOR_NAMES, ARMOR_ADDRESSES, \
    SHIELD_NAMES, SHIELD_ADDRESSES


dir_path = os.path.dirname(os.path.realpath(__file__))
background_dir = dir_path + '\\images\\aidyn.gif'
icon_dir = dir_path + '\\images\\aidyn.ico'


def file_dialog():
    # Searching function for the Browse button
    party_name_length = 9
    enemy_name_length = 17
    button_width = 10

    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("z64", "*.z64"), ("all files", "*.*")))
    if filename != '':
        browse_frame.destroy()
        root.configure(background='white')
        # root.geometry("500x500")
        aidyn = Label(root, image=image)
        aidyn.grid(column=0, row=0, rowspan=9)

        party_button = Button(root, text="Party", width=button_width,
                              command=lambda: characters.CharacterEdit(filename,
                                                                       icon_dir,
                                                                       PARTY,
                                                                       PARTY_ADDRESSES,
                                                                       party_name_length,
                                                                       1))
        party_button.grid(column=1, row=0, sticky='ew')

        enemy_button = Button(root, text="Enemy", width=button_width,
                              command=lambda: characters.CharacterEdit(filename,
                                                                       icon_dir,
                                                                       ENEMIES,
                                                                       ENEMY_ADDRESSES,
                                                                       enemy_name_length,
                                                                       0))
        enemy_button.grid(column=1, row=1)

        accessory_button = Button(root, text="Accessory", width=button_width,
                                  command=lambda: accessories.AccessoryEdit(filename, icon_dir))
        accessory_button.grid(column=1, row=2)

        armor_button = Button(root, text="Armor", width=button_width,
                              command=lambda: armorshields.ArmorShieldEdit(filename,
                                                                           icon_dir,
                                                                           ARMOR_NAMES,
                                                                           ARMOR_ADDRESSES,
                                                                           1))
        armor_button.grid(column=1, row=3)

        wandsscrolls_button = Button(root, text='Wand / Scroll', width=button_width,
                                     command=lambda: wandsscrolls.WandScrollEdit(filename, icon_dir))
        wandsscrolls_button.grid(column=1, row=4)

        shield_button = Button(root, text="Shield", width=button_width,
                               command=lambda: armorshields.ArmorShieldEdit(filename,
                                                                            icon_dir,
                                                                            SHIELD_NAMES,
                                                                            SHIELD_ADDRESSES,
                                                                            0))
        shield_button.grid(column=1, row=5)

        spell_button = Button(root, text="Spell", width=button_width,
                              command=lambda: spells.SpellEdit(filename, icon_dir))
        spell_button.grid(column=1, row=6)

        weapon_button = Button(root, text="Weapon", width=button_width,
                               command=lambda: weapons.WeaponEdit(filename, icon_dir))
        weapon_button.grid(column=1, row=7)


root = Tk()
root.resizable(False, False)
root.title("Aidyn Editor")
root.iconbitmap(icon_dir)
image = PhotoImage(file=background_dir)

browse_frame = LabelFrame(root, text="Aidyn Chronicles ROM")
browse_frame.pack()
browse_button = Button(browse_frame, text='Browse', command=file_dialog)
browse_button.pack()

mainloop()
