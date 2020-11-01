<template>
  <v-card min-width="385" max-width="420">
    <v-card-title class="navbar white--text">
      <div>
        <v-icon v-if="planningMode" color="link" class="mb-1 mx-1">mdi-link</v-icon>
        {{ lane.name }}
      </div>
      <v-spacer></v-spacer>
      <v-menu offset-y close-on-click>
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
          class="lane-body  flex-column" 
          v-if="laneTasks"
          @drop="moveTask($event)"
          @dragover.prevent
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
    items: [
      { title: "+ New Task", action: "createEmptyTask" }
    ],
    epicItem: [{ title: "+ New Feature" }, { title: "+ New Task" }],
    featureItem: [{ title: "+ New Task" }],
    laneTasks: [],
    laneEpics: [],
    laneFeature: [],
    createInProgress: false
  }),
  components: {
    Task
  },
  props: {
    lane: {},
    planningMode: { type: Boolean, default: false },
  },
  methods: {
    ...mapActions("task", {
      fetchTask: "fetchList",
      fetchSingleTask: "fetchSingle",
      createTask: "create",
      updateTask: "update",
    }),
    ...mapActions("feature", {
      fetchFeature: "fetchList",
      createFeature: "create"
    }),
    ...mapActions("epic", {
      fetchEpic: "fetchList",
      createEpic: "create"
    }),
    ...mapActions("lane", {
      fetchSingleLane: "fetchSingle"
    }),
    handle_function_call(function_name) {
      if (function_name === undefined) return;
      this[function_name]();
    },
    fetchData(lane) {
      if (lane.id === undefined) return;
      this.laneTasks = this.tasksByIdArray(lane.task_cards);
      // this.fetchTask({ customUrlFnArgs: { laneId: lane.id } }).then(
      //   function() {
      //     this.laneTasks = this.tasksByIdArray(lane.task_cards);
      //   }.bind(this)
      // );
      this.fetchEpic({ customUrlFnArgs: { laneId: lane.id } }).then(
        function() {
          this.laneEpics = this.epicsByIdArray(lane.epic_cards);
        }.bind(this)
      );
      this.fetchFeature({ customUrlFnArgs: { laneId: lane.id } }).then(
        function() {
          this.laneFeature = this.featuresByIdArray(lane.feature_cards);
        }.bind(this)
      );
    },
    createEmptyTask() {
      this.helperFunctionGetFeatureId();
    },
    helperFunctionGetFeatureId() {
      //If no Epics then create one
      if (this.lane.id === undefined) return;
      if (this.laneEpics.length <= 0) {
        this.createInProgress = true;
        this.createEpic({
          customUrlFnArgs: {},
          data: {
            name: "DefaultEpic",
            description: "",
            numbering: 0,
            status: "NS",
            lane: this.lane.id
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
                lane: this.lane.id,
                epic: value.data.id
              }
            }).then(
              function() {
                this.fetchData(this.lane);
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
            lane: this.lane.id,
            epic: this.laneEpics[0].id
          }
        }).then(
          function() {
            this.fetchData(this.lane);
          }.bind(this)
        );
      } else {
        this.createTaskHelper(this.lane.id);
      }
    },
    createTaskHelper(laneId) {
      this.$store.commit("showTaskDetail", true);
      var task = {
        lane: laneId,
        feature: this.laneFeature[0].id
      };
      this.$store.commit("setSelectedTaskDetail", task);
      /*
      this.createTask({
        data: {
          name: "myTaskCard",
          description: "",
          numbering: 1,
          storypoints: 0,
          lane: laneId,
          feature: this.laneFeature[0].id
        },
        customUrlFnArgs: {}
      }).then(
        function(value) {
          if (!(value.data.id === undefined)) {
            this.fetchSingleTask({
              id: value.data.id,
              customUrlFnArgs: {}
            }).then(
              function(value) {
                if (!(value.data.id === undefined)) {
                  this.laneTasks.push(this.tasksById(value.data.id));
                }
              }.bind(this)
            );
          }
        }.bind(this)
      );
      
      */
      this.createInProgress = false;
    },
    moveTask(e){
      console.log(e)
      const taskId = e.dataTransfer.getData("task-id");
      const taskName = e.dataTransfer.getData("task-name");
      const taskFeatureId = e.dataTransfer.getData("task-feature-id");
      //const fromLane = e.dataTransfer.getData("from-lane")
      const taskNumbering = e.dataTransfer.getData("task-numbering")
      console.log(taskId)
      this.updateTask({
        id: taskId,
        data: {
          lane: this.lane.id,
          name: taskName,
          feature: taskFeatureId,
          numbering: taskNumbering
        },
        customUrlFnArgs: {}
      })
      .then(() => {
          this.fetchSingleLane({id: this.lane.id}).then(() => {
            this.laneTasks = this.tasksByIdArray(this.lane.task_cards);
          })
      })
      .catch((error) => {
        console.log(error)
        // if(error.response.data.non_field_errors.length > 0){
        //   this.$store.commit("showSystemAlert", {message: error.response.data.non_field_errors[error.response.data.non_field_errors.length - 1], category: "error"});
        // }
      })
    }    
  },

  watch: {
    lane(currentLane, prevLane) {
      if ((currentLane === undefined) | (prevLane.id === currentLane.id))
        return;
      this.fetchData(currentLane);
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
    })
  },

  created() {
    this.fetchData(this.lane);
  },

  updated() {

  },
  
};
</script>

<style lang="css" scoped>
  @import "../main.css";
</style>