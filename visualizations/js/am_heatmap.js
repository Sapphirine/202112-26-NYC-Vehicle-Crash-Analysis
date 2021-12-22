am5.ready(function() {

// Create root element
// https://www.amcharts.com/docs/v5/getting-started/#Root_element
var root = am5.Root.new("am_heatmap");


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
  wheelX: "none",
  wheelY: "none",
  layout: root.verticalLayout
}));


// Create axes and their renderers
var yRenderer = am5xy.AxisRendererY.new(root, {
  visible: false,
  minGridDistance: 20,
  inversed: true
});

yRenderer.grid.template.set("visible", false);

var yAxis = chart.yAxes.push(am5xy.CategoryAxis.new(root, {
  maxDeviation: 0,
  renderer: yRenderer,
  categoryField: "weekday"
}));

var xRenderer = am5xy.AxisRendererX.new(root, {
  visible: false,
  minGridDistance: 30,
  opposite:true
});

xRenderer.grid.template.set("visible", false);

var xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {
  renderer: xRenderer,
  categoryField: "hour"
}));


// Create series
// https://www.amcharts.com/docs/v5/charts/xy-chart/#Adding_series
var series = chart.series.push(am5xy.ColumnSeries.new(root, {
  calculateAggregates: true,
  stroke: am5.color(0xffffff),
  clustered: false,
  xAxis: xAxis,
  yAxis: yAxis,
  categoryXField: "hour",
  categoryYField: "weekday",
  valueField: "value"
}));

series.columns.template.setAll({
  tooltipText: "{value}",
  strokeOpacity: 1,
  strokeWidth: 2,
  width: am5.percent(100),
  height: am5.percent(100)
});

series.columns.template.events.on("pointerover", function(event) {
  var di = event.target.dataItem;
  if (di) {
    heatLegend.showValue(di.get("value", 0));
  }
});

series.events.on("datavalidated", function() {
  heatLegend.set("startValue", series.getPrivate("valueHigh"));
  heatLegend.set("endValue", series.getPrivate("valueLow"));
});


// Set up heat rules
// https://www.amcharts.com/docs/v5/concepts/settings/heat-rules/
series.set("heatRules", [{
  target: series.columns.template,
  min: am5.color(0xfffb77),
  max: am5.color(0xfe131a),
  dataField: "value",
  key: "fill"
}]);


// Add heat legend
// https://www.amcharts.com/docs/v5/concepts/legend/heat-legend/
var heatLegend = chart.bottomAxesContainer.children.push(am5.HeatLegend.new(root, {
  orientation: "horizontal",
  endColor: am5.color(0xfffb77),
  startColor: am5.color(0xfe131a)
}));


// Set data
// https://www.amcharts.com/docs/v5/charts/xy-chart/#Setting_data
var data = [{weekday: "Friday",	hour: "10am",	value: 14517},{weekday: "Friday",	hour: "10pm",	value: 10005},{weekday: "Friday",	hour: "11am",	value: 15149},{weekday: "Friday",	hour: "11pm",	value: 8940},{weekday: "Friday",	hour: "12am",	value: 8270},{weekday: "Friday",	hour: "12pm",	value: 16158},{weekday: "Friday",	hour: "1am",	value: 4026},{weekday: "Friday",	hour: "1pm",	value: 16877},{weekday: "Friday",	hour: "2am",	value: 2923},{weekday: "Friday",	hour: "2pm",	value: 20138},{weekday: "Friday",	hour: "3am",	value: 2293},{weekday: "Friday",	hour: "3pm",	value: 19192},{weekday: "Friday",	hour: "4am",	value: 2683},{weekday: "Friday",	hour: "4pm",	value: 21864},{weekday: "Friday",	hour: "5am",	value: 3369},{weekday: "Friday",	hour: "5pm",	value: 21762},{weekday: "Friday",	hour: "6am",	value: 6426},{weekday: "Friday",	hour: "6pm",	value: 18739},{weekday: "Friday",	hour: "7am",	value: 9163},{weekday: "Friday",	hour: "7pm",	value: 15440},{weekday: "Friday",	hour: "8am",	value: 17100},{weekday: "Friday",	hour: "8pm",	value: 12849},{weekday: "Friday",	hour: "9am",	value: 16522},{weekday: "Friday",	hour: "9pm",	value: 10630},{weekday: "Monday",	hour: "10am",	value: 14609},{weekday: "Monday",	hour: "10pm",	value: 6919},{weekday: "Monday",	hour: "11am",	value: 14705},{weekday: "Monday",	hour: "11pm",	value: 5466},{weekday: "Monday",	hour: "12am",	value: 7280},{weekday: "Monday",	hour: "12pm",	value: 14990},{weekday: "Monday",	hour: "1am",	value: 3456},{weekday: "Monday",	hour: "1pm",	value: 15564},{weekday: "Monday",	hour: "2am",	value: 2413},{weekday: "Monday",	hour: "2pm",	value: 17717},{weekday: "Monday",	hour: "3am",	value: 1969},{weekday: "Monday",	hour: "3pm",	value: 16949},{weekday: "Monday",	hour: "4am",	value: 2391},{weekday: "Monday",	hour: "4pm",	value: 20023},{weekday: "Monday",	hour: "5am",	value: 3276},{weekday: "Monday",	hour: "5pm",	value: 19380},{weekday: "Monday",	hour: "6am",	value: 6464},{weekday: "Monday",	hour: "6pm",	value: 16404},{weekday: "Monday",	hour: "7am",	value: 9386},{weekday: "Monday",	hour: "7pm",	value: 12758},{weekday: "Monday",	hour: "8am",	value: 17567},{weekday: "Monday",	hour: "8pm",	value: 10146},{weekday: "Monday",	hour: "9am",	value: 16551},{weekday: "Monday",	hour: "9pm",	value: 8082},{weekday: "Saturday",	hour: "10am",	value: 10620},{weekday: "Saturday",	hour: "10pm",	value: 10373},{weekday: "Saturday",	hour: "11am",	value: 12389},{weekday: "Saturday",	hour: "11pm",	value: 9350},{weekday: "Saturday",	hour: "12am",	value: 10367},{weekday: "Saturday",	hour: "12pm",	value: 13707},{weekday: "Saturday",	hour: "1am",	value: 6756},{weekday: "Saturday",	hour: "1pm",	value: 14980},{weekday: "Saturday",	hour: "2am",	value: 5565},{weekday: "Saturday",	hour: "2pm",	value: 16548},{weekday: "Saturday",	hour: "3am",	value: 5071},{weekday: "Saturday",	hour: "3pm",	value: 14465},{weekday: "Saturday",	hour: "4am",	value: 5591},{weekday: "Saturday",	hour: "4pm",	value: 16845},{weekday: "Saturday",	hour: "5am",	value: 4605},{weekday: "Saturday",	hour: "5pm",	value: 15508},{weekday: "Saturday",	hour: "6am",	value: 4388},{weekday: "Saturday",	hour: "6pm",	value: 14496},{weekday: "Saturday",	hour: "7am",	value: 4340},{weekday: "Saturday",	hour: "7pm",	value: 12640},{weekday: "Saturday",	hour: "8am",	value: 7602},{weekday: "Saturday",	hour: "8pm",	value: 11642},{weekday: "Saturday",	hour: "9am",	value: 8989},{weekday: "Saturday",	hour: "9pm",	value: 10527},{weekday: "Sunday",	hour: "10am",	value: 8356},{weekday: "Sunday",	hour: "10pm",	value: 8168},{weekday: "Sunday",	hour: "11am",	value: 10169},{weekday: "Sunday",	hour: "11pm",	value: 6509},{weekday: "Sunday",	hour: "12am",	value: 10530},{weekday: "Sunday",	hour: "12pm",	value: 11646},{weekday: "Sunday",	hour: "1am",	value: 7433},{weekday: "Sunday",	hour: "1pm",	value: 13121},{weekday: "Sunday",	hour: "2am",	value: 6042},{weekday: "Sunday",	hour: "2pm",	value: 15180},{weekday: "Sunday",	hour: "3am",	value: 5687},{weekday: "Sunday",	hour: "3pm",	value: 13335},{weekday: "Sunday",	hour: "4am",	value: 6433},{weekday: "Sunday",	hour: "4pm",	value: 15059},{weekday: "Sunday",	hour: "5am",	value: 5105},{weekday: "Sunday",	hour: "5pm",	value: 13823},{weekday: "Sunday",	hour: "6am",	value: 3960},{weekday: "Sunday",	hour: "6pm",	value: 12785},{weekday: "Sunday",	hour: "7am",	value: 3499},{weekday: "Sunday",	hour: "7pm",	value: 11254},{weekday: "Sunday",	hour: "8am",	value: 5559},{weekday: "Sunday",	hour: "8pm",	value: 10076},{weekday: "Sunday",	hour: "9am",	value: 6522},{weekday: "Sunday",	hour: "9pm",	value: 8944},{weekday: "Thursday",	hour: "10am",	value: 14787},{weekday: "Thursday",	hour: "10pm",	value: 8696},{weekday: "Thursday",	hour: "11am",	value: 14921},{weekday: "Thursday",	hour: "11pm",	value: 6970},{weekday: "Thursday",	hour: "12am",	value: 7205},{weekday: "Thursday",	hour: "12pm",	value: 15499},{weekday: "Thursday",	hour: "1am",	value: 3151},{weekday: "Thursday",	hour: "1pm",	value: 16118},{weekday: "Thursday",	hour: "2am",	value: 2283},{weekday: "Thursday",	hour: "2pm",	value: 18499},{weekday: "Thursday",	hour: "3am",	value: 1840},{weekday: "Thursday",	hour: "3pm",	value: 17413},{weekday: "Thursday",	hour: "4am",	value: 2099},{weekday: "Thursday",	hour: "4pm",	value: 20596},{weekday: "Thursday",	hour: "5am",	value: 2983},{weekday: "Thursday",	hour: "5pm",	value: 20479},{weekday: "Thursday",	hour: "6am",	value: 6118},{weekday: "Thursday",	hour: "6pm",	value: 17705},{weekday: "Thursday",	hour: "7am",	value: 9181},{weekday: "Thursday",	hour: "7pm",	value: 14223},{weekday: "Thursday",	hour: "8am",	value: 17940},{weekday: "Thursday",	hour: "8pm",	value: 11712},{weekday: "Thursday",	hour: "9am",	value: 16944},{weekday: "Thursday",	hour: "9pm",	value: 9780},{weekday: "Tuesday",	hour: "10am",	value: 15372},{weekday: "Tuesday",	hour: "10pm",	value: 7663},{weekday: "Tuesday",	hour: "11am",	value: 15300},{weekday: "Tuesday",	hour: "11pm",	value: 6090},{weekday: "Tuesday",	hour: "12am",	value: 6420},{weekday: "Tuesday",	hour: "12pm",	value: 15570},{weekday: "Tuesday",	hour: "1am",	value: 2687},{weekday: "Tuesday",	hour: "1pm",	value: 16152},{weekday: "Tuesday",	hour: "2am",	value: 1892},{weekday: "Tuesday",	hour: "2pm",	value: 18530},{weekday: "Tuesday",	hour: "3am",	value: 1498},{weekday: "Tuesday",	hour: "3pm",	value: 17244},{weekday: "Tuesday",	hour: "4am",	value: 1678},{weekday: "Tuesday",	hour: "4pm",	value: 20623},{weekday: "Tuesday",	hour: "5am",	value: 2953},{weekday: "Tuesday",	hour: "5pm",	value: 20549},{weekday: "Tuesday",	hour: "6am",	value: 6372},{weekday: "Tuesday",	hour: "6pm",	value: 17549},{weekday: "Tuesday",	hour: "7am",	value: 9646},{weekday: "Tuesday",	hour: "7pm",	value: 13878},{weekday: "Tuesday",	hour: "8am",	value: 18375},{weekday: "Tuesday",	hour: "8pm",	value: 10923},{weekday: "Tuesday",	hour: "9am",	value: 17644},{weekday: "Tuesday",	hour: "9pm",	value: 8762},{weekday: "Wednesday",	hour: "10am",	value: 14411},{weekday: "Wednesday",	hour: "10pm",	value: 8051},{weekday: "Wednesday",	hour: "11am",	value: 14227},{weekday: "Wednesday",	hour: "11pm",	value: 6245},{weekday: "Wednesday",	hour: "12am",	value: 6699},{weekday: "Wednesday",	hour: "12pm",	value: 15216},{weekday: "Wednesday",	hour: "1am",	value: 2965},{weekday: "Wednesday",	hour: "1pm",	value: 15624},{weekday: "Wednesday",	hour: "2am",	value: 1980},{weekday: "Wednesday",	hour: "2pm",	value: 18731},{weekday: "Wednesday",	hour: "3am",	value: 1645},{weekday: "Wednesday",	hour: "3pm",	value: 17484},{weekday: "Wednesday",	hour: "4am",	value: 1868},{weekday: "Wednesday",	hour: "4pm",	value: 20350},{weekday: "Wednesday",	hour: "5am",	value: 2877},{weekday: "Wednesday",	hour: "5pm",	value: 20437},{weekday: "Wednesday",	hour: "6am",	value: 6154},{weekday: "Wednesday",	hour: "6pm",	value: 18073},{weekday: "Wednesday",	hour: "7am",	value: 9509},{weekday: "Wednesday",	hour: "7pm",	value: 14161},{weekday: "Wednesday",	hour: "8am",	value: 17740},{weekday: "Wednesday",	hour: "8pm",	value: 11071},{weekday: "Wednesday",	hour: "9am",	value: 16363},{weekday: "Wednesday",	hour: "9pm",	value: 9187}]

series.data.setAll(data);

yAxis.data.setAll([
  { weekday: "Sunday" },
  { weekday: "Monday" },
  { weekday: "Tuesday" },
  { weekday: "Wednesday" },
  { weekday: "Thursday" },
  { weekday: "Friday" },
  { weekday: "Saturday" }
]);

xAxis.data.setAll([
  { hour: "12am" },
  { hour: "1am" },
  { hour: "2am" },
  { hour: "3am" },
  { hour: "4am" },
  { hour: "5am" },
  { hour: "6am" },
  { hour: "7am" },
  { hour: "8am" },
  { hour: "9am" },
  { hour: "10am" },
  { hour: "11am" },
  { hour: "12pm" },
  { hour: "1pm" },
  { hour: "2pm" },
  { hour: "3pm" },
  { hour: "4pm" },
  { hour: "5pm" },
  { hour: "6pm" },
  { hour: "7pm" },
  { hour: "8pm" },
  { hour: "9pm" },
  { hour: "10pm" },
  { hour: "11pm" }
]);

// Make stuff animate on load
// https://www.amcharts.com/docs/v5/concepts/animations/#Initial_animation
chart.appear(1000, 100);

}); // end am5.ready()