from functools import partial

from lib.fuctions import int_cast, limit_127
from views.item import Item
from lib.variables import inv_EQUIPMENT_STAT, inv_SKILL_ATTRIBUTE, \
    inv_RESIST, inv_RESIST_AMOUNTS, EQUIPMENT_STAT, SKILL_ATTRIBUTE, RESIST, RESIST_AMOUNTS


class AccessoryEdit(Item):
    def __init__(self, f, i, a, s, r, n):
        super().__init__(f, i, a, s, r, n)
        self.win.title("Accessory Edit")

        stat_var = ['Damage', 'Protection', 'Strength Required', 'Intelligence Required']
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
            self.stats[2].set(int(d[4] + d[5], 16))
            self.stats[3].set(int(d[6] + d[7], 16))
            self.value.set((int(d[10] + d[11], 16) * 256) + int(d[8] + d[9], 16))
            self.aspect.set(d[13])
            self.att.set(inv_EQUIPMENT_STAT[(d[14] + d[15]).upper()])
            at = int(d[16] + d[17], 16)
            if at > 127:
                at = at - 256
            self.att_amount.set(at)

            self.skill.set(inv_SKILL_ATTRIBUTE[(d[18] + d[19]).upper()])
            aa = int(d[20] + d[21], 16)
            if aa > 127:
                aa = aa - 256
            self.skill_amount.set(aa)

            self.spell.set(self.spell_dic[(d[22:26]).upper()])
            self.spell_level.set(int(d[26] + d[27], 16))

            self.magic.set(self.spell_dic[(d[30:34]).upper()])
            self.magic_level.set(int(d[34] + d[35], 16))
            self.resist.set(inv_RESIST[(d[36] + d[37]).upper()])
            self.resist_amount.set(inv_RESIST_AMOUNTS[(d[38] + d[39]).upper()])

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
            if new_value == '':
                new_value = '0'
            v2, v1 = divmod(int(new_value), 256)
            if v2 == 256:
                v2 = 255
                v1 = 255

            st = int(self.att_amount.get())
            if st == '':
                st = 00
            if st < 0:
                st = st + 256

            sk = int(self.skill_amount.get())
            if sk == '':
                sk = 00
            if sk < 0:
                sk = sk + 256

            towrite = [
                self.stats[0].get(),
                self.stats[1].get(),
                self.stats[2].get(),
                self.stats[3].get(),
                v1, v2,
                self.aspect.get(),
                int(EQUIPMENT_STAT[self.att.get()], 16),
                st,
                int(SKILL_ATTRIBUTE[self.skill.get()], 16),
                sk,
                int(self.inv_spell_dic[self.spell.get()][:2], 16),
                int(self.inv_spell_dic[self.spell.get()][2:], 16),
                self.spell_level.get(),
                (d[28] + d[29]),
                int(self.inv_spell_dic[self.magic.get()][:2], 16),
                int(self.inv_spell_dic[self.magic.get()][2:], 16),
                self.magic_level.get(),
                int(RESIST[self.resist.get()], 16),
                int(RESIST_AMOUNTS[self.resist_amount.get()], 16)
            ]

            f.seek(address + self.data_seek)
            for item in towrite:
                item = int_cast(item)
                f.write(item.to_bytes(1, byteorder='big'))

            self.reset_list()
            self.item.set(self.item_list[self.item_list.index(self.name.get().rstrip('\x00'))])
        self.set_defaults()
