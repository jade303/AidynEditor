from tkinter import Tk, LabelFrame, mainloop, Button, PhotoImage, Label
from tkinter import filedialog

from lib import characters, accessories, armorshields, wandsscrolls, spells, weapons
from lib.variables import PARTY, PARTY_ADDRESSES, ENEMIES, ENEMY_ADDRESSES, ARMOR_NAMES, ARMOR_ADDRESSES, SHIELD_NAMES, \
    SHIELD_ADDRESSES


def file_dialog():
    # Searching function for the Browse button
    party_name_length = 9
    enemy_name_length = 17

    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("z64", "*.z64"), ("all files", "*.*")))
    if filename != '':
        browse_frame.destroy()
        root.configure(background='white')
        # root.geometry("500x500")
        aidyn = Label(root, image=image)
        aidyn.grid(column=0, row=0, rowspan=9)

        party_button = Button(root, text="Party Edit", width=12,
                              command=lambda: characters.CharacterEdit(filename,
                                                                       PARTY,
                                                                       PARTY_ADDRESSES,
                                                                       party_name_length,
                                                                       1))
        party_button.grid(column=1, row=0, sticky='ew')

        enemy_button = Button(root, text="Enemy Edit", width=12,
                              command=lambda: characters.CharacterEdit(filename,
                                                                       ENEMIES,
                                                                       ENEMY_ADDRESSES,
                                                                       enemy_name_length,
                                                                       0))
        enemy_button.grid(column=1, row=1)

        accessory_button = Button(root, text="Accessory Edit", width=12,
                                  command=lambda: accessories.AccessoryEdit(filename))
        accessory_button.grid(column=1, row=2)

        armor_button = Button(root, text="Armor Edit", width=12,
                              command=lambda: armorshields.ArmorShieldEdit(filename,
                                                                           ARMOR_NAMES,
                                                                           ARMOR_ADDRESSES,
                                                                           1))
        armor_button.grid(column=1, row=3)

        item_button = Button(root, text='Item Edit', width=12,
                             command=lambda: wandsscrolls.ItemEdit(filename))
        item_button.grid(column=1, row=4)

        shield_button = Button(root, text="Shield Edit", width=12,
                               command=lambda: armorshields.ArmorShieldEdit(filename,
                                                                            SHIELD_NAMES,
                                                                            SHIELD_ADDRESSES,
                                                                            0))
        shield_button.grid(column=1, row=5)

        spell_button = Button(root, text="Spell Edit", width=12,
                              command=lambda: spells.SpellEdit(filename))
        spell_button.grid(column=1, row=6)

        weapon_button = Button(root, text="Weapon Edit", width=12,
                               command=lambda: weapons.WeaponEdit(filename))
        weapon_button.grid(column=1, row=7)


root = Tk()
root.resizable(False, False)
root.title("Aidyn Editor")
root.iconbitmap('images\\aidyn.ico')
image = PhotoImage(file="images\\aidyn.gif")

browse_frame = LabelFrame(root, text="Aidyn Chronicles ROM")
browse_frame.pack()
browse_button = Button(browse_frame, text='Browse', command=file_dialog)
browse_button.pack()

mainloop()
