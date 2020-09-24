from functools import partial
from tkinter import Toplevel, Label, StringVar, LabelFrame, Entry, Frame, Button, Radiobutton
from tkinter.ttk import Combobox

from lib.fuctions import get_minor_dic, get_major_name_lists, int_cast, limit_name_size, limit, limit_127
from lib.variables import WAND_ADDRESSES, SCROLL_ADDRESSES, inv_SKILL_ATTRIBUTE, \
    inv_RESIST, inv_RESIST_AMOUNTS, SKILL_ATTRIBUTE, RESIST, RESIST_AMOUNTS, SPELL_DIC


class WandScrollEdit:
    def __init__(self, filename, icon):
        win = Toplevel()
        win.resizable(False, False)
        win.title("Wand and Scroll Edit")
        win.iconbitmap(icon)
        filename = filename
        data_seek = 24
        data_read = 20
        name_length = 18

        self.scroll_list, self.scroll_addresses = get_major_name_lists(filename, SCROLL_ADDRESSES, name_length)
        self.wand_list, self.wand_addresses = get_major_name_lists(filename, WAND_ADDRESSES, name_length)
        self.sc_menu = Combobox()
        self.wa_menu = Combobox()

        spell_dic = get_minor_dic(filename, SPELL_DIC, 22)
        inv_spell_dic = {v: k for k, v in spell_dic.items()}

        def wand_defaults(*args):
            with open(filename, 'rb') as f:
                address = self.wand_addresses[self.wa_menu.current()]
                f.seek(address)
                wa_name.set(f.read(name_length).decode("utf-8"))

                f.seek(address + data_seek)
                d = f.read(data_read).hex()

                wa_damage.set(int(d[0] + d[1], 16))
                wa_protection.set(int(d[2] + d[3], 16))
                wa_str_req.set(int(d[4] + d[5], 16))
                wa_int_req.set(int(d[6] + d[7], 16))
                wa_value.set((int(d[10] + d[11], 16) * 256) + int(d[8] + d[9], 16))
                wa_aspect.set(d[13])
                wa_skill.set(inv_SKILL_ATTRIBUTE[(d[14] + d[15]).upper()])
                att_amount = int(d[16] + d[17], 16)
                if att_amount > 127:
                    att_amount = att_amount - 256
                wa_skill_amount.set(att_amount)
                wa_spell.set(spell_dic[(d[22:26]).upper()])
                wa_charges.set(int(d[26] + d[27], 16))
                wa_spell_level.set(int(d[28] + d[29], 16))
                wa_resist.set(inv_RESIST[(d[36] + d[37]).upper()])
                wa_resist_amount.set(inv_RESIST_AMOUNTS[(d[38] + d[39]).upper()])

        def scroll_defaults(*args):
            with open(filename, 'rb') as f:
                address = self.scroll_addresses[self.sc_menu.current()]
                f.seek(address)
                sc_name.set(f.read(name_length).decode("utf-8"))

                f.seek(address + data_seek)
                d = f.read(data_read).hex()

                sc_value.set((int(d[10] + d[11], 16) * 256) + int(d[8] + d[9], 16))
                sc_spell.set(spell_dic[(d[22:26]).upper()])
                sc_cast_level.set(int(d[28] + d[29], 16))

        def wand_write():
            with open(filename, 'rb+') as f:
                address = self.wand_addresses[self.wa_menu.current()]

                new_name = bytearray(wa_name.get(), 'utf-8')
                if len(new_name) < name_length:
                    while len(new_name) < name_length:
                        new_name.append(0x00)
                f.seek(address)
                f.write(new_name)

                f.seek(address + data_seek)
                d = f.read(data_read).hex()

                new_value = wa_value.get()
                v2, v1 = divmod(int(new_value), 256)
                if v2 == 256:
                    v2 = 255
                    v1 = 255

                sk = int(wa_skill_amount.get())
                if sk < 0:
                    sk = sk + 256

                towrite = [
                    wa_damage.get(),
                    wa_protection.get(),
                    wa_str_req.get(),
                    wa_int_req.get(),
                    v1, v2,
                    wa_aspect.get(),
                    SKILL_ATTRIBUTE[wa_skill.get()],
                    sk,
                    (d[18] + d[19]),
                    (d[20] + d[21]),
                    inv_spell_dic[wa_spell.get()][:2],
                    inv_spell_dic[wa_spell.get()][2:],
                    wa_charges.get(),
                    wa_spell_level.get(),
                    (d[30] + d[31]),
                    (d[32] + d[33]),
                    (d[34] + d[35]),
                    RESIST[wa_resist.get()],
                    RESIST_AMOUNTS[wa_resist_amount.get()]
                ]

                f.seek(address + data_seek)
                for item in towrite:
                    item = int_cast(item)
                    f.write(item.to_bytes(1, byteorder='big'))

                wand_reset_list()
                self.wand.set(self.wand_list[self.wand_list.index(wa_name.get().rstrip('\x00'))])
            wand_defaults()

        def scroll_write():
            with open(filename, 'rb+') as f:
                address = self.scroll_addresses[self.sc_menu.current()]

                new_name = bytearray(sc_name.get(), 'utf-8')
                if len(new_name) < name_length:
                    while len(new_name) < name_length:
                        new_name.append(0x00)
                f.seek(address)
                f.write(new_name)

                f.seek(address + data_seek)
                d = f.read(data_read).hex()

                new_value = sc_value.get()
                v2, v1 = divmod(int(new_value), 256)
                if v2 == 256:
                    v2 = 255
                    v1 = 255

                towrite = []

                for i in range(0, 8, 2):
                    towrite.append(d[i] + d[i + 1])

                towrite.append(v1)
                towrite.append(v2)

                for i in range(12, 22, 2):
                    towrite.append(d[i] + d[i + 1])

                towrite.append(inv_spell_dic[sc_spell.get()][:2])
                towrite.append(inv_spell_dic[sc_spell.get()][2:])
                towrite.append(d[26] + d[27])
                towrite.append(sc_cast_level.get())

                for i in range(30, 40, 2):
                    towrite.append(d[i] + d[i + 1])

                f.seek(address + data_seek)
                for item in towrite:
                    item = int_cast(item)
                    f.write(item.to_bytes(1, byteorder='big'))

                scroll_reset_list()
                self.scroll.set(self.scroll_list[self.scroll_list.index(sc_name.get().rstrip('\x00'))])
            scroll_defaults()

        def build():
            box = Frame(win)
            box.grid(padx=5, pady=5)

            sc_box = LabelFrame(box, text='Scrolls:', bd=6)
            sc_box.grid(column=0, row=0, sticky='n')

            self.sc_menu = Combobox(sc_box, textvariable=self.scroll, width=20,
                                    values=self.scroll_list,
                                    postcommand=scroll_reset_list, state='readonly')
            self.sc_menu.grid(column=0, row=0, columnspan=2)
            sc_new_name_label = LabelFrame(sc_box, text='New Name')
            sc_new_name_label.grid(column=0, row=1, columnspan=2)
            sc_new_name_entry = Entry(sc_new_name_label, textvariable=sc_name, width=20)
            sc_new_name_entry.grid(column=0, row=0)
            sc_spell_label = LabelFrame(sc_box, text='Spell learned/cast')
            sc_spell_label.grid(column=0, row=2, columnspan=2)
            sc_spell_menu = Combobox(sc_spell_label, textvariable=sc_spell, width=20,
                                     values=list(inv_spell_dic.keys()), state='readonly')
            sc_spell_menu.grid(column=0, row=0)

            sc_spell_label = Label(sc_box, text='Cast Level')
            sc_spell_label.grid(column=0, row=3, sticky='e')
            sc_spell_entry = Entry(sc_box, textvariable=sc_cast_level, width=4)
            sc_spell_entry.grid(column=1, row=3, sticky='w')
            sc_value_label = Label(sc_box, text='Base Value')
            sc_value_label.grid(column=0, row=4, sticky='e')
            sc_value_entry = Entry(sc_box, textvariable=sc_value, width=6)
            sc_value_entry.grid(column=1, row=4, sticky='w')
            sc_save = Button(sc_box, text='Save Scroll Edits', command=scroll_write)
            sc_save.grid(column=0, row=5, columnspan=2)

            wa_box = LabelFrame(box, text='Wands', bd=6)
            wa_box.grid(column=1, row=0)

            self.wa_menu = Combobox(wa_box, textvariable=self.wand, width=20,
                                    values=self.wand_list,
                                    postcommand=wand_reset_list)
            self.wa_menu.grid(column=0, row=0, columnspan=2)
            wa_new_name_label = LabelFrame(wa_box, text='New Name')
            wa_new_name_label.grid(column=0, row=1, columnspan=2)
            wa_new_name_entry = Entry(wa_new_name_label, textvariable=wa_name, width=20)
            wa_new_name_entry.grid(column=0, row=0)
            wa_spell_label = LabelFrame(wa_box, text='Spell Cast')
            wa_spell_label.grid(column=0, row=2, columnspan=2)
            wa_spell_menu = Combobox(wa_spell_label, textvariable=wa_spell, width=20,
                                     values=list(inv_spell_dic.keys()), state='readonly')
            wa_spell_menu.grid(column=0, row=0)

            wa_level_label = Label(wa_box, text='Spell Level')
            wa_level_label.grid(column=0, row=3, sticky='e')
            wa_level_entry = Entry(wa_box, textvariable=wa_spell_level, width=4)
            wa_level_entry.grid(column=1, row=3, sticky='w')

            wa_charges_label = Label(wa_box, text='Charges')
            wa_charges_label.grid(column=0, row=4, sticky='e')
            wa_charges_entry = Entry(wa_box, textvariable=wa_charges, width=4)
            wa_charges_entry.grid(column=1, row=4, sticky='w')

            wa_damage_label = Label(wa_box, text='Damage')
            wa_damage_label.grid(column=0, row=5, sticky='e')
            wa_damage_entry = Entry(wa_box, textvariable=wa_damage, width=4)
            wa_damage_entry.grid(column=1, row=5, sticky='w')

            wa_protection_label = Label(wa_box, text='Protection')
            wa_protection_label.grid(column=0, row=6, sticky='e')
            wa_protection_entry = Entry(wa_box, textvariable=wa_protection, width=4)
            wa_protection_entry.grid(column=1, row=6, sticky='w')

            wa_str_label = Label(wa_box, text='Str Req')
            wa_str_label.grid(column=0, row=7, sticky='e')
            wa_str_entry = Entry(wa_box, textvariable=wa_str_req, width=4)
            wa_str_entry.grid(column=1, row=7, sticky='w')

            wa_int_label = Label(wa_box, text='Int Req')
            wa_int_label.grid(column=0, row=8, sticky='e')
            wa_int_entry = Entry(wa_box, textvariable=wa_int_req, width=4)
            wa_int_entry.grid(column=1, row=8, sticky='w')

            wa_value_label = Label(wa_box, text='Base Value')
            wa_value_label.grid(column=0, row=9, sticky='e')
            wa_value_entry = Entry(wa_box, textvariable=wa_value, width=6)
            wa_value_entry.grid(column=1, row=9, sticky='w')

            aspect_frame = LabelFrame(wa_box, text='Aspect')
            aspect_frame.grid(column=0, row=10, columnspan=2)
            none_radio = Radiobutton(aspect_frame, text='NONE', variable=wa_aspect, value=0)
            none_radio.grid(column=0, row=0)
            solar_radio = Radiobutton(aspect_frame, text="Solar", variable=wa_aspect, value=2)
            solar_radio.grid(column=1, row=0)
            lunar_radio = Radiobutton(aspect_frame, text='Lunar', variable=wa_aspect, value=1)
            lunar_radio.grid(column=2, row=0)

            ski_att_frame = LabelFrame(wa_box, text='Skill/Attribute')
            ski_att_frame.grid(column=0, row=11, columnspan=2)
            ski_att_menu = Combobox(ski_att_frame, textvariable=wa_skill, width=16,
                                    values=list(SKILL_ATTRIBUTE.keys()), state='readonly')
            ski_att_menu.grid(column=0, row=0)
            ski_att_amo_entry = Entry(ski_att_frame, textvariable=wa_skill_amount, width=4)
            ski_att_amo_entry.grid(column=1, row=0)

            resist_frame = LabelFrame(wa_box, text='Resist')
            resist_frame.grid(column=0, row=12, columnspan=2)
            resist_menu = Combobox(resist_frame, textvariable=wa_resist, width=16,
                                   values=list(RESIST.keys()), state='readonly')
            resist_menu.grid(column=0, row=0)
            resist_amount_menu = Combobox(resist_frame, textvariable=wa_resist_amount, width=5,
                                          values=list(RESIST_AMOUNTS.keys()), state='readonly')
            resist_amount_menu.grid(column=1, row=0)

            wa_save = Button(wa_box, text='Save Wand Edits', command=wand_write)
            wa_save.grid(column=0, row=13, columnspan=2)

        def scroll_reset_list():
            self.scroll_list[:] = []
            self.scroll_addresses[:] = []
            self.scroll_list, self.scroll_addresses = get_major_name_lists(filename, SCROLL_ADDRESSES, name_length)
            self.sc_menu['values'] = self.scroll_list

        def wand_reset_list():
            self.wand_list[:] = []
            self.wand_addresses[:] = []
            self.wand_list, self.wand_addresses = get_major_name_lists(filename, WAND_ADDRESSES, name_length)
            self.wa_menu['values'] = self.wand_list

        self.wand = StringVar()
        self.wand.trace('w', wand_defaults)
        wa_name = StringVar()
        wa_name.trace('w', partial(limit_name_size, wa_name, name_length))
        wa_damage = StringVar()
        wa_damage.trace('w', partial(limit, wa_damage, 255))
        wa_protection = StringVar()
        wa_protection.trace('w', partial(limit, wa_protection, 255))
        wa_str_req = StringVar()
        wa_str_req.trace('w', partial(limit, wa_str_req, 30))
        wa_int_req = StringVar()
        wa_int_req.trace('w', partial(limit, wa_str_req, 30))
        wa_value = StringVar()
        wa_value.trace('w', partial(limit, wa_value, 65535))
        wa_aspect = StringVar()
        wa_skill = StringVar()
        wa_skill_amount = StringVar()
        wa_skill_amount.trace('w', partial(limit_127, wa_skill_amount))
        wa_spell = StringVar()
        wa_charges = StringVar()
        wa_charges.trace('w', partial(limit, wa_charges, 255))
        wa_spell_level = StringVar()
        wa_spell_level.trace('w', partial(limit, wa_spell_level, 15))
        wa_resist = StringVar()
        wa_resist_amount = StringVar()

        self.scroll = StringVar()
        self.scroll.trace('w', scroll_defaults)
        sc_name = StringVar()
        sc_name.trace('w', partial(limit_name_size, sc_name, name_length))
        sc_value = StringVar()
        sc_value.trace('w', partial(limit, sc_value, 65535))
        sc_spell = StringVar()
        sc_cast_level = StringVar()
        sc_cast_level.trace('w', partial(limit, sc_cast_level, 15))

        build()
        self.wand.set(self.wand_list[0])
        self.scroll.set(self.scroll_list[0])
