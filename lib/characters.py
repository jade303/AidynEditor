from functools import partial
from tkinter import Toplevel, Frame, LabelFrame, Entry, Button, Radiobutton, Label, StringVar, IntVar
from tkinter.ttk import Combobox

from lib.fuctions import get_major_item_dic, get_minor_dic, get_major_name_lists, int_cast, limit_name_size, limit, \
    limit_127
from lib.variables import ATTRIBUTES, SKILLS, SPELL_DIC, RESIST, \
    RESIST_AMOUNTS, inv_RESIST, inv_RESIST_AMOUNTS, SCHOOL, inv_SCHOOL


class Characters:
    def __init__(self, f, i, a, n, r, t):
        self.win = Toplevel()
        self.win.resizable(False, False)
        self.win.geometry('+200+10')
        self.win.iconbitmap(i)
        self.filename = f
        self.addresses = a
        self.name_length = n
        self.data_read = r
        self.char_type = t
        self.data_seek = 44

        # dictionaries and lists
        self.major_dic = get_major_item_dic(self.filename)
        self.inv_major_dic = {v: k for k, v in self.major_dic.items()}
        self.armor_lst = ['NONE'] + [item[8:] for item in self.major_dic.values() if item.startswith('(armor)')]
        self.shield_lst = ['NONE'] + [item[9:] for item in self.major_dic.values() if item.startswith('(shield)')]
        self.weapon_lst = ['NONE'] + [item[9:] for item in self.major_dic.values() if item.startswith('(weapon)')]
        self.spell_dic = get_minor_dic(self.filename, SPELL_DIC, 22)
        self.inv_spell_dic = {v: k for k, v in self.spell_dic.items()}
        self.character_list, self.character_addresses = get_major_name_lists(self.filename, self.addresses,
                                                                             self.name_length)

        # variables
        self.character = StringVar()
        self.character.trace('w', self.set_defaults)
        self.name = StringVar()
        self.name.trace('w', partial(limit_name_size, self.name, self.name_length))
        self.aspect = IntVar()
        self.skills = []
        for _ in SKILLS:
            i = StringVar()
            i.trace('w', partial(limit, i, 10))
            self.skills.append(i)
        self.shield_skill = StringVar()
        self.shield_skill.trace('w', partial(limit, self.shield_skill, 10))
        self.atts = []
        for i in range(6):
            i = StringVar()
            i.trace('w', partial(limit, i, 127))
            self.atts.append(i)
        self.level = StringVar()
        self.level.trace('w', partial(limit, self.level, 40))
        self.weapons = [StringVar() for i in range(3)]
        self.spells = [StringVar() for i in range(5)]
        self.schools = StringVar()
        self.spell_levels = []
        for i in range(5):
            i = StringVar()
            i.trace('w', partial(limit, i, 15))
            self.spell_levels.append(i)
        self.armor = StringVar()
        self.protection = StringVar()
        self.protection.trace('w', partial(limit_127, self.protection))
        self.shield = StringVar()
        self.resist1a = StringVar()
        self.resist1b = StringVar()
        self.resist2a = StringVar()
        self.resist2b = StringVar()

        # build items
        self.box = Frame(self.win)
        self.not_loot_frame = Frame(self.box)
        self.default_name_menu = Combobox()
        self.new_name_frame = LabelFrame(self.not_loot_frame, text="New Name")
        self.new_name_entry = Entry(self.new_name_frame, textvariable=self.name, width=19)
        self.save = Button(self.not_loot_frame, text="Save", command=self.write, width=8)
        self.aspect_frame = LabelFrame(self.not_loot_frame, text='Aspect')
        self.solar_radio = Radiobutton(self.aspect_frame, text='Solar', variable=self.aspect, value='2')
        self.lunar_radio = Radiobutton(self.aspect_frame, text='Lunar', variable=self.aspect, value='1')
        self.school_level_frame = Frame(self.not_loot_frame)
        self.school_frame = LabelFrame(self.school_level_frame, text='School')
        self.school_box = Combobox(self.school_frame, textvariable=self.schools, width=12, state='readonly',
                                   values=list(SCHOOL.keys()))
        self.level_frame = LabelFrame(self.school_level_frame, text='Level')
        self.level_entry = Entry(self.level_frame, textvariable=self.level, width=4)
        self.spell_frame = LabelFrame(self.not_loot_frame, text='Spells and Spell Level')
        self.spell = []
        self.spell_level = []
        for x in range(5):
            self.spell.append(
                Combobox(self.spell_frame, textvariable=self.spells[x], values=list(self.inv_spell_dic.keys()),
                         width=16, state='readonly'))
            self.spell_level.append(Entry(self.spell_frame, textvariable=self.spell_levels[x], width=4))
        self.resist_frame = LabelFrame(self.not_loot_frame, text='Resists')
        self.resist_menu1 = Combobox(self.resist_frame, textvariable=self.resist1a, values=list(RESIST.keys()),
                                     width=16, state='readonly')
        self.resist_amount_menu1 = Combobox(self.resist_frame, textvariable=self.resist1b, width=5,
                                            values=list(RESIST_AMOUNTS.keys()), state='readonly')
        self.resist_menu2 = Combobox(self.resist_frame, textvariable=self.resist2a, values=list(RESIST.keys()),
                                     width=16, state='readonly')
        self.resist_amount_menu2 = Combobox(self.resist_frame, textvariable=self.resist2b, width=5,
                                            values=list(RESIST_AMOUNTS.keys()), state='readonly')
        self.att_frame = LabelFrame(self.not_loot_frame, text='Attributes')
        self.att_label = []
        self.att_num = []
        for x in range(6):
            self.att_label.append(Label(self.att_frame, text=ATTRIBUTES[x]))
            self.att_num.append(Entry(self.att_frame, textvariable=self.atts[x], width=4))
        self.protection_label = Label(self.att_frame, text='Base Protection')
        self.protection_entry = Entry(self.att_frame, textvariable=self.protection, width=4)
        self.equipment_frame = LabelFrame(self.not_loot_frame, text='Equipment')
        self.weapon_frame = LabelFrame(self.equipment_frame, text='Weapons')
        self.weapon_menu = []
        for x in range(3):
            self.weapon_menu.append(Combobox(self.weapon_frame, textvariable=self.weapons[x], values=self.weapon_lst,
                                             width=16, state='readonly'))
        self.armor_frame = LabelFrame(self.equipment_frame, text='Armor')
        self.armor_menu = Combobox(self.armor_frame, textvariable=self.armor, values=self.armor_lst, width=16,
                                   state='readonly')
        self.shield_frame = LabelFrame(self.equipment_frame, text='Shield')
        self.shield_menu = Combobox(self.shield_frame, textvariable=self.shield, values=self.shield_lst, width=16,
                                    state='readonly')
        self.skill_frame = LabelFrame(self.not_loot_frame)
        self.shield_num = Entry(self.skill_frame, textvariable=self.shield_skill, width=4)
        self.shield_label = Label(self.skill_frame, text='Shield', anchor='e', width=9)

    def set_defaults(self, *args):
        with open(self.filename, 'rb') as f:
            address = self.character_addresses[self.default_name_menu.current()]
            f.seek(address)
            self.name.set(f.read(self.name_length).decode("utf-8"))

            f.seek(address + self.data_seek)
            d = f.read(self.data_read).hex()

            self.aspect.set(d[1])

            for s in self.skills:
                sn = int(d[(self.skills.index(s) * 2) + 6] + d[(self.skills.index(s) * 2) + 7], 16)
                if sn == 255:
                    sn = ''
                s.set(sn)

            shi = int(d[146] + d[147], 16)
            if shi == 255:
                shi = ''
            self.shield_skill.set(shi)

            for a in self.atts:
                a.set(int(d[(self.atts.index(a) * 2) + 52] + d[(self.atts.index(a) * 2) + 53], 16))

            self.level.set(int(d[66] + d[67], 16))

            for w in self.weapons:
                i = d[((self.weapons.index(w) * 4) + 70):((self.weapons.index(w) * 4) + 74)].upper()
                if i == '0000':
                    w.set(self.major_dic.get(i))
                else:
                    w.set(self.major_dic.get(i)[9:])

            ar = d[136:140].upper()
            if ar == '0000':
                self.armor.set(self.major_dic[ar])
            else:
                self.armor.set(self.major_dic[ar][8:])

            self.protection.set(int(d[140] + d[141], 16))

            sh = d[142:146].upper()
            if sh == '0000':
                self.shield.set(self.major_dic[sh])
            else:
                self.shield.set(self.major_dic[sh][9:])

            self.schools.set(inv_SCHOOL[(d[106] + d[107]).upper()])

            for s in self.spells:
                s.set(self.spell_dic[
                          d[((self.spells.index(s) * 4) + 86):(((self.spells.index(s) * 4) + 86) + 4)].upper()])

            for s in self.spell_levels:
                s.set(int(d[((self.spell_levels.index(s) * 2) + 108)] + d[((self.spell_levels.index(s) * 2) + 108) + 1],
                          16))

            self.resist1a.set(inv_RESIST[(d[148] + d[149]).upper()])
            self.resist1b.set(inv_RESIST_AMOUNTS[(d[150] + d[151]).upper()])
            self.resist2a.set(inv_RESIST[(d[152] + d[153]).upper()])
            self.resist2b.set(inv_RESIST_AMOUNTS[(d[154] + d[155]).upper()])

    def write(self):
        with open(self.filename, 'rb+') as f:
            address = self.character_addresses[self.default_name_menu.current()]
            new_name = bytearray(self.name.get(), 'utf-8')
            if len(new_name) < self.name_length:
                while len(new_name) < self.name_length:
                    new_name.append(0x00)
            f.seek(address)
            f.write(new_name)

            f.seek(address + self.data_seek)
            d = f.read(self.data_read).hex()

            towrite = [self.aspect.get(), (d[2] + d[3]),
                       (d[4] + d[5])]

            for i in self.skills:
                j = i.get()
                if j == '':
                    if self.char_type == 0:
                        j = 255
                    elif self.char_type == 1:
                        j = 0
                towrite.append(j)

            for i in self.atts:
                j = i.get()
                towrite.append(j)

            towrite.append(d[64] + d[65])
            towrite.append(self.level.get())
            towrite.append(d[68] + d[69])

            for i in self.weapons:
                w = i.get()
                if w == 'NONE':
                    towrite.append(int((self.inv_major_dic[w])[:2], 16))
                    towrite.append(int((self.inv_major_dic[w])[2:], 16))
                else:

                    towrite.append(int((self.inv_major_dic['(weapon) ' + w])[:2], 16))
                    towrite.append(int((self.inv_major_dic['(weapon) ' + w])[2:], 16))

            towrite.append(d[82] + d[83])
            towrite.append(d[84] + d[85])

            for i in self.spells:
                towrite.append(self.inv_spell_dic[i.get()][:2])
                towrite.append(self.inv_spell_dic[i.get()][2:])

            towrite.append(SCHOOL[self.schools.get()])

            for i in self.spell_levels:
                towrite.append(i.get())

            for i in range(118, 136, 2):
                towrite.append(d[i] + d[i + 1])

            a = self.armor.get()
            if a == 'NONE':
                towrite.append(int((self.inv_major_dic[a])[:2], 16))
                towrite.append(int((self.inv_major_dic[a])[2:], 16))
            else:
                towrite.append(int((self.inv_major_dic['(armor) ' + a])[:2], 16))
                towrite.append(int((self.inv_major_dic['(armor) ' + a])[2:], 16))

            towrite.append(self.protection.get())

            s = self.shield.get()
            if s == 'NONE':
                towrite.append(int((self.inv_major_dic[s])[:2], 16))
                towrite.append(int((self.inv_major_dic[s])[2:], 16))
            else:
                towrite.append(int((self.inv_major_dic['(shield) ' + s])[:2], 16))
                towrite.append(int((self.inv_major_dic['(shield) ' + s])[2:], 16))

            shi = self.shield_skill.get()
            if shi == '':
                if self.char_type == 0:
                    shi = 255
                elif self.char_type == 1:
                    shi = 0
            towrite.append(shi)

            towrite.append(RESIST[self.resist1a.get()])
            towrite.append(RESIST_AMOUNTS[self.resist1b.get()])
            towrite.append(RESIST[self.resist2a.get()])
            towrite.append(RESIST_AMOUNTS[self.resist2b.get()])

            f.seek(address + self.data_seek)
            for item in towrite:
                item = int_cast(item)
                f.write(item.to_bytes(1, byteorder='big'))

            self.reset_character_list()
            self.character.set(self.character_list[self.character_list.index(self.name.get().rstrip('\x00'))])
        self.set_defaults()

    def build(self):
        self.box.grid(column=0, row=0, pady=5, padx=5)
        self.not_loot_frame.grid(column=0, row=0, sticky='n')

        self.default_name_menu = Combobox(self.not_loot_frame, width=17,
                                          state='readonly',
                                          textvariable=self.character,
                                          values=self.character_list,
                                          postcommand=self.reset_character_list)
        self.default_name_menu.grid(column=0, row=0)

        self.new_name_frame.grid(column=0, row=1, ipady=2, ipadx=2)
        self.new_name_entry.grid()

        self.save.grid(column=1, row=0)

        self.aspect_frame.grid(column=1, row=1)
        self.solar_radio.grid(column=0, row=0, sticky='w')
        self.lunar_radio.grid(column=1, row=0, sticky='w')

        self.school_level_frame.grid(column=0, row=2)

        self.school_frame.grid(column=0, row=0)
        self.school_box.grid()

        self.level_frame.grid(column=1, row=0, ipady=1, padx=(11, 0))
        self.level_entry.grid(sticky='e')

        self.spell_frame.grid(column=0, row=3)
        for x in range(5):
            self.spell[x].grid(column=0, row=x, sticky='e')
            self.spell_level[x].grid(column=1, row=x, sticky='w')

        self.att_frame.grid(column=1, row=2, rowspan=2)
        for x in range(6):
            self.att_label[x].grid(column=0, row=x, sticky='e')
            self.att_num[x].grid(column=1, row=x, stick='w')
        self.protection_label.grid(column=0, row=6, stick='e')
        self.protection_entry.grid(column=1, row=6, stick='w')

        self.resist_frame.grid(column=0, row=4, columnspan=2)
        self.resist_menu1.grid(column=0, row=0)
        self.resist_amount_menu1.grid(column=1, row=0)
        self.resist_menu2.grid(column=0, row=1)
        self.resist_amount_menu2.grid(column=1, row=1)

        self.equipment_frame.grid(column=0, row=5, columnspan=2)

        self.weapon_frame.grid(column=0, rowspan=2)
        for x in range(3):
            self.weapon_menu[x].grid()

        self.armor_frame.grid(column=1, row=0)
        self.armor_menu.grid()

        self.shield_frame.grid(column=1, row=1)
        self.shield_menu.grid()

        self.skill_frame.grid(column=2, row=0, rowspan=24, padx=2)

        for skill in SKILLS:
            x = SKILLS.index(skill)
            skill_label = Label(self.skill_frame, text=skill, anchor='e', width=9)
            skill_label.grid(column=0, row=x)
            skill_num = Entry(self.skill_frame, textvariable=self.skills[x], width=4)
            skill_num.grid(column=1, row=x)
        self.shield_label.grid(column=0, row=23)
        self.shield_num.grid(column=1, row=23)

    def reset_character_list(self):
        self.character_list[:] = []
        self.character_addresses[:] = []
        self.character_list, self.character_addresses = get_major_name_lists(self.filename, self.addresses,
                                                                             self.name_length)
        self.default_name_menu['values'] = self.character_list
