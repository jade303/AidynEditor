from functools import partial
from tkinter import Toplevel, StringVar, IntVar, LabelFrame, Frame, Entry, Label, Button, Radiobutton
from tkinter.ttk import Combobox

from lib.limits import limit_name_size, limit_127, limit
from lib.list_functions import get_minor_dic, get_major_name_lists
from lib.variables import inv_EQUIPMENT_STAT, inv_SKILL_ATTRIBUTE, inv_RESIST, inv_RESIST_AMOUNTS, \
    EQUIPMENT_STAT, SKILL_ATTRIBUTE, RESIST, RESIST_AMOUNTS, SPELL_DIC


class ArmorShield:
    def __init__(self, filename, icon, addresses, title):
        win = Toplevel()
        win.resizable(False, False)
        if title == 5:
            win.title("Armor Edit")
        elif title == 6:
            win.title("Shield Edit")
        elif title == 7:
            win.title("Weapon Edit")
        win.iconbitmap(icon)
        filename = filename
        data_seek = 26
        data_read = 25
        name_length = 22

        self.item_list, self.item_addresses = get_major_name_lists(filename, addresses, name_length)
        self.default_item_menu = Combobox()

        spell_dic = get_minor_dic(filename, SPELL_DIC, 22)
        inv_spell_dic = {v: k for k, v in spell_dic.items()}

        def set_defaults(*args):
            with open(filename, 'rb') as f:
                address = self.item_addresses[self.default_item_menu.current()]
                f.seek(address)
                name.set(f.read(name_length).decode("utf-8"))

                f.seek(address + data_seek)
                d = f.read(data_read).hex()

                defense.set(int(d[0] + d[1], 16))
                protection.set(int(d[2] + d[3], 16))
                dx = int(d[4] + d[5], 16)
                if dx > 127:
                    dx = dx - 256
                dexterity.set(dx)

                sneak = int(d[8] + d[9], 16)
                if sneak > 127:
                    sneak = sneak - 256
                stealth.set(sneak)
                value.set((int(d[12] + d[13], 16) * 256) + int(d[10] + d[11], 16))

                aspect.set(d[17])
                stat.set(inv_EQUIPMENT_STAT[(d[18] + d[19]).upper()])
                st = int(d[20] + d[21], 16)
                if st > 127:
                    st = st - 256
                stat_amount.set(st)
                skill.set(inv_SKILL_ATTRIBUTE[(d[22] + d[23]).upper()])
                att_amount = int(d[24] + d[25], 16)
                if att_amount > 127:
                    att_amount = att_amount - 256
                skill_amount.set(att_amount)
                spell.set(spell_dic[(d[26:30]).upper()])
                spell_level.set(int(d[30] + d[31], 16))

                magic.set(spell_dic[(d[34:38]).upper()])
                magic_level.set(int(d[38] + d[39], 16))
                resist.set(inv_RESIST[(d[40] + d[41]).upper()])
                resist_amount.set(inv_RESIST_AMOUNTS[(d[42] + d[43]).upper()])

        def write():
            with open(filename, 'rb+') as f:
                address = self.item_addresses[self.item_list.index(self.default_item_menu.get())]

                new_name = bytearray(name.get(), 'utf-8')
                if len(new_name) < name_length:
                    while len(new_name) < name_length:
                        new_name.append(0x00)
                f.seek(address)
                f.write(new_name)

                f.seek(address + data_seek)
                d = f.read(data_read).hex()

                new_value = value.get()
                v2, v1 = divmod(int(new_value), 256)
                if v2 == 256:
                    v2 = 255
                    v1 = 255

                dx = int(dexterity.get())
                if dx < 0:
                    dx = dx + 256

                sneak = int(stealth.get())
                if sneak < 0:
                    sneak = sneak + 256

                st = int(stat_amount.get())
                if st < 0:
                    st = st + 256

                sk = int(skill_amount.get())
                if sk < 0:
                    sk = sk + 256

                towrite = [
                    int(defense.get()),
                    int(protection.get()),
                    int(dx),
                    int(d[6] + d[7], 16),
                    int(sneak),
                    int(v1), int(v2),
                    int(d[14] + d[15], 16),
                    aspect.get(),
                    int(EQUIPMENT_STAT[stat.get()], 16),
                    int(st),
                    int(SKILL_ATTRIBUTE[skill.get()], 16),
                    int(sk),
                    int((inv_spell_dic[spell.get()])[:2], 16),
                    int((inv_spell_dic[spell.get()])[2:], 16),
                    int(spell_level.get()),
                    int(d[32] + d[33], 16),
                    int((inv_spell_dic[magic.get()])[:2], 16),
                    int((inv_spell_dic[magic.get()])[2:], 16),
                    int(magic_level.get()),
                    int(RESIST[resist.get()], 16),
                    int(RESIST_AMOUNTS[resist_amount.get()], 16)
                ]

                f.seek(address + data_seek)
                for i in towrite:
                    f.write(i.to_bytes(1, byteorder='big'))

                reset_list()
                self.item.set(self.item_list[self.item_list.index(name.get().rstrip('\x00'))])
            set_defaults()

        def build():
            box = Frame(win)
            box.grid(column=0, row=0, pady=5, padx=5)
            self.default_item_menu = Combobox(box, textvariable=self.item, width=21,
                                              values=self.item_list,
                                              postcommand=reset_list, state='readonly')
            self.default_item_menu.grid(column=0, row=0)

            new_name_label = LabelFrame(box, text='New Name')
            new_name_label.grid(column=0, row=1)
            new_name_entry = Entry(new_name_label, textvariable=name, width=21)
            new_name_entry.grid()

            stat_frame = LabelFrame(box, text='Stats:')
            stat_frame.grid(column=0, row=2, rowspan=4)

            defense_label = Label(stat_frame, text='Defense:')
            defense_label.grid(column=0, row=0, sticky='e')
            defense_entry = Entry(stat_frame, textvariable=defense, width=4)
            defense_entry.grid(column=1, row=0, sticky='w')

            protection_label = Label(stat_frame, text='Protection:')
            protection_label.grid(column=0, row=1, sticky='e')
            protection_entry = Entry(stat_frame, textvariable=protection, width=4)
            protection_entry.grid(column=1, row=1, sticky='w')

            dexterity_label = Label(stat_frame, text='Dexterity:')
            dexterity_label.grid(column=0, row=2, sticky='e')
            dexterity_entry = Entry(stat_frame, textvariable=dexterity, width=4)
            dexterity_entry.grid(column=1, row=2, sticky='w')

            stealth_label = Label(stat_frame, text='Stealth:')
            stealth_label.grid(column=0, row=3, sticky='e')
            stealth_entry = Entry(stat_frame, textvariable=stealth, width=4)
            stealth_entry.grid(column=1, row=3, sticky='w')

            value_label = Label(stat_frame, text='Base Value:')
            value_label.grid(column=0, row=4, sticky='e')
            value_entry = Entry(stat_frame, textvariable=value, width=6)
            value_entry.grid(column=1, row=4, sticky='w')
            value_label2 = Label(stat_frame, text='Max base value: 65535', font=(None, 8))
            value_label2.grid(row=5, columnspan=2)

            save = Button(box, text='Save', command=write, width=8)
            save.grid(column=1, row=0)

            aspect_frame = LabelFrame(box, text='Aspect')
            aspect_frame.grid(column=1, row=1)
            none_radio = Radiobutton(aspect_frame, text='NONE', variable=aspect, value=0)
            none_radio.grid(column=0, row=0)
            solar_radio = Radiobutton(aspect_frame, text="Solar", variable=aspect, value=2)
            solar_radio.grid(column=1, row=0)
            lunar_radio = Radiobutton(aspect_frame, text='Lunar', variable=aspect, value=1)
            lunar_radio.grid(column=2, row=0)

            att_frame = LabelFrame(box, text='Attribute')
            att_frame.grid(column=1, row=2)
            att_menu = Combobox(att_frame, textvariable=stat, values=list(EQUIPMENT_STAT.keys()),
                                width=16, state='readonly')
            att_menu.grid(column=0, row=0)
            att_entry = Entry(att_frame, textvariable=stat_amount, width=4)
            att_entry.grid(column=1, row=0, sticky='e')

            ski_att_frame = LabelFrame(box, text='Skill/Attribute')
            ski_att_frame.grid(column=1, row=3)
            ski_att_menu = Combobox(ski_att_frame, textvariable=skill, values=list(SKILL_ATTRIBUTE.keys()),
                                    width=16, state='readonly')
            ski_att_menu.grid(column=0, row=0)
            ski_att_amo_entry = Entry(ski_att_frame, textvariable=skill_amount, width=4)
            ski_att_amo_entry.grid(column=1, row=0)

            spell_frame = LabelFrame(box, text='Spell')
            spell_frame.grid(column=1, row=4)
            spell_menu = Combobox(spell_frame, textvariable=spell, values=list(inv_spell_dic.keys()),
                                  width=16, state='readonly')
            spell_menu.grid(column=0, row=0)
            spell_entry = Entry(spell_frame, textvariable=spell_level, width=4)
            spell_entry.grid(column=1, row=0)

            magic_frame = LabelFrame(box, text='Magic')
            magic_frame.grid(column=1, row=5)
            magic_menu = Combobox(magic_frame, textvariable=magic, values=list(inv_spell_dic.keys()),
                                  width=16, state='readonly')
            magic_menu.grid(column=0, row=0)
            magic_entry = Entry(magic_frame, textvariable=magic_level, width=4)
            magic_entry.grid(column=1, row=0)

            resist_frame = LabelFrame(box, text='Resist')
            resist_frame.grid(column=1, row=6)
            resist_menu = Combobox(resist_frame, textvariable=resist, values=list(RESIST.keys()),
                                   width=16, state='readonly')
            resist_menu.grid(column=0, row=0)
            resist_amount_menu = Combobox(resist_frame, textvariable=resist_amount, width=5,
                                          values=list(RESIST_AMOUNTS.keys()), state='readonly')
            resist_amount_menu.grid(column=1, row=0)

        def reset_list():
            self.item_list[:] = []
            self.item_addresses[:] = []
            self.item_list, self.item_addresses = get_major_name_lists(filename, addresses, name_length)
            self.default_item_menu['values'] = self.item_list

        self.item = StringVar()
        self.item.trace('w', set_defaults)
        name = StringVar()
        name.trace('w', partial(limit_name_size, name, name_length))

        defense = StringVar()
        defense.trace('w', partial(limit_127, defense))
        protection = StringVar()
        protection.trace('w', partial(limit_127, protection))
        dexterity = StringVar()
        dexterity.trace('w', partial(limit_127, dexterity))
        stealth = StringVar()
        stealth.trace('w', partial(limit_127, stealth))
        value = StringVar()
        value.trace('w', partial(limit, value, 65535))
        aspect = IntVar()
        stat = StringVar()
        stat_amount = StringVar()
        stat_amount.trace('w', partial(limit_127, stat_amount))
        skill = StringVar()
        skill_amount = StringVar()
        skill_amount.trace('w', partial(limit_127, skill_amount))
        spell = StringVar()
        spell_level = StringVar()
        spell_level.trace('w', partial(limit, spell_level, 15))
        magic = StringVar()
        magic_level = StringVar()
        magic_level.trace('w', partial(limit, magic_level, 15))
        resist = StringVar()
        resist_amount = StringVar()

        build()
        self.item.set(self.item_list[0])
