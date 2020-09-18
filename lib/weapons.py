from functools import partial
from tkinter import StringVar, LabelFrame
from tkinter.ttk import Combobox

from lib.fuctions import int_cast
from lib.item import Item
from lib.limits import limit
from lib.variables import inv_WEAPON_TYPE, inv_WEAPON_ANIMATIONS, inv_EQUIPMENT_STAT, \
    inv_SKILL_ATTRIBUTE, inv_RESIST, inv_RESIST_AMOUNTS, WEAPON_TYPE, WEAPON_ANIMATIONS, EQUIPMENT_STAT, \
    SKILL_ATTRIBUTE, RESIST, RESIST_AMOUNTS


class WeaponEdit(Item):
    def __init__(self, f, i, a, s, r, n):
        super().__init__(f, i, a, s, r, n)
        self.win.title('Weapon Edit')

        stat_var = ['Strength Required', 'Hit', 'Damage', 'Range']
        for s in stat_var:
            self.stats[stat_var.index(s)].trace('w', partial(limit, self.stats[stat_var.index(s)], 255))
            self.stat_label[stat_var.index(s)]['text'] = s

        self.damage_type = StringVar()
        self.weapon_type = StringVar()
        self.animation = StringVar()

        # run
        self.build()
        self.item.set(self.item_list[0])

    def set_defaults(self, *args):
        with open(self.filename, 'rb') as f:
            address = self.address_list[self.default_item_menu.current()]
            f.seek(address)
            self.name.set(f.read(self.name_length).decode("utf-8"))

            f.seek(address + self.data_seek)
            d = f.read(self.data_read).hex()

            self.weapon_type.set(inv_WEAPON_TYPE[d[1].upper()])
            self.stats[0].set(int(d[2] + d[3], 16))
            self.stats[1].set(int(d[4] + d[5], 16))
            self.stats[2].set(int(d[6] + d[7], 16))
            self.value.set((int(d[10] + d[11], 16) * 256) + int(d[8] + d[9], 16))
            self.stats[3].set(int(d[14] + d[15], 16))
            self.animation.set(inv_WEAPON_ANIMATIONS[d[16] + d[17].upper()])
            self.damage_type.set(inv_RESIST[(d[20] + d[21]).upper()])
            self.aspect.set(d[23])

            self.att.set(inv_EQUIPMENT_STAT[(d[24] + d[25]).upper()])
            at = int(d[26] + d[27], 16)
            if at > 127:
                at = at - 256
            self.att_amount.set(at)

            self.skill.set(inv_SKILL_ATTRIBUTE[(d[28] + d[29]).upper()])
            aa = int(d[30] + d[31], 16)
            if aa > 127:
                aa = aa - 256
            self.skill_amount.set(aa)

            self.spell.set(self.spell_dic[(d[32:36]).upper()])
            self.spell_level.set(int(d[36] + d[37], 16))

            self.magic.set(self.spell_dic[(d[40:44]).upper()])
            self.magic_level.set(int(d[44] + d[45], 16))

            self.resist.set(inv_RESIST[(d[46] + d[47]).upper()])
            self.resist_amount.set(inv_RESIST_AMOUNTS[(d[48] + d[49]).upper()])

    def write(self):
        with open(self.filename, 'rb+') as f:
            address = self.address_list[self.default_item_menu.current()]
            new_name = bytearray(self.name.get(), 'utf-8')
            if len(new_name) < self.name_length:
                while len(new_name) < self.name_length:
                    new_name.append(0x00)
            f.seek(address)
            f.write(new_name)

            f.seek(address + self.data_seek)
            d = f.read(self.data_read).hex()

            new_value = self.value.get()
            v2, v1 = divmod(int(new_value), 256)
            if v2 == 256:
                v2 = 255
                v1 = 255

            st = int(self.att_amount.get())
            if st < 0:
                st = st + 256

            sk = int(self.skill_amount.get())
            if sk < 0:
                sk = sk + 256

            towrite = [
                WEAPON_TYPE[self.weapon_type.get()],
                self.stats[0].get(),
                self.stats[1].get(),
                self.stats[2].get(),
                v1, v2,
                (d[12] + d[13]),
                self.stats[3].get(),
                WEAPON_ANIMATIONS[self.animation.get()],
                (d[18] + d[19]),
                RESIST[self.damage_type.get()],
                self.aspect.get(),
                EQUIPMENT_STAT[self.att.get()],
                st,
                SKILL_ATTRIBUTE[self.skill.get()],
                sk,
                self.inv_spell_dic[self.spell.get()][:2],
                self.inv_spell_dic[self.spell.get()][2:],
                self.spell_level.get(),
                (d[38] + d[39]),
                self.inv_spell_dic[self.magic.get()][:2],
                self.inv_spell_dic[self.magic.get()][2:],
                self.magic_level.get(),
                RESIST[self.resist.get()],
                RESIST_AMOUNTS[self.resist_amount.get()]
            ]

            f.seek(address + self.data_seek)
            for item in towrite:
                item = int_cast(item)
                f.write(item.to_bytes(1, byteorder='big'))

            self.reset_list()
            self.item.set(self.item_list[self.item_list.index(self.name.get().rstrip('\x00'))])
        self.set_defaults()

    def build(self):
        super().build()

        damage_type_frame = LabelFrame(self.box, text='Damage Type')
        damage_type_box = Combobox(damage_type_frame, textvariable=self.damage_type,
                                   values=list(RESIST.keys())[1:],
                                   width=14, state='readonly')

        weapon_type_frame = LabelFrame(self.box, text='Weapon Type')
        weapon_type_menu = Combobox(weapon_type_frame, width=14, textvariable=self.weapon_type,
                                    values=list(WEAPON_TYPE.keys()), state='readonly')

        animation_frame = LabelFrame(self.box, text='Animation')
        animation_menu = Combobox(animation_frame, textvariable=self.animation, width=14,
                                  values=list(WEAPON_ANIMATIONS.keys()), state='readonly')

        damage_type_frame.grid(column=0, row=6)
        damage_type_box.grid()

        weapon_type_frame.grid(column=0, row=7)
        weapon_type_menu.grid()

        animation_frame.grid(column=0, row=8)
        animation_menu.grid()
