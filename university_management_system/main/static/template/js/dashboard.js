(function ($) {
  "use strict";
  function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }
  $(function () {
    var $sales_chart = $("#sales-chart");
    $.ajax({
      url: $sales_chart.data("url"),
      success: function (data) {
        var SalesChartCanvas = $("#sales-chart").get(0).getContext("2d");
        var barColors = [];
        var barColors = [];
        for(let i=0; i<120; i++){
          barColors.push(getRandomColor());
        }
        var SalesChart = new Chart(SalesChartCanvas, {
          type: "bar",
          data: {
            labels: data.labels,
            datasets: [
              {
                label: "Marks",
                data: data.data,
                backgroundColor: barColors,
                // backgroundColor: '#98BDFF'
              },
            ],
          },
          options: {
            cornerRadius: 1,
            responsive: true,
            maintainAspectRatio: true,
            layout: {
              padding: {
                left: 0,
                right: 0,
                top: 0,
                bottom: 0,
              },
            },
            scales: {
              yAxes: [
                {
                  display: true,
                  gridLines: {
                    display: true,
                    drawBorder: false,
                    color: "#F2F2F2",
                    // color: '#98BDFF',
                  },
                  ticks: {
                    display: true,
                    min: 0,
                    max: 10,
                    callback: function (value, index, values) {
                      return value;
                    },
                    autoSkip: true,
                    maxTicksLimit: 10,
                    fontColor: "#6C7383",
                  },
                },
              ],
              xAxes: [
                {
                  stacked: false,
                  ticks: {
                    beginAtZero: true,
                    fontColor: "#6C7383",
                  },
                  gridLines: {
                    color: "rgba(0, 0, 0, 0)",
                    display: false,
                  },
                  barPercentage: 1,
                },
              ],
            },
            legend: {
              display: false,
            },
            elements: {
              point: {
                radius: 0,
              },
            },
          },
        });
        document.getElementById("sales-legend").innerHTML =
          SalesChart.generateLegend();
      },
    });

  });
 

  $(function () {
    var $pie_chart = $("#pieChart");
    var barColors = [];
    for(let i=0; i<120; i++){
      barColors.push(getRandomColor());
    }

    $.ajax({
      url: $pie_chart.data("url"),
      success: function (data) {
        var pieChartCanvas = $("#pieChart").get(0).getContext("2d");
        var pieChart = new Chart(pieChartCanvas, {
          type: "doughnut",
          data: {
            labels: data.labels,
            datasets: [{
              backgroundColor: barColors,
              data: data.data,
              hoverOffset: 4
            }]
          },
          options: {
            title: {
              display: true,
              text: "Skill-Set On Subject category"
            }
          }
        });
      
    }
  });
});

$(function () {
  var $bar_chart_h = $("#barChartH");
  var barColors = [];
  for(let i=0; i<120; i++){
    barColors.push(getRandomColor());
  }

  $.ajax({
    url: $bar_chart_h.data("url"),
    success: function (data) {
      var barChartCanvas = $("#barChartH").get(0).getContext("2d");
      var barChartH = new Chart(barChartCanvas, {
        type: "horizontalBar",
        data: {
          labels: data.labels,
          datasets: [{
            backgroundColor: barColors,
            data: data.data,
            hoverOffset: 5
          }]
        },
        options: {
          cornerRadius: 1,
          responsive: true,
          maintainAspectRatio: true,
          layout: {
            padding: {
              left: 0,
              right: 0,
              top: 0,
              bottom: 0,
            },
          },
          scales: {
            xAxes: [
              {
                display: true,
                gridLines: {
                  display: true,
                  drawBorder: false,
                  color: "#F2F2F2",
                  // color: '#98BDFF',
                },
                ticks: {
                  display: true,
                  min: 0,
                  max: 10,
                  callback: function (value, index, values) {
                    return value;
                  },
                  autoSkip: true,
                  maxTicksLimit: 100,
                  fontColor: "#6C7383",
                },
              },
            ],
            yAxes: [
              {
                stacked: false,
                ticks: {
                  beginAtZero: true,
                  fontColor: "#6C7383",
                },
                gridLines: {
                  color: "rgba(0, 0, 0, 0)",
                  display: false,
                },
                barPercentage: 1,
              },
            ],
          },
          legend: {
            display: false,
          },
          elements: {
            point: {
              radius: 0,
            },
          },
        },
      });
    
  }
});
});


})(jQuery);
