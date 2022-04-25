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
        self.level = 100

    def __str__(self):
        return "Hp: {}\nAtk: {}\nDef: {}\nSpa: {}\nSpd: {}\nSpe: {}".format(
            *self.stats.values()
        )

    def __gt__(self, other):
        return self.get("speed") > other.get("speed")

    def __lt__(self, other):
        return self.get("speed") < other.get("speed")

    def get(self, key):
        ret = self.stats[key]
        ret *= (self.level / 50)
        if key == "hp":
            ret += 110
        return ret

    def get_base(self, key):
        return self.stats[key]
