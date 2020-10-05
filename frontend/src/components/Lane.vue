<template>
  <v-card class="lane" min-width="370" max-width="420" height="80vh">
    <v-card-title class="navbar white--text">
      <div>
        {{ lane.name }}
      </div>
      <v-spacer></v-spacer>
      <v-menu>
        <template v-slot:activator="{ on }">
          <v-btn dark icon v-on="on" class="icon" height="32">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item v-for="(item, i) in items" :key="i">
            <v-list-tile @click="handle_function_call(item.action)">
              <v-list-item-title>
                {{ item.title }}
              </v-list-item-title>
            </v-list-tile>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-card-title>
    <v-layout column>
      <v-flex style="overflow: auto">
        <v-card-text v-if="laneTasks" class="lane-body">
          <v-row v-for="task in laneTasks" :key="task.id">
            <v-col>
              <Task v-bind:task="task" />
            </v-col>
          </v-row>
        </v-card-text>
      </v-flex>
    </v-layout>
  </v-card>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import Task from "@/components/Task.vue";
export default {
  data: () => ({
    items: [
      { title: "+ New Lane", action: undefined },
      { title: "+ New Epic", action: undefined },
      { title: "+ New Feature", action: undefined },
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
  props: ["lane"],
  methods: {
    ...mapActions("task", {
      fetchTask: "fetchList",
      createTask: "create"
    }),
    ...mapActions("feature", {
      fetchFeature: "fetchList",
      createFeature: "create"
    }),
    ...mapActions("epic", {
      fetchEpic: "fetchList",
      createEpic: "create"
    }),
    handle_function_call(function_name) {
      if (function_name === undefined) return;
      this[function_name]();
    },
    fetchData(lane) {
      if (lane.id === undefined) return;
      this.fetchTask({ customUrlFnArgs: { laneId: lane.id } }).then(
        function() {
          this.laneTasks = this.tasksByIdArray(lane.task_cards);
        }.bind(this)
      );
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
        this.createTask({
          data: {
            name: "myTaskCard",
            description: "",
            numbering: 1,
            storypoints: 0,
            lane: this.lane,
            feature: this.feature_cards[0].id
          }
        });
      }
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
        this.createTask({
          data: {
            name: "myTaskCard",
            description: "",
            numbering: 1,
            storypoints: 0,
            lane: this.lane,
            feature: this.feature_cards[0].id
          }
        });
        this.createInProgress = false;
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
  updated() {},
  created() {
    this.fetchData(this.lane);
  }
};
</script>

<style lang="scss" scoped>
</style>