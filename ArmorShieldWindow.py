from tkinter import Toplevel, StringVar, IntVar, OptionMenu, LabelFrame, Frame, Entry, Label, Button, Radiobutton

from variables import inv_EQUIPMENT_STAT, inv_SKILL_ATTRIBUTE, inv_SPELLS, inv_RESIST, inv_RESIST_AMOUNTS, \
    EQUIPMENT_STAT, SKILL_ATTRIBUTE, SPELLS, RESIST, RESIST_AMOUNTS


class ArmorShieldEdit:
    def __init__(self, filename, names, addresses):
        shiwin = Toplevel()
        shiwin.title("Armor and Shield Edit")
        filename = filename
        names = names
        addresses = addresses

        def set_defaults(*args):
            with open(filename, 'rb') as f:
                address = addresses[names.index(item.get())]
                f.seek(address)
                name.set(f.read(22).decode("utf-8"))

                f.seek(address + 26)
                data = f.read(22)
                d = data.hex()

                pos_stats[0].set(int(d[0] + d[1], 16))
                pos_stats[1].set(int(d[2] + d[3], 16))
                dx = int(d[4] + d[5], 16)
                if dx > 127:
                    dx = dx - 256
                neg_stats[0].set(str(dx))

                st = int(d[8] + d[9], 16)
                if st > 127:
                    st = st - 256
                neg_stats[1].set(str(st))
                value.set((int(d[12] + d[13], 16) * 256) + int(d[10] + d[11], 16))

                aspect.set(d[17])
                stat.set(inv_EQUIPMENT_STAT[(d[18] + d[19]).upper()])
                pos_stats[2].set(int(d[20] + d[21], 16))
                skill_attribute.set(inv_SKILL_ATTRIBUTE[(d[22] + d[23]).upper()])
                pos_stats[3].set(int(d[24] + d[25], 16))
                spell.set(inv_SPELLS[(d[26:30]).upper()])
                pos_stats[4].set(int(d[30] + d[31], 16))

                magic.set(inv_SPELLS[(d[34:38]).upper()])
                pos_stats[5].set(int(d[38] + d[39], 16))
                resist.set(inv_RESIST[(d[40] + d[41]).upper()])
                resist_amount.set(inv_RESIST_AMOUNTS[(d[42] + d[43]).upper()])

        def write():
            # 6/7 14/15 32/33
            pass

        def build():
            lawfulgood_frame = Frame(shiwin)
            lawfulgood_frame.grid(column=0, row=0)
            default_item_menu = OptionMenu(lawfulgood_frame, item, *names)
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
            defense_entry = Entry(lawfulneutral_frame, textvariable=pos_stats[0])
            defense_entry.grid(column=1, row=0, stick='e')
            defense_entry.config(width=4)

            protection_label = Label(lawfulneutral_frame, text='Protection:')
            protection_label.grid(column=0, row=1, sticky='e')
            protection_entry = Entry(lawfulneutral_frame, textvariable=pos_stats[1])
            protection_entry.grid(column=1, row=1, sticky='e')
            protection_entry.config(width=4)

            dexterity_label = Label(lawfulneutral_frame, text='Dexterity:')
            dexterity_label.grid(column=0, row=2, sticky='e')
            dexterity_entry = Entry(lawfulneutral_frame, textvariable=neg_stats[0])
            dexterity_entry.grid(column=1, row=2, sticky='e')
            dexterity_entry.config(width=4)

            stealth_label = Label(lawfulneutral_frame, text='Stealth:')
            stealth_label.grid(column=0, row=3, sticky='e')
            stealth_entry = Entry(lawfulneutral_frame, textvariable=neg_stats[1])
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
            stat_menu = OptionMenu(stat_frame, stat, *EQUIPMENT_STAT)
            stat_menu.grid(column=0, row=0)
            stat_menu.config(width=16)
            stat_entry = Entry(stat_frame, textvariable=pos_stats[2])
            stat_entry.grid(column=1, row=0, sticky='e')
            stat_entry.config(width=4)

            ski_att_frame = LabelFrame(trueneutral_frame, text='Skill/Attribute')
            ski_att_frame.grid(column=0, row=1)
            ski_att_menu = OptionMenu(ski_att_frame, skill_attribute, *SKILL_ATTRIBUTE)
            ski_att_menu.grid(column=0, row=0)
            ski_att_menu.config(width=16)
            ski_att_amo_entry = Entry(ski_att_frame, textvariable=pos_stats[3])
            ski_att_amo_entry.grid(column=1, row=0)
            ski_att_amo_entry.config(width=4)

            spell_frame = LabelFrame(trueneutral_frame, text='Spell')
            spell_frame.grid(column=0, row=2)
            spell_menu = OptionMenu(spell_frame, spell, *SPELLS)
            spell_menu.grid(column=0, row=0)
            spell_menu.config(width=16)
            spell_entry = Entry(spell_frame, textvariable=pos_stats[4])
            spell_entry.grid(column=1, row=0)
            spell_entry.config(width=4)

            magic_frame = LabelFrame(trueneutral_frame, text='Magic')
            magic_frame.grid(column=0, row=3)
            magic_menu = OptionMenu(magic_frame, magic, *SPELLS)
            magic_menu.grid(column=0, row=0)
            magic_menu.config(width=16)
            magic_entry = Entry(magic_frame, textvariable=pos_stats[5])
            magic_entry.grid(column=1, row=0)
            magic_entry.config(width=4)

            resist_frame = LabelFrame(shiwin, text='Resist')
            resist_frame.grid(column=1, row=2)
            resist_menu = OptionMenu(resist_frame, resist, *RESIST)
            resist_menu.grid(column=0, row=0)
            resist_menu.config(width=16)
            resist_amount_menu = OptionMenu(resist_frame, resist_amount, *RESIST_AMOUNTS)
            resist_amount_menu.grid(column=1, row=0)
            resist_amount_menu.config(width=4)

        def limit_name_size(*args):
            n = name.get()
            if len(n) > 21:
                name.set(n[:22])

        def pos_check(*args):
            for i in pos_stats:
                val = i.get()
                if val.isnumeric():
                    if int(val) > 255:
                        i.set(255)
                    else:
                        i.set(val)
                else:
                    i.set('')

        def neg_check(*args):
            for i in neg_stats:
                val = i.get()
                if val[0] == '-':
                    sign = -1
                    if val[1:].isnumeric():
                        if int(val[1:]) > 127:
                            i.set(-127)
                        else:
                            i.set(val)
                    else:
                        i.set('')
                else:
                    sign = 1
                if val.isnumeric():
                    if int(val) > 127:
                        i.set(127)
                    else:
                        i.set(val)
                else:
                    i.set('')

        def value_check(*args):
            val = value.get()
            if val.isnumeric():
                if int(val) > 65535:
                    value.set(65535)
                else:
                    value.set(val)
            else:
                value.set('')

        item = StringVar()
        item.trace('w', set_defaults)
        name = StringVar()
        name.trace('w', limit_name_size)

        # defense, protection, stat_amount, skill_attribute_amount, spell_level, magic_level
        pos_stats = []
        for i in range(6):
            i = StringVar()
            i.trace('w', pos_check)
            pos_stats.append(i)

        # dexterity, stealth
        neg_stats = []
        for i in range(2):
            i = StringVar()
            i.trace('w', neg_check)
            neg_stats.append(i)

        value = StringVar()
        value.trace('w', value_check)
        aspect = IntVar()
        stat = StringVar()
        skill_attribute = StringVar()
        spell = StringVar()
        magic = StringVar()
        resist = StringVar()
        resist_amount = StringVar()

        item.set(names[0])
        build()
