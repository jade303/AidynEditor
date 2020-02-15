from functools import partial
from tkinter import Toplevel, Frame, LabelFrame, Entry, Button, Radiobutton, Label, StringVar, IntVar
from tkinter.ttk import Combobox

from lib.limits import limit_name_size, limit
from lib.variables import inv_WEAPONS, inv_SHIELDS, inv_ARMORS, inv_SPELLS, WEAPONS, SPELLS, ARMORS, SHIELDS, \
    ATTRIBUTES, SKILLS, DROP_CAT, ITEMS, inv_DROP_CAT, DROP_CAT_ADDRESSES, inv_DROP_ITEMS


class CharacterEdit:
    def __init__(self, filename, icon_dir, characters, character_addresses, name_length, char_type):
        win = Toplevel()
        win.resizable(False, False)
        if char_type == 0:
            win.title("Party Edit -- Edits are NEW GAME only")
            data_read = 74
        elif char_type == 1:
            win.title("Enemy and Loot Edit")
            data_read = 92
            drop_data_read = 34
        win.iconbitmap(icon_dir)
        data_seek = 44

        def set_defaults(*args):
            with open(filename, 'rb') as f:
                address = character_addresses[characters.index(character.get())]

                # get name that can be changed
                f.seek(address)
                name.set(f.read(name_length).decode("utf-8"))

                # seek address for everything else
                f.seek(address + data_seek)
                d = f.read(data_read).hex()

                # set aspect default
                aspect.set(d[1])

                # set skill defaults
                for s in skills:
                    sn = int(d[(skills.index(s) * 2) + 6] + d[(skills.index(s) * 2) + 7], 16)
                    if sn == 255:
                        sn = ''
                    s.set(sn)

                shi = int(d[146] + d[147], 16)
                if shi == 255:
                    shi = ''
                shield_skill.set(shi)

                # set attribute defaults
                for a in atts:
                    a.set(int(d[(atts.index(a) * 2) + 52] + d[(atts.index(a) * 2) + 53], 16))

                # set level default
                level.set(int(d[66] + d[67], 16))

                # set equipment defaults
                for w in weapons:
                    w.set(inv_WEAPONS[d[((weapons.index(w) * 4) + 70):(((weapons.index(w) * 4) + 70) + 4)].upper()])
                armor.set(inv_ARMORS[d[136:140].upper()])
                shield.set(inv_SHIELDS[d[142:146].upper()])

                # set school
                school.set(d[107])

                # 5 initial spells
                for s in spells:
                    s.set(inv_SPELLS[d[((spells.index(s) * 4) + 86):(((spells.index(s) * 4) + 86) + 4)].upper()])

                # spell levels
                for s in spell_levels:
                    s.set(int(d[((spell_levels.index(s) * 2) + 108)] + d[((spell_levels.index(s) * 2) + 108) + 1], 16))

                # set exp
                # exp.set(int(d[180] + d[181], 16))

                # enemy drop
                if char_type == 1:
                    enemy_drop_cat.set(inv_DROP_CAT[(d[182] + d[183]).upper()])
                    drop_cat.set(inv_DROP_CAT[(d[182] + d[183]).upper()])

        def set_drop_defaults(*args):
            with open(filename, 'rb') as f:
                address = DROP_CAT_ADDRESSES[list(DROP_CAT).index(drop_cat.get())]

                f.seek(address)
                d = f.read(drop_data_read).hex()

                gold_min.set(int((d[2] + d[3]) + (d[0] + d[1]), 16))
                gold_max.set(int(d[6] + d[7] + d[4] + d[5], 16))
                armor_chance.set(int(d[8] + d[9], 16))
                shield_chance.set(int(d[10] + d[11], 16))
                weap1_chance.set(int(d[12] + d[13], 16))
                weap2_chance.set(int(d[14] + d[15], 16))
                weap3_chance.set(int(d[16] + d[17], 16))
                reagent_chance.set(int(d[18] + d[19], 16))
                reagent_min.set(int(d[20] + d[21], 16))
                reagent_max.set(int(d[22] + d[23], 16))

                for i, c, mi, mx in zip(item, item_chance, item_min, item_max):
                    i.set(inv_DROP_ITEMS[d[(10 * item.index(i) + 24):(10 * item.index(i) + 28)].upper()])
                    c.set(int(d[(10 * item.index(i) + 28)] + d[(10 * item.index(i) + 29)], 16))
                    mi.set(int(d[(10 * item.index(i) + 30)] + d[(10 * item.index(i) + 31)], 16))
                    mx.set(int(d[(10 * item.index(i) + 32)] + d[(10 * item.index(i) + 33)], 16))

                for i, c in zip(other_items, other_items_chance):
                    i.set(inv_DROP_ITEMS[d[((other_items.index(i) * 6) + 44):
                                           ((other_items.index(i) * 6) + 48)].upper()])
                    c.set(int(d[((other_items.index(i) * 6) + 48)] + d[((other_items.index(i) * 6) + 49)], 16))

        def drop_save():
            with open(filename, 'rb+') as f:
                address = DROP_CAT_ADDRESSES[list(DROP_CAT).index(drop_cat.get())]

                new_value = gold_min.get()
                min_v2, min_v1 = divmod(int(new_value), 256)
                if min_v2 == 256:
                    min_v2 = 255
                    min_v1 = 255

                new_value = gold_max.get()
                max_v2, max_v1 = divmod(int(new_value), 256)
                if max_v2 == 256:
                    max_v2 = 255
                    max_v1 = 255

                towrite = [
                    int(min_v1), int(min_v2),
                    int(max_v1), int(max_v2),
                    int(armor_chance.get()),
                    int(shield_chance.get()),
                    int(weap1_chance.get()),
                    int(weap2_chance.get()),
                    int(weap3_chance.get()),
                    int(reagent_chance.get()),
                    int(reagent_min.get()),
                    int(reagent_max.get())
                ]

                for i in item:
                    towrite.append(int((ITEMS[i.get()])[:2], 16))
                    towrite.append(int((ITEMS[i.get()])[2:], 16))
                    towrite.append(int(item_chance[item.index(i)].get()))
                    towrite.append(int(item_min[item.index(i)].get()))
                    towrite.append(int(item_max[item.index(i)].get()))

                for i, c in zip(other_items, other_items_chance):
                    towrite.append(int((ITEMS[i.get()])[:2], 16))
                    towrite.append(int((ITEMS[i.get()])[2:], 16))
                    towrite.append(int(c.get()))

                f.seek(address)
                for i in towrite:
                    f.write(i.to_bytes(1, byteorder='big'))

        def write():
            with open(filename, 'rb+') as f:
                address = (character_addresses[characters.index(character.get())])
                # write new name to file
                new_name = bytearray(name.get(), 'utf-8')
                if len(new_name) < name_length:
                    while len(new_name) < name_length:
                        new_name.append(0x00)
                f.seek(address)
                f.write(new_name)

                f.seek(address + data_seek)
                d = f.read(data_read).hex()

                towrite = [aspect.get(), int(d[3] + d[4], 16),
                           int(d[5] + d[6], 16)]
                for i in skills:
                    j = i.get()
                    if j == '':
                        j = 255
                    towrite.append(int(j))

                for i in atts:
                    j = i.get()
                    towrite.append(int(j))

                towrite.append(int(d[64] + d[65], 16))
                towrite.append(int(level.get()))
                towrite.append(int(d[68] + d[69], 16))

                for i in weapons:
                    towrite.append(int((WEAPONS[i.get()])[:2], 16))
                    towrite.append(int((WEAPONS[i.get()])[2:], 16))

                towrite.append(int(d[82] + d[83], 16))
                towrite.append(int(d[84] + d[85], 16))

                for i in spells:
                    towrite.append(int((SPELLS[i.get()])[:2], 16))
                    towrite.append(int((SPELLS[i.get()])[2:], 16))
                towrite.append(school.get())

                for i in spell_levels:
                    towrite.append(int(i.get()))

                for i in range(118, 135, 2):
                    towrite.append(int(d[i] + d[i + 1], 16))

                towrite.append(int((ARMORS[armor.get()])[:2], 16))
                towrite.append(int((ARMORS[armor.get()])[2:], 16))
                towrite.append(int(d[140] + d[141], 16))
                towrite.append(int((SHIELDS[shield.get()])[:2], 16))
                towrite.append(int((SHIELDS[shield.get()])[2:], 16))

                shi = shield_skill.get()
                if shi == '':
                    shi = 255
                towrite.append(int(shi))

                if char_type == 1:
                    for i in range(148, 181, 2):
                        towrite.append(int(d[i] + d[i + 1], 16))
                        towrite.append(int((DROP_CAT[enemy_drop_cat.get()]), 16))

                f.seek(address + data_seek)
                for i in towrite:
                    f.write(i.to_bytes(1, byteorder='big'))

        def build():
            # column 0, row 0
            box = Frame(win)
            box.grid(column=0, row=0)

            lawfulgood_frame = Frame(box)
            lawfulgood_frame.grid(column=0, row=0)
            new_name_frame = LabelFrame(lawfulgood_frame, text="New Name")
            new_name_frame.grid(column=0, row=1)
            new_name_frame.config(width=18)

            default_name_menu = Combobox(lawfulgood_frame, textvariable=character, values=characters)
            default_name_menu.grid(column=0, row=0)
            default_name_menu.config(width=18)

            new_name_entry = Entry(new_name_frame, textvariable=name)
            new_name_entry.grid(column=0, row=1)
            new_name_entry.config(width=18)

            save = Button(lawfulgood_frame, text="Save", command=write)
            save.grid(column=1, row=0)
            save.config(width=8)

            # column 0, row 1
            lawfulneutral_frame = Frame(box)
            lawfulneutral_frame.grid(column=0, row=1)
            aspect_frame = LabelFrame(lawfulneutral_frame, text='Aspect:')
            aspect_frame.grid(column=0, row=0)
            level_frame = LabelFrame(lawfulneutral_frame, text='Level:')
            level_frame.grid(column=1, row=0)
            school_frame = LabelFrame(lawfulneutral_frame, text='School')
            school_frame.grid(column=0, row=1)
            att_frame = LabelFrame(lawfulneutral_frame, text='Attributes')
            att_frame.grid(column=1, row=1)

            solar_radio = Radiobutton(aspect_frame, text='Solar', variable=aspect, value='2')
            solar_radio.grid(column=0, row=0, sticky='w')
            lunar_radio = Radiobutton(aspect_frame, text='Lunar', variable=aspect, value='1')
            lunar_radio.grid(column=1, row=0, sticky='w')

            level_entry = Entry(level_frame, textvariable=level, width=4)
            level_entry.grid(column=1, row=1)

            school0 = Radiobutton(school_frame, text='Chaos', variable=school, value='0')
            school0.grid(sticky='w')
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

            for att in ATTRIBUTES:
                x = ATTRIBUTES.index(att)
                att_label = Label(att_frame, text=att, anchor='e', width=9)
                att_label.grid(column=0, row=x)
                att_num = Entry(att_frame, textvariable=atts[x], width=4)
                att_num.grid(column=1, row=x)

            # column 0, row 2
            lawfulevil_frame = LabelFrame(box, text='Equipment')
            lawfulevil_frame.grid(column=0, row=2)
            weapon_frame = LabelFrame(lawfulevil_frame, text='Weapons')
            weapon_frame.grid(column=0, rowspan=2)
            armor_frame = LabelFrame(lawfulevil_frame, text='Armor')
            armor_frame.grid(column=1, row=0)
            shield_frame = LabelFrame(lawfulevil_frame, text='Shield')
            shield_frame.grid(column=1, row=1)

            for w in weapons:
                weapon_menu = Combobox(weapon_frame, textvariable=w, values=list(WEAPONS.keys()))
                weapon_menu.grid()
                weapon_menu.config(width=16)
            armor_menu = Combobox(armor_frame, textvariable=armor, values=list(ARMORS.keys()))
            armor_menu.grid(column=1)
            armor_menu.config(width=16)
            shield_menu = Combobox(shield_frame, textvariable=shield, values=list(SHIELDS.keys()))
            shield_menu.grid()
            shield_menu.config(width=16)

            # column 1, row all
            neutralgood_frame = LabelFrame(box, text='Skills\n(blank = cannot learn)')
            neutralgood_frame.grid(column=1, row=0, rowspan=23)

            for skill in SKILLS:
                x = SKILLS.index(skill)
                skill_label = Label(neutralgood_frame, text=skill, anchor='e', width=9)
                skill_label.grid(column=0, row=x)
                skill_num = Entry(neutralgood_frame, textvariable=skills[x], width=4)
                skill_num.grid(column=1, row=x)
            shield_label = Label(neutralgood_frame, text='Shield', anchor='e', width=9)
            shield_label.grid(column=0, row=23)
            shield_num = Entry(neutralgood_frame, textvariable=shield_skill, width=4)
            shield_num.grid(column=1, row=23)

            # column 0, row 4, column 2, row all
            chaoticgood_frame = LabelFrame(box, text='Spells and Spell Level')
            chaoticgood_frame.grid(column=0, row=3)
            for s in spells:
                x = spells.index(s)
                spell = Combobox(chaoticgood_frame, textvariable=s, values=list(SPELLS.keys()))
                spell.grid(column=0, row=x)
                spell.config(width=16)
                spell_level = Entry(chaoticgood_frame, textvariable=spell_levels[spells.index(s)])
                spell_level.grid(column=1, row=x)
                spell_level.config(width=4)

            if char_type == 1:
                """
                exp_frame = LabelFrame(win, text='EXP given')
                exp_frame.grid(column=0, row=4)
                exp_entry = Entry(exp_frame, textvariable=exp)
                exp_entry.grid(column=0, row=0)
                exp_note = Label(exp_frame, text='(there is some unknown \nformula involved with EXP)')
                exp_note.grid(column=0, row=1)
                exp_note.config(font=(None, 8))
                """

                enemy_drop_cat_label = LabelFrame(box, text='Current Enemy Loot Type')
                enemy_drop_cat_label.grid(row=4, column=0, pady=12)
                enemy_drop_cat_box = Combobox(enemy_drop_cat_label, textvariable=enemy_drop_cat,
                                              values=list(DROP_CAT.keys()))
                enemy_drop_cat_box.grid(column=0, row=0)

                drop_frame = LabelFrame(win, text='Loot Editing:', bd=4)
                drop_frame.grid(column=2, row=0)

                drop_box_label = Label(drop_frame, text='Loot Category:')
                drop_box_label.grid(column=0, row=0, sticky='e')
                drop_box = Combobox(drop_frame, textvariable=drop_cat, values=list(DROP_CAT.keys()))
                drop_box.grid(column=1, row=0, sticky='w')

                save = Button(drop_frame, text="Save Loot Changes", command=drop_save, width=18)
                save.grid(column=0, row=1, columnspan=2, pady=12)

                drop_stats = LabelFrame(drop_frame, text='Loot details\n(editing these affects all enemies with the '
                                                         'same drop type)')
                drop_stats.grid(column=0, row=2, columnspan=2)

                gold_min_label = Label(drop_stats, text='Random Gold MIN/MAX:')
                gold_min_label.grid(column=0, row=0, sticky='e')
                gold_min_entry = Entry(drop_stats, textvariable=gold_min, width=6)
                gold_min_entry.grid(column=1, row=0, sticky='e')
                gold_max_entry = Entry(drop_stats, textvariable=gold_max, width=6)
                gold_max_entry.grid(column=2, row=0, sticky='e')

                armor_chance_label = Label(drop_stats, text='% chance to drop armor:', anchor='e')
                armor_chance_label.grid(column=0, row=2, sticky='e')
                armor_chance_entry = Entry(drop_stats, textvariable=armor_chance, width=4)
                armor_chance_entry.grid(column=1, row=2, sticky='e')

                shield_chance_label = Label(drop_stats, text='% chance to drop shield:', anchor='e')
                shield_chance_label.grid(column=0, row=3, sticky='e')
                shield_chance_entry = Entry(drop_stats, textvariable=shield_chance, width=4)
                shield_chance_entry.grid(column=1, row=3, sticky='e')

                weap1_chance_label = Label(drop_stats, text='% chance to drop weapon 1:')
                weap1_chance_label.grid(column=0, row=4, sticky='e')
                weap1_chance_entry = Entry(drop_stats, textvariable=weap1_chance, width=4)
                weap1_chance_entry.grid(column=1, row=4, sticky='e')

                weap2_chance_label = Label(drop_stats, text='% chance to drop weapon 2:')
                weap2_chance_label.grid(column=0, row=5, sticky='e')
                weap2_chance_entry = Entry(drop_stats, textvariable=weap2_chance, width=4)
                weap2_chance_entry.grid(column=1, row=5, sticky='e')

                weap3_chance_label = Label(drop_stats, text='% chance to drop weapon 3:')
                weap3_chance_label.grid(column=0, row=6, sticky='e')
                weap3_chance_entry = Entry(drop_stats, textvariable=weap3_chance, width=4)
                weap3_chance_entry.grid(column=1, row=6, sticky='e')

                reagent_chance_label = Label(drop_stats, text='% chance to drop random reagent:')
                reagent_chance_label.grid(column=0, row=7, sticky='e')
                reagent_chance_entry = Entry(drop_stats, textvariable=reagent_chance, width=4)
                reagent_chance_entry.grid(column=1, row=7, sticky='e')

                reagent_min_label = Label(drop_stats, text='MIN/MAX reagent drop:')
                reagent_min_label.grid(column=0, row=8, sticky='e')
                reagent_min_entry = Entry(drop_stats, textvariable=reagent_min, width=4)
                reagent_min_entry.grid(column=1, row=8, sticky='e')
                reagent_max_entry = Entry(drop_stats, textvariable=reagent_max, width=4)
                reagent_max_entry.grid(column=2, row=8, sticky='w')

                for i in item:
                    item_frame = LabelFrame(drop_stats, text=('Item ' + str(item.index(i))))
                    item_frame.grid(column=0, row=(9 + item.index(i)), sticky='e', columnspan=2)
                    item_box = Combobox(item_frame, textvariable=i, values=list(ITEMS.keys()), width=28)
                    item_box.grid(column=0, row=0, columnspan=3)
                    item_chance_label = Label(item_frame, text='% chance to drop item:')
                    item_chance_label.grid(column=0, row=1, sticky='e')
                    item_chance_entry = Entry(item_frame, textvariable=item_chance[item.index(i)], width=4)
                    item_chance_entry.grid(column=1, row=1, sticky='e')
                    item_min_max = Label(item_frame, text='MIN/MAX item amount:')
                    item_min_max.grid(column=0, row=2)
                    item_min_entry = Entry(item_frame, textvariable=item_min[item.index(i)], width=4)
                    item_min_entry.grid(column=1, row=2, sticky='e')
                    item_max_entry = Entry(item_frame, textvariable=item_max[item.index(i)], width=4)
                    item_max_entry.grid(column=2, row=2, sticky='w')

                item_more = LabelFrame(drop_stats, text='Items 3-6 and drop %')
                item_more.grid(column=0, row=11, sticky='e', columnspan=2)

                for i in other_items:
                    other_item_frame = LabelFrame(item_more, text=('Item' + str(other_items.index(i) + 3)))
                    other_item_frame.grid(column=0, row=other_items.index(i))
                    other_item_box = Combobox(other_item_frame, textvariable=i, values=list(ITEMS.keys()), width=28)
                    other_item_box.grid(column=0, row=0, columnspan=2)
                    other_item_chance_label = Label(other_item_frame, text='% chance to drop item:')
                    other_item_chance_label.grid(column=0, row=1, sticky='e')
                    other_item_chance_entry = Entry(other_item_frame,
                                                    textvariable=other_items_chance[other_items.index(i)], width=4)
                    other_item_chance_entry.grid(column=1, row=1, sticky='e')

        # initial declaration of variables
        if char_type == 1:
            enemy_drop_cat = StringVar()
            drop_cat = StringVar()
            drop_cat.trace('w', set_drop_defaults)
            gold_min = StringVar()
            gold_min.trace('w', partial(limit, gold_min, 65535))
            gold_max = StringVar()
            gold_max.trace('w', partial(limit, gold_max, 65535))
            armor_chance = StringVar()
            armor_chance.trace('w', partial(limit, armor_chance, 100))
            shield_chance = StringVar()
            shield_chance.trace('w', partial(limit, shield_chance, 100))
            weap1_chance = StringVar()
            weap1_chance.trace('w', partial(limit, weap1_chance, 100))
            weap2_chance = StringVar()
            weap2_chance.trace('w', partial(limit, weap2_chance, 100))
            weap3_chance = StringVar()
            weap3_chance.trace('w', partial(limit, weap3_chance, 100))
            reagent_chance = StringVar()
            reagent_chance.trace('w', partial(limit, reagent_chance, 100))
            reagent_min = StringVar()
            reagent_min.trace('w', partial(limit, reagent_min, 99))
            reagent_max = StringVar()
            reagent_max.trace('w', partial(limit, reagent_max, 99))

            item, item_chance, item_min, item_max = ([] for i in range(4))
            for i in range(2):
                i = StringVar()
                item.append(i)
                c = StringVar()
                c.trace('w', partial(limit, c, 100))
                item_chance.append(c)
                mi = StringVar()
                mi.trace('w', partial(limit, mi, 99))
                item_min.append(mi)
                mx = StringVar()
                mx.trace('w', partial(limit, mx, 99))
                item_max.append(mx)

            other_items, other_items_chance = ([] for i in range(2))
            for i in range(4):
                i = StringVar()
                other_items.append(i)
                c = StringVar()
                c.trace('w', partial(limit, c, 100))
                other_items_chance.append(c)

        character = StringVar()
        character.trace('w', set_defaults)

        name = StringVar()
        name.trace('w', partial(limit_name_size, name, name_length))
        aspect = IntVar()
        skills = []
        for _ in SKILLS:
            i = StringVar()
            i.trace('w', partial(limit, i, 10))
            skills.append(i)
        shield_skill = StringVar()
        shield_skill.trace('w', partial(limit, shield_skill, 10))
        atts = []
        for _ in ATTRIBUTES:
            i = StringVar()
            atts.append(i)
            if atts.index(i) in range(3) or atts.index(i) == 4:
                i.trace('w', partial(limit, i, 30))
            elif atts.index(i) == 3:
                i.trace('w', partial(limit, i, 40))
            elif atts.index(i) == 5:
                i.trace('w', partial(limit, i, 120))
        level = StringVar()
        level.trace('w', partial(limit, level, 40))
        weapons = [StringVar() for i in range(3)]
        spells = [StringVar() for i in range(5)]
        school = IntVar()
        spell_levels = []
        for i in range(5):
            i = StringVar()
            i.trace('w', partial(limit, i, 15))
            spell_levels.append(i)
        armor = StringVar()
        shield = StringVar()
        # exp = StringVar()

        character.set(characters[0])
        build()
