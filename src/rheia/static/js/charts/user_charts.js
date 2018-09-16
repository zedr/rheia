(function (NS) {
  "use strict";

  var $ = NS.jQuery,
    nv = NS.nv,
    d3 = NS.d3;

  function draw(data) {
    nv.addGraph(function () {
      var chart = nv.models.pieChart()
        .x(function (d) {
          return d.label;
        })
        .y(function (d) {
          return d.value;
        });
      d3.select("#chart svg")
        .datum(data)
        .transition().duration(350)
        .call(chart);
      return chart;
    });
  }

  function initialise() {
    $.get("time", null, draw, "json");
  }

  $(NS.document).ready(initialise);

}(this));
