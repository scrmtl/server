<template>
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
        <v-tab>Summary</v-tab>
      </v-tabs>
      <v-tabs-items>
        <!-- Details -->
        <v-tab-item
          v-model="tab"
          background-color="navbar"
          color="navbar"
        >
          <v-card flat dark color="navbar" tile>
            <v-card-title>
                <span class="headline">{{ sprintName }}</span>
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
                    v-model="status"
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
                    v-model="value"
                    outlined
                    dense
                    readonly
                    label="Duration (in d)"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row align="center">
                <v-col>
                  <v-text-field
                    v-model="version"
                    outlined
                    dense
                    label="Product Version"
                  ></v-text-field>
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
          </v-card> 
        </v-tab-item>
        <!-- Summary -->
        <v-tab-item
          v-model="tab"
          background-color="navbar"
          color="navbar"
        >
          <v-card flat dark color="navbar" tile>
            <v-card-text>
              <v-row align="center">
                <v-col>
                  <v-text-field
                    v-model="value"
                    outlined
                    dense
                    label="Planned card number"
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    v-model="value"
                    outlined
                    dense
                    label="Finished card number"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row align="center">
                <v-col>
                  <v-text-field
                    v-model="value"
                    outlined
                    dense
                    label="Planned Story Points"
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    v-model="value"
                    outlined
                    dense
                    label="Finished Story Points"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row align="center">
                <v-col>
                  <v-text-field
                    v-model="value"
                    outlined
                    dense
                    label="Duration"
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    v-model="value"
                    outlined
                    dense
                    label="remaining duration"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card> 
        </v-tab-item>
      </v-tabs-items>

    </v-container>
  </v-navigation-drawer>
</template>

<script>
import { mapActions } from "vuex";
import { mapFields } from "vuex-map-fields";
export default {
  name: "TheDetailSprint",
  data: () => ({
    tab: null,
    sprintName: "Create new sprint",
    value: 0, //placeholder
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
          
          status: "NW"
        },
        customUrlFnArgs: {}
      })
      .then(() => {
        this.fetchSprints({customUrlFnArgs: {}});
        this.$store.commit("selected/hideSprintDetail");
        this.$store.commit("showSystemAlert", {
          message: "Create new Sprint",
          category: "info"
        });
      })
    },
    
    saveSprint() {

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
      "sprint.visableDetail",
      "sprint.visableCreate",
    ]),

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
      if (this.visableDetail && !this.visableCreate) {
        this.sprintName = "Sprint " + this.number;
      } else {
        this.sprintName = "Create new sprint"
      }
    },
  },
  created() {

  }
}
</script>

<style lang="css" scoped>
  @import "../main.css";
</style>