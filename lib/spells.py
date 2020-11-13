from functools import partial
from tkinter import Toplevel, Frame, LabelFrame, Entry, Radiobutton, Label, Button, StringVar, IntVar
from tkinter.ttk import Combobox

from lib.fuctions import get_major_name_lists, int_cast, limit_name_size, limit
from lib.variables import SPELL_ADDRESSES, inv_TARGET_NUM, inv_TARGET_TYPE, inv_SPELL_INGREDIENTS, \
    TARGET_NUM, TARGET_TYPE, SPELL_INGREDIENTS, SCHOOL, inv_SCHOOL


class SpellEdit:
    def __init__(self, f, i):
        self.win = Toplevel()
        self.win.resizable(False, False)
        self.filename = f
        self.icon = i
        self.win.title("Spell Edit")
        self.win.iconbitmap(self.icon)
        self.data_seek = 25
        self.data_read = 11
        self.name_length = 22

        # lists
        self.spell_list, self.spell_addresses = get_major_name_lists(self.filename, SPELL_ADDRESSES, self.name_length)

        # variables
        self.spell = StringVar()
        self.spell.trace('w', self.set_defaults)
        self.name = StringVar()
        self.name.trace('w', partial(limit_name_size, self.name, self.name_length))
        self.damage = StringVar()
        self.damage.trace('w', partial(limit, self.damage, 255))
        self.stamina = StringVar()
        self.stamina.trace('w', partial(limit, self.stamina, 127))
        self.wizard = StringVar()
        self.wizard.trace('w', partial(limit, self.wizard, 10))
        self.spell_range = StringVar()
        self.spell_range.trace('w', partial(limit, self.spell_range, 255))
        self.exp = StringVar()
        self.exp.trace('w', partial(limit, self.exp, 255))
        self.school = StringVar()
        self.target_num = StringVar()
        self.target_type = StringVar()
        # self.target_area = IntVar()
        self.aspect = IntVar()
        self.ingredient = StringVar()

        # build items
        self.box = Frame(self.win)
        self.default_spell_menu = Combobox(self.box, textvariable=self.spell, width=22,
                                           values=self.spell_list,
                                           postcommand=self.reset_list, state='readonly')
        self.new_name_label = LabelFrame(self.box, text='New Name')
        self.new_name_entry = Entry(self.new_name_label, textvariable=self.name, width=22)
        self.stats_frame = LabelFrame(self.box, text='Stats')
        self.damage_label = Label(self.stats_frame, text='Damage:')
        self.damage_entry = Entry(self.stats_frame, textvariable=self.damage, width=4)
        self.stamina_label = Label(self.stats_frame, text='Stamina Cost:')
        self.stamina_entry = Entry(self.stats_frame, textvariable=self.stamina, width=4)
        self.wizard_label = Label(self.stats_frame, text='Wizard Required:')
        self.wizard_entry = Entry(self.stats_frame, textvariable=self.wizard, width=4)
        self.range_label = Label(self.stats_frame, text='Range:')
        self.range_entry = Entry(self.stats_frame, textvariable=self.spell_range, width=4)
        self.exp_label1 = Label(self.stats_frame, text='EXP to Rank:')
        self.exp_entry = Entry(self.stats_frame, textvariable=self.exp, width=4)
        self.exp_label2 = Label(self.stats_frame, text='(Higher # = more EXP to rank)', font=(None, 8))
        self.save = Button(self.box, text='Save', command=self.write, width=8)
        self.aspect_frame = LabelFrame(self.box, text='Aspect')
        self.aspect_none = Radiobutton(self.aspect_frame, text='NONE', variable=self.aspect, value=0)
        self.aspect_solar = Radiobutton(self.aspect_frame, text='Solar', variable=self.aspect, value=4)
        self.aspect_lunar = Radiobutton(self.aspect_frame, text='Lunar', variable=self.aspect, value=3)
        self.school_frame = LabelFrame(self.box, text='School')
        self.school_box = Combobox(self.school_frame, textvariable=self.school, width=12, state='readonly',
                                   values=(list(SCHOOL.keys())[0:1] + list(SCHOOL.keys())[2:]))
        self.ingredient_frame = LabelFrame(self.box, text='Ingredient')
        self.ingredient_menu = Combobox(self.ingredient_frame, textvariable=self.ingredient, width=12,
                                        values=list(SPELL_INGREDIENTS.keys()), state='readonly')
        self.target_num_frame = LabelFrame(self.box, text='Number of targets:')
        self.target_num_menu = Combobox(self.target_num_frame, textvariable=self.target_num, width=23,
                                        values=list(TARGET_NUM.keys()), state='readonly')
        self.target_type_frame = LabelFrame(self.box, text='Who is targeted:')
        self.target_type_menu = Combobox(self.target_type_frame, textvariable=self.target_type,
                                         values=list(TARGET_TYPE.keys()),
                                         width=23, state='readonly')

        # run
        self.build()
        self.spell.set(self.spell_list[0])

    def set_defaults(self, *args):
        with open(self.filename, 'rb') as f:
            address = self.spell_addresses[self.default_spell_menu.current()]

            f.seek(address)
            self.name.set(f.read(self.name_length).decode("utf-8"))

            f.seek(address + self.data_seek)
            d = f.read(self.data_read).hex()

            self.school.set(inv_SCHOOL[(d[0] + d[1]).upper()])
            self.damage.set(int(d[2] + d[3], 16))
            self.stamina.set(int(d[4] + d[5], 16))
            self.target_num.set(inv_TARGET_NUM[d[7]])
            self.target_type.set(inv_TARGET_TYPE[d[9]])
            # self.target_area.set(int(sd[10] + sd[11], 16))
            self.wizard.set(int(d[12] + d[13], 16))
            asp = d[15]
            if asp == range(0, 2):
                asp = 0
            self.aspect.set(asp)
            self.spell_range.set(int(d[16] + d[17], 16))
            self.ingredient.set(inv_SPELL_INGREDIENTS[d[19]])
            self.exp.set(int(d[20] + d[21], 16))

    def write(self):
        with open(self.filename, 'rb+') as f:
            address = self.spell_addresses[self.default_spell_menu.current()]

            new_name = bytearray(self.name.get(), 'utf-8')
            if len(new_name) < self.name_length:
                while len(new_name) < self.name_length:
                    new_name.append(0x00)
            f.seek(address)
            f.write(new_name)

            f.seek(address + self.data_seek)
            d = f.read(self.data_read).hex()

            towrite = [
                SCHOOL[self.school.get()],
                self.damage.get(),
                self.stamina.get(),
                TARGET_NUM[self.target_num.get()],
                TARGET_TYPE[self.target_type.get()],
                (d[10] + d[11]),
                self.wizard.get(),
                self.aspect.get(),
                self.spell_range.get(),
                SPELL_INGREDIENTS[self.ingredient.get()],
                self.exp.get()
            ]

            f.seek(address + self.data_seek)
            for item in towrite:
                item = int_cast(item)
                f.write(item.to_bytes(1, byteorder='big'))

            self.reset_list()
            self.spell.set(self.spell_list[self.spell_list.index(self.name.get().rstrip('\x00'))])
        self.set_defaults()

    def build(self):
        self.box.grid(column=0, row=0, pady=5, padx=5)

        self.default_spell_menu.grid(column=0, row=0)

        self.new_name_label.grid(column=0, row=1)
        self.new_name_entry.grid()

        self.stats_frame.grid(column=0, row=2, rowspan=4)
        self.damage_label.grid(column=0, row=0, sticky='e')
        self.damage_entry.grid(column=1, row=0, sticky='w')

        self.stamina_label.grid(column=0, row=1, sticky='e')
        self.stamina_entry.grid(column=1, row=1, sticky='w')

        self.wizard_label.grid(column=0, row=2, sticky='e')
        self.wizard_entry.grid(column=1, row=2, sticky='w')

        self.range_label.grid(column=0, row=3, sticky='e')
        self.range_entry.grid(column=1, row=3, sticky='w')

        self.exp_label1.grid(column=0, row=4, sticky='e')
        self.exp_entry.grid(column=1, row=4, sticky='w')
        self.exp_label2.grid(row=5, columnspan=3, rowspan=2, sticky='ew')

        self.save.grid(column=1, row=0)

        self.aspect_frame.grid(column=1, row=1)
        self.aspect_none.grid(column=0, row=0)
        self.aspect_solar.grid(column=1, row=0)
        self.aspect_lunar.grid(column=2, row=0)

        self.school_frame.grid(column=1, row=2)
        self.school_box.grid()

        self.ingredient_frame.grid(column=1, row=3)
        self.ingredient_menu.grid(column=0, row=0)

        self.target_num_frame.grid(column=1, row=4)
        self.target_num_menu.grid()

        self.target_type_frame.grid(column=1, row=5)
        self.target_type_menu.grid()

    def reset_list(self):
        self.spell_list[:] = []
        self.spell_addresses[:] = []
        self.spell_list, self.spell_addresses = get_major_name_lists(self.filename, SPELL_ADDRESSES, self.name_length)
        self.default_spell_menu['values'] = self.spell_list
