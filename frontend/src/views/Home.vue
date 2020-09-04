/* eslint-disable */
<template>
  <v-content class="tabbody tab-content">
    <v-row>
      <div class="projectBtn">
        <div class="my-2">
          <v-dialog
            v-model="dialog"
            persistent
            max-width="400px"
            content-class="createProjectDialog"
            hide-overlay
            scrollable
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn text large color="link" v-bind="attrs" v-on="on">
                <v-icon class="mr-1">mdi-folder-plus</v-icon>Projekt erstellen
              </v-btn>
            </template>
            <v-card color="navbar" dark>
              <v-card-title>
                <span class="headline ma-0 pa-1">Projekterstellung</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-text-field
                    label="Projektname*"
                    required
                    prepend-icon="mdi-information-outline"
                    class="ma-1"
                  ></v-text-field>
                  <v-text-field
                    label="Projekt Start*"
                    hint="DD/MM/JJJJ"
                    required
                    persistent-hint
                    prepend-icon="mdi-calendar-range"
                    class="ma-1"
                  ></v-text-field>
                  <v-text-field
                    label="Projekt Ende*"
                    hint="DD/MM/JJJJ"
                    persistent-hint
                    required
                    prepend-icon="mdi-calendar-range"
                    class="mb-6 mt-1 ml-1 mr-1"
                  ></v-text-field>
                  <v-textarea
                    label="Projektbeschreibung"
                    prepend-icon="mdi-information-outline"
                    outlined
                    height="70"
                    class="ma-1"
                  ></v-textarea>
                  <v-textarea
                    label="Definition of Ready"
                    prepend-icon="mdi-information-outline"
                    outlined
                    height="70"
                    class="ma-1"
                  ></v-textarea>
                  <v-textarea
                    label="Definition of Done"
                    prepend-icon="mdi-information-outline"
                    outlined
                    height="70"
                    class="ma-0"
                  ></v-textarea>
                  <v-select
                    :items="['User1', 'User2', 'User3', 'User4']"
                    label="Projekt Mitglieder*"
                    multiple
                    required
                    prepend-icon="mdi-account-multiple-plus"
                  ></v-select>
                  <v-select
                    :items="['Nicht gestartet', 'Läuft', 'Überzogen', 'Beendet']"
                    label="Status*"
                    required
                    prepend-icon="mdi-circle-edit-outline"
                  ></v-select>
                  <small>*müssen ausgefüllt sein</small>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="link" text @click="dialog = false">Close</v-btn>
                <v-btn color="link" text @click="dialog = false">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <v-btn text large color="link">
            <v-icon class="mr-1">mdi-delete-forever</v-icon>Projekt(e) löschen
          </v-btn>
        </div>
      </div>
    </v-row>
    <v-row>
      <v-col cols="10" md="10" class="v-col">
        <v-container fluid>
          <v-layout>
            <v-flex>
              <div v-for="project in listProjects" :key="project.id">
                <ProjectCard v-bind:project="project" />
              </div>
            </v-flex>
          </v-layout>
        </v-container>
      </v-col>
      <v-col cols="2" md="2">
        <v-container>
          <MyTasksLane />
        </v-container>
      </v-col>
    </v-row>
  </v-content>
</template>

<script>
import ProjectCard from "@/components/ProjectCard.vue";
import MyTasksLane from "@/components/MyTasksLane.vue";
import {mapGetters, mapActions} from "vuex";
//import scrmtlServices from '@/services/scrmtlServices.js'

export default {
  data: () => ({
    dialog: false
  }),
  components: {
    ProjectCard,
    MyTasksLane
  },
  async created() {
    if (!this.$store.getters.getToken) {
      this.$router.push("/login");
    }
    // Load Projects
    this.fetchProjects();
    //Load user's tasks
  },
  methods: {
    ...mapActions("project", {
      fetchProjects: "fetchList"
    }),
    loadData: function() {
      this.fetchProjects();
    }
  },
  computed:{
    ...mapGetters("project", 
    {listProjects: "list"
    })
  },
  mounted: function() {
    console.log(this.listProjects);
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