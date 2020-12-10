<template>
  <v-main class="tabbody tab-content">
    <v-row>
      <v-col>
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
      <v-col>
        <v-card class="lane" height="100vh-50" max-width="400">
          <v-card-title class="navbar white--text">Statistic</v-card-title>
          <v-card-text class="tabbody--text">
            Number of task in sprint: {{ sum_of_planned_tasks }} <br />
            Number of storypoints in sprint: {{ sum_of_sp }} <br />
            Finished tasks: {{ sum_of_done_tasks }} <br />
            Not finished tasks: {{ sum_of_not_done_tasks }} <br />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col>
        <v-timeline>
          <v-timeline-item
            v-for="sprint in listSprints"
            :key="sprint.number"
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
    </v-row>
  </v-main>
</template>

<script>
import { mapGetters } from "vuex";
import Plotly from "@/components/Plotly.vue";

export default {
  name: "Statistic",
  data: () => ({
    plotTitle: "No sprint selected",

    sum_of_planned_tasks: "X",
    sum_of_sp: "X",
    sum_of_done_tasks: "X",
    sum_of_not_done_tasks: "X",

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

      //Zuweisen der einzelnen Werte zu den Anzeigevariablen
      this.sum_of_planned_tasks = stats.sum_of_tasks;
      this.sum_of_sp = stats.sum_of_sp;
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
        name: "Planed",
        type: "scatter",
        mode: "lines",
      };
      let done = {
        x: this.plotly_data.done.x_data,
        y: this.plotly_data.done.y_data,
        name: "Done",
        type: "scatter",
        mode: "lines",
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
        //font: this.config.font,
        xaxis: {
          title: "Days",
        },
        yaxis: {
          title: "Story Points",
        },
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