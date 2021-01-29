<template>
  <v-container fluid>
    <v-row dense>
      <v-col cols="12">
        <v-switch
          color="link"
          inset
          dark
          v-model="showAllPokerVotings"
          label="Show all Planning Pokers"
        >
        </v-switch>
      </v-col>
    </v-row>
    <v-row dense>
      <v-col cols="4"></v-col>
      <v-col cols="4" v-if="listFilteredPokerVoting.length == 0">
        <span class="white--text text-center">
          No upcoming Planning Poker for you</span
        >
      </v-col>
      <v-col cols="4"></v-col>
    </v-row>
    <v-row justify="center">
      <v-col lg="1" class="hidden-md-and-down"> </v-col>
      <v-col lg="6" md="7" sm="12">
        <v-list
          class="transparent overflow-y-auto"
          style="max-height: calc(100vh - 225px)"
        >
          <v-list-item
            v-for="pokerVoting in listFilteredPokerVoting"
            :key="pokerVoting.id"
          >
            <v-list-item-content>
              <v-row justify="center">
                <v-tooltip top>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon
                      v-if="pokerVoting.manager === userId"
                      color="teal"
                      v-bind="attrs"
                      v-on="on"
                      class="mx-4"
                    >
                      mdi-account-cowboy-hat
                    </v-icon>
                  </template>
                  <span>I am planning poker manager</span>
                </v-tooltip>
                <span class="text-h5 white--text"
                  >{{ projectName(pokerVoting.project) }} (No.{{
                    pokerVoting.id
                  }})</span
                >
              </v-row>
              <v-row justify="center">
                <span class="text-h7 white--text"
                  >Mode: {{ pokerVoting.mode }}
                </span>
              </v-row>
              <v-row justify="center">
                <v-col>
                  <v-expansion-panels dark accordion>
                    <PokerVote
                      v-for="pokerVote in listFilteredPokerVotes(
                        pokerVoting.id
                      )"
                      :key="pokerVote.id"
                      v-bind:pokerVote="pokerVote"
                      @select-pokerVote="showPokerSummary($event)"
                    />
                  </v-expansion-panels>
                </v-col>
              </v-row>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-col>
      <v-col lg="4" md="5" class="hidden-sm-and-down">
        <PokerSummary v-if="visiblePokerSummary" class="hidden-sm-and-down" />
      </v-col>
      <v-col lg="1" class="hidden-md-and-down"> </v-col>
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
    showAllPokerVotings: false
  }),
  computed: {
    ...mapFields(["Userinfo.userId"]),
    ...mapFields("selected", ["pokerVote.visableDetail"]),
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

    visiblePokerSummary: {
      get() {
        return this.visableDetail;
      },
      set(newValue) {
        if (newValue) {
          this.$store.commit("selected/showPokerVoteDetail");
        } else {
          this.$store.commit("selected/hidePokerVoteDetail");
        }
      }
    },
    listFilteredPokerVoting() {
      // list only where userId involved
      var pokerVotings = this.listPokerVotings(this.userId);
      if (this.showAllPokerVotings) {
        return pokerVotings;
      } else {
        // Show only open pokerVoting
        return pokerVotings.filter(
          pokerVotings =>
            this.listPokerVotes(pokerVotings.id).filter(
              pokerVote => pokerVote.status == "WAIT"
            ).length > 0
        );
      }
    }
  },
  methods: {
    ...mapActions("pokerVoting", {
      fetchPokerVotings: "fetchList"
    }),
    ...mapActions("pokerVote", {
      fetchPokerVotes: "fetchList"
    }),
    ...mapActions("vote", {
      fetchUserVotes: "fetchList"
    }),
    ...mapActions("task", {
      fetchTasks: "fetchList"
    }),

    projectName(projectId) {
      return this.projectById(projectId).name;
    },

    listFilteredPokerVotes(pokerVotingId) {
      var pokerVotes = this.listPokerVotes(pokerVotingId);
      if (this.showAllPokerVotings) {
        return pokerVotes;
      } else {
        // Show only open pokerVotes
        return pokerVotes.filter(pokerVote => pokerVote.status == "WAIT");
      }
    },
    showPokerSummary(pokerVote) {
      this.$store.commit("selected/setPokerVoteDetail", pokerVote);
      this.$store.commit("selected/showPokerVoteDetail");
    }
  },
  watch: {
    showAllPokerVotings(current, prev) {
      if (current !== prev) {
        this.$store.commit("selected/hidePokerVoteDetail");
      }
    },
    listFilteredPokerVoting(current, prev) {
      if (current.length != prev.length) {
        this.$store.commit("selected/hidePokerVoteDetail");
      }
    }
  },
  mounted() {
    this.fetchPokerVotings().then(() => {
      this.listPokerVotings(this.userId).forEach(pokerVoting => {
        this.fetchTasks({
          customUrlFnArgs: { projectId: pokerVoting.project }
        });
      });
    });
    this.fetchPokerVotes();
    this.fetchUserVotes();
    this.$store.commit("selected/hidePokerVoteDetail");
  }
};
</script>

<style></style>
