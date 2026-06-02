const input = document.getElementById("id_neighbors_hosting")
input.addEventListener("change", function() {
    console.log(input.checked)
})

const form = document.getElementById("porch_signup_form")

form.addEventListener("submit", function(event) {
    if (!input.checked) {
        const confirm_no_neighbors = confirm("You indicated that you do not have neighbors hosting nearby. Are you sure this is correct?")
        if (!confirm_no_neighbors) {
            event.preventDefault()
        }
    }
})