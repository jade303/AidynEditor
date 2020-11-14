from functools import partial
from tkinter import StringVar, LabelFrame, Label, Button
from tkinter.ttk import Combobox, Entry

from lib.characters import Characters
from lib.fuctions import get_major_loot_lists, int_cast, limit, limit_name_size
from lib.variables import DROP_CAT, RESIST, RESIST_AMOUNTS, SCHOOL


class EnemyEdit(Characters):
    def __init__(self, f, i, a, n, r, t):
        super().__init__(f, i, a, n, r, t)
        self.win.title("Enemy and Loot Edit")
        self.drop_data_read = 34
        self.loot_name_length = 19

        self.loot_name_list, self.loot_code_list, self.loot_address_list = \
            get_major_loot_lists(self.filename, DROP_CAT, self.loot_name_length)

        # variables
        self.exp = StringVar()
        self.exp.set(0)
        self.exp.trace('w', partial(limit, self.exp, 255))
        self.exp.trace('w', self.update_exp)
        self.enemy_drop_cat = StringVar()
        self.drop_cat = StringVar()
        self.drop_cat.trace('w', self.set_drop_defaults)
        self.loot_name = StringVar()
        self.loot_name.trace('w', partial(limit_name_size, self.loot_name, self.loot_name_length))
        self.gold_min = StringVar()
        self.gold_min.trace('w', partial(limit, self.gold_min, 65535))
        self.gold_max = StringVar()
        self.gold_max.trace('w', partial(limit, self.gold_max, 65535))
        self.armor_chance = StringVar()
        self.armor_chance.trace('w', partial(limit, self.armor_chance, 100))
        self.shield_chance = StringVar()
        self.shield_chance.trace('w', partial(limit, self.shield_chance, 100))
        self.weap1_chance = StringVar()
        self.weap1_chance.trace('w', partial(limit, self.weap1_chance, 100))
        self.weap2_chance = StringVar()
        self.weap2_chance.trace('w', partial(limit, self.weap2_chance, 100))
        self.weap3_chance = StringVar()
        self.weap3_chance.trace('w', partial(limit, self.weap3_chance, 100))
        self.reagent_chance = StringVar()
        self.reagent_chance.trace('w', partial(limit, self.reagent_chance, 100))
        self.reagent_min = StringVar()
        self.reagent_min.trace('w', partial(limit, self.reagent_min, 99))
        self.reagent_max = StringVar()
        self.reagent_max.trace('w', partial(limit, self.reagent_max, 99))

        self.item, self.item_chance, self.item_min, self.item_max = ([] for i in range(4))
        for i in range(2):
            i = StringVar()
            self.item.append(i)
            c = StringVar()
            c.trace('w', partial(limit, c, 100))
            self.item_chance.append(c)
            mi = StringVar()
            mi.trace('w', partial(limit, mi, 99))
            self.item_min.append(mi)
            mx = StringVar()
            mx.trace('w', partial(limit, mx, 99))
            self.item_max.append(mx)

        self.other_items, self.other_items_chance = ([] for i in range(2))
        for i in range(4):
            i = StringVar()
            self.other_items.append(i)
            c = StringVar()
            c.trace('w', partial(limit, c, 100))
            self.other_items_chance.append(c)

        # build items
        self.enemy_drop_cat_box = Combobox()
        self.exp_total = Entry()
        self.drop_box = Combobox()

        # run
        self.build()
        self.character.set(self.character_list[0])

    def update_exp(self, *args):
        if self.exp.get() == '':
            self.exp_total.configure(text=' = ')
        else:
            xp = 75 * int(self.exp.get())
            if xp > 19125:
                xp = 19125
            self.exp_total.configure(text=' = ' + str(xp))

    def reset_loot_list(self):
        self.loot_name_list[:] = []
        self.loot_code_list[:] = []
        self.loot_address_list[:] = []
        self.loot_name_list, self.loot_code_list, self.loot_address_list = \
            get_major_loot_lists(self.filename, DROP_CAT, self.loot_name_length)
        self.drop_box['values'] = self.loot_name_list
        self.enemy_drop_cat_box['values'] = self.loot_name_list

    def set_defaults(self, *args):
        super().set_defaults()

        with open(self.filename, 'rb') as f:
            address = self.character_addresses[self.default_name_menu.current()] + 134
            f.seek(address)
            d = f.read(2).hex()
            self.exp.set(int(d[0] + d[1], 16))
            self.drop_cat.set(self.loot_name_list[self.loot_code_list.index((d[2] + d[3]).upper())])
            self.enemy_drop_cat.set(self.drop_cat.get())

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
                towrite.append(int(self.inv_spell_dic[i.get()][:2], 16))
                towrite.append(int(self.inv_spell_dic[i.get()][2:], 16))

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

            towrite.append(int(RESIST[self.resist1a.get()], 16))
            towrite.append(int(RESIST_AMOUNTS[self.resist1b.get()], 16))
            towrite.append(int(RESIST[self.resist2a.get()], 16))
            towrite.append(int(RESIST_AMOUNTS[self.resist2b.get()], 16))

            for i in range(156, 179, 2):
                towrite.append(d[i] + d[i + 1])
            towrite.append(self.exp.get())
            towrite.append(int(self.loot_code_list[self.loot_name_list.index(self.enemy_drop_cat.get())], 16))

            f.seek(address + self.data_seek)
            for item in towrite:
                item = int_cast(item)
                f.write(item.to_bytes(1, byteorder='big'))

            self.reset_character_list()
            self.character.set(self.character_list[self.character_list.index(self.name.get().rstrip('\x00'))])
        self.set_defaults()

    def set_drop_defaults(self, *args):
        with open(self.filename, 'rb') as f:
            address = self.loot_address_list[self.drop_box.current()]

            f.seek(address)
            self.loot_name.set(f.read(self.loot_name_length).decode("utf-8"))

            f.seek(address + 22)
            d = f.read(self.drop_data_read).hex()

            self.gold_min.set(int((d[2] + d[3]) + (d[0] + d[1]), 16))
            self.gold_max.set(int(d[6] + d[7] + d[4] + d[5], 16))
            self.armor_chance.set(int(d[8] + d[9], 16))
            self.shield_chance.set(int(d[10] + d[11], 16))
            self.weap1_chance.set(int(d[12] + d[13], 16))
            self.weap2_chance.set(int(d[14] + d[15], 16))
            self.weap3_chance.set(int(d[16] + d[17], 16))
            self.reagent_chance.set(int(d[18] + d[19], 16))
            self.reagent_min.set(int(d[20] + d[21], 16))
            self.reagent_max.set(int(d[22] + d[23], 16))

            for i, c, mi, mx in zip(self.item, self.item_chance, self.item_min, self.item_max):
                x = d[(10 * self.item.index(i) + 24):(10 * self.item.index(i) + 28)].upper()
                if x == '0B10':
                    x = '0000'
                i.set(self.major_dic[x])
                c.set(int(d[(10 * self.item.index(i) + 28)] + d[(10 * self.item.index(i) + 29)], 16))
                mi.set(int(d[(10 * self.item.index(i) + 30)] + d[(10 * self.item.index(i) + 31)], 16))
                mx.set(int(d[(10 * self.item.index(i) + 32)] + d[(10 * self.item.index(i) + 33)], 16))

            for i, c in zip(self.other_items, self.other_items_chance):
                i.set(self.major_dic[d[((self.other_items.index(i) * 6) + 44):
                                       ((self.other_items.index(i) * 6) + 48)].upper()])
                c.set(int(d[((self.other_items.index(i) * 6) + 48)] + d[((self.other_items.index(i) * 6) + 49)], 16))

    def write_drop(self):
        with open(self.filename, 'rb+') as f:
            address = self.loot_address_list[self.drop_box.current()]

            new_loot_name = bytearray(self.loot_name.get(), 'utf-8')
            if len(new_loot_name) < self.loot_name_length:
                while len(new_loot_name) < self.loot_name_length:
                    new_loot_name.append(0x00)
            f.seek(address)
            f.write(new_loot_name)

            new_value = self.gold_min.get()
            min_v2, min_v1 = divmod(int(new_value), 256)
            if min_v2 == 256:
                min_v2 = 255
                min_v1 = 255

            new_value = self.gold_max.get()
            max_v2, max_v1 = divmod(int(new_value), 256)
            if max_v2 == 256:
                max_v2 = 255
                max_v1 = 255

            towrite = [
                min_v1, min_v2,
                max_v1, max_v2,
                self.armor_chance.get(),
                self.shield_chance.get(),
                self.weap1_chance.get(),
                self.weap2_chance.get(),
                self.weap3_chance.get(),
                self.reagent_chance.get(),
                self.reagent_min.get(),
                self.reagent_max.get()
            ]

            for i in self.item:
                towrite.append(int(self.inv_major_dic[i.get()][:2], 16))
                towrite.append(int(self.inv_major_dic[i.get()][2:], 16))
                towrite.append(self.item_chance[self.item.index(i)].get())
                towrite.append(self.item_min[self.item.index(i)].get())
                towrite.append(self.item_max[self.item.index(i)].get())

            for i, c in zip(self.other_items, self.other_items_chance):
                towrite.append(int(self.inv_major_dic[i.get()][:2], 16))
                towrite.append(int(self.inv_major_dic[i.get()][2:], 16))
                towrite.append(c.get())

            f.seek(address + 22)
            for t in towrite:
                t = int_cast(t)
                f.write(t.to_bytes(1, byteorder='big'))

            self.reset_loot_list()
            if self.drop_cat.get() == self.enemy_drop_cat.get():
                self.drop_cat.set(self.loot_name_list[self.loot_name_list.index(self.loot_name.get().rstrip('\x00'))])
                self.enemy_drop_cat.set(self.drop_cat.get())
            else:
                self.drop_cat.set(self.loot_name_list[self.loot_name_list.index(self.loot_name.get().rstrip('\x00'))])
        self.set_drop_defaults()

    def build(self):
        super().build()

        self.skill_frame.configure(text='Skills')

        exp_frame = LabelFrame(self.not_loot_frame, text='EXP given')
        exp_frame.grid(column=0, row=8, columnspan=2)
        exp_label = Label(exp_frame, text='75 x ', width=6)
        exp_label.grid(column=0, row=0, sticky='e')
        exp_entry = Entry(exp_frame, textvariable=self.exp, width=4)
        exp_entry.grid(column=1, row=0, sticky='w')
        self.exp_total = Label(exp_frame, text=(' = ' + str(75 * int(self.exp.get()))), width=9)
        self.exp_total.grid(column=2, row=0, sticky='w')

        enemy_drop_cat_label = LabelFrame(self.not_loot_frame, text='Current Enemy Loot Type')
        enemy_drop_cat_label.grid(column=0, row=7, columnspan=2)
        self.enemy_drop_cat_box = Combobox(enemy_drop_cat_label, state='readonly',
                                           textvariable=self.enemy_drop_cat,
                                           values=self.loot_name_list,
                                           postcommand=self.reset_loot_list)
        self.enemy_drop_cat_box.grid(column=0, row=0)

        drop_frame = LabelFrame(self.box, text='Loot Editing:', bd=4)
        drop_frame.grid(column=1, row=0, ipadx=2)

        drop_box_label = Label(drop_frame, text='Loot Category:')
        drop_box_label.grid(column=0, row=0, sticky='e')
        self.drop_box = Combobox(drop_frame, state='readonly', width=19,
                                 textvariable=self.drop_cat,
                                 values=self.loot_name_list,
                                 postcommand=self.reset_loot_list)
        self.drop_box.grid(column=1, row=0, sticky='w')

        new_loot_name_frame = LabelFrame(drop_frame, text="Change Loot Name")
        new_loot_name_frame.grid(column=0, row=1, columnspan=2)
        new_loot_name_entry = Entry(new_loot_name_frame, textvariable=self.loot_name, width=19)
        new_loot_name_entry.grid()

        save = Button(drop_frame, text="Save Loot Changes", width=18,
                      command=self.write_drop)
        save.grid(column=0, row=2, columnspan=2, pady=8)

        drop_stats = LabelFrame(drop_frame, text='Loot details\n(editing these affects all enemies\n with the '
                                                 'same loot type)\n')
        drop_stats.grid(column=0, row=3, columnspan=2)

        gold_min_label = Label(drop_stats, text='Random Gold MIN/MAX')
        gold_min_label.grid(column=0, row=0, sticky='e')
        gold_min_entry = Entry(drop_stats, textvariable=self.gold_min, width=5)
        gold_min_entry.grid(column=1, row=0, sticky='e')
        gold_max_entry = Entry(drop_stats, textvariable=self.gold_max, width=5)
        gold_max_entry.grid(column=2, row=0, sticky='w')

        drop_chance_frame = LabelFrame(drop_stats, text='Drop Chance')
        drop_chance_frame.grid(column=0, row=2, columnspan=3)

        armor_chance_label = Label(drop_chance_frame, text='Armor %', anchor='e')
        armor_chance_label.grid(column=0, row=0, sticky='e')
        armor_chance_entry = Entry(drop_chance_frame, textvariable=self.armor_chance, width=5)
        armor_chance_entry.grid(column=1, row=0, sticky='w')

        shield_chance_label = Label(drop_chance_frame, text='Shield %', anchor='e')
        shield_chance_label.grid(column=0, row=1, sticky='e')
        shield_chance_entry = Entry(drop_chance_frame, textvariable=self.shield_chance, width=5)
        shield_chance_entry.grid(column=1, row=1, sticky='w')

        weap1_chance_label = Label(drop_chance_frame, text='Weapon 1 %')
        weap1_chance_label.grid(column=0, row=2, sticky='e')
        weap1_chance_entry = Entry(drop_chance_frame, textvariable=self.weap1_chance, width=5)
        weap1_chance_entry.grid(column=1, row=2, sticky='w')

        weap2_chance_label = Label(drop_chance_frame, text='Weapon 2 %')
        weap2_chance_label.grid(column=0, row=3, sticky='e')
        weap2_chance_entry = Entry(drop_chance_frame, textvariable=self.weap2_chance, width=5)
        weap2_chance_entry.grid(column=1, row=3, sticky='w')

        weap3_chance_label = Label(drop_chance_frame, text='Weapon 3 %')
        weap3_chance_label.grid(column=0, row=4, sticky='e')
        weap3_chance_entry = Entry(drop_chance_frame, textvariable=self.weap3_chance, width=5)
        weap3_chance_entry.grid(column=1, row=4, sticky='w')

        reagent_chance_label = Label(drop_chance_frame, text='Random Reagent %')
        reagent_chance_label.grid(column=0, row=5, sticky='e')
        reagent_chance_entry = Entry(drop_chance_frame, textvariable=self.reagent_chance, width=5)
        reagent_chance_entry.grid(column=1, row=5, sticky='w')

        reagent_min_label = Label(drop_stats, text='Reagent drop MIN/MAX')
        reagent_min_label.grid(column=0, row=4, sticky='e')
        reagent_min_entry = Entry(drop_stats, textvariable=self.reagent_min, width=5)
        reagent_min_entry.grid(column=1, row=4, sticky='e')
        reagent_max_entry = Entry(drop_stats, textvariable=self.reagent_max, width=5)
        reagent_max_entry.grid(column=2, row=4, sticky='w')

        for i in self.item:
            item_frame = LabelFrame(drop_stats, text=('Item ' + str(self.item.index(i) + 1)))
            item_frame.grid(column=0, row=(5 + self.item.index(i)), columnspan=3)
            item_box = Combobox(item_frame, textvariable=i, values=list(self.major_dic.values()),
                                width=28, state='readonly')
            item_box.grid(column=0, row=0, columnspan=3)
            item_chance_label = Label(item_frame, text='Drop Chance')
            item_chance_label.grid(column=0, row=1, sticky='e')
            item_chance_entry = Entry(item_frame, textvariable=self.item_chance[self.item.index(i)], width=4)
            item_chance_entry.grid(column=1, row=1, sticky='e')
            item_min_max = Label(item_frame, text='Item amount MIN/MAX')
            item_min_max.grid(column=0, row=2)
            item_min_entry = Entry(item_frame, textvariable=self.item_min[self.item.index(i)], width=4)
            item_min_entry.grid(column=1, row=2, sticky='e')
            item_max_entry = Entry(item_frame, textvariable=self.item_max[self.item.index(i)], width=4)
            item_max_entry.grid(column=2, row=2, sticky='w')

        for i in self.other_items:
            other_item_frame = LabelFrame(drop_stats, text=('Item ' + str(self.other_items.index(i) + 3)))
            other_item_frame.grid(column=0, row=(7 + self.other_items.index(i)), columnspan=3)
            other_item_box = Combobox(other_item_frame, textvariable=i, values=list(self.major_dic.values()),
                                      width=28, state='readonly')
            other_item_box.grid(column=0, row=0, columnspan=2)
            other_item_chance_label = Label(other_item_frame, text='Drop Chance')
            other_item_chance_label.grid(column=0, row=1, sticky='e')
            other_item_chance_entry = Entry(other_item_frame,
                                            textvariable=self.other_items_chance[self.other_items.index(i)], width=4)
            other_item_chance_entry.grid(column=1, row=1, sticky='w')
