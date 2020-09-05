<template>
  <div>
    <v-navigation-drawer v-model="visible" absolute right width="800" color="navbar" dark>
      <v-container>
        <v-card>
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
            <v-tab>Info</v-tab>
          </v-tabs>

          <v-tabs-items v-model="tab" background-color="navbar" color="navbar">
            <v-tab-item>
              <v-card flat dark color="navbar" tile>
                <v-card-text>
                  <v-text-field
                    label="Projektname*"
                    required
                    prepend-icon="mdi-information-outline"
                    class="ma-1"
                    v-model="localProject.name"
                  ></v-text-field>
                  <v-menu
                    ref="menu"
                    v-model="calendar1menu"
                    :close-on-content-click="false"
                    transition="scale-transition"
                    offset-y
                    min-width="290px"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field
                        v-model="localProject.start"
                        label="Projekt Start*"
                        hint="YYYY-MM-DD"
                        prepend-icon="mdi-calendar-range"
                        required
                        persistent-hint
                        class="ma-1"
                        readonly
                        v-bind="attrs"
                        v-on="on"
                      ></v-text-field>
                    </template>
                    <v-date-picker v-model="localProject.start" no-title scrollable>
                      <v-spacer></v-spacer>
                      <v-btn text color="primary" @click="calendar1menu = false">Cancel</v-btn>
                      <v-btn text color="primary" @click="calendar1menu = false">OK</v-btn>
                    </v-date-picker>
                  </v-menu>
                  <v-menu
                    ref="menu"
                    v-model="calendar2menu"
                    :close-on-content-click="false"
                    transition="scale-transition"
                    offset-y
                    min-width="290px"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field
                        v-model="localProject.end"
                        label="Projekt Ende*"
                        hint="YYYY-MM-DD"
                        prepend-icon="mdi-calendar-range"
                        required
                        persistent-hint
                        class="ma-1"
                        readonly
                        v-bind="attrs"
                        v-on="on"
                      ></v-text-field>
                    </template>
                    <v-date-picker v-model="localProject.end" no-title scrollable>
                      <v-spacer></v-spacer>
                      <v-btn text color="primary" @click="calendar2menu = false">Cancel</v-btn>
                      <v-btn text color="primary" @click="calendar2menu = false">OK</v-btn>
                    </v-date-picker>
                  </v-menu>
                  <v-textarea
                    label="Projektbeschreibung"
                    prepend-icon="mdi-information-outline"
                    outlined
                    height="70"
                    class="ma-1"
                    v-model="localProject.description"
                  ></v-textarea>
                  <v-textarea
                    label="Definition of Ready"
                    prepend-icon="mdi-information-outline"
                    outlined
                    height="70"
                    class="ma-1"
                    v-model="localProject.dor"
                  ></v-textarea>
                  <v-textarea
                    label="Definition of Done"
                    prepend-icon="mdi-information-outline"
                    outlined
                    height="70"
                    class="ma-0"
                    v-model="localProject.dod"
                  ></v-textarea>
                  <v-select
                    :items="['User1', 'User2', 'User3', 'User4']"
                    label="Projekt Mitglieder*"
                    multiple
                    required
                    prepend-icon="mdi-account-multiple-plus"
                    v-model="localProject.project_users"
                  ></v-select>
                  <v-btn color="link" text @click="close()">Close</v-btn>
                  <v-btn color="link" text @click="confirm()">Save</v-btn>
                </v-card-text>
              </v-card>
            </v-tab-item>
            <v-tab-item>
              <v-card flat dark color="navbar" tile>
                <v-card-text>
                  <v-select
                    :items="['NW', 'PL', 'NS', 'DO', 'IP', 'AC']"
                    label="Status*"
                    required
                    prepend-icon="mdi-circle-edit-outline"
                    v-model="localProject.status"
                  ></v-select>
                  <span class="headline ma-4">Sprintinformationen</span>
                  <v-row>
                    <div class="ma-4">
                      <v-progress-circular
                        :rotate="-90"
                        :size="100"
                        :width="15"
                        :value="valueDetail"
                        color="link"
                      >{{ valueDetail }}</v-progress-circular>
                    </div>
                    <div class="ma-4">
                      <p>Sprints absolviert: 75</p>
                      <p>Sprints geplant: 100</p>
                      <p>Sprintlänge in Wochentagen: 20</p>
                      <p>nächster Sprintende: 13.07.20</p>
                      <p>nächster Sprintstart: 14.07.20</p>
                    </div>
                  </v-row>
                  <v-btn color="link" text @click="close()">Close</v-btn>
                  <v-btn color="link" text @click="confirm()">Save</v-btn>
                </v-card-text>
              </v-card>
            </v-tab-item>
          </v-tabs-items>
        </v-card>
      </v-container>
    </v-navigation-drawer>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
export default {
  name: "DetailProject",
  data: () => ({
    tab: null,
    calendar1menu: false,
    calendar2menu: false,

    valueDetail: 50,
    localProject: {}
  }),
  computed: {
    ...mapState({
      project: "detailProject"
    }),

    visible: {
      get: function() {
        return this.$store.state.detailProjectVisable;
      },
      set: function(newValue) {
        this.$store.state.detailProjectVisable = newValue;
      }
    }
  },

  created: function() {
    this.$store.commit("hideProjectDetail");
    this.localProject.name = this.project.name;
  },

  updated: function() {
    this.localProject = this.project;
  },

  methods: {
    close() {
      this.$store.commit("hideProjectDetail");
    },

    confirm() {
      this.close();
      this.saveProject();
    },

    ...mapActions("project", {
      updateProject: "update"
    }),

    saveProject() {
      this.updateProject({
        id: this.localProject.id + "/",
        data: {
          id: this.localProject.id,
          name: this.localProject.name,
          description: this.localProject.description,
          status: this.localProject.status,
          start: this.localProject.start,
          end: this.localProject.end,
          dor: this.localProject.dor,
          dod: this.localProject.dod
        }
      });
    }
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>