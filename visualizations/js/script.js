
// Create chart instance
var chart = am4core.create("chartdiv", am4charts.PieChart);

// var title = chart.titles.create();
// title.text = "Distibution of Crashes over Boroughs";
// title.fontSize = 25;
// title.marginBottom = 10

// Create pie series
var series = chart.series.push(new am4charts.PieSeries());
series.dataFields.value = "crashes";
series.dataFields.category = "borough";

// Add data
chart.data = [
  {
    "borough": "Bronx",
    "crashes": 185476
  },
  {
    "borough": "Brooklyn",
    "crashes": 402085
  },
  {
    "borough": "Manhattan",
    "crashes": 293366
  },
  {
    "borough": "Queens",
    "crashes": 342033
  },
  {
    "borough": "Staten Island",
    "crashes": 53744
  }
];

// And, for a good measure, let's add a legend
chart.legend = new am4charts.Legend();
