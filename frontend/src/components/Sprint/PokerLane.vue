<template>
<v-card class="primary" min-width="300" max-width="400">
  <v-card-title class="white--text">
      Gromming
    </v-card-title>
    <v-card-subtitle class="white--text">
      Planning Poker
    </v-card-subtitle>
    <v-card-text class="overflow-y-auto" style="height: calc(95vh - 355px)">
      <v-row align="center">
        <v-col cols="12">
          <v-sheet
            color="secondary"
            height="100"
            @drop="addPoker($event)"
            @dragover="allowDrop($event)"
            @dragenter.prevent
            class="text-body-2 white--text d-flex justify-center align-center"
          >
          <v-icon color="white">mdi-download</v-icon>
          <span>Drop card here to vote them</span>
          </v-sheet>
        </v-col>
      </v-row>
      <v-row>
        <v-subheader class="white--text text-body-1">Cards to vote</v-subheader>
        <v-list two-line class="transparent overflow-y-auto" style="max-height: calc(65vh - 225px)">
          <v-list-item v-for="item in voteCards" :key="item.id">
          <v-list-item-content>
            <v-list-item-title class="white--text">#{{item.id}}: {{item.name}}</v-list-item-title>
            <v-list-item-subtitle class="white--text">Storypoints: {{item.storypoints}}</v-list-item-subtitle>
          </v-list-item-content>
          <v-list-item-action>
            <v-btn icon>
              <v-icon color="white" @click="removePoker(item)">mdi-close-circle</v-icon>
            </v-btn>
          </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-row>
    </v-card-text>
    <v-card-subtitle class="white--text text-body-1">
      Start Poker
    </v-card-subtitle>
    <v-card-actions>
      <v-btn outlined color="link">Poker Sync</v-btn>
      <v-spacer></v-spacer>
      <v-btn outlined color="link">Poker Async</v-btn>
    </v-card-actions>
</v-card>
  
</template>

<script>
import { mapFields } from "vuex-map-fields";
export default {
  name: "PokerLane",
  data: () =>({

  }),
  computed: {
    // See more under Two-way Computed Property https://vuex.vuejs.org/guide/forms.html
    // Implementation with https://github.com/maoberlehner/vuex-map-fields
    // the string after the last dot (e.g. `id`) is used
    // for defining the name of the computed property.
    ...mapFields("poker", ["voteCards"]),

  },
  methods: {
    allowDrop(e){
      const sprintStatus = e.dataTransfer.getData("task-status");
      // poker is only in new or planned task status allowed
      if(sprintStatus === "NW" || sprintStatus === "PL"){
        e.preventDefault();
        return true; 
      }
      else{
        return false;
      }
    },
    addPoker(e){
      const taskId = e.dataTransfer.getData("task-id");
      const taskName = e.dataTransfer.getData("task-name");
      // const taskFeatureId = e.dataTransfer.getData("task-feature-id");
      // const taskSprintId = e.dataTransfer.getData("task-sprint-id");
      // const taskSprintStatus = e.dataTransfer.getData("task-sprint-status");
      const taskStorypoints = e.dataTransfer.getData("task-storypoints");
      if(this.voteCards.findIndex(item => item.id == taskId) == -1){
        this.$store.commit("poker/addCardToVote", {cardName: taskName , cardId: taskId, cardStorypoints: taskStorypoints});
      }
      else{
        this.$store.commit("showSystemAlert", {
        message: "Card is already added in poker",
        category: "warning"
        });
      }
      
    },
    removePoker(vote){
      this.$store.commit("poker/removeCardToVote", vote.id);
    }

  }
}
</script>

<style lang="css" scoped>
  @import "../../main.css";
</style>