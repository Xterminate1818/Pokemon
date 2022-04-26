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


POKEDEX = load_pokedex()
MOVEDEX = load_movedex()
TYPECHART = load_typechart()

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
            temp = {
                "type": info[1].text,
                "category": info[2].get("data-sort-value"),
                "power": info[3].text.replace("\u2014", "-"),
                "accuracy": info[4].text.replace("\u2014", "-"),
                "pp": info[5].text.replace("\u2014", "-"),
                "description": info[6].text,
                "user_effects": [],
                "target_effects": []
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

    #generate_pokedex()
    #generate_movedex()
    #generate_typechart()
