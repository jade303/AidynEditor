from functools import partial
from tkinter import Toplevel, StringVar, IntVar, Frame, LabelFrame, Entry, Label, Button, Radiobutton
from tkinter.ttk import Combobox

from variables import ACCESSORY_NAMES, ACCESSORY_ADDRESSES, inv_EQUIPMENT_STAT, inv_SKILL_ATTRIBUTE, inv_SPELLS, \
    inv_RESIST, inv_RESIST_AMOUNTS, EQUIPMENT_STAT, SKILL_ATTRIBUTE, SPELLS, RESIST, RESIST_AMOUNTS


class AccessoryEdit:
    def __init__(self, filename):
        accesswin = Toplevel()
        accesswin.resizable(False, False)
        accesswin.title("Accessory Edit")
        accesswin.iconbitmap('images\icon.ico')
        filename = filename

        def set_defaults(*args):
            with open(filename, 'rb') as f:
                address = ACCESSORY_ADDRESSES[ACCESSORY_NAMES.index(item.get())]
                f.seek(address)
                name.set(f.read(20).decode("utf-8"))

                f.seek(address + 24)
                data = f.read(20)
                d = data.hex()

                damage.set(int(d[0] + d[1], 16))
                protection.set(int(d[2] + d[3], 16))
                str_req.set(int(d[4] + d[5], 16))
                int_req.set(int(d[6] + d[7], 16))
                value.set((int(d[10] + d[11], 16) * 256) + int(d[8] + d[9], 16))
                aspect.set(d[13])
                stat.set(inv_EQUIPMENT_STAT[(d[14] + d[15]).upper()])
                amount_stat = int(d[16] + d[17], 16)
                if amount_stat > 127:
                    amount_stat = amount_stat - 256
                stat_amount.set(amount_stat)
                skill.set(inv_SKILL_ATTRIBUTE[(d[18] + d[19]).upper()])
                att_amount = int(d[20] + d[21], 16)
                if att_amount > 127:
                    att_amount = att_amount - 256
                skill_amount.set(att_amount)
                spell.set(inv_SPELLS[(d[22:26]).upper()])
                spell_level.set(int(d[26] + d[27], 16))

                magic.set(inv_SPELLS[(d[30:34]).upper()])
                magic_level.set(int(d[34] + d[35], 16))
                resist.set(inv_RESIST[(d[36] + d[37]).upper()])
                resist_amount.set(inv_RESIST_AMOUNTS[(d[38] + d[39]).upper()])

        def write():
            with open(filename, 'rb+') as f:
                address = ACCESSORY_ADDRESSES[ACCESSORY_NAMES.index(item.get())]

                new_name = bytearray(name.get(), 'utf-8')
                if len(new_name) < 20:
                    while len(new_name) < 20:
                        new_name.append(0x00)
                f.seek(address)
                f.write(new_name)

                f.seek(address + 24)
                data = f.read(20)
                d = data.hex()

                new_value = value.get()
                v2, v1 = divmod(int(new_value), 256)
                if v2 == 256:
                    v2 = 255
                    v1 = 255

                st = int(stat_amount.get())
                if st < 0:
                    st = st + 256

                sk = int(skill_amount.get())
                if sk < 0:
                    sk = sk + 256

                towrite = [
                    int(damage.get()),
                    int(protection.get()),
                    int(str_req.get()),
                    int(int_req.get()),
                    int(v1), int(v2),
                    aspect.get(),
                    int(EQUIPMENT_STAT[stat.get()], 16),
                    int(st),
                    int(SKILL_ATTRIBUTE[skill.get()], 16),
                    int(sk),
                    int((SPELLS[spell.get()])[:2], 16),
                    int((SPELLS[spell.get()])[2:], 16),
                    int(spell_level.get()),
                    int(d[28] + d[29], 16),
                    int((SPELLS[magic.get()])[:2], 16),
                    int((SPELLS[magic.get()])[2:], 16),
                    int(magic_level.get()),
                    int(RESIST[resist.get()], 16),
                    int(RESIST_AMOUNTS[resist_amount.get()], 16)
                ]

                f.seek(address + 24)
                for i in towrite:
                    f.write(i.to_bytes(1, byteorder='big'))

        def build():
            lawfulgood_frame = Frame(accesswin)
            lawfulgood_frame.grid(column=0, row=0)
            default_item_menu = Combobox(lawfulgood_frame, textvariable=item, values=ACCESSORY_NAMES)
            default_item_menu.grid(column=0, row=0)
            default_item_menu.config(width=21)

            new_name_label = LabelFrame(lawfulgood_frame, text='New Name')
            new_name_label.grid(column=0, row=1)
            new_name_entry = Entry(new_name_label, textvariable=name)
            new_name_entry.grid()
            new_name_entry.config(width=21)

            lawfulneutral_frame = LabelFrame(accesswin, text='Stats:')
            lawfulneutral_frame.grid(column=0, row=1)

            defense_label = Label(lawfulneutral_frame, text='Damage:')
            defense_label.grid(column=0, row=0, sticky='e')
            defense_entry = Entry(lawfulneutral_frame, textvariable=damage)
            defense_entry.grid(column=1, row=0, stick='e')
            defense_entry.config(width=4)

            protection_label = Label(lawfulneutral_frame, text='Protection:')
            protection_label.grid(column=0, row=1, sticky='e')
            protection_entry = Entry(lawfulneutral_frame, textvariable=protection)
            protection_entry.grid(column=1, row=1, sticky='e')
            protection_entry.config(width=4)

            dexterity_label = Label(lawfulneutral_frame, text='Strength Required:')
            dexterity_label.grid(column=0, row=2, sticky='e')
            dexterity_entry = Entry(lawfulneutral_frame, textvariable=str_req)
            dexterity_entry.grid(column=1, row=2, sticky='e')
            dexterity_entry.config(width=4)

            stealth_label = Label(lawfulneutral_frame, text='Intelligence Required:')
            stealth_label.grid(column=0, row=3, sticky='e')
            stealth_entry = Entry(lawfulneutral_frame, textvariable=int_req)
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

            neutralgood_frame = Frame(accesswin)
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

            trueneutral_frame = Frame(accesswin)
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

            resist_frame = LabelFrame(accesswin, text='Resist')
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
            if len(n) > 20:
                name.set(n[:21])

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
        def twofivefive(i, *args):
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
        def onetwentyseven(i, *args):
            val = i.get()
            if len(val) > 0 and val[0] == '-':
                if val == '-':
                    return
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

        # sets limit of 15
        def fifteen(i, *args):
            val = i.get()
            if not val.isnumeric():
                val = ''.join(filter(str.isnumeric, val))
                i.set(val)
            elif val.isnumeric():
                if int(val) > 15:
                    i.set(15)
                else:
                    i.set(val)

        item = StringVar()
        item.trace('w', set_defaults)
        name = StringVar()
        name.trace('w', limit_name_size)

        damage = StringVar()
        damage.trace('w', partial(twofivefive, damage))
        protection = StringVar()
        protection.trace('w', partial(twofivefive, protection))
        str_req = StringVar()
        str_req.trace('w', partial(twofivefive, str_req))
        int_req = StringVar()
        int_req.trace('w', partial(twofivefive, int_req))
        value = StringVar()
        value.trace('w', value_check)
        aspect = IntVar()
        stat = StringVar()
        stat_amount = StringVar()
        stat_amount.trace('w', partial(onetwentyseven, stat_amount))
        skill = StringVar()
        skill_amount = StringVar()
        skill_amount.trace('w', partial(onetwentyseven, skill_amount))
        spell = StringVar()
        spell_level = StringVar()
        spell_level.trace('w', partial(fifteen, spell_level))
        magic = StringVar()
        magic_level = StringVar()
        magic_level.trace('w', partial(fifteen, magic_level))
        resist = StringVar()
        resist_amount = StringVar()

        item.set(ACCESSORY_NAMES[0])
        build()
