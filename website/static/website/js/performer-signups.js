document.addEventListener("htmx:afterSettle", e=>{
    const el = e.detail.target
    if(el.id === "performer_results"){
        if(el.childElementCount > 0){
            el.classList.add("open")
            el.addEventListener("animationend", ()=>{
                el.classList.remove("closed")
            },{once:true})
        }else{
            
        }
    }
})

document.addEventListener("htmx:beforeSwap", e=>{
    const el = e.detail.target
    if(el.id === "performer_results"){
        const hasResults = e.detail.serverResponse.trim() !== ""
        if(!hasResults && el.childElementCount > 0){
            console.log("Hero")
            e.detail.shouldSwap = false
            el.classList.add("closed")
            el.addEventListener("animationend", ()=>{
                console.log("NO?")
                el.innerHTML = ""
                el.classList.remove("open")
                el.classList.remove("closed")
            },{once:true})
        }
    }
})