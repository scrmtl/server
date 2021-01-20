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
                <PokerVote v-for="pokerVote in listPokerVotes(pokerVoting.id)"
                :key="pokerVote.id" v-bind:pokerVote="pokerVote" @select-pokerVote="selectedPokerVote = $event"/>
              </v-expansion-panels>
            </v-col>
          </v-row>
          </v-list-item-content>
        </v-list-item>
        </v-list>
      </v-col>
      <v-col lg="4" md="5" class="hidden-sm-and-down">
        <PokerSummary v-if="showPokerSummary" v-bind:selectedPokerVote="selectedPokerVote" class="hidden-sm-and-down"/>
      </v-col>
      <v-col lg="1"  class="hidden-md-and-down">
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import PokerSummary from "@/components/Poker/PokerSummary.vue";
import PokerVote from "@/components/Poker/PokerVote.vue";
import { mapFields } from "vuex-map-fields";
import { mapGetters, mapActions } from "vuex";
export default {
  name: "PlanningPoker",
  components: { 
    PokerSummary,
    PokerVote
  },
  data: () => ({
    selectedPokerVote: null
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
      listPokerVotes: "byPokerVotingId"
    }),
    ...mapGetters("project", {
      projectById: "byId"
    }),  
    showPokerSummary(){
      // TODO check, if session manager of selected pokerVote
      if(this.selectedPokerVote !== null){
        return true;
      }
      else{
        return false
      }
    }
  },
  methods:{
    ...mapActions("pokerVoting", {
      fetchPokerVotings: "fetchList",
    }),
    ...mapActions("pokerVote", {
      fetchPokerVotes: "fetchList",
    }),
    ...mapActions("vote", {
      fetchUserVotes: "fetchList",
    }),
    ...mapActions("task", {
      fetchTasks: "fetchList"
    }),
  
    projectName(projectId){
      return this.projectById(projectId).name;
    },
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