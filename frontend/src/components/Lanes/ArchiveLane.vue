<template>
  <v-card min-width="385" max-width="420">
    <v-card-title class="blue-grey darken-2 white--text">
      {{ laneName }}
      <v-spacer></v-spacer>
      <v-btn dark icon class="icon" height="32" @click="showSprintDetails()">
        <v-icon>mdi-information-outline</v-icon>
      </v-btn>
    </v-card-title>
    <v-card-subtitle class="blue-grey darken-2 white--text">
      {{ laneMetaData }}
    </v-card-subtitle>
    <v-card-text class="blue-grey darken-2 flex-column">
      <v-row justify="center" class="" v-for="task in laneTask" :key="task.id">
        <Task v-bind:task="task" />
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import Task from "@/components/Task.vue";
import { mapGetters } from "vuex";
export default {
  data: () => ({}),
  components: {
    Task,
  },
  props: {
    lane: {},
  },
  computed: {
    ...mapGetters("task", {
      tasksByIdArray: "byIdArray",
    }),
    ...mapGetters("sprint", {
      sprintById: "byId",
    }),
    laneName() {
      var startIndex = this.lane.name.indexOf(",", 0);
      var endIndex = this.lane.name.indexOf(":", 0);
      return this.lane.name.substring(startIndex + 1, endIndex);
    },
    laneMetaData() {
      var startIndex = this.lane.name.indexOf(":", 0);
      return this.lane.name.substring(startIndex + 1, this.lane.name.length);
    },
    sprint() {
      var endIndex = this.lane.name.indexOf(",", 0);
      var sprintId = this.lane.name.substring(0, endIndex);
      return this.sprintById(parseInt(sprintId));
    },

    laneTask() {
      return this.tasksByIdArray(this.lane.task_cards);
    },
  },
  methods: {
    showSprintDetails() {
      this.$store.commit("selected/setSprintDetail", this.sprint);
      this.$store.commit("selected/showSprintDetailWithReadOnly");
    },
  },
};
</script>

<style>
</style>