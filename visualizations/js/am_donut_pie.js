am5.ready(function() {

// Create root element
// https://www.amcharts.com/docs/v5/getting-started/#Root_element
var root = am5.Root.new("am_donut");

// Set themes
// https://www.amcharts.com/docs/v5/concepts/themes/
root.setThemes([
  am5themes_Animated.new(root)
]);

// Create chart
// https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/
var chart = root.container.children.push(am5percent.PieChart.new(root, {
  radius: am5.percent(90),
  innerRadius: am5.percent(50),
  layout: root.horizontalLayout
}));

// Create series
// https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Series
var series = chart.series.push(am5percent.PieSeries.new(root, {
  name: "Series",
  valueField: "collisions",
  categoryField: "type_of_vehicle"
}));

// Set data
// https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Setting_data
series.data.setAll([ {"type_of_vehicle":"Sedan","collisions": 927335},
  {"type_of_vehicle":"Station Wagon/Sport Utility Vehicle","collisions": 554798},
  {"type_of_vehicle":"Taxi","collisions": 77508},
  {"type_of_vehicle":"Others","collisions": 57504},
  {"type_of_vehicle":"Pick-Up Truck","collisions": 41219},
  {"type_of_vehicle":"Van","collisions": 33313},
  {"type_of_vehicle":"Bus","collisions": 31303},
  {"type_of_vehicle":"Box Truck","collisions": 20645},
  {"type_of_vehicle":"Large Com Vehicle(6 Or More Tires","collisions": 	14397},
  {"type_of_vehicle":"Small Com Vehicle(4 Tires","collisions":  	13216},
  {"type_of_vehicle":"Bike","collisions": 11094},
  {"type_of_vehicle":"Livery Vehicle","collisions": 10481},
  {"type_of_vehicle":"Motorcycle","collisions": 10375},
  {"type_of_vehicle":"Tractor Truck Diesel","collisions": 8766},
  {"type_of_vehicle":"Ambulance","collisions": 5530},
  {"type_of_vehicle":"Convertible","collisions": 3263}]);

// Disabling labels and ticks
series.labels.template.set("visible", false);
series.ticks.template.set("visible", false);

// Adding gradients
series.slices.template.set("strokeOpacity", 0);
series.slices.template.set("fillGradient", am5.RadialGradient.new(root, {
  stops: [{
    brighten: -0.8
  }, {
    brighten: -0.8
  }, {
    brighten: -0.5
  }, {
    brighten: 0
  }, {
    brighten: -0.5
  }]
}));

// Create legend
// https://www.amcharts.com/docs/v5/charts/percent-charts/legend-percent-series/
var legend = chart.children.push(am5.Legend.new(root, {
  centerY: am5.percent(50),
  y: am5.percent(50),
  marginTop: 15,
  marginBottom: 15,
  layout: root.verticalLayout
}));

legend.data.setAll(series.dataItems);


// Play initial series animation
// https://www.amcharts.com/docs/v5/concepts/animations/#Animation_of_series
series.appear(1000, 100);

}); // end am5.ready()