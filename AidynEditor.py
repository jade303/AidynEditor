from pathlib import Path
import shutil
from tkinter import Tk, LabelFrame, mainloop, Button, PhotoImage, Label, Checkbutton, BooleanVar
from tkinter import filedialog

from lib import accessories, armor_shields, characters_enemydrops, spells, wands_scrolls, weapons, trainers_shops
from lib.variables import ARMOR_ADDRESSES, SHIELD_ADDRESSES, PARTY_ADDRESSES, ENEMY_ADDRESSES

# todo: add comments/documentation
# todo: test exp stat / enemy vulnerabilities
# todo: giant bat vulnerable to solar and alchemist? 170 max hp lvl 40 with Pochangaret's stats (160 hp at lvl 30)

p = Path()
background = p / 'images/aidyn.gif'
icon = p / 'images/aidyn.ico'


def file_dialog():
    # function that searches for 'filename' and creates the links to the
    # different editing windows
    party_name_length = 9
    enemy_name_length = 17
    button_width = 10

    filename = filedialog.askopenfilename(initialdir='/',
                                          title='Select A File',
                                          filetype=(('z64', '*.z64'), ('all files', '*.*')))

    if filename != '':
        browse_frame.destroy()

        if backup.get():  # creates a backup of the ROM file before editing
            backup_file = filename.rstrip('.z64') + ' (backup).z64'
            shutil.copy2(filename, backup_file)

        root.configure(background='white')
        aidyn = Label(root, image=image)
        aidyn.grid(column=0, row=0, rowspan=9)

        party_button = Button(root, text='Party', width=button_width,
                              command=lambda: characters_enemydrops.CharacterEdit(filename,
                                                                                  icon,
                                                                                  PARTY_ADDRESSES,
                                                                                  party_name_length,
                                                                                  0))  # this number provides
        party_button.grid(column=1, row=0, sticky='ew')                                # the type of window
                                                                                       # i.e. 0 = party, 1 = enemy
        enemy_button = Button(root, text='Enemy', width=button_width,
                              command=lambda: characters_enemydrops.CharacterEdit(filename,
                                                                                  icon,
                                                                                  ENEMY_ADDRESSES,
                                                                                  enemy_name_length,
                                                                                  1))
        enemy_button.grid(column=1, row=1)

        trainer_button = Button(root, text='Shop / Trainer', width=button_width,
                                command=lambda: trainers_shops.TrainerEdit(filename, icon))
        trainer_button.grid(column=1, row=2)

        accessory_button = Button(root, text='Accessory', width=button_width,
                                  command=lambda: accessories.AccessoryEdit(filename, icon))
        accessory_button.grid(column=1, row=3)

        armor_button = Button(root, text='Armor', width=button_width,
                              command=lambda: armor_shields.ArmorShieldEdit(filename,
                                                                            icon,
                                                                            ARMOR_ADDRESSES,
                                                                            1))
        armor_button.grid(column=1, row=4)

        shield_button = Button(root, text='Shield', width=button_width,
                               command=lambda: armor_shields.ArmorShieldEdit(filename,
                                                                             icon,
                                                                             SHIELD_ADDRESSES,
                                                                             0))
        shield_button.grid(column=1, row=5)

        spell_button = Button(root, text='Spell', width=button_width,
                              command=lambda: spells.SpellEdit(filename, icon))
        spell_button.grid(column=1, row=6)

        wandsscrolls_button = Button(root, text='Wand / Scroll', width=button_width,
                                     command=lambda: wands_scrolls.WandScrollEdit(filename, icon))
        wandsscrolls_button.grid(column=1, row=7)

        weapon_button = Button(root, text='Weapon', width=button_width,
                               command=lambda: weapons.WeaponEdit(filename, icon))
        weapon_button.grid(column=1, row=8)


root = Tk()
root.resizable(False, False)
root.title('Aidyn Editor')
root.iconbitmap(icon)
image = PhotoImage(file=background)
backup = BooleanVar()
backup.set(True)  # sets default mode to create a backup (False would be default no)

browse_frame = LabelFrame(root, text='Aidyn Chronicles ROM')
browse_frame.pack()
browse_button = Button(browse_frame, text='Browse', command=file_dialog)
browse_button.pack()
back_up = Checkbutton(browse_frame, text='Backup', var=backup)
back_up.pack()

mainloop()
