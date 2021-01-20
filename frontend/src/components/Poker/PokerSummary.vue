<template>
<div>
  <v-card class="primary" >
    <v-card-title class="white--text">
      Planning Poker
    </v-card-title>
    <v-card-subtitle class="white--text">
      Summary
    </v-card-subtitle>
    <v-card-text class="overflow-y-auto" style="height: calc(100vh - 365px)">
      <v-row align="center">
        <v-col cols="6">
          <v-progress-circular
            class="mx-16"
            :rotate="-90"
            :size="100"
            :width="15"
            :value="storypointsInPercent"
            color="link"
          >{{selectedPokerVote.act_storypoints || 0}} SP </v-progress-circular>
        </v-col>
        <v-col cols="6">
          <v-row dense>
              <v-text-field
                :value="pokerVoting.mode"
                label="Poker Mode"
                dense
                dark
                outlined
                readonly
                disabled
              ></v-text-field>
          </v-row>
          <v-row dense>
            <v-text-field
              :value="pokerNamedStatus"
              label="Status"
              dense
              dark
              outlined
              readonly
              disabled
            ></v-text-field>
          </v-row>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col cols="6">
          <v-text-field
            v-model="votedPlayer"
            label="Voted"
            dense
            dark
            outlined
            readonly
            disabled
            suffix="Players"
          ></v-text-field>
        </v-col>
        <v-col cols="6">
          <v-text-field
            :value="selectedPokerVote.avg_storypoints || '-'"
            label="Avg. Story Points"
            dense
            dark
            outlined
            readonly
            disabled
            suffix="SP"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-list class="transparent overflow-y-auto" style="max-height: calc(75vh - 225px)">
          <v-list-item
            v-for="player in players"
            :key="player.name"
          >
            <v-list-item-icon >
              <v-icon :color="player.color">mdi-account</v-icon>
            </v-list-item-icon>
            <v-list-item-title :class="`${player.color}--text`">{{ player.name }}</v-list-item-title>
            <v-list-item-subtitle :class="`${player.color}--text text-right` ">
              {{ player.storypoints }}
            </v-list-item-subtitle>
          </v-list-item>
        </v-list>
        </v-col>
      </v-row>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions>
      <!-- Async Modus -->
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            v-if="pokerVoting.mode === 'ASYNC'"
            outlined
            color="link"
            v-bind="attrs"
            v-on="on"
            @click="acceptAsyncVote()"
          >Accept</v-btn>
        </template>
        <span>Accept voted storypoints and close vote</span>
      </v-tooltip>
      <v-spacer></v-spacer>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn 
            outlined
            color="link"
            v-bind="attrs"
            v-on="on"
            @click="skipAsyncVote()"
          >Skip</v-btn>
        </template>
        <span>Skipped and close vote</span>
      </v-tooltip>
      <v-spacer></v-spacer>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn 
            v-if="pokerVoting.mode === 'ASYNC'"
            outlined
            color="link"
            v-bind="attrs"
            v-on="on"
            @click="discardDialog = true"
          >Discard</v-btn>
        </template>
        <span>Discard voted storypoints and close vote. In a next step choose storypoints by your own</span>
      </v-tooltip>
      <!-- Sync Modus -->
      <v-btn
        v-if="pokerVoting.mode === 'SYNC'"
        outlined 
        color="link"
      >Next</v-btn>
    </v-card-actions>
  </v-card>
  <!-- discard Dialog -->
  <v-dialog
    v-model="discardDialog"
    persistent
    class="mx-auto"
    width="600"
    dark
  >
    <v-card color="tabbody" shaped>
      <v-card-text>
        <v-row>
          <span class="ml-12 headline pt-10">Do you want discard the voted storypoints?</span>
        </v-row>
        <v-row>
          <span class="ml-12 my-2 subtitle pt-8">Please choose the storypoints, first</span>
        </v-row>

        <v-row>
          <v-autocomplete
            class="mx-16"
            v-model="selectedStorypoints"
            :items="availableStorypoints"
            outlined
            dense
          ></v-autocomplete>
        </v-row>
      </v-card-text>
      <v-card-actions class="ml-10 pb-10 pt-10">
        <v-btn 
          width="250" 
          outlined 
          color="error"
          :disabled="selectedStorypoints === 0"
          @click="discardAsyncVote()"
          >Yes</v-btn
        >
        <v-btn
          width="250"
          outlined
          @click="discardDialog = false"
          >No</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "PokerSummary",
  props: ["selectedPokerVote"],
  data: () => ({
    discardDialog: false,
    selectedStorypoints: 0,
    availableStorypoints: [0, 1, 2, 3, 5, 8, 13, 21, 34, 55]
  }),
  computed: {
    ...mapGetters("vote", {
      voteById: "byPokerVoteId"
    }),
    ...mapGetters("user", {
      plattformUserById: "byId"
    }),
    ...mapGetters("pokerVoting", {
      pokerVotingById: "byId"
    }),
    storypointsInPercent(){
      return Math.round((this.selectedPokerVote.act_storypoints/55)*100)
    },
    votedPlayer(){
      return this.voteById(this.selectedPokerVote.id).length;
    },
    players(){
      var votes = this.voteById(this.selectedPokerVote.id);
      var voter = []
      if(votes.length > 0){
        votes.forEach(vote => {
          var user = this.plattformUserById(vote.user);
          voter.push({
            name: user.name + ` (${user.username})`,
            storypoints: vote.storypoints,
            color: "white"
          })  
        });
      }
      return voter;
    },
    pokerNamedStatus(){
      var namedStatus = "-";
      switch(this.selectedPokerVote.status){
        case "NS":
          namedStatus = "Not started";
          break;
        case "WAIT":
          namedStatus = "Waiting for vote";
          break;
        case "SKIP":
          namedStatus = "Skipped";
          break;
        case "FIN":
          namedStatus = "Voted";
          break;
      };
      return namedStatus;
    },
    pokerVoting(){
      if(this.selectedPokerVote !== null){
        var pokerVoting = this.pokerVotingById(this.selectedPokerVote.poker_voting);
        return pokerVoting;
      }
      else{
        return null;
      }
    }
  },
  methods: {
    acceptAsyncVote(){
      // TODO
    },
    skipAsyncVote(){
      // TODO
    },
    discardAsyncVote(){
      console.log(this.selectedStorypoints);
      // TODO
    }
  }
};
</script>

<style lang="css" scoped>
@import "../../main.css";
</style>
