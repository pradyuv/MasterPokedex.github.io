import requests
from bs4 import BeautifulSoup


URL = "https://pokemondb.net/pokedex/all"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
pokedex = soup.findAll("td", class_="cell-name")

for i in range(len(pokedex)):
    strPokemon = str(pokedex[i].encode("utf-8"))

    
    
    firstClosingBrace = strPokemon.index(">")
    secondClosingBrace = strPokemon[firstClosingBrace + 1:].index(">")
    thirdOpeningBrace = strPokemon[firstClosingBrace + secondClosingBrace + 2:].index("<")

    # Printing the name of the pokemon, but adding a different end character depending on if there's a unique version of said pokemon (e.g. megas, alolan, primal, etc.)
    if ("small" in strPokemon):
        print(strPokemon[firstClosingBrace + secondClosingBrace + 2:firstClosingBrace + secondClosingBrace + thirdOpeningBrace + 2], end=" ")
    else:
        print(strPokemon[firstClosingBrace + secondClosingBrace + 2:firstClosingBrace + secondClosingBrace + thirdOpeningBrace + 2])

    # Printing the unique version of said pokemon
    if ("small" in strPokemon):
        startingIndex = strPokemon.index("muted\">") + 7
        endingIndex = strPokemon[startingIndex:].index("<")
        print (strPokemon[startingIndex:startingIndex + endingIndex])
