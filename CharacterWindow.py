from functools import partial
from tkinter import Toplevel, Frame, LabelFrame, Entry, Button, Radiobutton, Label, StringVar, IntVar
from tkinter.ttk import Combobox
from variables import WEAPONS, inv_WEAPONS, ARMORS, inv_ARMORS, SHIELDS, inv_SHIELDS, \
    SPELLS, inv_SPELLS, ATTRIBUTES, SKILLS


class CharacterEdit:
    def __init__(self, filename, characters, character_addresses, name_length, title):
        charwin = Toplevel()
        charwin.resizable(False, False)
        if title == 1:
            charwin.title("Party Edit -- Edits are NEW GAME only")
        elif title == 0:
            charwin.title("Enemy Edit")
        filename = filename
        characters = characters
        character_addresses = character_addresses
        name_length = name_length

        def read_default_values(*args):
            with open(filename, 'rb') as f:
                address = character_addresses[characters.index(character.get())]

                # get name that can be changed
                f.seek(address - 44)
                name.set(f.read(name_length).decode("utf-8"))

                # seek address for everything else
                f.seek(address)
                character_data = f.read(74)
                d = character_data.hex()

                # set aspect default
                aspect.set(d[1])

                # set skill defaults
                for s in skills:
                    sa = skills.index(s) * 2
                    sn = int(d[sa + 6] + d[sa + 7], 16)
                    if sn == 255:
                        sn = ''
                    s.set(sn)

                shi = int(d[146] + d[147], 16)
                if shi == 255:
                    shi = ''
                shield_skill.set(shi)

                # set attribute defaults
                for a in atts:
                    aa = atts.index(a) * 2
                    an = int(d[aa + 52] + d[aa + 53], 16)
                    if an == 255:
                        an = ''
                    a.set(an)

                # set level default
                level.set(int(d[66] + d[67], 16))

                # set equipment defaults
                for w in weapons:
                    x = (weapons.index(w) * 4) + 70
                    y = x + 4
                    w.set(inv_WEAPONS[d[x:y].upper()])
                armor.set(inv_ARMORS[d[136:140].upper()])
                shield.set(inv_SHIELDS[d[142:146].upper()])

                # set school
                school.set(d[107])

                # 5 initial spells
                for s in spells:
                    x = (spells.index(s) * 4) + 86
                    y = x + 4
                    s.set(inv_SPELLS[d[x:y].upper()])

                # spell levels
                for s in spell_levels:
                    x = (spell_levels.index(s) * 2) + 108
                    s.set(int(d[x] + d[x + 1], 16))

        def write_to_file():
            with open(filename, 'rb+') as f:
                address = (character_addresses[characters.index(character.get())])
                # write new name to file
                new_name = bytearray(name.get(), 'utf-8')
                if len(new_name) < name_length:
                    while len(new_name) < name_length:
                        new_name.append(0x00)
                f.seek(address - 44)
                f.write(new_name)

                f.seek(address)
                character_data = f.read(74)
                d = character_data.hex()

                towrite = [aspect.get(), int(d[3] + d[4]),
                           int(d[5] + d[6])]
                for i in skills:
                    j = i.get()
                    if j == '':
                        j = 255
                    towrite.append(int(j))

                for i in atts:
                    j = i.get()
                    towrite.append(int(j))

                towrite.append(int((d[64] + d[65])))
                towrite.append(level.get())
                towrite.append(int((d[68] + d[69])))

                for i in weapons:
                    towrite.append(int((WEAPONS[i.get()])[:2], 16))
                    towrite.append(int((WEAPONS[i.get()])[2:], 16))

                towrite.append(int((d[82] + d[83])))
                towrite.append(int((d[84] + d[85])))

                for i in spells:
                    towrite.append(int((SPELLS[i.get()])[:2], 16))
                    towrite.append(int((SPELLS[i.get()])[2:], 16))

                towrite.append(school.get())

                for i in spell_levels:
                    towrite.append(i.get())

                for i in range(118, 135, 2):
                    towrite.append(int((d[i] + d[i + 1])))

                towrite.append(int((ARMORS[armor.get()])[:2], 16))
                towrite.append(int((ARMORS[armor.get()])[2:], 16))
                towrite.append(int((d[140] + d[141])))
                towrite.append(int((SHIELDS[shield.get()])[:2], 16))
                towrite.append(int((SHIELDS[shield.get()])[2:], 16))

                shi = shield_skill.get()
                if shi == '':
                    shi = 255
                towrite.append(int(shi))

                f.seek(address)
                for item in towrite:
                    f.write(item.to_bytes(1, byteorder='big'))

        def build_window():
            # column 0, row 0
            lawfulgood_frame = Frame(charwin)
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

            write = Button(lawfulgood_frame, text="Write To File", command=write_to_file)
            write.grid(column=1, row=0)

            # column 0, row 1
            lawfulneutral_frame = Frame(charwin)
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
            lawfulevil_frame = LabelFrame(charwin, text='Equipment')
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
            neutralgood_frame = LabelFrame(charwin, text='Skills\n(blank = cannot learn)')
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
            chaoticgood_frame = LabelFrame(charwin, text='Spells and Spell Level')
            chaoticgood_frame.grid(column=0, row=3)
            for s in spells:
                x = spells.index(s)
                spell = Combobox(chaoticgood_frame, textvariable=s, values=list(SPELLS.keys()))
                spell.grid(column=0, row=x)
                spell.config(width=16)
                spell_level = Entry(chaoticgood_frame, textvariable=spell_levels[spells.index(s)])
                spell_level.grid(column=1, row=x)
                spell_level.config(width=4)

        # limits the same size
        def limit_name_size(*args):
            n = name.get()
            if len(n) > name_length:
                name.set(n[:name_length])

        # limits stats and level to appropriate numbers
        # higher numbers than limits causes the game to crash
        # or the numbers don't work right
        def limit_atts(*args):
            # int, wil, dex, str
            limit_30_stats = [atts[0], atts[1], atts[2], atts[4]]
            for i in limit_30_stats:
                val = i.get()
                if not val.isnumeric():
                    val = ''.join(filter(str.isnumeric, val))
                    i.set(val)
                elif val.isnumeric():
                    if int(val) > 30:
                        i.set(30)
                    else:
                        i.set(val)

            # end and level
            limit_40_stats = [atts[3], level]
            for i in limit_40_stats:
                val = i.get()
                if not val.isnumeric():
                    val = ''.join(filter(str.isnumeric, val))
                    i.set(val)
                elif val.isnumeric():
                    if int(val) > 40:
                        i.set(40)
                    else:
                        i.set(val)

            # stamina
            stamina = atts[5].get()
            if not stamina.isnumeric():
                stamina = ''.join(filter(str.isnumeric, stamina))
                atts[5].set(stamina)
            elif stamina.isnumeric():
                if int(stamina) > 120:
                    atts[5].set(120)
                else:
                    atts[5].set(stamina)

        def twofivefive(*args):
            for i in spell_levels:
                val = i.get()
                if not val.isnumeric():
                    val = ''.join(filter(str.isnumeric, val))
                    i.set(val)
                elif val.isnumeric():
                    if int(val) > 255:
                        i.set(255)
                    else:
                        i.set(val)

        # places a limit of 10 on appropriate skills
        def limit_10(i, *args):
            val = i.get()
            if not val.isnumeric():
                val = ''.join(filter(str.isnumeric, val))
                i.set(val)
            elif val.isnumeric():
                if int(val) > 10:
                    i.set(10)
                else:
                    i.set(val)

        # initial declaration of variables
        character = StringVar()
        character.trace('w', read_default_values)

        name = StringVar()
        name.trace('w', limit_name_size)
        aspect = IntVar()
        skills = []
        for _ in SKILLS:
            i = StringVar()
            i.trace('w', partial(limit_10, i))
            skills.append(i)
        shield_skill = StringVar()
        shield_skill.trace('w', partial(limit_10, shield_skill))
        atts = []
        for _ in ATTRIBUTES:
            i = StringVar()
            i.trace('w', limit_atts)
            atts.append(i)
        level = StringVar()
        level.trace('w', limit_atts)
        weapons = [StringVar(), StringVar(), StringVar()]
        spells = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]
        school = IntVar()
        spell_levels = []
        for i in range(5):
            i = StringVar()
            i.trace('w', twofivefive)
            spell_levels.append(i)
        armor = StringVar()
        shield = StringVar()

        character.set(characters[0])
        build_window()
