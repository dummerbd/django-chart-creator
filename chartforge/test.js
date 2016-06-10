/**
 * Created by ben on 6/10/16.
 */
(function () {
  'use strict';

  var chartConfig = {
    "title": {
      "text": null
    },
    "credits": {
      "enabled": false
    },
    "legend": {
      "enabled": false
    },
    "chart": {
      "marginTop": 0,
      "marginBottom": 0,
      "marginRight": 6,
      "marginLeft": 60,
      "width": 210,
      "height": 250
    },
    "plotOptions": {
      "line": {
        "marker": {
          "enabled": false
        },
        "dataLabels": {
          "enabled": true,
          "format": "{point.name}",
          "y": 4
        }
      }
    },
    "xAxis": [
      {
        "labels": {
          "enabled": false
        }
      }
    ],
    "yAxis": [
      {
        "endOnTick": false,
        "startOnTick": false,
        "tickInterval": 10,
        "tickAmount": 6,
        "max": 105,
        "min": -15,
        "title": {
          "text": "TEMPERATURE",
          "style": {
            "color": "#666"
          }
        }
      }
    ],
    "tooltip": {
      "enabled": false
    },
    "series": [
      {
        "name": "Avg Hi",
        "type": "line",
        "data": [
          {
            "y": 76.5,
            "name": "Avg Hi 76.5"
          },
          {
            "y": 76.5,
            "name": ""
          }
        ],
        "color": "#af3333"
      },
      {
        "name": "Avg Low",
        "type": "line",
        "data": [
          {
            "y": 54.1,
            "name": "Avg Low 54.1"
          },
          {
            "y": 54.1,
            "name": ""
          }
        ],
        "color": "#3360a9"
      },
      {
        "name": "Record Hi",
        "type": "line",
        "data": [
          {
            "y": 89.1,
            "name": "Record (1933) 89.1"
          },
          {
            "y": 89.1,
            "name": "89.1F"
          }
        ],
        "color": "#ff3333"
      },
      {
        "name": "Min Temp",
        "type": "line",
        "data": [
          {
            "y": 35.6,
            "name": "Record (1977)"
          },
          {
            "y": 35.6,
            "name": "35.6F"
          }
        ],
        "color": "#3366ff"
      }
    ]
  };
})();
