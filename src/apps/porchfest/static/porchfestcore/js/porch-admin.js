$(document).on('googleMapPointFieldWidget:placeChanged', function(e, placeObj, lat, lng, wrapElemSelector, djangoInput){
	let streetAddress 											= ""
	placeObj.address_components.forEach(component=>{
		if(component.types.includes("street_number")){
			streetAddress 										+= component.long_name
			streetAddress 										+= " "
		}else if(component.types.includes("route")){
			streetAddress 										+= component.long_name
		}else if(component.types.includes("locality")){
			document.getElementById("id_city").value			= component.long_name
		}else if(component.types.includes("administrative_area_level_1")){
			document.getElementById("id_state").value			= component.long_name
		}else if(component.types.includes("country")){
			document.getElementById("id_country").value			= component.long_name
		}else if(component.types.includes("postal_code")){
			document.getElementById("id_zip_code").value		= component.long_name
		}
	})
	document.getElementById("id_street_address").value 			= streetAddress
})