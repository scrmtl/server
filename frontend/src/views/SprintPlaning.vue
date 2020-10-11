<template>
  <v-row>
    <v-col dense v-for="lane in neededPlanningLanes" :key="lane.numbering">
      <Lane v-bind:lane="lane"></Lane>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from 'vuex';
import Lane from "@/components/Lane.vue";
export default {
  data: () => ({

  }),
  components: {
    Lane
  },
  methods:{
    

  },
  computed:{
    ...mapGetters("board", {
      boardByType: "byType"
    }),
    ...mapGetters("lane", {
      laneByName: "byName"
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
    }

    

  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>