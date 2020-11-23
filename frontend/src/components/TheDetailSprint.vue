<template>
<div>
  <v-navigation-drawer
    v-model="visibleDrawer"
    right
    app
    temporary
    hide-overlay
    width="600"
    color="navbar"
    dark
  >
    <v-container>
      <v-tabs
        v-model="tab"
        dark
        background-color="navbar"
        slider-color="link"
        centered
        grow
        tile
      >
        <v-tab>Details</v-tab>
        <v-tab :disabled="visableCreate">Summary</v-tab>
      </v-tabs>

      <v-tabs-items v-model="tab" background-color="navbar" color="navbar">
        <!-- Details -->
        <v-tab-item >
          <v-card flat dark color="navbar" tile>
            <v-card-title>
                <span class="headline">{{ header }}</span>
            </v-card-title>
            <v-card-text>
              <v-row align="center">
                <v-col>
                  <v-text-field
                    v-model="number"
                    outlined
                    dense
                    readonly
                    label="Sprint No."
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    v-model="namedStatus"
                    outlined
                    dense
                    readonly
                    label="Status"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row align="center">
                <v-col>
                  <v-text-field
                    v-model="start"
                    outlined
                    dense
                    readonly
                    label="Start"
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    v-model="end"
                    outlined
                    dense
                    readonly
                    label="End"
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    :value="statistic.total_duration"
                    outlined
                    dense
                    readonly
                    suffix="days"
                    label="Duration"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row align="center">
                <v-col>
                  <v-form ref="form" v-model="isFormValid" lazy-validation>
                  <v-text-field
                    v-model="version"
                    outlined
                    dense
                    required
                    :rules="[rules.versionNaming]"
                    placeholder="V00.00.00.00"
                    label="Product Version"
                  ></v-text-field>
                  </v-form>
                </v-col>
              </v-row>
              <v-row align="center">
                <v-col>
                  <v-textarea
                    v-model="story"
                    outlined
                    min-height="70"
                    label="Story"
                  ></v-textarea>
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-actions>
              <v-btn color="link" text @click="close()">Close</v-btn>
              <v-btn
                v-if="!visableCreate"
                color="link"
                text
                @click="confirm()"
              >Save</v-btn>
              <v-btn
                v-if="visableCreate"
                color="link"
                text
                :disabled="!isFormValid"
                @click="addSprint()"
                >Create</v-btn>
              <v-btn
                v-if="!visableCreate"
                color="link"
                text
                absolute
                right
                :disabled="!SprintReleaseValidation"
                @click="sprintReleaseDialog = true"
              >Release</v-btn>
            </v-card-actions>
          </v-card> 
        </v-tab-item>
        <!-- Summary -->
        <v-tab-item :disabled="visableCreate">
          <v-card flat dark color="navbar" tile>
            <v-card-text>
              <v-row align="center">
                <v-col>
                  <v-text-field
                    :value="statistic.sum_of_tasks"
                    outlined
                    dense
                    readonly
                    label="Planned card number"
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    :value="statistic.sum_of_done_tasks"
                    outlined
                    dense
                    readonly
                    label="Finished card number"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row align="center">
                <v-col>
                  <v-text-field
                    :value="statistic.sum_of_sp"
                    outlined
                    dense
                    readonly
                    label="Planned Story Points"
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    :value="statistic.sum_of_done_sp"
                    outlined
                    dense
                    readonly
                    label="Finished Story Points"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row align="center">
                <v-col>
                  <v-text-field
                    :value="statistic.total_duration"
                    outlined
                    dense
                    readonly
                    suffix="days"
                    label="Duration"
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    :value="statistic.remaining_duration"
                    outlined
                    dense
                    readonly
                    suffix="days"
                    label="remaining duration"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-actions>
              <v-btn color="link" text @click="close()">Close</v-btn>
            </v-card-actions>
          </v-card> 
        </v-tab-item>
      </v-tabs-items>
    </v-container>
  </v-navigation-drawer>
  <!-- Sprint Release Dialog -->
  <v-dialog
    v-model="sprintReleaseDialog"
    persistent
    class="mx-auto"
    width="600"
    dark
  >
    <v-card color="tabbody" shaped>
      <v-card-text class="headline pt-10">
        <span class="ml-12">Do you want to release sprint {{number}}?</span>
      </v-card-text>
      <v-card-actions class="ml-10 pb-10 pt-10">
        <v-btn width="250" outlined  @click="releaseSprint()"
          >Yes</v-btn
        >
        <v-btn
          width="250"
          outlined
          @click="sprintReleaseDialog = false"
          >No</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import { mapFields } from "vuex-map-fields";
export default {
  name: "TheDetailSprint",
  data: () => ({
    tab: null,
    statistic: {},
    sprintReleaseDialog: false,
    header: "Create new sprint",
    placeHolderValue: 0, //placeholder
    namedStatus: "in Planning",
    isFormValid: null,
  	rules: {
      required: value => !!value || "Required",
      versionNaming: value => {
        const pattern = /^V\d{1,2}\.\d{1,2}\.\d{1,2}\.\d{1,2}$/;
        return pattern.test(value) || "Invaild Versioning";
      }
    }
  }),
  components: {
  },
  methods: {
    ...mapActions("sprint", {
      updateSprint: "update",
      createSprint: "create",
      fetchSprints: "fetchList",
      fetchSingleSprint: "fetchSingle"
    }),

    ...mapActions("sprintStatistics", {
      fetchSprintStatistics: "fetchList"
    }),
    
    close() {
      this.$store.commit("selected/hideSprintDetail");
    },
    confirm() {
      this.saveSprint();
      this.$store.commit("selected/hideSprintDetail");
    },
    
    addSprint() {
      this.createSprint({
        data:{
          project: this.$route.params.id,
          status: "IL",
          version: this.version,
          story: this.story
        },
        customUrlFnArgs: {}
      })
      .then(() => {
        this.fetchSprints({customUrlFnArgs: {projectId: this.$route.params.id } });
        this.fetchSprintStatistics();
        this.$store.commit("selected/hideSprintDetail");
        this.$store.commit("showSystemAlert", {
          message: "Create new Sprint",
          category: "success"
        });
      })
    },
    
    saveSprint() {
      this.updateSprint({
        id: this.id,
        data: {
          version: this.version,
          story: this.story
        },
        customUrlFnArgs: {}
      })
      .then(
        function(value) {
          if(value.data.id !== undefined){
            this.fetchSingleSprint({
              id: this.id,
              customUrlFnArgs: {}
            });
          }
          this.close();
        }.bind(this)
      );
    },

    releaseSprint() {
      this.sprintReleaseDialog = false;
      this.updateSprint({
        id: this.id,
        data: {
          status: "PL",
          version: this.version,
          story: this.story
        },
        customUrlFnArgs: {}
      })
      .then(
        function(value) {
          if(value.data.id !== undefined){
            this.fetchSingleSprint({
              id: this.id,
              customUrlFnArgs: {}
            });
          }
          this.close();
          this.$store.commit("showSystemAlert", {
          message: "Release Sprint " + this.number,
          category: "success"
        });
        }.bind(this)
      );
    },

    GetNamedStatus(status) {
      var namedStatus = "in Planning";
      switch (status) {
        case "IL":
          namedStatus = "In Planning";
          break;
        case "PL":
          namedStatus = "Planned";
          break;
        case "IR":
          namedStatus = "In Progress";
          break;
        case "DO":
          namedStatus = "Done";
          break;
        case "AC":
          namedStatus = "Accepted";
          break;
      }
      return namedStatus;
    },
    GetHeader() {
      if (this.visableDetail && !this.visableCreate) {
        return "Sprint " + this.number;
      } else {
        return "Create new sprint"
      }
    },
    GetStatitic() {
      if(this.visableDetail && !this.visableCreate){
        return this.sprintStatisticsById(this.id);
      }
      else{
        return {}
      }
    }

  },

  computed: {
    // See more under Two-way Computed Property https://vuex.vuejs.org/guide/forms.html
    // Implementation with https://github.com/maoberlehner/vuex-map-fields
    // the string after the last dot (e.g. `id`) is used
    // for defining the name of the computed property.
    ...mapFields("selected", [
      "sprint.details.id",
      "sprint.details.status",
      "sprint.details.number",
      "sprint.details.version",
      "sprint.details.start",
      "sprint.details.end",
      "sprint.details.story",
      "sprint.details.task_cards",
      "sprint.visableDetail",
      "sprint.visableCreate"
    ]),
    ...mapGetters("sprintStatistics", {
      sprintStatisticsById: "byId"
    }),

    SprintReleaseValidation() {
      if(this.status === "IL" && !this.visableCreate && this.task_cards.length > 0){
        return true;
      }
      else{
        return false;
      }
    },

    visibleDrawer: {
      get() {
        return this.visableDetail;
      },
      set(value) {
        if (value) {
          this.$store.commit("selected/showSprintDetail");
        } else {
          this.$store.commit("selected/hideSprintDetail");
        }
      }
    },
    
  },
  watch: {
    visibleDrawer(val, prev) {
      // Nothing to update
      if (val === prev) return;
      // Update props
      this.header = this.GetHeader();
      this.namedStatus = this.GetNamedStatus(this.status);
      this.statistic = this.GetStatitic()
    },
  },
  created() {
    this.header = this.GetHeader();
    this.namedStatus = this.GetNamedStatus(this.status);
  }
};
</script>

<style lang="css" scoped>
  @import "../main.css";
</style>
