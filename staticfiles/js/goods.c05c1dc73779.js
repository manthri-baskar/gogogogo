
var ourDiv = document.getElementById("our-div");
var para = document.getElementById("our-paragraph");
var wrapper = $('.repeat');
var fieldHTML = '<div class="col"><label for="exampleDataList" class="form-label">Raw material 1:</label><input class="form-control" list="datalistOptions" id="exampleDataList" type="text" name="raw_material0"><datalist id="datalistOptions">{% for an_item in items %}<option value="{{ an_item.name }}">{% endfor %}</datalist><br></div>';
document.getElementById("demo").addEventListener("click", myFunction);

function myFunction() {

    $(wrapper).append(fieldHTML);

}
