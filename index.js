// We know that there will be 3 pokemon per row in the table, so we need to have an appropriate number of rows
// In the future, 898 will be replaced with the number of lines in the txt file (which we will do in an upcoming commit) and this is
// so that in future generations when more pokemon are added, we can account for the new ones instead of having to manually change the number
let rows = (898 - 898 % 3) / 3;

// Keeping track of what pokedex number we are on
let counter = 1;

// Will need to change the file path here
const filePath = "masterpokedex.txt";
let fileContents;

// Composition of the dictionary will be as follows:
// "name": [pokedex number, [typing], mass, height, [evolutionary info], img src, description, abilities, [stats], total stats, region]
let pokemonDict = {};

// A list that contains the name of all Pokemon, this is so that setting the id of each button is easier
let pokemonNames = [];

function loadFile(){
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", filePath, false);
    xmlhttp.send();

    if (xmlhttp.status == 200){
        fileContents = xmlhttp.responseText;

        // We know that each entry is separated by the "δ" character
        let pokedexEntries = fileContents.split("δ");

        // Will have to process the elements here
        pokedexEntries.forEach(element => {
            let individualEntries = element.split("\n");

            if (individualEntries[1] == "Bulbasaur"){
                let pokedexNumber = individualEntries[0];
                let typing = individualEntries[2];
                let weight = individualEntries[3];
                let height = individualEntries[4];
                let evolutionaryInfo = individualEntries[5];
                let imageSrc = individualEntries[6];
                let description = individualEntries[8];
                let abilities = individualEntries[10];
                let baseStats = individualEntries[11];
                let totalStats = individualEntries[9];
                let region = individualEntries[12];
                let pokemonSprite = individualEntries[7];

                pokemonDict[individualEntries[1]] = [pokedexNumber, typing, weight, height, evolutionaryInfo, imageSrc, description, abilities, baseStats, totalStats, region, pokemonSprite];
                let pokemonName = individualEntries[1];
                pokemonNames.push(pokemonName);
            } else {
                let pokedexNumber = individualEntries[1];
                let typing = individualEntries[3];
                let weight = individualEntries[4];
                let height = individualEntries[5];
                let evolutionaryInfo = individualEntries[6];
                let imageSrc = individualEntries[7];
                let description = individualEntries[9];
                let abilities = individualEntries[11];
                let baseStats = individualEntries[12];
                let totalStats = individualEntries[10];
                let region = individualEntries[13];
                let pokemonSprite = individualEntries[8];

                pokemonDict[individualEntries[2]] = [pokedexNumber, typing, weight, height, evolutionaryInfo, imageSrc, description, abilities, baseStats, totalStats, region, pokemonSprite];
                let pokemonName = individualEntries[2];
                pokemonNames.push(pokemonName);
            }
        });

    }
}

// Looping through the table, and adding the table rows and table data elements accordingly
function loadTable(){
    // Retrieving the data from the file
    loadFile();
    for (let i = 0; i < rows+1; i++){
        var row = document.createElement("tr");
        for (let j = 0; j < 3; j++){
            var cell = document.createElement("td");
            // Adding a button with the counter as its inner text to simulate the pokedex entries (will be replaced with image of the sprite)
            var button = document.createElement("button");
            var text = document.createTextNode(pokemonNames[counter - 1]);
            var spritePokemon = document.createElement("img");
            spritePokemon.src = pokemonDict[pokemonNames[counter - 1]][11];
            button.appendChild(spritePokemon);
            button.id = pokemonNames[counter - 1];
            

            // Setting the on click functionality of the button. If a user clicks a specific button, it is the same as them selecting a
            // specific pokemon to learn more about. Only makes sense for us to display the information the user might be looking for.
            button.onclick = function(){
                document.getElementById("pokedexEntries").style.display = "none";
                document.getElementById("searchbar").style.display = "none";

                // Creating a back button to allow the user to get back to the general pokedex screen
                var backButton = document.getElementById("back");

                // Adding the functionality for the back button, allows the user to go between the specific Pokemon's pokedex entry and the
                // general pokedex
                backButton.onclick = function(){
                    document.getElementById("back").style.display = "none";
                    document.getElementById("specific_pokemon").style.display = "none";
                    document.getElementById("pokedexEntries").style.display = "table";
                    document.getElementById("searchbar").style.display = "block";
                }

                // Adding all the elements to the webpage for the users to see
                document.getElementById("specific_pokemon").style.display = "block";
                document.getElementById("back").style.display = "block";

                // Adding the necessary information to the screen
                document.getElementById("pokedex-number-name").innerHTML = pokemonDict[this.id][0] + ". " + this.id;

                // Setting the sprite for the pokemon
                //let imageSrc = pokemonDict[this.id][5].slice(1, pokemonDict[this.id][5].length - 1);
                document.getElementById("spriteImage").src = "Images/" + this.id + ".png";

                // Setting the description for the pokemon
                document.getElementById("description").innerHTML = pokemonDict[this.id][6];

                // Setting the typing for the pokemon
                let typing = getTyping(pokemonDict[this.id][1]);

                // Means there is only one type
                if (typeof typing === 'string'){
                    document.getElementById("typing").innerHTML = typing;
                // Means there are two types
                } else {
                    // Will need to edit this later, add IDs and everything to make the typing look a lot nicer
                    document.getElementById("typing").innerHTML = typing[0] + " " + typing[1];
                }

                // Using the same function as above as they are formatted the same way in the txt file. Why rebuild the wheel?
                let abilities = getTyping(pokemonDict[this.id][7]);

                // Means there is only one ability
                if (typeof abilities === 'string'){
                    document.getElementById("abilities").innerHTML = abilities;
                // Means there are two or more abilities
                } else {
                    // Will need to edit this later, add IDs and everything to make the typing look a lot nicer
                    document.getElementById("abilities").innerHTML = abilities[0] + ", " + abilities[1];
                }

                // EVOLUTIONARY INFO WILL BE PUT ON PAUSE FOR THE TIME BEING

                // Getting the region it was introduced in
                let regionIntroduced = getRegion(pokemonDict[this.id][10]);
                document.getElementById("region-introduced").innerHTML = regionIntroduced;

                // Assigning the height and weight of the pokemon
                document.getElementById("height").innerHTML = pokemonDict[this.id][3];
                document.getElementById("weight").innerHTML = pokemonDict[this.id][2];

                // The current pokemon's base stat for each stat
                let stats = getStats(pokemonDict[this.id][8]);

                var hp = stats[0];
                var attack = stats[1];
                var defense = stats[2];
                var specialattack = stats[3];
                var specialdefense = stats[4];
                var speed = stats[5];

                // The max base stat for any pokemon
                const max = 255;

                var hpColour = assignColour((hp / max) * 100);
                var attackColour = assignColour((attack / max) * 100);
                var defenseColour = assignColour((defense / max) * 100);
                var specialAttackColour = assignColour((specialattack / max) * 100);
                var specialDefenseColour = assignColour((specialdefense / max) * 100);
                var speedColour = assignColour((speed / max) * 100);

                // Calculating the percentage of the bar that must be filled in
                var healthpercentage = (hp / max) * 100 + "%";
                var attackpercentage = (attack / max) * 100 + "%";
                var defensepercentage = (defense / max) * 100 + "%";
                var specialattackpercentage = (specialattack / max) * 100 + "%";
                var specialdefensepercentage = (specialdefense / max) * 100 + "%";
                var speedpercentage = (speed / max) * 100 + "%";

                // Setting the size of the div and colour of the bar accordingly
                document.getElementById("health-bar-diagram").style.width = healthpercentage;
                document.getElementById("health-bar-diagram").style.backgroundColor = hpColour;

                document.getElementById("attack-bar-diagram").style.width = attackpercentage;
                document.getElementById("attack-bar-diagram").style.backgroundColor = attackColour;

                document.getElementById("defense-bar-diagram").style.width = defensepercentage;
                document.getElementById("defense-bar-diagram").style.backgroundColor = defenseColour;

                document.getElementById("special-attack-bar-diagram").style.width = specialattackpercentage;
                document.getElementById("special-attack-bar-diagram").style.backgroundColor = specialAttackColour;

                document.getElementById("special-defense-bar-diagram").style.width = specialdefensepercentage;
                document.getElementById("special-defense-bar-diagram").style.backgroundColor = specialDefenseColour;

                document.getElementById("speed-bar-diagram").style.width = speedpercentage;
                document.getElementById("speed-bar-diagram").style.backgroundColor = speedColour;
            };
            // Ensuring that buttons that are more than necessary are not displayed on screen.
            if (counter < 899){
                button.appendChild(text);
                cell.appendChild(button);
                row.appendChild(cell);
            }
            counter += 1;
        }

        // Adding the row with all the elements to the table
        var table = document.getElementById("pokedexEntries")
        table.appendChild(row);
    }

}

// This function is here so that users can search up specific pokemon. For the time being, you can only search up by pokedex number,
    // but we hope to allow users to search up via the name of the Pokemon.
    function search(){
        let input = document.getElementById("searchbar").value.toLowerCase();
        let pokedex = document.getElementById("pokedexEntries");

        for (let i = 0; i < pokedex.rows.length; i++){
            let data = pokedex.rows.item(i).cells;

            for (let j = 0; j < data.length; j++){
                if (data[j].innerHTML.toLowerCase().includes(input) == false){
                    // If the current cell does not contain the pokedex number the user is searching, its display is set to none, making it invisible
                    data[j].style.display = "none";
                } else {
                    // If the current cell does contain the pokedex number, its visibility is set to table-cell, mimicking a <td> element
                    data[j].style.display = "table-cell";
                }
            }
        }
    }

function assignColour(percentage){
    // Returning the colour based on what percentage the stat is relative to the max base stat. Will need to change some of the weightings
    // as the colours don't match up. Using the Pokemondb colours for reference.
    if (percentage <= 10){
        return "rgba(243, 68, 68, 255)";
    } else if (percentage > 10 && percentage <= 24){
        return "rgba(255, 127, 15, 255)";
    } else if (percentage > 24 && percentage <= 39){
        return "rgba(255, 221, 87, 255)";
    } else if (percentage > 39 && percentage <= 54){
        return "rgba(160, 229, 21, 255)";
    } else if (percentage > 50 && percentage <= 55){
        return "rgba(35, 205, 94, 255)";
    } else {
        return "rgba(0, 194, 184, 255)";
    }
}


function getStats(listOfStats){
    // This function will take a list made up of the stats along with some additional text and will filter out the unnecessary pieces
    // of information so that we're left with the numbers
    let splitList = listOfStats.split(" ");

    // Would use a traditional for loop, but "Special Attack" and "Special Defense" messes everything up and doesn't allow for clean splitting 
    // on the space character
    let hp = parseInt(splitList[1]);
    let attack = parseInt(splitList[3]);
    let defense = parseInt(splitList[5]);
    let specialAttack = parseInt(splitList[8]);
    let specialDefense = parseInt(splitList[11]);
    let speed = parseInt(splitList[13]);

    // Returning a list with all the processed stats 
    return [hp, attack, defense, specialAttack, specialDefense, speed];
}

// Getting the typing of the pokemon (same method is used to get the abiltiies of the pokemon as they are formatted the same in the txt file)
function getTyping(typeString){
    // This means the Pokemon has two types
    if (typeString.includes(",")){
        let listOfTypes = typeString.split(",");
        let firstType = listOfTypes[0].slice(2, listOfTypes[0].length - 1);
        let secondType = listOfTypes[1].slice(2, listOfTypes[1].length - 2);
        return [firstType, secondType];
    } else {
        return typeString.slice(2, typeString.length - 2);
    }
}

// Getting the region the pokemon was introduced in
function getRegion(regionString){
    let splitRegionString = regionString.split(", ");
    return splitRegionString[1].slice(1, splitRegionString[1].length - 2);
}