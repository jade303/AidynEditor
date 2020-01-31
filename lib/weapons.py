from functools import partial
from tkinter import Toplevel, Frame, LabelFrame, Entry, Label, Button, Radiobutton, StringVar, IntVar
from tkinter.ttk import Combobox

from lib.limits import limit_name_size, limit, limit_127
from lib.variables import WEAPON_ADDRESSES, WEAPON_NAMES, inv_WEAPON_TYPE, inv_WEAPON_ANIMATIONS, inv_EQUIPMENT_STAT, \
    inv_SKILL_ATTRIBUTE, inv_SPELLS, inv_RESIST, inv_RESIST_AMOUNTS, WEAPON_TYPE, WEAPON_ANIMATIONS, EQUIPMENT_STAT, \
    SKILL_ATTRIBUTE, SPELLS, RESIST, RESIST_AMOUNTS


class WeaponEdit:
    def __init__(self, filename, icon_dir):
        weapwin = Toplevel()
        weapwin.resizable(False, False)
        weapwin.title('Weapon Edit')
        weapwin.iconbitmap(icon_dir)
        filename = filename
        data_seek = 23
        data_read = 25
        name_length = 21

        def set_defaults(*args):
            with open(filename, 'rb') as f:
                address = WEAPON_ADDRESSES[WEAPON_NAMES.index(weapon.get())]
                f.seek(address)
                name.set(f.read(name_length).decode("utf-8"))

                f.seek(address + data_seek)
                data = f.read(data_read)
                d = data.hex()

                weapon_type.set(inv_WEAPON_TYPE[d[1].upper()])
                str_req.set(int(d[2] + d[3], 16))
                hit.set(int(d[4] + d[5], 16))
                damage.set(int(d[6] + d[7], 16))
                value.set((int(d[10] + d[11], 16) * 256) + int(d[8] + d[9], 16))
                weapon_range.set(int(d[14] + d[15], 16))
                animation.set(inv_WEAPON_ANIMATIONS[d[16] + d[17].upper()])
                aspect.set(d[23])

                stat.set(inv_EQUIPMENT_STAT[(d[24] + d[25]).upper()])
                st = int(d[26] + d[27], 16)
                if st > 127:
                    st = st - 256
                stat_amount.set(st)

                skill.set(inv_SKILL_ATTRIBUTE[(d[28] + d[29]).upper()])
                att_amount = int(d[30] + d[31], 16)
                if att_amount > 127:
                    att_amount = att_amount - 256
                skill_amount.set(att_amount)

                spell.set(inv_SPELLS[(d[32:36]).upper()])
                spell_level.set(int(d[36] + d[37], 16))

                magic.set(inv_SPELLS[(d[40:44]).upper()])
                magic_level.set(int(d[44] + d[45], 16))

                resist.set(inv_RESIST[(d[46] + d[47]).upper()])
                resist_amount.set(inv_RESIST_AMOUNTS[(d[48] + d[49]).upper()])

        def write():
            with open(filename, 'rb+') as f:
                address = WEAPON_ADDRESSES[WEAPON_NAMES.index(weapon.get())]
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

                st = int(stat_amount.get())
                if st < 0:
                    st = st + 256

                sk = int(skill_amount.get())
                if sk < 0:
                    sk = sk + 256

                towrite = [
                    int(WEAPON_TYPE[weapon_type.get()], 16),
                    int(str_req.get()),
                    int(hit.get()),
                    int(damage.get()),
                    int(v1), int(v2),
                    int(d[12] + d[13], 16),
                    int(weapon_range.get()),
                    int(WEAPON_ANIMATIONS[animation.get()], 16),
                    int(d[18] + d[19], 16), int(d[20] + d[21], 16),
                    aspect.get(),
                    int(EQUIPMENT_STAT[stat.get()], 16),
                    int(st),
                    int(SKILL_ATTRIBUTE[skill.get()], 16),
                    int(sk),
                    int((SPELLS[spell.get()])[:2], 16),
                    int((SPELLS[spell.get()])[2:], 16),
                    int(spell_level.get()),
                    int(d[38] + d[39], 16),
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
            lawfulgood_frame = Frame(weapwin)
            lawfulgood_frame.grid(column=0, row=0)
            default_weapon_menu = Combobox(lawfulgood_frame, textvariable=weapon, values=WEAPON_NAMES)
            default_weapon_menu.grid(column=0, row=0)
            default_weapon_menu.config(width=21)

            new_name_label = LabelFrame(lawfulgood_frame, text='New Name')
            new_name_label.grid(column=0, row=1)
            new_name_entry = Entry(new_name_label, textvariable=name)
            new_name_entry.grid()
            new_name_entry.config(width=21)

            weapon_type_menu = Combobox(lawfulgood_frame, textvariable=weapon_type, values=list(WEAPON_TYPE.keys()))
            weapon_type_menu.grid(column=0, row=3)
            weapon_type_menu.config(width=9)

            lawfulneutral_frame = LabelFrame(weapwin, text='Stats:')
            lawfulneutral_frame.grid(column=0, row=1)

            strength_label = Label(lawfulneutral_frame, text='Str Required:')
            strength_label.grid(column=0, row=0, sticky='e')
            strength_entry = Entry(lawfulneutral_frame, textvariable=str_req)
            strength_entry.grid(column=1, row=0, stick='e')
            strength_entry.config(width=4)

            hit_label = Label(lawfulneutral_frame, text='Hit:')
            hit_label.grid(column=0, row=1, sticky='e')
            hit_entry = Entry(lawfulneutral_frame, textvariable=hit)
            hit_entry.grid(column=1, row=1, sticky='e')
            hit_entry.config(width=4)

            damage_label = Label(lawfulneutral_frame, text='Damage:')
            damage_label.grid(column=0, row=2, sticky='e')
            damage_entry = Entry(lawfulneutral_frame, textvariable=damage)
            damage_entry.grid(column=1, row=2, sticky='e')
            damage_entry.config(width=4)

            range_label = Label(lawfulneutral_frame, text='Range:')
            range_label.grid(column=0, row=3, sticky='e')
            range_entry = Entry(lawfulneutral_frame, textvariable=weapon_range)
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
            animation_menu = Combobox(animation_frame, textvariable=animation, values=list(WEAPON_ANIMATIONS.keys()))
            animation_menu.grid(column=0, row=0)
            animation_menu.config(width=12)

            neutralgood_frame = Frame(weapwin)
            neutralgood_frame.grid(column=1, row=0)

            save = Button(neutralgood_frame, text='Save', command=write)
            save.grid(column=0, row=0)
            save.config(width=8)

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

            resist_frame = LabelFrame(weapwin, text='Resist')
            resist_frame.grid(column=1, row=2)
            resist_menu = Combobox(resist_frame, textvariable=resist, values=list(RESIST.keys()))
            resist_menu.grid(column=0, row=0)
            resist_menu.config(width=16)
            resist_amount_menu = Combobox(resist_frame, textvariable=resist_amount, values=list(RESIST_AMOUNTS.keys()))
            resist_amount_menu.grid(column=1, row=0)
            resist_amount_menu.config(width=5)

        weapon = StringVar()
        weapon.trace('w', set_defaults)
        name = StringVar()
        name.trace('w', partial(limit_name_size, name, name_length))

        str_req = StringVar()
        str_req.trace('w', partial(limit, str_req, 30))
        hit = StringVar()
        hit.trace('w', partial(limit, hit, 255))
        damage = StringVar()
        damage.trace('w', partial(limit, damage, 255))
        weapon_range = StringVar()
        weapon_range.trace('w', partial(limit, weapon_range, 255))
        weapon_type = StringVar()
        value = StringVar()
        value.trace('w', partial(limit, value, 65535))
        animation = StringVar()
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

        weapon.set(WEAPON_NAMES[0])
        build()
