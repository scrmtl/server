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
            v-if="groupIds[0] !== 1"
            color="link"
            inset
            dark
            v-model="showAllProjects"
          >
            <template v-slot:label>
              <span class="link--text">Show all Projects</span>
            </template>
          </v-switch>
        </div>
      </v-col>
    </v-row>
    <v-row align="start" justify="center">
      <v-col lg="8" md="7" sm="12">
        <div v-for="project in sortedProjects" :key="project.id">
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
import MyTasksLane from "@/components/Lanes/MyTasksLane.vue";
import { mapGetters, mapActions } from "vuex";
import { mapFields } from "vuex-map-fields";

export default {
  data: () => ({
    dialog: false,
    calendar1menu: false,
    calendar2menu: false,
    drawer: false,
    tab: null,
    localProject: {},
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
    ...mapActions("sprint", {
      fetchSprints: "fetchList",
    }),

    loadData() {
      // Load Projects
      this.fetchProjects({ customUrlFnArgs: {} });
      //Load User Groups
      this.fetchGroups();
      this.fetchUsers();
      this.fetchSprints({ customUrlFnArgs: {} });
    },

    showCreateProject() {
      this.$store.commit("selected/showProjectDetail", true);
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
      return projects;
    },
  },
  computed: {
    ...mapFields({
      userId: "Userinfo.userId",
      groupIds: "Userinfo.groups",
    }),
    ...mapGetters("project", {
      listProjects: "list",
    }),
    ...mapGetters("user", {
      projectUsersByUserId: "byUserId",
    }),

    sortedProjects() {
      // show all project if you admin or you set it via switch
      if (this.showAllProjects || this.groupIds[0] === 1) {
        return this.orderProjects(this.listProjects);
      }
      // show only your own projects
      else {
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
    },
  },

  mounted() {
    this.loadData();
  },

  created() {
    this.loadData();
  },
};
</script>

<style lang="css">
@import "../main.css";
</style>
