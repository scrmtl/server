<template>
  <v-container fluid>
    <v-row>
      <v-col cols="4">
        <ProjectInformation />
      </v-col>
      <v-col cols="8">
        <ProjectCalendar />
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
        <ProjectSummary />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Plotly from "@/components/Plotly.vue";
import ProjectInformation from "@/components/Dashboard/ProjectInformation.vue";
import ProjectSummary from "@/components/Dashboard/ProjectSummary.vue";
import ProjectCalendar from "@/components/Dashboard/ProjectCalendar.vue";
import { mapGetters } from "vuex";
export default {
  data: () => ({}),

  components: {
    Plotly,
    ProjectInformation,
    ProjectSummary,
    ProjectCalendar,
  },

  methods: {
    //Funktion um die Width der Bars beim Plotly einzustellen
    makeWidthArray(x_array) {
      var width = 0.1;
      var length = x_array.length;
      var data = [];

      for (var i = 0; i < length; i++) {
        data.push(width);
      }

      return data;
    },
  },

  computed: {
    ...mapGetters("projectStatistics", {
      projectStatisticById: "byProjectId",
    }),

    projectStatistic() {
      var stat = this.projectStatisticById(this.$route.params.id);
      if (stat !== undefined) {
        return stat;
      } else {
        var defaultData = {
          avg_finished_tasks_timeline: {
            x: [1, 2, 3, 4, 5],
            y: [0, 0, 0, 0, 0],
          },
          avg_finished_sp_timeline: {
            x: [1, 2, 3, 4, 5],
            y: [0, 0, 0, 0, 0],
          },
          finished_sp_timeline: {
            x: [1, 2, 3, 4, 5],
            y: [0, 0, 0, 0, 0],
          },
          finished_tasks_timeline: {
            x: [1, 2, 3, 4, 5],
            y: [0, 0, 0, 0, 0],
          },
        };
        return defaultData;
      }
    },

    //Data for Plotly projetc diagramm
    plotData() {
      let avg_finished_tasks = {
        x: this.projectStatistic.avg_finished_tasks_timeline.x,
        y: this.projectStatistic.avg_finished_tasks_timeline.y,
        name: "Average of finished Tasks",
        type: "scatter",
        mode: "lines",
        yaxis: "y2",
        line: {
          color: "#448AFF",
          width: 4,
          dash: "dash",
        },
        connectgaps: true,
      };
      let avg_finished_sp = {
        x: this.projectStatistic.avg_finished_sp_timeline.x,
        y: this.projectStatistic.avg_finished_sp_timeline.y,
        name: "Average of finished Story Points",
        type: "scatter",
        mode: "lines",
        line: {
          color: "#FF5252",
          width: 4,
          dash: "dash",
        },
        connectgaps: true,
      };
      let finished_tasks = {
        x: this.projectStatistic.finished_tasks_timeline.x,
        y: this.projectStatistic.finished_tasks_timeline.y,
        width: this.makeWidthArray(
          this.projectStatistic.finished_tasks_timeline.x
        ),
        name: "Finished Tasks",
        type: "bar",
        yaxis: "y2",
        marker: {
          color: "orange",
          size: 5,
          opacity: 0.6,
        },
        alignmentgroup: "1",
        connectgaps: true,
      };

      let finished_sp = {
        x: this.projectStatistic.finished_sp_timeline.x,
        y: this.projectStatistic.finished_sp_timeline.y,
        name: "Finished Story Points",
        type: "scatter",
        marker: {
          color: "#009688",
          size: 5,
        },
        connectgaps: true,
      };
      return [avg_finished_tasks, avg_finished_sp, finished_tasks, finished_sp];
    },

    //Layout optionen von dem Plotly
    plotLayout() {
      return {
        autosize: true,
        height: 700,
        argin: { t: 25, l: 45, r: 10, b: 30 },
        title: "Project analysis",
        font: {
          family: "sans-serif",
          size: 15,
          color: "#FFFFFF",
        },
        xaxis: {
          title: "Sprints",
          dtick: 1,
          gridcolor: "#636363",
          gridwidth: 2,
          zerolinecolor: "#636363",
          zerolinewidth: 4,
        },
        yaxis: {
          title: "Story points",
          dtick: 4,
          gridcolor: "#636363",
          gridwidth: 2,
          zerolinecolor: "#636363",
          zerolinewidth: 4,
        },
        yaxis2: {
          title: "Tasks",
          dtick: 1,
          //gridcolor: "#636363",
          //gridwidth: 2,
          //zerolinecolor: "#636363",
          //zerolinewidth: 4,
          overlaying: "y",
          side: "right",
        },
        legend: {
          x: 0,
          y: 50,
        },
        paper_bgcolor: "#6441A4",
        plot_bgcolor: "#6441A4",
        bargap: 0.5,
        barmode: "group",
      };
    },
  },

  mounted() {},
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>
