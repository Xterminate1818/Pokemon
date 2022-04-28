import database
from statblock import StatBlock


class Move:
    def __init__(self, name):
        self.name = name
        self.dex = database.MOVEDEX[name]
        self.pp = 999 if self.dex["pp"] == "-" else int(self.dex["pp"])
        self.priority = (self.name == "Quick Attack")

    def get_damage(self, user_stats, target_stats):
        power = self.dex["power"]
        if power == '-':
            return 0
        power = int(power)

        # https://static0.gamerantimages.com/wordpress/wp-content/uploads/2021/09/pokemon-damage-calculation-equation-and-ashs-injured-anime-pokemon.jpg
        # Physical or special damage
        atk_stat = user_stats.get("sp_attack")
        def_stat = target_stats.stats.get("sp_defense")
        if self.dex["category"] == "physical":
            atk_stat = user_stats.get("attack")
            def_stat = target_stats.get("defense")

        final_damage = (2 * user_stats.level / 5 + 2) * power * (atk_stat / def_stat)
        final_damage /= 50
        final_damage += 2
        return final_damage
