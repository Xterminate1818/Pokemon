import database
import random


class StatBlock:
    def __init__(self, name: str):
        dex = database.POKEDEX[name]
        self.stats = {
            "hp": dex["hp"],
            "attack": dex["attack"],
            "defense": dex["defense"],
            "sp_attack": dex["sp-attack"],
            "sp_defense": dex["sp-defense"],
            "speed": dex["speed"]
        }
        self.stat_stages = {
            "hp": 0,
            "attack": 0,
            "defense": 0,
            "sp_attack": 0,
            "sp_defense": 0,
            "speed": 0
        }
        self.statuses = {
            "Paralyze": False,
            "Poison": False,
            "Freeze": 0,
            "Burn": False,
            "Confuse": 0,
            "Infatuate": False,
        }
        self.level = 100

    def __gt__(self, other):
        return self.get("speed") > other.get("speed")

    def __lt__(self, other):
        return self.get("speed") < other.get("speed")

    def on_switch(self):
        self.stat_stages = {
            "hp": 0,
            "attack": 0,
            "defense": 0,
            "sp_attack": 0,
            "sp_defense": 0,
            "speed": 0
        }

    def get(self, key):
        ret = self.stats[key]
        ret *= (self.level / 50)
        if key == "hp":
            return ret + 110
        # Stat stages
        stage = self.stat_stages[key]
        numerator = 2
        denominator = 2
        if stage > 0:
            numerator += 2
        if stage < 0:
            denominator += abs(stage)
        return ret * (numerator / denominator)

    def modify_stat(self, key, amount):
        self.stat_stages[key] += amount

    def add_status(self, status):
        if status == "Freeze" or status == "Confusion":
            self.statuses[status] = max(self.statuses[status], random.randint(2, 5))
        else:
            self.statuses[status] = True

    def __str__(self):
        return "Hp: {}\nAtk: {}\nDef: {}\nSpa: {}\nSpd: {}\nSpe: {}".format(
            self.get("hp"), self.get("attack"), self.get("defense"),
            self.get("special_attack"), self.get("special_defense"), self.get("speed")
        )

    def get_base(self, key):
        return self.stats[key]
