/* eslint-disable */
<template>
  <v-content class="tabbody tab-content">
    <v-row>
      <div class="projectBtn">
        <div class="my-2">
          <v-btn text color="link" large @click="showCreateProject()">
            <v-icon class="mr-1">mdi-folder-plus</v-icon>Create Project
          </v-btn>
          <DetailProject />
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
      <v-col cols="2" md="4" sm="2" class="pr-2">
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
import DetailView from "@/components/DetailView";
import DetailProject from "@/components/DetailProject.vue";
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
    localProject: {},
    
  }),
  components: {
    ProjectCard,
    MyTasksLane,
    DetailView,
    DetailProject
  },
  beforeCreate(){
    // safe home route
    if (!this.$store.getters.getToken) {
      this.$router.push("/login");
    }
    else{
      // set auth header
      Axios.defaults.headers.common["Authorization"] = `Bearer ${this.$store.getters.getToken}`;
    }
  },
  created() {
    
    this.loadData();
    Axios.interceptors.request.use(config => {
      if (
        config.method === "post" &&
        config.url[config.url.length - 1] !== "/"
      ) {
        config.url += "/";
      }
      return config;
    });
  },

  methods: {
    ...mapActions("project", {
      ProjectsFetch: "fetchList",
      createProject: "create"
    }),
    ...mapActions("user", {
      UsersFetch: "fetchList"
    }),
    ...mapActions("group", {
      GroupsFetch: "fetchList"
    }),
    ...mapActions("session", {
      SessionFetch: "fetchList"
    }),
    

    loadData() {
      // Load Projects
      this.ProjectsFetch();
      //Load User Groups
      this.GroupsFetch();
      this.UsersFetch();
      this.SessionFetch({ customUrlFnArgs: {all: false}});
    },
    showCreateProject(){
      this.$store.commit("showProjectDetail", true);
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
    // setInterval(
    //   function() {
    //     this.loadData();
    //   }.bind(this),
    //   15000
    // );
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>