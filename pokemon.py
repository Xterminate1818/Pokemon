import database
import random
from move import Move
from statblock import StatBlock


class Pokemon(StatBlock):
    def __init__(self, name, mvs):
        super().__init__(name)
        self.name = name
        self.dex = database.POKEDEX[name]
        self.health = int(self.get("hp"))
        self.types = self.dex["type"]
        self.known_moves = mvs

    def __str__(self):
        return self.name + str(self.stats)

    def handle_status(self):
        pass

    def print_moves(self):
        for i in range(len(self.known_moves)):
            print(str(i+1) + ": " + self.known_moves[i].name)

    def use_move(self, move, target):
        # Damage calculation
        damage = move.get_damage(self, target)
        effectiveness = 1.0
        for t in target.types:
            effectiveness *= database.TYPECHART[move.dex["type"]][t]
        damage *= effectiveness
        damage *= 1.5 if move.dex["type"] in self.types else 1.0
        damage = int(damage)
        print(self.name + " used move " + move.name)
        if effectiveness > 1.0:
            print("It was super effective!")
        if effectiveness < 1.0 and effectiveness != 0.0:
            print("It wasn't very effective")
        if effectiveness == 0.0:
            print("It had no effect")
        print(str(damage) + " damage dealt")
        target.health -= damage
        # Secondary effects
        if move.dex["effects_who"] == "user":
