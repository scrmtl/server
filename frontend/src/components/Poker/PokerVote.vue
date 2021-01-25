<template>
<v-expansion-panel
  class="primary"
  @click="selectPokerVote()"
> 
  <v-expansion-panel-header disable-icon-rotate>
    <v-row no-gutters >
      <v-col cols="11"  class="my-1">
        {{taskName}}
      </v-col>
      <v-col cols="1">
        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-icon 
              v-if="voteStatus === 'VOTED'" 
              color="teal"
              v-bind="attrs"
              v-on="on"
            >
              mdi-check
            </v-icon>
            <v-icon 
              v-else-if="voteStatus ==='SKIP'"
              color="teal"
              v-bind="attrs"
              v-on="on"
            >
              mdi-skipped-next-outline
            </v-icon>
            <v-icon
              v-else-if="voteStatus ==='ABSTENTION'"
              color="teal"
              v-bind="attrs"
              v-on="on"
            >
              mdi-help-circle-outline
            </v-icon>
            <v-icon 
              v-else
              color="error"
              v-bind="attrs"
              v-on="on"
            >
              mdi-alert-circle-outline
            </v-icon>
          </template>
          <span v-if="voteStatus === 'VOTED'">Your storypoints have been submitted</span>
          <span v-else-if="voteStatus ==='SKIP'">Vote was skipped</span>
          <span v-else-if="voteStatus ==='ABSTENTION'">You abstained</span>
          <span v-else>Vote still open</span>
        </v-tooltip>
       
      </v-col>
    </v-row>
  </v-expansion-panel-header>
  <v-expansion-panel-content>
    <v-row no-gutters justify="start">
        <v-col>
          <v-row class="ma-2 mb-4">
            {{taskDescription || "No Description"}}
          </v-row>
          <v-row class="ma-2">
            <v-btn
              text
              color="white"
              outlined
              @click="showTaskDetails()"
            >
              More Details
            </v-btn>
          </v-row>
        </v-col>
        <v-divider
          vertical
          class="mx-4"
        ></v-divider>
        <v-col>
          <v-row >
            <v-col>
              <v-autocomplete
                :value="votedStorypoints"
                @input="updateSelectedStorypoints"
                :items="availableStorypoints"
                :disabled="voteStatus !== 'WAIT'"
                outlined
                dense
                label="Story points"
              ></v-autocomplete>
            </v-col>
          </v-row>
          <v-spacer></v-spacer>
          <v-row >
            <v-col>
              <v-btn
                text
                :disabled="voteStatus !== 'WAIT'"
                outlined
                color="white"
                @click="skipVote()"
              >
                Skip
              </v-btn>
            </v-col>
          </v-row>
          <v-row >
            <v-col >
              <v-btn
                text
                :disabled="voteStatus !== 'WAIT'"
                outlined
                color="link"
                @click="sendVote()"
              >
                Send vote
              </v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
  </v-expansion-panel-content>
</v-expansion-panel> 
</template>

<script>
import { mapFields } from "vuex-map-fields";
import { mapGetters, mapActions } from "vuex";
export default {
  name: "PokerVote",
  props: ["pokerVote"],
  data: () => ({
    selectedStorypoints: 0,
    status: "",
    availableStorypoints: [0, 1, 2, 3, 5, 8, 13, 21, 34, 55]
  }),
  computed:{
    ...mapFields([
      "Userinfo.userId"
    ]),
    ...mapGetters("task", {
      taskById: "byId"
    }),
    ...mapGetters("vote", {
      listVotes: "list",
      voteByIds: "byPokerVoteIdAndUserId"
    }),
    task(){
      return this.taskById(this.pokerVote.task);
    },
    taskName(){
      return `#${this.pokerVote.task} ` + this.task.name
    },
    taskDescription(){
      return this.task.description
    },
    votedStorypoints(){
      if(this.votes.length > 0 ){
        var votes = this.votes
        return votes.shift().storypoints;
      }
      else{
        return 0;
      }
    },
    votes(){
      // Own Votes by session (userid)
      return this.voteByIds({pokerVoteId: this.pokerVote.id, userId: this.userId});
    },
    voteStatus(){
      // Only from own votes
      // NS, WAIT, SKIPP, VOTED, ABSTENTION, NOTVOTED, AC
      if(this.votes.length > 0 && this.pokerVote.status === "WAIT"){
        // check vote abstention 
        if(this.votes.some(vote => vote.storypoints === 0)){
          return "ABSTENTION";
        }
        else{
          return "VOTED";
        }
      }
      // Voting is closed
      else if(this.votes.length > 0 && this.pokerVote.status === "FIN"){
        // check vote abstention 
        if(this.votes.some(vote => vote.storypoints === 0)){
          return "ABSTENTION";
        }
        else{
          return "VOTED";
        }
      }
      // Not voted, still waiting for voting
      else if(this.votes.length == 0 && this.pokerVote.status === "WAIT"){
        return "WAIT";
      }
      // Voting is closed
      else if(this.votes.length == 0 && this.pokerVote.status === "FIN"){
        return "NOTVOTED";
      }
      //
      else{
        return this.pokerVote.status;
      }
      
    },
  },
  methods:{
    ...mapActions("pokerVote", {
      fetchPokerVotes: "fetchList",
      fetchSinglePokerVote: "fetchSingle",
    }),
    ...mapActions("vote", {
      fetchUserVotes: "fetchList",
      fetchSingleUserVote: "fetchSingle",
      createUserVote: "create"
    }),
    ...mapActions("task", {
      fetchTasks: "fetchList"
    }),
    
    updateSelectedStorypoints(value){
      this.selectedStorypoints = value;
    },
    
    showTaskDetails(){
      this.$store.commit("selected/setTaskDetail", this.task);
      // open without create dialog
      this.$store.commit("selected/showTaskDetail");
    },
    selectPokerVote(){
      this.$emit("select-pokerVote", this.pokerVote);
    },
    skipVote(){
      // At skipped, send 0 in storypoint to backend
      this.createUserVote({
        data:{
          poker_vote: this.pokerVote.id,
          user: this.userId,
          storypoints: 0
        }
      })
      .then(()=> {
        this.fetchSinglePokerVote({id: this.pokerVote.id})
        this.fetchUserVotes();
      });
    },
    sendVote(){
      if(this.selectedStorypoints > 0){
        this.createUserVote({
          data:{
            poker_vote: this.pokerVote.id,
            user: this.userId,
            storypoints: this.selectedStorypoints
          }
        })
        .then(()=> {
          this.fetchSinglePokerVote({id: this.pokerVote.id});
          this.fetchUserVotes();
        })
      }
      else{
        this.$store.commit("showSystemAlert", {
        message: "Storypoint can't be zero. May you want to skip the vote",
        category: "warning"
        });
      }
    }

  },
  mounted(){

  }
}
</script>

<style>

</style>