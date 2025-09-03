console.log("call porches")

document.getElementById("call_porch_form").addEventListener("submit", function(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        }
    })
    .then(response => response.json())
    .then(data => {
        const msgDiv = document.getElementById("form-message");
        if(data.success){
            msgDiv.textContent = data.message;
            form.reset();
        } else {
			const errors = JSON.parse(data.errors)
			let html = '<ul>'
			for(const error in errors){
				if(errors.hasOwnProperty(error)){
					console.log(errors[error])
					errors[error].map(msg=>{
						console.log(msg.message)
						html += `<li>${msg.message}</li>`
					})
				}
			}
			html += '</ul>'
			msgDiv.innerHTML = html
            // msgDiv.textContent = data.errors || "Something went wrong.";
        }
    })
    .catch(() => {
        document.getElementById("form-message").textContent = "Network error.";
    });
});
