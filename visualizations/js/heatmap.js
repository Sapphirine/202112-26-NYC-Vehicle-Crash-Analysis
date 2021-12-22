var map, heatmap;

var heatmap_data = []
var heatmap_brooklyn_data = []
var heatmap_bronx_data = []
var heatmap_queens_data = []
var heatmap_staten_data = []

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 10.5,
    center: { lat: 40.754932, lng: 	-73.984016 },
    mapTypeId: "hybrid",
  });
  heatmap = new google.maps.visualization.HeatmapLayer({
    data: getPoints(),
    map: map,
  });
    map_brooklyn = new google.maps.Map(document.getElementById("map_brooklyn"), {
    zoom: 11,
    center: { lat: 40.650002, lng: 	-73.949997 },
    mapTypeId: "hybrid",
  });
  heatmap_brooklyn = new google.maps.visualization.HeatmapLayer({
    data: getPoints_brooklyn(),
    map: map_brooklyn,
  });
    map_bronx = new google.maps.Map(document.getElementById("map_bronx"), {
    zoom: 11,
    center: { lat: 40.837048, lng: 	-73.865433 },
    mapTypeId: "hybrid",
  });
  heatmap_bronx = new google.maps.visualization.HeatmapLayer({
    data: getPoints_bronx(),
    map: map_bronx,
  });
  map_queens = new google.maps.Map(document.getElementById("map_queens"), {
    zoom: 11,
    center: { lat: 40.742054, lng: 	-73.769417},
    mapTypeId: "hybrid",
  });
  heatmap_queens = new google.maps.visualization.HeatmapLayer({
    data: getPoints_queens(),
    map: map_queens,
  });
  map_staten = new google.maps.Map(document.getElementById("map_staten"), {
    zoom: 11,
    center: { lat:  40.579021, lng: 	-74.151535 },
    mapTypeId: "hybrid",
  });
  heatmap_staten = new google.maps.visualization.HeatmapLayer({
    data: getPoints_staten(),
    map: map_staten,
  });
  document
    .getElementById("toggle-heatmap")
    .addEventListener("click", toggleHeatmap);
  document
    .getElementById("change-gradient")
    .addEventListener("click", changeGradient);
  document
    .getElementById("change-opacity")
    .addEventListener("click", changeOpacity);
  document
    .getElementById("change-radius")
    .addEventListener("click", changeRadius);
}

function toggleHeatmap() {
  heatmap.setMap(heatmap.getMap() ? null : map);
  heatmap_brooklyn.setMap(heatmap_brooklyn.getMap() ? null : map_brooklyn);
  heatmap_bronx.setMap(heatmap_bronx.getMap() ? null : map_bronx);
  heatmap_queens.setMap(heatmap_queens.getMap() ? null : map_queens);
  heatmap_staten.setMap(heatmap_staten.getMap() ? null : map_staten);
}

function changeGradient() {
  const gradient = [
    "rgba(0, 255, 255, 0)",
    "rgba(0, 255, 255, 1)",
    "rgba(0, 191, 255, 1)",
    "rgba(0, 127, 255, 1)",
    "rgba(0, 63, 255, 1)",
    "rgba(0, 0, 255, 1)",
    "rgba(0, 0, 223, 1)",
    "rgba(0, 0, 191, 1)",
    "rgba(0, 0, 159, 1)",
    "rgba(0, 0, 127, 1)",
    "rgba(63, 0, 91, 1)",
    "rgba(127, 0, 63, 1)",
    "rgba(191, 0, 31, 1)",
    "rgba(255, 0, 0, 1)",
  ];

  heatmap.set("gradient", heatmap.get("gradient") ? null : gradient);
  heatmap_brooklyn.set("gradient", heatmap_brooklyn.get("gradient") ? null : gradient);
  heatmap_bronx.set("gradient", heatmap_bronx.get("gradient") ? null : gradient);
  heatmap_queens.set("gradient", heatmap_queens.get("gradient") ? null : gradient);
  heatmap_staten.set("gradient", heatmap_staten.get("gradient") ? null : gradient);
}

function changeRadius() {
  heatmap.set("radius", heatmap.get("radius") ? null : 20);
  heatmap_brooklyn.set("radius", heatmap_brooklyn.get("radius") ? null : 20);
  heatmap_bronx.set("radius", heatmap_bronx.get("radius") ? null : 20);
  heatmap_queens.set("radius", heatmap_queens.get("radius") ? null : 20);
  heatmap_staten.set("radius", heatmap_staten.get("radius") ? null : 20);
}

function changeOpacity() {
  heatmap.set("opacity", heatmap.get("opacity") ? null : 0.2);
  heatmap_brooklyn.set("opacity", heatmap_brooklyn.get("opacity") ? null : 0.2);
  heatmap_bronx.set("opacity", heatmap_bronx.get("opacity") ? null : 0.2);
  heatmap_queens.set("opacity", heatmap_queens.get("opacity") ? null : 0.2);
  heatmap_staten.set("opacity", heatmap_staten.get("opacity") ? null : 0.2);
}

function load() {
	var mydata = JSON.parse(data);
    console.log(mydata[0]['location_latitude'])
    mydata.forEach((x, i) => heatmap_data.push(new google.maps.LatLng(x['location_latitude'],x['location_longitude'])));

    var brooklyn_data = JSON.parse(data_brooklyn);
    brooklyn_data.forEach((x, i) => heatmap_brooklyn_data.push(new google.maps.LatLng(x['location_latitude'],x['location_longitude'])));

    var bronx_data = JSON.parse(data_bronx);
    bronx_data.forEach((x, i) => heatmap_bronx_data.push(new google.maps.LatLng(x['location_latitude'],x['location_longitude'])));

    var queens_data = JSON.parse(data_queens);
    queens_data.forEach((x, i) => heatmap_queens_data.push(new google.maps.LatLng(x['location_latitude'],x['location_longitude'])));

    var staten_data = JSON.parse(data_staten);
    staten_data.forEach((x, i) => heatmap_staten_data.push(new google.maps.LatLng(x['location_latitude'],x['location_longitude'])));

}

// Heatmap data: 500 Points
function getPoints() {
  return heatmap_data

}

function getPoints_brooklyn() {
  return heatmap_brooklyn_data

}

function getPoints_bronx() {
  return heatmap_bronx_data

}

function getPoints_queens() {
  return heatmap_queens_data

}

function getPoints_staten() {
  return heatmap_staten_data

}
