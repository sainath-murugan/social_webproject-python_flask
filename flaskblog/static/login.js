const inputs = document.querySelectorAll(".input");

function addcl(){
        let parent = this.parentNode.parentNode;
        parent.classList.add("focus")
}

function remcl(){
        let parent = this.parentNode.parentNode;
        if(this.value == ""){
            parent.classList.remove("focus")
        }
}
inputs.forEach(inputs => {
        input.addEventLister("focus", addcl);
        input.addEventLister("blur", remcl);
})