<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col lg="1"  class="hidden-md-and-down">
      </v-col>
      <v-col lg="6" md="7" sm="12">
        <v-list class="transparent overflow-y-auto" style="max-height: calc(100vh - 225px)">
        <v-list-item v-for="pokerVoting in listPokerVotings(userId)" :key="pokerVoting.id">
          <v-list-item-content>
          <v-row justify="center">
          <span class="text-h5 white--text">{{projectName(pokerVoting.project)}}</span>
          </v-row>
          <v-row justify="center">
            <span class="text-h7 white--text">Mode: {{pokerVoting.mode}}</span>
          </v-row>
          <v-row justify="center">
            <v-col>
              <v-expansion-panels dark accordion>
              <v-expansion-panel
                v-for="pokerVote in listPokerVotes(pokerVoting.id)"
                :key="pokerVote.id"
                class="primary"
              > 
                <v-expansion-panel-header disable-icon-rotate>
                  <v-row no-gutters >
                    <v-col cols="11"  class="my-1">
                      {{taskName(pokerVote.task)}}
                    </v-col>
                    <v-col cols="1">
                       <v-icon v-if="status(pokerVote.status, pokerVote.id) === 'VOTED'" color="teal">
                        mdi-check
                      </v-icon>
                      <v-icon v-else color="error">
                        mdi-alert-circle-outline
                      </v-icon>
                    </v-col>
                  </v-row>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <v-row no-gutters justify="start">
                      <v-col>
                        {{taskDescription(pokerVote.task)}}
                        <v-btn
                          text
                          color="white"
                          @click="showTaskDetails(pokerVote.task)"
                        >
                          More Details
                        </v-btn>
                        
                      </v-col>
                      <v-divider
                        vertical
                        class="mx-4"
                      ></v-divider>
                      <v-col>
                        <v-row >
                          <v-col>
                            <v-autocomplete
                              v-model="selectedStorypoints"
                              :items="availableStorypoints"
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
                              outlined
                              color="white"
                              @click="skipVote(pokerVote.id)"
                            >
                              Skip
                            </v-btn>
                          </v-col>
                        </v-row>
                        <v-row >
                          <v-col >
                            <v-btn
                              text
                              outlined
                              color="link"
                              @click="sendVote(pokerVote.id)"
                            >
                              Send vote
                            </v-btn>
                          </v-col>
                        </v-row>
                      </v-col>
                    </v-row>
                </v-expansion-panel-content>
              </v-expansion-panel>
              </v-expansion-panels>
            </v-col>
          </v-row>
          </v-list-item-content>
        </v-list-item>
        </v-list>
      </v-col>
      <v-col lg="4" md="5" class="hidden-sm-and-down">
        <PokerSummary class="hidden-sm-and-down"/>
      </v-col>
      <v-col lg="1"  class="hidden-md-and-down">
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import PokerSummary from "@/components/Poker/PokerSummary.vue";
import statusMaxin from "@/mixins/statusMixin";
import { mapFields } from "vuex-map-fields";
import { mapGetters, mapActions } from "vuex";
export default {
  name: "PlanningPoker",
  components: { PokerSummary },
  mixins: [statusMaxin],
  data: () => ({
    selectedStorypoints: 0,
    availableStorypoints: [0, 1, 2, 3, 5, 8, 13, 21, 34, 55],
  }),
  computed:{
    ...mapFields([
      "Userinfo.userId"
    ]),
    ...mapGetters("pokerVoting", {
      listPokerVotings: "byVoterId",
      pokerVotingById: "byId"
    }),
    ...mapGetters("pokerVote", {
      listPokerVotes: "byPokerVotingId",
      pokerVoteById: "byId"
    }),
    ...mapGetters("vote", {
      listVotes: "list",
      voteByIds: "byPokerVoteIdAndUserId"
    }),
    ...mapGetters("task", {
      taskById: "byId"
    }),
    ...mapGetters("project", {
      projectById: "byId"
    }),
    
  },
  methods:{
    ...mapActions("pokerVoting", {
      fetchPokerVotings: "fetchList",
      fetchSinglePokerVoting: "fetchSingle",
    }),
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
    status(pokerVoteStatus, pokerVoteId){
      var voteStatus = "VOTED"
      var votes = this.voteByIds({pokerVoteId: pokerVoteId, userId: this.userId})
      if(votes.length > 0){
        voteStatus = "VOTED"
      }
      else{
        voteStatus = "WAIT"
      }
      console.log(votes)
      // Waiting for Voting

      // Skipped

      // Voted
      return voteStatus
    },
    projectName(projectId){
      return this.projectById(projectId).name;
    },
    taskName(taskId){
      return `#${taskId} ` + this.taskById(taskId).name
    },
    taskDescription(taskId){
      return this.taskById(taskId).description
    },
    showTaskDetails(taskId){
      this.$store.commit("selected/setTaskDetail", this.taskById(taskId));
      // open without create dialog
      this.$store.commit("selected/showTaskDetail");
    },
    currentStorypointVote(){
      return null;
    },
    skipVote(pokerVoteId){
      console.log(pokerVoteId)
      // At skipped, send 0 in storypoint to backend
      this.createUserVote({
        data:{
          poker_vote: pokerVoteId,
          user: this.userId,
          storypoints: 0
        }
      })
      .then((res)=> {
        this.fetchSinglePokerVote({id: pokerVoteId})
        this.fetchSingleUserVote({id: res.data.id})
      })
    },
    sendVote(pokerVoteId){
      if(this.selectedStorypoints){
        // Check, if vote already done
        // TODO
        this.createUserVote({
          data:{
            poker_vote: pokerVoteId,
            user: this.userId,
            storypoints: this.selectedStorypoints
          }
        })
        .then((res)=> {
          this.fetchSinglePokerVote({id: pokerVoteId});
          this.fetchSingleUserVote({id: res.data.id});
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
  watch:{

  },
  mounted(){
    this.fetchPokerVotings().then(()=>{
      this.listPokerVotings(this.userId).forEach(pokerVoting => {
        this.fetchTasks({ customUrlFnArgs: { projectId: pokerVoting.project } });
      });
    })
    this.fetchPokerVotes();
    this.fetchUserVotes();
  }
}
</script>

<style>

</style>