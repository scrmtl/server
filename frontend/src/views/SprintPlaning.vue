<template>
  <v-row justify="center">
    <v-col
      lg="3"
      md="3"
      sm="3"
      dense
      v-for="lane in neededPlanningLanes"
      :key="lane.numbering"
    >
      <Lane v-bind:lane="lane" planningMode allowedAdd></Lane>
    </v-col>
    <v-col lg="2" md="1" sm="1" alignSelf="start">
      <PokerLane />
    </v-col>
    <v-col lg="3" md="3" sm="3">
      <SprintLane />
    </v-col>
    <v-col lg="1" md="1" sm="1">
      <v-timeline>
        <v-timeline-item
          v-for="sprint in sortedSprintList"
          :key="`${sprint.number}-sprint`"
          small
          fill-dot
        >
          <template v-slot:icon>
            <v-btn
              fab
              small
              color="link"
              class="white--text"
              @click="showSprint(sprint)"
            >
              {{ sprint.number }}
            </v-btn>
          </template>
        </v-timeline-item>
      </v-timeline>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from "vuex";
import Lane from "@/components/Lane.vue";
import SprintLane from "@/components/Sprint/SprintLane.vue";
import PokerLane from "@/components/Sprint/PokerLane.vue";
export default {
  components: {
    Lane,
    SprintLane,
    PokerLane,
  },
  methods: {
    showSprint(sprint) {
      this.$store.commit("selected/setSprintDetail", sprint);
    },
  },
  computed: {
    ...mapGetters("task", {
      tasksByIdArray: "byIdArray",
    }),
    ...mapGetters("lane", {
      laneByName: "byName",
    }),
    ...mapGetters("sprint", {
      listSprints: "list",
    }),

    neededPlanningLanes() {
      var lanes = [];
      var growningLane = this.laneByName("Growning (for Refinement)");
      var readyLane = this.laneByName("Ready (for next Sprints)");
      if (growningLane.length > 0 && readyLane.length > 0) {
        lanes.push(growningLane.shift());
        lanes.push(readyLane.shift());
      }
      return lanes;
    },

    sortedSprintList() {
      var list = this.listSprints;
      var sorted = list.sort(function (a, b) {
        var keyA = a.number;
        var keyB = b.number;
        // Vergleiche ob AC oder AR
        if (keyA < keyB) return -1;
        if (keyA > keyB) return 1;
        return 0;
      });
      return sorted;
    },
  },
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>