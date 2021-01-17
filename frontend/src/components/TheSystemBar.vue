<template>
  <v-app-bar
    color="appbar"
    app
    dark
    prominent
    dense
    :shrink-on-scroll="this.$route.params.id === undefined"
  >
    <v-container fluid>
      <v-row>
        <v-app-bar-nav-icon class="mt-n3"
          @click="showNavigation()"
        ></v-app-bar-nav-icon>
        <v-toolbar-title class="mt-n3">Scrum Tool</v-toolbar-title>      
        <v-spacer></v-spacer>
        <span class="hidden-sm-and-down text-subtitle-1" v-if="this.$route.params.id !== undefined">{{RoutedProjectName}}</span>
        <v-spacer></v-spacer>
        <v-btn
          class="mt-n1"
          dense
          text
          >
          <v-icon>mdi-account</v-icon>
          {{ userinfos.username }}
        </v-btn>

        <v-btn class="mt-n3" icon @click="logoutDialog = true">
          <v-tooltip bottom color="link">
            <template v-slot:activator="{ on, attrs }">
              <v-icon
                color="link"
                v-bind="attrs"
                v-on="on"
              >mdi-logout</v-icon>
            </template>
            <span>Logout</span>
          </v-tooltip>
        </v-btn>
        
      </v-row>
      <v-row>
        <v-tabs v-if="this.$route.params.id !== undefined" background-color="transparent" slider-color="link"
        dark centered grow show-arrows center-active v-model="activeTab">
          <v-tab v-for="tab in tabs" :key="tab.id" :to="tab.route" exact>{{ tab.name }}</v-tab>     
        </v-tabs>
      </v-row>
    </v-container>
    <!-- Delete Dialog -->
    <v-dialog
      v-model="logoutDialog"
      persistent
      class="mx-auto"
      width="600"
      dark
    >
      <v-card color="tabbody" shaped>
        <v-card-text class="headline pt-10">
          <span class="ml-12">Do you really want to logout?</span>
        </v-card-text>
        <v-card-actions class="ml-10 pb-10 pt-10">
          <v-btn width="250" outlined color="error" @click="logout()"
            >Yes</v-btn
          >
          <v-btn
            width="250"
            outlined
            @click="logoutDialog = false"
            >No</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app-bar>
</template>

<script>
import { mapGetters, mapActions, mapState } from "vuex";



export default {
  name: "TheSystemBar",
  data() {
    return {
      activeTab: `/project/${this.$route.params.id}`,
      logoutDialog: false,
    } 
  },
  components: {
  },
  methods: {
    closeAlert() {
      this.$store.commit("hideSystemAlert");
    },
    showNavigation() {
      this.$store.commit("showNavigation");
    },

    logout() {
      this.$store.dispatch("logout").then(() => {
        this.$router.push("/login");
      });
    },
    ...mapActions("session", {
      fetchSession: "fetchList"
    }),
  },

  computed: {
    ...mapState(["selectedProject"]),
    ...mapState(["systemAlert"]),
    ...mapGetters("session", {
      listSession: "list"
    }),
    ...mapGetters({ userinfos: "getUserinfo" }),
    ...mapGetters("project",{
      projectById: "byId"
    }),

    RoutedProjectName (){
      if(this.$route.params.id !== undefined){
        var project = this.projectById(this.$route.params.id)
        if( project !== undefined){
          if(project.name.length > 30){
            return project.name.slice(0, 30) +"..." ;
          }
          else{
            return project.name
          }
          
        }
        else{
          return "";
        }
      }
      else{
        return "";
      }
    },
    tabs(){
      return [
        { id: 1, name: "Dashboard", route: `/project/${this.$route.params.id}` },
        { id: 2, name: "Product Backlog", route: `/project/${this.$route.params.id}/ProductBacklog` },
        { id: 3, name: "Sprint Planing", route: `/project/${this.$route.params.id}/SprintPlaning` },
        { id: 4, name: "Sprint Backlog", route: `/project/${this.$route.params.id}/SprintBacklog` },
        { id: 5, name: "Archive", route: `/project/${this.$route.params.id}/Archive` },
        { id: 6, name: "Statistic", route: `/project/${this.$route.params.id}/Statistic`},
        
      ]
    }
  },
  mounted() {
    
  },
  updated(){
    
  }
};
</script>

<style lang="css">
  @import "../main.css";
</style>