import pokemon
import database
import json


class Team:
    switch = "SWITCH"

    def __init__(self, ls):
        self.pkms: list[pokemon.Pokemon] = ls
        self.active: int = -1
        self.prepped_action = None

    def to_list(self):
        return list(p.to_dict() for p in self.pkms)

    def get_active(self):
        return self.pkms[self.active]

    def on_switch(self, new):
        print("Switched!")
        self.active = new

    def prepare_action(self):
        return 0

    def query_switch(self):
        pass

    def query_move(self):
        pass

    def perform_action(self, other):
        if isinstance(self.prepped_action, int):
            self.on_switch(self.prepped_action)
        else:
            self.pkms[self.active].use_move(self.prepped_action, other)
        self.prepped_action = None


class PlayerTeam(Team):
    def query_move(self):
        print("Which move?")
        self.pkms[self.active].print_moves()
        choice = int(input("> "))
        move = self.pkms[self.active].known_moves[choice - 1]
        self.prepped_action = move
        return move

    def query_switch(self):
        print("Which Pokemon?")
        for p in range(len(self.pkms)):
            print(str(p + 1) + ": " + self.pkms[p].name + " (KO)" if self.pkms[p].is_ko() else "")
        choice = input("> ")
        self.prepped_action = int(choice)
        return self.prepped_action

    def prepare_action(self):
        print("What would you like to do?")
        print("1. Attack\n2. Switch Pokemon")
        choice = int(input("> "))
        if choice == 1:
            move = self.query_move()
            return 1 if move.priority else 0
        if choice == 2:
            self.query_switch()
            return 2


def ask_team():
    team = {}
    pkm = []
    print("How many pokemon in team? 1-6")
    while True:
        i = input(database.INPUT_STR)
        if not i.isdigit():
            print("Not a number")
        elif not 1 <= int(i) <= 6:
            print("Invalid number")
        else:
            num = int(i)
            break

    for i in range(num):
        print("Pokemon in slot " + str(i + 1) + ":")
        temp = pokemon.Pokemon(pokemon.ask_pokemon_name())
        temp.known_moves += pokemon.ask_pokemon_moves(temp.name)
        pkm += [temp]

    team = Team(pkm)

    while True:
        print("What name to give this team?")
        i = input(database.INPUT_STR)
        if i in database.TEAMS:
            print("Team with that name already exists")
        elif i == "":
            print("Name cannot be empty")
        else:
            database.TEAMS[i] = team.to_list()
            with open("teams.json", "w") as outfile:
                outfile.write(json.dumps(database.TEAMS, indent=4))
            return
