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
            @click="createSprint()"
          >
          <v-list-item-icon>
            <v-icon>mdi-plus-circle-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Create new sprint</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item 
            @click="showSprintDetails()"
            :disabled="selectedSprintName==='No sprint selected'"
          >
          <v-list-item-icon>
            <v-icon>mdi-information-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Sprint details</v-list-item-title>
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
import { mapGetters, mapActions } from 'vuex';
export default {
  data: () => ({
    selectedSprintName: "No sprint selected",
    selectedSprintDateInfo: "",
    selectedSprint: {},
    item: 1,
  }),
  components: {
    Task
  },
  methods:{
    ...mapActions("task", {
      fetchSingleTask: "fetchSingle",
      updateTask: "update",
    }),
    ...mapActions("lane", {
      fetchSingleLane: "fetchSingle"
    }),
    ...mapActions("sprint", {
      fetchSingleSprint: "fetchSingle"
    }),
    createSprint(){
      console.log("Create Sprint")
    },
    showSprintDetails(){
      console.log("show Sprint detail")
    },
    moveTask(e){
      const taskId = e.dataTransfer.getData("task-id");
      const taskName = e.dataTransfer.getData("task-name");
      const taskFeatureId = e.dataTransfer.getData("task-feature-id");
      const fromLane = e.dataTransfer.getData("from-lane");
      // const taskNumbering = e.dataTransfer.getData("task-numbering");
      const taskSprintId = e.dataTransfer.getData("task-sprint-id");
      // task from PB Lane to Sprint Lane (change Status and Sprint)
      if(this.selectedSprint.id !== undefined && taskSprintId !== this.selectedSprint.id){
        // set sprint
        // change status
        this.updateTask({
          id: taskId,
          data: {
            name: taskName,
            feature: taskFeatureId,
            lane: fromLane,
            status: "PL",
            sprint: this.selectedSprint.id
          },
          customUrlFnArgs: {}
        })
        .then(()=> {
          // Update From
          this.fetchSingleLane({id: fromLane, customUrlFnArgs: {}})
          // Update Task
          this.fetchSingleTask({id: taskId, customUrlFnArgs: {}})
          // Update Sprint
          if(this.selectedSprint.id != null){
            this.fetchSingleSprint({id: this.selectedSprint.id, customUrlFnArgs: {}})
            .then(()=>{
              this.$store.commit("setSelectedSprintDetail", this.sprintById(this.selectedSprint.id));
            })
          }
          
        })
      }
    }

  },
  computed:{
    ...mapGetters(
      {sprintDetails: "getSprintDetails"}),
    ...mapGetters("sprint", {
      sprintById: "byId",
      listSprint: "list"
    }),
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
    sprintDetails(currentSprint){
      this.selectedSprint = currentSprint;
      this.selectedSprintName = "Sprint " + currentSprint.number;
      this.selectedSprintDateInfo = "(" + currentSprint.start + " to " + currentSprint.end + ")";
    },

  },
  created() {
  }

}
</script>

<style lang="css" scoped>
  @import "../main.css";
</style>