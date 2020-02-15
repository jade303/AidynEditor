from functools import partial
from tkinter import Toplevel, Label, StringVar, LabelFrame, Entry, Frame, Button, Radiobutton
from tkinter.ttk import Combobox

from lib.limits import limit, limit_127, limit_name_size
from lib.variables import WAND_NAMES, SCROLL_NAMES, WAND_ADDRESSES, SCROLL_ADDRESSES, inv_SPELLS, inv_SKILL_ATTRIBUTE, \
    inv_RESIST, inv_RESIST_AMOUNTS, SPELLS, SKILL_ATTRIBUTE, RESIST, RESIST_AMOUNTS


class WandScrollEdit:
    def __init__(self, filename, icon_dir):
        win = Toplevel()
        win.resizable(False, False)
        win.title("Wand and Scroll Edit")
        win.iconbitmap(icon_dir)
        filename = filename
        data_seek = 24
        data_read = 20
        name_length = 18

        def wand_defaults(*args):
            with open(filename, 'rb') as f:
                address = WAND_ADDRESSES[WAND_NAMES.index(wand.get())]
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
                wa_spell.set(inv_SPELLS[(d[22:26]).upper()])
                wa_charges.set(int(d[26] + d[27], 16))
                wa_spell_level.set(int(d[28] + d[29], 16))
                wa_resist.set(inv_RESIST[(d[36] + d[37]).upper()])
                wa_resist_amount.set(inv_RESIST_AMOUNTS[(d[38] + d[39]).upper()])

        def scroll_defaults(*args):
            with open(filename, 'rb') as f:
                address = SCROLL_ADDRESSES[SCROLL_NAMES.index(scroll.get())]
                f.seek(address)
                sc_name.set(f.read(name_length).decode("utf-8"))

                f.seek(address + data_seek)
                d = f.read(data_read).hex()

                sc_value.set((int(d[10] + d[11], 16) * 256) + int(d[8] + d[9], 16))
                sc_spell.set(inv_SPELLS[(d[22:26]).upper()])
                sc_cast_level.set(int(d[28] + d[29], 16))

        def wand_write():
            with open(filename, 'rb+') as f:
                address = WAND_ADDRESSES[WAND_NAMES.index(wand.get())]

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
                    int(wa_damage.get()),
                    int(wa_protection.get()),
                    int(wa_str_req.get()),
                    int(wa_int_req.get()),
                    int(v1), int(v2),
                    int(wa_aspect.get()),
                    int(d[14] + d[15], 16),
                    int(d[16] + d[17], 16),
                    int(SKILL_ATTRIBUTE[wa_skill.get()], 16),
                    int(sk),
                    int((SPELLS[wa_spell.get()])[:2], 16),
                    int((SPELLS[wa_spell.get()])[2:], 16),
                    int(wa_charges.get()),
                    int(wa_spell_level.get()),
                    int(d[30] + d[31], 16),
                    int(d[32] + d[33], 16),
                    int(d[34] + d[35], 16),
                    int(RESIST[wa_resist.get()], 16),
                    int(RESIST_AMOUNTS[wa_resist_amount.get()], 16)
                ]

                f.seek(address + data_seek)
                for i in towrite:
                    f.write(i.to_bytes(1, byteorder='big'))

        def scroll_write():
            with open(filename, 'rb+') as f:
                address = SCROLL_ADDRESSES[SCROLL_NAMES.index(scroll.get())]

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
                    towrite.append(int(d[i] + d[i+1], 16))

                towrite.append(int(v1))
                towrite.append(int(v2))

                for i in range(12, 22, 2):
                    towrite.append(int(d[i] + d[i+1], 16))

                towrite.append(int((SPELLS[sc_spell.get()])[:2], 16))
                towrite.append(int((SPELLS[sc_spell.get()])[2:], 16))
                towrite.append(int(d[26] + d[27], 16))
                towrite.append(int(sc_cast_level.get()))

                for i in range(30, 40, 2):
                    towrite.append(int(d[i] + d[i + 1], 16))

                f.seek(address + data_seek)
                for i in towrite:
                    f.write(i.to_bytes(1, byteorder='big'))

        def build():
            sc_fr = LabelFrame(win, text='Scrolls:', bd=6)
            sc_fr.grid(column=0, row=0, sticky='n')

            sc_box = Combobox(sc_fr, textvariable=scroll, values=SCROLL_NAMES)
            sc_box.grid(column=0, row=0)
            sc_box.config(width=20)
            sc_new_name_label = LabelFrame(sc_fr, text='New Name')
            sc_new_name_label.grid(column=0, row=1)
            sc_new_name_entry = Entry(sc_new_name_label, textvariable=sc_name)
            sc_new_name_entry.grid(column=0, row=0)
            sc_new_name_entry.config(width=20)
            sc_spell_label = LabelFrame(sc_fr, text='Spell learned/cast')
            sc_spell_label.grid(column=0, row=2)
            sc_spell_menu = Combobox(sc_spell_label, textvariable=sc_spell, values=list(SPELLS.keys()))
            sc_spell_menu.grid(column=0, row=0)
            sc_spell_menu.config(width=20)
            sc_other_atts = Frame(sc_fr)
            sc_other_atts.grid(column=0, row=3)
            sc_spell_label = Label(sc_other_atts, text='Cast Level')
            sc_spell_label.grid(column=0, row=0, sticky='e')
            sc_spell_entry = Entry(sc_other_atts, textvariable=sc_cast_level)
            sc_spell_entry.grid(column=1, row=0, sticky='e')
            sc_spell_entry.config(width=4)
            sc_value_label = Label(sc_other_atts, text='Base Value')
            sc_value_label.grid(column=0, row=1, sticky='e')
            sc_value_entry = Entry(sc_other_atts, textvariable=sc_value)
            sc_value_entry.grid(column=1, row=1, sticky='e')
            sc_value_entry.config(width=6)
            sc_save = Button(sc_fr, text='Save Scroll Edits', command=scroll_write)
            sc_save.grid(column=0, row=4)

            wa_fr = LabelFrame(win, text='Wands', bd=6)
            wa_fr.grid(column=1, row=0)

            wa_box = Combobox(wa_fr, textvariable=wand, values=WAND_NAMES)
            wa_box.grid(column=0, row=0)
            wa_box.config(width=20)
            wa_new_name_label = LabelFrame(wa_fr, text='New Name')
            wa_new_name_label.grid(column=0, row=1)
            wa_new_name_entry = Entry(wa_new_name_label, textvariable=wa_name)
            wa_new_name_entry.grid(column=0, row=0)
            wa_new_name_entry.config(width=20)
            wa_spell_label = LabelFrame(wa_fr, text='Spell Cast')
            wa_spell_label.grid(column=0, row=2)
            wa_spell_menu = Combobox(wa_spell_label, textvariable=wa_spell, values=list(SPELLS.keys()))
            wa_spell_menu.grid(column=0, row=0)
            wa_spell_menu.config(width=20)

            wa_other_atts = Frame(wa_fr)
            wa_other_atts.grid(column=0, row=3)

            wa_level_label = Label(wa_other_atts, text='Spell Level')
            wa_level_label.grid(column=0, row=0, sticky='e')
            wa_level_entry = Entry(wa_other_atts, textvariable=wa_spell_level, width=4)
            wa_level_entry.grid(column=1, row=0, sticky='e')

            wa_charges_label = Label(wa_other_atts, text='Charges')
            wa_charges_label.grid(column=0, row=1, sticky='e')
            wa_charges_entry = Entry(wa_other_atts, textvariable=wa_charges, width=4)
            wa_charges_entry.grid(column=1, row=1, sticky='e')

            wa_damage_label = Label(wa_other_atts, text='Damage')
            wa_damage_label.grid(column=0, row=2, sticky='e')
            wa_damage_entry = Entry(wa_other_atts, textvariable=wa_damage, width=4)
            wa_damage_entry.grid(column=1, row=2, sticky='e')

            wa_protection_label = Label(wa_other_atts, text='Protection')
            wa_protection_label.grid(column=0, row=3, sticky='e')
            wa_protection_entry = Entry(wa_other_atts, textvariable=wa_protection, width=4)
            wa_protection_entry.grid(column=1, row=3, sticky='e')

            wa_str_label = Label(wa_other_atts, text='Str Req')
            wa_str_label.grid(column=0, row=4, sticky='e')
            wa_str_entry = Entry(wa_other_atts, textvariable=wa_str_req, width=4)
            wa_str_entry.grid(column=1, row=4, sticky='e')

            wa_int_label = Label(wa_other_atts, text='Int Req')
            wa_int_label.grid(column=0, row=5, sticky='e')
            wa_int_entry = Entry(wa_other_atts, textvariable=wa_int_req, width=4)
            wa_int_entry.grid(column=1, row=5, sticky='e')

            wa_value_label = Label(wa_other_atts, text='Base Value')
            wa_value_label.grid(column=0, row=6, sticky='e')
            wa_value_entry = Entry(wa_other_atts, textvariable=wa_value, width=6)
            wa_value_entry.grid(column=1, row=6, sticky='e')

            aspect_frame = LabelFrame(wa_fr, text='Aspect')
            aspect_frame.grid(column=0, row=4)
            none_radio = Radiobutton(aspect_frame, text='NONE', variable=wa_aspect, value=0)
            none_radio.grid(column=0, row=0)
            solar_radio = Radiobutton(aspect_frame, text="Solar", variable=wa_aspect, value=2)
            solar_radio.grid(column=1, row=0)
            lunar_radio = Radiobutton(aspect_frame, text='Lunar', variable=wa_aspect, value=1)
            lunar_radio.grid(column=2, row=0)

            wa_bottom = Frame(wa_fr)
            wa_bottom.grid(column=0, row=5)

            ski_att_frame = LabelFrame(wa_bottom, text='Skill/Attribute')
            ski_att_frame.grid(column=0, row=0)
            ski_att_menu = Combobox(ski_att_frame, textvariable=wa_skill, values=list(SKILL_ATTRIBUTE.keys()))
            ski_att_menu.grid(column=0, row=0)
            ski_att_menu.config(width=16)
            ski_att_amo_entry = Entry(ski_att_frame, textvariable=wa_skill_amount)
            ski_att_amo_entry.grid(column=1, row=0)
            ski_att_amo_entry.config(width=4)

            resist_frame = LabelFrame(wa_bottom, text='Resist')
            resist_frame.grid(column=0, row=1)
            resist_menu = Combobox(resist_frame, textvariable=wa_resist, values=list(RESIST.keys()))
            resist_menu.grid(column=0, row=0)
            resist_menu.config(width=16)
            resist_amount_menu = Combobox(resist_frame, textvariable=wa_resist_amount, values=list(RESIST_AMOUNTS.keys()))
            resist_amount_menu.grid(column=1, row=0)
            resist_amount_menu.config(width=5)

            wa_save = Button(wa_fr, text='Save Wand Edits', command=wand_write)
            wa_save.grid(column=0, row=6)

        wand = StringVar()
        wand.trace('w', wand_defaults)
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
        wa_spell_level.trace('w', partial(limit, wa_spell_level, 255))
        wa_resist = StringVar()
        wa_resist_amount = StringVar()

        scroll = StringVar()
        scroll.trace('w', scroll_defaults)
        sc_name = StringVar()
        sc_name.trace('w', partial(limit_name_size, sc_name, name_length))
        sc_value = StringVar()
        sc_value.trace('w', partial(limit, sc_value, 65535))
        sc_spell = StringVar()
        sc_cast_level = StringVar()
        sc_cast_level.trace('w', partial(limit, sc_cast_level, 15))

        wand.set(WAND_NAMES[0])
        scroll.set(SCROLL_NAMES[0])
        build()
