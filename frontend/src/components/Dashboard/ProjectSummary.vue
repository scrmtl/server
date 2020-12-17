<template>
<v-card>
  <v-card-title class="navbar white--text">Project summary</v-card-title>
  <v-card-text class="navbar white--text">
    <v-list class="transparent">
      <v-subheader class="white--text ">STORYPOINTS</v-subheader>
      <v-list-item dense>
        <v-list-item-title class="white--text">Total amount</v-list-item-title>
        <v-list-item-subtitle class="white--text text-right">{{ projectSummary.sumSp }}</v-list-item-subtitle>
      </v-list-item>
      <v-list-item dense>
        <v-list-item-title class="white--text">Done</v-list-item-title>
        <v-list-item-subtitle class="white--text text-right">{{ projectSummary.sumDoneSp }}</v-list-item-subtitle>
      </v-list-item>
      <v-list-item dense>
        <v-list-item-title class="white--text">Accepted</v-list-item-title>
        <v-list-item-subtitle class="white--text text-right">{{ projectSummary.sumAcceptedSp}}</v-list-item-subtitle>
      </v-list-item>
      <v-subheader class="white--text">TASKS</v-subheader>
      <v-list-item dense>
        <v-list-item-title class="white--text">Total amount</v-list-item-title>
        <v-list-item-subtitle class="white--text text-right">{{ projectSummary.sumTasks }}</v-list-item-subtitle>
      </v-list-item>
      <v-list-item dense>
        <v-list-item-title class="white--text">Planned</v-list-item-title>
        <v-list-item-subtitle class="white--text text-right">{{ projectSummary.sumPlannedTasks }}</v-list-item-subtitle>
      </v-list-item>
      <v-list-item dense>
        <v-list-item-title class="white--text">Done</v-list-item-title>
        <v-list-item-subtitle class="white--text text-right">{{ projectSummary.sumDoneTasks }}</v-list-item-subtitle>
      </v-list-item>
      <v-list-item dense>
        <v-list-item-title class="white--text">Accepted</v-list-item-title>
        <v-list-item-subtitle class="white--text text-right">{{ projectSummary.sumAcceptedTasks }}</v-list-item-subtitle>
      </v-list-item>
      <v-subheader class="white--text">SPRINTS</v-subheader>
      <v-list-item dense>
        <v-list-item-title class="white--text">Average accepted Tasks</v-list-item-title>
        <v-list-item-subtitle class="white--text text-right">{{ projectSummary.avgAcceptedSp }}</v-list-item-subtitle>
      </v-list-item>
      <v-list-item dense>
        <v-list-item-title class="white--text">Average accepted Stortypoints</v-list-item-title>
        <v-list-item-subtitle class="white--text text-right">{{ projectSummary.avgAcceptedTasks }}</v-list-item-subtitle>
      </v-list-item>
      <v-list-item dense>
        <v-list-item-title class="white--text">The 3 worst sprints (related Tasks)</v-list-item-title>
        <v-list-item-subtitle class="white--text text-right">{{ projectSummary.rank3WorstSprintTasks }}</v-list-item-subtitle>
      </v-list-item>
      <v-list-item dense>
        <v-list-item-title class="white--text">The 3 worst sprints (related SP)</v-list-item-title>
        <v-list-item-subtitle class="white--text text-right">{{ projectSummary.rank3WorstSprintSp }}</v-list-item-subtitle>
      </v-list-item>
    </v-list>
  </v-card-text>
</v-card>
</template>

<script>
export default {
  name: "ProjectSummary",
  data: () =>({

  }),
  computed: {
    projectSummary(){
      // TODO Call Project statistic api
      var summary = {
        sumSp: "10",
        sumDoneSp: "1",
        sumAcceptedSp: "1",
        sumTasks: "5",
        sumPlannedTasks: "5",
        sumDoneTasks: "1",
        sumAcceptedTasks: "1",
        avgAcceptedSp: "1",
        avgAcceptedTasks: "1",
        rank3WorstSprintSp: "1, 2, 3",
        rank3WorstSprintTasks: "4, 5, 8"
      } 
      return summary;
    }
  }
}
</script>

<style>

</style>