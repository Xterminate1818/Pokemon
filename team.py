from pokemon import Pokemon


class Team:
	switch = "SWITCH"

	def __init__(self, ls):
		self.pkms: list[Pokemon] = ls
		self.active: int = -1
		self.prepped_action = None

	def get_active(self):
		return self.pkms[self.active]

	def on_switch(self, new):
		print("Switched!")
		self.active = new

	def prepare_action(self):
		return 0

	def perform_action(self, other):
		if isinstance(self.prepped_action, int):
			self.on_switch(self.prepped_action)
		else:
			self.pkms[self.active].use_move(self.prepped_action, other)
		self.prepped_action = None


class PlayerTeam(Team):
	def prepare_action(self):
		print("What would you like to do?")
		print("1. Attack\n2. Switch Pokemon")
		choice = int(input("> "))
		if choice == 1:
			print("Which move?")
			self.pkms[self.active].print_moves()
			choice = int(input("> "))
			move = self.pkms[self.active].known_moves[choice - 1]
			self.prepped_action = move
			return 1 if move.priority else 0
		if choice == 2:
			print("Which Pokemon?")
			for p in range(len(self.pkms)):
				print(str(p + 1) + ": " + self.pkms[p].name)
			choice = input("> ")
			self.prepped_action = int(choice)
			return 2

