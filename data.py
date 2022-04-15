import requests
import json
from bs4 import BeautifulSoup


def load_pokedex() -> dict:
    with open("pokedex.json", "r") as file:
        return json.load(file)


def load_movedex() -> dict:
    with open("movedex.json", "r") as file:
        return json.load(file)


def get_moves(name: str):
    url = "https://pokemondb.net/pokedex/"+name
    page = requests.get(url)
    # Parse html and get the main table
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("div", class_="tabset-moves-game sv-tabs-wrapper")
    movedex = load_movedex()
    ret = []
    for i in table.find_all("td"):
        if i.text in movedex.keys() and i.text not in ret:
            ret.append(i.text)
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
            "id": info[0].text,
            "type": info[2].text.strip().split(" "),
            "total": info[3].text,
            "hp": info[4].text,
            "attack": info[5].text,
            "defense": info[6].text,
            "sp-attack": info[7].text,
            "sp-defense": info[8].text,
            "speed": info[9].text,
            "description": "",
        }
        # Special case for Nidoran
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
            "tags": []
        }
        dump[info[0].text] = temp
    # Write to output file
    with open("movedex.json", "w") as outfile:
        outfile.write(json.dumps(dump, indent=4))


if __name__ == "__main__":
    generate_movedex()
    generate_pokedex()
