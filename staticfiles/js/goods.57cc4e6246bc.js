
var ourDiv = document.getElementById("our-div");
var para = document.getElementById("our-paragraph");


$(document).ready(function(){
    var maxField = length; //Input fields increment limitation
    var addButton = $('.add_button'); //Add button selector
    var wrapper = $('#our-div'); //Input field wrapper
    var fieldHTML = '<div class="row"><div class="col"><label for="exampleDataList" class="form-label">Raw material 1:</label><input class="form-control" list="datalistOptions" id="exampleDataList" type="text" name="raw_material0"><datalist id="datalistOptions">{% for an_item in items %}<option value="{{ an_item.name }}">{% endfor %}</datalist><br></div><div class="col"><label for="validationCustom05">Required Amount 1</label><input type="number" class="form-control" id="validationCustom05" name="required_amount0" min="1" required></div></div>'; //New input field html 
    var x = 0; //Initial field counter is 1
    
    //Once add button is clicked
    $(addButton).click(function(){
        //Check maximum number of input fields
        if(x < maxField){ 
            x++; //Increment field counter
            $(wrapper).append(fieldHTML); //Add field html
        }
    });
    
    //Once remove button is clicked
    $(wrapper).on('click', '.remove_button', function(e){
        e.preventDefault();
        $(this).parent('div').remove(); //Remove field html
        x--; //Decrement field counter
    });
});