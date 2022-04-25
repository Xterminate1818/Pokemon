from pokemon import Pokemon
from move import Move


class Team:
    def __init__(self, ls):
        self.pkms: list[Pokemon] = ls
        self.active: int = 0

    def get_active(self):
        return self.pkms[self.active]

    def switch(self, new):
        self.active = new


class Battle:
    def __init__(self, t1, t2):
        self.team1: Team = t1
        self.team2: Team = t2
        self.current_turn = 1

    def pass_turn(self):
        order = [self.team1.get_active(), self.team2.get_active()]
        order.sort()
        fast: Pokemon = order[0]
        slow: Pokemon = order[1]

        fast.pass_turn(slow)
        slow.pass_turn(fast)


t1 = Team([Pokemon("Bulbasaur", [Move("Vine Whip")])])
t2 = Team([Pokemon("Charmander", [Move("Ember")])])

b = Battle(t1, t2)
b.pass_turn()
