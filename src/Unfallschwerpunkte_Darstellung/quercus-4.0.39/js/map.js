
// adds a method called "has" to the array prototype, which checks if the array contains an item
Object.defineProperty(Array.prototype,'has', {
	value: function(o) {
		return this.indexOf(o) != -1;
	}
});

// MAP
var map;

// MAP LAYERS
var hospitals_layer;
var schools_layer;
var kindergarten_layer;

var layers;

var CITIES = ['Berlin','Potsdam'];

var AMINITIES = ['school', 'hospital', 'kindergarten'];

var AMINITIES_TO_LAYERS = {};
// has to be done when layers are not undefined anymore, because ohne undefined will be saved otherwise and not updated when the values for layers change (reference by value?)
/*AMINITIES_TO_LAYERS['school'] = schools_layer;
AMINITIES_TO_LAYERS['hospital'] = hospitals_layer;
AMINITIES_TO_LAYERS['kindergarten'] = kindergarten_layer;*/

var AMINITIES_TO_COLORS = {};
AMINITIES_TO_COLORS['school'] = 'blue';
AMINITIES_TO_COLORS['hospital'] = 'red';
AMINITIES_TO_COLORS['kindergarten'] = 'yellow';

var AMINITIES_TO_IMPORTANCES = {};
AMINITIES_TO_IMPORTANCES['school'] = 6.0;
AMINITIES_TO_IMPORTANCES['hospital'] = 16.0;
AMINITIES_TO_IMPORTANCES['kindergarten'] = 10.0;

var AMENITIES_TO_RADIUS = {};
AMENITIES_TO_RADIUS['school'] = 500; // 1km // 1000m
AMENITIES_TO_RADIUS['hospital'] = 1000;
AMENITIES_TO_RADIUS['kindergarten'] = 500;

var VIEW_CENTER_COORDINATES = [52.52, 13.41];
var INITIAL_VIEW_ZOOM = 12;

var MAPBOX_URL_TEMPLATE = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}';
var MAPBOX_MAP_ID = 'garrin.7c8d8963';
var MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiZ2FycmluIiwiYSI6IjFiMDMyNzk3Mzg3M2NmNGM2OWU4YTFkOGE5MTcwMzUwIn0.SHu3pvdrqFyronTC8wfw4w';

var ATTRIBUTION_HTML = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>';

var MAXIMUM_ZOOM = 18;
var MINIMUM_ZOOM = 8;

var TILE_SIZE = 256; // for mapbox it only works with 256px * 256px

//var MAP_BOUNDS_SOUTHWEST = L.latLng(52.44, 13.49);
//var MAP_BOUNDS_NORTHEAST = L.latLng(52.60, 13.33);
//var MAP_BOUNDS = L.latLngBounds(MAP_BOUNDS_SOUTHWEST, MAP_BOUNDS_NORTHEAST);

var MAP_OPTIONS = {
	attribution:	ATTRIBUTION_HTML,
	maxZoom:		MAXIMUM_ZOOM,
	minZoom: 		MINIMUM_ZOOM,
	id:				MAPBOX_MAP_ID,
	accessToken:	MAPBOX_ACCESS_TOKEN,
	tileSize:		TILE_SIZE,
	reuseTiles:		true, // does this create any problems?
	//bounds:			MAP_BOUNDS
}








$(document).ready(function() {
	// define some layers of the map
	hospitals_layer = L.layerGroup();
	schools_layer = L.layerGroup();
	kindergarten_layer = L.layerGroup();
	layers = [schools_layer, hospitals_layer, kindergarten_layer];
	
	AMINITIES_TO_LAYERS['school'] = schools_layer;
	AMINITIES_TO_LAYERS['hospital'] = hospitals_layer;
	AMINITIES_TO_LAYERS['kindergarten'] = kindergarten_layer;
		
	// initialize the map
	initializeMap(layers);
	
	// add data from OpenStreetMap
	add_json_map_data();

	// SETUP THE "CLEAR" FUNCTION
	// When you zoom in/out you want the json layer to get cleared
	// and repopulated with new (relevant) json data
	// this means you can have different data for each layer
	map.on("zoomend", function() {
		clear_all_layers();
	});

	// action listers for the buttons
	add_action_listeners();
});

function clear_all_layers() {
	// should I really clear map data?
}

function initializeMap(mylayers) {
	// create a map object and give it the coordinates of the location it shall show
	// we also pass map options as a second parameter to L.map(...)
	map = L.map('map', {
		zoomControl: true,
		layers: mylayers
	}).setView(
		VIEW_CENTER_COORDINATES,
		INITIAL_VIEW_ZOOM
	);

	// create a tile layer, which shows a default map and add it to the map
	L.tileLayer(MAPBOX_URL_TEMPLATE, MAP_OPTIONS).addTo(map);

	// sets the prefix for map attributions
	map.attributionControl.setPrefix("");
}


// action listers for the layer buttons
function add_action_listeners() {
	
}


// this function draws filled circles around POIs
function add_json_map_data() {
	//var city = 'Potsdam';
	
	// add all map data
	get_json_map_data().done(function(json_map_data) {
		console.log('SUCCESS');
		//console.log(json_map_data);
		
		// clear the existing layers
		$.each(layers, function(index, element){
			console.log('CLEARING LAYER ' + index);
			element.clearLayers();
		});
		
		draw_circles(json_map_data);
		
	}).fail(function(error) {
		//console.log(error);
		console.log('ERROR');
	
	}).always(function() {
		console.log('COMPLETE');
	});	
}

function draw_circles(json_map_data) {
	
	//console.log(json_map_data);
	//console.log('DRAW CIRCLES HAS BEGUN');
	
	$.each(json_map_data.elements, function(index, element) {
		
		console.log(element);
		//console.log('ITERATING OVER JSON MAP DATA');
		//console.log(element.tags.amenity + ' color: ' + AMINITIES_TO_COLORS[element.tags.amenity]);
		
		if(element.hasOwnProperty('tags')) {
			if(element.tags.hasOwnProperty('name')) {
				
				//console.log('BEFORE IF');
				//console.log('TAG.AMENITY = ' + element.tags.amenity);
				
				if(AMINITIES.has(element.tags.amenity)) { //self defined has method for arrays
					
					console.log('IN IF');
					
					L.circle([element.lat, element.lon], 1)
						.bindPopup(element.tags.name)
						.setStyle({
							stroke: false,
							fill: true,
							fillColor: AMINITIES_TO_COLORS[element.tags.amenity],
							fillOpacity: 0.01 * AMINITIES_TO_IMPORTANCES[element.tags.amenity]
						})
						.addTo(AMINITIES_TO_LAYERS[element.tags.amenity])
						.setRadius(AMENITIES_TO_RADIUS[element.tags.amenity]) // 500m
				}
			}
		}
	});
}


function get_json_map_data() {
	
	var map_bounds = map.getBounds();
	
	var cities_string = CITIES[0];
	for(var i = 1; i < CITIES.length; ++i) {
		cities_string += '|' + CITIES[i];
	}
	
	// ask for multiple amenities in one query
	var amenities_string = AMINITIES[0];
	for(var i = 1; i < AMINITIES.length; ++i) {
		amenities_string += '|' + AMINITIES[i];
	}
	
	var bounds = map.getBounds();
	var boundary =
		'(' + 
		bounds._southWest.lat + ',' +
		bounds._southWest.lng + ',' +
		bounds._northEast.lat + ',' +
		bounds._northEast.lng + 
		')';
	
	var url = 'https://www.overpass-api.de/api/interpreter?';
	var data = 
		'[out:json]' +
		'[timeout:600];' +
		
		'area' +
		//'	["boundary"~"administrative"]' +
		'	["boundary"~"' + 'administrative' + '"]' +
		'	["name"~"' + cities_string + '"];' +
		
		'node' +
		'	(area)' + 
		'	["amenity"~"' + amenities_string + '"];' +
		'out;';
	
	console.log(data);
	
	return $.ajax({
		url: url,
		dataType: 'json',
		data: {data: data},
		type: 'GET',
		async: true,
		crossDomain: true
	});
}
   