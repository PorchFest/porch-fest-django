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
		this.trolleyMarkers	= []
		this.center 		= [36.765, -119.805]
		this.userLocation	= {}
		this.map 			= L.map("map", {
			attributionControl: false,
			zoomControl: false
		}).setView(this.center, 14)
		this.activeMarker 	= null
		this.locationButton = document.getElementById("use_location")
		this.trolleyPath	= L.polyline([
			{lat: 36.76499756442535, 	lng: -119.79898676073246},
			{lat: 36.76493481691089, 	lng: -119.7989826567562},
			{lat: 36.76495642400253, 	lng: -119.79634088202028},
			{lat: 36.76508606642457, 	lng: -119.79633491954776},
			{lat: 36.76505957380197, 	lng: -119.79898258411826},
			{lat: 36.76499756442535, 	lng: -119.79898676073246},
			{lat: 36.76497392052814, 	lng: -119.8010560470801},
			{lat: 36.757276833053425, 	lng: -119.80104330058255},
			{lat: 36.75695599895826, 	lng: -119.80094172815676},
			{lat: 36.75673524935291, 	lng: -119.80074325330153},
			{lat: 36.75653040063636, 	lng: -119.80046655600141},
			{lat: 36.7562301419388, 	lng: -119.800289096131},
			{lat: 36.7504125518585, 	lng: -119.80036587536627},
			{lat: 36.75039926645446, 	lng: -119.80285847982687},
			{lat: 36.75063812285461, 	lng: -119.80283660334874},
			{lat: 36.75765247439101, 	lng: -119.802858812864},
			{lat: 36.7576463078158, 	lng: -119.80575299684742},
			{lat: 36.762494940188596, 	lng: -119.80578027260596},
			{lat: 36.762494940188596, 	lng: -119.805935},
			{lat: 36.76498, 			lng: -119.805935},
			{lat: 36.76498, 			lng: -119.80410004432838},
			{lat: 36.76853348956645, lng: -119.80413},
			{lat: 36.76853348956645, lng: -119.80413},
			{lat: 36.768675246218805, lng: -119.80405},
			{lat: 36.7722, lng: -119.80401},
			{lat: 36.7722, lng: -119.80107},
			{lat: 36.76497392052814, 	lng: -119.8010560470801},
		], {
			color: "#FFA500",
			opacity: 0.7,
			weight: 12
		})
		this.trolleyStops 	= [
			[36.76519733738659, 	-119.7974],
			[36.76221, 				-119.80114888041491],
			[36.75842471932054, 	-119.80113762653039],
			[36.7504997822508, 		-119.80067302535736],
			[36.75480596956797, 	-119.80275868274168],
			[36.75772922560339, 	-119.80542965887803],
			[36.762581303241724, 	-119.80579212689115],
			[36.768639382450395, 	-119.80397571187719],
			[36.772133403462355, 	-119.80129489426042],
		]
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
		this.locationButton.addEventListener("click", ()=>{
			this.getUserLocation()
		})
		this.trolleyMarkers = this.trolleyStops.map(stop=>{
			const marker 		= L.marker(stop, {
				icon: L.icon({
					iconUrl: "/static/porchfestcore/images/glyph-bus.svg",
					className: "porch-marker",
					iconSize: [40, 40],
					iconAnchor:	[10, 40],
				})
			}).addTo(this.map)
			return marker
		})
	}
	async buildMarkers(data){
		this.markers.forEach(marker=>{
			this.map.removeLayer(marker)
		})
		if(data){
			if(data.show_bus){
				this.trolleyPath.addTo(this.map)
			}else{
				this.map.removeLayer(this.trolleyPath)
			}
		}
		this.markers = []
		try{
			const response = await axios.get("/api/porch-map", {
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
			Alpine.store("ui").filteredCount = response.data.count
			porches.features.forEach(porch=>{
				const [lon, lat] 	= porch.geometry.coordinates
				let iconObj = {
					iconUrl: "/static/porchfestcore/images/glyph.svg",
					className: "porch-marker",
					iconSize: [40, 40],
					iconAnchor:	[10, 40],
				}
				if(porch.properties.porta_potty){
					iconObj.iconUrl = "/static/porchfestcore/images/glyph-porta.svg"
					iconObj.iconSize = [30, 30]
					iconAnchor: [0, 30]
				}
				// else if(porch.properties.vendor){
				// 	iconObj.iconUrl = "/static/porchfestcore/images/glyph-vendor.svg"
				// }
				else if(porch.properties.parking){
					iconObj.iconUrl = "/static/porchfestcore/images/glyph-parking.svg"
				}else if(porch.properties.drinking_water){
					iconObj.iconUrl = "/static/porchfestcore/images/glyph-drinking-water.png"
				}else if(porch.properties.bicycle_repair){
					iconObj.iconUrl = "/static/porchfestcore/images/glyph-bike-repair.png"
				}else if(porch.properties.info_booth){
					iconObj.iconUrl = "/static/porchfestcore/images/glyph-info.svg"
				}else if(porch.properties.after_party){
					iconObj.iconUrl = "/static/porchfestcore/images/glyph-after-party.png"
				}
				// else if(porch.properties.childrens_activities){
				// 	console.log("hahahahahaha")
				// }
				else if(porch.properties.sponsor_logo || porch.properties.sponsored){
					// if(porch.properties.sponsor_logo){
					// 	iconObj.iconUrl = porch.properties.sponsor_logo
					// }
					// // else if(porch.properties.vendor){
					// // 	iconObj.iconUrl = "/static/porchfestcore/images/glyph-vendor-sponsor.svg"
					// // }
					// else{
					// }
					iconObj.iconUrl = "/static/porchfestcore/images/glyph-sponsor.svg"
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
	async getUserLocation(){
		if(navigator.geolocation){
			try{
				const position = await new Promise((resolve, reject)=>{
					navigator.geolocation.getCurrentPosition(resolve, reject)
				})
				this.userLocation = position.coords
				const marker = L.marker([this.userLocation.latitude, this.userLocation.longitude], {
					icon: L.icon({
						iconUrl: "/static/porchfestcore/images/person.svg",
						className: "porch-marker",
						iconSize: [30, 60],
						iconAnchor:	[15, 60],
					})
				}).addTo(this.map)
				this.map.panTo([this.userLocation.latitude, this.userLocation.longitude])
			}catch(error){
				console.error("Error getting location: ", error)
			}
		}else{
			console.error("Geolocation not supported")
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

			this.$watch('$store.porch.open', isOpen=>{
				if(this.isPopping) return

				if(isOpen){
					if(history.state && history.state.modal){
						history.replaceState({modal: 'porch'}, '')
					}else{
						history.pushState({modal: 'porch'}, '')
					}
				}
			})

			this.$watch('$store.ui.showItinerary', isOpen=>{
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