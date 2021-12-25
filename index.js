// We know that there will be 3 pokemon per row in the table, so we need to have an appropriate number of rows
// In the future, 898 will be replaced with the number of lines in the txt file (which we will do in an upcoming commit) and this is
// so that in future generations when more pokemon are added, we can account for the new ones instead of having to manually change the number
let rows = (898 - 898 % 3) / 3;

// Keeping track of what pokedex number we are on
let counter = 1;

// Looping through the table, and adding the table rows and table data elements accordingly
for (let i = 0; i < rows+1; i++){
    var row = document.createElement("tr");
    for (let j = 0; j < 3; j++){
        var cell = document.createElement("td");
        // Adding a button with the counter as its inner text to simulate the pokedex entries (will be replaced with image of the sprite)
        var button = document.createElement("button");
        var text = document.createTextNode(counter);
        button.id = counter;
        // Setting the on click functionality of the button. If a user clicks a specific button, it is the same as them selecting a
        // specific pokemon to learn more about. Only makes sense for us to display the information the user might be looking for.
        button.onclick = function(){
            document.getElementById("pokedexEntries").style.display = "none";
            document.getElementById("searchbar").style.display = "none";

            let pokedexDiv = document.getElementById("pokedex");

            // Creating a back button to allow the user to get back to the general pokedex screen
            var backButton = document.createElement("button");
            var backButtonText = document.createTextNode("Back");
            backButton.id = "back";

            // Adding the functionality for the back button, allows the user to go between the specific Pokemon's pokedex entry and the
            // general pokedex
            backButton.onclick = function(){
                document.getElementById("back").remove();
                document.getElementById("pokedexEntries").style.display = "table";
                document.getElementById("searchbar").style.display = "input";
            }

            // Adding all the elements to the webpage for the users to see
            backButton.appendChild(backButtonText);
            pokedexDiv.appendChild(backButton);
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

// This function is here so that users can search up specific pokemon. For the time being, you can only search up by pokedex number,
// but we hope to allow users to search up via the name of the Pokemon.
function search(){
    let input = document.getElementById("searchbar").value;
    let pokedex = document.getElementById("pokedexEntries");

    for (let i = 0; i < pokedex.rows.length; i++){
        let data = pokedex.rows.item(i).cells;

        for (let j = 0; j < data.length; j++){
            if (data[j].innerHTML.includes(input) == false){
                // If the current cell does not contain the pokedex number the user is searching, its display is set to none, making it invisible
                data[j].style.display = "none";
            } else {
                // If the current cell does contain the pokedex number, its visibility is set to table-cell, mimicking a <td> element
                data[j].style.display = "table-cell";
            }
        }
    }
}
