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
		this.markers 		= []
		this.center 		= [36.765, -119.805]
		this.map 			= L.map("map", {
			attributionControl: false,
			zoomControl: false
		}).setView(this.center, 14)
		this.activeMarker 	= null
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
		this.markers.forEach(marker=>{
			this.map.removeLayer(marker)
		})
		this.markers = []
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
				const [lon, lat] 	= porch.geometry.coordinates
				let iconObj = {
					iconUrl: "/static/porchfestcore/images/glyph.svg",
					className: "porch-marker",
					iconSize: [40, 40],
					iconAnchor:	[10, 40],
				}
				if(porch.properties.sponsor_logo){
					if(!porch.properties.vendor){
						iconObj.iconUrl = porch.properties.sponsor_logo
						iconObj.className = "sponsor-logo"
					}else{
						iconObj.iconUrl = "/static/porchfestcore/images/glyph-vendor-sponsor.svg"
					}
				}else if(porch.properties.porta_potty){
					iconObj.iconUrl = "/static/porchfestcore/images/glyph-porta.svg"
				}else if(porch.properties.vendor){
					iconObj.iconUrl = "/static/porchfestcore/images/glyph-vendor.svg"
				}else if(porch.properties.parking){
					iconObj.iconUrl = "/static/porchfestcore/images/glyph-parking.svg"
				}
				const marker 		= L.marker([lat, lon], {
					icon: L.icon(iconObj)
				}).addTo(this.map)
				if(porch.properties.slug === this.activePorch){
					this.setActiveMarker(marker)
					this.map.panTo([lat, lon])
				}
				marker.on("click", e=>{
					this.loadPorch(porch)
					this.setActiveMarker(marker)
					this.map.panTo([lat, lon])
				})
				this.markers.push(marker)
			})
		}catch(error){
			console.error("Error fetching porches:", error)
			return null
		}
	}
	setActiveMarker(marker){
		if(this.activeMarker){
			const activeIcon = this.activeMarker.options.icon
			activeIcon.options.iconSize = [40,40]
			activeIcon.options.iconAnchor = [10,40]
			this.activeMarker.setIcon(activeIcon)
		}
		const icon = marker.options.icon
		icon.options.iconSize = [60,60]
		icon.options.iconAnchor = [20,60]
		marker.setIcon(icon)
		this.activeMarker = marker
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
			this.isPopping = false

			window.addEventListener('popstate', event=>{
				this.isPopping = true

				if(!event.state || !event.state.modal){
					this.$store.porch.open = false
					this.$store.ui.showItinerary = false
				}else if(event.state.modal === 'itinerary'){
					this.$store.ui.showItinerary = true
					this.$store.porch.open = false
				}else if(event.state.modal === 'porch'){
					this.$store.porch.open = true
					this.$store.ui.showItinerary = false
				}

				this.$nextTick(()=>this.isPopping = false)
			})

			this.$watch('$store.porch.open', (isOpen)=>{
				if(this.isPopping) return

				if(isOpen){
					if(history.state && history.state.modal){
						history.replaceState({modal: 'porch'}, '')
					}else{
						history.pushState({modal: 'porch'}, '')
					}
				}
			})

			this.$watch('$store.ui.showItinerary', (isOpen)=>{
				if(this.isPopping) return

				if(isOpen){
					if(history.state && history.state.modal){
						history.replaceState({modal: 'itinerary'}, '')
					}else{
						history.pushState({modal: 'itinerary'}, '')
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