var cnode = document.querySelector("canvas");
function r(cnode){
    if (cnode && cnode.nodeName !== 'BODY'){
    var cparent = cnode.parentNode;
    var children = cparent.childNodes;
    for (var i=0;i<children.length;i++){
         if(children[i] !== cnode && children[i].nodeName !=='SCRIPT' && typeof(children[i]) !== 'undefined'){
            console.log(children[i]);
         	cparent.removeChild(children[i]);
         }
    }
    r(cparent);
    }
}
for(var n=0;n<5;n++){
   r(cnode);
}
