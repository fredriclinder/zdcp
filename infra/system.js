// Tools created using javascript
//
// Version: 17.11.17GA
// Author:  Zacharias El Banna
// 

//
// Button functions - accepts proper JScript object:
//  Set attribute log=true to log operation
//
// - [load]   div url [spin=true/div] [msg = for confirmation] [frm = if doing a post]
// - redirect url
// - iload    iframe url
// - logout   url/div
// - toggle   div
// - hide     div
// - single   div select
// - empty    div
// - submit   frm
//

function btn(event) {
 var op  = $(this).attr("op");
 var div = $("#"+$(this).attr("div"));
 var url = $(this).attr("url");
 var log = $(this).attr("log");

 if (log)
  console.log("Log OP:"+op);

 if (!op || op == 'load') {
  var msg  = this.getAttribute("msg");
  if (msg && !confirm(msg)) return;
  var spin = this.getAttribute("spin");
  if (spin){
    if(spin == 'true')
     spin = div;
    else
     spin = $("#"+spin);
    spin.scrollTop(0);
    spin.css("overflow-y","hidden");
    spin.append("<DIV CLASS='overlay'><DIV CLASS='loader'></DIV></DIV>");
  }
  var frm  = this.getAttribute("frm");
  if(frm)
   $.post(url, $("#"+frm).serializeArray() , function(result) { 
    div.html(result); 
    if(spin){
     $(".overlay").remove();
     spin.css("overflow-y","auto");
    }
   });
  else
   div.load(url, function(responseTxt, statusTxt, xhr){
    if (spin) {
     $(".overlay").remove();
     spin.css("overflow-y","auto");
    }
   });
 } else if (op == 'redirect') {
  location.replace(url);
 } else if (op == 'submit') {
  $("#"+ this.getAttribute("frm")).submit();
 } else if (op == 'iload') {
  $("#"+ this.getAttribute("iframe")).attr('src',url);
 } else if (op == 'logout') {
  var cookies = document.cookie.split(";");
  for(var i=0; i < cookies.length; i++) {
   var equals = cookies[i].indexOf("=");
   var name = equals > -1 ? cookies[i].substr(0, equals) : cookies[i];
   document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
  }
  if(url)
   location.replace(url);
  else
   div.html('')
 } else if (op == 'single') {
  $(this.getAttribute("selector")).hide();
  div.show();
 } else if (op == 'toggle') {
  div.toggle();
 } else if (op == 'hide') {
  div.hide();
 } else if (op == 'empty') {
  div.html('');
 }
};

//
//
function focus(event){
 if (event.originalEvent.type == 'focus')
  $(this).addClass('highlight');
 else if (event.originalEvent.type == 'blur')
  $(this).removeClass('highlight');
};

//
// Drag-n'-drop
// - updating a list of element id's on attribute "dest" on drop element
//
function dragndrop(){
 $("li.drag").off();
 $("ul.drop").off();
 $("li.drag").attr("draggable","true");
 $("li.drag").on("dragstart", dragstart);
 $("ul.drop").on("dragover", dragover);
 $("ul.drop").on("drop", drop);
 $("ul.drop").on("dragenter", dragenter);
 $("ul.drop").on("dragleave", dragleave);
}

//
function dragstart(event){
 console.log("Drag " + this.id + " FROM " + this.parentElement.id);
 this.style.opacity = '0.4';
 event.originalEvent.dataTransfer.setData("Text",this.id);
 event.originalEvent.dataTransfer.effectAllowed = 'move';
}

//
function dragover(event){
 if(event.preventDefault)
  event.preventDefault();
 return false;
}
function dragenter(event){ this.classList.add('highlight'); }
function dragleave(event){ this.classList.remove('highlight'); }

//
function drop(event){
 event.preventDefault();
 var el_id = event.originalEvent.dataTransfer.getData("Text");
 var el    = document.getElementById(el_id);
 var parent= el.parentElement;
 el.style.opacity = '';
 this.appendChild(el);
 console.log("Drop " + el_id + " INTO " + this.id + " FROM " + parent.id);
 updatelist(this);
 updatelist(parent);
 this.classList.remove('highlight');
}

//
function updatelist(obj){
 var list = [];
 for (i = 0; i < obj.children.length; i++){ list.push(obj.children[i].id); }
 $("#" + obj.getAttribute("dest")).attr("value",list);
}
