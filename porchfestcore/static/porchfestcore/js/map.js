function setVhUnit(){
	const vh = window.innerHeight * 0.01;
	document.documentElement.style.setProperty('--vh', `${vh}px`)
}
setVhUnit()
window.addEventListener('resize', setVhUnit)

class PorchMap{
	constructor(){
		this.map = null
		this.markers = null
		this.center = [36.7639, -119.8]
	}

	async init(){
		this.buildMap()
		this.buildMarkers()
	}

	buildMap(){
		this.map = L.map("map", {
			attributionControl: false,
			zoomControl: false
		}).setView(this.center, 16)

		L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(this.map)
	}

	async buildMarkers(data){
		try{
			const response = await axios.get("/api/porches/porches", {
				params: data
			})
			console.log("Porches fetched successfully:", response.data)
			// return response.data
			const porches = response.data
			porches.features.forEach(porch=>{
				console.log(porch)
				const [lon, lat] = porch.geometry.coordinates
				const marker = L.marker([lat, lon]).addTo(this.map)
			})
		}catch(error){
			console.error("Error fetching porches:", error)
			return null
		}
	}
}

const map = new PorchMap()
map.init()



const form = document.getElementById("map_filter")



form.addEventListener("submit", (e)=>{
	e.preventDefault()
	console.log("Form submitted")
	const formData = new FormData(form)
	const values = Object.fromEntries(formData.entries())
	getPorches(values)
})

async function getPorches(data){
	try{
		const response = await axios.get("/api/porches/porches", {
			params: data
		})
		console.log("Porches fetched successfully:", response.data)
	}catch(error){
		console.error("Error fetching porches:", error)
	}
}
