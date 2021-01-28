<template>
  <div>
    <v-card class="primary" min-width="300" max-width="400">
      <v-card-title class="white--text"> Gromming </v-card-title>
      <v-card-subtitle class="white--text"> Planning Poker </v-card-subtitle>
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
        <v-divider dark></v-divider>
        <v-row>
          <v-subheader class="white--text subtitle-1"
            >Cards to vote</v-subheader
          >
          <v-list
            two-line
            class="transparent overflow-y-auto"
            style="max-height: calc(65vh - 350px)"
          >
            <v-list-item v-for="item in cardsToVote" :key="item.cardId">
              <v-list-item-content>
                <v-list-item-title class="white--text text-body-1"
                  >#{{ item.cardId }}: {{ item.cardName }}</v-list-item-title
                >
                <v-list-item-subtitle class="white--text text-body-2"
                  >Storypoints: {{ item.cardStorypoints }}</v-list-item-subtitle
                >
              </v-list-item-content>
              <v-list-item-action>
                <v-btn icon>
                  <v-icon color="white" @click="removePoker(item)"
                    >mdi-close-circle</v-icon
                  >
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-row>
        <v-divider dark></v-divider>
        <v-row>
          <v-subheader class="white--text subtitle-1">Options</v-subheader>
        </v-row>
        <v-row no-gutters align="center">
          <v-col cols="6">
            <v-checkbox
              label="Open End Vote"
              v-model="openEndVote"
              value
              color="link"
              dark
            ></v-checkbox>
          </v-col>
          <v-col cols="6">
            <v-menu
              ref="voteDateMenu"
              v-model="VoteDateMenu"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="endVoteDate"
                  label="End Vote date"
                  prepend-icon="mdi-calendar"
                  readonly
                  dark
                  :disabled="openEndVote"
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                ref="picker"
                v-model="endVoteDate"
                :min="new Date().toISOString()"
                @change="saveEndVoteDate"
              ></v-date-picker>
            </v-menu>
          </v-col>
        </v-row>
        <v-row no-gutters>
          <v-col>
            <v-radio-group
              v-model="voterSetting"
              column
              dark
              label="Voter scope"
            >
              <v-radio
                label="All project users in project"
                value="all"
              ></v-radio>
              <v-radio
                label="group of specify project users"
                value="specify"
              ></v-radio>
              <v-btn
                text
                outlined
                :disabled="voterSetting !== 'specify'"
                @click="voterSettingDialog = true"
              >
                select Voters
              </v-btn>
            </v-radio-group>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-subtitle class="white--text text-body-1">
        Start Poker
      </v-card-subtitle>
      <v-card-actions>
        <v-btn outlined disabled color="link">Poker Sync</v-btn>
        <v-spacer></v-spacer>
        <v-btn
          outlined
          color="link"
          :disabled="!allowAsyncPoker"
          @click="asyncPokerDialog = true"
          >Poker Async</v-btn
        >
      </v-card-actions>
    </v-card>
    <!-- Sprint Release Dialog -->
    <v-dialog
      v-model="asyncPokerDialog"
      persistent
      class="mx-auto"
      width="600"
      dark
    >
      <v-card color="tabbody" shaped>
        <v-card-text class="headline pt-10">
          <span class="ml-12"
            >Do you want to start a Async Planning Poker?</span
          >
        </v-card-text>
        <v-card-actions class="ml-10 pb-10 pt-10">
          <v-btn width="250" outlined @click="startAsyncPoker()">Yes</v-btn>
          <v-btn width="250" outlined @click="asyncPokerDialog = false"
            >No</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- select voter setting dialog -->
    <v-dialog
      v-model="voterSettingDialog"
      persistent
      class="mx-auto"
      width="600"
      dark
    >
      <v-card color="tabbody" shaped>
        <v-card-title> Select specify Voter </v-card-title>
        <v-card-text>
          <v-list
            class="transparent overflow-y-auto"
            style="max-height: calc(65vh - 225px)"
          >
            <v-list-item-group
              v-model="selectedVoters"
              multiple
              item-value="id"
              active-class="link--text"
            >
              <v-list-item
                v-for="voter in availableVoters"
                :key="voter.id"
                :value="voter.id"
              >
                <template v-slot:default="{ active }">
                  <v-list-item-action>
                    <v-checkbox :input-value="active"></v-checkbox>
                  </v-list-item-action>

                  <v-list-item-content>
                    <v-list-item-title>{{ voter.username }}</v-list-item-title>
                    <v-list-item-subtitle>{{
                      voter.name
                    }}</v-list-item-subtitle>
                  </v-list-item-content>
                </template>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-btn outlined @click="voterSettingDialog = false">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import { mapFields } from "vuex-map-fields";
export default {
  name: "PokerLane",
  data: () => ({
    asyncPokerDialog: false,
    VoteDateMenu: false,
    openEndVote: true,
    endVoteDate: null,
    cardsToVote: [],
    voterSetting: "all",
    voterSettingDialog: false,
    selectedVoters: [],
  }),
  computed: {
    // See more under Two-way Computed Property https://vuex.vuejs.org/guide/forms.html
    // Implementation with https://github.com/maoberlehner/vuex-map-fields
    // the string after the last dot (e.g. `id`) is used
    // for defining the name of the computed property.
    ...mapFields(["Userinfo.userId"]),
    ...mapGetters("user", {
      plattformUsersbyProjectId: "byProjectId",
    }),
    allowAsyncPoker() {
      var allowed = false;
      if (this.cardsToVote.length > 0 && this.openEndVote) {
        allowed = true;
      } else if (
        this.cardsToVote.length > 0 &&
        !this.openEndVote &&
        this.endVoteDate !== null
      ) {
        allowed = true;
      } else {
        allowed = false;
      }
      return allowed;
    },
    availableVoters() {
      return this.plattformUsersbyProjectId(
        parseInt(this.$route.params.id, 10)
      );
    },
  },
  methods: {
    ...mapActions("pokerVoting", {
      fetchSingleAsyncPokerVoting: "fetchSingle",
      createAsyncPokerVoting: "create",
      deleteAsyncPokerVoting: "destroy",
    }),
    ...mapActions("pokerVote", {
      fetchSingleAsyncPokerVote: "fetchSingle",
      createAsyncPokerVote: "create",
    }),
    allowDrop(e) {
      const taskStatus = e.dataTransfer.getData("task-status");
      const sprintStatus = e.dataTransfer.getData("task-sprint-status");

      // poker is only in new or planned task status allowed
      // if a task in a sprint, there is sprint status have to in planning
      if (
        (sprintStatus === "IL" || sprintStatus === "") &&
        (taskStatus === "NW" || taskStatus === "PL")
      ) {
        e.preventDefault();
        return true;
      } else {
        return false;
      }
    },
    addPoker(e) {
      const taskId = e.dataTransfer.getData("task-id");
      const taskName = e.dataTransfer.getData("task-name");
      // const taskFeatureId = e.dataTransfer.getData("task-feature-id");
      // const taskSprintId = e.dataTransfer.getData("task-sprint-id");
      // const taskSprintStatus = e.dataTransfer.getData("task-sprint-status");
      const taskStorypoints = e.dataTransfer.getData("task-storypoints");
      if (this.cardsToVote.findIndex((item) => item.cardId == taskId) == -1) {
        this.cardsToVote.push({
          cardName: taskName,
          cardId: taskId,
          cardStorypoints: taskStorypoints,
        });
      } else {
        this.$store.commit("showSystemAlert", {
          message: "Card is already added in planning poker",
          category: "warning",
        });
      }
    },
    removePoker(vote) {
      this.cardsToVote = this.cardsToVote.filter(
        (item) => item.cardId !== vote.cardId
      );
    },
    saveEndVoteDate(date) {
      this.$refs.voteDateMenu.save(date);
    },

    startAsyncPoker() {
      this.asyncPokerDialog = false;
      var asyncPokerData = {
        project: this.$route.params.id,
        modus: "ASYNC",
        manager: this.userId,
        voters: [],
      };
      // specify voter group
      if (this.voterSetting === "specify") {
        console.log(this.selectedVoters);
        asyncPokerData.voters = this.selectedVoters;
        this.selectedVoters = [];
      } else {
        this.selectedVoters = [];
      }
      // timeboxed or open end vote
      if (this.openEndVote) {
        asyncPokerData.start = new Date().toISOString().slice(0, 10);
        asyncPokerData.end = null;
      } else {
        asyncPokerData.start = new Date().toISOString().slice(0, 10);
        asyncPokerData.end = this.endVoteDate;
      }
      console.log(asyncPokerData);
      this.createAsyncPokerVoting({
        data: asyncPokerData,
      }).then((res) => {
        console.log(res);
        // Create pokerVotes belongs to the created pokerVoting
        const pokerVotingId = res.data.id;
        if (pokerVotingId !== null) {
          this.cardsToVote.forEach((card) => {
            this.createAsyncPokerVote({
              data: {
                poker_voting: pokerVotingId,
                task: card.cardId,
                status: "WAIT",
              },
            })
              .then(() => {
                this.$store.commit("showSystemAlert", {
                  message: "Planning Poker is created.",
                  category: "info",
                });
              })
              .catch((error) => {
                // Delete PokerVoting, if get errors to create pokerVotes
                this.deleteAsyncPokerVoting({ id: pokerVotingId });
                this.$store.commit("showSystemAlert", {
                  message:
                    "Async planning poker with one of those cards already exist." +
                    error.data.non_field_errors[0],
                  category: "error",
                });
              });
          });
          // delete list with card to vote
          this.cardsToVote = [];
        } else {
          this.$store.commit("showSystemAlert", {
            message: "Can't create async planning poker",
            category: "error",
          });
        }
      });
    },
  },
};
</script>

<style lang="css" scoped>
@import "../../main.css";
</style>