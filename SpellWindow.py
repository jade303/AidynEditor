from tkinter import Toplevel, Frame, LabelFrame, Entry, Radiobutton, Label, Button, StringVar, IntVar
from tkinter.ttk import Combobox

from variables import SPELL_ADDRESSES, SPELL_INGREDIENTS, SPELL_NAMES, inv_SPELL_INGREDIENTS, \
    TARGET_NUM, TARGET_TYPE, inv_TARGET_NUM, inv_TARGET_TYPE


class SpellEdit:
    def __init__(self, filename):
        spellwin = Toplevel()
        spellwin.resizable(False, False)
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
                d = spell_data.hex()

                school.set(d[1])
                pos_stats[0].set(int(d[2] + d[3], 16))
                pos_stats[1].set(int(d[4] + d[5], 16))
                target_num.set(inv_TARGET_NUM[d[7]])
                target_type.set(inv_TARGET_TYPE[d[9]])
                # target_area.set(int(sd[10] + sd[11], 16))
                pos_stats[2].set(int(d[12] + d[13], 16))
                aspect.set(d[14])
                pos_stats[3].set(int(d[16] + d[17], 16))
                ingredient.set(inv_SPELL_INGREDIENTS[d[19]])
                pos_stats[4].set(int(d[20] + d[21], 16))

        def write_values():
            with open(filename, 'rb+') as f:
                address = SPELL_ADDRESSES[SPELL_NAMES.index(spell.get())]
                new_name = bytearray(name.get(), 'utf-8')
                if len(new_name) < 22:
                    while len(new_name) < 22:
                        new_name.append(0x00)
                f.seek(address)
                f.write(new_name)

                f.seek(address + 25)
                spell_data = f.read(11)
                d = spell_data.hex()

                towrite = [
                    school.get(),
                    int(pos_stats[0].get()),
                    int(pos_stats[1].get()),
                    int(TARGET_NUM[target_num.get()]),
                    int(TARGET_TYPE[target_type.get()]),
                    int(d[10] + d[11], 16),
                    int(pos_stats[2].get()),
                    aspect.get(),
                    int(pos_stats[3].get()),
                    int(SPELL_INGREDIENTS[ingredient.get()]),
                    int(pos_stats[4].get())
                ]

                f.seek(address + 25)
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
            damage_entry = Entry(stuff_frame, textvariable=pos_stats[0])
            damage_entry.grid(column=1, row=0, sticky='e')
            damage_entry.config(width=4)

            stamina_label = Label(stuff_frame, text='Stamina Cost:')
            stamina_label.grid(column=0, row=1, sticky='e')
            stamina_entry = Entry(stuff_frame, textvariable=pos_stats[1])
            stamina_entry.grid(column=1, row=1, sticky='e')
            stamina_entry.config(width=4)

            wizard_label = Label(stuff_frame, text='Wizard Required:')
            wizard_label.grid(column=0, row=2, sticky='e')
            wizard_entry = Entry(stuff_frame, textvariable=pos_stats[2])
            wizard_entry.grid(column=1, row=2, sticky='e')
            wizard_entry.config(width=4)

            range_label = Label(stuff_frame, text='Range:')
            range_label.grid(column=0, row=3, sticky='e')
            range_entry = Entry(stuff_frame, textvariable=pos_stats[3])
            range_entry.grid(column=1, row=3, sticky='e')
            range_entry.config(width=4)

            exp_label = Label(stuff_frame, text='EXP to Rank:')
            exp_label.grid(column=0, row=4, sticky='e')
            exp_entry = Entry(stuff_frame, textvariable=pos_stats[4])
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

        # limits the same size
        def limit_name_size(*args):
            n = name.get()
            if len(n) > 22:
                name.set(n[:22])

        # check for positive 255
        def pos_check(*args):
            for i in pos_stats:
                val = i.get()
                if not val.isnumeric():
                    val = ''.join(filter(str.isnumeric, val))
                    i.set(val)
                elif val.isnumeric():
                    if int(val) > 255:
                        i.set(255)
                    else:
                        i.set(val)

        spell = StringVar()
        spell.trace('w', read_defaults)
        name = StringVar()
        name.trace('w', limit_name_size)

        # group of stats:
        # damage, stamina, wizard, spell range, exp
        # grouped to make it easier to run a 255 check
        pos_stats = []
        for i in range(5):
            i = StringVar()
            i.trace('w', pos_check)
            pos_stats.append(i)

        school = IntVar()
        target_num = StringVar()
        target_type = StringVar()
        # target_area = IntVar()
        aspect = IntVar()
        ingredient = StringVar()

        spell.set(SPELL_NAMES[0])
        build_window()
