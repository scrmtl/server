<template>
  <v-card class="primary" >
    <v-card-title class="white--text">
      Planning Poker
    </v-card-title>
    <v-card-subtitle class="white--text">
      Summary
    </v-card-subtitle>
    <v-card-text class="overflow-y-auto" style="height: calc(100vh - 365px)">
      <v-row align="center">
        <v-col cols="auto">
          <v-progress-circular
            :rotate="-90"
            :size="100"
            :width="15"
            :value="13"
            color="link"
          >{{selectedPokerVote.end_storypoints || 0}} SP </v-progress-circular>
        </v-col>
        <v-col cols="auto">
          <v-text-field
            :value="selectedPokerVote.status || '-'"
            label="Poker Modus"
            dense
            dark
            outlined
            readonly
            disabled
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row dense justify="center" >
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
      <v-btn outlined color="link">Next</v-btn>
      <v-btn outlined color="link">Skip</v-btn>
      <v-btn outlined color="link">End</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "PokerSummary",
  props: ["selectedPokerVote"],
  data: () => ({
    
  }),
  computed: {
    ...mapGetters("vote", {
      voteById: "byPokerVoteId"
    }),
    ...mapGetters("user", {
      plattformUserById: "byId"
    }),
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
    }
  },
  methods: {

  }
}
</script>

<style lang="css" scoped>
  @import "../../main.css";
</style>