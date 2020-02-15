from functools import partial
from tkinter import Toplevel, StringVar, Button, LabelFrame, Label, Entry, Frame
from tkinter.ttk import Combobox

from lib.limits import limit
from lib.variables import SKILLS, SHOP_SKILLS, SHOPS, SHOP_SHIELD, SHOP_SPELLS, inv_SPELLS, SPELLS, ITEMS, \
    inv_DROP_ITEMS, SHOP_ITEM_ADDRESSES


class TrainerEdit:
    def __init__(self, filename, icon_dir):
        win = Toplevel()
        win.resizable(False, False)
        win.title("Shops and Trainer Edit")
        win.iconbitmap(icon_dir)
        filename = filename
        skill_read = 23
        shield_read = 1
        spell_read = 16
        NOT = ["Talewok : Dryad", "Talewok : Professor 1", "Talewok : Professor 2", "Talewok : Professor 3"]

        main_win = Frame(win)
        main_win.grid(column=0, row=0)
        shop_win = Frame(win)
        shop_win.grid(column=1, row=0)

        def defaults(*args):
            with open(filename, 'rb') as f:
                # trainer skills + shield
                address = SHOP_SKILLS[SHOPS.index(trainer.get())]
                f.seek(address)
                d = f.read(skill_read).hex()

                for s in skills:
                    sa = skills.index(s) * 2
                    sn = int(d[sa] + d[sa + 1], 16)
                    if sn == 255:
                        sn = ''
                    s.set(sn)

                address = SHOP_SHIELD[SHOPS.index(trainer.get())]
                f.seek(address)
                d = f.read(shield_read).hex()

                shi = int(d[0] + d[1], 16)
                if shi == 255:
                    shi = ''
                shield_skill.set(shi)

                # trainer spells
                address = SHOP_SPELLS[SHOPS.index(trainer.get())]
                f.seek(address)
                d = f.read(spell_read).hex()

                for s in spells:
                    x = (spells.index(s) * 4)
                    y = x + 4
                    s.set(inv_SPELLS[d[x:y].upper()])

                for s in spell_levels:
                    x = (spell_levels.index(s) * 2) + 22
                    s.set(int(d[x] + d[x + 1], 16))

                if trainer.get() in NOT:
                    shop_win.grid_forget()
                    for item in shop_item:
                        item.set('')

                else:
                    shop_win.grid(column=1, row=0)
                    address = SHOP_ITEM_ADDRESSES[SHOPS.index(trainer.get())]
                    f.seek(address)

                    for item in shop_item:
                        d = f.read(2).hex()
                        item.set(inv_DROP_ITEMS[d[0:4].upper()])
                        if shop_item.index(item) < 20:
                            address += 5
                            f.seek(address)
                        else:
                            address += 2
                            f.seek(address)

        def write():
            with open(filename, 'rb+') as f:
                # write skills + shield
                address = SHOP_SKILLS[SHOPS.index(trainer.get())]
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

                address = SHOP_SHIELD[SHOPS.index(trainer.get())]
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
                address = SHOP_SPELLS[SHOPS.index(trainer.get())]
                f.seek(address)
                d = f.read(spell_read).hex()

                for i in spells:
                    towrite.append(int((SPELLS[i.get()])[:2], 16))
                    towrite.append(int((SPELLS[i.get()])[2:], 16))

                towrite.append(int(d[9] + d[10], 16))

                for i in spell_levels:
                    towrite.append(int(i.get()))

                f.seek(address)
                for item in towrite:
                    f.write(item.to_bytes(1, byteorder='big'))

                towrite[:] = []
                if trainer.get() not in NOT:
                    address = SHOP_ITEM_ADDRESSES[SHOPS.index(trainer.get())]
                    f.seek(address)
                    d = f.read(108).hex()

                    for item in shop_item:
                        if shop_item.index(item) < 20:
                            towrite.append(int((ITEMS[item.get()])[:2], 16))
                            towrite.append(int((ITEMS[item.get()])[2:], 16))
                            for x in range(5, 11, 2):
                                towrite.append(int(d[((shop_item.index(item) * 10) + x)] +
                                                   d[((shop_item.index(item) * 10) + (x + 1))], 16))

                        else:
                            towrite.append(int((ITEMS[item.get()])[:2], 16))
                            towrite.append(int((ITEMS[item.get()])[2:], 16))

                    f.seek(address)
                    for item in towrite:
                        f.write(item.to_bytes(1, byteorder='big'))

        def build():
            default_name_menu = Combobox(main_win, textvariable=trainer, values=SHOPS, width=26)
            default_name_menu.grid(column=0, row=0)

            spell_frame = LabelFrame(main_win, text='Spells and Spell Level')
            spell_frame.grid(column=0, row=1)

            for s in spells:
                x = spells.index(s)
                spell = Combobox(spell_frame, textvariable=s, values=list(SPELLS.keys()))
                spell.grid(column=0, row=x)
                spell.config(width=16)
                spell_level = Entry(spell_frame, textvariable=spell_levels[spells.index(s)])
                spell_level.grid(column=1, row=x)
                spell_level.config(width=4)

            save = Button(main_win, text="Save", command=write)
            save.grid(column=0, row=3)
            save.config(width=8)

            skill_frame = LabelFrame(main_win, text='Skills\n(blank = cannot learn)')
            skill_frame.grid(column=1, row=0, rowspan=23)

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

            item_frame = LabelFrame(shop_win, text='Shop Items')
            item_frame.grid(column=2, row=0, rowspan=23)

            for item in shop_item:
                item_box = Combobox(item_frame, textvariable=item, values=list(ITEMS.keys()), width=28)
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

        trainer.set(SHOPS[0])
        build()
