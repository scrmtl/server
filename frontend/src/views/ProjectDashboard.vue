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