from functools import partial
from tkinter import Toplevel, Frame, LabelFrame, Entry, Label, Button, Radiobutton, StringVar, IntVar
from tkinter.ttk import Combobox

from lib.limits import limit_name_size, limit, limit_127
from lib.list_functions import get_minor_dic, get_major_name_lists
from lib.variables import inv_WEAPON_TYPE, inv_WEAPON_ANIMATIONS, inv_EQUIPMENT_STAT, \
    inv_SKILL_ATTRIBUTE, inv_RESIST, inv_RESIST_AMOUNTS, WEAPON_TYPE, WEAPON_ANIMATIONS, EQUIPMENT_STAT, \
    SKILL_ATTRIBUTE, RESIST, RESIST_AMOUNTS, SPELL_DIC


class WeaponEdit:
    def __init__(self, filename, icon, addresses):
        win = Toplevel()
        win.resizable(False, False)
        win.title('Weapon Edit')
        win.iconbitmap(icon)
        filename = filename
        data_seek = 23
        data_read = 25
        name_length = 21

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

                weapon_type.set(inv_WEAPON_TYPE[d[1].upper()])
                str_req.set(int(d[2] + d[3], 16))
                hit.set(int(d[4] + d[5], 16))
                damage.set(int(d[6] + d[7], 16))
                value.set((int(d[10] + d[11], 16) * 256) + int(d[8] + d[9], 16))
                weapon_range.set(int(d[14] + d[15], 16))
                animation.set(inv_WEAPON_ANIMATIONS[d[16] + d[17].upper()])
                damage_type.set(inv_RESIST[(d[20] + d[21]).upper()])
                aspect.set(d[23])

                stat.set(inv_EQUIPMENT_STAT[(d[24] + d[25]).upper()])
                st = int(d[26] + d[27], 16)
                if st > 127:
                    st = st - 256
                stat_amount.set(st)

                skill.set(inv_SKILL_ATTRIBUTE[(d[28] + d[29]).upper()])
                att_amount = int(d[30] + d[31], 16)
                if att_amount > 127:
                    att_amount = att_amount - 256
                skill_amount.set(att_amount)

                spell.set(spell_dic[(d[32:36]).upper()])
                spell_level.set(int(d[36] + d[37], 16))

                magic.set(spell_dic[(d[40:44]).upper()])
                magic_level.set(int(d[44] + d[45], 16))

                resist.set(inv_RESIST[(d[46] + d[47]).upper()])
                resist_amount.set(inv_RESIST_AMOUNTS[(d[48] + d[49]).upper()])

        def write():
            with open(filename, 'rb+') as f:
                address = self.item_addresses[self.default_item_menu.current()]
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

                st = int(stat_amount.get())
                if st < 0:
                    st = st + 256

                sk = int(skill_amount.get())
                if sk < 0:
                    sk = sk + 256

                towrite = [
                    int(WEAPON_TYPE[weapon_type.get()], 16),
                    int(str_req.get()),
                    int(hit.get()),
                    int(damage.get()),
                    int(v1), int(v2),
                    int(d[12] + d[13], 16),
                    int(weapon_range.get()),
                    int(WEAPON_ANIMATIONS[animation.get()], 16),
                    int(d[18] + d[19], 16),
                    int(RESIST[damage_type.get()], 16),
                    aspect.get(),
                    int(EQUIPMENT_STAT[stat.get()], 16),
                    int(st),
                    int(SKILL_ATTRIBUTE[skill.get()], 16),
                    int(sk),
                    int((inv_spell_dic[spell.get()])[:2], 16),
                    int((inv_spell_dic[spell.get()])[2:], 16),
                    int(spell_level.get()),
                    int(d[38] + d[39], 16),
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

            weapon_type_frame = LabelFrame(box, text='Weapon Type')
            weapon_type_frame.grid(column=0, row=2)
            weapon_type_menu = Combobox(weapon_type_frame, width=9, textvariable=weapon_type,
                                        values=list(WEAPON_TYPE.keys()), state='readonly')
            weapon_type_menu.grid()

            animation_frame = LabelFrame(box, text='Animation')
            animation_frame.grid(column=0, row=3)
            animation_menu = Combobox(animation_frame, textvariable=animation, width=12,
                                      values=list(WEAPON_ANIMATIONS.keys()), state='readonly')
            animation_menu.grid(column=0, row=0)

            stat_frame = LabelFrame(box, text='Stats:')
            stat_frame.grid(column=0, row=4, rowspan=4)

            strength_label = Label(stat_frame, text='Str Required:')
            strength_label.grid(column=0, row=0, sticky='e')
            strength_entry = Entry(stat_frame, textvariable=str_req, width=4)
            strength_entry.grid(column=1, row=0, stick='w')

            hit_label = Label(stat_frame, text='Hit:')
            hit_label.grid(column=0, row=1, sticky='e')
            hit_entry = Entry(stat_frame, textvariable=hit, width=4)
            hit_entry.grid(column=1, row=1, sticky='w')

            damage_label = Label(stat_frame, text='Damage:')
            damage_label.grid(column=0, row=2, sticky='e')
            damage_entry = Entry(stat_frame, textvariable=damage, width=4)
            damage_entry.grid(column=1, row=2, sticky='w')

            range_label = Label(stat_frame, text='Range:')
            range_label.grid(column=0, row=3, sticky='e')
            range_entry = Entry(stat_frame, textvariable=weapon_range, width=4)
            range_entry.grid(column=1, row=3, sticky='w')

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

            damage_type_frame = LabelFrame(box, text='Damage Type')
            damage_type_frame.grid(column=1, row=2)
            damage_type_box = Combobox(damage_type_frame, textvariable=damage_type, values=list(RESIST.keys())[1:],
                                       width=16, state='readonly')
            damage_type_box.grid()

            att_frame = LabelFrame(box, text='Attribute')
            att_frame.grid(column=1, row=3)
            att_menu = Combobox(att_frame, textvariable=stat, values=list(EQUIPMENT_STAT.keys()),
                                width=16, state='readonly')
            att_menu.grid(column=0, row=0)
            att_entry = Entry(att_frame, textvariable=stat_amount, width=4)
            att_entry.grid(column=1, row=0, sticky='e')

            ski_att_frame = LabelFrame(box, text='Skill/Attribute')
            ski_att_frame.grid(column=1, row=4)
            ski_att_menu = Combobox(ski_att_frame, textvariable=skill, width=16,
                                    values=list(SKILL_ATTRIBUTE.keys()), state='readonly')
            ski_att_menu.grid(column=0, row=0)
            ski_att_amo_entry = Entry(ski_att_frame, textvariable=skill_amount, width=4)
            ski_att_amo_entry.grid(column=1, row=0)

            spell_frame = LabelFrame(box, text='Spell')
            spell_frame.grid(column=1, row=5)
            spell_menu = Combobox(spell_frame, textvariable=spell, values=list(inv_spell_dic.keys()),
                                  width=16, state='readonly')
            spell_menu.grid(column=0, row=0)
            spell_entry = Entry(spell_frame, textvariable=spell_level, width=4)
            spell_entry.grid(column=1, row=0)

            magic_frame = LabelFrame(box, text='Magic')
            magic_frame.grid(column=1, row=6)
            magic_menu = Combobox(magic_frame, textvariable=magic, values=list(inv_spell_dic.keys()),
                                  width=16, state='readonly')
            magic_menu.grid(column=0, row=0)
            magic_entry = Entry(magic_frame, textvariable=magic_level, width=4)
            magic_entry.grid(column=1, row=0)

            resist_frame = LabelFrame(box, text='Resist')
            resist_frame.grid(column=1, row=7)
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

        str_req = StringVar()
        str_req.trace('w', partial(limit, str_req, 30))
        hit = StringVar()
        hit.trace('w', partial(limit, hit, 255))
        damage = StringVar()
        damage.trace('w', partial(limit, damage, 255))
        weapon_range = StringVar()
        weapon_range.trace('w', partial(limit, weapon_range, 255))
        weapon_type = StringVar()
        value = StringVar()
        value.trace('w', partial(limit, value, 65535))
        animation = StringVar()
        damage_type = StringVar()
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
