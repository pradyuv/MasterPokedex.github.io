# Importing the necessary libraries for webscraping
import requests
import string
from bs4 import BeautifulSoup

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
        pokedexNumber = str(tempSoup.find("strong"))
        pokemonType = list(tempSoup.findAll("a", class_="type-icon"))
        evolutionConditionRaw = list((tempSoup.findAll("i", class_="icon-arrow")))
        evolutionCondition = []
        for e in evolutionConditionRaw:
            try:
                evolutionCondition.append(e.next_sibling.get_text())
            except AttributeError:
                try:
                    evolutionCondition.append(e.next_sibling.get_text())
                except AttributeError:
                    evolutionCondition.append(e.previous_sibling.get_text())
        evolution=[x for x in evolutionCondition if x is not None]
        thisPokemonType = []
        # Checks if a pokemon has a certain type and appends it to its own list
        for x in range(2):
            if "title" not in pokemonType[x]:
                for typeCheck in allTypes:
                    if typeCheck in pokemonType[x]:
                        thisPokemonType.append(typeCheck)

        wFinder = tempSoup.find("th", string="Weight")
        hFinder = tempSoup.find("th", string="Height")
        weight = wFinder.next_sibling.next_sibling
        height = hFinder.next_sibling.next_sibling
        # Apologies for the confusing variable names, this variable serves the same purpose as firstClosingBrace below,
        # but this time it's a local variable
        firstClosingBracket = pokedexNumber.index(">")
        # Same purpose as above, just trying to find the index
        secondOpeningBracket = pokedexNumber[firstClosingBracket + 1:].index("<")

        # Properly formatting the pokedex number so that it's easy to read when displayed on screen
        formattedPokedexNumber = pokedexNumber[firstClosingBracket + 1:firstClosingBracket + secondOpeningBracket + 1]

        # Appending the pokedex number and the name to the pokemon info list
        pokemonInfo.append([formattedPokedexNumber, name, thisPokemonType, weight, height, evolution])

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
print(info)
