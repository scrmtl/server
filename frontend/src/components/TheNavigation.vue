<template>
  <v-navigation-drawer
    v-model="visibleDrawer"
    left
    app
    temporary
    dark
    floating
  >
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="title">
          Scrum Tool
        </v-list-item-title>
        <v-list-item-subtitle>
          Dark, Easy, Cool
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
      <v-list-item disabled link >
        <v-list-item-icon>
          <v-icon>mdi-cards</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Planning Poker</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item 
        link 
        @click="plattformManagementDialog = true" 
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
      <PlattformUserManagement
        @close-dialog="plattformManagementDialog = false" 
        :dialog="plattformManagementDialog" 
        v-if="plattformManagementDialog"
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
import PlattformUserManagement from "@/components/PlattformUserManagement.vue";
import { mapGetters, mapActions, mapState } from "vuex";
export default {
  data: () => ({
    plattformManagementDialog: false,
    groupId: 0
  }),
  components: {
    PlattformUserManagement
  },
  methods:{
    logout() {
      this.$store.dispatch("logout").then(() => {
        this.$router.push("/login");
      });
    },
    GoHome(){
      this.$router.push({ name: 'Home' })
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