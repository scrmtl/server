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
        <v-card class="lane" height="100vh-50" >
          <v-card-title class="navbar white--text">{{ infoTitle }}</v-card-title>
          <v-card-text class=" navbar white--text">
            <v-list class="transparent">
              <v-subheader class="white--text text-decoration-underline text-subtitle-1">STORYPOINTS</v-subheader>
              <v-list-item>
                <v-list-item-title class="white--text">Total amount</v-list-item-title>
                <v-list-item-subtitle class="white--text text-right">{{ sum_of_planned_sp }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title class="white--text">Finished</v-list-item-title>
                <v-list-item-subtitle class="white--text text-right">{{ sum_of_done_sp }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title class="white--text">Not finished</v-list-item-title>
                <v-list-item-subtitle class="white--text text-right">{{ sum_of_not_done_sp }}</v-list-item-subtitle>
              </v-list-item>
              <v-subheader class="white--text text-decoration-underline text-subtitle-1">TASKS</v-subheader>
              <v-list-item>
                <v-list-item-title class="white--text">Total amount</v-list-item-title>
                <v-list-item-subtitle class="white--text text-right">{{ sum_of_planned_tasks }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title class="white--text">Finished</v-list-item-title>
                <v-list-item-subtitle class="white--text text-right">{{ sum_of_done_tasks }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title class="white--text">Not finished</v-list-item-title>
                <v-list-item-subtitle class="white--text text-right">{{ sum_of_not_done_tasks }}</v-list-item-subtitle>
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