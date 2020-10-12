/* eslint-disable */
<template>
  <v-app>
    <SystemBar v-if="this.$store.getters.isLoggedIn" />
    <DetailProject v-if="this.$store.getters.isLoggedIn" />
    <DetailTask v-if="this.$store.getters.isLoggedIn" />
    <!-- v-main is necessary. Do not use v-content -->
    <v-main class="tabbody">
      <router-view />
      <v-snackbar
        v-model="errorMessage.visible"
        timeout="-1"
      >
      {{ errorMessage.message }}

      <template v-slot:action="{ attrs }">
        <v-btn
          color="error"
          text
          v-bind="attrs"
          @click="close()"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
    </v-main>

    <v-footer color="appbar" class="white--text" app>
      <span>dark, cool, easy</span>
      <v-spacer></v-spacer>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
import SystemBar from "@/components/TheSystemBar.vue";
import DetailProject from "@/components/TheDetailProject.vue";
import DetailTask from "@/components/TheDetailTask.vue";
import Axios from "axios";
import { mapState } from "vuex";
export default {
  name: "App",
  data: () => ({
    //
  }),
  components: {
    SystemBar,
    DetailProject,
    DetailTask
  },

  methods: {
    close() {
      this.$store.commit("hideErrorView");
    },
  },

  computed:{
    ...mapState(["errorMessage"]),
  },
  created() {
    Axios.interceptors.response.use(undefined, function(err) {
      return new Promise(() => {
        if (err.status === 401 && err.detail === "Anmeldedaten fehlen") {
          this.$store.dispatch("logout");
        }
        throw err;
      });
    });
  }
};
</script>

<style lang="css" >
@import "/main.css";
</style>
