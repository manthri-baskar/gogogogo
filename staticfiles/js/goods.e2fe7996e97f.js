var ourDiv = document.getElementById("our-div");
var newParagraph = document.createElement("p");
var copy = document.createTextNode("Hello, world!");

newParagraph.appendChild( copy ); 
ourDiv.appendChild( newParagraph ); 

var foo = 5;
alert(foo); 