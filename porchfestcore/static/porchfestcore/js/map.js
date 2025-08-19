function setVhUnit(){
	const vh = window.innerHeight * 0.01;
	document.documentElement.style.setProperty('--vh', `${vh}px`)
}
setVhUnit()
window.addEventListener('resize', setVhUnit)

class EventsMap{
	constructor(){
		// this.mapContainer                       = document.getElementById("map")
		// this.apiUrl                             = "/api/venues-events"
		this.map                                = null
		this.center								= null
		this.latitude                          	= null
		this.longitude                         	= null
	}

	async init(){
		console.log("Loading...")
		try{
			const {latitude, longitude}         = await this.getUserLocation()
			this.buildMap(latitude, longitude)
			this.buildMarkers(latitude, longitude)
		}catch(error){
			console.log("Error", error.message)
		}finally{
			console.log("Loaded. This should not be here")
		}
	}

	async getUserLocation(){
		return new Promise((resolve, reject)=>{
			if(navigator.geolocation){
				navigator.geolocation.getCurrentPosition(
					position=>resolve(position.coords),
					error=>reject(error)
				)
			}else{
				reject(new Error("Geolocation is not supported by this browser."))
			}
		})
	}

	buildMap(lat, lng){
		console.log(lat, lng)
		this.map = L.map("map").setView([lat, lng], 13)
		L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
			maxZoom: 19,
			attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
		}).addTo(this.map)

		// document.getElementById("loading").style.display = "none"
		// document.getElementById(this.mapContainerId).style.display = "block"
	}

	async buildMarkers(){
		// const markerDataFetch			= await fetch(`/api/nearby-venues?lat=${this.lat}&lon=${this.lon}&radius=5`)
		// const markerData				= await markerDataFetch.json()
		// console.log(markerData)
		// const customIcon = L.icon({
		// 	iconUrl: "https://cdn.theatlantic.com/thumbor/U1zpgym9tgu0xAY818RviLy6A3U=/1x0:1079x606/976x549/media/img/mt/2023/04/PegmanAnim_2/original.gif",  // Path to your custom icon
		// 	iconSize: [80, 80],  // Size of the icon [width, height]
		// 	iconAnchor: [19, 38],  // Point of the icon which will correspond to marker's location
		// 	popupAnchor: [0, -38], // Point from which the popup should open relative to the iconAnchor
		// 	// shadowUrl: '/path-to-your-shadow.png', // Optional: shadow image
		// 	// shadowSize: [50, 50],  // Size of the shadow
		// 	// shadowAnchor: [25, 50] // Anchor of the shadow
		// })

		const markers		= L.markerClusterGroup({
			spiderfyOnMaxZoom: true,
			zoomToBoundsOnClick: false,
		})
		for(let i = 0; i < 100; i++){
			const lat 		= 36.759 + (Math.random() - 0.5) * 0.1
			const lng 		= -119.80 + (Math.random() - 0.5) * 0.1
			const marker 	= L.marker([lat, lng], {})
			marker.bindPopup(`<b>Hello, World!</b><br>I am popup number ${i}.`)
			markers.addLayer(marker)
		}
		markers.on("clusterclick", e=>{
			console.log(e)
			const cluster = e.layer
			const childCount			= cluster.getChildCount()
			let popupContent			= ``

			cluster.getAllChildMarkers().forEach((marker, i)=>{
				popupContent			+= `Marker ${i + 1}: ${marker.getLatLng()}`
			})

			cluster.bindPopup(popupContent).openPopup()
		})
		this.map.addLayer(markers)

		
		// while(haveEvents){
		// 	// add events
		// }
	}

	async fetchMarkers(lat, lng){


		// try{
		// 	const response                       = await fetch()
		// 	if(!response.ok){
		// 		throw new Error("Fetch markers failed")
		// 	}

		// 	const venues                         = await response.json()
		// 	this.loadMarkers(venues)
		// }catch(e){
		// 	console.logerror("Error fetching markers: ", e)
		// }
	}


}
const map = new EventsMap()
map.init()