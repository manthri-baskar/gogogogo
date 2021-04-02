
document.getElementById("moreFields").addEventListener("click", moreFields);

var counter = 1;


function moreFields() {
	counter++;
	var newFields = document.getElementById('repeat').cloneNode(true);
    newFields.id = '';
	newFields.style.display = 'block';
	var newField = newFields.childNodes;
    var RawMat=document.getElementById('raw')
    RawMat.name=String('raw_material')+String(counter)
    var ReqAmt=document.getElementById('req')
    ReqAmt.name=String('required_amount')+String(counter)

    var Place_hold1=document.getElementById('raw')
    Place_hold1.placeholder=String('Raw Material ')+String(counter)
    
	/*for (var i=0;i<newField.length;i++) {
		var theName = newField[i].placeholder
		if (theName)
			newField[i].placeholder = theName + counter;
	}*/

    
    var insertHere = document.getElementById('writeroot');
    insertHere.parentNode.insertBefore(newFields,insertHere);
}