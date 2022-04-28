from pokemon import Pokemon
from move import Move
from team import PlayerTeam, Team


class Battle:
	def __init__(self, t1, t2):
		self.team1: Team = t1
		self.team2: Team = t2
		self.current_turn = 1

	def pass_turn(self):
		a1 = self.team1.prepare_action()
		a2 = self.team2.prepare_action()

		fast = self.team1
		slow = self.team2

		if a1 == a2 and self.team2.get_active() > self.team1.get_active():
			fast = self.team2
			slow = self.team1

		if a2 > a1:
			fast = self.team2
			slow = self.team1

		fast.perform_action(slow.get_active())
		slow.perform_action(fast.get_active())

		fast.get_active().post_move()
		slow.get_active().post_move()

		if fast.get_active().is_ko():
			switch = fast.query_switch()
			fast.on_switch(switch)
		if slow.get_active().is_ko():
			switch = slow.query_switch()
			slow.perform_action(switch)

