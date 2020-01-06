from tkinter import *
from variables import SPELL_NAMES


class SpellEdit:
    def __init__(self, filename):
        spellwin = Toplevel()
        spellwin.title("Spell Edit")
        filename = filename

        def read_defaults():
            pass

        def write_values():
            pass

        def build_window():
            lawfulgood_frame = Frame(spellwin)
            lawfulgood_frame.grid(column=0, row=0)
            default_spell_menu = OptionMenu(lawfulgood_frame, spell, *SPELL_NAMES)
            default_spell_menu.grid()

        spell = StringVar()
        # spell.trace('w', read_defaults)
        school = IntVar()
        damage = IntVar()
        stamina = IntVar()
        targetnum = IntVar()
        targettype = IntVar()
        # targetarea = IntVar()
        wizard = IntVar()
        aspect = IntVar()
        range = IntVar()
        exp = IntVar()

        spell.set(SPELL_NAMES[27])
        build_window()