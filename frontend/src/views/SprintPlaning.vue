<template>
  <v-row>
    <v-col dense v-for="lane in neededPlanningLanes" :key="lane.numbering">
      <Lane v-bind:lane="lane" planningMode></Lane>
    </v-col>
    <v-col>

    </v-col>
    <v-col>
      <SprintLane />
    </v-col>
    <v-col>
      <v-timeline>
        <v-timeline-item
          v-for="sprint in listSprints" :key="sprint.number"
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
              {{sprint.number}}
            </v-btn>
          </template>
        </v-timeline-item>
      </v-timeline>
    </v-col>
    <v-col>

    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from 'vuex';
import Lane from "@/components/Lane.vue";
import SprintLane from "@/components/SprintLane.vue";
export default {
  components: {
    Lane,
    SprintLane
  },
  methods:{
    showSprint(sprint) {
      this.$store.commit("setSelectedSprintDetail", sprint);
    },

  },
  computed:{
    ...mapGetters("task", {
      tasksByIdArray: "byIdArray"
    }),
    ...mapGetters("lane", {
      laneByName: "byName"
    }),
    ...mapGetters("sprint", {
      listSprints: "list"
    }),

    neededPlanningLanes(){
      var lanes = [];
      var growningLane = this.laneByName("Growning (for Refinement)");
      var readyLane = this.laneByName("Ready (for next Sprints)");
      if(growningLane.length > 0 && readyLane.length > 0){
        lanes.push(growningLane.shift());
        lanes.push(readyLane.shift());
      }
      return lanes;
    },
  }
};
</script>

<style lang="css" scoped>
  @import "../main.css";
</style>