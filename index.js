
// Need to add 898 buttons to the pokedex

// Will have to make it so that it will iterate over the number of lines in the file, as the number of pokemon changes with each 
// generation

let rows = (898 - 898 % 3) / 3;
console.log(rows);
let counter = 1;

for (let i = 0; i < rows+1; i++){
    var row = document.createElement("tr");
    for (let j = 0; j < 3; j++){
        var cell = document.createElement("td");
        var button = document.createElement("button");
        var text = document.createTextNode(counter);
        if (counter < 899){
            button.appendChild(text);
            cell.appendChild(button);
            row.appendChild(cell);
        }
        counter += 1;
    }

    var table = document.getElementById("pokedexEntries")
    table.appendChild(row);
}