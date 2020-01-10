from tkinter import *
from variables import *


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
                strength.set(int(d[2] + d[3], 16))
                hit.set(int(d[4] + d[5], 16))
                damage.set(int(d[6] + d[7], 16))
                value.set((int(d[10] + d[11], 16) * 256) + int(d[8] + d[9], 16))
                weapon_range.set(int(d[14] + d[15], 16))
                animation.set(inv_WEAPON_ANIMATIONS[d[16] + d[17].upper()])
                aspect.set(d[23])

                stat.set(inv_EQUIPMENT_STAT[(d[24] + d[25]).upper()])
                stat_amount.set(int(d[26] + d[27], 16))

                skill_attribute.set(inv_SKILL_ATTRIBUTE[(d[28] + d[29]).upper()])
                skill_attribute_amount.set(int(d[30] + d[31], 16))

                spell.set(inv_EQUIPMENT_SPELLS_MAGIC[(d[32:36]).upper()])
                spell_level.set(int(d[36] + d[37], 16))

                magic.set(inv_EQUIPMENT_SPELLS_MAGIC[(d[40:44]).upper()])
                magic_level.set(int(d[44] + d[45], 16))

                resist.set(inv_RESIST[(d[46] + d[47]).upper()])
                resist_amount.set(inv_RESIST_AMOUNTS[(d[48] + d[49]).upper()])

        def write():
            with open(filename, 'rb+') as f:
                address = WEAPON_ADDRESSES[WEAPON_NAMES.index(weapon.get())]
                new_name = name.get()
                if len(new_name) > 21:
                    new_name = bytes(new_name[:22], 'utf-8')
                if len(new_name) < 21:
                    new_name = bytearray(new_name, 'utf-8')
                    while len(new_name) < 21:
                        new_name.append(0x00)
                f.seek(address)
                f.write(new_name.encode('utf-8'))

                f.seek(address + 23)
                data = f.read(25)
                d = data.hex()

                new_value = value.get()
                v2, v1 = divmod(new_value, 256)
                if v2 == 256:
                    v2 = 255
                    v1 = 255

                towrite = [
                    int(WEAPON_TYPE[weapon_type.get()], 16), strength.get(), hit.get(), damage.get(), v1, v2,
                    int(d[12] + d[13], 16), weapon_range.get(), int(WEAPON_ANIMATIONS[animation.get()], 16),
                    int(d[18] + d[19], 16), int(d[20] + d[21], 16), aspect.get(),
                    int(EQUIPMENT_STAT[stat.get()], 16), int(stat_amount.get()),
                    int(SKILL_ATTRIBUTE[skill_attribute.get()], 16), skill_attribute_amount.get(),
                    int((EQUIPMENT_SPELLS_MAGIC[spell.get()])[:2], 16),
                    int((EQUIPMENT_SPELLS_MAGIC[spell.get()])[2:], 16),
                    spell_level.get(), int(d[38] + d[39], 16), int((EQUIPMENT_SPELLS_MAGIC[magic.get()])[:2], 16),
                    int((EQUIPMENT_SPELLS_MAGIC[magic.get()])[2:], 16), magic_level.get(),
                    int(RESIST[resist.get()], 16), int(RESIST_AMOUNTS[resist_amount.get()], 16)
                ]

                f.seek(address + 23)
                for item in towrite:
                    f.write(item.to_bytes(1, byteorder='big'))

        def build():
            reg = weapwin.register(input_val)
            egg = weapwin.register(value_input_val)
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
            strength_entry = Entry(lawfulneutral_frame, textvariable=strength)
            strength_entry.grid(column=1, row=0, stick='e')
            strength_entry.config(width=4)
            strength_entry.configure(validate='key', vcmd=(reg, "%P"))

            hit_label = Label(lawfulneutral_frame, text='Hit:')
            hit_label.grid(column=0, row=1, sticky='e')
            hit_entry = Entry(lawfulneutral_frame, textvariable=hit)
            hit_entry.grid(column=1, row=1, sticky='e')
            hit_entry.config(width=4)
            hit_entry.configure(validate='key', vcmd=(reg, "%P"))

            damage_label = Label(lawfulneutral_frame, text='Damage:')
            damage_label.grid(column=0, row=2, sticky='e')
            damage_entry = Entry(lawfulneutral_frame, textvariable=damage)
            damage_entry.grid(column=1, row=2, sticky='e')
            damage_entry.config(width=4)
            damage_entry.configure(validate='key', vcmd=(reg, "%P"))

            range_label = Label(lawfulneutral_frame, text='Range:')
            range_label.grid(column=0, row=3, sticky='e')
            range_entry = Entry(lawfulneutral_frame, textvariable=weapon_range)
            range_entry.grid(column=1, row=3, sticky='e')
            range_entry.config(width=4)
            range_entry.configure(validate='key', vcmd=(reg, "%P"))

            value_label = Label(lawfulneutral_frame, text='Base Value:')
            value_label.grid(column=0, row=4, sticky='e')
            value_entry = Entry(lawfulneutral_frame, textvariable=value)
            value_entry.grid(column=1, row=4, sticky='e')
            value_entry.config(width=6)
            value_entry.configure(validate='key', vcmd=(egg, "%P"))
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
            stat_entry = Entry(stat_frame, textvariable=stat_amount)
            stat_entry.grid(column=1, row=0, sticky='e')
            stat_entry.config(width=4)
            stat_entry.configure(validate='key', vcmd=(reg, "%P"))

            ski_att_frame = LabelFrame(trueneutral_frame, text='Skill/Attribute')
            ski_att_frame.grid(column=0, row=1)
            ski_att_menu = OptionMenu(ski_att_frame, skill_attribute, *SKILL_ATTRIBUTE)
            ski_att_menu.grid(column=0, row=0)
            ski_att_menu.config(width=16)
            ski_att_amo_entry = Entry(ski_att_frame, textvariable=skill_attribute_amount)
            ski_att_amo_entry.grid(column=1, row=0)
            ski_att_amo_entry.config(width=4)
            ski_att_amo_entry.configure(validate='key', vcmd=(reg, "%P"))

            spell_frame = LabelFrame(trueneutral_frame, text='Spell')
            spell_frame.grid(column=0, row=2)
            spell_menu = OptionMenu(spell_frame, spell, *EQUIPMENT_SPELLS_MAGIC)
            spell_menu.grid(column=0, row=0)
            spell_menu.config(width=16)
            spell_entry = Entry(spell_frame, textvariable=spell_level)
            spell_entry.grid(column=1, row=0)
            spell_entry.config(width=4)
            spell_entry.configure(validate='key', vcmd=(reg, "%P"))

            magic_frame = LabelFrame(trueneutral_frame, text='Magic')
            magic_frame.grid(column=0, row=3)
            magic_menu = OptionMenu(magic_frame, magic, *EQUIPMENT_SPELLS_MAGIC)
            magic_menu.grid(column=0, row=0)
            magic_menu.config(width=16)
            magic_entry = Entry(magic_frame, textvariable=magic_level)
            magic_entry.grid(column=1, row=0)
            magic_entry.config(width=4)
            magic_entry.configure(validate='key', vcmd=(reg, "%P"))

            resist_frame = LabelFrame(weapwin, text='Resist')
            resist_frame.grid(column=1, row=2)
            resist_menu = OptionMenu(resist_frame, resist, *RESIST)
            resist_menu.grid(column=0, row=0)
            resist_menu.config(width=16)
            resist_amount_menu = OptionMenu(resist_frame, resist_amount, *RESIST_AMOUNTS)
            resist_amount_menu.grid(column=1, row=0)
            resist_amount_menu.config(width=4)

        def input_val(inp):
            if inp.isnumeric() and int(inp) in range(1, 256):
                return True
            elif inp == "":
                return True
            else:
                return False

        def value_input_val(inp):
            if inp.isnumeric() and int(inp) in range(1, 65536):
                return True
            elif inp == "":
                return True
            else:
                return False

        def limit_name_size(*args):
            n = name.get()
            if len(n) > 21:
                name.set(n[:21])

        weapon = StringVar()
        weapon.trace('w', set_defaults)
        name = StringVar()
        name.trace('w', limit_name_size)

        weapon_type = StringVar()
        strength = IntVar()
        hit = IntVar()
        damage = IntVar()
        value = IntVar()
        weapon_range = IntVar()
        animation = StringVar()
        aspect = IntVar()
        stat = StringVar()
        stat_amount = IntVar()
        skill_attribute = StringVar()
        skill_attribute_amount = IntVar()
        spell = StringVar()
        spell_level = IntVar()
        magic = StringVar()
        magic_level = IntVar()
        resist = StringVar()
        resist_amount = StringVar()

        weapon.set(WEAPON_NAMES[28])
        build()
