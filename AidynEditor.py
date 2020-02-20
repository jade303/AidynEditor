from pathlib import Path
import shutil
from tkinter import Tk, LabelFrame, mainloop, Button, PhotoImage, Label, Checkbutton, BooleanVar, IntVar
from tkinter import filedialog

from lib import accessories, armor_shields, characters_enemydrops, spells, wands_scrolls, weapons, trainers_shops
from lib.variables import PARTY, PARTY_ADDRESSES, ENEMIES, ENEMY_ADDRESSES, ARMOR_NAMES, ARMOR_ADDRESSES, \
    SHIELD_NAMES, SHIELD_ADDRESSES

p = Path()
background = p / 'images/aidyn.gif'
icon = p / 'images/aidyn.ico'


def file_dialog():
    # Searching function for the Browse button
    party_name_length = 9
    enemy_name_length = 17
    button_width = 10

    filename = filedialog.askopenfilename(initialdir='/',
                                          title='Select A File',
                                          filetype=(('z64', '*.z64'), ('all files', '*.*')))

    if filename != '':
        browse_frame.destroy()

        if backup.get():
            backup_file = filename + '.bak'
            shutil.copy2(filename, backup_file)

        root.configure(background='white')
        aidyn = Label(root, image=image)
        aidyn.grid(column=0, row=0, rowspan=9)

        party_button = Button(root, text='Party', width=button_width,
                              command=lambda: characters_enemydrops.CharacterEdit(filename,
                                                                                  icon,
                                                                                  PARTY,
                                                                                  PARTY_ADDRESSES,
                                                                                  party_name_length,
                                                                                  0))
        party_button.grid(column=1, row=0, sticky='ew')

        enemy_button = Button(root, text='Enemy', width=button_width,
                              command=lambda: characters_enemydrops.CharacterEdit(filename,
                                                                                  icon,
                                                                                  ENEMIES,
                                                                                  ENEMY_ADDRESSES,
                                                                                  enemy_name_length,
                                                                                  1))
        enemy_button.grid(column=1, row=1)

        accessory_button = Button(root, text='Accessory', width=button_width,
                                  command=lambda: accessories.AccessoryEdit(filename, icon))
        accessory_button.grid(column=1, row=2)

        armor_button = Button(root, text='Armor', width=button_width,
                              command=lambda: armor_shields.ArmorShieldEdit(filename,
                                                                            icon,
                                                                            ARMOR_NAMES,
                                                                            ARMOR_ADDRESSES,
                                                                            1))
        armor_button.grid(column=1, row=3)

        wandsscrolls_button = Button(root, text='Wand / Scroll', width=button_width,
                                     command=lambda: wands_scrolls.WandScrollEdit(filename, icon))
        wandsscrolls_button.grid(column=1, row=4)

        shield_button = Button(root, text='Shield', width=button_width,
                               command=lambda: armor_shields.ArmorShieldEdit(filename,
                                                                             icon,
                                                                             SHIELD_NAMES,
                                                                             SHIELD_ADDRESSES,
                                                                             0))
        shield_button.grid(column=1, row=5)

        spell_button = Button(root, text='Spell', width=button_width,
                              command=lambda: spells.SpellEdit(filename, icon))
        spell_button.grid(column=1, row=6)

        trainer_button = Button(root, text='Shop / Trainer', width=button_width,
                                command=lambda: trainers_shops.TrainerEdit(filename, icon))
        trainer_button.grid(column=1, row=7)

        weapon_button = Button(root, text='Weapon', width=button_width,
                               command=lambda: weapons.WeaponEdit(filename, icon))
        weapon_button.grid(column=1, row=8)


root = Tk()
root.resizable(False, False)
root.title('Aidyn Editor')
root.iconbitmap(icon)
image = PhotoImage(file=background)
backup = BooleanVar()
backup.set(True)

browse_frame = LabelFrame(root, text='Aidyn Chronicles ROM')
browse_frame.pack()
browse_button = Button(browse_frame, text='Browse', command=file_dialog)
browse_button.pack()
back_up = Checkbutton(browse_frame, text='Backup', var=backup)
back_up.pack()

mainloop()
