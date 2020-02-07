from functools import partial
from tkinter import Toplevel, StringVar, Button, LabelFrame, Label, Entry
from tkinter.ttk import Combobox

from lib.limits import limit
from lib.variables import SKILLS, SHOP_SKILLS, SHOPS, SHOP_SHIELD, SHOP_SPELLS, inv_SPELLS, SPELLS


class TrainerEdit:
    def __init__(self, filename, icon_dir):
        trainwin = Toplevel()
        trainwin.resizable(False, False)
        trainwin.title("Trainer Edit")
        trainwin.iconbitmap(icon_dir)
        filename = filename
        skill_read = 23
        shield_read = 1
        spell_read = 16

        def defaults(*args):
            with open(filename, 'rb') as f:
                # trainer skills + shield
                address = SHOP_SKILLS[SHOPS.index(trainer.get())]
                f.seek(address)
                data = f.read(skill_read)
                d = data.hex()

                for s in skills:
                    sa = skills.index(s) * 2
                    sn = int(d[sa] + d[sa + 1], 16)
                    if sn == 255:
                        sn = ''
                    s.set(sn)

                address = SHOP_SHIELD[SHOPS.index(trainer.get())]
                f.seek(address)
                data = f.read(shield_read)
                d = data.hex()

                shi = int(d[0] + d[1], 16)
                if shi == 255:
                    shi = ''
                shield_skill.set(shi)

                # trainer spells
                address = SHOP_SPELLS[SHOPS.index(trainer.get())]
                f.seek(address)
                data = f.read(spell_read)
                d = data.hex()

                for s in spells:
                    x = (spells.index(s) * 4)
                    y = x + 4
                    s.set(inv_SPELLS[d[x:y].upper()])

                for s in spell_levels:
                    x = (spell_levels.index(s) * 2) + 22
                    s.set(int(d[x] + d[x + 1], 16))

        def write():
            with open(filename, 'rb+') as f:
                # write skills + shield
                address = SHOP_SKILLS[SHOPS.index(trainer.get())]
                f.seek(address)
                data = f.read(skill_read)
                d = data.hex()

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
                data = f.read(shield_read)
                d = data.hex()

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
                data = f.read(spell_read)
                d = data.hex()

                for i in spells:
                    towrite.append(int((SPELLS[i.get()])[:2], 16))
                    towrite.append(int((SPELLS[i.get()])[2:], 16))

                towrite.append(int(d[9] + d[10], 16))

                for i in spell_levels:
                    towrite.append(int(i.get()))

                f.seek(address)
                for item in towrite:
                    f.write(item.to_bytes(1, byteorder='big'))

        def build():
            default_name_menu = Combobox(trainwin, textvariable=trainer, values=SHOPS)
            default_name_menu.grid(column=0, row=0)
            default_name_menu.config(width=26)

            spell_frame = LabelFrame(trainwin, text='Spells and Spell Level')
            spell_frame.grid(column=0, row=1)

            for s in spells:
                x = spells.index(s)
                spell = Combobox(spell_frame, textvariable=s, values=list(SPELLS.keys()))
                spell.grid(column=0, row=x)
                spell.config(width=16)
                spell_level = Entry(spell_frame, textvariable=spell_levels[spells.index(s)])
                spell_level.grid(column=1, row=x)
                spell_level.config(width=4)

            save = Button(trainwin, text="Save", command=write)
            save.grid(column=0, row=3)
            save.config(width=8)

            skill_frame = LabelFrame(trainwin, text='Skills\n(blank = cannot learn)')
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

        trainer.set(SHOPS[0])
        build()
