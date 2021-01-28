<template>
  <div ref="pdf">
    <v-row>
      <v-col cols="8">
        <!-- Hier kommt dann das weitere... /-->
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
      <v-col cols="3">
        <div>
          <v-card class="lane primary" height="700">
            <v-card-title class="navbar white--text">{{
              infoTitle
            }}</v-card-title>
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
                    >Done</v-list-item-title
                  >
                  <v-list-item-subtitle class="white--text text-right">{{
                    sum_of_done_sp
                  }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item dense>
                  <v-list-item-title class="white--text"
                    >Not done</v-list-item-title
                  >
                  <v-list-item-subtitle class="white--text text-right">{{
                    sum_of_not_done_sp
                  }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item dense>
                  <v-list-item-title class="white--text"
                    >Accepted</v-list-item-title
                  >
                  <v-list-item-subtitle class="white--text text-right">{{
                    sum_of_accepted_sp
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
                    >Done</v-list-item-title
                  >
                  <v-list-item-subtitle class="white--text text-right">{{
                    sum_of_done_tasks
                  }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item dense>
                  <v-list-item-title class="white--text"
                    >Not done</v-list-item-title
                  >
                  <v-list-item-subtitle class="white--text text-right">{{
                    sum_of_not_done_tasks
                  }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item dense>
                  <v-list-item-title class="white--text"
                    >Accepted</v-list-item-title
                  >
                  <v-list-item-subtitle class="white--text text-right">{{
                    sum_of_accepted_tasks
                  }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-card-text>
            <v-card-actions>
              <v-btn
                color="link"
                :disabled="selectedSprint == null"
                outlined
                @click="createReport(selectedSprint)"
              >
                <v-icon>mdi-file-chart</v-icon>
                Export Sprint Report
              </v-btn>
            </v-card-actions>
          </v-card>
        </div>
      </v-col>
      <v-col cols="1">
        <v-timeline class="sprint-number-lane">
          <v-timeline-item
            v-for="sprint in sortedSprintList"
            :key="`${sprint.number}-sprint`"
            small
            fill-dot
          >
            <template v-slot:icon>
              <v-btn
                fab
                small
                :color="formatSprintList(sprint).color"
                :class="`${formatSprintList(sprint).text}--text`"
                @click="showSprint(sprint)"
              >
                {{ sprint.number }}
              </v-btn>
            </template>
          </v-timeline-item>
        </v-timeline>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import Plotly from "@/components/Plotly.vue";
import exportPdf from "@/mixins/pdfExportMixin";

export default {
  name: "Statistic",
  components: {
    Plotly,
  },
  mixins: [exportPdf],
  data: () => ({
    reportDialog: false,
    selectedSprint: null,
    selectedSprintStatistic: null,
    plotTitle: "No sprint selected",
    infoTitle: "No sprint selected",
    sum_of_planned_tasks: "No sprint selected",
    sum_of_done_tasks: "No sprint selected",
    sum_of_accepted_tasks: "No sprint selected",
    sum_of_not_done_tasks: "No sprint selected",
    sum_of_planned_sp: "No sprint selected",
    sum_of_done_sp: "No sprint selected",
    sum_of_accepted_sp: "No sprint selected",
    sum_of_not_done_sp: "No sprint selected",

    plotly_data: {
      planed: {
        //x_data: [1, 2, 3, 4, 5],
        x_data: [1, 2, 3, 4, 5],
        //y_data: [10, 0, 10, 0, 10],
        y_data: [0, 0, 0, 0, 0],
      },
      done: {
        //x_data: [1, 2, 3, 4, 5],
        x_data: [1, 2, 3, 4, 5],
        //y_data: [5, 5, 5, 5, 5],
        y_data: [0, 0, 0, 0, 0],
      },
      done_tasks: {
        //x_data: [1, 2, 3, 4, 5],
        x_data: [1, 2, 3, 4, 5],
        //y_data: [10, 10, 10, 10, 10],
        y_data: [0, 0, 0, 0, 0],
      },
    },
  }),

  methods: {
    showSprint(sprint) {
      let stats = this.sprintStatistic(sprint.id);
      if (stats != undefined) {
        //Setzten des Graph-Titels
        this.selectedSprint = sprint;
        this.selectedSprintStatistic = stats;
        this.plotTitle = "Burn-Down chart Sprint " + sprint.number;
        this.infoTitle = "Summary Sprint " + sprint.number;
        //Zuweisen der einzelnen Werte zu den Anzeigevariablen
        this.sum_of_planned_sp = stats.sum_of_sp;
        this.sum_of_done_sp = stats.sum_of_done_sp;
        this.sum_of_accepted_sp = stats.sum_of_accepted_sp;
        this.sum_of_not_done_sp = stats.sum_of_sp - stats.sum_of_done_sp;
        this.sum_of_planned_tasks = stats.sum_of_tasks;
        this.sum_of_done_tasks = stats.sum_of_done_tasks;
        this.sum_of_accepted_tasks = stats.sum_of_accepted_tasks;
        this.sum_of_not_done_tasks =
          stats.sum_of_tasks - stats.sum_of_done_tasks;
        this.plotly_data.planed.x_data = stats.planned_sp_timeline.x;
        this.plotly_data.planed.y_data = stats.planned_sp_timeline.y;
        this.plotly_data.done.x_data = stats.finished_sp_timeline.x;
        this.plotly_data.done.y_data = stats.finished_sp_timeline.y;
        this.plotly_data.done_tasks.x_data = stats.finished_tasks_timeline.x;
        this.plotly_data.done_tasks.y_data = stats.finished_tasks_timeline.y;
      }
    },
    formatSprintList(sprint) {
      var format = {
        color: "link",
        text: "white",
      };
      switch (sprint.status) {
        // In Planning
        case "IL":
          format.color = "link";
          format.text = "white";
          break;
        // Planned
        case "PL":
          format.color = "primary";
          format.text = "white";
          break;
        // In Progress
        case "IR":
          format.color = "primary";
          format.text = "link";
          break;
        // Done
        case "DO":
          format.color = "secondary";
          format.text = "white";
          break;
        // Accepted
        case "AC":
          format.color = "secondary";
          format.text = "white";
          break;
      }
      return format;
    },
  },
  computed: {
    ...mapGetters("sprint", {
      listSprints: "byProjectId",
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
      let done_tasks = {
        x: this.plotly_data.done_tasks.x_data,
        y: this.plotly_data.done_tasks.y_data,
        name: "Done Tasks",
        type: "bar",
        yaxis: "y2",
        marker: {
          color: "orange",
        },
      };

      return [planed, done, done_tasks];
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
          title: "Story Points",
          dtick: 5,
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
      };
    },

    sortedSprintList() {
      var list = this.listSprints(parseInt(this.$route.params.id));
      var sorted = list.sort(function (a, b) {
        var keyA = a.number;
        var keyB = b.number;
        // Vergleiche ob AC oder AR
        if (keyA > keyB) return -1;
        if (keyA < keyB) return 1;
        return 0;
      });
      return sorted;
    },
  },
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>