from pokemon import Pokemon


class Team:
    switch = "SWITCH"

    def __init__(self, ls):
        self.pkms: list[Pokemon] = ls
        self.active: int = -1

    def get_active(self):
        return self.pkms[self.active]

    def on_switch(self, new):
        self.active = new

    def get_action(self):
        return


class PlayerTeam(Team):
    def get_action(self):
        print("What would you like to do?")
        choice = int(input("1. Attack\n2. Switch Pokemon"))
        if choice == 1:
            print("Which move?")
            self.pkms[self.active].print_moves()
            choice = int(input("> "))
            return self.pkms[self.active].known_moves[choice-1]
        if choice == 2:
            print("Which Pokemon?")
            for p in range(len(self.pkms)):
                print(str(p+1) + ": " + self.pkms[p].name)

