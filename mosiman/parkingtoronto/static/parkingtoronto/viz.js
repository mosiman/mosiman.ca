
$(document).ready(function() {
        
    var csrftoken = Cookies.get('csrftoken')
	var mymap = L.map('mapid').setView([43.653908, -79.384293], 13);
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		maxZoom: 18,
		id: 'mapbox.streets',
		accessToken: 'pk.eyJ1IjoibW9zaW1hbiIsImEiOiJjam4xNmdyZXIxZ3VtM3FybzM4dXRiOHM5In0.Yh0CQpkMw1PYQNDTSN2XpQ'
	}).addTo(mymap); 

    var active_polygon;
	var popup = L.popup()


    function generateStats(data){
        document.getElementById("streetinfo").innerHTML = data.name
    }

	function onMapClick(e){
		// This is going to be the workhorse function, probably.
		popup.setLatLng(e.latlng).setContent("Loading data for coordinates " + e.latlng.toString()).openOn(mymap)
        console.log($("#Url").attr("data-url"))
        $.ajax({
            url: $("#Url").attr("data-url"), 
			headers: {
				"X-CSRFToken" : Cookies.get('csrftoken')
			},
            data: {lat: e.latlng.lat, lng: e.latlng.lng},
            type: 'POST',
            success: function(data) {
                console.log(data.bbox)
                console.log(data.outstring)
                console.log(data.infs)
                //console.log(data.infnodes)

                if (data.found){
                    console.log("found!")
                    generateStats(data)
                    popup.setLatLng(e.latlng).setContent(data.name).openOn(mymap)
                    if (active_polygon){
                        mymap.removeLayer(active_polygon)
                    }
                    active_polygon = new L.polygon([
                                [data.bbox[0], data.bbox[2]],
                                [data.bbox[0], data.bbox[3]],
                                [data.bbox[1], data.bbox[3]],
                                [data.bbox[1], data.bbox[2]]]).addTo(mymap);

                    // calculate some statistics
                    // total_infractions = data.infnodes.length
                    // mean_fine = data.infnodes.map(function(x){return x.fine}).reduce(function(total,x){ return total + x}) / total_infractions
                    // console.log("total infractions: ")
                    // console.log(total_infractions)
                    // console.log("mean fine:")
                    // console.log(mean_fine)
                } else {
                    popup.setLatLng(e.latlng).setContent("No parking tickets found for this location!").openOn(mymap)


                }
            },
            fail: function(xhr, textStatus, errorThrown){
                       alert('request failed');
                    }
        })

	}

	mymap.on('click', onMapClick);

	$("#ajaxButton").click( function() {
		console.log("clickeddd")
		console.log(csrftoken)
        $.ajax({
            url: $("#Url").attr("data-url"), 
			headers: {
				"X-CSRFToken" : csrftoken
			},
            data: {somenum: 8},
            type: 'POST',
            success: function(data) {
                console.log(data.result)
            }})
	})


})
