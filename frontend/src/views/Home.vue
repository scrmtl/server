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
        <div class="projectBtn my-2">
          <v-switch
            v-if="this.groupId !== 1"
            color="link"
            inset
            dark
            @click.stop="orderedProjects()"
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
          v-for="project in orderedProjects(
            listProjects,
            this.groupId,
            projectUsers(this.userId)
          )"
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

  beforeCreate() {},

  created() {
    this.loadData();

    this.fetchGroupId();
  },

  methods: {
    ...mapActions("project", {
      ProjectsFetch: "fetchList",
      createProject: "create",
    }),
    ...mapActions("user", {
      UsersFetch: "fetchList",
    }),
    ...mapActions("group", {
      GroupsFetch: "fetchList",
    }),
    ...mapActions("session", {
      SessionFetch: "fetchList",
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
          project_users: this.localProject.project_users,
        },
        customUrl: "/api/projects/",
      });
    },

    orderedProjects(projects, groupId, projectUsers) {
      //Wenn der User-Status 1 ist, dann ist der User Admin
      //Den Tooglebutton sieht der Admin nicht, deswegen die Abfrage nach Variable
      if (groupId === 1 || this.showAllProjects === true) {
        return this.orderProjects(projects);
      }
      //Bei -1 fetchen wir uns die ID nochmal... Kann vielleicht in Zukunft mal raus
      else if (groupId === -1) {
        this.fetchGroupId();
        groupId = this.groupId;
      } else {
        //Filtert die Liste von Projekt_usern zu der einen User id (siehe HTML-Code)
        //und packt dann die Projekte des Users in das Result array
        var user_projects = [];
        projectUsers.forEach((projectUser) => {
          projects.forEach((element) => {
            if (element.id === projectUser.project) {
              user_projects.push(element);
            }
          });
        });
        return this.orderProjects(user_projects);
      }
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
      return projects;
    },

    ...mapActions("session", {
      fetchSession: "fetchList",
    }),

    fetchGroupId() {
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
  },
  computed: {
    ...mapGetters("project", { listProjects: "list" }),
    ...mapGetters("session", {
      listSession: "list",
    }),
    ...mapGetters("user", {
      projectUsers: "byUserId",
    }),

    ...mapGetters("group", {
      groupById: "byId",
    }),
    ...mapGetters({ userinfos: "getUserinfo" }),
    getGroupId: function () {
      if (this.groupId === 0) {
        this.fetchGroupId();
      }
      return this.groupId;
    },

    ...mapState({
      project: "detailProject",
    }),
  },
  mounted() {
    this.loadData();
    // setInterval(
    //   function() {
    //     this.loadData();
    //   }.bind(this),
    //   15000
    // );
  },
};
</script>

<style lang="css" >
@import "../main.css";
</style>