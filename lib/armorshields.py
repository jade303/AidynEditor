from functools import partial
from tkinter import Toplevel, StringVar, IntVar, LabelFrame, Frame, Entry, Label, Button, Radiobutton
from tkinter.ttk import Combobox

from lib.functions import limit_name_size, limit_127, limit
from lib.variables import inv_EQUIPMENT_STAT, inv_SKILL_ATTRIBUTE, inv_SPELLS, inv_RESIST, inv_RESIST_AMOUNTS, \
    EQUIPMENT_STAT, SKILL_ATTRIBUTE, SPELLS, RESIST, RESIST_AMOUNTS


class ArmorShieldEdit:
    def __init__(self, filename, names, addresses, title):
        shiwin = Toplevel()
        shiwin.resizable(False, False)
        if title == 1:
            shiwin.title("Armor Edit")
        elif title == 0:
            shiwin.title("Shield Edit")
        shiwin.iconbitmap('images\\aidyn.ico')
        filename = filename
        data_seek = 26
        data_read = 25
        name_length = 22
        names = names
        addresses = addresses

        def set_defaults(*args):
            with open(filename, 'rb') as f:
                address = addresses[names.index(item.get())]
                f.seek(address)
                name.set(f.read(name_length).decode("utf-8"))

                f.seek(address + data_seek)
                data = f.read(data_read)
                d = data.hex()

                defense.set(int(d[0] + d[1], 16))
                protection.set(int(d[2] + d[3], 16))
                dx = int(d[4] + d[5], 16)
                if dx > 127:
                    dx = dx - 256
                dexterity.set(dx)

                sneak = int(d[8] + d[9], 16)
                if sneak > 127:
                    sneak = sneak - 256
                stealth.set(sneak)
                value.set((int(d[12] + d[13], 16) * 256) + int(d[10] + d[11], 16))

                aspect.set(d[17])
                stat.set(inv_EQUIPMENT_STAT[(d[18] + d[19]).upper()])
                st = int(d[20] + d[21], 16)
                if st > 127:
                    st = st - 256
                stat_amount.set(st)
                skill.set(inv_SKILL_ATTRIBUTE[(d[22] + d[23]).upper()])
                att_amount = int(d[24] + d[25], 16)
                if att_amount > 127:
                    att_amount = att_amount - 256
                skill_amount.set(att_amount)
                spell.set(inv_SPELLS[(d[26:30]).upper()])
                spell_level.set(int(d[30] + d[31], 16))

                magic.set(inv_SPELLS[(d[34:38]).upper()])
                magic_level.set(int(d[38] + d[39], 16))
                resist.set(inv_RESIST[(d[40] + d[41]).upper()])
                resist_amount.set(inv_RESIST_AMOUNTS[(d[42] + d[43]).upper()])

        def write():
            with open(filename, 'rb+') as f:
                address = addresses[names.index(item.get())]

                new_name = bytearray(name.get(), 'utf-8')
                if len(new_name) < name_length:
                    while len(new_name) < name_length:
                        new_name.append(0x00)
                f.seek(address)
                f.write(new_name)

                f.seek(address + data_seek)
                data = f.read(data_read)
                d = data.hex()

                new_value = value.get()
                v2, v1 = divmod(int(new_value), 256)
                if v2 == 256:
                    v2 = 255
                    v1 = 255

                dx = int(dexterity.get())
                if dx < 0:
                    dx = dx + 256

                sneak = int(stealth.get())
                if sneak < 0:
                    sneak = sneak + 256

                st = int(stat_amount.get())
                if st < 0:
                    st = st + 256

                sk = int(skill_amount.get())
                if sk < 0:
                    sk = sk + 256

                towrite = [
                    int(defense.get()),
                    int(protection.get()),
                    int(dx),
                    int(d[6] + d[7], 16),
                    int(sneak),
                    int(v1), int(v2),
                    int(d[14] + d[15], 16),
                    aspect.get(),
                    int(EQUIPMENT_STAT[stat.get()], 16),
                    int(st),
                    int(SKILL_ATTRIBUTE[skill.get()], 16),
                    int(sk),
                    int((SPELLS[spell.get()])[:2], 16),
                    int((SPELLS[spell.get()])[2:], 16),
                    int(spell_level.get()),
                    int(d[32] + d[33], 16),
                    int((SPELLS[magic.get()])[:2], 16),
                    int((SPELLS[magic.get()])[2:], 16),
                    int(magic_level.get()),
                    int(RESIST[resist.get()], 16),
                    int(RESIST_AMOUNTS[resist_amount.get()], 16)
                ]

                f.seek(address + data_seek)
                for i in towrite:
                    f.write(i.to_bytes(1, byteorder='big'))

        def build():
            lawfulgood_frame = Frame(shiwin)
            lawfulgood_frame.grid(column=0, row=0)
            default_item_menu = Combobox(lawfulgood_frame, textvariable=item, values=names)
            default_item_menu.grid(column=0, row=0)
            default_item_menu.config(width=21)

            new_name_label = LabelFrame(lawfulgood_frame, text='New Name')
            new_name_label.grid(column=0, row=1)
            new_name_entry = Entry(new_name_label, textvariable=name)
            new_name_entry.grid()
            new_name_entry.config(width=21)

            lawfulneutral_frame = LabelFrame(shiwin, text='Stats:')
            lawfulneutral_frame.grid(column=0, row=1)

            defense_label = Label(lawfulneutral_frame, text='Defense:')
            defense_label.grid(column=0, row=0, sticky='e')
            defense_entry = Entry(lawfulneutral_frame, textvariable=defense)
            defense_entry.grid(column=1, row=0, stick='e')
            defense_entry.config(width=4)

            protection_label = Label(lawfulneutral_frame, text='Protection:')
            protection_label.grid(column=0, row=1, sticky='e')
            protection_entry = Entry(lawfulneutral_frame, textvariable=protection)
            protection_entry.grid(column=1, row=1, sticky='e')
            protection_entry.config(width=4)

            dexterity_label = Label(lawfulneutral_frame, text='Dexterity:')
            dexterity_label.grid(column=0, row=2, sticky='e')
            dexterity_entry = Entry(lawfulneutral_frame, textvariable=dexterity)
            dexterity_entry.grid(column=1, row=2, sticky='e')
            dexterity_entry.config(width=4)

            stealth_label = Label(lawfulneutral_frame, text='Stealth:')
            stealth_label.grid(column=0, row=3, sticky='e')
            stealth_entry = Entry(lawfulneutral_frame, textvariable=stealth)
            stealth_entry.grid(column=1, row=3, sticky='e')
            stealth_entry.config(width=4)

            value_label = Label(lawfulneutral_frame, text='Base Value:')
            value_label.grid(column=0, row=4, sticky='e')
            value_entry = Entry(lawfulneutral_frame, textvariable=value)
            value_entry.grid(column=1, row=4, sticky='e')
            value_entry.config(width=6)
            value_label2 = Label(lawfulneutral_frame, text='Max base value: 65535')
            value_label2.grid(row=5, columnspan=2)
            value_label2.config(font=(None, 8))

            neutralgood_frame = Frame(shiwin)
            neutralgood_frame.grid(column=1, row=0)

            write_button = Button(neutralgood_frame, text='Write To File', command=write)
            write_button.grid(column=0, row=0)
            write_button.config(width=16)

            aspect_frame = LabelFrame(neutralgood_frame, text='Aspect')
            aspect_frame.grid(column=0, row=1)
            none_radio = Radiobutton(aspect_frame, text='NONE', variable=aspect, value=0)
            none_radio.grid(column=0, row=0)
            solar_radio = Radiobutton(aspect_frame, text="Solar", variable=aspect, value=2)
            solar_radio.grid(column=1, row=0)
            lunar_radio = Radiobutton(aspect_frame, text='Lunar', variable=aspect, value=1)
            lunar_radio.grid(column=2, row=0)

            trueneutral_frame = Frame(shiwin)
            trueneutral_frame.grid(column=1, row=1)

            stat_frame = LabelFrame(trueneutral_frame, text='Stat')
            stat_frame.grid(column=0, row=0)
            stat_menu = Combobox(stat_frame, textvariable=stat, values=list(EQUIPMENT_STAT.keys()))
            stat_menu.grid(column=0, row=0)
            stat_menu.config(width=16)
            stat_entry = Entry(stat_frame, textvariable=stat_amount)
            stat_entry.grid(column=1, row=0, sticky='e')
            stat_entry.config(width=4)

            ski_att_frame = LabelFrame(trueneutral_frame, text='Skill/Attribute')
            ski_att_frame.grid(column=0, row=1)
            ski_att_menu = Combobox(ski_att_frame, textvariable=skill, values=list(SKILL_ATTRIBUTE.keys()))
            ski_att_menu.grid(column=0, row=0)
            ski_att_menu.config(width=16)
            ski_att_amo_entry = Entry(ski_att_frame, textvariable=skill_amount)
            ski_att_amo_entry.grid(column=1, row=0)
            ski_att_amo_entry.config(width=4)

            spell_frame = LabelFrame(trueneutral_frame, text='Spell')
            spell_frame.grid(column=0, row=2)
            spell_menu = Combobox(spell_frame, textvariable=spell, values=list(SPELLS.keys()))
            spell_menu.grid(column=0, row=0)
            spell_menu.config(width=16)
            spell_entry = Entry(spell_frame, textvariable=spell_level)
            spell_entry.grid(column=1, row=0)
            spell_entry.config(width=4)

            magic_frame = LabelFrame(trueneutral_frame, text='Magic')
            magic_frame.grid(column=0, row=3)
            magic_menu = Combobox(magic_frame, textvariable=magic, values=list(SPELLS.keys()))
            magic_menu.grid(column=0, row=0)
            magic_menu.config(width=16)
            magic_entry = Entry(magic_frame, textvariable=magic_level)
            magic_entry.grid(column=1, row=0)
            magic_entry.config(width=4)

            resist_frame = LabelFrame(shiwin, text='Resist')
            resist_frame.grid(column=1, row=2)
            resist_menu = Combobox(resist_frame, textvariable=resist, values=list(RESIST.keys()))
            resist_menu.grid(column=0, row=0)
            resist_menu.config(width=16)
            resist_amount_menu = Combobox(resist_frame, textvariable=resist_amount, values=list(RESIST_AMOUNTS.keys()))
            resist_amount_menu.grid(column=1, row=0)
            resist_amount_menu.config(width=5)

        item = StringVar()
        item.trace('w', set_defaults)
        name = StringVar()
        name.trace('w', partial(limit_name_size, name, name_length))

        defense = StringVar()
        defense.trace('w', partial(limit_127, defense))
        protection = StringVar()
        protection.trace('w', partial(limit_127, protection))
        dexterity = StringVar()
        dexterity.trace('w', partial(limit_127, dexterity))
        stealth = StringVar()
        stealth.trace('w', partial(limit_127, stealth))
        value = StringVar()
        value.trace('w', partial(limit, value, 65535))
        aspect = IntVar()
        stat = StringVar()
        stat_amount = StringVar()
        stat_amount.trace('w', partial(limit_127, stat_amount))
        skill = StringVar()
        skill_amount = StringVar()
        skill_amount.trace('w', partial(limit_127, skill_amount))
        spell = StringVar()
        spell_level = StringVar()
        spell_level.trace('w', partial(limit, spell_level, 15))
        magic = StringVar()
        magic_level = StringVar()
        magic_level.trace('w', partial(limit, magic_level, 15))
        resist = StringVar()
        resist_amount = StringVar()

        item.set(names[0])
        build()
