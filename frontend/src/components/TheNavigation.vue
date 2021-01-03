<template>
  <v-navigation-drawer
    v-model="visibleDrawer"
    left
    app
    temporary
    dark
    floating
    color="tabbody"
  >
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="title">
          Scrum Tool
        </v-list-item-title>
        <v-list-item-subtitle>
          Dark, Cool, Easy
        </v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>

    <v-list nav>
      <v-list-item @click="GoHome()" link >
        <v-list-item-icon>
          <v-icon>mdi-home</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Home</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item @click="GoPoker()" link >
        <v-list-item-icon>
          <v-icon>mdi-cards</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Planning Poker</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item 
        link 
        @click="settingsDialog = true" 
        :disabled="getGroupId != 1"
        class="hidden-sm-and-down"
      >
        <v-list-item-icon>
          <v-icon>mdi-cog</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Settings</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <Settings
        @close-dialog="settingsDialog = false" 
        :dialog="settingsDialog"
      />
    </v-list>
    <template v-slot:append>
      <div class="pa-2">
        <v-btn block @click="logout()">
          <v-icon>mdi-logout</v-icon>
          Logout
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
import Settings from "@/components/settings/Settings.vue";
import { mapGetters, mapActions, mapState } from "vuex";
export default {
  data: () => ({
    settingsDialog: false,
    groupId: 0
  }),
  components: {
    Settings
  },
  methods:{
    logout() {
      this.$store.dispatch("logout").then(() => {
        this.$router.push("/login");
      });
    },
    GoHome(){
      if(this.$router.history.current.name !== "Home"){
        this.$router.push({ name: 'Home' })
      }
    },
    GoPoker(){
      if(this.$router.history.current.name !== "PlanningPoker"){
        this.$router.push({ name: 'PlanningPoker' })
      }
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
  computed:{
    visibleDrawer: {
      get() {
        return this.navigation.visable;
      },
      set(newValue) {
        if (newValue) {
          this.$store.commit("showNavigation");
        } else {
          this.$store.commit("hideNavigation");
        }
      }
    },
    ...mapState(["navigation"]),
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
    },
  },
  mounted() {
    this.listSession;
  }
}
</script>

<style lang="css">
  @import "../main.css";
</style>