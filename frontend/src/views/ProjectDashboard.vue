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
        <ProjectSummary v-bind:statistics="statistics" />
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
import { mapGetters } from "vuex";
export default {
  data: () => ({
    //Werte für die Statistik
    statistics: {
      sum_of_done_sp: 0,
      sum_of_accepted_sp: 0,
      sum_of_sp: 0,
      sum_of_tasks: 0,
      sum_tasks_rated_not_finished: 0,
      sum_of_done_tasks: 0,
      sum_of_accepted_tasks: 0,
      avg_tasks_in_sprint: 0,
      avg_sp_in_sprint: 0,
      worst_sprints_sp: "0, 0, 0",
      worst_sprints_tasks: "0, 0, 0",
    },

    //Werte für den Plotly
    plotTitle: "Project burndown",
    plotly_data: {
      avg_finished_tasks_timeline: {
        x_data: [1, 2, 3, 4, 5],
        y_data: [0, 0, 0, 0, 0],
      },
      avg_finished_sp_timeline: {
        x_data: [1, 2, 3, 4, 5],
        y_data: [0, 0, 0, 0, 0],
      },
      finished_sp_timeline: {
        x_data: [1, 2, 3, 4, 5],
        y_data: [0, 0, 0, 0, 0],
      },
      finished_tasks_timeline: {
        x_data: [1, 2, 3, 4, 5],
        y_data: [0, 0, 0, 0, 0],
      },
    },
  }),

  components: {
    Plotly,
    ProjectInformation,
    ProjectSummary,
    ProjectCalendar,
  },

  methods: {
    //Daten aus dem Backend holen und den Variablen zuweisen...
    getProjectStatistic() {
      let stats = this.projectStatistic(this.$route.params.id);
      if (stats != undefined) {
        //Plotly-Data
        this.plotly_data.avg_finished_tasks_timeline.x_data =
          stats.avg_finished_tasks_timeline.x;
        this.plotly_data.avg_finished_tasks_timeline.y_data =
          stats.avg_finished_tasks_timeline.y;

        this.plotly_data.avg_finished_sp_timeline.y_data =
          stats.avg_finished_sp_timeline.x;
        this.plotly_data.avg_finished_sp_timeline.y_data =
          stats.avg_finished_sp_timeline.y;

        this.plotly_data.finished_sp_timeline.y_data =
          stats.finished_sp_timeline.x;
        this.plotly_data.finished_sp_timeline.y_data =
          stats.finished_sp_timeline.y;

        this.plotly_data.finished_tasks_timeline.y_data =
          stats.finished_tasks_timeline.x;
        this.plotly_data.finished_tasks_timeline.y_data =
          stats.finished_tasks_timeline.y;

        //Weitere Statisik-Werte
        this.statistics.sum_of_done_sp = stats.sum_of_done_sp;
        this.statistics.sum_of_accepted_sp = stats.sum_of_accepted_sp;
        this.statistics.sum_of_sp = stats.sum_of_sp;
        this.statistics.sum_of_tasks = stats.sum_of_tasks;
        this.statistics.sum_tasks_rated_not_finished =
          stats.sum_tasks_rated_not_finished;
        this.statistics.sum_of_done_tasks = stats.sum_of_done_tasks;
        this.statistics.sum_of_accepted_tasks = stats.sum_of_accepted_tasks;
        this.statistics.avg_tasks_in_sprint = stats.avg_tasks_in_sprint;
        this.statistics.avg_sp_in_sprint = stats.avg_sp_in_sprint;
        this.statistics.worst_sprints_sp = stats.worst_sprints_sp;
        this.statistics.worst_sprints_tasks = stats.worst_sprints_tasks;
      }
    },
  },

  computed: {
    ...mapGetters("projectStatistics", {
      projectStatistic: "byProjectId",
    }),

    //Daten für den Plotly
    plotData() {
      let avg_finished_tasks = {
        x: this.plotly_data.avg_finished_tasks_timeline.x_data,
        y: this.plotly_data.avg_finished_tasks_timeline.y_data,
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
        x: this.plotly_data.avg_finished_sp_timeline.x_data,
        y: this.plotly_data.avg_finished_sp_timeline.y_data,
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
        x: this.plotly_data.finished_tasks_timeline.x_data,
        y: this.plotly_data.finished_tasks_timeline.y_data,
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
        x: this.plotly_data.finished_sp_timeline.x_data,
        y: this.plotly_data.finished_sp_timeline.y_data,
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
        title: this.plotTitle,
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

  //Wenn die View gemounted wird, werden die Statistiken geladen
  mounted() {
    this.getProjectStatistic();
  },
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>