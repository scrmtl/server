<template>
  <v-app-bar color="appbar" app dark dense flat>
    <v-btn icon text color="appbar" :to="{ name: 'Home' }">
      <v-icon large color="link">mdi-home</v-icon>
    </v-btn>

    <v-toolbar-title class="link--text">ScrumTool</v-toolbar-title>

    <v-btn
      color="link"
      text
      x-small
      dark
      @click.stop="dialog = true"
      v-if="getGroupId == 1"
      >Benutzerverwaltung
    </v-btn>
    <PlattformUserManagement v-model="dialog" v-if="dialog" />

    <v-spacer></v-spacer>
    <v-icon class="systemBarIcon">mdi-account</v-icon>
    <span class="systemBarUser">{{ userinfos.username }}</span>
    <v-btn icon text @click="logout()">
      <v-tooltip bottom color="link">
        <template v-slot:activator="{ on, attrs }">
          <v-icon
            class="task-status-icons"
            color="link"
            v-bind="attrs"
            v-on="on"
            >mdi-logout</v-icon
          >
        </template>
        <span>Logout</span>
      </v-tooltip>
    </v-btn>
  </v-app-bar>
</template>

<script>
import PlattformUserManagement from "@/components/PlattformUserManagement.vue";
import { mapGetters, mapActions } from "vuex";

export default {
  data() {
    return {
      dialog: false,
      groupId: 0
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
  }
};
</script>

<style lang="css">
@import "../main.css";
</style>