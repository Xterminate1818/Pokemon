from pokemon import Pokemon
from move import Move
from team import Team


class Battle:
    def __init__(self, t1, t2):
        self.team1: Team = t1
        self.team2: Team = t2
        self.current_turn = 1

    def pass_turn(self):
        a1 = t1.get_action()
        a2 = t2.get_action()

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
