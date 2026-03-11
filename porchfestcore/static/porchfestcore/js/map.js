class PorchMap{
	constructor(){
		this.map 		= null
		this.markers 	= null
		this.center 	= [36.7639, -119.8]
	}
	async init(){
		this.markers = []
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
		this.markers.forEach(marker=>{
			this.map.removeLayer(marker)
		})
		this.markers = []
		try{
			const response = await axios.get("/api/porches/porches", {
				params: data
			})
			const porches = response.data
			porches.features.forEach(porch=>{
				const [lon, lat] = porch.geometry.coordinates
				const marker = L.marker([lat, lon]).addTo(this.map)
				this.markers.push(marker)
			})
		}catch(error){
			console.error("Error fetching porches:", error)
			return null
		}
	}
}
const map 	= new PorchMap()
const form 	= document.getElementById("map_filter")
map.init()
form.addEventListener("submit", (e)=>{
	e.preventDefault()
	const formData 	= new FormData(form)
	const values 	= Object.fromEntries(formData.entries())
	map.buildMarkers(values)
})
function setVhUnit(){
	const vh = window.innerHeight * 0.01;
	document.documentElement.style.setProperty('--vh', `${vh}px`)
}
setVhUnit()
window.addEventListener('resize', setVhUnit)