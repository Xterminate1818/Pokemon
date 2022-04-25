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

    def pass_turn(self, other):
        print(self.name + " - " +
              str(self.health) + "/" + str(self.get("hp"))
              )
        for m in self.known_moves:
            print(m.name)
        selected: Move = self.known_moves[int(input("Which move - "))]
        damage = selected.get_damage(self, other)
        effectiveness = 1.0
        for t in other.types:
            effectiveness *= database.TYPECHART[selected.dex["type"]][t]
        damage *= effectiveness
        damage *= 1.5 if selected.dex["type"] in self.types else 1.0
        damage = int(damage)
        print(self.name + " used move " + selected.name)
        if effectiveness > 1.0:
            print("It was super effective!")
        if effectiveness < 1.0 and effectiveness != 0.0:
            print("It wasn't very effective")
        if effectiveness == 0.0:
            print("It had no effect")
        print(str(damage) + " damage dealt")
        other.health -= damage


