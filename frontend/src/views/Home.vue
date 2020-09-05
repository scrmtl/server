/* eslint-disable */
<template>
  <v-content class="tabbody tab-content">
    <v-row>
      <div class="projectBtn">
        <div class="my-2">
          <v-navigation-drawer
            v-model="drawer"
            absolute
            right
            width="800"
            color="navbar"
            dark
          >
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
                        <v-btn color="link" text @click="drawer = false">Close</v-btn>
                        <v-btn color="link" text @click="saveProject()">Save</v-btn>
                      </v-card-text>
                    </v-card>
                  </v-tab-item>
                  <v-tab-item>
                    <v-card flat dark color="navbar" tile>
                      <v-card-text>
                        <v-select
                          :items="['Nicht gestartet', 'Läuft', 'Überzogen', 'Beendet']"
                          label="Status*"
                          required
                          prepend-icon="mdi-circle-edit-outline"
                        ></v-select>
                        <v-btn color="link" text @click="drawer = false">Close</v-btn>
                        <v-btn color="link" text @click="saveProject()">Save</v-btn>
                      </v-card-text>
                    </v-card>
                  </v-tab-item>
                </v-tabs-items>
              </v-card>
            </v-container>
          </v-navigation-drawer>
          <v-btn text color="link" large @click.stop="drawer = !drawer">
            <v-icon class="mr-1">mdi-folder-plus</v-icon>Projekt erstellen
          </v-btn>
        </div>
      </div>
    </v-row>
    <v-row>
      <v-col cols="12" sm="6" md="8">
        <v-container fluid>
          <v-layout>
            <v-flex>
              <div v-for="project in listProjects" :key="project.id">
                <ProjectCard v-bind:project="project" />
              </div>
            </v-flex>
          </v-layout>
          <DetailView></DetailView>
        </v-container>
      </v-col>
      <v-col
      cols="2"
      md="4"
      sm="2"
      class="pr-2"
      >
      <v-flex>
        <v-container>
          <MyTasksLane />
        </v-container>
      </v-flex>
      </v-col>
    </v-row>
  </v-content>
</template>

<script>
import ProjectCard from "@/components/ProjectCard.vue";
import MyTasksLane from "@/components/MyTasksLane.vue";
import DetailView from "../components/DetailView";
import { mapGetters, mapActions, mapState } from "vuex";
import Axios from "axios";
//import scrmtlServices from '@/services/scrmtlServices.js'

export default {
  data: () => ({
    dialog: false,
    calendar1menu: false,
    calendar2menu: false,
    drawer: false,
    tab: null,
    localProject: {}
  }),
  components: {
    ProjectCard,
    MyTasksLane,
    DetailView
  },
  async created() {
    if (!this.$store.getters.getToken) {
      this.$router.push("/login");
    }
    // Load Projects
    this.ProjectsFetch();
    //Load user's tasks

    // set auth header
      Axios.defaults.headers.common["Authorization"] = `Bearer ${this.$store.getters.getToken}`
  },

  methods: {
    ...mapActions("project", {
      ProjectsFetch: "fetchList",
      createProject: "create"
    }),
    ...mapActions("user", {
      UsersFetch: "fetchList"
    }),

    loadData: function() {
      this.ProjectsFetch();
      this.UsersFetch();
    },

    saveProject() {
      this.drawer = false;
      this.createProject({
        data: {
          name: this.localProject.name,
          description: this.localProject.description,
          start: this.localProject.start,
          end: this.localProject.end,
          sprint_duration: this.localProject.sprint_duration,
          dor: this.localProject.dor,
          dod: this.localProject.dod,
          numOfSprints: this.localProject.numOfSprints,
          status: this.localProject.status,
          project_users: this.localProject.project_users
        },
        customUrl: "/api/projects/"
      });
    }
  },
  computed: {
    ...mapGetters("project", { listProjects: "list" }),

    ...mapState({
      project: "detailProject"
    })
  },
  mounted() {
    this.loadData();
    setInterval(
      function() {
        this.loadData();
      }.bind(this),
      10000
    );
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>