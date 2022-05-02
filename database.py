import requests
import json
from bs4 import BeautifulSoup
from collections import defaultdict


def load_pokedex() -> dict:
	with open("pokedex.json", "r") as file:
		return json.load(file)


def load_movedex() -> dict:
	with open("movedex.json", "r") as file:
		return json.load(file)


def load_typechart() -> dict:
	with open("typechart.json", "r") as file:
		return json.load(file)


def load_teams() -> dict:
	with open("teams.json", "r") as file:
		return json.load(file)


POKEDEX = load_pokedex()
MOVEDEX = load_movedex()
TYPECHART = load_typechart()
TEAMS = load_teams()


def get_pokedex_id(id) -> str:
	for p in POKEDEX:
		if POKEDEX[p]["id"] == id:
			return p
	raise IndexError


def search_pokedex_name(name) -> list[str]:
	ret = []
	for p in POKEDEX:
		if name.lower() in p.lower():
			ret += [p]
	return ret


INPUT_STR = "> "



if __name__ == "__main__":
	def get_moves(name: str):
		url = "https://pokemondb.net/pokedex/" + name + "/moves/1"
		page = requests.get(url)
		# Parse html and get the main table
		soup = BeautifulSoup(page.content, "html.parser")
		table = soup.find("div", id="tab-moves-1")
		ret = []
		for i in table.find_all("tr"):
			temp = i.find("a", class_="ent-name")
			if temp is not None and temp.text != "0":
				ret.append(temp.text)
		return ret


	def generate_pokedex():
		# Grab html
		url = "https://pokemondb.net/pokedex/stats/gen1"
		page = requests.get(url)
		# Parse html and get the main table
		soup = BeautifulSoup(page.content, "html.parser")
		pokedex = soup.find(id="pokedex")
		rows = pokedex.find_all("tr")
		rows.pop(0)

		dump = {}
		for pkm in rows:
			info = pkm.find_all("td")
			temp = {
				"id": int(info[0].text),
				"type": info[2].text.strip().split(" "),
				"total": int(info[3].text),
				"hp": int(info[4].text),
				"attack": int(info[5].text),
				"defense": int(info[6].text),
				"sp-attack": int(info[7].text),
				"sp-defense": int(info[8].text),
				"speed": int(info[9].text),
				"description": "",
			}

			# Filter out special characters
			name = info[1].text
			name = name.replace("♀", "-f").replace("♂", "-m").replace("'", "").replace(". ", "-")
			print(name)
			temp["moves"] = get_moves(name)

			dump[info[1].text] = temp
		# Write to output file
		with open("pokedex.json", "w") as outfile:
			outfile.write(json.dumps(dump, indent=4))


	def parse_description(desc):
		desc = desc.lower()
		effects_who = "none"
		stat_effected = "none"
		level = 0
		chance = 100
		status = "none"
		# Who to effect
		if "user" in desc:
			effecst_who = "user"
		elif "opponent" in desc:
			effects_who = "opponent"
		# Stat changes
		if "special attack" in desc:
			stat_effected = "sp_attack"
		elif "special defense" in desc:
			stat_effected = "sp_defense"
		elif "attack" in desc:
			stat_effected = "attack"
		elif "defense" in desc:
			stat_effected = "defense"
		elif "speed" in desc:
			stat_effected = "speed"
		if stat_effected != "none":
			level = 0.5
		if "sharply" in desc:
			level = 1
		if "lower" in desc:
			level = -level
		# All moves marked as 'may' have a 10% chance
		if "may" in desc:
			chance = 10
		# Status effects
		if "paralyze" in desc:
			status = "Paralyze"
		if "sleep" in desc:
			status = "Sleep"
		if "confuse" in desc:
			status = "Confuse"
		if "freeze" in desc:
			status = "Freeze"
		if "burn" in desc:
			status = "Burn"
		if "poison" in desc:
			status = "Poison"
		return [effects_who, stat_effected, level, chance, status]


	def generate_movedex():
		# Grab html
		url = "https://pokemondb.net/move/generation/1"
		page = requests.get(url)
		# Parse html and get the main table
		soup = BeautifulSoup(page.content, "html.parser")
		movedex = soup.find("table")
		rows = movedex.find_all("tr")
		rows.pop(0)

		dump = {}
		for move in rows:
			info = move.find_all("td")
			effects = parse_description(info[6].text)
			temp = {
				"type": info[1].text,
				"category": info[2].get("data-sort-value"),
				"power": info[3].text.replace("\u2014", "-"),
				"accuracy": info[4].text.replace("\u2014", "-"),
				"pp": info[5].text.replace("\u2014", "-"),
				"description": info[6].text,
				"effects_who": effects[0],
				"stat_effected": effects[1],
				"level": effects[2],
				"chance": effects[3],
				"status": effects[4],
			}
			dump[info[0].text] = temp
		# Write to output file
		with open("movedex.json", "w") as outfile:
			outfile.write(json.dumps(dump, indent=4))


	def generate_typechart():
		# Grab html
		url = "https://pokemondb.net/type"
		page = requests.get(url)
		# Parse html and get the main table
		soup = BeautifulSoup(page.content, "html.parser")
		tbl = soup.find("tbody")
		dump = defaultdict(lambda: {})
		for td in tbl.find_all("td"):
			txt = td["title"].replace(" =", "").replace(" →", "")
			temp = txt.split(" ")
			t1 = temp[0]
			t2 = temp[1]
			mult = 1
			if "not very effective" in txt:
				mult = 0.5
			elif "no effect" in txt:
				mult = 0.0
			elif "super-effective" in txt:
				mult = 2.0
			dump[t1][t2] = mult
		with open("typechart.json", "w") as outfile:
			outfile.write(json.dumps(dump, indent=4))

# generate_pokedex()
# generate_movedex()
# generate_typechart()
