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
        // NEXT STEPS:
        // IMPLEMENT SEARCH FUNCTIONALITY, FOR THAT WILL PROBABLY NEED TO ADD ID WHICH IS EQUAL TO THE NAME OF THE POKEMON (WE WILL HAVE THIS
        // WITH THE FILE)
        var button = document.createElement("button");
        var text = document.createTextNode(counter);
        button.id = counter;
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