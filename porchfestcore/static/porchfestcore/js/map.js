function setVhUnit(){
	const vh = window.innerHeight * 0.01;
	document.documentElement.style.setProperty('--vh', `${vh}px`)
}
setVhUnit()
window.addEventListener('resize', setVhUnit)

class PorchMap{
	constructor(){
		const queryParams 	= new URLSearchParams(window.location.search)
		this.activePorch 	= queryParams.get("porch") || null
		this.map 			= null
		this.markers 		= null
		this.activeMarker 	= null
		this.center 		= [36.765, -119.805]
		this.icon 			= L.icon({
			iconUrl: "/static/porchfestcore/images/glyph.svg",
			className: "porch-marker",
			iconAnchor:	[15, 40],
		})
		this.activeIcon 	= L.icon({
			iconUrl: "/static/porchfestcore/images/glyph-active.svg",
			className: "porch-marker active",
			iconAnchor:	[15, 40],
		})
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
		}).setView(this.center, 14)
		L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
			attribution: '© Mapbox © OpenStreetMap',
			maxZoom: 20,
			id: 'mapbox/streets-v11',
			tileSize: 512,
			zoomOffset: -1,
			accessToken: MAPBOX_PUBLIC_KEY
		}).addTo(this.map)
	}
	async buildMarkers(data){
		this.markers.forEach(marker=>{
			this.map.removeLayer(marker)
		})
		this.markers = []
		console.log(this.activePorch)
		try{
			const response = await axios.get("/api/porches/porch-map", {
				params: data,
				paramsSerializer: params=>{
					const searchParams = new URLSearchParams()
					Object.entries(params).forEach(([key, value])=>{
						if(Array.isArray(value)){
							value.forEach(v=>searchParams.append(key, v))
						}else if(value !== undefined && value !== null){
							searchParams.append(key, value)
						}
					})
					return searchParams.toString()
				}
			})
			const porches = response.data
			porches.features.forEach(porch=>{
				// console.log(porch)
				const [lon, lat] 	= porch.geometry.coordinates
				let icon 			= this.icon
				if(porch.properties.slug === this.activePorch){
					icon = this.activeIcon
					this.map.panTo([lat, lon])
				}
				if(porch.properties.sponsor_logo){
					if(!porch.properties.vendor){
						icon 		= L.icon({
							iconUrl: porch.properties.sponsor_logo,
							className: "sponsor-logo",
							iconAnchor:	[15, 40],
						})
					}else{
						icon 		= L.icon({
							iconUrl: "/static/porchfestcore/images/glyph-vendor-sponsor.svg",
							className: "porch-marker",
							iconAnchor:	[15, 40],
						})
					}
				}else if(porch.properties.porta_potty){
					icon 			= L.icon({
						iconUrl: "/static/porchfestcore/images/glyph-porta.svg",
						className: "porch-marker",
						iconAnchor:	[15, 40],
					})
				}else if(porch.properties.vendor){
					icon 			= L.icon({
						iconUrl: "/static/porchfestcore/images/glyph-vendor.svg",
						className: "porch-marker",
						iconAnchor:	[15, 40],
					})
				}else if(porch.properties.parking){
					icon 			= L.icon({
						iconUrl: "/static/porchfestcore/images/glyph-parking.svg",
						className: "porch-marker",
						iconAnchor:	[15, 40],
					})
				}
				// console.log(icon)
				const marker 		= L.marker([lat, lon], {
					icon
				}).addTo(this.map)
				marker.on("click", e=>{
					this.loadPorch(porch)
					// if(this.activeMarker){
					// 	this.activeMarker.setIcon(this.icon)
					// }
					// if(!porch.properties.sponsor_logo){	
					// 	marker.setIcon(this.activeIcon)
					// 	this.activeMarker = marker
					// }
					this.map.panTo([lat, lon])
				})
				this.markers.push(marker)
			})
		}catch(error){
			console.error("Error fetching porches:", error)
			return null
		}
	}
	async loadPorch(porch){
		try{
			const response = await axios.get(`/porches/${porch.properties.slug}`, {
				headers: {
					"HX-Request": "true"
				},
				params: {
					performances: porch.properties.performances.join(",")
				}
			})
			Alpine.store("porch").content 	= response.data
			Alpine.store("porch").open 		= true
		}
		catch(error){
			console.error("Error loading porch:", error)
		}
	}
}

document.addEventListener("alpine:init", ()=>{
	Alpine.store("porch", {
		open: false,
		content: ""
	})
})

const map 	= new PorchMap()
const form 	= document.getElementById("map_filter")
map.init()

function updateResults(close=false){
	if(close){
		Alpine.store("ui", {
			showFilter: false,
		})
	}
	const formData 	= new FormData(form)
	const values = {
		...Object.fromEntries(formData.entries()),
		genres: formData.getAll("genres")
	}
	if(values.now_time){
		const time = new Date().toLocaleTimeString([], {
			hour: '2-digit',
			minute: '2-digit',
			hour12: false
		})
		values.after = time
	}
	if(values.sponsored)values.sponsored 	= true
	if(values.vendor)values.vendor			= true
	map.buildMarkers(values)
}

function modalHistory(){
    return{
        init(){
			window.addEventListener('popstate', (event)=>{
				if(!event.state || !event.state.modal){
					this.$store.porch.open = false
					this.$store.ui.showItinerary = false
					return
				}
				if(event.state.modal === 'porch'){
					this.$store.porch.open = true
					this.$store.ui.showItinerary = false
				}
				if(event.state.modal === 'itinerary'){
					this.$store.porch.open = false
					this.$store.ui.showItinerary = true
				}
			})
			this.$watch('$store.porch.open', (isOpen)=>{
				if(isOpen){
					if(!history.state || history.state.modal !== 'porch'){
						history.pushState({modal: 'porch'}, '')
					}else{
						if(history.state && history.state.modal === 'porch'){
							history.back()
						}
					}
				}
			})
			this.$watch('$store.ui.showItinerary', (isOpen)=>{
				if(isOpen){
					if(!history.state || history.state.modal !== 'itinerary'){
						history.pushState({modal: 'itinerary'}, '')
					}else{
						if(history.state && history.state.modal === 'itinerary'){
							history.back()
						}
					}
				}
			})
		},
        closeModal(){
			if(this.$store.porch.open){
				this.$store.porch.open = false
			}
			if(this.$store.ui.showItinerary){
				this.$store.ui.showItinerary = false
			}
            if(history.state && history.state.modal){
                history.back()
            }
        }
    }
}