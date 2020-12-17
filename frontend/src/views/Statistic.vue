<template>
  <v-row>
    <v-col cols="1">
      <v-timeline>
        <v-timeline-item
          v-for="sprint in listSprints"
          :key="`${sprint.number}-sprint`"
          small
          fill-dot
        >
          <template v-slot:icon>
            <v-btn
              fab
              small
              color="link"
              class="white--text"
              @click="showSprint(sprint)"
            >
              {{ sprint.number }}
            </v-btn>
          </template>
        </v-timeline-item>
      </v-timeline>
    </v-col>
    <v-col cols="8">
      <!-- Hier kommt dann das weitere... /-->
      <Plotly
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
    <v-col cols="3">
      <v-card class="lane" height="100vh-50">
        <v-card-title class="navbar white--text">{{ infoTitle }}</v-card-title>
        <v-card-text class="navbar white--text">
          <v-list class="transparent">
            <v-subheader class="white--text">STORYPOINTS</v-subheader>
            <v-list-item dense>
              <v-list-item-title class="white--text"
                >Total amount</v-list-item-title
              >
              <v-list-item-subtitle class="white--text text-right">{{
                sum_of_planned_sp
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item dense>
              <v-list-item-title class="white--text"
                >Finished</v-list-item-title
              >
              <v-list-item-subtitle class="white--text text-right">{{
                sum_of_done_sp
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item dense>
              <v-list-item-title class="white--text"
                >Not finished</v-list-item-title
              >
              <v-list-item-subtitle class="white--text text-right">{{
                sum_of_not_done_sp
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-subheader class="white--text">TASKS</v-subheader>
            <v-list-item dense>
              <v-list-item-title class="white--text"
                >Total amount</v-list-item-title
              >
              <v-list-item-subtitle class="white--text text-right">{{
                sum_of_planned_tasks
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item dense>
              <v-list-item-title class="white--text"
                >Finished</v-list-item-title
              >
              <v-list-item-subtitle class="white--text text-right">{{
                sum_of_done_tasks
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item dense>
              <v-list-item-title class="white--text"
                >Not finished</v-list-item-title
              >
              <v-list-item-subtitle class="white--text text-right">{{
                sum_of_not_done_tasks
              }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from "vuex";
import Plotly from "@/components/Plotly.vue";

export default {
  name: "Statistic",
  data: () => ({
    plotTitle: "No sprint selected",
    infoTitle: "No sprint selected",
    sum_of_planned_tasks: "No sprint selected",
    sum_of_done_tasks: "No sprint selected",
    sum_of_not_done_tasks: "No sprint selected",
    sum_of_planned_sp: "No sprint selected",
    sum_of_done_sp: "No sprint selected",
    sum_of_not_done_sp: "No sprint selected",

    plotly_data: {
      planed: {
        x_data: [1, 2, 3, 4, 5],
        y_data: [10, 0, 10, 0, 10],
      },
      done: {
        x_data: [1, 2, 3, 4, 5],
        y_data: [5, 5, 5, 5, 5],
      },
    },
  }),
  components: {
    Plotly,
  },

  methods: {
    showSprint(sprint) {
      let stats = this.sprintStatistic(sprint.id);
      //Setzten des Graph-Titels
      this.plotTitle = "Burndownchart Sprint " + sprint.number;
      this.infoTitle = "Statistic Sprint " + sprint.number;
      //Zuweisen der einzelnen Werte zu den Anzeigevariablen
      this.sum_of_planned_sp = stats.sum_of_sp;
      this.sum_of_done_sp = stats.sum_of_done_sp;
      this.sum_of_not_done_sp = stats.sum_of_sp - stats.sum_of_done_sp;
      this.sum_of_planned_tasks = stats.sum_of_tasks;
      this.sum_of_done_tasks = stats.sum_of_done_tasks;
      this.sum_of_not_done_tasks = stats.sum_of_tasks - stats.sum_of_done_tasks;
      this.plotly_data.planed.x_data = stats.planned_sp_timeline.x;
      this.plotly_data.planed.y_data = stats.planned_sp_timeline.y;
      this.plotly_data.done.x_data = stats.finished_sp_timeline.x;
      this.plotly_data.done.y_data = stats.finished_sp_timeline.y;
    },
  },
  computed: {
    ...mapGetters("sprint", {
      listSprints: "list",
    }),

    ...mapGetters("sprintStatistics", {
      sprintStatistic: "bySprintId",
    }),

    plotData() {
      let planed = {
        x: this.plotly_data.planed.x_data,
        y: this.plotly_data.planed.y_data,
        name: "Ideal Story Points remaining",
        type: "scatter",
        //mode: "lines",
        line: {
          color: "#FFFFFF",
          width: 2,
        },
        connectgaps: true,
      };
      let done = {
        x: this.plotly_data.done.x_data,
        y: this.plotly_data.done.y_data,
        name: "Actual Story Points remaining",
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

      return [planed, done];
    },

    plotLayout() {
      return {
        autosize: true,
        width: 1100,
        height: 600,
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
          title: "Story Points",
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