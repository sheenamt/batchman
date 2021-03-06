import React from "react";
import {Vega} from 'react-vega';

var ChartSpec={
  "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
  "repeat": ["%cpu", "%mem", "peak_rss", "peak_vmem"],
  "columns": 1,
  "spec": {
    "width": 800,
    "height": 200,
    "layer": [
      {
        "mark": {"type": "tick"},
        "encoding": {
          "color": {"field": "process", "type": "nominal"},
          "opacity": {"value": 0.7},
          "y": {
            "field": "process",
            "type": "ordinal",
            "title":  null
          },
          "x": {
            "field": {"repeat": "repeat"},
            "type": "quantitative",
            "axis": {
              "grid": true,
              "tickCount": 10
            }
          },
          "tooltip": [
            {"field": "task", "type": "ordinal"},
            {"field": "%cpu", "type": "quantitative"}
          ]
        }
      }
    ]
  },
  "config": {
    "view": {
       "stroke": "transparent"
    },
    "tick": {
      "thickness": 3,
      "bandSize": 30
    }
  }
};

export const ResourceChart = ({taskData}) => {
	if (taskData === undefined){
		return null;
	}
  const data = taskData.map((t) => ({
  	"task": t.taskLastTrace.name, // e.g., 'fastqc (1)'
  	"process": t.taskLastTrace.process, // e.g., 'fastqc'
  	// add mapping of resource metrics here
    "%cpu": t.taskLastTrace['%cpu'],
    "%mem": t.taskLastTrace['%mem'],
    "peak_rss": t.taskLastTrace['peak_rss'],
    "peak_vmem": t.taskLastTrace['peak_vmem'],
  }))
	ChartSpec.data = {"values": data};
	return <Vega spec={ChartSpec} />

}
