from tkinter import Toplevel, StringVar, IntVar, LabelFrame, Frame, Entry, Label, Button, Radiobutton
from tkinter.ttk import Combobox

from variables import inv_EQUIPMENT_STAT, inv_SKILL_ATTRIBUTE, inv_SPELLS, inv_RESIST, inv_RESIST_AMOUNTS, \
    EQUIPMENT_STAT, SKILL_ATTRIBUTE, SPELLS, RESIST, RESIST_AMOUNTS


class ArmorShieldEdit:
    def __init__(self, filename, names, addresses, title):
        shiwin = Toplevel()
        shiwin.resizable(False, False)
        if title == 1:
            shiwin.title("Armor Edit")
        elif title == 0:
            shiwin.title("Shield Edit")
        shiwin.iconbitmap('images\icon.ico')
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

                twofivefive_stats[0].set(int(d[0] + d[1], 16))
                twofivefive_stats[1].set(int(d[2] + d[3], 16))
                dx = int(d[4] + d[5], 16)
                if dx > 127:
                    dx = dx - 256
                onetwentyseven_stats[0].set(dx)

                stealth = int(d[8] + d[9], 16)
                if stealth > 127:
                    stealth = stealth - 256
                onetwentyseven_stats[1].set(stealth)
                value.set((int(d[12] + d[13], 16) * 256) + int(d[10] + d[11], 16))

                aspect.set(d[17])
                stat.set(inv_EQUIPMENT_STAT[(d[18] + d[19]).upper()])
                stat_amount = int(d[20] + d[21], 16)
                if stat_amount > 127:
                    stat_amount = stat_amount - 256
                onetwentyseven_stats[2].set(stat_amount)
                skill_attribute.set(inv_SKILL_ATTRIBUTE[(d[22] + d[23]).upper()])
                att_amount = int(d[24] + d[25], 16)
                if att_amount > 127:
                    att_amount = att_amount - 256
                onetwentyseven_stats[3].set(att_amount)
                spell.set(inv_SPELLS[(d[26:30]).upper()])
                twofivefive_stats[2].set(int(d[30] + d[31], 16))

                magic.set(inv_SPELLS[(d[34:38]).upper()])
                twofivefive_stats[3].set(int(d[38] + d[39], 16))
                resist.set(inv_RESIST[(d[40] + d[41]).upper()])
                resist_amount.set(inv_RESIST_AMOUNTS[(d[42] + d[43]).upper()])

        def write():
            with open(filename, 'rb+') as f:
                address = addresses[names.index(item.get())]

                new_name = bytearray(name.get(), 'utf-8')
                if len(new_name) < 22:
                    while len(new_name) < 22:
                        new_name.append(0x00)
                f.seek(address)
                f.write(new_name)

                f.seek(address + 26)
                data = f.read(25)
                d = data.hex()

                new_value = value.get()
                v2, v1 = divmod(int(new_value), 256)
                if v2 == 256:
                    v2 = 255
                    v1 = 255

                new_onetwentyseven_stats = []
                for i in onetwentyseven_stats:
                    j = int(i.get())
                    if j < 0:
                        j = j + 256
                    new_onetwentyseven_stats.append(j)

                towrite = [
                    int(twofivefive_stats[0].get()),
                    int(twofivefive_stats[1].get()),
                    int(new_onetwentyseven_stats[0]),
                    int(d[6] + d[7], 16),
                    int(new_onetwentyseven_stats[1]),
                    int(v1), int(v2),
                    int(d[14] + d[15], 16),
                    aspect.get(),
                    int(EQUIPMENT_STAT[stat.get()], 16),
                    int(new_onetwentyseven_stats[2]),
                    int(SKILL_ATTRIBUTE[skill_attribute.get()], 16),
                    int(new_onetwentyseven_stats[3]),
                    int((SPELLS[spell.get()])[:2], 16),
                    int((SPELLS[spell.get()])[2:], 16),
                    int(twofivefive_stats[2].get()),
                    int(d[32] + d[33], 16),
                    int((SPELLS[magic.get()])[:2], 16),
                    int((SPELLS[magic.get()])[2:], 16),
                    int(twofivefive_stats[3].get()),
                    int(RESIST[resist.get()], 16),
                    int(RESIST_AMOUNTS[resist_amount.get()], 16)
                ]

                f.seek(address + 26)
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
            defense_entry = Entry(lawfulneutral_frame, textvariable=twofivefive_stats[0])
            defense_entry.grid(column=1, row=0, stick='e')
            defense_entry.config(width=4)

            protection_label = Label(lawfulneutral_frame, text='Protection:')
            protection_label.grid(column=0, row=1, sticky='e')
            protection_entry = Entry(lawfulneutral_frame, textvariable=twofivefive_stats[1])
            protection_entry.grid(column=1, row=1, sticky='e')
            protection_entry.config(width=4)

            dexterity_label = Label(lawfulneutral_frame, text='Dexterity:')
            dexterity_label.grid(column=0, row=2, sticky='e')
            dexterity_entry = Entry(lawfulneutral_frame, textvariable=onetwentyseven_stats[0])
            dexterity_entry.grid(column=1, row=2, sticky='e')
            dexterity_entry.config(width=4)

            stealth_label = Label(lawfulneutral_frame, text='Stealth:')
            stealth_label.grid(column=0, row=3, sticky='e')
            stealth_entry = Entry(lawfulneutral_frame, textvariable=onetwentyseven_stats[1])
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
            stat_entry = Entry(stat_frame, textvariable=onetwentyseven_stats[2])
            stat_entry.grid(column=1, row=0, sticky='e')
            stat_entry.config(width=4)

            ski_att_frame = LabelFrame(trueneutral_frame, text='Skill/Attribute')
            ski_att_frame.grid(column=0, row=1)
            ski_att_menu = Combobox(ski_att_frame, textvariable=skill_attribute, values=list(SKILL_ATTRIBUTE.keys()))
            ski_att_menu.grid(column=0, row=0)
            ski_att_menu.config(width=16)
            ski_att_amo_entry = Entry(ski_att_frame, textvariable=onetwentyseven_stats[3])
            ski_att_amo_entry.grid(column=1, row=0)
            ski_att_amo_entry.config(width=4)

            spell_frame = LabelFrame(trueneutral_frame, text='Spell')
            spell_frame.grid(column=0, row=2)
            spell_menu = Combobox(spell_frame, textvariable=spell, values=list(SPELLS.keys()))
            spell_menu.grid(column=0, row=0)
            spell_menu.config(width=16)
            spell_entry = Entry(spell_frame, textvariable=twofivefive_stats[2])
            spell_entry.grid(column=1, row=0)
            spell_entry.config(width=4)

            magic_frame = LabelFrame(trueneutral_frame, text='Magic')
            magic_frame.grid(column=0, row=3)
            magic_menu = Combobox(magic_frame, textvariable=magic, values=list(SPELLS.keys()))
            magic_menu.grid(column=0, row=0)
            magic_menu.config(width=16)
            magic_entry = Entry(magic_frame, textvariable=twofivefive_stats[3])
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

        # limits the same size
        def limit_name_size(*args):
            n = name.get()
            if len(n) > 21:
                name.set(n[:22])

        # check for max value of item
        def value_check(*args):
            val = value.get()
            if val.isnumeric():
                if int(val) > 65535:
                    value.set(65535)
                else:
                    value.set(val)
            else:
                val = ''.join(filter(str.isnumeric, val))
                value.set(val)

        # check for positive 255
        def twofivefive(*args):
            for i in twofivefive_stats:
                val = i.get()
                if not val.isnumeric():
                    val = ''.join(filter(str.isnumeric, val))
                    i.set(val)
                elif val.isnumeric():
                    if int(val) > 255:
                        i.set(255)
                    else:
                        i.set(val)

        # check for neg/pos 127
        def onetwentyseven(*args):
            for i in onetwentyseven_stats:
                val = i.get()
                if len(val) > 0 and val[0] == '-':
                    if val == '-':
                        break
                    else:
                        val = val[1:]
                    if not val.isnumeric():
                        val = ''.join(filter(str.isnumeric, val))
                        i.set(int(val) * -1)
                    elif val.isnumeric():
                        if int(val) > 127:
                            i.set('-127')
                        else:
                            i.set(int(val) * -1)
                else:
                    if not val.isnumeric():
                        val = ''.join(filter(str.isnumeric, val))
                        i.set(val)
                    elif val.isnumeric():
                        if int(val) > 127:
                            i.set(127)
                        else:
                            i.set(val)

        item = StringVar()
        item.trace('w', set_defaults)
        name = StringVar()
        name.trace('w', limit_name_size)

        # group of stats:
        # defense, protection, spell_level, magic_level
        # grouped to make it easier to run a 255 check
        twofivefive_stats = []
        for i in range(4):
            i = StringVar()
            i.trace('w', twofivefive)
            twofivefive_stats.append(i)

        # dexterity, stealth, stat_amount, skill_attribute_amount
        # grouped to make it easier to run a neg/pos 127 check
        onetwentyseven_stats = []
        for i in range(4):
            i = StringVar()
            i.trace('w', onetwentyseven)
            onetwentyseven_stats.append(i)

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
