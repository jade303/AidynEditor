from functools import partial
from tkinter import Toplevel, StringVar, Frame, LabelFrame, Entry, Label, Button, Radiobutton, IntVar
from tkinter.ttk import Combobox
from lib.limits import limit_name_size, limit, limit_127
from lib.list_functions import get_major_name_lists, get_minor_dic
from lib.variables import SPELL_DIC, EQUIPMENT_STAT, SKILL_ATTRIBUTE, RESIST_AMOUNTS, RESIST


class Item:
    def __init__(self, f, i, a, s, r, n):
        self.win = Toplevel()
        self.win.resizable(False, False)
        self.win.iconbitmap(i)
        self.filename = f
        self.item_addresses = a
        self.data_seek = s
        self.data_read = r
        self.name_length = n

        # dictionaries and lists
        self.spell_dic = get_minor_dic(self.filename, SPELL_DIC, 22)
        self.inv_spell_dic = {v: k for k, v in self.spell_dic.items()}
        self.item_list, self.address_list = get_major_name_lists(self.filename, self.item_addresses, self.name_length)

        # variables
        self.item = StringVar()
        self.item.trace('w', self.set_defaults)
        self.name = StringVar()
        self.name.trace('w', partial(limit_name_size, self.name, self.name_length))
        self.value = StringVar()
        self.value.trace('w', partial(limit, self.value, 65535))
        self.aspect = IntVar()
        self.stats = [StringVar() for i in range(5)]
        self.att = StringVar()
        self.att_amount = StringVar()
        self.att_amount.trace('w', partial(limit_127, self.att_amount))
        self.skill = StringVar()
        self.skill_amount = StringVar()
        self.skill_amount.trace('w', partial(limit_127, self.skill_amount))
        self.spell = StringVar()
        self.spell_level = StringVar()
        self.spell_level.trace('w', partial(limit, self.spell_level, 15))
        self.magic = StringVar()
        self.magic_level = StringVar()
        self.magic_level.trace('w', partial(limit, self.magic_level, 15))
        self.resist = StringVar()
        self.resist_amount = StringVar()

        # build items
        self.box = Frame(self.win)

        self.default_item_menu = Combobox(self.box, postcommand=self.reset_list, state='readonly', width=21,
                                          textvariable=self.item,
                                          values=self.item_list)

        self.new_name_label = LabelFrame(self.box, text='New Name')
        self.new_name_entry = Entry(self.new_name_label, textvariable=self.name, width=21)

        self.save = Button(self.box, text='Save', width=8, command=self.write)

        self.aspect_frame = LabelFrame(self.box, text='Aspect')
        self.none_radio = Radiobutton(self.aspect_frame, text='NONE', variable=self.aspect, value=0)
        self.solar_radio = Radiobutton(self.aspect_frame, text="Solar", variable=self.aspect, value=2)
        self.lunar_radio = Radiobutton(self.aspect_frame, text='Lunar', variable=self.aspect, value=1)

        self.att_frame = LabelFrame(self.box, text='Attribute')
        self.att_menu = Combobox(self.att_frame, state='readonly', width=16,
                                 textvariable=self.att, values=list(EQUIPMENT_STAT.keys()))
        self.att_entry = Entry(self.att_frame, textvariable=self.att_amount, width=4)

        self.ski_att_frame = LabelFrame(self.box, text='Skill/Attribute')
        self.ski_att_menu = Combobox(self.ski_att_frame, width=16, state='readonly',
                                     textvariable=self.skill, values=list(SKILL_ATTRIBUTE.keys()))
        self.ski_att_amo_entry = Entry(self.ski_att_frame, textvariable=self.skill_amount, width=4)

        self.spell_frame = LabelFrame(self.box, text='Spell')
        self.spell_menu = Combobox(self.spell_frame, width=16, state='readonly',
                                   textvariable=self.spell, values=list(self.inv_spell_dic.keys()))
        self.spell_entry = Entry(self.spell_frame, textvariable=self.spell_level, width=4)

        self.magic_frame = LabelFrame(self.box, text='Magic')
        self.magic_menu = Combobox(self.magic_frame, width=16, state='readonly',
                                   textvariable=self.magic, values=list(self.inv_spell_dic.keys()), )
        self.magic_entry = Entry(self.magic_frame, textvariable=self.magic_level, width=4)

        self.resist_frame = LabelFrame(self.box, text='Resist')
        self.resist_menu = Combobox(self.resist_frame, width=16, state='readonly',
                                    textvariable=self.resist, values=list(RESIST.keys()))
        self.resist_amount_menu = Combobox(self.resist_frame, width=5, state='readonly',
                                           textvariable=self.resist_amount, values=list(RESIST_AMOUNTS.keys()))

        self.stat_frame = LabelFrame(self.box, text='Stats:')
        self.stat_label = []
        self.stat_entry = []
        for x in range(5):
            self.stat_label.append(Label(self.stat_frame))
            self.stat_entry.append(Entry(self.stat_frame, textvariable=self.stats[x], width=4))
        self.value_label = Label(self.stat_frame, text='Base Value:')
        self.value_entry = Entry(self.stat_frame, textvariable=self.value, width=5)
        self.value_label2 = Label(self.stat_frame, text='Max base value: 65535', font=(None, 8))

    def set_defaults(self):
        pass

    def write(self):
        pass

    def build(self):
        self.box.grid(column=0, row=0, pady=5, padx=5)

        self.default_item_menu.grid(column=0, row=0)

        self.new_name_label.grid(column=0, row=1)
        self.new_name_entry.grid()

        self.stat_frame.grid(column=0, row=2, rowspan=4)

        for i in range(5):
            self.stat_label[i].grid(column=0, row=i, sticky='e')
            self.stat_entry[i].grid(column=1, row=i, sticky='w')

        self.value_label.grid(column=0, row=4, sticky='e')
        self.value_entry.grid(column=1, row=4, sticky='w')
        self.value_label2.grid(row=5, columnspan=2)

        self.save.grid(column=1, row=0)

        self.aspect_frame.grid(column=1, row=1)
        self.none_radio.grid(column=0, row=0)
        self.solar_radio.grid(column=1, row=0)
        self.lunar_radio.grid(column=2, row=0)

        self.att_frame.grid(column=1, row=2)
        self.att_menu.grid(column=0, row=0)
        self.att_entry.grid(column=1, row=0, sticky='e')

        self.ski_att_frame.grid(column=1, row=3)
        self.ski_att_menu.grid(column=0, row=0)
        self.ski_att_amo_entry.grid(column=1, row=0)

        self.spell_frame.grid(column=1, row=4)
        self.spell_menu.grid(column=0, row=0)
        self.spell_entry.grid(column=1, row=0)

        self.magic_frame.grid(column=1, row=5)
        self.magic_menu.grid(column=0, row=0)
        self.magic_entry.grid(column=1, row=0)

        self.resist_frame.grid(column=1, row=6)
        self.resist_menu.grid(column=0, row=0)
        self.resist_amount_menu.grid(column=1, row=0)

    def reset_list(self):
        self.item_list[:] = []
        self.address_list[:] = []
        self.item_list, self.address_list = get_major_name_lists(self.filename, self.item_addresses, self.name_length)
        self.default_item_menu['values'] = self.item_list
