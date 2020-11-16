/* eslint-disable */
<template>
  <v-container fluid>
    <v-row class="hidden-sm-and-down">
      <v-col cols="12">
        <div class="projectBtn my-2">
          <v-btn text color="link" large @click="showCreateProject()">
            <v-icon class="mr-1">mdi-folder-plus</v-icon>Create Project
          </v-btn>
        </div>
        <div class="projectBtn my-n1">
          <v-switch
            v-if="this.groupId !== 1"
            color="link"
            inset
            dark
            v-model="showAllProjects"
          >
            <template v-slot:label>
              <span class="link_color">Show all Projects</span>
            </template>
          </v-switch>
        </div>
      </v-col>
    </v-row>
    <v-row align="start" justify="center">
      <v-col lg="8" md="7" sm="12">
        <div
          v-for="project in sortedProjects"
          :key="project.id"
        >
          <ProjectCard v-bind:project="project" />
        </div>
      </v-col>
      <v-col lg="4" md="5" class="hidden-sm-and-down">
        <MyTasksLane class="hidden-sm-and-down" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ProjectCard from "@/components/ProjectCard.vue";
import MyTasksLane from "@/components/MyTasksLane.vue";

import { mapGetters, mapActions, mapState } from "vuex";
//import scrmtlServices from '@/services/scrmtlServices.js'

export default {
  data: () => ({
    dialog: false,
    calendar1menu: false,
    calendar2menu: false,
    drawer: false,
    tab: null,
    localProject: {},
    groupId: 0,
    userId: {},
    showAllProjects: false,
  }),
  components: {
    ProjectCard,
    MyTasksLane,
  },

  

  methods: {
    ...mapActions("project", {
      fetchProjects: "fetchList",
      createProject: "create",
    }),
    ...mapActions("user", {
      fetchUsers: "fetchList",
    }),
    ...mapActions("group", {
      fetchGroups: "fetchList",
    }),
    ...mapActions("session", {
      fetchSession: "fetchList",
    }),

    loadData() {
      // Load Projects
      this.fetchProjects({ customUrlFnArgs: {} });
      //Load User Groups
      this.fetchGroups();
      this.fetchUsers();
      this.fetchSession({ customUrlFnArgs: { all: false } });
    },

    GetSessionIds() {
      this.groupId = -1;
      this.userId = -1;
      this.fetchSession({
        id: null,
        customUrlFnArgs: { all: false },
      })
        .then(() => {
          //get groupId
          var session = Object.values(this.listSession)[0];
          this.groupId = session.groups[0];
          this.userId = session.id;
        })
        .catch(() => {
          if (this.groupId <= 0) {
            this.groupId = 0;
            this.userId = 0;
          }
        });
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
          project_users: this.localProject.project_users,
        },
        customUrl: "/api/projects/",
      });
    },

    //Ordnet die Projekte nach dem Status (Ob Aktiv oder Archiv)
    orderProjects(projects) {
       projects.sort(function (a, b) {
        var keyA = a.status;
        var keyB = b.status;
        // Vergleiche ob AC oder AR
        if (keyA < keyB) return -1;
        if (keyA > keyB) return 1;
        return 0;
      });
      return projects
    },

    

    
  },
  computed: {
    ...mapState({
      project: "detailProject",
    }),
    ...mapGetters("project", {
      listProjects: "list" }),
    ...mapGetters("session", {
      listSession: "list",
    }),
    ...mapGetters("user", {
      projectUsersByUserId: "byUserId",
    }),
    ...mapGetters("group", {
      groupById: "byId",
    }),
    ...mapGetters({ userinfos: "getUserinfo" }),

    getGroupId: function () {
      if (this.groupId === 0) {
        this.GetSessionIds();
      }
      return this.groupId;
    },

    

    sortedProjects(){
      // show all project if you admin or you set it via switch
      if(this.showAllProjects || this.groupId === 1){
        console.log(this.listProjects)
        return this.orderProjects(this.listProjects);
      }
      // show only your own projects
      else{
        var userProjects = [];
        this.projectUsersByUserId(this.userId).forEach((projectUser) => {
          this.listProjects.forEach((project) => {
            if (project.id === projectUser.project) {
              userProjects.push(project);
            }
          });
        });
        return this.orderProjects(userProjects);
      }
    }
  },

  mounted() {
    this.loadData();
    this.GetSessionIds();
  },

  created() {
    this.loadData();
    this.GetSessionIds();
  },

};
</script>

<style lang="css" >
@import "../main.css";
</style>