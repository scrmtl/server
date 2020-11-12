<template>
  <v-card min-width="385" max-width="420">
    <v-card-title class="navbar white--text">
      <div>
        {{ selectedSprintName }}
      </div>
      <v-spacer></v-spacer>
      <v-menu offset-y close-on-click>
        <template v-slot:activator="{ on }">
          <v-btn dark icon v-on="on" class="icon" height="32">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item 
            v-for="(menuItem, i) in menu" :key="i" 
            @click="menuItem.action"
          >
          <v-list-item-icon>
            <v-icon v-text="menuItem.icon"></v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="menuItem.text"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        </v-list>
      </v-menu>
    </v-card-title>
    <v-card-subtitle class="navbar white--text">
      {{ selectedSprintDateInfo }}
    </v-card-subtitle>
    <v-card-text 
      class="lane-body  flex-column" 
      @drop="moveTask($event)"
      @dragover.prevent
      @dragenter.prevent
    >
      <v-row justify="center"  class="" v-for="task in sprintLaneTask" :key="task.id">
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
    selectedSprintName: "No sprint selected",
    selectedSprintDateInfo: "",
    selectedSprint: {},
    item: 1,
    menu: [
      { text: "Create new sprint", icon: 'mdi-plus-circle-outline', action: "createSprint" },
      { text: "Sprint details", icon: 'mdi-information-outline', action: "showSprintDetails" },
    ],
  }),
  components: {
    Task
  },
  methods:{
    createSprint(){
      console.log("Create Sprint")
    },
    showSprintDetails(){
      console.log("show Sprint detail")
    },
    moveTask(e){
      console.log(e)
      const taskId = e.dataTransfer.getData("task-id");
      const taskName = e.dataTransfer.getData("task-name");
      const taskFeatureId = e.dataTransfer.getData("task-feature-id");
      const fromLane = e.dataTransfer.getData("from-lane");
      const taskNumbering = e.dataTransfer.getData("task-numbering");
      const taskSprintNumber = e.dataTransfer.getData("task-sprint-number");
      // TODO Set Sprint number with selected Sprint
      // TODO Detect, if 
      // - task from PB Lane to Sprint Lane (change Status and Sprint)
      console.log(taskId)
      console.log(taskName)
      console.log(taskFeatureId)
      // TODO
      if(taskSprint !== this.selectedSprint.number){
        // set sprint
        // change status

        // Accept changes (sprint and cards)
        // Update

      }
    }

  },
  computed:{
    ...mapGetters(
      {sprintDetails: "getSprintDetails"}),
    ...mapGetters("task", {
      tasksByIdArray: "byIdArray"
    }),
    sprintLaneTask(){
      if(this.selectedSprint.task_cards === undefined){
        return []
      }
      else{
        return this.tasksByIdArray(this.selectedSprint.task_cards);
      }
    },


  },
  watch:{
    sprintDetails(currentSprint, prevSprint){
      if(currentSprint.id !== prevSprint.id){
        this.selectedSprint = currentSprint;
        this.selectedSprintName = "Sprint " + currentSprint.number;
        this.selectedSprintDateInfo = "(" + currentSprint.start + " to " + currentSprint.end + ")";
      }
    }
  }

}
</script>

<style lang="css" scoped>
  @import "../main.css";
</style>