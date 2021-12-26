# Importing the necessary libraries for webscraping
import requests
import string
from bs4 import BeautifulSoup
import re

# *********************************************************************************************************************** #
#                                                     UNOFFICIAL POKEDEX (NAME PENDING)                                   #
# Welcome to the unofficial pokedex, a joint project consisting of Pradyu and Meekyle. The aim for this project was to    #
# create an online, interactive pokedex, putting our Python and web development skills to the test (two things that       #
# we focused on heavily in the first semester of university). This Python script's main purpose is to collect             #
# all the information necessary to create a pokedex. And, as the saying goes, why put in hard labour for a day to         #
# collect said information when you could automate it within a week? This Python script scrapes the Pokemondb.net         #
# website to gather the necessary information, and when we are done curating the data, we will write it to a file         #
# which we will then use as a "database" of sorts for our interactive pokedex.                                            #
#                                                                                                                         #
# We sincerely hope you enjoy this project. There will definitely be more to come from both parties in the future.        #
# *********************************************************************************************************************** #

allTypes = ['Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying',
            'Psychic', 'Bug', 'Rock', 'Ghost', 'Dark', 'Dragon', 'Steel', 'Fairy']


# This function here will take the processed names of each pokemon and then retrieve the necessary information
# from pokemondb.net. So far, it will only retrieve the pokedex number, but it's a start. Next steps include typing
# evolutions, evolution info (e.g. level it evolves at, specific conditions for evolution)
def printingInfo(pokemon):
    pokemonInfo = []
    # list referenced after to check for Pokemon types
    # Iterating over the list of names
    for name in pokemon:
        # Webscraping each individual page and then retrieving the pokedex number (as of writing this comment)
        # SUPER INEFFICIENT, ONLY PURPOSE WILL BE TO WRITE TO A FILE THAT WILL THEN BE REFERENCED BY THE
        # WEBPAGE
        tempurl = "https://pokemondb.net/pokedex/" + name.lower()
        temppage = requests.get(tempurl)
        tempSoup = BeautifulSoup(temppage.content, "html.parser")

        # Finding the element that contains the pokedex number for the pokemon. Fortunately for us, the pokedex
        # number is the only <strong> element in the entire webpage
        if name!="Zygarde" and name!="Toxel" and name!="Toxtricity":
            pokedexNumber = int(tempSoup.find("strong").get_text())
        elif name == "Zygarde":
            pokedexNumber=718
        elif name == "Toxel":
            pokedexNumber=848
        elif name == "Toxtricity":
            pokedexNumber=849
        pokemonType = list(tempSoup.findAll("a", class_="type-icon"))
        evolutionConditionRaw = list((tempSoup.findAll("i", class_="icon-arrow")))
        if name!="Pumpkaboo" and name!="Gourgeist":
            pokemonIconSrcFinder = str(list(tempSoup.find("a",{"rel":"lightbox"})))
            startSrc = pokemonIconSrcFinder.index("src=")
        elif name == 'Pumpkaboo':
            pokemonIconSrcFinder = '"https://img.pokemondb.net/artwork/pumpkaboo.jpg"'
            startSrc=None
        else:
            pokemonIconSrcFinder = '"https://img.pokemondb.net/artwork/gourgeist.jpg"'
            startSrc=None
        endSrclst=[]
        if startSrc is not None:
            for j in range(len(pokemonIconSrcFinder)-1,0,-1):
                if pokemonIconSrcFinder[j]=='"':
                    endSrclst.append(j)
                if len(endSrclst)>=3:
                    break
            pokemonIconSrc = pokemonIconSrcFinder[startSrc + len("src="):endSrclst[-1] + 1]
        pokemonDescp=(tempSoup.find("td",class_="cell-med-text")).string
        evolutionCondition = []
        for e in evolutionConditionRaw:
            if name == "Nincada" or name == "Ninjask" or name == "Shedinja":
                evolutionCondition.append(['(Level 20)','(Level 20, empty spot in party, Pokéball in bag)'])
                continue
            else:
                try:
                    evolutionCondition.append(e.next_sibling.get_text())
                except AttributeError:
                    try:
                        evolutionCondition.append(e.next_sibling.get_text())
                    except AttributeError:
                        evolutionCondition.append(e.previous_sibling.get_text())
        evolution = [x for x in evolutionCondition if x is not None]
        thisPokemonType = []
        # Checks if a pokemon has a certain type and appends it to its own list
        for x in range(2):
            if "title" not in pokemonType[x]:
                for typeCheck in allTypes:
                    if typeCheck in pokemonType[x]:
                        thisPokemonType.append(typeCheck)
        wFinder = tempSoup.find("th", string="Weight")
        hFinder = tempSoup.find("th", string="Height")
        baseStats=(tempSoup.find("td", class_="cell-total")).string

        if 0<pokedexNumber<=151:
            generationIntro=(1,"Kanto")
        elif 151<pokedexNumber<=251:
            generationIntro=(2,"Johto")
        elif 251<pokedexNumber<=386:
            generationIntro=(3,"Hoenn")
        elif 386<pokedexNumber<=493:
            generationIntro=(4,"Sinnoh")
        elif 493<pokedexNumber<=649:
            generationIntro=(5,"Unova")
        elif 649<pokedexNumber<=721:
            generationIntro=(6,"Kalos")
        elif 721<pokedexNumber<=809:
            generationIntro=(7,"Alola")
        else:
            generationIntro=(8,"Galar")
        normalAbilitiesList=list(tempSoup.findAll("span",class_="text-muted",limit=3))
        try:
            normalAbilityOneRaw=str(normalAbilitiesList[0])
            normalAbilityTwoRaw=str(normalAbilitiesList[1])
        except IndexError:
            x = 0
            y = 0
            openingBraceAbilityOne = 0
            closingBraceAbilityOne = 0
            for m in range(len(normalAbilityOneRaw)):
                if normalAbilityOneRaw[m] == ">":
                    x += 1
                if x == 2:
                    openingBraceAbilityOne = m
                    break
            for k in range(len(normalAbilityOneRaw)):
                if normalAbilityOneRaw[k] == "<":
                    y += 1
                if y == 3:
                    closingBraceAbilityOne = k
                    break
            normalAbilityOne = normalAbilityOneRaw[openingBraceAbilityOne + 1:closingBraceAbilityOne]
            normalAbilityTwo=''
        else:
            x = 0
            y = 0
            openingBraceAbilityOne = 0
            closingBraceAbilityOne = 0
            for m in range(len(normalAbilityOneRaw)):
                if normalAbilityOneRaw[m] == ">":
                    x += 1
                if x == 2:
                    openingBraceAbilityOne = m
                    break
            for k in range(len(normalAbilityOneRaw)):
                if normalAbilityOneRaw[k] == "<":
                    y += 1
                if y == 3:
                    closingBraceAbilityOne = k
                    break
            x = 0
            y = 0
            openingBraceAbilityTwo = 0
            closingBraceAbilityTwo = 0
            for c in range(len(normalAbilityTwoRaw)):
                if normalAbilityTwoRaw[c] == ">":
                    x += 1
                if x == 2:
                    openingBraceAbilityTwo = c
                    break
            for d in range(len(normalAbilityTwoRaw)):
                if normalAbilityTwoRaw[d] == "<":
                    y += 1
                if y == 3:
                    closingBraceAbilityTwo = d
                    break
            normalAbilityOne = normalAbilityOneRaw[openingBraceAbilityOne + 1:closingBraceAbilityOne]
            normalAbilityTwo = normalAbilityTwoRaw[openingBraceAbilityTwo + 1:closingBraceAbilityTwo]
        pokeHP=tempSoup.find("th",string="HP").next_sibling.next_sibling.string
        pokeAtt=tempSoup.find("th",string="Attack").next_sibling.next_sibling.string
        pokeDef=tempSoup.find("th",string="Defense").next_sibling.next_sibling.string
        pokeSpAtt=tempSoup.find("th",string="Sp. Atk").next_sibling.next_sibling.string
        pokeSpDef=tempSoup.find("th",string="Sp. Def").next_sibling.next_sibling.string
        pokeSpeed=tempSoup.find("th",string="Speed").next_sibling.next_sibling.string
        pokeStats=["HP: "+pokeHP,"Attack "+pokeAtt,"Defense "+pokeDef,"Special Attack "+pokeSpAtt,"Special Defense "+pokeSpDef,"Speed "+pokeSpeed]
        weight = wFinder.next_sibling.next_sibling
        height = hFinder.next_sibling.next_sibling
        # Appending the pokedex number and the name to the pokemon info list
        possibleAbiltiesRaw = [normalAbilityOne, normalAbilityTwo]
        for h in range(len(possibleAbiltiesRaw)):
            for v in range(len(possibleAbiltiesRaw[h])):
                if (possibleAbiltiesRaw[h][v].isalpha() or possibleAbiltiesRaw[h][v] ==' ') == False:
                    possibleAbiltiesRaw[h]=None
                    break
        possibleAbilites=[s for s in possibleAbiltiesRaw if s is not None]
        pokemonInfo.append([pokedexNumber, name, thisPokemonType, weight, height, evolution,pokemonIconSrc,pokemonDescp,baseStats,possibleAbilites,pokeStats])
    # Returning the list to the user (IN THE FUTURE, THIS LIST WILL BE WRITTEN TO A FILE, BUT FOR DEBUGGING PURPOSES
    # WE ARE JUST PRINTING FOR THE TIME BEING)
    return pokemonInfo


# This is the link that contains all the pokemon, will be retrieving the names of all the Pokemon through
# this link her e
URL = "https://pokemondb.net/pokedex/all"
# Getting the contents of the page
page = requests.get(URL)

# Creating a beautiful soup instance with the contents of the page
soup = BeautifulSoup(page.content, "html.parser")

# Getting each td entry, as the td elements contain the pokemon's name
pokedex = soup.findAll("td", class_="cell-name")

# A list that contains all the unique pokemons
pokemon_names = []

# A list that will contain any versions of each pokemon (e.g. megas, alolan, primal, etc.)
pokemon_names_with_megas = []

# Going through each table data element for processing purposes
for i in range(len(pokedex)):
    # Some processing of the raw text. Converting the line into a usable data type, string
    strPokemon = str(pokedex[i].encode("utf-8"))
    # Formatting the text to get the name out of the mess that is the HTML surrounding it
    firstClosingBrace = strPokemon.index(">")
    secondClosingBrace = strPokemon[firstClosingBrace + 1:].index(">")
    thirdOpeningBrace = strPokemon[firstClosingBrace + secondClosingBrace + 2:].index("<")

    # Assigning the formatted name to a variable for easy reference's sake
    name = strPokemon[
           firstClosingBrace + secondClosingBrace + 2:firstClosingBrace + secondClosingBrace + thirdOpeningBrace + 2]

    # Some processing of the name to ensure no punctuation is passed through. Some pokemon contain punctuation in
    # their name, and this punctuation is often not carried over in links. As a result, it is necessary to remove the
    # name of all invalid punctuation before it it sent off for web scraping their specific pages
    formattedName = ""
    for letter in name:
        if letter == "-":
            formattedName += "-"
        elif letter not in string.punctuation and letter != " ":
            formattedName += letter
        elif letter == " ":
            formattedName += "-"

    # Some specific pokemon have characters that do not abide by UTF-8. As a result, it is necessary to hard
    # code them in otherwise the name that gets passed on for web scraping is some nonsense that points to
    # a webpage that does not exist. Gotta love Python
    if "xe2x99x80" in formattedName:
        formattedName = "Nidoran-f"
    elif "xe2x99x82" in formattedName:
        formattedName = "Nidoran-m"
    elif "xc3xa9bxc3xa9" in formattedName:
        formattedName = "Flabebe"

    # Appending the name of the pokemon to the respective list. Mega if they have different forms,
    # or names for their base forms
    if "small" in strPokemon:
        startingIndex = strPokemon.index("muted\">") + 7
        endingIndex = strPokemon[startingIndex:].index("<")

        if formattedName not in pokemon_names:
            pokemon_names.append(formattedName)

        formattedName += " " + strPokemon[startingIndex:startingIndex + endingIndex]
        pokemon_names_with_megas.append(formattedName)
    else:
        pokemon_names.append(formattedName)

# Calling the printingInfo function to retrieve the pokedex numbers of each entry
info = printingInfo(pokemon_names)

# Printing just for the sake of debugging. WILL BE REMOvED IN THE FINAL PRODUCT
#print(info)
