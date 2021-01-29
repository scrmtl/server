<template>
  <v-card tile flat height="700" class="navbar">
    <v-card-title class="navbar white--text">Project summary</v-card-title>
    <v-card-text class="navbar white--text">
      <v-list class="transparent">
        <v-subheader class="white--text">STORYPOINTS</v-subheader>
        <v-list-item dense>
          <v-list-item-title class="white--text"
            >Total amount</v-list-item-title
          >
          <v-list-item-subtitle class="white--text text-right">{{
            projectStatistic.sum_of_sp
          }}</v-list-item-subtitle>
        </v-list-item>
        <v-list-item dense>
          <v-list-item-title class="white--text">Done</v-list-item-title>
          <v-list-item-subtitle class="white--text text-right">{{
            projectStatistic.sum_of_done_sp
          }}</v-list-item-subtitle>
        </v-list-item>
        <v-list-item dense>
          <v-list-item-title class="white--text">Accepted</v-list-item-title>
          <v-list-item-subtitle class="white--text text-right">{{
            projectStatistic.sum_of_accepted_sp
          }}</v-list-item-subtitle>
        </v-list-item>
        <v-subheader class="white--text">TASKS</v-subheader>
        <v-list-item dense>
          <v-list-item-title class="white--text"
            >Total amount</v-list-item-title
          >
          <v-list-item-subtitle class="white--text text-right">{{
            projectStatistic.sum_of_tasks
          }}</v-list-item-subtitle>
        </v-list-item>
        <v-list-item dense>
          <v-list-item-title class="white--text">Planned</v-list-item-title>
          <v-list-item-subtitle class="white--text text-right">{{
            projectStatistic.sum_tasks_rated_not_finished
          }}</v-list-item-subtitle>
        </v-list-item>
        <v-list-item dense>
          <v-list-item-title class="white--text">Done</v-list-item-title>
          <v-list-item-subtitle class="white--text text-right">{{
            projectStatistic.sum_of_done_tasks
          }}</v-list-item-subtitle>
        </v-list-item>
        <v-list-item dense>
          <v-list-item-title class="white--text">Accepted</v-list-item-title>
          <v-list-item-subtitle class="white--text text-right">{{
            projectStatistic.sum_of_accepted_tasks
          }}</v-list-item-subtitle>
        </v-list-item>
        <v-subheader class="white--text">SPRINTS</v-subheader>
        <v-list-item dense>
          <v-list-item-title class="white--text"
            >Average accepted Story Points</v-list-item-title
          >
          <v-list-item-subtitle class="white--text text-right">{{
            projectStatistic.avg_sp_in_sprint
          }}</v-list-item-subtitle>
        </v-list-item>
        <v-list-item dense>
          <v-list-item-title class="white--text"
            >Average accepted Tasks</v-list-item-title
          >
          <v-list-item-subtitle class="white--text text-right">{{
            projectStatistic.avg_tasks_in_sprint
          }}</v-list-item-subtitle>
        </v-list-item>
        <v-list-item dense>
          <v-list-item-title class="white--text"
            >The 3 worst sprints (related Tasks)</v-list-item-title
          >
          <v-list-item-subtitle class="white--text text-right">{{
            projectStatistic.worst_sprints_tasks
          }}</v-list-item-subtitle>
        </v-list-item>
        <v-list-item dense>
          <v-list-item-title class="white--text"
            >The 3 worst sprints (related SP)</v-list-item-title
          >
          <v-list-item-subtitle class="white--text text-right">{{
            projectStatistic.worst_sprints_sp
          }}</v-list-item-subtitle>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "ProjectSummary",
  data: () => ({}),
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
        };
        return defaultData;
      }
    },
  },
};
</script>

<style></style>