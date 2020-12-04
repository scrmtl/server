<template>
  <v-card min-width="385" max-width="420">
    <v-card-title class="navbar white--text">
      {{sprintName}}
    </v-card-title>
    <v-card-subtitle class="navbar white--text">
      {{ sprintMetaData }}
    </v-card-subtitle>
    <v-card-text 
      class="lane-body  flex-column" 
    >
      <v-row justify="center"  class="" v-for="task in laneTask" :key="task.id">
        <Task v-bind:task="task" />
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import Task from "@/components/Task.vue";
import { mapGetters } from 'vuex';
export default {
  data: () => ({
    
  }),
  components: {
    Task
  },
  props: {
    sprint: {},
  },
  computed:{
    ...mapGetters("task", {
      tasksByIdArray: "byIdArray"
    }),
    sprintName(){
      return "Sprint " + this.sprint.number;
    },
    sprintMetaData(){
      return "(" + this.sprint.start + " to " + this.sprint.end + ")";
    },
    laneTask(){
      return this.tasksByIdArray(this.sprint.task_cards);
    }

  }
}
</script>

<style>

</style>