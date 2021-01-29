<template>
  <div>
    <v-card class="primary">
      <v-card-title class="white--text"> Planning Poker </v-card-title>
      <v-card-subtitle class="white--text"> Summary </v-card-subtitle>
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
              >{{ act_storypoints || 0 }} SP
            </v-progress-circular>
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
            <v-row dense>
              <v-text-field
                :value="namedManager"
                label="Manager"
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
              :value="avg_storypoints || '-'"
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
            <v-list
              class="transparent overflow-y-auto"
              style="max-height: calc(75vh - 225px)"
            >
              <v-list-item v-for="player in players" :key="player.name">
                <v-list-item-icon>
                  <v-icon :color="player.color">mdi-account</v-icon>
                </v-list-item-icon>
                <v-list-item-title :class="`${player.color}--text`">{{
                  player.name
                }}</v-list-item-title>
                <v-list-item-subtitle
                  :class="`${player.color}--text text-right`"
                >
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
              :disabled="!isActionAllowed"
              >Accept</v-btn
            >
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
              :disabled="!isActionAllowed"
              >Skip</v-btn
            >
          </template>
          <span>Skipped and close vote</span>
        </v-tooltip>
        <!-- Sync Modus -->
        <v-btn v-if="pokerVoting.mode === 'SYNC'" outlined color="link"
          >Next</v-btn
        >
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
            <span class="ml-12 headline pt-10"
              >Do you want discard the voted storypoints?</span
            >
          </v-row>
          <v-row>
            <span class="ml-12 my-2 subtitle pt-8"
              >Please choose the storypoints, first</span
            >
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
          <v-btn width="250" outlined @click="discardDialog = false">No</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import { mapFields } from "vuex-map-fields";
export default {
  name: "PokerSummary",
  data: () => ({
    discardDialog: false,
    selectedStorypoints: 0,
    availableStorypoints: [0, 1, 2, 3, 5, 8, 13, 21, 34, 55]
  }),
  computed: {
    // See more under Two-way Computed Property https://vuex.vuejs.org/guide/forms.html
    // Implementation with https://github.com/maoberlehner/vuex-map-fields
    // the string after the last dot (e.g. `id`) is used
    // for defining the name of the computed property.
    ...mapFields(["Userinfo.userId"]),
    ...mapFields("selected", [
      "pokerVote.details.id",
      "pokerVote.details.manager",
      "pokerVote.details.status",
      "pokerVote.details.act_storypoints",
      "pokerVote.details.avg_storypoints",
      "pokerVote.details.end_storypoints",
      "pokerVote.details.poker_voting",
      "pokerVote.details.task",
      "pokerVote.visableDetail",
      "pokerVote.readOnly"
    ]),
    ...mapGetters("vote", {
      voteById: "byPokerVoteId"
    }),
    ...mapGetters("user", {
      plattformUserById: "byId"
    }),
    ...mapGetters("pokerVoting", {
      pokerVotingById: "byId"
    }),
    isActionAllowed() {
      if (this.manager === this.userId) {
        if (this.status !== "AC" && this.status !== "SKIP") {
          return true;
        } else {
          return false;
        }
      } else {
        return false;
      }
    },
    storypointsInPercent() {
      return Math.round((this.act_storypoints / 55) * 100);
    },
    votedPlayer() {
      return this.voteById(this.id).length;
    },
    players() {
      var votes = this.voteById(this.id);
      var voter = [];
      if (votes.length > 0) {
        votes.forEach(vote => {
          var user = this.plattformUserById(vote.user);
          voter.push({
            name: user.username + ` (${user.name})`,
            storypoints: vote.storypoints,
            color: "white"
          });
        });
      }
      return voter;
    },
    pokerNamedStatus() {
      var namedStatus = "-";
      switch (this.status) {
        case "NS":
          namedStatus = "Not started (Nobody Voted)";
          break;
        case "WAIT":
          namedStatus = "Waiting for additonal votes";
          break;
        case "SKIP":
          namedStatus = "Poker skipped";
          break;
        case "FIN":
          namedStatus = "All Voted";
          break;
        case "AC":
          namedStatus = "Poker accepted";
          break;
      }
      return namedStatus;
    },
    pokerVoting() {
      if (this.id !== null) {
        var pokerVoting = this.pokerVotingById(this.poker_voting);
        return pokerVoting;
      } else {
        return null;
      }
    },
    namedManager() {
      var user = this.plattformUserById(this.pokerVoting.manager);
      return user.username + ` (${user.name})`;
    }
  },
  methods: {
    ...mapActions("pokerVote", {
      fetchSinglePokerVote: "fetchSingle",
      updatePokerVote: "update"
    }),
    ...mapActions("task", {
      fetchSingleTask: "fetchSingle",
      updateTask: "update"
    }),

    acceptAsyncVote() {
      // Update PokerVote and close vote
      this.updatePokerVote({
        id: this.id,
        data: {
          poker_voting: this.poker_voting,
          status: "AC",
          task: this.task
        }
      }).then(res => {
        this.$store.commit("selected/setPokerVoteDetail", res.data);
        this.fetchSinglePokerVote({ id: this.id });
        this.fetchSingleTask({ id: this.task, customUrlFnArgs: {} });
      });
    },
    skipAsyncVote() {
      // update Poker vote to skipped and set SP to act/old Value
      this.updatePokerVote({
        id: this.id,
        data: {
          poker_voting: this.poker_voting,
          status: "SKIP",
          end_storypoints: this.act_storypoints,
          task: this.task
        }
      }).then(res => {
        this.$store.commit("selected/setPokerVoteDetail", res.data);
        this.fetchSinglePokerVote({ id: this.id });
        this.fetchSingleTask({ id: this.task, customUrlFnArgs: {} });
      });
    },
    discardAsyncVote() {
      console.log(this.selectedStorypoints);
      this.discardDialog = false;
      // update Poker vote to skipped and set SP to user defined Value
      this.updatePokerVote({
        id: this.id,
        data: {
          poker_voting: this.poker_voting,
          status: "SKIP",
          end_storypoints: this.selectedStorypoints,
          task: this.task
        }
      }).then(() => {
        this.fetchSinglePokerVote({ id: this.id });
      });
    }
  }
};
</script>

<style lang="css" scoped>
@import "../../main.css";
</style>
