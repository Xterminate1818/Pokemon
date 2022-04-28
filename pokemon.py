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

    def is_ko(self):
        return self.health <= 0

    def __str__(self):
        return self.name + str(self.stats)

    def print_moves(self):
        for i in range(len(self.known_moves)):
            print(str(i+1) + ": " + self.known_moves[i].name)

    def pre_move(self, move, target):
        # Frozen
        if self.statuses["Freeze"] > 0:
            self.statuses["Freeze"] -= 1
            print(self.name + " is frozen and can't move!")
            return True

        # Paralyzed
        if self.statuses["Paralyze"] and random.randint(0, 100) > 75:
            print(self.name + " is paralyzed and can't move!")
            return True

        # Out of pp
        if move.pp <= 0:
            print(self.name + " tried to use move " + move.name + ", but it was out of PP!")
            return True
        move.pp -= 1

        # Confusion
        if self.statuses["Confuse"] > 0:
            self.statuses["Confuse"] -= 1
            if random.randint(0, 100) > 50:
                print(self.name + " hurt itself in its confusion! (not implemented)")
                return True

        # Accuracy check
        if move.dex["accuracy"] != "-" and random.randint(0, 100) > int(move.dex["accuracy"]):
            print(self.name + " missed!")
            return True

        return False

    def post_move(self):
        if self.statuses["Poison"] or self.statuses["Burn"]:
            self.health -= self.get("hp") / 8
        if self.health <= 0:
            print(self.name + " has been knocked unconscious!")

    def secondary_effects(self, move, target):
        who = move.dex["effects_who"]
        stat = move.dex["stat_effected"]
        level = move.dex["level"]
        status = move.dex["status"]
        if who == "none":
            return
        if random.randint(0, 100) > move.dex["chance"]:
            return
        secondary_target = self if who == "user" else target
        if stat != "none":
            secondary_target.modify_stat(stat, level)
            print(
                (self.name if who == "user" else target.name) + "'s " +
                stat + " was " +
                ("sharply " if abs(level) == 1 else "") +
                ("raised" if level > 0 else "lowered")
            )
        if status != "none":
            secondary_target.add_status(status)
            print(
                (self.name if who == "user" else target.name) + " has been effected by status: " + status
            )

    def use_move(self, move, target):
        if self.pre_move(move, target):
            return

        # Damage calculation
        print(self.name + " used move " + move.name)
        damage = move.get_damage(self, target)
        if damage > 0:
            effectiveness = 1.0
            for t in target.types:
                effectiveness *= database.TYPECHART[move.dex["type"]][t]
            print("effectiveness: " + str(effectiveness))
            damage *= effectiveness
            damage *= 1.5 if move.dex["type"] in self.types else 1.0
            damage = int(damage)
            if effectiveness > 1.0:
                print("It was super effective!")
            if effectiveness < 1.0 and effectiveness != 0.0:
                print("It wasn't very effective")
            if effectiveness == 0.0:
                print("It had no effect")
            print(str(damage) + " damage dealt")
            target.health -= damage

        self.secondary_effects(move, target)

