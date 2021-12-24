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