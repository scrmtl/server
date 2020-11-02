/* eslint-disable */
<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <div class="projectBtn my-2">
          <v-btn text color="link" large @click="showCreateProject()">
            <v-icon class="mr-1">mdi-folder-plus</v-icon>Create Project
          </v-btn>
        </div>
      </v-col>
    </v-row>
    <v-row align="start" justify="center">
      <v-col cols="8">
        <div v-for="project in orderedProjects(listProjects)" :key="project.id">
          <ProjectCard v-bind:project="project" />
        </div>
      </v-col>
      <v-col cols="4">
        <MyTasksLane />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ProjectCard from "@/components/ProjectCard.vue";
import MyTasksLane from "@/components/MyTasksLane.vue";
import Axios from "axios";

import { mapGetters, mapActions, mapState } from "vuex";
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
    MyTasksLane
  },
  beforeCreate() {},
  created() {
    this.loadData();
    Axios.interceptors.request.use(config => {
      if (
        (config.method === "post") | (config.method === "patch") &&
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
      this.ProjectsFetch({ customUrlFnArgs: {} });
      //Load User Groups
      this.GroupsFetch();
      this.UsersFetch();
      this.SessionFetch({ customUrlFnArgs: { all: false } });
    },
    showCreateProject() {
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
    },

    orderedProjects(projects) {
      projects.sort(function(a, b) {
        var keyA = a.status;
        var keyB = b.status;
        // Vergleiche ob AC oder AR 
        if (keyA < keyB) return -1;
        if (keyA > keyB) return 1;
        return 0;
      });
      return projects;
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

<style lang="css" >
@import "../main.css";
</style>