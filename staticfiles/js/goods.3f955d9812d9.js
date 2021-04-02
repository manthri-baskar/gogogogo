
var ourDiv = document.getElementById("our-div");
var para = document.getElementById("our-paragraph");
document.getElementById("demo").addEventListener("click", myFunction);
len=0
function myFunction() {
    var div1 = document.createElement("div"); 
    div1.id=len
    var delLink = '<div style="text-align:right;margin-right:65px"><a href="javascript:delIt('+ ct +')">Del</a></div>';
    div1.innerHTML = document.getElementById('newlinktpl').innerHTML + delLink;
    document.getElementById('newlink').appendChild(div1);
    div1.appendChild(div1); 
    ourDiv.insertBefore( div1, para ); 
}
function delIt(eleId)
{
	d = document;
	var ele = d.getElementById(eleId);
	var parentEle = d.getElementById('newlink');
	parentEle.removeChild(ele);
}
