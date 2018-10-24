
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
    var polyline;
	var popup = L.popup()



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
                console.log(data.nodes)
                console.log(data.explambda)
                //console.log(data.infnodes)

                if (data.found){
                    console.log("found!")
                    popup.setLatLng(e.latlng).setContent(data.name).openOn(mymap)
                    document.getElementById("streetName").innerHTML = data.name
                    if (active_polygon){
                        mymap.removeLayer(active_polygon)
                    }
                    if (polyline){
                        mymap.removeLayer(polyline)
                    }
                    
                    // active_polygon = new L.polygon([
                    //             [data.bbox[0], data.bbox[2]],
                    //             [data.bbox[0], data.bbox[3]],
                    //             [data.bbox[1], data.bbox[3]],
                    //             [data.bbox[1], data.bbox[2]]]).addTo(mymap);

                    latlngs = data.nodes.map(x => [x.lat, x.lon])
                    polyline = new L.polyline(latlngs, {color: 'blue'}).addTo(mymap);
                    mymap.fitBounds(polyline.getBounds());

                    generateStats(data);

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

    function generateStats(data){
        infs = data.infs
        // Get tickethours
        var tickethours = infs.map(x => moment(x.datetime).get("Hour"))
        Plotly.newPlot("hourlyhist", [{
            x: tickethours, 
            type: 'histogram',
            autobinx: false,
            xbins: {
                start: 0,
                end: 25
            }}],
            {
                title: 'Tickets by hour',
                xaxis: { title: 'Hour',
                    range: [0,23]},
                yaxis: { title: 'Number of tickets' }
            })

        // get interarrivals
        
        if (data.numtickets > 100){
            // assuming more than one ticket, surely lambda > 0...
            sorted_dt = infs.map( x => moment(x.datetime))
            sorted_dt.sort(function(a,b){ return a-b })

            interarrivals = []

            for (let i = 0, size = sorted_dt.length - 1; i < size; i++){
                // divide for minutes
                timedelta = (sorted_dt[i+1] - sorted_dt[i]) / 60000
                if (timedelta > 15){
                    interarrivals.push(Math.floor(timedelta))
                }
            }

            expplot = preplot_exp(data.explambda, 0, Math.floor(Math.max.apply(Math, interarrivals)))
            console.log(expplot)

            interarrival_trace = {
                x: interarrivals,
                type: 'histogram',
            }
            expo_trace = {
                x: expplot[0],
                y: expplot[1],
                mode: 'lines'
            }
            Plotly.newPlot("interarrivalhist", [interarrival_trace],
                {
                    title: "Interarrival times",
                    xaxis: { title: 'Minutes' },
                    yaxis: { title: 'Frequency' }
                }
            )

            Plotly.newPlot("interarrivalboxplot", [{
                y: interarrivals,
                boxpoints: 'all', 
                jitter: 0.5,
                pointpos: -2,
                type: 'box' }],
                {
                    title: "Interarrival time boxplot"
                }
            )
        }


    }

	// thanks https://gist.github.com/joates/6584908
	function linspace(a,b,n) {
		if(typeof n === "undefined") n = Math.max(Math.round(b-a)+1,1);
		if(n<2) { return n===1?[a]:[]; }
		var i,ret = Array(n);
		n--;
		for(i=n;i>=0;i--) { ret[i] = (i*b+(n-i)*a)/n; }
        return ret;
    } 

    function preplot_exp(explambda, start,end){
        // make it a logspace
        xs = linspace(start,end,5000)
        xs = xs.map(x => Math.pow(Math.E, x))
        ys = xs.map(x => explambda * Math.pow(Math.E, -1 * explambda * x))
        return [xs, ys]
    }



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
