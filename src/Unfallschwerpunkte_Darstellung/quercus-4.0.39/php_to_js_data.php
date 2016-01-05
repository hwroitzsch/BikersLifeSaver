
<?php
        $servername = "localhost";
        $username = "telematik";
        $password = "12345";
        $dbname = "accidentspots";

        // Create connection
        $conn = mysqli_connect($servername, $username, $password, $dbname);
        // Check connection
        if (!$conn) {
                die("Connection failed: " . mysqli_connect_error());
        }

        $sql = "SELECT NodeId, Latitude, Longitude FROM accident_spots";
        $result = mysqli_query($conn, $sql);
?>

var nodeId = new Array();
var latitude = new Array();
var longitude = new Array();
//var accidentSpots = new Array();
<?php
        if (mysqli_num_rows($result) > 0) {
                // output data of each row
                while($row = mysqli_fetch_assoc($result)) { ?>
                        //accidentSpots.push('<?php echo $row["NodeId"]; ?>':{center:{lat: '<?php echo $row["Latitude"]; ?>', l$
                        nodeId.push(<?php echo $row["NodeId"]; ?>);
                        latitude.push(<?php echo $row["Latitude"]; ?>);
                        longitude.push(<?php echo $row["Longitude"]; ?>);
                <?php }
        } else {
                echo "0 results";
        }
?>
<?php
        mysqli_close($conn);
?>

function initialize() {
        var mapZoom = 8;
        var circlesDrawn = false;
        var mapCanvas = document.getElementById('map');
        var mapOptions = {
          center: new google.maps.LatLng(52.454336, 13.441086),
          zoom: mapZoom,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        }
        var map = new google.maps.Map(mapCanvas, mapOptions)
        // Construct the circle for each value in citymap.
        // Note: We scale the area of the circle based on the population.
        addMarker(map);
        drawCircle(map);
        // Listener: auskommentieren, wenn spaeter benoetigt wird
        // google.maps.event.addListener(map, 'zoom_changed', function() {
                // var zoomLevel = map.getZoom();
								// if(!circlesDrawn && zoomLevel>15){
                        // drawCircle(map,zoomLevel);
                        // circlesDrawn = true;
                // }
        // });
}
google.maps.event.addDomListener(window, 'load', initialize);


function drawCircle(map) {
        var accidentSpotsCircle;
        var cirleRadius = 20;
        for (var id in nodeId) {
                // zeichne die Unfallschwerpunkte als Kreise
                accidentSpotsCircle = new google.maps.Circle({
                  strokeColor: '#FF0000',
                  strokeOpacity: 0.00001,
                  strokeWeight: 0,
                  fillColor: '#FF0000',
                  fillOpacity: 0.35,
                  map: map,
                  center: {lat: latitude[id], lng: longitude[id]},
                  radius: cirleRadius
                });
        }
}
function addMarker(map) {
                var iconBase = 'images/';
                var marker;
        for (var id in nodeId) {
                  marker = new google.maps.Marker({
                  position: {lat: latitude[id], lng: longitude[id]},
                  map: map,
                  icon: iconBase + 'maroon_flag32.png'
                });
        }
}

function myFunction() {
        nodeId.toString();
        latitude.toString();
        longitude.toString();
        document.getElementById("nodeId").innerHTML = nodeId;
        document.getElementById("latitude").innerHTML = latitude;
        document.getElementById("longitude").innerHTML = longitude;
        // accidentSpots.toString();
        // document.getElementById("nodeId").innerHTML = accidentSpots;
}
