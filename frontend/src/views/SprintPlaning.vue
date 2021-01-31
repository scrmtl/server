<template>
  <v-row justify="center">
    <v-col class="d-flex flex-nowrap overflow-x-auto">
      <div
        class="ma-4"
        v-for="lane in neededPlanningLanes"
        :key="lane.numbering"
      >
        <Lane
          v-bind:lane="lane"
          planningMode
          :allowedAdd="allowedChanges"
        ></Lane>
      </div>
      <div class="ma-4">
        <PokerLane />
      </div>
      <div class="ma-4">
        <SprintLane />
      </div>
      <div class="my-4">
        <v-timeline class="sprint-number-lane">
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
                :color="formatSprintList(sprint).color"
                :class="`${formatSprintList(sprint).text}--text`"
                @click="showSprint(sprint)"
              >
                {{ sprint.number }}
              </v-btn>
            </template>
          </v-timeline-item>
        </v-timeline>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from "vuex";
import Lane from "@/components/Lanes/Lane.vue";
import SprintLane from "@/components/Lanes/SprintLane.vue";
import PokerLane from "@/components/Poker/PokerLane.vue";
export default {
  name: "SprintPlanningView",
  components: {
    Lane,
    SprintLane,
    PokerLane,
  },
  methods: {
    showSprint(sprint) {
      this.$store.commit("selected/setSprintDetail", sprint);
    },

    formatSprintList(sprint) {
      var format = {
        color: "link",
        text: "white",
      };
      switch (sprint.status) {
        // In Planning
        case "IL":
          format.color = "link";
          format.text = "white";
          break;
        // Planned
        case "PL":
          format.color = "primary";
          format.text = "white";
          break;
        // In Progress
        case "IR":
          format.color = "primary";
          format.text = "link";
          break;
        // Done
        case "DO":
          format.color = "secondary";
          format.text = "white";
          break;
        // Accepted
        case "AC":
          format.color = "secondary";
          format.text = "white";
          break;
      }
      return format;
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
      listSprints: "byProjectId",
    }),
    ...mapGetters("projectUser", {
      listProjectUser: "list",
    }),
    ...mapGetters(["getUserinfo"]),

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
      var list = this.listSprints(parseInt(this.$route.params.id));
      var sorted = list.sort(function (a, b) {
        var keyA = a.number;
        var keyB = b.number;
        // Vergleiche ob AC oder AR
        if (keyA > keyB) return -1;
        if (keyA < keyB) return 1;
        return 0;
      });
      return sorted;
    },
    allowedChanges() {
      var allowed = false;
      // role id 1 is always product owner
      var productOwnersInProject = this.listProjectUser.filter(
        (projectUser) =>
          projectUser.role === 1 && projectUser.project == this.$route.params.id
      );
      if (
        this.getUserinfo !== undefined &&
        productOwnersInProject !== undefined
      ) {
        if (
          productOwnersInProject.find(
            (po) => po.plattform_user === this.getUserinfo.userId
          ) !== undefined
        ) {
          allowed = true;
        } else {
          allowed = false;
        }
      }
      return allowed;
    },
  },
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>
