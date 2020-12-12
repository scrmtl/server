<template>
  <v-container fluid class="tabbody">
    <v-row>
      <v-col>
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
            Storypoints in project: {{ sp_in_project }} <br />
            Done storypoints: {{ done_sp_in_project }} <br />
            Accepted storypoints: {{ accepted_sp_in_project }} <br />
            Tasks in project: {{ tasks_in_project }} <br />
            Next Tasks: {{ sum_of_next_tasks }} <br />
            Done Tasks: {{ sum_of_done_tasks }} <br />
            Accepted Tasks: {{ sum_of_accepted_tasks }} <br /><br />

            Average accepted Tasks per sprint: {{ average_tasks_in_sprint }}
            <br />
            Averarge storypoints per sprint: {{ average_sp_in_sprint }}
            <br /><br />

            Three worst spirnts per storypoints: {{ worst_sprints_per_sp }}
            <br />
            Three worst sprints per tasks: {{ worst_sprints_per_task }} <br />
          </v-card-text> </v-card
      ></v-col>
    </v-row>
  </v-container>
</template>

<script>
//import { mapGetters } from "vuex";
import Plotly from "@/components/Plotly.vue";
export default {
  data: () => ({
    plotTitle: "Project burndown",

    //Statisik Werte:
    sp_in_project: "0",
    done_sp_in_project: "1",
    accepted_sp_in_project: "2",
    tasks_in_project: "3",
    sum_of_next_tasks: "4",
    sum_of_done_tasks: "5",
    sum_of_accepted_tasks: "6",
    average_tasks_in_sprint: "7",
    average_sp_in_sprint: "8",
    worst_sprints_per_sp: "9",
    worst_sprints_per_task: "10",

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
      };
      let todo_sp = {
        x: this.plotly_data.todo_sp.x_data,
        y: this.plotly_data.todo_sp.y_data,
        name: "ToDo storypoints",
        type: "scatter",
        mode: "lines",
      };
      let todo_tasks = {
        x: this.plotly_data.todo_tasks.x_data,
        y: this.plotly_data.todo_tasks.y_data,
        name: "ToDo tasks",
        type: "scatter",
        mode: "lines",
      };
      return [overall_sp, todo_sp, todo_tasks];
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
          title: "Story Points / Tasks",
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