<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col lg="1"  class="hidden-md-and-down">
      </v-col>
      <v-col lg="6" md="7" sm="12">
        <v-list class="transparent overflow-y-auto" style="max-height: calc(100vh - 225px)">
        <v-list-item v-for="pokerVoting in listPokerVotings" :key="pokerVoting.id">
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
                <v-expansion-panel-header v-slot="{ open }">
                  <v-row no-gutters>
                    <v-col cols="4">
                      {{taskName(pokerVote.task)}}
                    </v-col>
                    <v-col
                      cols="8"
                      class="text--secondary"
                    >
                      <v-fade-transition leave-absolute>
                        <span v-if="open && (pokerVote.status === 'NS'|| pokerVote.status === 'WAIT')">Please Vote!!!</span>
                        <span v-else-if="open && (pokerVote.status === 'SKIP')">Skipped</span>
                        <span v-else-if="open && (pokerVote.status === 'FIN')">Voted</span>
                        <v-row 
                          v-else
                          no-gutters
                          style="width: 100%"
                        >
                          <v-col cols="6">
                            Status: {{ GetPokerNamedStatus(pokerVote.status) }}
                          </v-col>
                          <v-col cols="6">
                            Your Vote: {{ currentStorypointVote() || 'Not set' }}
                          </v-col>
                        </v-row>
                      </v-fade-transition>
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
                              v-model="storypoints"
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
                              Enthalten
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
                              Abgeben
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
          <v-divider dark></v-divider>
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
import statusMaxin from "@/mixins/statusMixin"
import { mapGetters, mapActions } from "vuex";
export default {
  name: "PlanningPoker",
  components: { PokerSummary },
  mixins: [statusMaxin],
  data: () => ({
    storypoints: 0,
    availableStorypoints: [0, 1, 2, 3, 5, 8, 13, 21, 34, 55],
  }),
  computed:{
    ...mapGetters("pokerVoting", {
      listPokerVotings: "list",
      pokerVotingById: "byId"
    }),
    ...mapGetters("pokerVote", {
      listPokerVotes: "byPokerVotingId",
      pokerVoteById: "byId"
    }),
    ...mapGetters("vote", {
      listVotes: "list",
      voteById: "byId"
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
      // this.createUserVote({
      //   data:{

      //   }
      // })
    },
    sendVote(pokerVoteId){
      console.log(pokerVoteId)
    }
  },
  mounted(){
    this.fetchPokerVotings();
    this.fetchPokerVotes();
  }
}
</script>

<style>

</style>