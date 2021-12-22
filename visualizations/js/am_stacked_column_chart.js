am5.ready(function() {

// Create root element
// https://www.amcharts.com/docs/v5/getting-started/#Root_element
var root = am5.Root.new("am_clustered");


// Set themes
// https://www.amcharts.com/docs/v5/concepts/themes/
root.setThemes([
  am5themes_Animated.new(root)
]);


// Create chart
// https://www.amcharts.com/docs/v5/charts/xy-chart/
var chart = root.container.children.push(am5xy.XYChart.new(root, {
  panX: false,
  panY: false,
  wheelX: "panX",
  wheelY: "zoomX",
  layout: root.verticalLayout
}));

// Add scrollbar
// https://www.amcharts.com/docs/v5/charts/xy-chart/scrollbars/
chart.set("scrollbarX", am5.Scrollbar.new(root, {
  orientation: "horizontal"
}));

var data = [{"year": "2012", "number_of_pedestrians_injured": 5906,"number_of_pedestrians_killed":72,"number_of_cyclist_injured":2210, "number_of_cyclist_killed": 6, "number_of_motorist_injured": 19333,"number_of_motorist_killed":59},
{"year": "2013","number_of_pedestrians_injured": 11988,"number_of_pedestrians_killed":17,"number_of_cyclist_injured":	4075, "number_of_cyclist_killed": 11, "number_of_motorist_injured": 39060,"number_of_motorist_killed":110},
{"year": "2014","number_of_pedestrians_injured": 11036,"number_of_pedestrians_killed":13,"number_of_cyclist_injured":	4000, "number_of_cyclist_killed": 20, "number_of_motorist_injured": 36176,"number_of_motorist_killed":109},
{"year": "2015","number_of_pedestrians_injured": 10084,"number_of_pedestrians_killed":13,"number_of_cyclist_injured":	4281, "number_of_cyclist_killed": 15, "number_of_motorist_injured": 36992,"number_of_motorist_killed":95},
{"year": "2016","number_of_pedestrians_injured": 11090,"number_of_pedestrians_killed":14,"number_of_cyclist_injured":	4975, "number_of_cyclist_killed": 18, "number_of_motorist_injured": 44010,"number_of_motorist_killed":72},
{"year": "2017","number_of_pedestrians_injured": 11151,"number_of_pedestrians_killed":12,"number_of_cyclist_injured":	4889, "number_of_cyclist_killed": 27, "number_of_motorist_injured": 44616,"number_of_motorist_killed":107},
{"year": "2018","number_of_pedestrians_injured": 11124,"number_of_pedestrians_killed":12,"number_of_cyclist_injured":	4725, "number_of_cyclist_killed": 10, "number_of_motorist_injured": 46068,"number_of_motorist_killed":98},
{"year": "2019","number_of_pedestrians_injured": 10568,"number_of_pedestrians_killed":13,"number_of_cyclist_injured":	4986, "number_of_cyclist_killed": 31, "number_of_motorist_injured": 45834,"number_of_motorist_killed":82},
{"year": "2020","number_of_pedestrians_injured": 6689,"number_of_pedestrians_killed":10,"number_of_cyclist_injured":	5575, "number_of_cyclist_killed": 29, "number_of_motorist_injured": 32341,"number_of_motorist_killed":137},
{"year": "2021","number_of_pedestrians_injured": 6775,"number_of_pedestrians_killed":11,"number_of_cyclist_injured":	4662, "number_of_cyclist_killed": 16, "number_of_motorist_injured": 34724,"number_of_motorist_killed":118}]



// Create axes
// https://www.amcharts.com/docs/v5/charts/xy-chart/axes/
var xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {
  categoryField: "year",
  renderer: am5xy.AxisRendererX.new(root, {}),
  tooltip: am5.Tooltip.new(root, {})
}));

xAxis.data.setAll(data);

var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
  min: 0,
  max: 100,
  numberFormat: "#'%'",
  strictMinMax: true,
  calculateTotals: true,
  renderer: am5xy.AxisRendererY.new(root, {})
}));


// Add legend
// https://www.amcharts.com/docs/v5/charts/xy-chart/legend-xy-series/
var legend = chart.children.push(am5.Legend.new(root, {
  centerX: am5.p50,
  x: am5.p50
}));


// Add series
// https://www.amcharts.com/docs/v5/charts/xy-chart/series/
function makeSeries(name, fieldName) {
  var series = chart.series.push(am5xy.ColumnSeries.new(root, {
    name: name,
    stacked: true,
    xAxis: xAxis,
    yAxis: yAxis,
    valueYField: fieldName,
    valueYShow: "valueYTotalPercent",
    categoryXField: "year"
  }));

  series.columns.template.setAll({
    tooltipText: "{name}, {categoryX}:{valueYTotalPercent.formatNumber('#.#')}%",
    tooltipY: am5.percent(10)
  });
  series.data.setAll(data);

  // Make stuff animate on load
  // https://www.amcharts.com/docs/v5/concepts/animations/
  series.appear();

  series.bullets.push(function () {
    return am5.Bullet.new(root, {
      sprite: am5.Label.new(root, {
        text: "{valueYTotalPercent.formatNumber('#.#')}%",
        fill: root.interfaceColors.get("alternativeText"),
        centerY: am5.p50,
        centerX: am5.p50,
        populateText: true
      })
    });
  });

  legend.data.push(series);
}

makeSeries("Pedestrians injured", "number_of_pedestrians_injured");
makeSeries("Pedestrians killed", "number_of_pedestrians_killed");
makeSeries("Cyclist injured", "number_of_cyclist_injured");
makeSeries("Cyclist killed", "number_of_cyclist_killed");
makeSeries("Motorist injured", "number_of_motorist_injured");
makeSeries("Motorist killed", "number_of_motorist_killed");


// Make stuff animate on load
// https://www.amcharts.com/docs/v5/concepts/animations/
chart.appear(1000, 100);

});