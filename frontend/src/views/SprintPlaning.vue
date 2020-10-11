<template>
  <v-row>
    <v-col dense v-for="lane in neededPlanningLanes" :key="lane.numbering">
      <Lane v-bind:lane="lane"></Lane>
    </v-col>
    <v-col>

    </v-col>
    <v-col>
      <v-card min-width="385" max-width="420">
        <v-card-title class="navbar white--text"> {{ selectedSprintName }}</v-card-title>
        <v-card-text class="lane-body  flex-column" v-if="sprintLaneTask" >
          <v-row justify="center"  class="" v-for="task in sprintLaneTask" :key="task.id">
            <Task v-bind:task="task" />
          </v-row>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col>
      
      <v-timeline>
        <v-timeline-item
          small
          fill-dot
          color="tabbody"
        >
          <template v-slot:icon>
            <v-btn fab small icon color="link" >
              <v-icon>mdi-plus-circle-outline</v-icon>
            </v-btn>
          </template>
        </v-timeline-item>
        
        <v-timeline-item
          v-for="sprint in listSprints" :key="sprint.number"
          small
          fill-dot
          
        >
          <template v-slot:icon>
            <v-btn fab small color="link" class="white--text" >{{sprint.number}}</v-btn>
            
          </template>

        </v-timeline-item>

      </v-timeline>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from 'vuex';
import Lane from "@/components/Lane.vue";
export default {
  data: () => ({
    selectedSprintName: "No sprint selected"
  }),
  components: {
    Lane
  },
  methods:{
    

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

    sprintLaneTask(){
      return [];
    }

    

  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>