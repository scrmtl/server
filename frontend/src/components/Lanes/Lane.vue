<template>
  <v-card min-width="385" max-width="420">
    <v-card-title class="navbar white--text">
      <div>
        <v-icon v-if="planningMode" color="link" class="mb-1 mx-1">mdi-link</v-icon>
        {{ lane.name }}
      </div>
      <v-spacer></v-spacer>
      <v-menu offset-y close-on-click v-if="allowedAdd">
        <template v-slot:activator="{ on }">
          <v-btn dark icon v-on="on" class="icon" height="32">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item v-for="(item, i) in items" :key="i" link>
            <v-list-item-title @click="handle_function_call(item.action)">
              {{ item.title }}
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-card-title>
        <v-card-text 
          class="lane-body flex-column" 
          v-if="laneTasks"
          @drop="moveTask($event)"
          @dragover="allowDrop($event)"
          @dragenter.prevent
        >
          <v-row 
            justify="center" 
            v-for="task in laneTasks" :key="task.id"   
          >
            <Task v-bind:task="task" />
          </v-row>        
        </v-card-text>
  </v-card>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import Task from "@/components/Task.vue";
export default {
  data: () => ({
    items: [{ title: "+ New Task", action: "createEmptyTask" }],
    epicItem: [{ title: "+ New Feature" }, { title: "+ New Task" }],
    featureItem: [{ title: "+ New Task" }],
    laneFeature: [],
    laneEpics: [],  
    localLane: Object,
    createInProgress: false
  }),
  components: {
    Task
  },
  props: {
    lane: {},
    allowedAdd: { type: Boolean, default: false },
    planningMode: { type: Boolean, default: false }
  },
  methods: {
    ...mapActions("task", {
      fetchTask: "fetchList",
      fetchSingleTask: "fetchSingle",
      createTask: "create",
      updateTask: "update",
    }),
    ...mapActions("lane", {
      fetchSingleLane: "fetchSingle"
    }),
    ...mapActions("feature", {
      fetchFeature: "fetchList",
      createFeature: "create"
    }),
    ...mapActions("epic", {
      fetchEpic: "fetchList",
      createEpic: "create"
    }),
    ...mapActions("sprint", {
      fetchSingleSprint: "fetchSingle"
    }),
    handle_function_call(function_name) {
      if (function_name === undefined) return;
      this[function_name]();
    },
    fetchData(lane, isNewTaskCreate = false) {
      if (lane.id === undefined) return;
      this.fetchSingleLane({ id: lane.id, customUrlFnArgs: {} }).then(
        function() {
          this.localLane = this.laneById(this.localLane.id);
          this.fetchEpic({
            customUrlFnArgs: { laneId: this.localLane.id }
          }).then(
            function() {
              this.laneEpics = this.epicsByIdArray(this.localLane.epic_cards);
            }.bind(this)
          );
          this.fetchFeature({
            customUrlFnArgs: { laneId: this.localLane.id }
          }).then(
            function() {
              this.laneFeature = this.featuresByIdArray(
                this.localLane.feature_cards
              );
              if (isNewTaskCreate) {
                this.createTaskHelper(this.localLane.id);
              }
            }.bind(this)
          );
        }.bind(this)
      );
    },
    createEmptyTask() {
      this.helperFunctionGetFeatureId();
    },
    helperFunctionGetFeatureId() {
      //If no Epics then create one
      if (this.localLane.id === undefined) return;
      if (this.laneEpics.length <= 0) {
        this.createInProgress = true;
        this.createEpic({
          customUrlFnArgs: {},
          data: {
            name: "DefaultEpic",
            description: "",
            numbering: 0,
            status: "NS",
            lane: this.localLane.id
          }
        }).then(
          function(value) {
            this.createFeature({
              customUrlFnArgs: {},
              data: {
                name: "DefaultFeature",
                description: "",
                numbering: 0,
                status: "NS",
                lane: this.localLane.id,
                epic: value.data.id
              }
            }).then(
              function() {
                this.fetchData(this.localLane, true);
              }.bind(this)
            );
          }.bind(this)
        );
      } else if (this.laneFeature.length <= 0) {
        this.createInProgress = true;
        this.createFeature({
          customUrlFnArgs: {},
          data: {
            name: "DefaultFeature",
            description: "",
            numbering: 0,
            status: "NS",
            lane: this.localLane.id,
            epic: this.laneEpics[0].id
          }
        }).then(
          function() {
            this.fetchData(this.localLane);
          }.bind(this)
        );
      } else {
        this.createTaskHelper(this.localLane.id);
      }
    },
    createTaskHelper(laneId) {
      this.$store.commit("selected/showTaskDetail", true);
      var task = {
        name: "",
        description: "",
        storypoints: 0,
        lane: laneId,
        feature: this.laneFeature[0].id
      };
      this.$store.commit("selected/setTaskDetail", task);
      this.createInProgress = false;
    },

    allowDrop(e){
      const sprintStatus = e.dataTransfer.getData("task-sprint-status");
      if(this.planningMode && sprintStatus !== "IL"){
        return false;
      }
      else{
        e.preventDefault();
        return true;
      }

    },

    moveTask(e){
      const taskId = e.dataTransfer.getData("task-id");
      const taskName = e.dataTransfer.getData("task-name");
      const taskFeatureId = e.dataTransfer.getData("task-feature-id");
      const fromLane = e.dataTransfer.getData("from-lane");
      // const taskNumbering = e.dataTransfer.getData("task-numbering");
      const taskSprintId = e.dataTransfer.getData("task-sprint-id");
      // In planning mode
      if(this.planningMode && taskSprintId !== null){
        // task from Sprint Lane to PB Lane (change Status and Sprint)
        // delete sprint in card (null)
        // change lane
        // change status
        this.updateTask({
          id: taskId,
          data: {
            name: taskName,
            feature: taskFeatureId,
            lane: this.localLane.id,
            sprint: null,
            status: "NW"            
          },
          customUrlFnArgs: {}
        })
        .then(()=> {
          // Update From
          this.fetchSingleLane({id: fromLane, customUrlFnArgs: {}})
          // Update To
          this.fetchSingleLane({id: this.localLane.id, customUrlFnArgs: {}})
          // Update Task
          this.fetchSingleTask({id: taskId, customUrlFnArgs: {}})
          // Update Sprint
          if(taskSprintId !== "null"){
            this.fetchSingleSprint({id: taskSprintId, customUrlFnArgs: {}})
            .then((res)=>{
              if(res.status === 200){
                this.$store.commit("selected/setSprintDetail", res.data);
              }
            })
          }
        })        
      }
      else{
        if(fromLane != this.localLane.id){
          // change lane
          var localData = {
            name: taskName,
            feature: taskFeatureId,
            lane: this.localLane.id,
          }
          // change status (in certainly lanes)
          switch (this.localLane.name) {
            case "Doing":
              localData.status ="IP"
              break;
            case "Done":
              localData.status ="DO"
              break;
            case "Next (Sprint Backlog)":
              localData.status ="NS"
              break;
            case "Ready (for Review)":
              localData.status ="IP"
              break;     
          }
          // Accept changes
          this.updateTask({
            id: taskId,
            data: localData,
            customUrlFnArgs: {}
          })
          .then(()=> {         
            // Update From
            this.fetchSingleLane({id: fromLane, customUrlFnArgs: {}})
            // Update To
            this.fetchSingleLane({id: this.localLane.id, customUrlFnArgs: {}})
            // Update Task
            this.fetchSingleTask({id: taskId, customUrlFnArgs: {}})    
          })
        } 
      }
    }    
  },

  watch: {
    lane(currentLane, prevLane) {
      // performance increase, if lane already loaded
      if ((currentLane === undefined)){
        return;
      }
      // fetch, if add or remove cards in task_cards
      if(currentLane.task_cards.length !== prevLane.task_cards.length){
        this.localLane = currentLane;
        this.fetchData(currentLane); 
      }  
    },

    laneFeature(currentLane, prevLane) {
      if (this.createInProgress & !(currentLane.length === prevLane.length)) {
        this.createTaskHelper(currentLane.id);
      }
    }
  },
  computed: {
    ...mapGetters("task", {
      tasksById: "byId",
      tasksByIdArray: "byIdArray"
    }),
    ...mapGetters("feature", {
      featuresById: "byId",
      featuresByIdArray: "byIdArray"
    }),
    ...mapGetters("epic", {
      epicsById: "byId",
      epicsByIdArray: "byIdArray"
    }),
    ...mapGetters("lane", {
      laneById: "byId"
    }),
    laneTasks(){
      // Lane in Planning Mode
      if(this.planningMode){
        // Filter cards in lane, if lane in planning mode
        // Show cards, they not planned in Sprint
        return this.tasksByIdArray(this.localLane.task_cards).filter(card => card.sprint === null)
      }
      else{
        // Show all cards in lane
        return this.tasksByIdArray(this.localLane.task_cards);
      }
      
    }
  },

  created() {
    this.fetchData(this.lane);
    this.localLane = this.lane;
  }
};
</script>

<style lang="css" scoped>
  @import "../../main.css";
</style>