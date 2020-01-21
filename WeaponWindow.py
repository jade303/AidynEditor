from tkinter import Toplevel, Frame, LabelFrame, Entry, OptionMenu, Label, Button, Radiobutton, StringVar, IntVar
from variables import WEAPON_NAMES, WEAPON_ADDRESSES, WEAPON_TYPE, inv_WEAPON_TYPE, \
    WEAPON_ANIMATIONS, inv_WEAPON_ANIMATIONS, EQUIPMENT_STAT, inv_EQUIPMENT_STAT, \
    SKILL_ATTRIBUTE, inv_SKILL_ATTRIBUTE, SPELLS, inv_SPELLS, \
    RESIST, inv_RESIST, RESIST_AMOUNTS, inv_RESIST_AMOUNTS


class WeaponEdit:
    def __init__(self, filename):
        weapwin = Toplevel()
        weapwin.title('Weapon Edit')
        filename = filename

        def set_defaults(*args):
            with open(filename, 'rb') as f:
                address = WEAPON_ADDRESSES[WEAPON_NAMES.index(weapon.get())]
                f.seek(address)
                name.set(f.read(21).decode("utf-8"))

                f.seek(address + 23)
                data = f.read(25)
                d = data.hex()

                weapon_type.set(inv_WEAPON_TYPE[d[1].upper()])
                twofivefive_stats[0].set(int(d[2] + d[3], 16))
                twofivefive_stats[1].set(int(d[4] + d[5], 16))
                twofivefive_stats[2].set(int(d[6] + d[7], 16))
                value.set((int(d[10] + d[11], 16) * 256) + int(d[8] + d[9], 16))
                twofivefive_stats[3].set(int(d[14] + d[15], 16))
                animation.set(inv_WEAPON_ANIMATIONS[d[16] + d[17].upper()])
                aspect.set(d[23])

                stat.set(inv_EQUIPMENT_STAT[(d[24] + d[25]).upper()])
                stat_amount = int(d[26] + d[27], 16)
                if stat_amount > 127:
                    stat_amount = stat_amount - 256
                onetwentyseven_stats[0].set(stat_amount)

                skill_attribute.set(inv_SKILL_ATTRIBUTE[(d[28] + d[29]).upper()])
                att_amount = int(d[30] + d[31], 16)
                if att_amount > 127:
                    att_amount = att_amount - 256
                onetwentyseven_stats[1].set(att_amount)

                spell.set(inv_SPELLS[(d[32:36]).upper()])
                twofivefive_stats[4].set(int(d[36] + d[37], 16))

                magic.set(inv_SPELLS[(d[40:44]).upper()])
                twofivefive_stats[5].set(int(d[44] + d[45], 16))

                resist.set(inv_RESIST[(d[46] + d[47]).upper()])
                resist_amount.set(inv_RESIST_AMOUNTS[(d[48] + d[49]).upper()])

        def write():
            with open(filename, 'rb+') as f:
                address = WEAPON_ADDRESSES[WEAPON_NAMES.index(weapon.get())]
                new_name = bytearray(name.get(), 'utf-8')
                if len(new_name) < 21:
                    while len(new_name) < 21:
                        new_name.append(0x00)
                f.seek(address)
                f.write(new_name)

                f.seek(address + 23)
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
                    int(WEAPON_TYPE[weapon_type.get()], 16),
                    int(twofivefive_stats[0].get()),
                    int(twofivefive_stats[1].get()),
                    int(twofivefive_stats[2].get()),
                    int(v1), int(v2),
                    int(d[12] + d[13], 16),
                    int(twofivefive_stats[3].get()),
                    int(WEAPON_ANIMATIONS[animation.get()], 16),
                    int(d[18] + d[19], 16), int(d[20] + d[21], 16),
                    aspect.get(),
                    int(EQUIPMENT_STAT[stat.get()], 16),
                    int(new_onetwentyseven_stats[0]),
                    int(SKILL_ATTRIBUTE[skill_attribute.get()], 16),
                    int(new_onetwentyseven_stats[1]),
                    int((SPELLS[spell.get()])[:2], 16),
                    int((SPELLS[spell.get()])[2:], 16),
                    int(twofivefive_stats[4].get()),
                    int(d[38] + d[39], 16),
                    int((SPELLS[magic.get()])[:2], 16),
                    int((SPELLS[magic.get()])[2:], 16),
                    int(twofivefive_stats[5].get()),
                    int(RESIST[resist.get()], 16),
                    int(RESIST_AMOUNTS[resist_amount.get()], 16)
                ]

                f.seek(address + 23)
                for i in towrite:
                    f.write(i.to_bytes(1, byteorder='big'))

        def build():
            lawfulgood_frame = Frame(weapwin)
            lawfulgood_frame.grid(column=0, row=0)
            default_weapon_menu = OptionMenu(lawfulgood_frame, weapon, *WEAPON_NAMES)
            default_weapon_menu.grid(column=0, row=0)
            default_weapon_menu.config(width=21)

            new_name_label = LabelFrame(lawfulgood_frame, text='New Name')
            new_name_label.grid(column=0, row=1)
            new_name_entry = Entry(new_name_label, textvariable=name)
            new_name_entry.grid()
            new_name_entry.config(width=21)

            weapon_type_menu = OptionMenu(lawfulgood_frame, weapon_type, *WEAPON_TYPE)
            weapon_type_menu.grid(column=0, row=3)
            weapon_type_menu.config(width=9)

            lawfulneutral_frame = LabelFrame(weapwin, text='Stats:')
            lawfulneutral_frame.grid(column=0, row=1)

            strength_label = Label(lawfulneutral_frame, text='Str Required:')
            strength_label.grid(column=0, row=0, sticky='e')
            strength_entry = Entry(lawfulneutral_frame, textvariable=twofivefive_stats[0])
            strength_entry.grid(column=1, row=0, stick='e')
            strength_entry.config(width=4)

            hit_label = Label(lawfulneutral_frame, text='Hit:')
            hit_label.grid(column=0, row=1, sticky='e')
            hit_entry = Entry(lawfulneutral_frame, textvariable=twofivefive_stats[1])
            hit_entry.grid(column=1, row=1, sticky='e')
            hit_entry.config(width=4)

            damage_label = Label(lawfulneutral_frame, text='Damage:')
            damage_label.grid(column=0, row=2, sticky='e')
            damage_entry = Entry(lawfulneutral_frame, textvariable=twofivefive_stats[2])
            damage_entry.grid(column=1, row=2, sticky='e')
            damage_entry.config(width=4)

            range_label = Label(lawfulneutral_frame, text='Range:')
            range_label.grid(column=0, row=3, sticky='e')
            range_entry = Entry(lawfulneutral_frame, textvariable=twofivefive_stats[3])
            range_entry.grid(column=1, row=3, sticky='e')
            range_entry.config(width=4)

            value_label = Label(lawfulneutral_frame, text='Base Value:')
            value_label.grid(column=0, row=4, sticky='e')
            value_entry = Entry(lawfulneutral_frame, textvariable=value)
            value_entry.grid(column=1, row=4, sticky='e')
            value_entry.config(width=6)
            value_label2 = Label(lawfulneutral_frame, text='Max base value: 65535')
            value_label2.grid(row=5, columnspan=2)
            value_label2.config(font=(None, 8))

            animation_frame = LabelFrame(weapwin, text='Animation')
            animation_frame.grid(column=0, row=2)
            animation_menu = OptionMenu(animation_frame, animation, *WEAPON_ANIMATIONS)
            animation_menu.grid(column=0, row=0)
            animation_menu.config(width=12)

            neutralgood_frame = Frame(weapwin)
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

            trueneutral_frame = Frame(weapwin)
            trueneutral_frame.grid(column=1, row=1)

            stat_frame = LabelFrame(trueneutral_frame, text='Stat')
            stat_frame.grid(column=0, row=0)
            stat_menu = OptionMenu(stat_frame, stat, *EQUIPMENT_STAT)
            stat_menu.grid(column=0, row=0)
            stat_menu.config(width=16)
            stat_entry = Entry(stat_frame, textvariable=onetwentyseven_stats[0])
            stat_entry.grid(column=1, row=0, sticky='e')
            stat_entry.config(width=4)

            ski_att_frame = LabelFrame(trueneutral_frame, text='Skill/Attribute')
            ski_att_frame.grid(column=0, row=1)
            ski_att_menu = OptionMenu(ski_att_frame, skill_attribute, *SKILL_ATTRIBUTE)
            ski_att_menu.grid(column=0, row=0)
            ski_att_menu.config(width=16)
            ski_att_amo_entry = Entry(ski_att_frame, textvariable=onetwentyseven_stats[1])
            ski_att_amo_entry.grid(column=1, row=0)
            ski_att_amo_entry.config(width=4)

            spell_frame = LabelFrame(trueneutral_frame, text='Spell')
            spell_frame.grid(column=0, row=2)
            spell_menu = OptionMenu(spell_frame, spell, *SPELLS)
            spell_menu.grid(column=0, row=0)
            spell_menu.config(width=16)
            spell_entry = Entry(spell_frame, textvariable=twofivefive_stats[4])
            spell_entry.grid(column=1, row=0)
            spell_entry.config(width=4)

            magic_frame = LabelFrame(trueneutral_frame, text='Magic')
            magic_frame.grid(column=0, row=3)
            magic_menu = OptionMenu(magic_frame, magic, *SPELLS)
            magic_menu.grid(column=0, row=0)
            magic_menu.config(width=16)
            magic_entry = Entry(magic_frame, textvariable=twofivefive_stats[5])
            magic_entry.grid(column=1, row=0)
            magic_entry.config(width=4)

            resist_frame = LabelFrame(weapwin, text='Resist')
            resist_frame.grid(column=1, row=2)
            resist_menu = OptionMenu(resist_frame, resist, *RESIST)
            resist_menu.grid(column=0, row=0)
            resist_menu.config(width=16)
            resist_amount_menu = OptionMenu(resist_frame, resist_amount, *RESIST_AMOUNTS)
            resist_amount_menu.grid(column=1, row=0)
            resist_amount_menu.config(width=4)

        # limits the same size
        def limit_name_size(*args):
            n = name.get()
            if len(n) > 21:
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

        # check for 127
        def onetwentyseven(*args):
            for i in onetwentyseven_stats:
                val = i.get()
                if not val.isnumeric():
                    val = ''.join(filter(str.isnumeric, val))
                    i.set(val)
                elif val.isnumeric():
                    if int(val) > 255:
                        i.set(255)
                    else:
                        i.set(val)

        weapon = StringVar()
        weapon.trace('w', set_defaults)
        name = StringVar()
        name.trace('w', limit_name_size)

        # group of stats:
        # strength, hit, damage, weapon range, spell level, magic level
        # grouped to make it easier to run a 255 check
        twofivefive_stats = []
        for i in range(6):
            i = StringVar()
            i.trace('w', twofivefive)
            twofivefive_stats.append(i)

        # group of stats:
        # stat amount, skill attribute amount
        onetwentyseven_stats = []
        for i in range(2):
            i = StringVar()
            i.trace('w', onetwentyseven)
            onetwentyseven_stats.append(i)

        weapon_type = StringVar()
        value = StringVar()
        value.trace('w', value_check)
        animation = StringVar()
        aspect = IntVar()
        stat = StringVar()
        skill_attribute = StringVar()
        spell = StringVar()
        magic = StringVar()
        resist = StringVar()
        resist_amount = StringVar()

        weapon.set(WEAPON_NAMES[28])
        build()
