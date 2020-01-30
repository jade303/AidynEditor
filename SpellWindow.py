from functools import partial
from tkinter import Toplevel, Frame, LabelFrame, Entry, Radiobutton, Label, Button, StringVar, IntVar
from tkinter.ttk import Combobox

from functions import limit_name_size, limit
from variables import SPELL_ADDRESSES, SPELL_INGREDIENTS, SPELL_NAMES, inv_SPELL_INGREDIENTS, \
    TARGET_NUM, TARGET_TYPE, inv_TARGET_NUM, inv_TARGET_TYPE


class SpellEdit:
    def __init__(self, filename):
        spellwin = Toplevel()
        spellwin.resizable(False, False)
        spellwin.title("Spell Edit")
        spellwin.iconbitmap('images\\aidyn.ico')
        filename = filename
        data_seek = 25
        data_read = 11
        name_length = 22

        def read_defaults(*args):
            with open(filename, 'rb') as f:
                address = SPELL_ADDRESSES[SPELL_NAMES.index(spell.get())]

                # get name that can be changed
                f.seek(address)
                name.set(f.read(name_length).decode("utf-8"))

                # get everything else
                f.seek(address + data_seek)
                spell_data = f.read(data_read)
                d = spell_data.hex()

                school.set(d[1])
                damage.set(int(d[2] + d[3], 16))
                stamina.set(int(d[4] + d[5], 16))
                target_num.set(inv_TARGET_NUM[d[7]])
                target_type.set(inv_TARGET_TYPE[d[9]])
                # target_area.set(int(sd[10] + sd[11], 16))
                wizard.set(int(d[12] + d[13], 16))
                asp = d[15]
                if asp == range(0, 2):
                    asp = 0
                aspect.set(asp)
                spell_range.set(int(d[16] + d[17], 16))
                ingredient.set(inv_SPELL_INGREDIENTS[d[19]])
                exp.set(int(d[20] + d[21], 16))

        def write_values():
            with open(filename, 'rb+') as f:
                address = SPELL_ADDRESSES[SPELL_NAMES.index(spell.get())]
                new_name = bytearray(name.get(), 'utf-8')
                if len(new_name) < name_length:
                    while len(new_name) < name_length:
                        new_name.append(0x00)
                f.seek(address)
                f.write(new_name)

                f.seek(address + data_seek)
                spell_data = f.read(data_read)
                d = spell_data.hex()

                towrite = [
                    school.get(),
                    int(damage.get()),
                    int(stamina.get()),
                    int(TARGET_NUM[target_num.get()]),
                    int(TARGET_TYPE[target_type.get()]),
                    int(d[10] + d[11], 16),
                    int(wizard.get()),
                    aspect.get(),
                    int(spell_range.get()),
                    int(SPELL_INGREDIENTS[ingredient.get()]),
                    int(exp.get())
                ]

                f.seek(address + data_seek)
                for item in towrite:
                    f.write(item.to_bytes(1, byteorder='big'))

        def build_window():
            lawfulgood_frame = Frame(spellwin)
            lawfulgood_frame.grid(column=0, row=0)
            default_spell_menu = Combobox(lawfulgood_frame, textvariable=spell, values=SPELL_NAMES)
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

            stamina_label = Label(stuff_frame, text='Stamina Cost:')
            stamina_label.grid(column=0, row=1, sticky='e')
            stamina_entry = Entry(stuff_frame, textvariable=stamina)
            stamina_entry.grid(column=1, row=1, sticky='e')
            stamina_entry.config(width=4)

            wizard_label = Label(stuff_frame, text='Wizard Required:')
            wizard_label.grid(column=0, row=2, sticky='e')
            wizard_entry = Entry(stuff_frame, textvariable=wizard)
            wizard_entry.grid(column=1, row=2, sticky='e')
            wizard_entry.config(width=4)

            range_label = Label(stuff_frame, text='Range:')
            range_label.grid(column=0, row=3, sticky='e')
            range_entry = Entry(stuff_frame, textvariable=spell_range)
            range_entry.grid(column=1, row=3, sticky='e')
            range_entry.config(width=4)

            exp_label = Label(stuff_frame, text='EXP to Rank:')
            exp_label.grid(column=0, row=4, sticky='e')
            exp_entry = Entry(stuff_frame, textvariable=exp)
            exp_entry.grid(column=1, row=4, sticky='e')
            exp_entry.config(width=4)
            exp_label2 = Label(stuff_frame, text='(there is some unknown \nformula involved with EXP)')
            exp_label2.grid(row=5, columnspan=2, rowspan=2, sticky='ew')
            exp_label2.config(font=(None, 8))

            another_frame = Frame(spellwin)
            another_frame.grid(column=1, row=1)
            write_button = Button(spellwin, text='Write To File', command=write_values)
            write_button.grid(column=1, row=0)
            ingredient_frame = LabelFrame(another_frame, text='Ingredient')
            ingredient_frame.grid(column=0, row=0)
            ingredient_menu = Combobox(ingredient_frame, textvariable=ingredient, values=list(SPELL_INGREDIENTS.keys()))
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
            target_num_menu = Combobox(target_num_frame, textvariable=target_num, values=list(TARGET_NUM.keys()))
            target_num_menu.grid()
            target_num_menu.config(width=23)

            target_type_frame = LabelFrame(target_frame, text='Who is targeted:')
            target_type_frame.grid(column=0, row=1)
            target_type_menu = Combobox(target_type_frame, textvariable=target_type, values=list(TARGET_TYPE.keys()))
            target_type_menu.grid()
            target_type_menu.config(width=23)

        spell = StringVar()
        spell.trace('w', read_defaults)
        name = StringVar()
        name.trace('w', partial(limit_name_size, name, name_length))

        damage = StringVar()
        damage.trace('w', partial(limit, damage, 255))
        stamina = StringVar()
        stamina.trace('w', partial(limit, stamina, 120))
        wizard = StringVar()
        wizard.trace('w', partial(limit, wizard, 10))
        spell_range = StringVar()
        spell_range.trace('w', partial(limit, spell_range, 255))
        exp = StringVar()
        exp.trace('w', partial(limit, exp, 255))
        school = IntVar()
        target_num = StringVar()
        target_type = StringVar()
        # target_area = IntVar()
        aspect = IntVar()
        ingredient = StringVar()

        spell.set(SPELL_NAMES[0])
        build_window()
