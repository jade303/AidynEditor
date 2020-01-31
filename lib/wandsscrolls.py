from functools import partial
from tkinter import Toplevel, Label, StringVar, LabelFrame, Entry
from tkinter.ttk import Combobox

from lib.limits import limit, limit_127
from lib.variables import WAND_NAMES, SCROLL_NAMES, WAND_ADDRESSES, SCROLL_ADDRESSES, inv_SPELLS, inv_SKILL_ATTRIBUTE, \
    inv_RESIST, inv_RESIST_AMOUNTS


class WandScrollEdit:
    def __init__(self, filename, icon_dir):
        wandwin = Toplevel()
        wandwin.resizable(False, False)
        wandwin.title("Item Edit")
        wandwin.iconbitmap(icon_dir)
        filename = filename
        data_seek = 24
        data_read = 20
        name_length = 18

        label = Label(wandwin, text='Not yet finished')
        label.grid()

        """def wand_defaults(*args):
            with open(filename, 'rb') as f:
                address = WAND_ADDRESSES[WAND_NAMES.index(wand.get())]
                f.seek(address)
                wand_name.set(f.read(name_length).decode("utf-8"))

                f.seek(address + data_seek)
                data = f.read(data_read)
                d = data.hex()

                wand_str_req.set(int(d[10] + d[11], 16))
                wand_int_req.set(int(d[10] + d[11], 16))
                wand_value.set((int(d[10] + d[11], 16) * 256) + int(d[8] + d[9], 16))
                wand_aspect.set(d[13])
                wand_skill.set(inv_SKILL_ATTRIBUTE[(d[18] + d[19]).upper()])
                att_amount = int(d[20] + d[21], 16)
                if att_amount > 127:
                    att_amount = att_amount - 256
                wand_skill_amount.set(att_amount)
                wand_spell.set(inv_SPELLS[(d[22:26]).upper()])
                wand_charges.set(int(d[10] + d[11], 16))
                wand_spell_level.set(int(d[28] + d[29], 16))
                wand_resist.set(inv_RESIST[(d[36] + d[37]).upper()])
                wand_resist_amount.set(inv_RESIST_AMOUNTS[(d[38] + d[39]).upper()])

        def scroll_defaults(*args):
            with open(filename, 'rb') as f:
                address = SCROLL_ADDRESSES[SCROLL_NAMES.index(scroll.get())]
                f.seek(address)
                scroll_name.set(f.read(name_length).decode("utf-8"))

                f.seek(address + data_seek)
                data = f.read(data_read)
                d = data.hex()

                scroll_value.set((int(d[10] + d[11], 16) * 256) + int(d[8] + d[9], 16))
                scroll_spell.set(inv_SPELLS[(d[22:26]).upper()])
                scroll_cast_level.set(int(d[28] + d[29], 16))

        def wand_write():
            pass

        def scroll_write():
            pass

        def build():
            scroll_frame = LabelFrame(wandwin, text='Scrolls:')
            scroll_frame.grid(column=0, row=0)
            scroll_box = Combobox(scroll_frame, textvariable=scroll, values=SCROLL_NAMES)
            scroll_box.grid(column=0, row=0)
            scroll_box.config(width=21)
            scroll_value_label = Label(scroll_frame, text='Base Value')
            scroll_value_label.grid(column=0, row=1, sticky='e')
            scroll_value_entry = Entry(scroll_frame, textvariable=scroll_value)
            scroll_value_entry.grid(column=1, row=1, sticky='e')
            scroll_value_entry.config(width=6)

        wand = StringVar()
        wand.trace('w', wand_defaults)
        wand_name = StringVar()
        wand_name.trace('w', partial(limit, wand_name, name_length))
        wand_str_req = StringVar()
        wand_str_req.trace('w', partial(limit, wand_str_req, 30))
        wand_int_req = StringVar()
        wand_int_req.trace('w', partial(limit, wand_str_req, 30))
        wand_value = StringVar()
        wand_value.trace('w', partial(limit, wand_value, 65535))
        wand_aspect = StringVar()
        wand_skill = StringVar()
        wand_skill_amount = StringVar()
        wand_skill_amount.trace('w', partial(limit_127, wand_skill_amount))
        wand_spell = StringVar()
        wand_charges = StringVar()
        wand_charges.trace('w', partial(limit, wand_charges, 255))
        wand_spell_level = StringVar()
        wand_spell_level.trace('w', partial(limit, wand_spell_level, 255))
        wand_resist = StringVar()
        wand_resist_amount = StringVar()

        scroll = StringVar()
        scroll.trace('w', scroll_defaults)
        scroll_name = StringVar()
        scroll_name.trace('w', partial(limit, scroll_name, name_length))
        scroll_value = StringVar()
        scroll_value.trace('w', partial(limit, scroll_value, 65535))
        scroll_spell = StringVar()
        scroll_cast_level = StringVar()
        scroll_cast_level.trace('w', partial(limit, scroll_cast_level, 15))

        wand.set(WAND_NAMES[0])
        scroll.set(SCROLL_NAMES[0])
        build()"""
