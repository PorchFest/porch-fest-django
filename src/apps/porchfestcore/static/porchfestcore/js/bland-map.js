function setVhUnit(){
	const vh = window.innerHeight * 0.01;
	document.documentElement.style.setProperty('--vh', `${vh}px`)
}
setVhUnit()
window.addEventListener('resize', setVhUnit)
class PorchMap{
	constructor(){
		this.markers 		= []
		this.center 		= [36.765, -119.805]
		this.map 			= L.map("map", {
			attributionControl: false,
			zoomControl: false
		}).setView(this.center, 14)
	}
	async init(){
		L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
			attribution: '© Mapbox © OpenStreetMap',
			maxZoom: 20,
			id: 'mapbox/streets-v11',
			tileSize: 512,
			zoomOffset: -1,
			accessToken: MAPBOX_PUBLIC_KEY
		}).addTo(this.map)
		this.buildMarkers()
	}
	async buildMarkers(data){
		try{
			const response = await axios.get("/api/porches/porch-map")
			const porches = response.data
			porches.features.forEach(porch=>{
				const [lon, lat] 	= porch.geometry.coordinates
				const marker 		= L.marker([lat, lon], {
					icon: L.icon({
                        iconUrl: "/static/porchfestcore/images/glyph.svg",
                        className: "porch-marker",
                        iconSize: [40, 40],
                        iconAnchor:	[10, 40],
                    })
				}).addTo(this.map)
				this.markers.push(marker)
			})
		}catch(error){
			console.error("Error fetching porches:", error)
			return null
		}
	}
}
const map 	= new PorchMap()
map.init()