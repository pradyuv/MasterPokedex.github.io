import pyperclip as pc 

with open('C:\\Users\\meeky\\Desktop\\Website\\Pokedex Web Scraper\\Scripts\\masterpokedex.txt', encoding="utf8") as f:
    lines = f.readlines()
    firstGenCounter = 151 * 13
    pokemonList = []
    for i in range(len(lines)):
        if (i - 1) % 13 == 0 and i < firstGenCounter:
            pokemonList.append(lines[i][:len(lines[i]) - 1])


    for pokemon in pokemonList:
        pc.copy("https://img.pokemondb.net/artwork/" + pokemon.lower() + ".jpg")
        text = pc.paste()
        print (text)
        inputUser = input("Please press anything when you are ready to continue")
