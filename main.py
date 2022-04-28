from team import Team
from pokemon import Pokemon
from battle import Battle
import database


def ask(message: str, check, handler=None):
	while True:
		print(message)
		i = input("> ")
		if check(i):
			return i
		elif handler is not None:
			handler(i)


def ask_pokemon_name():
	while True:
		print("Enter a number between 1 and 151 to select a pokemon, or a string to search the pokedex")
		i = input("> ")
		if i.isdigit() and 1 <= int(i) <= 151:
			return database.get_pokedex_id(int(i))
		else:
			search_result = database.search_pokedex_name(i)
			if len(search_result) == 0:
				print("No results found for: " + i)
			for p in database.search_pokedex_name(i):
				print(str(database.POKEDEX[p]["id"]) + ": " + p)


def ask_pokemon_moves(pkm):
	print("Selecting moves for: " + pkm)
	print("Available moves: ")
	for m in database.POKEDEX[pkm]["moves"]:
		print(m)
	moves = []
	for j in range(4):
		while True:
			print("\nWhat move to use in slot " + str(j+1) + "?")
			i = input("> ")
			if i not in database.MOVEDEX:
				print("Unknown move: " + i)
			elif i in moves:
				print("Already knows move: " + i)
			else:
				moves += [i]
				break
	return moves


print(ask_pokemon_moves("Mew"))
