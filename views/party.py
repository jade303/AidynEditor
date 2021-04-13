from views.characters import Characters


class PartyEdit(Characters):
    def __init__(self, f, i, a, n, r, t):
        super().__init__(f, i, a, n, r, t)
        self.win.title("Party Edit -- Edits are NEW GAME only")

        # run
        self.build()
        self.character.set(self.character_list[0])

    def build(self):
        super().build()

        self.skill_frame.configure(text='Skills\n(blank = cannot learn)')
