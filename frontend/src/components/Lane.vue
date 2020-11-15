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
    items: [{ title: "+ New Task", action: "createEmptyTask" }],
    epicItem: [{ title: "+ New Feature" }, { title: "+ New Task" }],
    featureItem: [{ title: "+ New Task" }],
    laneTasks: [],
    laneEpics: [],
    laneFeature: [],
    localLane: Object,
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
    ...mapActions("lane", {
      fetchSingleLane: "fetchSingle"
    }),
    handle_function_call(function_name) {
      if (function_name === undefined) return;
      this[function_name]();
    },
    fetchData(lane, isNewTaskCreate = false) {
      if (lane.id === undefined) return;
      this.laneTasks = this.tasksByIdArray(lane.task_cards);
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
      this.$store.commit("showTaskDetail", true);
      var task = {
        lane: laneId,
        feature: this.laneFeature[0].id
      };
      this.$store.commit("setSelectedTaskDetail", task);
      this.createInProgress = false;
    },
    moveTask(e){
      console.log(e)
      const taskId = e.dataTransfer.getData("task-id");
      const taskName = e.dataTransfer.getData("task-name");
      const taskFeatureId = e.dataTransfer.getData("task-feature-id");
      const fromLane = e.dataTransfer.getData("from-lane");
      const taskNumbering = e.dataTransfer.getData("task-numbering");
      // TODO
      console.log(taskId)
      console.log(taskName)
      console.log(taskFeatureId)
      console.log(fromLane)
      console.log(taskNumbering)
    }    
  },

  watch: {
    lane(currentLane, prevLane) {
      if ((currentLane === undefined) | (prevLane.id === currentLane.id))
        return;
      this.localLane = currentLane;
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
    }),
    ...mapGetters("lane", {
      laneById: "byId"
    })
  },

  created() {
    this.fetchData(this.lane);
    this.localLane = this.lane;
  }
};
</script>

<style lang="css" scoped>
  @import "../main.css";
</style>