from tkinter import *
from variables import SPELL_ADDRESSES, SPELL_INGREDIENTS, SPELL_NAMES, inv_SPELL_INGREDIENTS
from variables import TARGET_NUM, TARGET_TYPE, inv_TARGET_NUM, inv_TARGET_TYPE


class SpellEdit:
    def __init__(self, filename):
        spellwin = Toplevel()
        spellwin.title("Spell Edit")
        filename = filename

        def read_defaults(*args):
            with open(filename, 'rb') as f:
                address = SPELL_ADDRESSES[SPELL_NAMES.index(spell.get())]

                # get name that can be changed
                f.seek(address)
                name.set(f.read(22).decode("utf-8"))

                # get everything else
                f.seek(address + 25)
                spell_data = f.read(11)
                sd = spell_data.hex()

                school.set(sd[1])
                damage.set(int(sd[2] + sd[3], 16))
                stamina.set(int(sd[4] + sd[5], 16))
                target_num.set(inv_TARGET_NUM[sd[7]])
                target_type.set(inv_TARGET_TYPE[sd[9]])
                # target_area.set(int(sd[10] + sd[11], 16))
                wizard.set(int(sd[12] + sd[13], 16))
                aspect.set(sd[14])
                spell_range.set(int(sd[17], 16))
                ingredient.set(inv_SPELL_INGREDIENTS[sd[19]])
                exp.set(int(sd[20] + sd[21], 16))

        def write_values():
            with open(filename, 'rb+') as f:
                address = SPELL_ADDRESSES[SPELL_NAMES.index(spell.get())]
                new_name = name.get()
                if len(new_name) > 22:
                    new_name = bytes(new_name[:22], 'utf-8')
                if len(new_name) < 22:
                    new_name = bytearray(new_name, 'utf-8')
                    while len(new_name) < 22:
                        new_name.append(0x00)
                f.seek(address)
                f.write(new_name.encode('utf-8'))

                f.seek(address + 25)
                spell_data = f.read(11)
                sd = spell_data.hex()

                towrite = [
                    school.get(), damage.get(), stamina.get(), int(TARGET_NUM[target_num.get()], 16),
                    int(TARGET_TYPE[target_type.get()], 16), int(sd[10] + sd[11]),
                    wizard.get(), aspect.get(), spell_range.get(), int(SPELL_INGREDIENTS[ingredient.get()], 16),
                    exp.get()
                ]

                f.seek(address + 25)
                for item in towrite:
                    f.write(item.to_bytes(1, byteorder='big'))

        def build_window():
            reg = spellwin.register(input_val)
            lawfulgood_frame = Frame(spellwin)
            lawfulgood_frame.grid(column=0, row=0)
            default_spell_menu = OptionMenu(lawfulgood_frame, spell, *SPELL_NAMES)
            default_spell_menu.grid()
            default_spell_menu.config(width=22)

            new_name_label = LabelFrame(lawfulgood_frame, text='New Name')
            new_name_label.grid()
            new_name_entry = Entry(new_name_label, textvariable=name)
            new_name_entry.grid()
            new_name_entry.config(width=22)

            school_frame = LabelFrame(spellwin, text='School')
            school_frame.grid()
            school1 = Radiobutton(school_frame, text='Elemental', variable=school, value='1')
            school1.grid(sticky='w')
            school2 = Radiobutton(school_frame, text='Naming', variable=school, value='2')
            school2.grid(sticky='w')
            school3 = Radiobutton(school_frame, text='Necromancy', variable=school, value='3')
            school3.grid(sticky='w')
            school5 = Radiobutton(school_frame, text='Star', variable=school, value='5')
            school5.grid(sticky='w')
            school4 = Radiobutton(school_frame, text='NONE', variable=school, value='4')
            school4.grid(sticky='w')

            stuff_frame = Frame(spellwin)
            stuff_frame.grid()
            damage_label = Label(stuff_frame, text='Damage:')
            damage_label.grid(column=0, row=0, sticky='e')
            damage_entry = Entry(stuff_frame, textvariable=damage)
            damage_entry.grid(column=1, row=0, sticky='e')
            damage_entry.config(width=4)
            damage_entry.configure(validate='key', vcmd=(reg, "%P"))

            stamina_label = Label(stuff_frame, text='Stamina Cost:')
            stamina_label.grid(column=0, row=1, sticky='e')
            stamina_entry = Entry(stuff_frame, textvariable=stamina)
            stamina_entry.grid(column=1, row=1, sticky='e')
            stamina_entry.config(width=4)
            stamina_entry.configure(validate='key', vcmd=(reg, "%P"))

            wizard_label = Label(stuff_frame, text='Wizard Required:')
            wizard_label.grid(column=0, row=2, sticky='e')
            wizard_entry = Entry(stuff_frame, textvariable=wizard)
            wizard_entry.grid(column=1, row=2, sticky='e')
            wizard_entry.config(width=4)
            wizard_entry.configure(validate='key', vcmd=(reg, "%P"))

            range_label = Label(stuff_frame, text='Range:')
            range_label.grid(column=0, row=3, sticky='e')
            range_entry = Entry(stuff_frame, textvariable=spell_range)
            range_entry.grid(column=1, row=3, sticky='e')
            range_entry.config(width=4)
            range_entry.configure(validate='key', vcmd=(reg, "%P"))

            exp_label = Label(stuff_frame, text='EXP to Rank:')
            exp_label.grid(column=0, row=4, sticky='e')
            exp_entry = Entry(stuff_frame, textvariable=exp)
            exp_entry.grid(column=1, row=4, sticky='e')
            exp_entry.config(width=4)
            exp_entry.configure(validate='key', vcmd=(reg, "%P"))
            exp_label2 = Label(stuff_frame, text='(there is some unknown \nformula involved with EXP)')
            exp_label2.grid(row=5, columnspan=2, rowspan=2, sticky='ew')
            exp_label2.config(font=(None, 8))

            another_frame = Frame(spellwin)
            another_frame.grid(column=1, row=1)
            write_button = Button(spellwin, text='Write To File', command=write_values)
            write_button.grid(column=1, row=0)
            ingredient_frame = LabelFrame(another_frame, text='Ingredient')
            ingredient_frame.grid(column=0, row=0)
            ingredient_menu = OptionMenu(ingredient_frame, ingredient, *SPELL_INGREDIENTS)
            ingredient_menu.grid(column=0, row=0)
            ingredient_menu.config(width=10)

            aspect_frame = LabelFrame(another_frame, text='Aspect')
            aspect_frame.grid(column=0, row=1)
            aspect_none = Radiobutton(aspect_frame, text='NONE', variable=aspect, value=0)
            aspect_none.grid(column=0, row=0, sticky='w')
            aspect_solar = Radiobutton(aspect_frame, text='Solar', variable=aspect, value=4)
            aspect_solar.grid(column=0, row=1, sticky='w')
            aspect_lunar = Radiobutton(aspect_frame, text='Lunar', variable=aspect, value=3)
            aspect_lunar.grid(column=0, row=2, sticky='w')

            target_frame = Frame(spellwin)
            target_frame.grid(column=1, row=2)
            target_num_frame = LabelFrame(target_frame, text='Number of targets:')
            target_num_frame.grid(column=0, row=0)
            target_num_menu = OptionMenu(target_num_frame, target_num, *TARGET_NUM)
            target_num_menu.grid()
            target_num_menu.config(width=23)

            target_type_frame = LabelFrame(target_frame, text='Who is targeted:')
            target_type_frame.grid(column=0, row=1)
            target_type_menu = OptionMenu(target_type_frame, target_type, *TARGET_TYPE)
            target_type_menu.grid()
            target_type_menu.config(width=23)

        def input_val(inp):
            if inp.isnumeric() and int(inp) in range(1, 256):
                return True
            elif inp == "":
                return True
            else:
                return False

        def limit_name_size(*args):
            n = name.get()
            if len(n) > 22:
                name.set(n[:22])

        spell = StringVar()
        spell.trace('w', read_defaults)
        name = StringVar()
        name.trace('w', limit_name_size)
        school = IntVar()
        damage = IntVar()
        stamina = IntVar()
        target_num = StringVar()
        target_type = StringVar()
        # target_area = IntVar()
        wizard = IntVar()
        aspect = IntVar()
        spell_range = IntVar()
        ingredient = StringVar()
        exp = IntVar()

        spell.set(SPELL_NAMES[0])
        build_window()
