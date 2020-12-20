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
  data: () => ({

  }),

  components: {
    Plotly,
    ProjectInformation,
    ProjectSummary,
    ProjectCalendar,
  },

  methods: {
    
  },

  computed: {
    ...mapGetters("projectStatistics", {
      projectStatisticById: "byProjectId",
    }),

    projectStatistic(){
      var stat = this.projectStatisticById(this.$route.params.id);
      if(stat !== undefined){
        return stat;
      }
      else{
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
        }
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
        line: {
          color: "#FFFFFF",
          width: 2,
        },
        connectgaps: true,
      };
      let avg_finished_sp = {
        x: this.projectStatistic.avg_finished_sp_timeline.x,
        y: this.projectStatistic.avg_finished_sp_timeline.y,
        name: "Average of finished Story Points",
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
      let finished_tasks = {
        x: this.projectStatistic.finished_tasks_timeline.x,
        y: this.projectStatistic.finished_tasks_timeline.y,
        name: "Finished Tasks",
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

      let finished_sp = {
        x: this.projectStatistic.finished_sp_timeline.x,
        y: this.projectStatistic.finished_sp_timeline.y,
        name: "Finished Story Points",
        type: "scatter",
        mode: "lines+markers",
        marker: {
          size: 10,
        },
        line: {
          color: "pink",
          width: 4,
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
          title: "Story Points / Tasks",
          dtick: 5,
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
      };
    },
  },

  mounted() {

  },
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>