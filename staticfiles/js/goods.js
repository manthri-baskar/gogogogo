
document.getElementById("moreFields").addEventListener("click", moreFields);

var counter = 0;


function moreFields() {
	counter++;
	var newFields = document.getElementById('repeat').cloneNode(true);
    newFields.id = '';
	newFields.style.display = 'block';
	var newField = newFields.childNodes;
    var RawMat=document.getElementById('raw')
    
	/*for (var i=0;i<newField.length;i++) {
		var theName = newField[i].placeholder
		if (theName)
			newField[i].placeholder = theName + counter;
	}*/

    
    var insertHere = document.getElementById('writeroot');
    insertHere.parentNode.insertBefore(newFields,insertHere);
}