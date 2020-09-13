from functools import partial
from tkinter import Toplevel, StringVar, Button, LabelFrame, Label, Entry, Frame
from tkinter.ttk import Combobox

from lib.limits import limit
from lib.list_functions import get_major_item_dic, get_minor_dic
from lib.variables import SKILLS, SHOP_SKILLS, SHOPS, SHOP_SHIELD, SHOP_SPELLS, SHOP_ITEM_ADDRESSES, SPELL_DIC


class TrainerEdit:
    def __init__(self, filename, icon):
        win = Toplevel()
        win.resizable(False, False)
        win.title("Shops and Trainer Edit")
        win.iconbitmap(icon)
        filename = filename
        skill_read = 23
        shield_read = 1
        spell_read = 16
        # following list are the trainers that do not provide shop features
        NOT = ["Talewok : Dryad", "Talewok : Professor 1", "Talewok : Professor 2", "Talewok : Professor 3"]

        shops = []
        with open(filename, 'rb') as f:
            # function for adding Becan's to the list of shops
            # this provides his custom name to the editor (if he is given one)
            f.seek(0x01FC7EA4)
            shops = ['Erromon : ' + f.read(9).decode("utf-8").rstrip('\x00')] + SHOPS

        items = get_major_item_dic(filename)
        inv_items = {v: k for k, v in items.items()}

        spell_dic = get_minor_dic(filename, SPELL_DIC, 22)
        inv_spell_dic = {v: k for k, v in spell_dic.items()}

        main_win = Frame(win)
        main_win.grid(column=0, row=0, pady=5, padx=(5, 0))
        shop_win = LabelFrame(win, text='Shop Items')
        shop_win.grid(column=1, row=0, pady=5, padx=(0, 5), sticky='n')

        def defaults(*args):
            with open(filename, 'rb') as f:
                # gets trainer skills + shield
                address = SHOP_SKILLS[shops.index(trainer.get())]
                f.seek(address)
                d = f.read(skill_read).hex()

                for s in skills:
                    sn = int(d[skills.index(s) * 2] + d[(skills.index(s) * 2) + 1], 16)
                    if sn == 255:
                        sn = ''
                    s.set(sn)

                address = SHOP_SHIELD[shops.index(trainer.get())]
                f.seek(address)
                d = f.read(shield_read).hex()

                shi = int(d[0] + d[1], 16)
                if shi == 255:
                    shi = ''
                shield_skill.set(shi)

                # trainer spells
                address = SHOP_SPELLS[shops.index(trainer.get())]
                f.seek(address)
                d = f.read(spell_read).hex()

                for s in spells:
                    x = (spells.index(s) * 4)
                    y = x + 4
                    s.set(spell_dic[d[x:y].upper()])

                for s in spell_levels:
                    x = (spell_levels.index(s) * 2) + 22
                    s.set(int(d[x] + d[x + 1], 16))

                # determines whether the shop part of the widget should show up
                # 'NOT' is the list of trainers that do not have shop services
                if trainer.get() in NOT:
                    shop_win.grid_forget()
                    for item in shop_item:
                        item.set('')
                else:
                    shop_win.grid(column=1, row=0, pady=5, padx=(0, 5), sticky='n')
                    address = SHOP_ITEM_ADDRESSES[shops.index(trainer.get())]
                    f.seek(address)

                    for item in shop_item:
                        d = f.read(2).hex()
                        item.set(items[d[0:4].upper()])
                        if shop_item.index(item) < 20:
                            address += 5
                            f.seek(address)
                        else:
                            address += 2
                            f.seek(address)

        def write():
            with open(filename, 'rb+') as f:
                # write skills + shield
                address = SHOP_SKILLS[shops.index(trainer.get())]
                f.seek(address)

                towrite = []
                for i in skills:
                    j = i.get()
                    if j == '':
                        j = 255
                    towrite.append(int(j))

                f.seek(address)
                for item in towrite:
                    f.write(item.to_bytes(1, byteorder='big'))

                towrite[:] = []

                address = SHOP_SHIELD[shops.index(trainer.get())]
                f.seek(address)

                shi = shield_skill.get()
                if shi == '':
                    shi = 255
                towrite.append(int(shi))

                f.seek(address)
                for item in towrite:
                    f.write(item.to_bytes(1, byteorder='big'))

                # write spells
                towrite[:] = []
                address = SHOP_SPELLS[shops.index(trainer.get())]
                f.seek(address)
                d = f.read(spell_read).hex()

                for i in spells:
                    towrite.append(int((inv_spell_dic[i.get()])[:2], 16))
                    towrite.append(int((inv_spell_dic[i.get()])[2:], 16))

                towrite.append(int(d[9] + d[10], 16))

                for i in spell_levels:
                    towrite.append(int(i.get()))

                f.seek(address)
                for item in towrite:
                    f.write(item.to_bytes(1, byteorder='big'))

                # process for writing shop items to file
                towrite[:] = []
                if trainer.get() not in NOT:
                    address = SHOP_ITEM_ADDRESSES[shops.index(trainer.get())]
                    f.seek(address)
                    d = f.read(108).hex()

                    for item in shop_item:
                        if shop_item.index(item) < 20:
                            towrite.append(int((inv_items[item.get()])[:2], 16))
                            towrite.append(int((inv_items[item.get()])[2:], 16))
                            for x in range(5, 11, 2):
                                towrite.append(int(d[((shop_item.index(item) * 10) + x)] +
                                                   d[((shop_item.index(item) * 10) + (x + 1))], 16))

                        else:
                            towrite.append(int((inv_items[item.get()])[:2], 16))
                            towrite.append(int((inv_items[item.get()])[2:], 16))

                    f.seek(address)
                    for item in towrite:
                        f.write(item.to_bytes(1, byteorder='big'))

        def build():
            default_name_menu = Combobox(main_win, textvariable=trainer, values=shops, width=26, state='readonly')
            default_name_menu.grid(column=0, row=0)

            save = Button(main_win, text="Save", command=write)
            save.grid(column=0, row=1)
            save.config(width=8)

            spell_frame = LabelFrame(main_win, text='Spells and Spell Level')
            spell_frame.grid(column=0, row=2)

            for s in spells:
                x = spells.index(s)
                spell = Combobox(spell_frame, textvariable=s, values=list(inv_spell_dic.keys()), state='readonly')
                spell.grid(column=0, row=x)
                spell.config(width=16)
                spell_level = Entry(spell_frame, textvariable=spell_levels[spells.index(s)])
                spell_level.grid(column=1, row=x)
                spell_level.config(width=4)

            skill_frame = LabelFrame(main_win, text='Skills')
            skill_frame.grid(column=1, row=0, rowspan=24, padx=(2, 5))

            for skill in SKILLS:
                x = SKILLS.index(skill)
                skill_label = Label(skill_frame, text=skill, anchor='e', width=9)
                skill_label.grid(column=0, row=x)
                skill_num = Entry(skill_frame, textvariable=skills[x], width=4)
                skill_num.grid(column=1, row=x)
            shield_label = Label(skill_frame, text='Shield', anchor='e', width=9)
            shield_label.grid(column=0, row=23)
            shield_num = Entry(skill_frame, textvariable=shield_skill, width=4)
            shield_num.grid(column=1, row=23)

            note_box = LabelFrame(main_win, text='Notes on skills')
            noteA = Label(note_box, anchor='w', width=30, font=(None, 8),
                          text='* ' + shops[0][10:] + ' edits affect the party version\nof his character\n'
                                                      '- So blank means he can\'t learn')
            noteC = Label(note_box, anchor='w', width=30, font=(None, 8),
                          text='* Blank and 0 mean those particular\nskills are not taught')
            note_box.grid(column=0, row=3)
            noteA.grid()
            noteC.grid()

            for item in shop_item:
                item_box = Combobox(shop_win, textvariable=item, values=list(inv_items.keys()),
                                    width=28, state='readonly')
                item_box.grid()

        trainer = StringVar()
        trainer.trace('w', defaults)

        skills = []
        for _ in SKILLS:
            i = StringVar()
            i.trace('w', partial(limit, i, 10))
            skills.append(i)
        shield_skill = StringVar()
        shield_skill.trace('w', partial(limit, shield_skill, 10))

        spells = []
        for i in range(5):
            i = StringVar()
            spells.append(i)

        spell_levels = []
        for i in range(5):
            i = StringVar()
            i.trace('w', partial(limit, i, 15))
            spell_levels.append(i)

        shop_item = []
        for i in range(1, 24):
            i = StringVar()
            shop_item.append(i)

        trainer.set(shops[0])
        build()
