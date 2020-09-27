<template>
  <v-app-bar color="appbar" app dark dense flat>
    <v-btn icon text color="appbar" :to="{ name: 'Home' }">
      <v-icon large color="link">mdi-home</v-icon>
    </v-btn>

    <v-toolbar-title class="link--text">ScrumTool</v-toolbar-title>

    <v-btn color="link" text x-small dark @click.stop="dialog = true"
      >Benutzerverwaltung</v-btn
    >
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
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      dialog: false
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

    initialize() {
      this.listSession();
    }
  },

  computed: {
    ...mapGetters("session", {
      listSession: "list"
    }),
    ...mapGetters({ userinfos: "getUserinfo" })
  },
  mounted() {
    this.listSession;
  }
};
</script>

<style lang="css">
@import "../main.css";
</style>