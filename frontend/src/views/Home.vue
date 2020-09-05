/* eslint-disable */
<template>
  <v-content class="tabbody tab-content">
    <v-row>
      <div class="projectBtn">
        <div class="my-2">
           <v-navigation-drawer
              v-model="drawer"
              absolute
              temporary
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
                  <v-tab
                  >
                    Details
                  </v-tab>
                  <v-tab
                  >
                    Info
                  </v-tab>
                </v-tabs>

                <v-tabs-items
                v-model="tab" 
                background-color="navbar"
                color="navbar"
                >
                  <v-tab-item
                  >
                    <v-card flat dark color="navbar" tile>
                      <v-card-text>
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
                        <v-btn color="link" text @click="drawer = false">Close</v-btn>
                        <v-btn color="link" text @click="drawer = false">Save</v-btn>
                      </v-card-text>
                    </v-card>
                  </v-tab-item>
                  <v-tab-item
                  >
                    <v-card flat dark color="navbar" tile>
                      <v-card-text>
                          <v-select
                            :items="['Nicht gestartet', 'Läuft', 'Überzogen', 'Beendet']"
                            label="Status*"
                            required
                            prepend-icon="mdi-circle-edit-outline"
                          ></v-select>
                          <v-btn color="link" text @click="drawer = false">Close</v-btn>
                        <v-btn color="link" text @click="drawer = false">Save</v-btn>
                        </v-card-text>
                    </v-card>
                  </v-tab-item>
                </v-tabs-items>
              </v-card>
              </v-container>
            </v-navigation-drawer>
          <v-btn 
          text
          color="link" 
          large 
          @click.stop="drawer = !drawer">
            <v-icon class="mr-1">mdi-folder-plus</v-icon>Projekt erstellen
          </v-btn>
          <v-btn 
          text 
          large 
          color="link"
          >
            <v-icon class="mr-1">mdi-delete-forever</v-icon>
            Projekt(e) löschen
          </v-btn>
        </div>
      </div>
    </v-row>
    <v-row>
      <v-col
      cols="12"
      sm="6"
      md="8">
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
      <v-col
      cols="6"
      md="4">
        <v-container>
          <MyTasksLane/>
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
    dialog: false,
    drawer: null,
    tab: null,
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
    this.ProjectsFetch();
    //Load user's tasks
  },
  methods: {
    ...mapActions("project", {
      ProjectsFetch: "fetchList"
    }),
    ...mapActions("user", {
      UsersFetch: "fetchList"
    }),
    loadData() {
      this.ProjectsFetch()
      this.UsersFetch();
    } 
  },
  computed:{
    ...mapGetters("project", 
    {listProjects: "list"
    })
  },
  mounted() {
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