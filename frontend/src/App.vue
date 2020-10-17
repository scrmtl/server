/* eslint-disable */
<template>
  <v-app>
    <SystemBar v-if="this.$store.getters.isLoggedIn" />
    <DetailProject v-if="this.$store.getters.isLoggedIn" />
    <DetailTask v-if="this.$store.getters.isLoggedIn" />
    <!-- v-main is necessary. Do not use v-content -->
    <v-main class="tabbody">
      <router-view />
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
export default {
  name: "App",
  data: () => ({
    //
  }),
  components: {
    SystemBar,
    DetailProject,
    DetailTask,
  },

  methods: {
    
  },

  computed:{
    
  },
  created() {
    Axios.interceptors.response.use(function(response) {
      if (response.status === 401 && response.detail === "Anmeldedaten fehlen") {
          this.$store.dispatch("logout");
      }
      // return new Promise(() => {
      //   if (err.status === 401 && err.detail === "Anmeldedaten fehlen") {
      //     this.$store.dispatch("logout");
      //   }
      //   throw err;
      // });
      return response;
    });
  }
};
</script>

<style lang="css" >
@import "/main.css";
</style>
