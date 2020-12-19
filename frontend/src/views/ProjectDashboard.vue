<template>
<v-container fluid>
  <v-row>
    <v-col cols="4">
      <ProjectInformation/>
    </v-col>
    <v-col cols="8">
      <ProjectCalendar/>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols="8">
      <Plotly
        autoResize
        :data="plotData"
        :layout="plotLayout"
        :options="{
          modeBarButtonsToRemove: [
            'sendDataToCloud',
            'toImage',
            'autoScale2d',
            'hoverClosestCartesian',
            'hoverCompareCartesian',
            'lasso2d',
            'select2d',
          ],
          displaylogo: false,
          showTips: false,
          staticPlot: true,
          displayModeBar: false,
        }"
      />
    </v-col>
    <v-col cols="4">
      <ProjectSummary/>
    </v-col>
  </v-row>
</v-container>
</template>

<script>
//import { mapGetters } from "vuex";
import Plotly from "@/components/Plotly.vue";
import ProjectInformation from "@/components/Dashboard/ProjectInformation.vue";
import ProjectSummary from "@/components/Dashboard/ProjectSummary.vue";
import ProjectCalendar from "@/components/Dashboard/ProjectCalendar.vue";
export default {
  data: () => ({
    plotTitle: "Project burndown",
    //Werte für den Plotly
    plotly_data: {
      overall_sp: {
        x_data: [1, 2, 3, 4, 5],
        y_data: [5, 4, 3, 2, 1],
      },
      todo_sp: {
        x_data: [1, 2, 3, 4, 5],
        y_data: [5, 5, 5, 5, 0],
      },
      todo_tasks: {
        x_data: [1, 2, 3, 4, 5],
        y_data: [4, 4, 4, 4, 3],
      }
    },
  }),

  components: {
    Plotly,
    ProjectInformation,
    ProjectSummary,
    ProjectCalendar
  },

  methods: {},

  computed: {
    plotData() {
      let overall_sp = {
        x: this.plotly_data.overall_sp.x_data,
        y: this.plotly_data.overall_sp.y_data,
        name: "Planed storypoints",
        type: "scatter",
        mode: "lines",
          line: {
          color: "#FFFFFF",
          width: 2,
        },
        connectgaps: true,
      };
      let todo_sp = {
        x: this.plotly_data.todo_sp.x_data,
        y: this.plotly_data.todo_sp.y_data,
        name: "ToDo Story Points",
        type: "scatter",
        mode: "lines+markers",
        marker: {
          size: 10,
        },
        line: {
          color: "#31AA96",
          width: 4,
        },
        connectgaps: true,
      };
      let todo_tasks = {
        x: this.plotly_data.todo_tasks.x_data,
        y: this.plotly_data.todo_tasks.y_data,
        name: "ToDo Tasks",
        type: "scatter",
        mode: "lines+markers",
        marker: {
          size: 10,
        },
        line: {
          color: "orange",
          width: 4,
        },
        connectgaps: true,
      };
      return [overall_sp, todo_sp, todo_tasks];
    },

plotLayout() {
      return {
        autosize: true,
        height: 700,
        argin: { t: 25, l: 45, r: 10, b: 30 },
        title: this.plotTitle,
        font: {
          family: "sans-serif",
          size: 15,
          color: "#FFFFFF",
        },
        xaxis: {
          title: "Days",
          dtick: 5,
          gridcolor: "#636363",
          gridwidth: 2,
          zerolinecolor: "#636363",
          zerolinewidth: 4,
        },
        yaxis: {
          title: "Story Points / Tasks",
          dtick: 1,
          gridcolor: "#636363",
          gridwidth: 2,
          zerolinecolor: "#636363",
          zerolinewidth: 4,
        },
        legend: {
          x: 0,
          y: 50,
        },
        paper_bgcolor: "#6441A4",
        plot_bgcolor: "#6441A4",
        //bargap: 0,
        //showlegend: this.legend
      };
    },
  },
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>