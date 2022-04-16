import database


class StatBlock:
    def __init__(self, hp: int, attack: int, defense: int, sp_attack: int, sp_defense: int, speed: int):
        self.hp:            int = hp
        self.attack:        int = attack
        self.defense:       int = defense
        self.sp_attack:     int = sp_attack
        self.sp_defense:    int = sp_defense
        self.speed:         int = speed

    @staticmethod
    def from_pokedex(dex: dict):
        return StatBlock(
            int(dex["hp"]),
            int(dex["attack"]),
            int(dex["defense"]),
            int(dex["sp-attack"]),
            int(dex["sp-defense"]),
            int(dex["speed"]),
        )


class Pokemon:
    def __init__(self, name):
        self.dex = database.POKEDEX[name]
        self.stats = StatBlock.from_pokedex(self.dex)
        self.level = 100

    def use_move(self, move, target):
        if move["power"] == '-':

