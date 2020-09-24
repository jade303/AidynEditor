from functools import partial

from lib.fuctions import int_cast, limit_127
from lib.item import Item
from lib.variables import inv_EQUIPMENT_STAT, inv_SKILL_ATTRIBUTE, inv_RESIST, inv_RESIST_AMOUNTS, \
    EQUIPMENT_STAT, SKILL_ATTRIBUTE, RESIST, RESIST_AMOUNTS


class ArmorShield(Item):
    def __init__(self, f, i, a, s, r, n, win_type):
        super().__init__(f, i, a, s, r, n)
        if win_type == 5:
            self.win.title("Armor Edit")
        elif win_type == 6:
            self.win.title("Shield Edit")

        stat_var = ['Defense', 'Protection', 'Dexterity', 'Stealth']
        for s in stat_var:
            self.stats[stat_var.index(s)].trace('w', partial(limit_127, self.stats[stat_var.index(s)]))
            self.stat_label[stat_var.index(s)]['text'] = s

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

            self.stats[0].set(int(d[0] + d[1], 16))
            self.stats[1].set(int(d[2] + d[3], 16))
            dx = int(d[4] + d[5], 16)
            if dx > 127:
                dx = dx - 256
            self.stats[2].set(dx)

            sneak = int(d[8] + d[9], 16)
            if sneak > 127:
                sneak = sneak - 256
            self.stats[3].set(sneak)
            self.value.set((int(d[12] + d[13], 16) * 256) + int(d[10] + d[11], 16))
            self.aspect.set(d[17])

            self.att.set(inv_EQUIPMENT_STAT[(d[18] + d[19]).upper()])
            at = int(d[20] + d[21], 16)
            if at > 127:
                at = at - 256
            self.att_amount.set(at)

            self.skill.set(inv_SKILL_ATTRIBUTE[(d[22] + d[23]).upper()])
            aa = int(d[24] + d[25], 16)
            if aa > 127:
                aa = aa - 256
            self.skill_amount.set(aa)

            self.spell.set(self.spell_dic[(d[26:30]).upper()])
            self.spell_level.set(int(d[30] + d[31], 16))

            self.magic.set(self.spell_dic[(d[34:38]).upper()])
            self.magic_level.set(int(d[38] + d[39], 16))
            self.resist.set(inv_RESIST[(d[40] + d[41]).upper()])
            self.resist_amount.set(inv_RESIST_AMOUNTS[(d[42] + d[43]).upper()])

    def write(self):
        with open(self.filename, 'rb+') as f:
            address = self.address_list[self.item_list.index(self.default_item_menu.get())]

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

            dx = int(self.stats[2].get())
            if dx < 0:
                dx = dx + 256

            sneak = int(self.stats[3].get())
            if sneak < 0:
                sneak = sneak + 256

            st = int(self.att_amount.get())
            if st < 0:
                st = st + 256

            sk = int(self.skill_amount.get())
            if sk < 0:
                sk = sk + 256

            towrite = [
                self.stats[0].get(),
                self.stats[1].get(),
                dx,
                (d[6] + d[7]),
                sneak,
                v1, v2,
                (d[14] + d[15]),
                self.aspect.get(),
                EQUIPMENT_STAT[self.att.get()],
                st,
                SKILL_ATTRIBUTE[self.skill.get()],
                sk,
                self.inv_spell_dic[self.spell.get()][:2],
                self.inv_spell_dic[self.spell.get()][2:],
                self.spell_level.get(),
                (d[32] + d[33]),
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
