<template>
  
  <v-app-bar color="appbar" app dark prominent dense :shrink-on-scroll="this.$route.params.id === undefined">
    <v-container fluid>
      <v-row>
        <v-btn class="mt-n3" icon color="appbar" :to="{ name: 'Home' }">
          <v-icon large color="link">mdi-home</v-icon>
        </v-btn>
        <span class="mt-n1 mx-2 ">Scrum Tool</span>
        
        
        <v-btn
          color="link"
          text
          class="mt-1"
          x-small
          dark
          @click="plattformManagementDialog = true"
          v-if="getGroupId == 1"
          > Plattform User Management
        </v-btn>
        <PlattformUserManagement  @close-dialog="plattformManagementDialog = false" :dialog="plattformManagementDialog" v-if="plattformManagementDialog" />
        <v-spacer></v-spacer>

        <v-btn
          class="mt-n1"
          dense
          text
          >
          <v-icon>mdi-account</v-icon>
          {{ userinfos.username }}
        </v-btn>

        <v-btn class="mt-n3" icon @click="logout()">
          <v-tooltip bottom color="link">
            <template v-slot:activator="{ on, attrs }">
              <v-icon
                color="link"
                v-bind="attrs"
                v-on="on"
                >mdi-logout</v-icon
              >
            </template>
            <span>Logout</span>
          </v-tooltip>
        </v-btn>
        
      </v-row>
      <v-row >
        <v-tabs v-if="this.$route.params.id !== undefined" background-color="transparent" slider-color="link"
        dark centered grow v-model="activeTab">
          <v-tab v-for="tab in tabs" :key="tab.id" :to="tab.route" exact>{{ tab.name }}</v-tab>     
        </v-tabs>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script>
import PlattformUserManagement from "@/components/PlattformUserManagement.vue";
import { mapGetters, mapActions, mapState } from "vuex";

export default {
  data() {
    return {
      plattformManagementDialog: false,
      groupId: 0,
      activeTab: `/project/${this.$route.params.id}`,
      tabs: [
        { id: 1, name: "Dashboard", route: `/project/${this.$route.params.id}` },
        { id: 2, name: "Product Backlog", route: `/project/${this.$route.params.id}/ProductBacklog` },
        { id: 3, name: "Sprint Planing", route: `/project/${this.$route.params.id}/SprintPlaning` },
        { id: 4, name: "Sprint Backlog", route: `/project/${this.$route.params.id}/SprintBacklog` },
        { id: 5, name: "Archive", route: `/project/${this.$route.params.id}/Archive` },
        { id: 6, name: "Statistic", route: `/project/${this.$route.params.id}/Statistic`},
        
      ]
    };
  },
  components: {
    PlattformUserManagement
  },
  methods: {
    logout() {
      this.$store.dispatch("logout").then(() => {
        this.$router.push("/login");
      });
    },
    ...mapActions("session", {
      fetchSession: "fetchList"
    }),
    fetchGroupId() {
      this.groupId = -1;
      this.fetchSession({
        id: null,
        customUrlFnArgs: { all: false }
      })
        .then(() => {
          //get groupId
          var session = Object.values(this.listSession)[0];
          this.groupId = session.groups[0];
        })
        .catch(() => {
          if (this.groupId <= 0) {
            this.groupId = 0;
          }
        });
    }
  },

  computed: {
    ...mapState(["selectedProject"]),
    ...mapGetters("session", {
      listSession: "list"
    }),
    ...mapGetters("group", {
      groupById: "byId"
    }),
    ...mapGetters({ userinfos: "getUserinfo" }),
    getGroupId: function() {
      if (this.groupId === 0) {
        this.fetchGroupId();
      }
      return this.groupId;
    }
  },
  mounted() {
    this.listSession;
    
  },
  updated(){
    
  }
};
</script>

<style lang="css">
@import "../main.css";
</style>