import database


class Status:
    PAR = "Paralyzed"
    PSN = "Poisoned"
    BRN = "Burned"
    FRZ = "Frozen"
    CFD = "Confused"

    def __init__(self, id, length):
        self.id: int = id
        self.length: int = length


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
        self.level = 100

    def __gt__(self, other):
        return self.get("speed") > other.get("speed")

    def __lt__(self, other):
        return self.get("speed") < other.get("speed")

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

    def __str__(self):
        return "Hp: {}\nAtk: {}\nDef: {}\nSpa: {}\nSpd: {}\nSpe: {}".format(
            self.get("hp"), self.get("attack"), self.get("defense"),
            self.get("special_attack"), self.get("special_defense"), self.get("speed")
        )

    def get_base(self, key):
        return self.stats[key]
