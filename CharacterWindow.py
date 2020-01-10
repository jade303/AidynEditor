from tkinter import *
# from tkinter import filedialog
from variables import WEAPONS, inv_WEAPONS, ARMORS, inv_ARMORS, SHIELDS, inv_SHIELDS
from variables import SPELLS, inv_SPELLS, ATTRIBUTES, SKILLS


class CharacterEdit:
    def __init__(self, filename, characters, character_addresses, name_length):
        charwin = Toplevel()
        charwin.title("Character Edit")
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
                cd = character_data.hex()

                # set aspect default
                aspect.set(cd[1])

                # set skill defaults
                for s in skills:
                    sa = skills.index(s) * 2
                    sn = int(cd[sa + 6] + cd[sa + 7], 16)
                    if sn == 255:
                        sn = ''
                    s.set(sn)

                shi = int(cd[146] + cd[147], 16)
                if shi == 255:
                    shi = ''
                shield_skill.set(shi)

                # set attribute defaults
                for a in atts:
                    aa = atts.index(a) * 2
                    an = int(cd[aa + 52] + cd[aa + 53], 16)
                    if an == 255:
                        an = ''
                    a.set(an)

                # set level default
                level.set(int(cd[66] + cd[67], 16))

                # set equipment defaults
                for w in weapons:
                    x = (weapons.index(w) * 4) + 70
                    y = x + 4
                    w.set(inv_WEAPONS[cd[x:y].upper()])
                armor.set(inv_ARMORS[cd[136:140].upper()])
                shield.set(inv_SHIELDS[cd[142:146].upper()])

                # set school
                school.set(cd[107])

                # 5 initial spells
                for s in spells:
                    x = (spells.index(s) * 4) + 86
                    y = x + 4
                    s.set(inv_SPELLS[cd[x:y].upper()])

                # spell levels
                for s in spell_levels:
                    x = (spell_levels.index(s) * 2) + 108
                    s.set(int(cd[x] + cd[x + 1], 16))

        def write_to_file():
            with open(filename, 'rb+') as f:
                address = (character_addresses[characters.index(character.get())])

                # write new name to file
                new_name = name.get()
                if len(new_name) > name_length:
                    new_name = bytes(new_name[:name_length], 'utf-8')
                if len(new_name) < name_length:
                    new_name = bytearray(new_name, 'utf-8')
                    while len(new_name) < name_length:
                        new_name.append(0x00)
                f.seek(address - 44)
                f.write(new_name.encode('utf-8'))

                f.seek(address)
                character_data = f.read(74)
                cd = character_data.hex()
                towrite = [aspect.get(), int((cd[3] + cd[4]).encode('utf-8'), 16),
                           int((cd[5] + cd[6]).encode('utf-8'), 16)]
                for i in skills:
                    j = i.get()
                    if j == '':
                        j = 255
                    towrite.append(int(j))

                for i in atts:
                    j = i.get()
                    towrite.append(int(j))

                towrite.append(int((cd[64] + cd[65]).encode('utf-8'), 16))
                towrite.append(level.get())
                towrite.append(int((cd[68] + cd[69]).encode('utf-8'), 16))

                for i in weapons:
                    towrite.append(int((WEAPONS[i.get()])[:2], 16))
                    towrite.append(int((WEAPONS[i.get()])[2:], 16))

                towrite.append(int((cd[82] + cd[83]).encode('utf-8'), 16))
                towrite.append(int((cd[84] + cd[85]).encode('utf-8'), 16))

                for i in spells:
                    towrite.append(int((SPELLS[i.get()])[:2], 16))
                    towrite.append(int((SPELLS[i.get()])[2:], 16))

                towrite.append(school.get())

                for i in spell_levels:
                    towrite.append(i.get())

                for i in range(118, 135, 2):
                    towrite.append(int((cd[i] + cd[i+1]).encode('utf-8'), 16))

                towrite.append(int((ARMORS[armor.get()])[:2], 16))
                towrite.append(int((ARMORS[armor.get()])[2:], 16))
                towrite.append(int((cd[140] + cd[141]).encode('utf-8'), 16))
                towrite.append(int((SHIELDS[shield.get()])[:2], 16))
                towrite.append(int((SHIELDS[shield.get()])[2:], 16))

                shi = shield_skill.get()
                if shi == '':
                    shi = 255
                towrite.append(int(shi))

                f.seek(address)
                for item in towrite:
                    f.write(item.to_bytes(1, byteorder='big'))
            # messagebox.showinfo('Finished','Write Complete')

        def build_window():
            reg = charwin.register(input_val)
            # column 0, row 0
            lawfulgood_frame = Frame(charwin)
            lawfulgood_frame.grid(column=0, row=0)
            new_name_frame = LabelFrame(lawfulgood_frame, text="New Name")
            new_name_frame.grid(column=0, row=1)
            new_name_frame.config(width=18)

            default_name_menu = OptionMenu(lawfulgood_frame, character, *characters)
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
            level_entry.configure(validate='key', vcmd=(reg, "%P"))
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
                att_num.configure(validate='key', vcmd=(reg, "%P"))
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
                weapon_menu = OptionMenu(weapon_frame, w, *WEAPONS)
                weapon_menu.grid()
                weapon_menu.config(width=16)
            armor_menu = OptionMenu(armor_frame, armor, *ARMORS)
            armor_menu.grid(column=1)
            armor_menu.config(width=16)
            shield_menu = OptionMenu(shield_frame, shield, *SHIELDS)
            shield_menu.grid()
            shield_menu.config(width=16)

            # column 1, row all
            neutralgood_frame = LabelFrame(charwin, text='Skills')
            neutralgood_frame.grid(column=1, row=0, rowspan=23)

            for skill in SKILLS:
                x = SKILLS.index(skill)
                skill_label = Label(neutralgood_frame, text=skill, anchor='e', width=9)
                skill_label.grid(column=0, row=x)
                skill_num = Entry(neutralgood_frame, textvariable=skills[x], width=4)
                skill_num.configure(validate='key', vcmd=(reg, "%P"))
                skill_num.grid(column=1, row=x)
            shield_label = Label(neutralgood_frame, text='Shield', anchor='e', width=9)
            shield_label.grid(column=0, row=23)
            shield_num = Entry(neutralgood_frame, textvariable=shield_skill, width=4)
            shield_num.configure(validate='key', vcmd=(reg, "%P"))
            shield_num.grid(column=1, row=23)

            # column 0, row 4, column 2, row all
            chaoticgood_frame = LabelFrame(charwin, text='Spells and Spell Level')
            chaoticgood_frame.grid(column=0, row=3)
            for s in spells:
                x = spells.index(s)
                spell = OptionMenu(chaoticgood_frame, s, *SPELLS)
                spell.grid(column=0, row=x)
                spell.config(width=16)
                spell_level = Entry(chaoticgood_frame, textvariable=spell_levels[spells.index(s)])
                spell_level.configure(validate='key', vcmd=(reg, "%P"))
                spell_level.grid(column=1, row=x)
                spell_level.config(width=4)

        def input_val(inp):
            if inp.isnumeric() and int(inp) in range(1, 256):
                return True
            elif inp == "":
                return True
            else:
                return False

        def limit_name_size(*args):
            n = name.get()
            if len(n) > name_length:
                name.set(n[:name_length])

        # initial declaration of variables
        character = StringVar()
        character.trace('w', read_default_values)

        name = StringVar()
        name.trace('w', limit_name_size)
        aspect = IntVar()
        skills = []
        for _ in SKILLS:
            i = StringVar()
            skills.append(i)
        shield_skill = StringVar()
        atts = []
        for _ in ATTRIBUTES:
            i = IntVar()
            atts.append(i)
        level = IntVar()
        weapons = [StringVar(), StringVar(), StringVar()]
        spells = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]
        school = IntVar()
        spell_levels = [IntVar(), IntVar(), IntVar(), IntVar(), IntVar()]
        armor = StringVar()
        shield = StringVar()

        character.set(characters[0])
        build_window()
