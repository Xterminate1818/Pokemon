import requests
import json
from bs4 import BeautifulSoup
from collections import defaultdict
from PIL import Image


def load_pokedex() -> list[dict]:
	with open("pokedex.json", "r") as file:
		return json.load(file)


def load_movedex() -> list[dict]:
	with open("movedex.json", "r") as file:
		return json.load(file)


def load_typechart() -> dict:
	with open("typechart.json", "r") as file:
		return json.load(file)


def load_teams() -> dict:
	with open("teams.json", "r") as file:
		return json.load(file)


def get_sprite(_id):
	return Image.open("./images/" + str(_id) + ".png")

POKEDEX: list[dict] = load_pokedex()
MOVEDEX: list[dict] = load_movedex()
TYPECHART = load_typechart()
TEAMS = load_teams()


def add_team(name: str, info: list[dict]):
	TEAMS[name] = info
	with open("teams.json", "w") as outfile:
		outfile.write(json.dumps(TEAMS, indent=4))


def _search(what: list, key: str, value, comp, get=None, amount=None) -> list[dict]:
	comp_func = {
		"==": value.__eq__,
		"!=": value.__ne__,
		"<=": value.__le__,
		">=": value.__ge__,
		"<": value.__lt__,
		">": value.__gt__
	}[comp]
	if isinstance(value, str):
		if comp == "==":
			comp_func = lambda a, b=value: (b.lower() in a.lower())
		elif comp == "!=":
			comp_func = lambda a, b=value: (b.lower() not in a.lower())

	ret = []
	for i in what:
		if comp_func(i[key]):
			if get is None:
				ret += [i]
			else:
				ret += [i[get]]
	if amount is not None and len(ret) > amount:
		ret = ret[:amount]
	if amount == 1:
		return ret[0] if len(ret) > 0 else None
	return ret


def search_pokedex(key: str, value, comp="==", get=None, amount=None):
	return _search(POKEDEX, key, value, comp, get=get, amount=amount)


def search_movedex(key: str, value, comp="==", get=None, amount=None):
	return _search(MOVEDEX, key, value, comp, get=get, amount=amount)


INPUT_STR = ">"

if __name__ == "__main__":
	def get_moves(name: str) -> list[str]:
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


	def generate_pokedex() -> None:
		# Grab html
		url = "https://pokemondb.net/pokedex/stats/gen1"
		page = requests.get(url)
		# Parse html and get the main table
		soup = BeautifulSoup(page.content, "html.parser")
		pokedex = soup.find(id="pokedex")
		rows = pokedex.find_all("tr")
		rows.pop(0)

		dump = []
		for pkm in rows:
			info = pkm.find_all("td")
			temp = {
				"id": int(info[0].text),
				"name": str(info[1].text),
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
			dump.append(temp)

		# Write to output file
		with open("pokedex.json", "w") as outfile:
			outfile.write(json.dumps(dump, indent=4))


	def parse_description(desc) -> list:
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

		dump = []
		for move in rows:
			info = move.find_all("td")
			effects = parse_description(info[6].text)
			temp = {
				"name": info[0].text,
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
			dump.append(temp)
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


	def generate_images():
		# Grab html
		url = "https://pokemondb.net/pokedex/game/red-blue-yellow"
		page = requests.get(url)
		# Parse html and get the main table
		soup = BeautifulSoup(page.content, "html.parser")
		index = 1
		for i in soup.find_all("img", class_="img-sprite img-sprite-v1"):
			print(i["src"])
			image_url = i["src"]
			image_data = requests.get(image_url).content
			with open("images/" + str(index) + ".png", 'wb') as handler:
				handler.write(image_data)
			index += 1

# generate_images()
# generate_pokedex()
# generate_movedex()
# generate_typechart()
